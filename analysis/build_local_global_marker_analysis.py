from __future__ import annotations

import math
from collections import Counter, defaultdict
from itertools import combinations

import numpy as np
import pandas as pd

from build_marker_stability_prototype import assign_neighborhood, build_records
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR, build_profile_summary, split_marker_text
from marker_label_utils import normalize_label


PAIR_SUMMARY_PATH = RESULTS_DIR / "local_global_marker_pair_summary.tsv"
PAPER_SUMMARY_PATH = RESULTS_DIR / "local_global_paper_marker_summary.tsv"
LABEL_SUMMARY_PATH = RESULTS_DIR / "local_global_label_coherence_summary.tsv"
PROFILE_LIFTOVER_PATH = RESULTS_DIR / "local_global_profile_marker_liftover.tsv"
REPORT_PATH = RESULTS_DIR / "local_global_marker_report.md"

MIN_MARKERS = 3
MIN_LABEL_PROFILES = 3
MIN_LABEL_PAPERS = 2


def ceil_log2(n: int) -> int:
    if n <= 1:
        return 0
    return (n - 1).bit_length()


def jaccard(a: set[str], b: set[str]) -> tuple[int, int, float]:
    shared = len(a & b)
    union = len(a | b)
    return shared, union, shared / union if union else 0.0


def summarize_values(values: list[float], shared_counts: list[int]) -> dict[str, object]:
    if not values:
        return {
            "n_pairs": 0,
            "mean_jaccard": np.nan,
            "median_jaccard": np.nan,
            "q25_jaccard": np.nan,
            "q75_jaccard": np.nan,
            "pct_jaccard_eq_0": np.nan,
            "pct_jaccard_ge_0_10": np.nan,
            "pct_jaccard_ge_0_25": np.nan,
            "pct_jaccard_eq_1": np.nan,
            "mean_shared_genes": np.nan,
        }
    arr = np.asarray(values, dtype=float)
    shared_arr = np.asarray(shared_counts, dtype=float)
    return {
        "n_pairs": len(values),
        "mean_jaccard": float(arr.mean()),
        "median_jaccard": float(np.median(arr)),
        "q25_jaccard": float(np.quantile(arr, 0.25)),
        "q75_jaccard": float(np.quantile(arr, 0.75)),
        "pct_jaccard_eq_0": float((arr == 0).mean()),
        "pct_jaccard_ge_0_10": float((arr >= 0.10).mean()),
        "pct_jaccard_ge_0_25": float((arr >= 0.25).mean()),
        "pct_jaccard_eq_1": float((arr == 1).mean()),
        "mean_shared_genes": float(shared_arr.mean()),
    }


def build_profiles() -> tuple[pd.DataFrame, dict[str, str]]:
    records_df = build_records()
    _profiles_df, filtered_profiles_df, _filtered_profiles, id_to_name = build_profile_summary(
        records_df,
        min_markers=MIN_MARKERS,
        feature_id_col="feature_id_std",
        feature_name_col="feature_name_std",
    )
    profiles_df = filtered_profiles_df.copy().reset_index(drop=True)
    profiles_df["profile_idx"] = np.arange(len(profiles_df))
    profiles_df["profile_uid"] = [
        f"{row.source_corpus}|{row.paper_id}|{row.cell_type}"
        for row in profiles_df.itertuples(index=False)
    ]
    profiles_df["paper_uid"] = [
        f"{row.source_corpus}|{row.paper_id}"
        for row in profiles_df.itertuples(index=False)
    ]
    profiles_df["normalized_cell_type"] = profiles_df["cell_type"].map(normalize_label)
    profiles_df["neighborhood"] = profiles_df["cell_type"].map(assign_neighborhood)
    profiles_df["marker_set"] = profiles_df["marker_ids"].map(lambda value: set(split_marker_text(value)))
    return profiles_df, id_to_name


def pair_category(row_a: object, row_b: object) -> str:
    same_paper = row_a.paper_uid == row_b.paper_uid
    same_label = (
        row_a.normalized_cell_type != ""
        and row_a.normalized_cell_type == row_b.normalized_cell_type
    )
    same_neighborhood = (
        row_a.neighborhood != ""
        and row_a.neighborhood == row_b.neighborhood
    )
    both_neighborhoods = row_a.neighborhood != "" and row_b.neighborhood != ""

    if same_paper and same_label:
        return "within_paper_same_exact_label"
    if same_paper:
        return "within_paper_different_label"
    if same_label:
        return "between_paper_same_exact_label"
    if same_neighborhood:
        return "between_paper_same_broad_neighborhood"
    if both_neighborhoods:
        return "between_paper_different_broad_neighborhood"
    return "between_paper_other"


