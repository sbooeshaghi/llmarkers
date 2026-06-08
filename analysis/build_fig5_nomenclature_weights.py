from __future__ import annotations

import re
import warnings
from collections import Counter, defaultdict
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch, Rectangle
from matplotlib.ticker import PercentFormatter
from scipy.sparse import csr_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score

from build_marker_stability_prototype import assign_neighborhood, build_records
from build_fig5_cluster_prototypes import (
    MARKER_CLUSTER_JACCARD,
    connected_components as marker_connected_components,
    marker_pair_edges,
    summarize_marker_clusters,
)
from build_myeloid_profile_graph_comparison import (
    COMPARE_COMPONENTS as MYELOID_COMPONENTS,
    JACCARD_THRESHOLD as MYELOID_JACCARD_THRESHOLD,
    build_myeloid_profiles,
    comparison_profiles as myeloid_comparison_profiles,
    component_memberships as myeloid_component_memberships,
    marker_sets as myeloid_marker_sets,
    summarize_components as summarize_myeloid_components,
)
from build_tcell_marker_cluster_summary import (
    JACCARD_THRESHOLD as TCELL_MARKER_CLUSTER_JACCARD,
    build_name_to_ids as build_tcell_name_to_ids,
    component_memberships as tcell_component_memberships,
    connected_components,
    label_relation,
    label_tokens,
    marker_sets as tcell_marker_sets,
    module_gene_rows as tcell_module_gene_rows,
    normalize_label,
    summarize_components as summarize_tcell_components,
)
from build_tcell_marker_hierarchy import profile_module_scores
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR, build_profile_summary, split_marker_text


warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn")
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

MIN_MARKERS = 3
MIN_GENE_PROFILE_COUNT = 4
MYELOID_MIN_GENE_PROFILE_COUNT = 2
MIN_LABEL_PROFILE_COUNT = 3
MYELOID_MIN_LABEL_PROFILE_COUNT = 2
MIN_SHARED_PAIRS_FOR_DISPLAY = 10
MYELOID_MIN_SHARED_PAIRS_FOR_DISPLAY = 2
MIN_LABEL_TOKEN_PAIRS = 20
MYELOID_MIN_LABEL_TOKEN_PAIRS = 3
N_SPLITS = 10
TEST_PAPER_FRACTION = 0.30
RANDOM_SEED = 17
LOGISTIC_C = 0.60
LABEL_TOKEN_STOPWORDS = {
    "associated",
    "cell",
    "cells",
    "cluster",
    "clusters",
    "high",
    "hi",
    "ii",
    "iii",
    "iv",
    "like",
    "lo",
    "low",
    "mp",
    "negative",
    "non",
    "pos",
    "positive",
    "pre",
    "sc",
    "subcluster",
    "subclusters",
    "type",
    "types",
}

GENE_WEIGHTS_PATH = RESULTS_DIR / "fig5_nomenclature_gene_weights.tsv"
PAIR_SCORES_PATH = RESULTS_DIR / "fig5_nomenclature_pair_scores.tsv"
CV_METRICS_PATH = RESULTS_DIR / "fig5_nomenclature_cv_metrics.tsv"
LABEL_TOKEN_SCORES_PATH = RESULTS_DIR / "fig5_nomenclature_label_token_scores.tsv"
LABEL_SILHOUETTE_PATH = RESULTS_DIR / "fig5_nomenclature_label_silhouette_scores.tsv"
MARKER_CLUSTER_SUMMARY_PATH = RESULTS_DIR / "fig5_nomenclature_marker_cluster_summary.tsv"
MARKER_CLUSTER_MEMBERSHIP_PATH = RESULTS_DIR / "fig5_nomenclature_marker_cluster_membership.tsv"
MARKER_CLUSTER_LABEL_SILHOUETTE_PATH = RESULTS_DIR / "fig5_nomenclature_marker_cluster_label_silhouette.tsv"
LABEL_GROUP_GENE_SCORES_PATH = RESULTS_DIR / "fig5_nomenclature_label_group_gene_scores.tsv"
MARKER_GROUP_GENE_SCORES_PATH = RESULTS_DIR / "fig5_nomenclature_marker_group_gene_scores.tsv"
GROUP_GENE_F1_COMPARISON_PATH = RESULTS_DIR / "fig5_nomenclature_group_gene_f1_comparison.tsv"
MYELOID_GENE_WEIGHTS_PATH = RESULTS_DIR / "fig5_myeloid_nomenclature_gene_weights.tsv"
MYELOID_PAIR_SCORES_PATH = RESULTS_DIR / "fig5_myeloid_nomenclature_pair_scores.tsv"
MYELOID_LABEL_TOKEN_SCORES_PATH = RESULTS_DIR / "fig5_myeloid_nomenclature_label_token_scores.tsv"
MYELOID_LABEL_SILHOUETTE_PATH = RESULTS_DIR / "fig5_myeloid_nomenclature_label_silhouette_scores.tsv"
TCELL_GENE_F1_CLUSTER_TABLE_PATH = RESULTS_DIR / "tcell_gene_f1_ratio_by_cluster.tsv"
TCELL_GENE_F1_GENE_SUMMARY_PATH = RESULTS_DIR / "tcell_gene_f1_ratio_gene_summary.tsv"
REPORT_PATH = RESULTS_DIR / "fig5_nomenclature_weights_report.md"
FIGURE_PATH = FIGURE_DIR / "fig5_nomenclature_weights.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig5_nomenclature_weights.png"
MAIN_FIGURE_PATH = FIGURE_DIR / "fig_marker_program_resolution.pdf"
MAIN_FIGURE_PNG_PATH = FIGURE_DIR / "fig_marker_program_resolution.png"
TCELL_GENE_F1_PSEUDOCOUNT = 0.02
EXAMPLE_GROUPS = [
    {
        "key": "TREG",
        "label": "TREG",
        "marker_query": "TREG",
        "label_title": "Label group: TREG -> genes",
        "marker_title": "Marker cluster C{cluster}: TREG -> genes",
        "f1_title": "TREG gene F1 shifts",
    },
    {
        "key": "EXHAUSTED",
        "label_contains": "EXHAUST",
        "marker_query": "EXHAUST",
        "label_title": "Label set: exhausted T cells -> genes",
        "marker_title": "Marker cluster C{cluster}: exhausted/TREG -> genes",
        "f1_title": "Exhausted gene F1 shifts",
    },
]


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
    profiles_df["normalized_cell_type"] = profiles_df["cell_type"].map(normalize_label)
    profiles_df["marker_set"] = profiles_df["marker_ids"].map(lambda value: set(split_marker_text(value)))
    return profiles_df, id_to_name


def reset_profile_indices(profiles_df: pd.DataFrame) -> pd.DataFrame:
    df = profiles_df.copy().reset_index(drop=True)
    df["profile_idx"] = np.arange(len(df))
    if "profile_uid" not in df.columns:
        df["profile_uid"] = [
            f"{row.source_corpus}|{row.paper_id}|{row.cell_type}"
            for row in df.itertuples(index=False)
        ]
    if "normalized_cell_type" not in df.columns:
        df["normalized_cell_type"] = df["cell_type"].map(normalize_label)
    if "marker_set" not in df.columns:
        df["marker_set"] = df["marker_ids"].map(lambda value: set(split_marker_text(value)))
    return df


def build_myeloid_c1_c3_profiles() -> tuple[pd.DataFrame, dict[str, str]]:
    myeloid_df, id_to_name = build_myeloid_profiles()
    profile_gene_sets = myeloid_marker_sets(myeloid_df)
    components, edges = connected_components(
        profile_gene_sets,
        myeloid_df["paper_key"].tolist(),
        threshold=MYELOID_JACCARD_THRESHOLD,
    )
    summary_df = summarize_myeloid_components(myeloid_df, profile_gene_sets, id_to_name, components, edges)
    membership_df = myeloid_component_memberships(myeloid_df, components, summary_df)
    subset_df = myeloid_comparison_profiles(membership_df)
    subset_df = subset_df.loc[subset_df["component"].isin(MYELOID_COMPONENTS)].copy()
    return reset_profile_indices(subset_df), id_to_name


def build_pair_table(profiles_df: pd.DataFrame, gene_vocab: set[str], id_to_name: dict[str, str]) -> pd.DataFrame:
    gene_to_profiles: dict[str, list[int]] = defaultdict(list)
    for row in profiles_df.itertuples(index=False):
        for gene_id in row.marker_set & gene_vocab:
            gene_to_profiles[gene_id].append(int(row.profile_idx))

    pair_to_shared: dict[tuple[int, int], set[str]] = defaultdict(set)
    for gene_id, profile_indices in gene_to_profiles.items():
        for left_idx, right_idx in combinations(sorted(set(profile_indices)), 2):
            left = profiles_df.iloc[left_idx]
            right = profiles_df.iloc[right_idx]
            if left["paper_key"] == right["paper_key"]:
                continue
            pair_to_shared[(left_idx, right_idx)].add(gene_id)

    pair_rows = []
    for (left_idx, right_idx), shared_gene_ids in sorted(pair_to_shared.items()):
        left = profiles_df.iloc[left_idx]
        right = profiles_df.iloc[right_idx]
        left_markers = left["marker_set"]
        right_markers = right["marker_set"]
        union = left_markers | right_markers
        full_shared = left_markers & right_markers
        relation = label_relation(left["normalized_cell_type"], right["normalized_cell_type"])
        shared_gene_ids = sorted(shared_gene_ids)
        pair_rows.append(
            {
                "profile_idx_a": left_idx,
                "profile_idx_b": right_idx,
                "paper_key_a": left["paper_key"],
                "paper_key_b": right["paper_key"],
                "cell_type_a": left["cell_type"],
                "cell_type_b": right["cell_type"],
                "normalized_cell_type_a": left["normalized_cell_type"],
                "normalized_cell_type_b": right["normalized_cell_type"],
                "label_relation": relation,
                "label_linked": int(relation in {"Exact", "Partial"}),
                "n_markers_a": len(left_markers),
                "n_markers_b": len(right_markers),
                "n_shared": len(full_shared),
                "n_union": len(union),
                "jaccard": len(full_shared) / len(union) if union else 0.0,
                "shared_gene_ids": ";".join(shared_gene_ids),
                "shared_gene_names": ";".join(id_to_name.get(gene_id, gene_id) for gene_id in shared_gene_ids),
            }
        )
    return pd.DataFrame(pair_rows)


def sparse_pair_features(pair_df: pd.DataFrame, gene_to_col: dict[str, int]) -> csr_matrix:
    rows = []
    cols = []
    for row_idx, shared_gene_ids in enumerate(pair_df["shared_gene_ids"].map(split_marker_text)):
        for gene_id in shared_gene_ids:
            col_idx = gene_to_col.get(gene_id)
            if col_idx is None:
                continue
            rows.append(row_idx)
            cols.append(col_idx)
    data = np.ones(len(rows), dtype=np.float64)
    return csr_matrix((data, (rows, cols)), shape=(len(pair_df), len(gene_to_col)), dtype=np.float64)


