from __future__ import annotations

from collections import Counter
from pathlib import Path

import pandas as pd

from build_fig5_nomenclature_weights import build_profiles
from build_marker_stability_prototype import assign_neighborhood
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR, split_marker_text


GENE_SUMMARY_PATH = RESULTS_DIR / "tcell_gene_f1_ratio_gene_summary.tsv"
MEMBERSHIP_PATH = RESULTS_DIR / "tcell_marker_cluster_membership.tsv"
GENE_LABEL_SUMMARY_PATH = RESULTS_DIR / "tcell_highlight_gene_label_summary.tsv"
GENE_SET_LABEL_SUMMARY_PATH = RESULTS_DIR / "tcell_highlight_gene_set_label_summary.tsv"
PROFILE_MATCHES_PATH = RESULTS_DIR / "tcell_highlight_gene_set_profile_matches.tsv"
REPORT_PATH = RESULTS_DIR / "tcell_highlight_gene_label_summary.md"


HIGHLIGHT_GENE_SETS = [
    {
        "set_name": "Naive/memory green markers",
        "color_class": "marker-cluster enriched",
        "genes": ["SELL", "CCR7"],
    },
    {
        "set_name": "Cytotoxic/exhaustion green markers",
        "color_class": "marker-cluster enriched",
        "genes": ["HAVCR2", "PRF1", "GZMB"],
    },
    {
        "set_name": "Residency green marker",
        "color_class": "marker-cluster enriched",
        "genes": ["ZNF683"],
    },
    {
        "set_name": "CD3 blue markers",
        "color_class": "high in both",
        "genes": ["CD3D", "CD3G"],
    },
    {
        "set_name": "Treg blue marker",
        "color_class": "high in both",
        "genes": ["FOXP3"],
    },
    {
        "set_name": "Costimulation orange markers",
        "color_class": "label enriched",
        "genes": ["BATF", "TNFRSF4", "TNFRSF9"],
    },
    {
        "set_name": "CD8 orange marker",
        "color_class": "label enriched",
        "genes": ["CD8B"],
    },
]


def clean_join(values: list[str], max_items: int = 8) -> str:
    values = [str(value) for value in values if pd.notna(value) and str(value)]
    return "; ".join(values[:max_items])


def top_counter_text(values: pd.Series, max_items: int = 8) -> str:
    counts = Counter(str(value) for value in values.dropna() if str(value))
    return "; ".join(f"{label} ({count})" for label, count in counts.most_common(max_items))


def marker_names_from_ids(marker_ids: set[str], id_to_name: dict[str, str]) -> str:
    return "; ".join(id_to_name.get(gene_id, gene_id) for gene_id in sorted(marker_ids))


def add_tcell_membership(profiles_df: pd.DataFrame) -> pd.DataFrame:
    membership_df = pd.read_csv(MEMBERSHIP_PATH, sep="\t")
    membership_df["profile_uid"] = [
        f"{row.source_corpus}|{row.paper_id}|{row.cell_type}"
        for row in membership_df.itertuples(index=False)
    ]
    keep_cols = [
        "profile_uid",
        "component",
        "dominant_module",
    ]
    profiles_df = profiles_df.merge(membership_df[keep_cols], on="profile_uid", how="left")
    return profiles_df


def summarize_gene_profiles(
    profiles_df: pd.DataFrame,
    gene_summary_df: pd.DataFrame,
    id_to_name: dict[str, str],
) -> pd.DataFrame:
    query_genes = sorted({gene for gene_set in HIGHLIGHT_GENE_SETS for gene in gene_set["genes"]})
    query_df = gene_summary_df.loc[gene_summary_df["gene_name"].isin(query_genes)].copy()
    gene_meta = query_df.set_index("gene_name").to_dict("index")

    rows = []
    for gene_name in query_genes:
        meta = gene_meta.get(gene_name)
        if meta is None:
            continue
        gene_id = meta["gene_id"]
        hit_df = profiles_df.loc[
            profiles_df["marker_set"].map(lambda marker_set: gene_id in marker_set)
        ].copy()
        tcell_hit_df = hit_df.loc[hit_df["neighborhood"].eq("T cell")].copy()
        rows.append(
            {
                "gene_name": gene_name,
                "gene_id": gene_id,
                "shift_class": meta["shift_class"],
                "marker_cluster_f1": meta["marker_cluster_f1"],
                "best_label_f1": meta["best_label_f1"],
                "best_label_group": meta["best_label_group"],
                "n_profiles_all": len(hit_df),
                "n_profiles_tcell": len(tcell_hit_df),
                "n_papers_tcell": tcell_hit_df["paper_key"].nunique(),
                "top_tcell_labels": top_counter_text(tcell_hit_df["cell_type"]),
                "top_tcell_marker_clusters": top_counter_text(
                    tcell_hit_df["component"].dropna().map(lambda value: f"C{int(value)}")
                ),
                "top_tcell_cluster_programs": top_counter_text(tcell_hit_df["dominant_module"]),
            }
        )
    return pd.DataFrame(rows)