def build_pair_summary(profiles_df: pd.DataFrame) -> pd.DataFrame:
    rows = list(profiles_df.itertuples(index=False))
    marker_sets = [row.marker_set for row in rows]
    category_values: dict[str, list[float]] = defaultdict(list)
    category_shared: dict[str, list[int]] = defaultdict(list)

    for idx_a, idx_b in combinations(range(len(rows)), 2):
        shared, _union, value = jaccard(marker_sets[idx_a], marker_sets[idx_b])
        category = pair_category(rows[idx_a], rows[idx_b])
        category_values[category].append(value)
        category_shared[category].append(shared)

    category_order = [
        "within_paper_different_label",
        "within_paper_same_exact_label",
        "between_paper_same_exact_label",
        "between_paper_same_broad_neighborhood",
        "between_paper_different_broad_neighborhood",
        "between_paper_other",
    ]
    summary_rows = []
    for category in category_order:
        summary_rows.append(
            {
                "pair_category": category,
                **summarize_values(category_values[category], category_shared[category]),
            }
        )
    return pd.DataFrame(summary_rows)


def greedy_separating_panel(profile_gene_sets: dict[str, set[str]]) -> tuple[list[str], int, int]:
    profile_ids = sorted(profile_gene_sets)
    signature_to_profiles: dict[tuple[str, ...], list[str]] = defaultdict(list)
    for profile_id in profile_ids:
        signature_to_profiles[tuple(sorted(profile_gene_sets[profile_id]))].append(profile_id)

    representatives = [profiles[0] for profiles in signature_to_profiles.values()]
    constraints: list[set[str]] = []
    for left, right in combinations(representatives, 2):
        diff = profile_gene_sets[left] ^ profile_gene_sets[right]
        if diff:
            constraints.append(diff)

    uncovered = set(range(len(constraints)))
    genes = sorted(set().union(*profile_gene_sets.values())) if profile_gene_sets else []
    gene_to_constraints: dict[str, set[int]] = {gene: set() for gene in genes}
    for constraint_idx, diff in enumerate(constraints):
        for gene in diff:
            gene_to_constraints[gene].add(constraint_idx)

    selected = []
    while uncovered:
        best_gene = ""
        best_cover: set[int] = set()
        for gene, constraint_ids in gene_to_constraints.items():
            cover = constraint_ids & uncovered
            if len(cover) > len(best_cover) or (
                len(cover) == len(best_cover) and best_gene and gene < best_gene
            ):
                best_gene = gene
                best_cover = cover
        if not best_cover:
            break
        selected.append(best_gene)
        uncovered -= best_cover

    n_distinct_signatures = len(signature_to_profiles)
    n_duplicate_profiles = sum(len(profiles) for profiles in signature_to_profiles.values() if len(profiles) > 1)
    return selected, n_distinct_signatures, n_duplicate_profiles


def build_paper_summary(profiles_df: pd.DataFrame, id_to_name: dict[str, str]) -> pd.DataFrame:
    summary_rows = []
    for (source_corpus, paper_id, paper_key), paper_df in profiles_df.groupby(
        ["source_corpus", "paper_id", "paper_key"], sort=True
    ):
        if len(paper_df) < 2:
            continue

        profile_gene_sets = {
            row.profile_uid: row.marker_set for row in paper_df.itertuples(index=False)
        }
        selected, n_distinct_signatures, n_duplicate_profiles = greedy_separating_panel(profile_gene_sets)
        jaccards = []
        shared_counts = []
        paper_rows = list(paper_df.itertuples(index=False))
        for row_a, row_b in combinations(paper_rows, 2):
            shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
            jaccards.append(value)
            shared_counts.append(shared)

        selected_names = [id_to_name.get(gene_id, gene_id) for gene_id in selected]
        summary_rows.append(
            {
                "source_corpus": source_corpus,
                "paper_id": paper_id,
                "paper_key": paper_key,
                "n_profiles": len(paper_df),
                "n_genes": len(set().union(*profile_gene_sets.values())),
                "n_distinct_marker_signatures": n_distinct_signatures,
                "n_duplicate_profile_signatures": n_duplicate_profiles,
                "all_profiles_locally_identifiable": n_duplicate_profiles == 0,
                "information_lower_bound_log2": ceil_log2(n_distinct_signatures),
                "greedy_local_panel_size": len(selected),
                "greedy_local_panel_genes": "; ".join(selected_names[:25]),
                **summarize_values(jaccards, shared_counts),
            }
        )
    return pd.DataFrame(summary_rows).sort_values(
        ["n_profiles", "greedy_local_panel_size"], ascending=[False, False]
    )