def fit_model(x_train, y_train) -> LogisticRegression:
    model = LogisticRegression(
        penalty="l1",
        solver="liblinear",
        C=LOGISTIC_C,
        class_weight="balanced",
        max_iter=1000,
        random_state=RANDOM_SEED,
    )
    return model.fit(x_train, y_train)


def safe_scores(y_true: np.ndarray, scores: np.ndarray) -> tuple[float, float]:
    if len(np.unique(y_true)) < 2:
        return np.nan, np.nan
    return float(roc_auc_score(y_true, scores)), float(average_precision_score(y_true, scores))


def evaluate_heldout_papers(pair_df: pd.DataFrame, features: csr_matrix) -> pd.DataFrame:
    papers = sorted(set(pair_df["paper_key_a"]) | set(pair_df["paper_key_b"]))
    rng = np.random.default_rng(RANDOM_SEED)
    rows = []
    for split_idx in range(N_SPLITS):
        test_n = max(2, int(round(len(papers) * TEST_PAPER_FRACTION)))
        test_papers = set(rng.choice(papers, size=test_n, replace=False))
        train_mask = ~pair_df["paper_key_a"].isin(test_papers) & ~pair_df["paper_key_b"].isin(test_papers)
        test_mask = pair_df["paper_key_a"].isin(test_papers) & pair_df["paper_key_b"].isin(test_papers)
        train_idx = np.flatnonzero(train_mask.to_numpy())
        test_idx = np.flatnonzero(test_mask.to_numpy())
        if len(train_idx) < 100 or len(test_idx) < 20:
            continue
        y_train = pair_df.iloc[train_idx]["label_linked"].to_numpy()
        y_test = pair_df.iloc[test_idx]["label_linked"].to_numpy()
        if len(np.unique(y_train)) < 2 or len(np.unique(y_test)) < 2:
            continue

        model = fit_model(features[train_idx], y_train)
        weighted_scores = model.decision_function(features[test_idx])
        baselines = {
            "weighted shared genes": weighted_scores,
            "plain Jaccard": pair_df.iloc[test_idx]["jaccard"].to_numpy(),
            "shared gene count": pair_df.iloc[test_idx]["n_shared"].to_numpy(),
        }
        for model_name, scores in baselines.items():
            auroc, auprc = safe_scores(y_test, scores)
            rows.append(
                {
                    "split": split_idx,
                    "model": model_name,
                    "auroc": auroc,
                    "auprc": auprc,
                    "n_train_pairs": len(train_idx),
                    "n_test_pairs": len(test_idx),
                    "train_positive_fraction": float(y_train.mean()),
                    "test_positive_fraction": float(y_test.mean()),
                    "n_test_papers": len(test_papers),
                }
            )
    return pd.DataFrame(rows)


