from __future__ import annotations

from pathlib import Path

import pandas as pd

from cross_study_gene_space import (
    build_gene_name_map,
    ids_to_names,
    normalize_text,
    standardize_marker_records,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "analysis" / "results"

MARKER_RECORDS_PATH = RESULTS_DIR / "cross_study_marker_records.tsv"
PROGRAM_PROFILE_OUT = RESULTS_DIR / "tcell_program_profiles.tsv"
PROGRAM_SUMMARY_OUT = RESULTS_DIR / "tcell_program_summary.tsv"
PROGRAM_MARKDOWN_OUT = RESULTS_DIR / "tcell_program_summary.md"

TCELL_TERMS = [
    "T CELL",
    "T CELLS",
    "TREG",
    "CD8",
    "CD4",
    "NAIVE",
    "NAÏVE",
    "MEMORY",
    "TCM",
    "TN",
    "TRM",
    "TEM",
    "TEMRA",
    "CYTOTOX",
    "MAIT",
    "NKT",
]

PROGRAMS = {
    "resting_naive_memory": {
        "ENSG00000081059",  # TCF7
        "ENSG00000126353",  # CCR7
        "ENSG00000138795",  # LEF1
        "ENSG00000188404",  # SELL
    },
    "resting_naive_memory_klf2": {
        "ENSG00000081059",  # TCF7
        "ENSG00000126353",  # CCR7
        "ENSG00000127528",  # KLF2
        "ENSG00000138795",  # LEF1
        "ENSG00000188404",  # SELL
    },
    "activation_effector": {
        "ENSG00000111537",  # IFNG
        "ENSG00000274221",  # CCL3
        "ENSG00000275302",  # CCL4
    },
    "regulatory_core": {
        "ENSG00000049768",  # FOXP3
        "ENSG00000134460",  # IL2RA
        "ENSG00000168685",  # IL7R
    },
    "cytotoxic_core": {
        "ENSG00000105374",  # NKG7
        "ENSG00000115523",  # GNLY
        "ENSG00000180644",  # PRF1
    },
    "cytotoxic_gzmk": {
        "ENSG00000105374",  # NKG7
        "ENSG00000113088",  # GZMK
        "ENSG00000271503",  # CCL5
    },
    "exhaustion_inhibitory": {
        "ENSG00000089692",  # LAG3
        "ENSG00000135077",  # HAVCR2
        "ENSG00000188389",  # PDCD1
    },
    "exhaustion_terminal": {
        "ENSG00000089692",  # LAG3
        "ENSG00000135077",  # HAVCR2
        "ENSG00000188389",  # PDCD1
        "ENSG00000198846",  # TOX
    },
}


def is_tcell_label(label: object) -> bool:
    label_text = normalize_text(label).upper()
    return any(term in label_text for term in TCELL_TERMS)


def program_memberships(marker_ids: list[str]) -> list[str]:
    marker_set = set(marker_ids)
    memberships = []
    for program_name, genes in PROGRAMS.items():
        if genes.issubset(marker_set):
            memberships.append(program_name)
    return memberships


def build_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    records_df = pd.read_csv(MARKER_RECORDS_PATH, sep="\t").fillna("")
    records_df = standardize_marker_records(records_df)
    records_df = records_df.loc[records_df["group_name"].map(is_tcell_label)].copy()
    id_to_name = build_gene_name_map(records_df)

    rows = []
    grouped = records_df.groupby(["source_corpus", "paper_key", "group_name"], sort=False)
    for (source_corpus, paper_key, cell_type), group in grouped:
        marker_ids = sorted({normalize_text(value) for value in group["feature_id_std"] if normalize_text(value)})
        marker_names = ids_to_names(marker_ids, id_to_name)
        rows.append(
            {
                "source_corpus": source_corpus,
                "paper_key": paper_key,
                "cell_type": cell_type,
                "n_markers": len(marker_ids),
                "marker_ids": ";".join(marker_ids),
                "marker_names": ";".join(marker_names),
                "programs": program_memberships(marker_ids),
            }
        )

    profiles_df = pd.DataFrame(rows)
    profiles_df["program_count"] = profiles_df["programs"].map(len)
    profiles_df["programs_text"] = profiles_df["programs"].map(lambda values: "; ".join(values))

    summary_rows = []
    for program_name, genes in PROGRAMS.items():
        matched = profiles_df.loc[profiles_df["programs"].map(lambda values: program_name in values)].copy()
        summary_rows.append(
            {
                "program": program_name,
                "program_gene_ids": "; ".join(sorted(genes)),
                "program_gene_labels": "; ".join(ids_to_names(sorted(genes), id_to_name)),
                "n_profiles": int(len(matched)),
                "n_labels": int(matched["cell_type"].nunique()),
                "n_papers": int(matched["paper_key"].nunique()),
                "n_corpora": int(matched["source_corpus"].nunique()),
                "example_labels": "; ".join(sorted(matched["cell_type"].unique())[:12]),
            }
        )

    profile_keep = [
        "source_corpus",
        "paper_key",
        "cell_type",
        "n_markers",
        "marker_ids",
        "marker_names",
        "programs_text",
        "program_count",
    ]
    profile_df = profiles_df.loc[:, profile_keep].sort_values(["program_count", "cell_type", "paper_key"], ascending=[False, True, True]).reset_index(drop=True)
    summary_df = pd.DataFrame(summary_rows).sort_values(["n_profiles", "n_labels", "program"], ascending=[False, False, True]).reset_index(drop=True)
    return profile_df, summary_df


def write_markdown(profile_df: pd.DataFrame, summary_df: pd.DataFrame) -> None:
    lines: list[str] = []
    lines.append("# T-cell Program Summary")
    lines.append("")
    lines.append("This table summarizes recurring T-cell marker programs after collapsing the corpus into standardized gene-id space.")
    lines.append("Marker matching uses standardized Ensembl gene IDs; gene symbols are included only for readability.")
    lines.append("")
    lines.append("## Program summary")
    lines.append("")
    lines.append("| Program | Gene IDs | Gene labels | Profiles | Labels | Papers | Corpora | Example labels |")
    lines.append("|---|---|---|---:|---:|---:|---:|---|")
    for row in summary_df.itertuples(index=False):
        lines.append(
            f"| {row.program} | {row.program_gene_ids} | {row.program_gene_labels} | {row.n_profiles} | {row.n_labels} | {row.n_papers} | {row.n_corpora} | {row.example_labels or '—'} |"
        )
    lines.append("")
    lines.append("## Matched profiles")
    lines.append("")
    lines.append("| Corpus | Paper | Cell type | Markers (IDs) | Markers (labels) | Programs |")
    lines.append("|---|---|---|---|---|---|")
    for row in profile_df.loc[profile_df["program_count"] > 0].itertuples(index=False):
        lines.append(
            f"| {row.source_corpus} | {row.paper_key} | {row.cell_type} | {row.marker_ids} | {row.marker_names} | {row.programs_text or '—'} |"
        )
    PROGRAM_MARKDOWN_OUT.write_text("\n".join(lines))


def main() -> None:
    profile_df, summary_df = build_tables()
    profile_df.to_csv(PROGRAM_PROFILE_OUT, sep="\t", index=False)
    summary_df.to_csv(PROGRAM_SUMMARY_OUT, sep="\t", index=False)
    write_markdown(profile_df, summary_df)

    print(f"Wrote T-cell program profiles to {PROGRAM_PROFILE_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote T-cell program summary to {PROGRAM_SUMMARY_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote markdown report to {PROGRAM_MARKDOWN_OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