def build_label_summary(profiles_df: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    df = profiles_df.loc[profiles_df["normalized_cell_type"].ne("")].copy()
    for label, label_df in df.groupby("normalized_cell_type", sort=True):
        n_papers = label_df["paper_uid"].nunique()
        if len(label_df) < MIN_LABEL_PROFILES or n_papers < MIN_LABEL_PAPERS:
            continue

        jaccards = []
        shared_counts = []
        rows = list(label_df.itertuples(index=False))
        for row_a, row_b in combinations(rows, 2):
            if row_a.paper_uid == row_b.paper_uid:
                continue
            shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
            jaccards.append(value)
            shared_counts.append(shared)
        if not jaccards:
            continue

        example_labels = sorted({row.cell_type for row in rows})[:8]
        summary_rows.append(
            {
                "normalized_cell_type": label,
                "n_profiles": len(label_df),
                "n_papers": n_papers,
                "n_source_corpora": label_df["source_corpus"].nunique(),
                "example_reported_labels": "; ".join(example_labels),
                "global_label_underspecification_score": 1.0 - float(np.median(jaccards)),
                **summarize_values(jaccards, shared_counts),
            }
        )
    return pd.DataFrame(summary_rows).sort_values(
        ["global_label_underspecification_score", "n_profiles"], ascending=[False, False]
    )


def build_profile_liftover(profiles_df: pd.DataFrame, id_to_name: dict[str, str]) -> pd.DataFrame:
    paper_to_gene_counts: dict[str, Counter] = {}
    label_to_rows: dict[str, list[object]] = defaultdict(list)
    neighborhood_to_rows: dict[str, list[object]] = defaultdict(list)

    for paper_uid, paper_df in profiles_df.groupby("paper_uid", sort=False):
        paper_to_gene_counts[paper_uid] = Counter(
            gene_id for marker_set in paper_df["marker_set"] for gene_id in marker_set
        )
    for row in profiles_df.itertuples(index=False):
        if row.normalized_cell_type:
            label_to_rows[row.normalized_cell_type].append(row)
        if row.neighborhood:
            neighborhood_to_rows[row.neighborhood].append(row)

    rows_out = []
    for row in profiles_df.itertuples(index=False):
        paper_gene_counts = paper_to_gene_counts[row.paper_uid]
        local_private = {gene_id for gene_id in row.marker_set if paper_gene_counts[gene_id] == 1}

        same_label_other_profiles = 0
        same_label_other_union: set[str] = set()
        for other in label_to_rows.get(row.normalized_cell_type, []):
            if other.paper_uid != row.paper_uid:
                same_label_other_profiles += 1
                same_label_other_union |= other.marker_set

        same_neighborhood_other_profiles = 0
        same_neighborhood_other_union: set[str] = set()
        for other in neighborhood_to_rows.get(row.neighborhood, []):
            if other.paper_uid != row.paper_uid:
                same_neighborhood_other_profiles += 1
                same_neighborhood_other_union |= other.marker_set

        local_private_names = [id_to_name.get(gene_id, gene_id) for gene_id in sorted(local_private)]
        rows_out.append(
            {
                "source_corpus": row.source_corpus,
                "paper_id": row.paper_id,
                "paper_key": row.paper_key,
                "cell_type": row.cell_type,
                "normalized_cell_type": row.normalized_cell_type,
                "neighborhood": row.neighborhood,
                "n_markers": len(row.marker_set),
                "n_local_private_markers": len(local_private),
                "local_private_fraction": len(local_private) / len(row.marker_set) if row.marker_set else 0.0,
                "n_same_label_other_paper_profiles": same_label_other_profiles,
                "n_same_label_other_paper_markers": len(same_label_other_union),
                "marker_fraction_recovered_by_same_label_other_papers": (
                    len(row.marker_set & same_label_other_union) / len(row.marker_set)
                    if row.marker_set and same_label_other_profiles
                    else np.nan
                ),
                "local_private_fraction_recovered_by_same_label_other_papers": (
                    len(local_private & same_label_other_union) / len(local_private)
                    if local_private and same_label_other_profiles
                    else np.nan
                ),
                "n_same_neighborhood_other_paper_profiles": same_neighborhood_other_profiles,
                "marker_fraction_recovered_by_same_neighborhood_other_papers": (
                    len(row.marker_set & same_neighborhood_other_union) / len(row.marker_set)
                    if row.marker_set and same_neighborhood_other_profiles
                    else np.nan
                ),
                "local_private_marker_names": "; ".join(local_private_names[:30]),
            }
        )
    return pd.DataFrame(rows_out)


def markdown_table(df: pd.DataFrame) -> str:
    string_df = df.fillna("").astype(str)
    header = "| " + " | ".join(string_df.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(string_df.columns)) + " |"
    rows = ["| " + " | ".join(row) + " |" for row in string_df.itertuples(index=False, name=None)]
    return "\n".join([header, separator, *rows])


def format_float(value: float) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return f"{value:.3f}"


def write_report(
    pair_summary_df: pd.DataFrame,
    paper_summary_df: pd.DataFrame,
    label_summary_df: pd.DataFrame,
    profile_liftover_df: pd.DataFrame,
) -> None:
    local_pairs = pair_summary_df.loc[
        pair_summary_df["pair_category"].eq("within_paper_different_label")
    ].iloc[0]
    same_label_pairs = pair_summary_df.loc[
        pair_summary_df["pair_category"].eq("between_paper_same_exact_label")
    ].iloc[0]
    paper_panel_median = paper_summary_df["greedy_local_panel_size"].median()
    paper_profile_median = paper_summary_df["n_profiles"].median()
    liftover_median = profile_liftover_df[
        "marker_fraction_recovered_by_same_label_other_papers"
    ].dropna().median()

    pair_display = pair_summary_df[
        [
            "pair_category",
            "n_pairs",
            "median_jaccard",
            "mean_jaccard",
            "pct_jaccard_eq_0",
            "pct_jaccard_ge_0_25",
        ]
    ].copy()
    for col in ["median_jaccard", "mean_jaccard", "pct_jaccard_eq_0", "pct_jaccard_ge_0_25"]:
        pair_display[col] = pair_display[col].map(format_float)

    paper_display = paper_summary_df[
        [
            "paper_key",
            "n_profiles",
            "n_distinct_marker_signatures",
            "information_lower_bound_log2",
            "greedy_local_panel_size",
            "median_jaccard",
        ]
    ].head(12).copy()
    paper_display["median_jaccard"] = paper_display["median_jaccard"].map(format_float)

    label_display = label_summary_df[
        [
            "normalized_cell_type",
            "n_profiles",
            "n_papers",
            "median_jaccard",
            "global_label_underspecification_score",
            "example_reported_labels",
        ]
    ].head(15).copy()
    for col in ["median_jaccard", "global_label_underspecification_score"]:
        label_display[col] = label_display[col].map(format_float)

    lines = [
        "# Local vs Global Marker Analysis",
        "",
        "This analysis quantifies the distinction between local marker claims within a paper and global marker reuse across papers.",
        "A same-paper pair approximates the local comparison set used to report markers. A different-paper pair approximates the atlas-scale comparison problem.",
        "",
        "Important caveat: marker absence means not reported as a marker in this corpus, not absent expression.",
        "",
        "## Headline",
        "",
        f"- Within-paper different-label pairs have median marker Jaccard {local_pairs.median_jaccard:.3f}.",
        f"- Between-paper same-exact-label pairs have median marker Jaccard {same_label_pairs.median_jaccard:.3f}.",
        f"- The median paper has {paper_profile_median:.0f} reported profiles and a greedy local separating panel of {paper_panel_median:.0f} genes.",
        f"- Across profiles with same-label matches in other papers, the median fraction of markers recovered by same-label profiles elsewhere is {liftover_median:.3f}.",
        "",
        "## Pairwise Marker Overlap",
        "",
        markdown_table(pair_display),
        "",
        "## Largest Local Marker Problems",
        "",
        markdown_table(paper_display),
        "",
        "## Most Underspecified Recurrent Labels",
        "",
        markdown_table(label_display),
        "",
        "## Interpretation",
        "",
        "Local markers are selected in a paper-specific comparison set. They often separate the cell types reported in that paper, but the same label across papers does not necessarily recover the same marker set.",
        "This is the empirical version of the formal distinction between a local binary marker matrix `X_i` and a global atlas-scale marker matrix `X`.",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    profiles_df, id_to_name = build_profiles()

    pair_summary_df = build_pair_summary(profiles_df)
    paper_summary_df = build_paper_summary(profiles_df, id_to_name)
    label_summary_df = build_label_summary(profiles_df)
    profile_liftover_df = build_profile_liftover(profiles_df, id_to_name)

    pair_summary_df.to_csv(PAIR_SUMMARY_PATH, sep="\t", index=False)
    paper_summary_df.to_csv(PAPER_SUMMARY_PATH, sep="\t", index=False)
    label_summary_df.to_csv(LABEL_SUMMARY_PATH, sep="\t", index=False)
    profile_liftover_df.to_csv(PROFILE_LIFTOVER_PATH, sep="\t", index=False)
    write_report(pair_summary_df, paper_summary_df, label_summary_df, profile_liftover_df)

    print(f"Wrote {PAIR_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PAPER_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {LABEL_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PROFILE_LIFTOVER_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