def gene_weight_table(
    pair_df: pd.DataFrame,
    features: csr_matrix,
    model: LogisticRegression,
    gene_vocab: list[str],
    profile_gene_counts: Counter[str],
    id_to_name: dict[str, str],
) -> pd.DataFrame:
    coefficients = model.coef_[0]
    background = float(pair_df["label_linked"].mean())
    rows = []
    csc = features.tocsc()
    for col_idx, gene_id in enumerate(gene_vocab):
        pair_indices = csc[:, col_idx].nonzero()[0]
        if len(pair_indices) == 0:
            continue
        linked_fraction = float(pair_df.iloc[pair_indices]["label_linked"].mean())
        rows.append(
            {
                "gene_id": gene_id,
                "gene_name": id_to_name.get(gene_id, gene_id),
                "coefficient": float(coefficients[col_idx]),
                "n_profiles_with_gene": int(profile_gene_counts[gene_id]),
                "n_shared_pairs_with_gene": int(len(pair_indices)),
                "label_linked_fraction_when_shared": linked_fraction,
                "background_label_linked_fraction": background,
                "label_linked_lift": linked_fraction / background if background else np.nan,
                "mean_jaccard_when_shared": float(pair_df.iloc[pair_indices]["jaccard"].mean()),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["coefficient", "n_shared_pairs_with_gene"],
        ascending=[False, False],
    )


def informative_label_terms(normalized_label: str) -> set[str]:
    terms = {
        term
        for term in label_tokens(normalized_label)
        if term != "cd" and term not in LABEL_TOKEN_STOPWORDS and not term.isdigit()
    }
    text = f" {normalized_label.upper()} "
    for match in re.finditer(r"\bCD\s*([0-9]+)\b", text):
        terms.add(f"CD{match.group(1)}")
    if re.search(r"\bT\s+CELL", text):
        terms.add("T_CELL")
    if re.search(r"\bB\s+CELL", text):
        terms.add("B_CELL")
    if re.search(r"\bNK\b|NATURAL\s+KILLER", text):
        terms.add("NK_CELL")
    return terms


def cross_paper_pair_count(values: list[str]) -> int:
    total = len(values) * (len(values) - 1) // 2
    same_paper = sum(count * (count - 1) // 2 for count in Counter(values).values())
    return total - same_paper


def build_label_token_scores(
    profiles_df: pd.DataFrame,
    pair_df: pd.DataFrame,
    min_label_token_pairs: int = MIN_LABEL_TOKEN_PAIRS,
) -> pd.DataFrame:
    profile_terms: dict[int, set[str]] = {}
    token_to_paper_counts: dict[str, Counter[str]] = defaultdict(Counter)
    token_profile_counts: Counter[str] = Counter()
    for row in profiles_df.itertuples(index=False):
        terms = informative_label_terms(row.normalized_cell_type)
        profile_terms[int(row.profile_idx)] = terms
        for token in terms:
            token_to_paper_counts[token][row.paper_key] += 1
            token_profile_counts[token] += 1

    all_pair_count = cross_paper_pair_count(profiles_df["paper_key"].tolist())
    background_marker_linked = len(pair_df) / all_pair_count if all_pair_count else 0.0
    background_jaccard = pair_df["jaccard"].sum() / all_pair_count if all_pair_count else 0.0

    token_marker_linked_counts: Counter[str] = Counter()
    token_jaccard_sums: dict[str, float] = defaultdict(float)
    for row in pair_df.itertuples(index=False):
        shared_terms = profile_terms[int(row.profile_idx_a)] & profile_terms[int(row.profile_idx_b)]
        for token in shared_terms:
            token_marker_linked_counts[token] += 1
            token_jaccard_sums[token] += float(row.jaccard)

    rows = []
    for token, paper_counts in sorted(token_to_paper_counts.items()):
        pair_count = cross_paper_pair_count(
            [
                paper_key
                for paper_key, count in paper_counts.items()
                for _ in range(count)
            ]
        )
        if pair_count < min_label_token_pairs:
            continue
        marker_linked_count = token_marker_linked_counts[token]
        jaccard_sum = token_jaccard_sums[token]
        marker_linked_fraction = marker_linked_count / pair_count
        mean_jaccard = jaccard_sum / pair_count if pair_count else 0.0
        rows.append(
            {
                "label_token": token,
                "display_label_token": token.replace("_", " "),
                "n_profiles_with_token": int(token_profile_counts[token]),
                "n_papers_with_token": len(paper_counts),
                "n_cross_paper_pairs_with_token": pair_count,
                "marker_linked_fraction": marker_linked_fraction,
                "background_marker_linked_fraction": background_marker_linked,
                "marker_linked_lift": marker_linked_fraction / background_marker_linked if background_marker_linked else np.nan,
                "mean_marker_jaccard": mean_jaccard,
                "background_mean_marker_jaccard": background_jaccard,
                "mean_marker_jaccard_lift": mean_jaccard / background_jaccard if background_jaccard else np.nan,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["marker_linked_lift", "n_cross_paper_pairs_with_token"],
        ascending=[False, False],
    )


def select_label_extremes(
    label_token_df: pd.DataFrame,
    high_n: int,
    low_n: int,
) -> pd.DataFrame:
    if label_token_df.empty:
        return label_token_df
    high_df = label_token_df.sort_values(
        ["marker_linked_fraction", "n_cross_paper_pairs_with_token"],
        ascending=[False, False],
    ).head(high_n)
    low_df = label_token_df.sort_values(
        ["marker_linked_fraction", "n_cross_paper_pairs_with_token"],
        ascending=[True, False],
    ).head(low_n)
    return (
        pd.concat([low_df, high_df], ignore_index=True)
        .drop_duplicates("label_token")
        .sort_values("marker_linked_fraction")
    )


def profile_gene_matrix(profiles_df: pd.DataFrame) -> tuple[csr_matrix, list[str]]:
    gene_vocab = sorted(set().union(*profiles_df["marker_set"].tolist()))
    gene_to_col = {gene_id: col_idx for col_idx, gene_id in enumerate(gene_vocab)}
    rows = []
    cols = []
    for row in profiles_df.itertuples(index=False):
        for gene_id in row.marker_set:
            rows.append(int(row.profile_idx))
            cols.append(gene_to_col[gene_id])
    data = np.ones(len(rows), dtype=np.float64)
    return csr_matrix((data, (rows, cols)), shape=(len(profiles_df), len(gene_vocab))), gene_vocab


def sparse_jaccard_similarity(marker_matrix: csr_matrix) -> csr_matrix:
    intersections = (marker_matrix @ marker_matrix.T).tocoo()
    marker_counts = np.asarray(marker_matrix.sum(axis=1)).ravel()
    unions = marker_counts[intersections.row] + marker_counts[intersections.col] - intersections.data
    similarities = np.divide(
        intersections.data,
        unions,
        out=np.zeros_like(intersections.data, dtype=np.float64),
        where=unions > 0,
    )
    return csr_matrix(
        (similarities, (intersections.row, intersections.col)),
        shape=intersections.shape,
    )


def build_label_silhouette_scores(
    profiles_df: pd.DataFrame,
    min_label_profiles: int,
) -> pd.DataFrame:
    label_counts_df = (
        profiles_df.groupby("normalized_cell_type")
        .agg(
            n_profiles=("profile_idx", "size"),
            n_papers=("paper_key", "nunique"),
            display_label=("cell_type", "first"),
        )
        .reset_index()
    )
    eligible_labels = set(
        label_counts_df.loc[
            label_counts_df["n_profiles"].ge(min_label_profiles)
            & label_counts_df["n_papers"].ge(2),
            "normalized_cell_type",
        ]
    )
    silhouette_profiles_df = profiles_df.loc[
        profiles_df["normalized_cell_type"].isin(eligible_labels)
    ].copy()
    if silhouette_profiles_df["normalized_cell_type"].nunique() < 2:
        return pd.DataFrame(
            columns=[
                "normalized_cell_type",
                "display_label",
                "n_profiles",
                "n_papers",
                "mean_silhouette",
                "mean_within_jaccard",
            ]
        )
    silhouette_profiles_df = reset_profile_indices(silhouette_profiles_df)
    marker_matrix, _gene_vocab = profile_gene_matrix(silhouette_profiles_df)
    similarity_matrix = sparse_jaccard_similarity(marker_matrix)

    labels = sorted(silhouette_profiles_df["normalized_cell_type"].unique())
    label_to_col = {label: col_idx for col_idx, label in enumerate(labels)}
    label_cols = silhouette_profiles_df["normalized_cell_type"].map(label_to_col).to_numpy()
    indicator = csr_matrix(
        (
            np.ones(len(silhouette_profiles_df), dtype=np.float64),
            (np.arange(len(silhouette_profiles_df)), label_cols),
        ),
        shape=(len(silhouette_profiles_df), len(labels)),
    )
    label_counts = np.asarray(indicator.sum(axis=0)).ravel()
    similarity_sums = (similarity_matrix @ indicator).toarray()
    mean_similarity_to_label = similarity_sums / label_counts

    same_counts = label_counts[label_cols] - 1
    same_similarity = np.divide(
        similarity_sums[np.arange(len(silhouette_profiles_df)), label_cols] - 1,
        same_counts,
        out=np.zeros(len(silhouette_profiles_df), dtype=np.float64),
        where=same_counts > 0,
    )
    own_masked_similarity = mean_similarity_to_label.copy()
    own_masked_similarity[np.arange(len(silhouette_profiles_df)), label_cols] = -np.inf
    nearest_other_similarity = np.max(own_masked_similarity, axis=1)

    a = 1 - same_similarity
    b = 1 - nearest_other_similarity
    silhouette = np.divide(
        b - a,
        np.maximum(a, b),
        out=np.zeros(len(silhouette_profiles_df), dtype=np.float64),
        where=np.maximum(a, b) > 0,
    )
    silhouette_profiles_df["silhouette"] = silhouette
    silhouette_profiles_df["within_jaccard"] = same_similarity

    rows = []
    for label, group_df in silhouette_profiles_df.groupby("normalized_cell_type"):
        display_label = label_counts_df.loc[
            label_counts_df["normalized_cell_type"].eq(label),
            "display_label",
        ].iloc[0]
        rows.append(
            {
                "normalized_cell_type": label,
                "display_label": display_label,
                "n_profiles": int(len(group_df)),
                "n_papers": int(group_df["paper_key"].nunique()),
                "mean_silhouette": float(group_df["silhouette"].mean()),
                "mean_within_jaccard": float(group_df["within_jaccard"].mean()),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["mean_silhouette", "n_profiles"],
        ascending=[False, False],
    )


def label_token_jaccard(left_label: str, right_label: str) -> float:
    if left_label == right_label:
        return 1.0
    left_terms = label_tokens(left_label)
    right_terms = label_tokens(right_label)
    union = left_terms | right_terms
    return len(left_terms & right_terms) / len(union) if union else 0.0


def build_marker_cluster_label_silhouette_scores(
    marker_cluster_summary_df: pd.DataFrame,
    marker_cluster_membership_df: pd.DataFrame,
) -> pd.DataFrame:
    if marker_cluster_summary_df.empty or marker_cluster_membership_df.empty:
        return pd.DataFrame(
            columns=[
                "cluster",
                "n_profiles",
                "n_papers",
                "n_labels",
                "dominant_label",
                "mean_label_silhouette",
                "mean_within_label_jaccard",
            ]
        )

    clustered_df = marker_cluster_membership_df.copy().reset_index(drop=True)
    cluster_ids = clustered_df["cluster"].astype(int).to_numpy()
    labels = clustered_df["normalized_cell_type"].tolist()
    n_profiles = len(clustered_df)
    label_similarity = np.eye(n_profiles, dtype=np.float64)
    for left_idx, right_idx in combinations(range(n_profiles), 2):
        similarity = label_token_jaccard(labels[left_idx], labels[right_idx])
        label_similarity[left_idx, right_idx] = similarity
        label_similarity[right_idx, left_idx] = similarity
    label_distance = 1 - label_similarity

    cluster_masks = {
        cluster_id: cluster_ids == cluster_id
        for cluster_id in sorted(set(cluster_ids))
    }
    sample_silhouette = np.zeros(n_profiles, dtype=np.float64)
    sample_within_similarity = np.zeros(n_profiles, dtype=np.float64)
    for idx, cluster_id in enumerate(cluster_ids):
        same_mask = cluster_masks[cluster_id].copy()
        same_mask[idx] = False
        if same_mask.sum() == 0:
            continue
        a = float(label_distance[idx, same_mask].mean())
        sample_within_similarity[idx] = float(label_similarity[idx, same_mask].mean())
        other_distances = [
            float(label_distance[idx, mask].mean())
            for other_cluster, mask in cluster_masks.items()
            if other_cluster != cluster_id and mask.any()
        ]
        if not other_distances:
            continue
        b = min(other_distances)
        denominator = max(a, b)
        sample_silhouette[idx] = (b - a) / denominator if denominator > 0 else 0.0

    clustered_df["label_silhouette"] = sample_silhouette
    clustered_df["within_label_jaccard"] = sample_within_similarity
    summary_lookup = marker_cluster_summary_df.set_index("cluster")
    rows = []
    for cluster_id, group_df in clustered_df.groupby("cluster"):
        summary_row = summary_lookup.loc[int(cluster_id)]
        rows.append(
            {
                "cluster": int(cluster_id),
                "n_profiles": int(summary_row["n_profiles"]),
                "n_papers": int(summary_row["n_papers"]),
                "n_labels": int(summary_row["n_labels"]),
                "dominant_label": summary_row["dominant_label"],
                "mean_label_silhouette": float(group_df["label_silhouette"].mean()),
                "mean_within_label_jaccard": float(group_df["within_label_jaccard"].mean()),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["mean_label_silhouette", "n_profiles"],
        ascending=[False, False],
    )


def group_gene_scores(
    profiles_df: pd.DataFrame,
    profile_indices: set[int],
    id_to_name: dict[str, str],
    group_name: str,
) -> pd.DataFrame:
    profile_gene_sets = profiles_df.set_index("profile_idx")["marker_set"].to_dict()
    all_profile_count = len(profiles_df)
    global_gene_counts = Counter(
        gene_id
        for marker_set in profiles_df["marker_set"]
        for gene_id in marker_set
    )
    group_n = len(profile_indices)
    outside_n = all_profile_count - group_n
    group_gene_counts = Counter(
        gene_id
        for profile_idx in profile_indices
        for gene_id in profile_gene_sets[profile_idx]
    )
    rows = []
    for gene_id, in_count in group_gene_counts.items():
        global_count = global_gene_counts[gene_id]
        outside_count = max(global_count - in_count, 0)
        coverage = in_count / group_n if group_n else 0.0
        purity = in_count / global_count if global_count else 0.0
        outside_prevalence = outside_count / outside_n if outside_n else 0.0
        harmonic = (
            2 * coverage * purity / (coverage + purity)
            if coverage + purity > 0
            else 0.0
        )
        rows.append(
            {
                "group_name": group_name,
                "gene_id": gene_id,
                "gene_name": id_to_name.get(gene_id, gene_id),
                "n_profiles_group": group_n,
                "n_profiles_with_gene_in_group": in_count,
                "n_profiles_with_gene_global": global_count,
                "coverage": coverage,
                "purity": purity,
                "outside_prevalence": outside_prevalence,
                "coverage_purity_hmean": harmonic,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["coverage_purity_hmean", "coverage", "purity"],
        ascending=[False, False, False],
    )


def profile_uid(row: pd.Series) -> str:
    return f"{row['source_corpus']}|{row['paper_id']}|{row['cell_type']}"


def build_tcell_marker_groups(
    profiles_df: pd.DataFrame,
    id_to_name: dict[str, str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    tcell_df = profiles_df.copy()
    tcell_df["neighborhood"] = tcell_df["cell_type"].map(assign_neighborhood)
    tcell_df = tcell_df.loc[tcell_df["neighborhood"].eq("T cell")].copy().reset_index(drop=True)
    if tcell_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    profile_gene_sets = tcell_marker_sets(tcell_df)
    gene_vocab = sorted(set().union(*profile_gene_sets)) if profile_gene_sets else []
    records_df = build_records()
    name_to_ids = build_tcell_name_to_ids(records_df)
    module_genes_df = tcell_module_gene_rows(name_to_ids, set(gene_vocab))
    module_scores_df = profile_module_scores(profile_gene_sets, module_genes_df)
    tcell_df["profile_index"] = np.arange(len(tcell_df))
    tcell_df = tcell_df.merge(module_scores_df, on="profile_index", how="left")

    components, edges = connected_components(
        profile_gene_sets,
        tcell_df["paper_key"].tolist(),
        threshold=TCELL_MARKER_CLUSTER_JACCARD,
    )
    summary_df = summarize_tcell_components(tcell_df, profile_gene_sets, id_to_name, components, edges)
    membership_df = tcell_component_memberships(tcell_df, components, summary_df)
    return summary_df, membership_df


def build_tcell_label_gene_reference(
    profiles_df: pd.DataFrame,
    tcell_membership_df: pd.DataFrame,
    id_to_name: dict[str, str],
    min_label_profiles: int = MIN_LABEL_PROFILE_COUNT,
) -> pd.DataFrame:
    if tcell_membership_df.empty:
        return pd.DataFrame()

    uid_to_profile_idx = profiles_df.set_index("profile_uid")["profile_idx"].astype(int).to_dict()
    membership_df = tcell_membership_df.copy()
    membership_df["profile_uid"] = membership_df.apply(profile_uid, axis=1)
    tcell_profile_indices = set(membership_df["profile_uid"].map(uid_to_profile_idx).dropna().astype(int))
    tcell_df = profiles_df.loc[profiles_df["profile_idx"].isin(tcell_profile_indices)].copy()
    label_counts = tcell_df["normalized_cell_type"].value_counts()
    eligible_labels = label_counts.loc[label_counts >= min_label_profiles].index.tolist()

    label_tables = []
    for label in eligible_labels:
        label_profile_indices = set(
            profiles_df.loc[profiles_df["normalized_cell_type"].eq(label), "profile_idx"].astype(int)
        )
        scores_df = group_gene_scores(
            profiles_df,
            label_profile_indices,
            id_to_name,
            f"label {label}",
        )
        if scores_df.empty:
            continue
        scores_df["label_group"] = label
        label_tables.append(scores_df)

    if not label_tables:
        return pd.DataFrame()

    all_scores = pd.concat(label_tables, ignore_index=True)
    best_rows = (
        all_scores.sort_values(
            ["coverage_purity_hmean", "coverage", "purity", "n_profiles_group"],
            ascending=[False, False, False, False],
        )
        .drop_duplicates("gene_id")
        .rename(
            columns={
                "label_group": "best_label_group",
                "coverage_purity_hmean": "best_label_f1",
                "coverage": "best_label_coverage",
                "purity": "best_label_purity",
                "n_profiles_group": "best_label_n_profiles",
            }
        )
    )
    return best_rows[
        [
            "gene_id",
            "gene_name",
            "best_label_group",
            "best_label_f1",
            "best_label_coverage",
            "best_label_purity",
            "best_label_n_profiles",
        ]
    ]


def marker_to_label_ratio(marker_f1: float, label_f1: float) -> float:
    if label_f1 == 0:
        return np.inf if marker_f1 > 0 else 1.0
    return marker_f1 / label_f1


def marker_to_label_log2_ratio(marker_f1: float, label_f1: float) -> float:
    return float(
        np.log2(
            (marker_f1 + TCELL_GENE_F1_PSEUDOCOUNT)
            / (label_f1 + TCELL_GENE_F1_PSEUDOCOUNT)
        )
    )


def classify_tcell_gene_shift(marker_f1: float, label_f1: float) -> str:
    if marker_f1 >= 0.25 and label_f1 >= 0.25:
        return "high in both"
    if marker_f1 >= 0.12 and marker_f1 >= label_f1 * 1.5:
        return "marker-cluster enriched"
    if label_f1 >= 0.12 and label_f1 >= marker_f1 * 1.5:
        return "label enriched"
    return "weak or similar"


def build_tcell_gene_f1_tables(
    profiles_df: pd.DataFrame,
    id_to_name: dict[str, str],
    tcell_summary_df: pd.DataFrame,
    tcell_membership_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if tcell_summary_df.empty or tcell_membership_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    uid_to_profile_idx = profiles_df.set_index("profile_uid")["profile_idx"].astype(int).to_dict()
    membership_df = tcell_membership_df.copy()
    membership_df["profile_uid"] = membership_df.apply(profile_uid, axis=1)
    membership_df["global_profile_idx"] = membership_df["profile_uid"].map(uid_to_profile_idx)
    membership_df = membership_df.dropna(subset=["global_profile_idx"])
    membership_df["global_profile_idx"] = membership_df["global_profile_idx"].astype(int)

    label_reference_df = build_tcell_label_gene_reference(
        profiles_df,
        membership_df,
        id_to_name,
    )
    label_reference = label_reference_df.set_index("gene_id").to_dict("index") if not label_reference_df.empty else {}
    summary_by_component = tcell_summary_df.set_index("component").to_dict("index")

    rows = []
    for component, component_df in membership_df.groupby("component", sort=True):
        profile_indices = set(component_df["global_profile_idx"].astype(int))
        marker_scores = group_gene_scores(
            profiles_df,
            profile_indices,
            id_to_name,
            f"T-cell marker cluster C{component}",
        )
        if marker_scores.empty:
            continue
        summary = summary_by_component.get(component, {})
        for row in marker_scores.itertuples(index=False):
            label_ref = label_reference.get(row.gene_id, {})
            best_label_f1 = float(label_ref.get("best_label_f1", 0.0) or 0.0)
            marker_f1 = float(row.coverage_purity_hmean)
            rows.append(
                {
                    "component": int(component),
                    "dominant_program": summary.get("dominant_program"),
                    "n_profiles_cluster": int(row.n_profiles_group),
                    "n_papers_cluster": summary.get("papers"),
                    "n_labels_cluster": summary.get("labels"),
                    "top_labels": summary.get("top_labels"),
                    "core_marker_genes": summary.get("core_marker_genes"),
                    "gene_id": row.gene_id,
                    "gene_name": row.gene_name,
                    "marker_cluster_f1": marker_f1,
                    "marker_cluster_coverage": row.coverage,
                    "marker_cluster_purity": row.purity,
                    "marker_cluster_gene_count": int(row.n_profiles_with_gene_in_group),
                    "global_gene_count": int(row.n_profiles_with_gene_global),
                    "best_label_f1": best_label_f1,
                    "best_label_group": label_ref.get("best_label_group"),
                    "best_label_coverage": label_ref.get("best_label_coverage", 0.0),
                    "best_label_purity": label_ref.get("best_label_purity", 0.0),
                    "best_label_n_profiles": label_ref.get("best_label_n_profiles", 0),
                    "marker_to_label_f1_ratio": marker_to_label_ratio(marker_f1, best_label_f1),
                    "log2_marker_to_label_f1_ratio": marker_to_label_log2_ratio(marker_f1, best_label_f1),
                    "shift_class": classify_tcell_gene_shift(marker_f1, best_label_f1),
                }
            )

    cluster_gene_df = pd.DataFrame(rows)
    if cluster_gene_df.empty:
        return cluster_gene_df, pd.DataFrame()
    cluster_gene_df = cluster_gene_df.sort_values(
        ["component", "log2_marker_to_label_f1_ratio", "marker_cluster_f1"],
        ascending=[True, False, False],
    )
    gene_summary_df = (
        cluster_gene_df.sort_values(
            ["marker_cluster_f1", "log2_marker_to_label_f1_ratio"],
            ascending=[False, False],
        )
        .drop_duplicates("gene_id")
        .sort_values(["log2_marker_to_label_f1_ratio", "marker_cluster_f1"], ascending=[False, False])
        .reset_index(drop=True)
    )
    return cluster_gene_df, gene_summary_df


def select_marker_cluster_for_label(
    marker_cluster_summary_df: pd.DataFrame,
    label: str,
) -> int:
    exact_df = marker_cluster_summary_df.loc[
        marker_cluster_summary_df["dominant_label"].eq(label)
    ].copy()
    if exact_df.empty:
        contains_df = marker_cluster_summary_df.loc[
            marker_cluster_summary_df["top_labels"].str.contains(label, case=False, regex=False)
        ].copy()
        if contains_df.empty:
            raise SystemExit(f"No marker cluster was found for label {label!r}.")
        exact_df = contains_df
    return int(exact_df.sort_values("n_profiles", ascending=False).iloc[0]["cluster"])


def example_label_profile_indices(profiles_df: pd.DataFrame, example: dict[str, str]) -> set[int]:
    if "label" in example:
        mask = profiles_df["normalized_cell_type"].eq(example["label"])
    elif "label_contains" in example:
        mask = profiles_df["normalized_cell_type"].str.contains(
            example["label_contains"],
            case=False,
            regex=False,
            na=False,
        )
    else:
        raise ValueError(f"Example {example['key']!r} needs a label or label_contains field.")
    return set(profiles_df.loc[mask, "profile_idx"].astype(int))


def add_gene_coverage_panel(
    ax,
    gene_scores_df: pd.DataFrame,
    title: str,
    max_labels: int = 7,
) -> None:
    plot_df = gene_scores_df.copy()
    ax.set_title(title, loc="left", fontsize=8.2, fontweight="bold", pad=5)
    if plot_df.empty:
        ax.text(0.5, 0.5, "No genes in group", ha="center", va="center", fontsize=7.0)
        ax.axis("off")
        return

    ax.scatter(
        plot_df["coverage"],
        plot_df["purity"],
        s=16 + 4 * np.sqrt(plot_df["n_profiles_with_gene_global"]),
        color="#d9d9d9",
        edgecolor="#222222",
        linewidth=0.42,
        alpha=0.9,
        zorder=2,
    )
    label_df = plot_df.head(max_labels)
    for idx, row in enumerate(label_df.itertuples(index=False)):
        y_offset = 4 if idx % 2 == 0 else -7
        ax.annotate(
            row.gene_name,
            (row.coverage, row.purity),
            xytext=(5, y_offset),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=5.8,
            arrowprops={"arrowstyle": "-", "linewidth": 0.25, "color": "#777777"},
        )

    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Coverage", fontsize=7.0)
    ax.set_ylabel("Purity", fontsize=7.0)
    ax.tick_params(axis="x", labelsize=6.0, length=2, width=0.5)
    ax.tick_params(axis="y", labelsize=6.0, length=2, width=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)


def compare_group_gene_f1(
    label_group_gene_scores_df: pd.DataFrame,
    marker_group_gene_scores_df: pd.DataFrame,
) -> pd.DataFrame:
    left_df = label_group_gene_scores_df[
        ["gene_id", "gene_name", "coverage_purity_hmean"]
    ].rename(columns={"coverage_purity_hmean": "label_group_f1"})
    right_df = marker_group_gene_scores_df[
        ["gene_id", "gene_name", "coverage_purity_hmean"]
    ].rename(columns={"coverage_purity_hmean": "marker_group_f1"})
    comparison_df = left_df.merge(
        right_df,
        on=["gene_id", "gene_name"],
        how="outer",
    ).fillna({"label_group_f1": 0.0, "marker_group_f1": 0.0})
    comparison_df["delta_marker_minus_label"] = (
        comparison_df["marker_group_f1"] - comparison_df["label_group_f1"]
    )
    return comparison_df.sort_values(
        "delta_marker_minus_label",
        ascending=False,
    )


def add_group_gene_f1_panel(
    ax,
    f1_comparison_df: pd.DataFrame,
    title: str,
    max_labels_each_side: int = 4,
) -> None:
    plot_df = f1_comparison_df.copy()
    ax.set_title(title, loc="left", fontsize=8.2, fontweight="bold", pad=5)
    if plot_df.empty:
        ax.text(0.5, 0.5, "No shared genes to compare", ha="center", va="center", fontsize=7.0)
        ax.axis("off")
        return

    sector_specs = [
        (0.0, 0.5, 0.5, 0.5, "#d7ecd0", "Marker-cluster enriched"),
        (0.5, 0.0, 0.5, 0.5, "#f6d7bd", "Label enriched"),
        (0.5, 0.5, 0.5, 0.5, "#d6e7f2", "Shared high F1"),
        (0.0, 0.0, 0.5, 0.5, "#f0f0f0", "Weak in both"),
    ]
    for x, y, width, height, color, _label in sector_specs:
        ax.add_patch(
            Rectangle(
                (x, y),
                width,
                height,
                facecolor=color,
                edgecolor="none",
                alpha=0.32,
                zorder=0,
            )
        )
    ax.plot([0, 1], [0, 1], color="#777777", linewidth=0.65, linestyle="--", zorder=1)
    ax.plot([0, 1], [1, 0], color="#bdbdbd", linewidth=0.55, linestyle="--", zorder=1)
    ax.axvline(0.5, color="#bdbdbd", linewidth=0.55, linestyle="--", zorder=1)
    ax.axhline(0.5, color="#bdbdbd", linewidth=0.55, linestyle="--", zorder=1)
    ax.scatter(
        plot_df["label_group_f1"],
        plot_df["marker_group_f1"],
        s=24,
        color="#d9d9d9",
        edgecolor="#222222",
        linewidth=0.42,
        alpha=0.9,
        zorder=2,
    )
    label_df = pd.concat(
        [
            plot_df.sort_values("delta_marker_minus_label", ascending=False).head(max_labels_each_side),
            plot_df.sort_values("delta_marker_minus_label", ascending=True).head(max_labels_each_side),
            plot_df.sort_values(["label_group_f1", "marker_group_f1"], ascending=False).head(3),
        ],
        ignore_index=True,
    ).drop_duplicates("gene_id")
    for idx, row in enumerate(label_df.itertuples(index=False)):
        y_offset = 4 if idx % 2 == 0 else -7
        ax.annotate(
            row.gene_name,
            (row.label_group_f1, row.marker_group_f1),
            xytext=(5, y_offset),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=5.8,
            arrowprops={"arrowstyle": "-", "linewidth": 0.25, "color": "#777777"},
        )

    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("F1 in label group", fontsize=7.0)
    ax.set_ylabel("F1 in marker cluster", fontsize=7.0)
    legend_handles = [
        Patch(facecolor=color, edgecolor="none", alpha=0.45, label=label)
        for _x, _y, _width, _height, color, label in sector_specs
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.24),
        ncol=2,
        frameon=False,
        fontsize=5.5,
        handlelength=1.1,
        columnspacing=0.9,
        handletextpad=0.35,
    )
    ax.tick_params(axis="x", labelsize=6.0, length=2, width=0.5)
    ax.tick_params(axis="y", labelsize=6.0, length=2, width=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)


def add_tcell_gene_f1_panel(
    ax,
    gene_summary_df: pd.DataFrame,
    title: str,
) -> None:
    ax.set_title(title, loc="left", fontsize=8.2, fontweight="bold", pad=5)
    if gene_summary_df.empty:
        ax.text(0.5, 0.5, "No T-cell genes to compare", ha="center", va="center", fontsize=7.0)
        ax.axis("off")
        return

    colors = {
        "marker-cluster enriched": "#7fbf7b",
        "label enriched": "#ef8a62",
        "high in both": "#67a9cf",
        "weak or similar": "#d9d9d9",
    }
    plot_df = gene_summary_df.loc[
        gene_summary_df["marker_cluster_f1"].ge(0.08)
        | gene_summary_df["best_label_f1"].ge(0.08)
    ].copy()
    if plot_df.empty:
        plot_df = gene_summary_df.copy()
    plot_df["delta_marker_minus_label"] = plot_df["marker_cluster_f1"] - plot_df["best_label_f1"]
    plot_df["min_f1"] = plot_df[["marker_cluster_f1", "best_label_f1"]].min(axis=1)

    for shift_class, group_df in plot_df.groupby("shift_class", sort=False):
        ax.scatter(
            group_df["best_label_f1"],
            group_df["marker_cluster_f1"],
            s=18,
            color=colors.get(shift_class, "#d9d9d9"),
            edgecolor="#222222",
            linewidth=0.35,
            alpha=0.9,
            label=shift_class,
            zorder=2,
        )
    ax.plot([0, 1], [0, 1], color="#777777", linewidth=0.65, linestyle="--", zorder=1)

    marker_extreme_df = (
        plot_df.loc[
            plot_df["shift_class"].eq("marker-cluster enriched")
            & plot_df["marker_cluster_f1"].ge(0.12)
        ]
        .sort_values("delta_marker_minus_label", ascending=False)
        .head(8)
    )
    label_extreme_df = (
        plot_df.loc[plot_df["shift_class"].eq("label enriched")]
        .sort_values("delta_marker_minus_label", ascending=True)
        .head(4)
    )
    shared_extreme_df = (
        plot_df.loc[plot_df["shift_class"].eq("high in both")]
        .sort_values(["min_f1", "marker_cluster_f1"], ascending=[False, False])
        .head(5)
    )
    shared_marker_extreme_df = (
        plot_df.loc[plot_df["shift_class"].eq("high in both")]
        .sort_values("marker_cluster_f1", ascending=False)
        .head(1)
    )
    extreme_df = (
        pd.concat(
            [marker_extreme_df, label_extreme_df, shared_extreme_df, shared_marker_extreme_df],
            ignore_index=True,
        )
        .drop_duplicates("gene_id")
    )
    if not extreme_df.empty:
        ax.scatter(
            extreme_df["best_label_f1"],
            extreme_df["marker_cluster_f1"],
            s=42,
            facecolors="none",
            edgecolor="#111111",
            linewidth=0.85,
            alpha=1.0,
            zorder=4,
        )

    label_genes = [
        "SELL",
        "CCR7",
        "HAVCR2",
        "PRF1",
        "GZMB",
        "ZNF683",
        "CD3G",
        "FOXP3",
        "CD3D",
        "BATF",
        "TNFRSF4",
        "TNFRSF9",
        "CD8B",
    ]
    label_genes = [gene for gene in label_genes if gene in set(extreme_df["gene_name"])]
    label_df = plot_df.loc[plot_df["gene_name"].isin(label_genes)].copy()
    label_df["label_order"] = label_df["gene_name"].map({gene: idx for idx, gene in enumerate(label_genes)})
    label_df = label_df.sort_values("label_order")
    label_positions = {
        "SELL": (0.31, 0.74),
        "CD3G": (0.39, 0.70),
        "CCR7": (0.31, 0.60),
        "HAVCR2": (0.31, 0.50),
        "GZMB": (0.31, 0.38),
        "PRF1": (0.31, 0.27),
        "ZNF683": (0.31, 0.16),
        "FOXP3": (0.69, 0.49),
        "CD3D": (0.69, 0.60),
        "TNFRSF4": (0.58, 0.28),
        "BATF": (0.58, 0.20),
        "TNFRSF9": (0.58, 0.12),
        "CD8B": (0.58, 0.04),
    }
    for idx, row in enumerate(label_df.itertuples(index=False)):
        text_x, text_y = label_positions.get(
            row.gene_name,
            (
                min(0.95, row.best_label_f1 + 0.16),
                min(0.96, max(0.04, row.marker_cluster_f1 + (0.07 if idx % 2 == 0 else -0.07))),
            ),
        )
        ax.annotate(
            row.gene_name,
            (row.best_label_f1, row.marker_cluster_f1),
            xytext=(text_x, text_y),
            textcoords="data",
            ha="left",
            va="center",
            fontsize=5.6,
            bbox={
                "boxstyle": "round,pad=0.12",
                "facecolor": "white",
                "edgecolor": "none",
                "alpha": 0.85,
            },
            arrowprops={
                "arrowstyle": "-",
                "linewidth": 0.35,
                "color": "#555555",
                "shrinkA": 2.5,
                "shrinkB": 2.5,
            },
            annotation_clip=False,
            zorder=5,
        )

    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Best F1 in repeated T-cell label", fontsize=7.0)
    ax.set_ylabel("Best F1 in T-cell marker cluster", fontsize=7.0)
    ax.tick_params(axis="x", labelsize=6.0, length=2, width=0.5)
    ax.tick_params(axis="y", labelsize=6.0, length=2, width=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.24),
        ncol=2,
        frameon=False,
        fontsize=5.4,
        handlelength=1.1,
        columnspacing=0.8,
        handletextpad=0.35,
    )


def run_nomenclature_model(
    profiles_df: pd.DataFrame,
    id_to_name: dict[str, str],
    min_gene_profile_count: int,
    min_label_token_pairs: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, csr_matrix, LogisticRegression, list[str]]:
    profile_gene_counts = Counter(gene_id for marker_set in profiles_df["marker_set"] for gene_id in marker_set)
    gene_vocab = sorted(
        gene_id
        for gene_id, count in profile_gene_counts.items()
        if count >= min_gene_profile_count
    )
    pair_df = build_pair_table(profiles_df, set(gene_vocab), id_to_name)
    if pair_df.empty:
        raise SystemExit("No cross-paper pairs with shared marker genes were found.")

    gene_to_col = {gene_id: idx for idx, gene_id in enumerate(gene_vocab)}
    features = sparse_pair_features(pair_df, gene_to_col)
    y = pair_df["label_linked"].to_numpy()
    if len(np.unique(y)) < 2:
        raise SystemExit("Cannot fit nomenclature model because label-linked target has one class.")

    model = fit_model(features, y)
    pair_df["weighted_gene_score"] = model.decision_function(features)
    pair_df["weighted_gene_probability"] = model.predict_proba(features)[:, 1]
    gene_weights_df = gene_weight_table(
        pair_df,
        features,
        model,
        gene_vocab,
        profile_gene_counts,
        id_to_name,
    )
    label_token_df = build_label_token_scores(
        profiles_df,
        pair_df,
        min_label_token_pairs=min_label_token_pairs,
    )
    return pair_df, gene_weights_df, label_token_df, features, model, gene_vocab


def add_metric_panel(ax, cv_metrics_df: pd.DataFrame) -> None:
    ax.set_title("Held-out paper prediction", loc="left", fontsize=9.0, fontweight="bold", pad=6)
    model_order = ["plain Jaccard", "shared gene count", "weighted shared genes"]
    metric_order = [("auroc", "AUROC"), ("auprc", "AUPRC")]
    colors = {
        "plain Jaccard": "#d9d9d9",
        "shared gene count": "#bdbdbd",
        "weighted shared genes": "#222222",
    }
    x_positions = []
    x_labels = []
    bar_values = []
    bar_colors = []
    for metric_idx, (metric, metric_label) in enumerate(metric_order):
        base_x = metric_idx * (len(model_order) + 1)
        for model_idx, model_name in enumerate(model_order):
            x = base_x + model_idx
            values = cv_metrics_df.loc[cv_metrics_df["model"].eq(model_name), metric].dropna()
            x_positions.append(x)
            x_labels.append(model_name.replace(" ", "\n"))
            bar_values.append(values.mean())
            bar_colors.append(colors[model_name])
            ax.scatter(
                np.full(len(values), x) + np.linspace(-0.11, 0.11, max(len(values), 1))[: len(values)],
                values,
                s=12,
                color="white" if model_name == "weighted shared genes" else "#222222",
                edgecolor="#222222",
                linewidth=0.45,
                zorder=3,
            )
        ax.text(
            base_x + 1,
            1.05,
            metric_label,
            ha="center",
            va="bottom",
            fontsize=7.0,
            fontweight="bold",
        )
    ax.bar(x_positions, bar_values, width=0.66, color=bar_colors, edgecolor="#222222", linewidth=0.6, zorder=2)
    ax.set_xticks(x_positions)
    ax.set_xticklabels(x_labels, fontsize=5.5)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("Score", fontsize=7.0)
    ax.tick_params(axis="y", labelsize=6.0, length=2, width=0.5)
    ax.tick_params(axis="x", length=0, pad=2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)


def add_weight_panel(ax, gene_weights_df: pd.DataFrame) -> None:
    display_df = gene_weights_df.loc[
        gene_weights_df["n_shared_pairs_with_gene"].ge(MIN_SHARED_PAIRS_FOR_DISPLAY)
        & gene_weights_df["coefficient"].ne(0)
    ].copy()
    positive = display_df.sort_values("coefficient", ascending=False).head(10)
    negative = display_df.sort_values("coefficient", ascending=True).head(10)
    plot_df = pd.concat([negative, positive], ignore_index=True).sort_values("coefficient")
    colors = np.where(plot_df["coefficient"].ge(0), "#4c9a2a", "#9e9e9e")

    ax.set_title("Gene weights for shared nomenclature", loc="left", fontsize=9.0, fontweight="bold", pad=6)
    y = np.arange(len(plot_df))
    ax.barh(y, plot_df["coefficient"], color=colors, edgecolor="#222222", linewidth=0.45)
    ax.axvline(0, color="#222222", linewidth=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(plot_df["gene_name"], fontsize=6.1)
    ax.set_xlabel("Logistic coefficient", fontsize=7.0)
    ax.tick_params(axis="x", labelsize=6.0, length=2, width=0.5)
    ax.tick_params(axis="y", length=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)


def add_label_token_panel(
    ax,
    label_token_df: pd.DataFrame,
    title: str,
    high_n: int = 10,
    low_n: int = 4,
    support_n: int = 2,
    annotate_all: bool = False,
) -> None:
    plot_df = label_token_df.copy()
    ax.set_title(title, loc="left", fontsize=8.2, fontweight="bold", pad=5)
    if plot_df.empty:
        ax.text(0.5, 0.5, "No label terms passed filter", ha="center", va="center", fontsize=7.0)
        ax.axis("off")
        return

    ax.scatter(
        plot_df["n_cross_paper_pairs_with_token"],
        plot_df["mean_marker_jaccard"],
        s=34,
        color="#d9d9d9",
        edgecolor="#222222",
        linewidth=0.45,
        alpha=0.9,
        zorder=2,
    )
    background = float(plot_df["background_mean_marker_jaccard"].iloc[0])
    ax.axhline(background, color="#777777", linewidth=0.75, linestyle="--", zorder=1)

    if annotate_all:
        annotate_df = plot_df
    else:
        high_df = plot_df.sort_values(
            ["mean_marker_jaccard", "n_cross_paper_pairs_with_token"],
            ascending=[False, False],
        ).head(high_n)
        low_df = plot_df.sort_values(
            ["mean_marker_jaccard", "n_cross_paper_pairs_with_token"],
            ascending=[True, False],
        ).head(low_n)
        support_df = plot_df.sort_values("n_cross_paper_pairs_with_token", ascending=False).head(support_n)
        annotate_df = (
            pd.concat([high_df, low_df, support_df], ignore_index=True)
            .drop_duplicates("label_token")
        )
    for idx, row in enumerate(annotate_df.itertuples(index=False)):
        y_offset = 4 if idx % 2 == 0 else -7
        ax.annotate(
            f"{row.display_label_token}\n(n={int(row.n_cross_paper_pairs_with_token):,})",
            (row.n_cross_paper_pairs_with_token, row.mean_marker_jaccard),
            xytext=(4, y_offset),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=5.8,
            arrowprops={"arrowstyle": "-", "linewidth": 0.25, "color": "#777777"},
        )

    x_min = max(1, plot_df["n_cross_paper_pairs_with_token"].min() * 0.75)
    x_max = plot_df["n_cross_paper_pairs_with_token"].max() * 1.45
    ax.set_xscale("log")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, min(1.0, max(0.08, plot_df["mean_marker_jaccard"].max() * 1.22)))
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
    ax.set_xlabel("Cross-paper profile pairs sharing label term", fontsize=7.0)
    ax.set_ylabel("Mean marker-gene Jaccard", fontsize=7.0)
    ax.tick_params(axis="x", labelsize=6.0, length=2, width=0.5)
    ax.tick_params(axis="y", labelsize=6.0, length=2, width=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)


def add_label_silhouette_panel(
    ax,
    label_silhouette_df: pd.DataFrame,
    title: str,
    high_n: int = 6,
    low_n: int = 2,
    support_n: int = 2,
    annotate_all: bool = False,
) -> None:
    plot_df = label_silhouette_df.copy()
    ax.set_title(title, loc="left", fontsize=8.2, fontweight="bold", pad=5)
    if plot_df.empty:
        ax.text(0.5, 0.5, "No labels passed filter", ha="center", va="center", fontsize=7.0)
        ax.axis("off")
        return

    ax.scatter(
        plot_df["n_profiles"],
        plot_df["mean_silhouette"],
        s=17,
        color="#d9d9d9",
        edgecolor="#222222",
        linewidth=0.45,
        alpha=0.9,
        zorder=2,
    )
    ax.axhline(0, color="#777777", linewidth=0.75, linestyle="--", zorder=1)

    if annotate_all:
        annotate_df = plot_df
    else:
        high_df = plot_df.sort_values(
            ["mean_silhouette", "n_profiles"],
            ascending=[False, False],
        ).head(high_n)
        low_df = plot_df.sort_values(
            ["mean_silhouette", "n_profiles"],
            ascending=[True, False],
        ).head(low_n)
        support_df = plot_df.sort_values("n_profiles", ascending=False).head(support_n)
        annotate_df = (
            pd.concat([high_df, low_df, support_df], ignore_index=True)
            .drop_duplicates("normalized_cell_type")
        )
    for idx, row in enumerate(annotate_df.itertuples(index=False)):
        y_offset = 4 if idx % 2 == 0 else -7
        ax.annotate(
            f"{row.display_label}\n(n={int(row.n_profiles):,})",
            (row.n_profiles, row.mean_silhouette),
            xytext=(4, y_offset),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=5.8,
            arrowprops={"arrowstyle": "-", "linewidth": 0.25, "color": "#777777"},
        )

    x_min = max(1, plot_df["n_profiles"].min() * 0.75)
    x_max = plot_df["n_profiles"].max() * 1.6
    ax.set_xscale("log")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-1, 1)
    ax.set_xlabel("Profiles with exact label", fontsize=7.0)
    ax.set_ylabel("Mean silhouette\n(marker Jaccard distance)", fontsize=7.0)
    ax.tick_params(axis="x", labelsize=6.0, length=2, width=0.5)
    ax.tick_params(axis="y", labelsize=6.0, length=2, width=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)


def add_marker_cluster_label_silhouette_panel(
    ax,
    cluster_label_silhouette_df: pd.DataFrame,
    title: str,
    support_n: int = 3,
    high_n: int = 3,
    low_n: int = 2,
) -> None:
    plot_df = cluster_label_silhouette_df.copy()
    ax.set_title(title, loc="left", fontsize=8.2, fontweight="bold", pad=5)
    if plot_df.empty:
        ax.text(0.5, 0.5, "No marker clusters passed filter", ha="center", va="center", fontsize=7.0)
        ax.axis("off")
        return

    ax.scatter(
        plot_df["n_profiles"],
        plot_df["mean_label_silhouette"],
        s=18 + 5 * np.sqrt(plot_df["n_papers"]),
        color="#d9d9d9",
        edgecolor="#222222",
        linewidth=0.45,
        alpha=0.9,
        zorder=2,
    )
    annotate_df = pd.concat(
        [
            plot_df.sort_values("n_profiles", ascending=False).head(support_n),
            plot_df.sort_values("mean_label_silhouette", ascending=False).head(high_n),
            plot_df.sort_values("mean_label_silhouette", ascending=True).head(low_n),
        ],
        ignore_index=True,
    ).drop_duplicates("cluster")
    for idx, row in enumerate(annotate_df.itertuples(index=False)):
        y_offset = -9 if row.mean_label_silhouette > 0.82 else (4 if idx % 2 == 0 else -7)
        ax.annotate(
            f"C{int(row.cluster)}\n{row.dominant_label}",
            (row.n_profiles, row.mean_label_silhouette),
            xytext=(4, y_offset),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=5.8,
            arrowprops={"arrowstyle": "-", "linewidth": 0.25, "color": "#777777"},
        )

    x_min = max(1, plot_df["n_profiles"].min() * 0.75)
    x_max = plot_df["n_profiles"].max() * 1.6
    ax.set_xscale("log")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-1, 1)
    ax.axhline(0, color="#777777", linewidth=0.75, linestyle="--", zorder=1)
    ax.set_xlabel("Profiles in marker cluster", fontsize=7.0)
    ax.set_ylabel("Mean silhouette\n(label token distance)", fontsize=7.0)
    ax.tick_params(axis="x", labelsize=6.0, length=2, width=0.5)
    ax.tick_params(axis="y", labelsize=6.0, length=2, width=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)


def add_panel_label(ax, label: str, x: float = -0.12, y: float = 1.08) -> None:
    ax.text(
        x,
        y,
        label,
        transform=ax.transAxes,
        fontsize=9.5,
        fontweight="bold",
        ha="left",
        va="top",
    )


def select_gene_extremes(
    gene_weights_df: pd.DataFrame,
    min_shared_pairs: int,
    high_n: int,
    low_n: int,
) -> pd.DataFrame:
    eligible_df = gene_weights_df.loc[
        gene_weights_df["n_shared_pairs_with_gene"].ge(min_shared_pairs)
    ].copy()
    if eligible_df.empty:
        return eligible_df
    high_df = eligible_df.sort_values(
        ["label_linked_fraction_when_shared", "n_shared_pairs_with_gene"],
        ascending=[False, False],
    ).head(high_n)
    low_df = eligible_df.sort_values(
        ["label_linked_fraction_when_shared", "n_shared_pairs_with_gene"],
        ascending=[True, False],
    ).head(low_n)
    return (
        pd.concat([low_df, high_df], ignore_index=True)
        .drop_duplicates("gene_id")
        .sort_values("label_linked_fraction_when_shared")
    )


def add_gene_fraction_panel(
    ax,
    gene_weights_df: pd.DataFrame,
    title: str,
    min_shared_pairs: int = MIN_SHARED_PAIRS_FOR_DISPLAY,
    high_n: int = 10,
    low_n: int = 5,
) -> None:
    plot_df = select_gene_extremes(
        gene_weights_df,
        min_shared_pairs=min_shared_pairs,
        high_n=high_n,
        low_n=low_n,
    )
    ax.set_title(title, loc="left", fontsize=8.2, fontweight="bold", pad=5)
    if plot_df.empty:
        ax.text(0.5, 0.5, "No genes passed filter", ha="center", va="center", fontsize=7.0)
        ax.axis("off")
        return
    y = np.arange(len(plot_df))
    background = float(plot_df["background_label_linked_fraction"].iloc[0]) if not plot_df.empty else 0
    colors = np.where(plot_df["label_linked_fraction_when_shared"].ge(background), "#d9d9d9", "#f2f2f2")
    ax.barh(
        y,
        plot_df["label_linked_fraction_when_shared"],
        color=colors,
        edgecolor="#222222",
        linewidth=0.45,
    )
    ax.axvline(background, color="#777777", linewidth=0.7, linestyle="--")
    y_labels = [
        f"{row.gene_name} (n={int(row.n_shared_pairs_with_gene):,})"
        for row in plot_df.itertuples(index=False)
    ]
    ax.set_yticks(y)
    ax.set_yticklabels(y_labels, fontsize=6.0)
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=0))
    ax.set_xlabel("Profile pairs with exact/partial label match", fontsize=7.0)
    ax.tick_params(axis="x", labelsize=6.0, length=2, width=0.5)
    ax.tick_params(axis="y", length=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)


def write_report(
    profiles_df: pd.DataFrame,
    pair_df: pd.DataFrame,
    gene_weights_df: pd.DataFrame,
    cv_metrics_df: pd.DataFrame,
    label_token_df: pd.DataFrame,
    label_silhouette_df: pd.DataFrame,
    marker_cluster_summary_df: pd.DataFrame,
    marker_cluster_label_silhouette_df: pd.DataFrame,
    label_group_gene_scores_df: pd.DataFrame,
    marker_group_gene_scores_df: pd.DataFrame,
    group_gene_f1_comparison_df: pd.DataFrame,
    myeloid_profiles_df: pd.DataFrame,
    myeloid_pair_df: pd.DataFrame,
    myeloid_gene_weights_df: pd.DataFrame,
    myeloid_label_token_df: pd.DataFrame,
    myeloid_label_silhouette_df: pd.DataFrame,
) -> None:
    metric_summary = (
        cv_metrics_df.groupby("model")[["auroc", "auprc"]]
        .agg(["mean", "std"])
        .round(3)
        .reset_index()
    )
    metric_summary.columns = [
        "model",
        "auroc_mean",
        "auroc_std",
        "auprc_mean",
        "auprc_std",
    ]
    metric_lines = [
        "| model | AUROC mean | AUROC sd | AUPRC mean | AUPRC sd |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in metric_summary.itertuples(index=False):
        metric_lines.append(
            f"| {row.model} | {row.auroc_mean:.3f} | {row.auroc_std:.3f} | {row.auprc_mean:.3f} | {row.auprc_std:.3f} |"
        )
    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Nomenclature Gene Weights Prototype",
                "",
                "## Assumptions",
                "",
                "- Unit of analysis is a cross-paper pair of marker profiles that share at least one frequent mapped marker gene.",
                f"- Frequent genes are those present in at least {MIN_GENE_PROFILE_COUNT} marker profiles.",
                f"- The myeloid C1-C3 subset uses a lower threshold of {MYELOID_MIN_GENE_PROFILE_COUNT} marker profiles because it is a focused lineage subset.",
                "- Target is whether reported labels are exact or partial matches after label normalization.",
                "- Predictors are binary indicators for which marker genes are shared by the pair.",
                "- Evaluation holds out papers, trains on pairs where both papers are in the training set, and tests on pairs where both papers are in the held-out set.",
                "- The learned gene weights quantify predictability of reported nomenclature, not ground-truth cell identity.",
                "",
                "## Counts",
                "",
                f"- Marker profiles: {len(profiles_df):,}",
                f"- Papers: {profiles_df['paper_key'].nunique():,}",
                f"- Cross-paper shared-gene pairs: {len(pair_df):,}",
                f"- Label-linked pair fraction: {pair_df['label_linked'].mean():.3f}",
                f"- Genes with nonzero coefficients: {gene_weights_df['coefficient'].ne(0).sum():,}",
                f"- Label terms scored: {len(label_token_df):,}",
                f"- Exact labels scored by marker silhouette: {len(label_silhouette_df):,}",
                f"- Marker-gene clusters scored for label purity: {len(marker_cluster_summary_df):,}",
                f"- Marker-gene clusters scored by label silhouette: {len(marker_cluster_label_silhouette_df):,}",
                f"- Label-derived example genes scored: {len(label_group_gene_scores_df):,}",
                f"- Marker-derived example genes scored: {len(marker_group_gene_scores_df):,}",
                f"- Label/marker example gene F1 scores compared: {len(group_gene_f1_comparison_df):,}",
                f"- Myeloid C1-C3 marker profiles: {len(myeloid_profiles_df):,}",
                f"- Myeloid C1-C3 shared-gene pairs: {len(myeloid_pair_df):,}",
                f"- Myeloid C1-C3 label-linked pair fraction: {myeloid_pair_df['label_linked'].mean():.3f}",
                f"- Myeloid C1-C3 genes with nonzero coefficients: {myeloid_gene_weights_df['coefficient'].ne(0).sum():,}",
                f"- Myeloid C1-C3 label terms scored: {len(myeloid_label_token_df):,}",
                f"- Myeloid C1-C3 exact labels scored by marker silhouette: {len(myeloid_label_silhouette_df):,}",
                "",
                "## Cross-Validation Metrics",
                "",
                "\n".join(metric_lines),
                "",
                "## Outputs",
                "",
                f"- Figure: `{FIGURE_PATH.relative_to(REPO_ROOT)}`",
                f"- Gene weights: `{GENE_WEIGHTS_PATH.relative_to(REPO_ROOT)}`",
                f"- Pair scores: `{PAIR_SCORES_PATH.relative_to(REPO_ROOT)}`",
                f"- Cross-validation metrics: `{CV_METRICS_PATH.relative_to(REPO_ROOT)}`",
                f"- Label token scores: `{LABEL_TOKEN_SCORES_PATH.relative_to(REPO_ROOT)}`",
                f"- Label silhouette scores: `{LABEL_SILHOUETTE_PATH.relative_to(REPO_ROOT)}`",
                f"- Marker cluster summary: `{MARKER_CLUSTER_SUMMARY_PATH.relative_to(REPO_ROOT)}`",
                f"- Marker cluster membership: `{MARKER_CLUSTER_MEMBERSHIP_PATH.relative_to(REPO_ROOT)}`",
                f"- Marker cluster label silhouette: `{MARKER_CLUSTER_LABEL_SILHOUETTE_PATH.relative_to(REPO_ROOT)}`",
                f"- Label-derived example gene scores: `{LABEL_GROUP_GENE_SCORES_PATH.relative_to(REPO_ROOT)}`",
                f"- Marker-derived example gene scores: `{MARKER_GROUP_GENE_SCORES_PATH.relative_to(REPO_ROOT)}`",
                f"- Label/marker example gene F1 comparison: `{GROUP_GENE_F1_COMPARISON_PATH.relative_to(REPO_ROOT)}`",
                f"- Myeloid C1-C3 gene weights: `{MYELOID_GENE_WEIGHTS_PATH.relative_to(REPO_ROOT)}`",
                f"- Myeloid C1-C3 pair scores: `{MYELOID_PAIR_SCORES_PATH.relative_to(REPO_ROOT)}`",
                f"- Myeloid C1-C3 label token scores: `{MYELOID_LABEL_TOKEN_SCORES_PATH.relative_to(REPO_ROOT)}`",
                f"- Myeloid C1-C3 label silhouette scores: `{MYELOID_LABEL_SILHOUETTE_PATH.relative_to(REPO_ROOT)}`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    profiles_df, id_to_name = build_profiles()
    pair_df, gene_weights_df, label_token_df, features, _full_model, _gene_vocab = run_nomenclature_model(
        profiles_df,
        id_to_name,
        min_gene_profile_count=MIN_GENE_PROFILE_COUNT,
        min_label_token_pairs=MIN_LABEL_TOKEN_PAIRS,
    )
    cv_metrics_df = evaluate_heldout_papers(pair_df, features)
    label_silhouette_df = build_label_silhouette_scores(
        profiles_df,
        min_label_profiles=MIN_LABEL_PROFILE_COUNT,
    )
    marker_edges = marker_pair_edges(profiles_df, threshold=MARKER_CLUSTER_JACCARD)
    marker_components = marker_connected_components(len(profiles_df), marker_edges)
    marker_cluster_summary_df, marker_cluster_membership_df = summarize_marker_clusters(
        profiles_df,
        marker_components,
        marker_edges,
        id_to_name,
    )
    marker_cluster_label_silhouette_df = build_marker_cluster_label_silhouette_scores(
        marker_cluster_summary_df,
        marker_cluster_membership_df,
    )
    tcell_marker_summary_df, tcell_marker_membership_df = build_tcell_marker_groups(
        profiles_df,
        id_to_name,
    )
    tcell_gene_f1_cluster_df, tcell_gene_f1_summary_df = build_tcell_gene_f1_tables(
        profiles_df,
        id_to_name,
        tcell_marker_summary_df,
        tcell_marker_membership_df,
    )
    example_results = []
    label_group_gene_score_tables = []
    marker_group_gene_score_tables = []
    group_gene_f1_comparison_tables = []
    for example in EXAMPLE_GROUPS:
        label_group_profile_ids = example_label_profile_indices(profiles_df, example)
        marker_group_cluster = select_marker_cluster_for_label(
            marker_cluster_summary_df,
            example["marker_query"],
        )
        marker_group_profile_ids = set(
            marker_cluster_membership_df.loc[
                marker_cluster_membership_df["cluster"].eq(marker_group_cluster),
                "profile_idx",
            ].astype(int)
        )
        label_group_gene_scores = group_gene_scores(
            profiles_df,
            label_group_profile_ids,
            id_to_name,
            f"label group {example['key']}",
        )
        marker_group_gene_scores = group_gene_scores(
            profiles_df,
            marker_group_profile_ids,
            id_to_name,
            f"marker cluster C{marker_group_cluster}",
        )
        group_gene_f1_comparison = compare_group_gene_f1(
            label_group_gene_scores,
            marker_group_gene_scores,
        )
        label_group_gene_scores.insert(0, "example", example["key"])
        marker_group_gene_scores.insert(0, "example", example["key"])
        group_gene_f1_comparison.insert(0, "example", example["key"])
        group_gene_f1_comparison.insert(1, "marker_cluster", marker_group_cluster)
        label_group_gene_score_tables.append(label_group_gene_scores)
        marker_group_gene_score_tables.append(marker_group_gene_scores)
        group_gene_f1_comparison_tables.append(group_gene_f1_comparison)
        example_results.append(
            {
                "config": example,
                "marker_cluster": marker_group_cluster,
                "label_scores": label_group_gene_scores,
                "marker_scores": marker_group_gene_scores,
                "f1_scores": group_gene_f1_comparison,
            }
        )
    label_group_gene_scores_df = pd.concat(label_group_gene_score_tables, ignore_index=True)
    marker_group_gene_scores_df = pd.concat(marker_group_gene_score_tables, ignore_index=True)
    group_gene_f1_comparison_df = pd.concat(group_gene_f1_comparison_tables, ignore_index=True)

    myeloid_profiles_df, myeloid_id_to_name = build_myeloid_c1_c3_profiles()
    (
        myeloid_pair_df,
        myeloid_gene_weights_df,
        myeloid_label_token_df,
        _myeloid_features,
        _myeloid_model,
        _myeloid_gene_vocab,
    ) = run_nomenclature_model(
        myeloid_profiles_df,
        myeloid_id_to_name,
        min_gene_profile_count=MYELOID_MIN_GENE_PROFILE_COUNT,
        min_label_token_pairs=MYELOID_MIN_LABEL_TOKEN_PAIRS,
    )
    myeloid_label_silhouette_df = build_label_silhouette_scores(
        myeloid_profiles_df,
        min_label_profiles=MYELOID_MIN_LABEL_PROFILE_COUNT,
    )

    gene_weights_df.to_csv(GENE_WEIGHTS_PATH, sep="\t", index=False)
    pair_df.to_csv(PAIR_SCORES_PATH, sep="\t", index=False)
    cv_metrics_df.to_csv(CV_METRICS_PATH, sep="\t", index=False)
    label_token_df.to_csv(LABEL_TOKEN_SCORES_PATH, sep="\t", index=False)
    label_silhouette_df.to_csv(LABEL_SILHOUETTE_PATH, sep="\t", index=False)
    marker_cluster_summary_df.to_csv(MARKER_CLUSTER_SUMMARY_PATH, sep="\t", index=False)
    marker_cluster_membership_df.to_csv(MARKER_CLUSTER_MEMBERSHIP_PATH, sep="\t", index=False)
    marker_cluster_label_silhouette_df.to_csv(MARKER_CLUSTER_LABEL_SILHOUETTE_PATH, sep="\t", index=False)
    label_group_gene_scores_df.to_csv(LABEL_GROUP_GENE_SCORES_PATH, sep="\t", index=False)
    marker_group_gene_scores_df.to_csv(MARKER_GROUP_GENE_SCORES_PATH, sep="\t", index=False)
    group_gene_f1_comparison_df.to_csv(GROUP_GENE_F1_COMPARISON_PATH, sep="\t", index=False)
    tcell_gene_f1_cluster_df.to_csv(TCELL_GENE_F1_CLUSTER_TABLE_PATH, sep="\t", index=False)
    tcell_gene_f1_summary_df.to_csv(TCELL_GENE_F1_GENE_SUMMARY_PATH, sep="\t", index=False)
    myeloid_gene_weights_df.to_csv(MYELOID_GENE_WEIGHTS_PATH, sep="\t", index=False)
    myeloid_pair_df.to_csv(MYELOID_PAIR_SCORES_PATH, sep="\t", index=False)
    myeloid_label_token_df.to_csv(MYELOID_LABEL_TOKEN_SCORES_PATH, sep="\t", index=False)
    myeloid_label_silhouette_df.to_csv(MYELOID_LABEL_SILHOUETTE_PATH, sep="\t", index=False)
    write_report(
        profiles_df,
        pair_df,
        gene_weights_df,
        cv_metrics_df,
        label_token_df,
        label_silhouette_df,
        marker_cluster_summary_df,
        marker_cluster_label_silhouette_df,
        label_group_gene_scores_df,
        marker_group_gene_scores_df,
        group_gene_f1_comparison_df,
        myeloid_profiles_df,
        myeloid_pair_df,
        myeloid_gene_weights_df,
        myeloid_label_token_df,
        myeloid_label_silhouette_df,
    )

    plt.rcParams.update({"font.size": 8})
    fig = plt.figure(figsize=(11.4, 10.4))
    gs = fig.add_gridspec(3, 6, height_ratios=[1.05, 1.0, 1.0], wspace=0.54, hspace=0.52)
    top_left_ax = fig.add_subplot(gs[0, :3])
    top_right_ax = fig.add_subplot(gs[0, 3:])
    add_label_silhouette_panel(
        top_left_ax,
        label_silhouette_df,
        "All profiles: labels -> marker genes",
        high_n=6,
        low_n=2,
        support_n=2,
    )
    add_marker_cluster_label_silhouette_panel(
        top_right_ax,
        marker_cluster_label_silhouette_df,
        "All profiles: marker genes -> labels",
    )
    example_axes_rows = []
    for example_idx, example_result in enumerate(example_results):
        row_idx = 1 + example_idx
        axes_row = [
            fig.add_subplot(gs[row_idx, 0:2]),
            fig.add_subplot(gs[row_idx, 2:4]),
            fig.add_subplot(gs[row_idx, 4:6]),
        ]
        example_axes_rows.append(axes_row)
        config = example_result["config"]
        marker_cluster = example_result["marker_cluster"]
        add_gene_coverage_panel(
            axes_row[0],
            example_result["label_scores"],
            config["label_title"],
        )
        add_gene_coverage_panel(
            axes_row[1],
            example_result["marker_scores"],
            config["marker_title"].format(cluster=marker_cluster),
        )
        add_group_gene_f1_panel(
            axes_row[2],
            example_result["f1_scores"],
            config["f1_title"],
        )
    fig.canvas.draw()
    bottom_positions = [ax.get_position() for axes_row in example_axes_rows for ax in axes_row]
    bottom_left = min(position.x0 for position in bottom_positions)
    bottom_right = max(position.x1 for position in bottom_positions)
    bottom_gap = example_axes_rows[0][1].get_position().x0 - example_axes_rows[0][0].get_position().x1
    top_left_position = top_left_ax.get_position()
    top_right_position = top_right_ax.get_position()
    top_width = (bottom_right - bottom_left - bottom_gap) / 2
    top_left_ax.set_position([bottom_left, top_left_position.y0, top_width, top_left_position.height])
    top_right_ax.set_position(
        [
            bottom_left + top_width + bottom_gap,
            top_right_position.y0,
            top_width,
            top_right_position.height,
        ]
    )
    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    fig.savefig(FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)

    main_fig = plt.figure(figsize=(7.8, 2.55))
    main_gs = main_fig.add_gridspec(1, 3, wspace=0.42)
    main_axes = [
        main_fig.add_subplot(main_gs[0, 0]),
        main_fig.add_subplot(main_gs[0, 1]),
        main_fig.add_subplot(main_gs[0, 2]),
    ]
    add_label_silhouette_panel(
        main_axes[0],
        label_silhouette_df,
        "Labels $\\rightarrow$ marker genes",
        high_n=2,
        low_n=0,
        support_n=1,
    )
    add_marker_cluster_label_silhouette_panel(
        main_axes[1],
        marker_cluster_label_silhouette_df,
        "Marker genes $\\rightarrow$ labels",
        support_n=2,
        high_n=1,
        low_n=1,
    )
    add_tcell_gene_f1_panel(
        main_axes[2],
        tcell_gene_f1_summary_df,
        "T-cell gene F1 shifts",
    )
    main_axes[0].set_box_aspect(1)
    main_axes[1].set_box_aspect(1)
    main_axes[2].set_aspect("equal", adjustable="box")
    for axis, panel_label in zip(main_axes, ["D", "E", "F"], strict=False):
        legend = axis.get_legend()
        if legend is not None and panel_label != "F":
            legend.remove()
        add_panel_label(axis, panel_label, x=-0.18, y=1.14)

    main_fig.subplots_adjust(left=0.085, right=0.995, top=0.80, bottom=0.24)
    main_fig.savefig(MAIN_FIGURE_PATH, bbox_inches="tight")
    main_fig.savefig(MAIN_FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(main_fig)

    print(f"Profiles: {len(profiles_df):,}")
    print(f"Shared-gene profile pairs: {len(pair_df):,}")
    print(f"Label-linked fraction: {pair_df['label_linked'].mean():.3f}")
    print(f"Nonzero gene coefficients: {gene_weights_df['coefficient'].ne(0).sum():,}")
    print(f"Label terms scored: {len(label_token_df):,}")
    print(f"Exact labels scored by marker silhouette: {len(label_silhouette_df):,}")
    print(f"Marker clusters scored by label purity: {len(marker_cluster_summary_df):,}")
    print(f"Marker clusters scored by label silhouette: {len(marker_cluster_label_silhouette_df):,}")
    print(f"Label-derived example genes scored: {len(label_group_gene_scores_df):,}")
    print(f"Marker-derived example genes scored: {len(marker_group_gene_scores_df):,}")
    print(f"Label/marker example gene F1 scores compared: {len(group_gene_f1_comparison_df):,}")
    print(f"T-cell marker groups: {len(tcell_marker_summary_df):,}")
    print(f"T-cell marker/label gene F1 scores compared: {len(tcell_gene_f1_cluster_df):,}")
    print(f"Myeloid C1-C3 profiles: {len(myeloid_profiles_df):,}")
    print(f"Myeloid C1-C3 shared-gene profile pairs: {len(myeloid_pair_df):,}")
    print(f"Myeloid C1-C3 label-linked fraction: {myeloid_pair_df['label_linked'].mean():.3f}")
    print(f"Myeloid C1-C3 nonzero gene coefficients: {myeloid_gene_weights_df['coefficient'].ne(0).sum():,}")
    print(f"Myeloid C1-C3 label terms scored: {len(myeloid_label_token_df):,}")
    print(f"Myeloid C1-C3 exact labels scored by marker silhouette: {len(myeloid_label_silhouette_df):,}")
    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PNG_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MAIN_FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MAIN_FIGURE_PNG_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {GENE_WEIGHTS_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PAIR_SCORES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {CV_METRICS_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {LABEL_TOKEN_SCORES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {LABEL_SILHOUETTE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MARKER_CLUSTER_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MARKER_CLUSTER_MEMBERSHIP_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MARKER_CLUSTER_LABEL_SILHOUETTE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {LABEL_GROUP_GENE_SCORES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MARKER_GROUP_GENE_SCORES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {GROUP_GENE_F1_COMPARISON_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {TCELL_GENE_F1_CLUSTER_TABLE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {TCELL_GENE_F1_GENE_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MYELOID_GENE_WEIGHTS_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MYELOID_PAIR_SCORES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MYELOID_LABEL_TOKEN_SCORES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MYELOID_LABEL_SILHOUETTE_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
