"""Verify the nesting of the CAP liver myeloid file inside the all-cell file.

Writes a long-format artifact recording the facts the paper states about the
two CAP AnnData files: cell counts, distinct author labels, barcode overlap,
and agreement between each myeloid cell's mapped broad label and the label it
carries in the all-cell analysis.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import anndata as ad
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / "analysis" / "artifacts" / "cap_liver_nesting_check.tsv"

spec = importlib.util.spec_from_file_location(
    "build_cap_liver_local_global_deg",
    REPO_ROOT / "analysis" / "build_cap_liver_local_global_deg.py",
)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def main() -> None:
    myeloid = ad.read_h5ad(builder.MYELOID_PATH, backed="r")
    all_cells = ad.read_h5ad(builder.ALL_CELLS_PATH, backed="r")

    myeloid_labels = myeloid.obs[builder.LABEL_COL].astype(str)
    all_labels = all_cells.obs[builder.LABEL_COL].astype(str)

    shared = myeloid.obs_names.intersection(all_cells.obs_names)
    rows = [
        ("myeloid_file", builder.MYELOID_PATH.name),
        ("all_cells_file", builder.ALL_CELLS_PATH.name),
        ("n_cells_myeloid", myeloid.n_obs),
        ("n_cells_all", all_cells.n_obs),
        ("n_distinct_labels_myeloid", myeloid_labels.nunique()),
        ("n_distinct_labels_all", all_labels.nunique()),
        ("n_barcodes_shared", len(shared)),
        ("n_myeloid_barcodes_missing_from_all", myeloid.n_obs - len(shared)),
    ]

    # Label agreement: does each myeloid cell carry its mapped broad label in
    # the all-cell analysis?
    all_label_by_barcode = all_labels.reindex(myeloid.obs_names)
    mapped = myeloid_labels.map(builder.LOCAL_TO_GLOBAL_LABEL)
    agree = (all_label_by_barcode.values == mapped.values)
    rows.append(("n_myeloid_cells_with_mapped_label_in_all", int(agree.sum())))
    rows.append(("fraction_mapped_label_agreement", round(float(agree.mean()), 4)))

    for local_label in builder.LOCAL_TO_GLOBAL_LABEL:
        mask = myeloid_labels.eq(local_label).to_numpy()
        rows.append(
            (
                f"fraction_mapped_label_agreement__{local_label}",
                round(float(agree[mask].mean()), 4),
            )
        )

    myeloid.file.close()
    all_cells.file.close()

    df = pd.DataFrame(rows, columns=["metric", "value"])
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, sep="\t", index=False)
    print(df.to_string(index=False))
    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
