from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATASETS = {
    "biorxiv": REPO_ROOT / "data" / "biorxiv" / "meca",
    "hca": REPO_ROOT / "data" / "hca" / "manuscripts",
}
FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
RESULTS_DIR = REPO_ROOT / "analysis" / "results"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

MIN_MARKERS = 3
GENERIC_LABEL_TOKENS = {
    "a",
    "an",
    "and",
    "cell",
    "cells",
    "cluster",
    "clusters",
    "population",
    "populations",
    "type",
    "types",
}

LABEL_ORDER = ["Exact", "Partial", "Different"]
MARKER_ORDER = ["Exact", "Partial", "None"]

CELL_COLORS = {
    ("Exact", "Exact"): "#a8d8cf",
    ("Different", "None"): "#e6e6e6",
}
DEFAULT_AMBIGUOUS_COLOR = "#f3dfb7"


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def clean_upper(value: object) -> str:
    return clean_text(value).upper()


def normalize_label(value: object) -> str:
    text = clean_text(value)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.upper()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    text = re.sub(r"(?<=[A-Z])(?=[0-9])", " ", text)
    text = re.sub(r"(?<=[0-9])(?=[A-Z])", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def label_tokens(label: str) -> set[str]:
    return {
        token
        for token in label.lower().split()
        if token not in GENERIC_LABEL_TOKENS and len(token) >= 2
    }


def label_relation(label_a: str, label_b: str) -> str:
    if label_a == label_b:
        return "Exact"
    if not label_a or not label_b:
        return "Different"

    padded_a = f" {label_a} "
    padded_b = f" {label_b} "
    if padded_a in padded_b or padded_b in padded_a:
        return "Partial"

    tokens_a = label_tokens(label_a)
    tokens_b = label_tokens(label_b)
    if tokens_a and tokens_b and tokens_a.intersection(tokens_b):
        return "Partial"
    return "Different"


def label_similarity(label_a: str, label_b: str) -> float:
    if label_a == label_b and label_a:
        return 1.0
    if not label_a or not label_b:
        return 0.0

    padded_a = f" {label_a} "
    padded_b = f" {label_b} "
    if padded_a in padded_b or padded_b in padded_a:
        return 0.75

    tokens_a = label_tokens(label_a)
    tokens_b = label_tokens(label_b)
    if not tokens_a or not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / len(tokens_a | tokens_b)


def marker_relation(jaccard: float) -> str:
    if np.isclose(jaccard, 1.0):
        return "Exact"
    if jaccard > 0:
        return "Partial"
    return "None"


def format_percent(percent: float, count: int) -> str:
    if count > 0 and percent < 0.1:
        return "<0.1%"
    return f"{percent:.1f}%"


def iter_marker_records(source_corpus: str, base_dir: Path):
    for markers_path in sorted(base_dir.rglob("markers.json")):
        paper_dir = markers_path.parent
        try:
            markers = json.loads(markers_path.read_text())
        except Exception:
            continue
        if not isinstance(markers, list):
            continue

        paper_id = paper_dir.name
        paper_key = f"{source_corpus}:{paper_id}"
        for row_idx, marker in enumerate(markers):
            verification = marker.get("_verification") or {}
            yield {
                "source_corpus": source_corpus,
                "paper_id": paper_id,
                "paper_key": paper_key,
                "record_index": row_idx,
                "organism": clean_text(marker.get("organism")).lower(),
                "group_name_norm": clean_upper(marker.get("group_name")),
                "feature_id": clean_text(marker.get("feature_id")),
                "all_verified": bool(verification.get("all_verified")),
            }


def load_profiles() -> pd.DataFrame:
    records = pd.DataFrame(
        row
        for source_corpus, base_dir in DATASETS.items()
        for row in iter_marker_records(source_corpus, base_dir)
    )

    canonical = records.loc[
        (records["organism"] == "homo_sapiens")
        & records["feature_id"].ne("")
        & records["group_name_norm"].ne("")
        & records["all_verified"]
    ].copy()

    canonical = canonical.sort_values(
        ["source_corpus", "paper_id", "group_name_norm", "feature_id", "record_index"]
    ).drop_duplicates(
        subset=["source_corpus", "paper_id", "group_name_norm", "feature_id"],
        keep="first",
    )

    profile_rows = []
    for (source_corpus, paper_id, paper_key, cell_type), group in canonical.groupby(
        ["source_corpus", "paper_id", "paper_key", "group_name_norm"], sort=True
    ):
        gene_ids = sorted(group["feature_id"].unique())
        profile_rows.append(
            {
                "source_corpus": source_corpus,
                "paper_id": paper_id,
                "paper_key": paper_key,
                "cell_type": cell_type,
                "cell_type_norm": normalize_label(cell_type),
                "n_markers": len(gene_ids),
                "marker_ids": ";".join(gene_ids),
            }
        )

    profiles = pd.DataFrame(profile_rows)
    return profiles.loc[profiles["n_markers"] >= MIN_MARKERS].reset_index(drop=True)


profiles_df = load_profiles()
profile_keys = [
    (row.source_corpus, row.paper_id, row.cell_type)
    for row in profiles_df.itertuples(index=False)
]
profile_genes = [set(row.marker_ids.split(";")) for row in profiles_df.itertuples(index=False)]

gene_to_profiles: dict[str, list[int]] = defaultdict(list)
for profile_idx, genes in enumerate(profile_genes):
    for gene_id in genes:
        gene_to_profiles[gene_id].append(profile_idx)

shared_gene_pairs: set[tuple[int, int]] = set()
for profile_indices in gene_to_profiles.values():
    for pair in combinations(sorted(set(profile_indices)), 2):
        if profile_keys[pair[0]][:2] != profile_keys[pair[1]][:2]:
            shared_gene_pairs.add(pair)

exact_or_partial_label_pairs: set[tuple[int, int]] = set()
label_to_profiles: dict[str, list[int]] = defaultdict(list)
token_to_profiles: dict[str, list[int]] = defaultdict(list)
for profile_idx, label in enumerate(profiles_df["cell_type_norm"]):
    label_to_profiles[label].append(profile_idx)
    for token in label_tokens(label):
        token_to_profiles[token].append(profile_idx)

for profile_indices in label_to_profiles.values():
    for pair in combinations(sorted(profile_indices), 2):
        if profile_keys[pair[0]][:2] != profile_keys[pair[1]][:2]:
            exact_or_partial_label_pairs.add(pair)

for profile_indices in token_to_profiles.values():
    for pair in combinations(sorted(set(profile_indices)), 2):
        if profile_keys[pair[0]][:2] != profile_keys[pair[1]][:2]:
            exact_or_partial_label_pairs.add(pair)

all_positive_pairs = shared_gene_pairs | exact_or_partial_label_pairs

counts = pd.DataFrame(0, index=LABEL_ORDER, columns=MARKER_ORDER, dtype=np.int64)
observed_pairs = 0
positive_pair_rows = []
for i, j in sorted(all_positive_pairs):
    observed_pairs += 1
    labels = profiles_df.loc[[i, j], "cell_type_norm"].tolist()
    genes_i = profile_genes[i]
    genes_j = profile_genes[j]
    union = genes_i | genes_j
    jaccard = len(genes_i & genes_j) / len(union) if union else 0.0
    label_rel = label_relation(labels[0], labels[1])
    marker_rel = marker_relation(jaccard)
    counts.loc[label_rel, marker_rel] += 1
    positive_pair_rows.append(
        {
            "profile_i": i,
            "profile_j": j,
            "label_relation": label_rel,
            "marker_relation": marker_rel,
            "jaccard": jaccard,
        }
    )

total_cross_paper_pairs = 0
paper_key_to_indices: dict[str, list[int]] = defaultdict(list)
for idx, paper_key in enumerate(profiles_df["paper_key"]):
    paper_key_to_indices[paper_key].append(idx)

for i, j in combinations(range(len(profiles_df)), 2):
    if profile_keys[i][:2] != profile_keys[j][:2]:
        total_cross_paper_pairs += 1

unobserved_different_none = total_cross_paper_pairs - observed_pairs
counts.loc["Different", "None"] += unobserved_different_none
fractions = counts / total_cross_paper_pairs

summary_rows = []
for label_rel in LABEL_ORDER:
    for marker_rel in MARKER_ORDER:
        summary_rows.append(
            {
                "label_relation": label_rel,
                "marker_relation": marker_rel,
                "pairs": int(counts.loc[label_rel, marker_rel]),
                "fraction": float(fractions.loc[label_rel, marker_rel]),
                "percent": 100 * float(fractions.loc[label_rel, marker_rel]),
            }
        )
joint_df = pd.DataFrame(summary_rows)
joint_df.to_csv(RESULTS_DIR / "cross_study_label_marker_joint_distribution.tsv", sep="\t", index=False)
positive_pair_df = pd.DataFrame(positive_pair_rows)

plt.rcParams.update(
    {
        "font.size": 8,
        "font.family": "DejaVu Sans",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

fig, ax = plt.subplots(figsize=(4.9, 4.5))
ax.set_xlim(0, 3)
ax.set_ylim(0, 3)
ax.invert_yaxis()
ax.set_aspect("equal")
ax.axis("off")

for row_idx, label_rel in enumerate(LABEL_ORDER):
    for col_idx, marker_rel in enumerate(MARKER_ORDER):
        color = CELL_COLORS.get((label_rel, marker_rel), DEFAULT_AMBIGUOUS_COLOR)
        if label_rel == "Different" and marker_rel == "None":
            color = CELL_COLORS[(label_rel, marker_rel)]
        rect = plt.Rectangle((col_idx, row_idx), 1, 1, facecolor=color, edgecolor="#777777", linewidth=0.8)
        ax.add_patch(rect)
        count = counts.loc[label_rel, marker_rel]
        percent = 100 * fractions.loc[label_rel, marker_rel]
        text_color = "white" if percent > 45 else "#111111"
        ax.text(
            col_idx + 0.5,
            row_idx + 0.43,
            format_percent(percent, int(count)),
            ha="center",
            va="center",
            fontsize=9.2,
            fontweight="bold",
            color=text_color,
        )
        ax.text(
            col_idx + 0.5,
            row_idx + 0.64,
            f"({count:,})",
            ha="center",
            va="center",
            fontsize=7.5,
            color=text_color,
        )

ax.add_patch(
    plt.Rectangle(
        (1, 0),
        1,
        3,
        facecolor="none",
        edgecolor="#b33a3a",
        linewidth=1.8,
        zorder=8,
    )
)

for row_idx, label_rel in enumerate(LABEL_ORDER):
    ax.text(-0.18, row_idx + 0.5, label_rel, ha="right", va="center", fontsize=8.2)

for col_idx, marker_rel in enumerate(MARKER_ORDER):
    sublabel = {"Exact": "$J=1$", "Partial": "$0<J<1$", "None": "$J=0$"}[marker_rel]
    ax.text(col_idx + 0.5, -0.28, marker_rel, ha="center", va="bottom", fontsize=8.2)
    ax.text(col_idx + 0.5, -0.11, sublabel, ha="center", va="bottom", fontsize=7.2)

ax.text(1.5, -0.62, "Marker genes", ha="center", va="bottom", fontsize=9.2, fontweight="bold")
ax.text(-0.62, 1.5, "Cell type labels", ha="center", va="center", rotation=90, fontsize=9.2, fontweight="bold")

legend_items = [
    ("#a8d8cf", "likely same cell type"),
    (DEFAULT_AMBIGUOUS_COLOR, "context clarifies cell type vs. state"),
    ("#e6e6e6", "likely different cell type"),
]
legend_y = 3.28
legend_x = 0.08
for color, label in legend_items:
    ax.add_patch(
        plt.Rectangle(
            (legend_x, legend_y - 0.07),
            0.10,
            0.10,
            facecolor=color,
            edgecolor="#777777",
            linewidth=0.6,
            clip_on=False,
        )
    )
    ax.text(legend_x + 0.14, legend_y - 0.02, label, ha="left", va="center", fontsize=7.4, clip_on=False)
    legend_y += 0.22

fig.savefig(FIGURE_DIR / "fig_cross_study_joint_distribution.pdf", bbox_inches="tight")
fig.savefig(FIGURE_DIR / "fig_cross_study_joint_distribution.png", bbox_inches="tight", dpi=240)


def directed_positive_pairs(pair_df: pd.DataFrame) -> pd.DataFrame:
    directed_rows = []
    for row in pair_df.itertuples(index=False):
        directed_rows.append(
            {
                "source_profile": row.profile_i,
                "neighbor_profile": row.profile_j,
                "label_relation": row.label_relation,
                "marker_relation": row.marker_relation,
                "jaccard": row.jaccard,
            }
        )
        directed_rows.append(
            {
                "source_profile": row.profile_j,
                "neighbor_profile": row.profile_i,
                "label_relation": row.label_relation,
                "marker_relation": row.marker_relation,
                "jaccard": row.jaccard,
            }
        )
    return pd.DataFrame(directed_rows)


directed_pair_df = directed_positive_pairs(positive_pair_df)

partial_marker_df = positive_pair_df.loc[positive_pair_df["marker_relation"].eq("Partial")].copy()
partial_marker_summary_df = (
    partial_marker_df.groupby("label_relation", sort=False)["jaccard"]
    .agg(
        pairs="size",
        median_jaccard="median",
        mean_jaccard="mean",
        q25_jaccard=lambda values: float(values.quantile(0.25)),
        q75_jaccard=lambda values: float(values.quantile(0.75)),
    )
    .reindex(LABEL_ORDER)
    .reset_index()
)
partial_marker_summary_df.to_csv(
    RESULTS_DIR / "cross_study_partial_marker_overlap_summary.tsv",
    sep="\t",
    index=False,
)

marker_neighbor_candidates = directed_pair_df.loc[directed_pair_df["marker_relation"].ne("None")].copy()
marker_neighbor_candidates["top_jaccard"] = marker_neighbor_candidates.groupby("source_profile")["jaccard"].transform("max")
marker_neighbor_df = marker_neighbor_candidates.loc[
    np.isclose(marker_neighbor_candidates["jaccard"], marker_neighbor_candidates["top_jaccard"])
].copy()
marker_neighbor_summary_df = (
    marker_neighbor_df["label_relation"]
    .value_counts()
    .reindex(LABEL_ORDER, fill_value=0)
    .rename_axis("label_relation")
    .reset_index(name="top_marker_neighbor_ties")
)
marker_neighbor_summary_df["percent"] = (
    100 * marker_neighbor_summary_df["top_marker_neighbor_ties"] / marker_neighbor_summary_df["top_marker_neighbor_ties"].sum()
)
marker_neighbor_summary_df.to_csv(
    RESULTS_DIR / "cross_study_marker_neighbor_label_summary.tsv",
    sep="\t",
    index=False,
)

label_neighbor_candidates = directed_pair_df.loc[directed_pair_df["label_relation"].isin(["Exact", "Partial"])].copy()
label_neighbor_candidates["label_rank"] = label_neighbor_candidates["label_relation"].map({"Exact": 2, "Partial": 1})
label_neighbor_candidates["top_label_rank"] = label_neighbor_candidates.groupby("source_profile")["label_rank"].transform("max")
label_neighbor_df = label_neighbor_candidates.loc[
    label_neighbor_candidates["label_rank"].eq(label_neighbor_candidates["top_label_rank"])
].copy()
label_neighbor_summary_df = (
    label_neighbor_df["marker_relation"]
    .value_counts()
    .reindex(MARKER_ORDER, fill_value=0)
    .rename_axis("marker_relation")
    .reset_index(name="top_label_neighbor_ties")
)
label_neighbor_summary_df["percent"] = (
    100 * label_neighbor_summary_df["top_label_neighbor_ties"] / label_neighbor_summary_df["top_label_neighbor_ties"].sum()
)
label_neighbor_summary_df.to_csv(
    RESULTS_DIR / "cross_study_label_neighbor_marker_summary.tsv",
    sep="\t",
    index=False,
)

K_VALUES = [1, 5, 10]
PLOT_K = 10
RANDOM_SEED = 17

n_profiles = len(profiles_df)
paper_ids = np.array([key[:2] for key in profile_keys], dtype=object)
marker_similarity = np.zeros((n_profiles, n_profiles), dtype=np.float32)
label_similarity_matrix = np.zeros((n_profiles, n_profiles), dtype=np.float32)
labels_norm = profiles_df["cell_type_norm"].tolist()

for row in positive_pair_df.itertuples(index=False):
    if row.jaccard > 0:
        marker_similarity[row.profile_i, row.profile_j] = row.jaccard
        marker_similarity[row.profile_j, row.profile_i] = row.jaccard
    sim = label_similarity(labels_norm[row.profile_i], labels_norm[row.profile_j])
    if sim > 0:
        label_similarity_matrix[row.profile_i, row.profile_j] = sim
        label_similarity_matrix[row.profile_j, row.profile_i] = sim


def top_indices(scores: np.ndarray, candidate_indices: np.ndarray, k: int) -> np.ndarray:
    candidate_scores = scores[candidate_indices]
    order = np.lexsort((candidate_indices, -candidate_scores))
    return candidate_indices[order[:k]]


def compute_neighborhood_overlap(k_values: list[int]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(RANDOM_SEED)
    rows = []
    for profile_idx, key in enumerate(profile_keys):
        cross_paper = np.array(
            [other_idx for other_idx, other_key in enumerate(profile_keys) if other_key[:2] != key[:2]],
            dtype=np.int32,
        )
        marker_positive = cross_paper[marker_similarity[profile_idx, cross_paper] > 0]
        if len(cross_paper) < max(k_values):
            continue

        for k in k_values:
            if len(marker_positive) < k:
                continue

            marker_neighbors = top_indices(marker_similarity[profile_idx], marker_positive, k)
            label_neighbors = top_indices(label_similarity_matrix[profile_idx], cross_paper, k)
            overlap_n = len(set(marker_neighbors).intersection(set(label_neighbors)))
            random_neighbors = rng.choice(cross_paper, size=k, replace=False)
            random_overlap_n = len(set(random_neighbors).intersection(set(label_neighbors)))

            rows.extend(
                [
                    {
                        "k": k,
                        "profile_index": profile_idx,
                        "paper_key": profiles_df.loc[profile_idx, "paper_key"],
                        "cell_type": profiles_df.loc[profile_idx, "cell_type"],
                        "comparison": "Observed",
                        "overlap_at_k": overlap_n / k,
                        "jaccard_at_k": overlap_n / (2 * k - overlap_n),
                        "overlap_n": overlap_n,
                        "marker_positive_neighbors": len(marker_positive),
                        "top_marker_jaccard": float(marker_similarity[profile_idx, marker_neighbors[0]]),
                        "top_label_similarity": float(label_similarity_matrix[profile_idx, label_neighbors[0]]),
                    },
                    {
                        "k": k,
                        "profile_index": profile_idx,
                        "paper_key": profiles_df.loc[profile_idx, "paper_key"],
                        "cell_type": profiles_df.loc[profile_idx, "cell_type"],
                        "comparison": "Random",
                        "overlap_at_k": random_overlap_n / k,
                        "jaccard_at_k": random_overlap_n / (2 * k - random_overlap_n),
                        "overlap_n": random_overlap_n,
                        "marker_positive_neighbors": len(marker_positive),
                        "top_marker_jaccard": float(marker_similarity[profile_idx, marker_neighbors[0]]),
                        "top_label_similarity": float(label_similarity_matrix[profile_idx, label_neighbors[0]]),
                    },
                ]
            )

    overlap_df = pd.DataFrame(rows)
    summary_df = (
        overlap_df.groupby(["k", "comparison"], sort=True)
        .agg(
            profiles=("profile_index", "nunique"),
            mean_overlap_at_k=("overlap_at_k", "mean"),
            median_overlap_at_k=("overlap_at_k", "median"),
            mean_jaccard_at_k=("jaccard_at_k", "mean"),
            median_jaccard_at_k=("jaccard_at_k", "median"),
        )
        .reset_index()
    )
    return overlap_df, summary_df


neighborhood_overlap_df, neighborhood_overlap_summary_df = compute_neighborhood_overlap(K_VALUES)
neighborhood_overlap_df.to_csv(
    RESULTS_DIR / "cross_study_neighborhood_overlap_at_k.tsv",
    sep="\t",
    index=False,
)
neighborhood_overlap_summary_df.to_csv(
    RESULTS_DIR / "cross_study_neighborhood_overlap_at_k_summary.tsv",
    sep="\t",
    index=False,
)


def draw_joint_table(ax: plt.Axes) -> None:
    ax.set_xlim(-1.18, 3.0)
    ax.set_ylim(3.02, -0.54)
    ax.set_aspect("equal")
    ax.set_anchor("E")
    ax.axis("off")

    for row_idx, label_rel in enumerate(LABEL_ORDER):
        for col_idx, marker_rel in enumerate(MARKER_ORDER):
            color = CELL_COLORS.get((label_rel, marker_rel), DEFAULT_AMBIGUOUS_COLOR)
            if label_rel == "Different" and marker_rel == "None":
                color = CELL_COLORS[(label_rel, marker_rel)]
            rect = plt.Rectangle(
                (col_idx, row_idx),
                1,
                1,
                facecolor=color,
                edgecolor="#777777",
                linewidth=0.7,
            )
            ax.add_patch(rect)
            count = counts.loc[label_rel, marker_rel]
            percent = 100 * fractions.loc[label_rel, marker_rel]
            text_color = "white" if percent > 45 else "#111111"
            ax.text(
                col_idx + 0.5,
                row_idx + 0.43,
                format_percent(percent, int(count)),
                ha="center",
                va="center",
                fontsize=7.2,
                fontweight="bold",
                color=text_color,
            )
            ax.text(
                col_idx + 0.5,
                row_idx + 0.64,
                f"({count:,})",
                ha="center",
                va="center",
                fontsize=5.8,
                color=text_color,
            )

    ax.add_patch(
        plt.Rectangle(
            (1, 0),
            1,
            3,
            facecolor="none",
            edgecolor="#b33a3a",
            linewidth=1.4,
            zorder=8,
        )
    )

    for row_idx, label_rel in enumerate(LABEL_ORDER):
        ax.text(-0.08, row_idx + 0.5, label_rel, ha="right", va="center", fontsize=6.6)
    for col_idx, marker_rel in enumerate(MARKER_ORDER):
        sublabel = {"Exact": "$J=1$", "Partial": "$0<J<1$", "None": "$J=0$"}[marker_rel]
        ax.text(col_idx + 0.5, -0.27, marker_rel, ha="center", va="bottom", fontsize=6.6)
        ax.text(col_idx + 0.5, -0.10, sublabel, ha="center", va="bottom", fontsize=5.8)

    ax.text(1.5, -0.49, "Marker genes", ha="center", va="bottom", fontsize=7.4, fontweight="bold")
    ax.text(-1.02, 1.5, "Cell type labels", ha="center", va="center", rotation=90, fontsize=7.2, fontweight="bold")


def draw_partial_jaccard_marginal(ax: plt.Axes) -> None:
    ax.set_anchor("W")
    box_data = [
        partial_marker_df.loc[partial_marker_df["label_relation"].eq(label_rel), "jaccard"].to_numpy()
        for label_rel in LABEL_ORDER
    ]
    box = ax.boxplot(
        box_data,
        vert=False,
        positions=[0.5, 1.5, 2.5],
        patch_artist=True,
        showfliers=False,
        widths=0.42,
        medianprops={"color": "black", "linewidth": 1.1},
        boxprops={"edgecolor": "#555555", "linewidth": 0.8},
        whiskerprops={"color": "#555555", "linewidth": 0.8},
        capprops={"color": "#555555", "linewidth": 0.8},
    )
    for patch in box["boxes"]:
        patch.set_facecolor("#d9d9d9")
    ax.set_ylim(3.02, -0.54)
    ax.set_xlim(0, 1.0)
    ax.set_yticks([0.5, 1.5, 2.5])
    ax.set_yticklabels([])
    ax.set_xlabel("Jaccard\n$(0<J<1)$", fontsize=6.8)
    ax.set_xticks([0, 1.0])
    ax.tick_params(axis="x", labelsize=6.0)
    ax.tick_params(axis="y", length=0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)


def draw_percent_bars(ax: plt.Axes, summary_df: pd.DataFrame, category_col: str, value_col: str, ylabel: str, xlabel: str) -> None:
    color_map = {
        "Exact": "#a8d8cf",
        "Partial": DEFAULT_AMBIGUOUS_COLOR,
        "Different": "#d9d9d9",
        "None": "#d9d9d9",
    }
    positions = np.arange(len(summary_df))
    colors = [color_map.get(category, "#d9d9d9") for category in summary_df[category_col]]
    ax.bar(positions, summary_df["percent"], color=colors, edgecolor="#555555", linewidth=0.8)
    ax.set_xticks(positions)
    display_labels = {"Different": "Diff."}
    ax.set_xticklabels(
        [f"{display_labels.get(row[category_col], row[category_col])}\n{int(row[value_col]):,}" for _, row in summary_df.iterrows()],
        fontsize=5.5,
    )
    ax.set_ylabel(ylabel, fontsize=6.5)
    ax.set_xlabel(xlabel, fontsize=6.5)
    ax.set_ylim(0, max(5, min(100, summary_df["percent"].max() * 1.18)))
    ax.tick_params(axis="y", labelsize=5.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for x, pct in zip(positions, summary_df["percent"], strict=True):
        ax.text(x, pct + max(1, summary_df["percent"].max() * 0.025), f"{pct:.1f}%", ha="center", va="bottom", fontsize=5.8)


def draw_neighbor_relation_stacks(ax: plt.Axes) -> None:
    colors = {
        "Exact": "#a8d8cf",
        "Partial": DEFAULT_AMBIGUOUS_COLOR,
        "Different / none": "#d9d9d9",
    }
    bars = [
        {
            "label": "Marker-neighbor\nlabel relation",
            "summary": marker_neighbor_summary_df,
            "category_col": "label_relation",
            "order": ["Exact", "Partial", "Different"],
            "display": {"Different": "Different / none"},
        },
        {
            "label": "Label-neighbor\nmarker relation",
            "summary": label_neighbor_summary_df,
            "category_col": "marker_relation",
            "order": ["Exact", "Partial", "None"],
            "display": {"None": "Different / none"},
        },
    ]

    for x_pos, bar in enumerate(bars):
        bottom = 0.0
        indexed = bar["summary"].set_index(bar["category_col"])
        for category in bar["order"]:
            percent = float(indexed.loc[category, "percent"])
            legend_label = bar["display"].get(category, category)
            ax.bar(
                x_pos,
                percent,
                bottom=bottom,
                width=0.55,
                color=colors[legend_label],
                edgecolor="#555555",
                linewidth=0.8,
                label=legend_label if x_pos == 0 else None,
            )
            if percent >= 4:
                ax.text(x_pos, bottom + percent / 2, f"{percent:.1f}%", ha="center", va="center", fontsize=5.8)
            else:
                ax.text(x_pos + 0.34, bottom + max(percent / 2, 1.0), f"{percent:.1f}%", ha="left", va="center", fontsize=5.3)
            bottom += percent

    ax.set_xlim(-0.55, 1.55)
    ax.set_ylim(0, 100)
    ax.set_xticks([0, 1])
    ax.set_xticklabels([bar["label"] for bar in bars], fontsize=5.8)
    ax.set_ylabel("Best cross-paper matches (%)", fontsize=6.5)
    ax.tick_params(axis="y", labelsize=5.8)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.18),
        ncol=3,
        frameon=False,
        fontsize=5.4,
        handlelength=0.9,
        columnspacing=0.7,
    )
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def draw_neighborhood_overlap(ax: plt.Axes, overlap_df: pd.DataFrame, k: int) -> None:
    plot_df = overlap_df.loc[overlap_df["k"].eq(k)].copy()
    order = ["Observed", "Random"]
    data = [plot_df.loc[plot_df["comparison"].eq(label), "overlap_at_k"].to_numpy() for label in order]
    positions = np.arange(len(order))
    means = [float(np.mean(values)) if len(values) else 0.0 for values in data]
    colors = ["#a8d8cf", "#d9d9d9"]
    ax.bar(positions, means, width=0.48, color=colors, edgecolor="#555555", linewidth=0.8)
    for pos, mean in zip(positions, means, strict=True):
        ax.text(pos, mean + 0.004, f"{mean:.3f}", ha="center", va="bottom", fontsize=5.8)

    counts_by_label = plot_df.groupby("comparison")["profile_index"].nunique().reindex(order, fill_value=0)
    ax.set_xticks(positions)
    ax.set_xticklabels([f"{label}\n{int(counts_by_label.loc[label]):,}" for label in order], fontsize=5.5)
    ax.set_ylabel(f"Mean marker-label\nneighborhood overlap@{k}", fontsize=6.5)
    ax.set_ylim(0, 1)
    ax.tick_params(axis="y", labelsize=5.8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


multi_fig = plt.figure(figsize=(7.8, 2.55))
outer = multi_fig.add_gridspec(1, 3, width_ratios=[3.0, 1.35, 0.78], wspace=0.62)
top = outer[0, 0].subgridspec(1, 2, width_ratios=[1.0, 0.24], wspace=0.00)
ax_joint = multi_fig.add_subplot(top[0, 0])
ax_marginal = multi_fig.add_subplot(top[0, 1])
ax_marker = multi_fig.add_subplot(outer[0, 1])
ax_overlap = multi_fig.add_subplot(outer[0, 2])

draw_joint_table(ax_joint)
draw_partial_jaccard_marginal(ax_marginal)
draw_neighbor_relation_stacks(ax_marker)
draw_neighborhood_overlap(ax_overlap, neighborhood_overlap_df, PLOT_K)
for axis, panel_label in [(ax_joint, "A"), (ax_marker, "B"), (ax_overlap, "C")]:
    axis.text(
        -0.12,
        1.08,
        panel_label,
        transform=axis.transAxes,
        fontsize=9.5,
        fontweight="bold",
        ha="left",
        va="top",
    )
multi_fig.subplots_adjust(left=0.035, right=0.995, bottom=0.24, top=0.88)
multi_fig.savefig(FIGURE_DIR / "fig_cross_study_unification.pdf", bbox_inches="tight")
multi_fig.savefig(FIGURE_DIR / "fig_cross_study_unification.png", bbox_inches="tight", dpi=300)

print(f"Profiles: {len(profiles_df):,}")
print(f"Cross-paper profile pairs: {total_cross_paper_pairs:,}")
print(joint_df.to_string(index=False))
print(f"saved {FIGURE_DIR / 'fig_cross_study_joint_distribution.pdf'}")
print(f"saved {FIGURE_DIR / 'fig_cross_study_unification.pdf'}")