def summarize_gene_sets(
    profiles_df: pd.DataFrame,
    gene_summary_df: pd.DataFrame,
    id_to_name: dict[str, str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    gene_name_to_id = gene_summary_df.set_index("gene_name")["gene_id"].to_dict()
    summary_rows = []
    match_rows = []

    for gene_set in HIGHLIGHT_GENE_SETS:
        requested_names = gene_set["genes"]
        requested_ids = [gene_name_to_id[gene] for gene in requested_names if gene in gene_name_to_id]
        requested_id_set = set(requested_ids)
        if not requested_id_set:
            continue

        tcell_df = profiles_df.loc[profiles_df["neighborhood"].eq("T cell")].copy()
        tcell_df["matched_gene_ids"] = tcell_df["marker_set"].map(lambda markers: markers & requested_id_set)
        tcell_df["matched_gene_count"] = tcell_df["matched_gene_ids"].map(len)

        for threshold_label, threshold in [
            ("any", 1),
            ("at least 2", min(2, len(requested_id_set))),
            ("all", len(requested_id_set)),
        ]:
            hit_df = tcell_df.loc[tcell_df["matched_gene_count"].ge(threshold)].copy()
            if threshold_label == "at least 2" and len(requested_id_set) == 1:
                continue
            summary_rows.append(
                {
                    "set_name": gene_set["set_name"],
                    "color_class": gene_set["color_class"],
                    "genes": "; ".join(requested_names),
                    "match_rule": threshold_label,
                    "n_genes_in_set": len(requested_id_set),
                    "n_profiles": len(hit_df),
                    "n_papers": hit_df["paper_key"].nunique(),
                    "top_labels": top_counter_text(hit_df["cell_type"]),
                    "top_marker_clusters": top_counter_text(
                        hit_df["component"].dropna().map(lambda value: f"C{int(value)}")
                    ),
                    "top_cluster_programs": top_counter_text(hit_df["dominant_module"]),
                }
            )

            for row in hit_df.sort_values(["matched_gene_count", "cell_type"], ascending=[False, True]).itertuples(
                index=False
            ):
                match_rows.append(
                    {
                        "set_name": gene_set["set_name"],
                        "color_class": gene_set["color_class"],
                        "genes": "; ".join(requested_names),
                        "match_rule": threshold_label,
                        "matched_genes": marker_names_from_ids(row.matched_gene_ids, id_to_name),
                        "matched_gene_count": int(row.matched_gene_count),
                        "component": int(row.component) if pd.notna(row.component) else None,
                        "dominant_module": row.dominant_module,
                        "source_corpus": row.source_corpus,
                        "paper_key": row.paper_key,
                        "cell_type": row.cell_type,
                        "normalized_cell_type": row.normalized_cell_type,
                        "n_markers": int(row.n_markers),
                        "marker_names": row.marker_names,
                    }
                )

    return pd.DataFrame(summary_rows), pd.DataFrame(match_rows)


def write_report(gene_df: pd.DataFrame, set_df: pd.DataFrame, report_path: Path) -> None:
    lines = [
        "# T-cell highlighted gene label summary",
        "",
        "This report asks what reported cell type labels appear among T-cell marker profiles that contain the highlighted genes from panel F.",
        "",
        "## Individual genes",
        "",
    ]
    for row in gene_df.sort_values(["shift_class", "gene_name"]).itertuples(index=False):
        lines.append(
            f"- **{row.gene_name}** ({row.shift_class}): "
            f"{row.n_profiles_tcell} T-cell profiles across {row.n_papers_tcell} papers. "
            f"Top labels: {row.top_tcell_labels or 'none'}."
        )

    lines.extend(["", "## Gene sets", ""])
    display_df = set_df.loc[set_df["match_rule"].isin(["any", "all"])].copy()
    for row in display_df.itertuples(index=False):
        lines.append(
            f"- **{row.set_name}** ({row.color_class}, {row.match_rule}; {row.genes}): "
            f"{row.n_profiles} profiles across {row.n_papers} papers. "
            f"Top labels: {row.top_labels or 'none'}."
        )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    profiles_df, id_to_name = build_profiles()
    profiles_df["neighborhood"] = profiles_df["cell_type"].map(assign_neighborhood)
    profiles_df = add_tcell_membership(profiles_df)
    profiles_df["marker_set"] = profiles_df["marker_ids"].map(lambda value: set(split_marker_text(value)))
    gene_summary_df = pd.read_csv(GENE_SUMMARY_PATH, sep="\t")

    gene_df = summarize_gene_profiles(profiles_df, gene_summary_df, id_to_name)
    set_df, matches_df = summarize_gene_sets(profiles_df, gene_summary_df, id_to_name)

    gene_df.to_csv(GENE_LABEL_SUMMARY_PATH, sep="\t", index=False)
    set_df.to_csv(GENE_SET_LABEL_SUMMARY_PATH, sep="\t", index=False)
    matches_df.to_csv(PROFILE_MATCHES_PATH, sep="\t", index=False)
    write_report(gene_df, set_df, REPORT_PATH)

    print(f"Wrote {GENE_LABEL_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {GENE_SET_LABEL_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PROFILE_MATCHES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
