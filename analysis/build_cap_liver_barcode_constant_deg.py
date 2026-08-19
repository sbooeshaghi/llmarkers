"""Barcode-constant variant of the CAP liver local/global comparison.

The published all-cell analysis groups cells by the study's own all-cell
labels, which disagree with the myeloid labels for 16% of the myeloid cells.
This variant instead defines each target group in the all-cell matrix by the
exact barcodes that carry the corresponding myeloid label, so target
membership is identical between the two analyses and only the background
cells change. One-vs-rest scoring reuses the builder's functions unchanged.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / "analysis" / "artifacts" / "cap_liver_barcode_constant_recovery.tsv"
SUMMARY_PATH = REPO_ROOT / "analysis" / "artifacts" / "cap_liver_local_global_deg_summary.tsv"

spec = importlib.util.spec_from_file_location(
    "build_cap_liver_local_global_deg",
    REPO_ROOT / "analysis" / "build_cap_liver_local_global_deg.py",
)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def main() -> None:
    records = builder.marker_records()

    print("Loading myeloid obs (labels only)")
    myeloid = ad.read_h5ad(builder.MYELOID_PATH, backed="r")
    myeloid_labels = myeloid.obs[builder.LABEL_COL].astype(str)
    myeloid_barcode_label = dict(zip(myeloid.obs_names, myeloid_labels))
    myeloid.file.close()

    print("Loading all-cell AnnData")
    all_adata, all_x, all_obs, gene_ids, _ = builder.load_expression(builder.ALL_CELLS_PATH)

    labels = pd.Series(
        [myeloid_barcode_label.get(barcode, "__rest__") for barcode in all_obs.index],
        index=all_obs.index,
    )
    local_labels = list(builder.LOCAL_TO_GLOBAL_LABEL)
    print(f"Computing barcode-constant one-vs-rest rankings for {len(local_labels)} labels")
    de = builder.compute_one_vs_rest(all_x, labels, local_labels, gene_ids)
    all_adata.file.close()

    gene_universe = set(gene_ids)
    reference = pd.read_csv(SUMMARY_PATH, sep="\t").set_index("local_label")

    rows = []
    for local_label in local_labels:
        reported, _ = builder.reported_marker_set(records, "1440", local_label)
        reported = {gene for gene in reported if gene in gene_universe}
        top100 = de[local_label]["top_sets"][100]
        rows.append(
            {
                "local_label": local_label,
                "global_label": builder.LOCAL_TO_GLOBAL_LABEL[local_label],
                "n_cells_target": de[local_label]["n_cells"],
                "n_reported_markers": len(reported),
                "recovery_top100_barcode_constant": len(reported & top100) / len(reported),
                "recovery_top100_local": reference.loc[local_label, "local_reported_recovery_top100"],
                "recovery_top100_global_label_based": reference.loc[
                    local_label, "global_recovery_of_local_reported_top100"
                ],
            }
        )

    df = pd.DataFrame(rows)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, sep="\t", index=False)
    print(df.to_string(index=False))
    means = df[
        [
            "recovery_top100_local",
            "recovery_top100_barcode_constant",
            "recovery_top100_global_label_based",
        ]
    ].mean()
    print("\nMeans:")
    print(means.to_string())
    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
