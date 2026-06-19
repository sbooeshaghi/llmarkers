from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from scipy.cluster.hierarchy import leaves_list, linkage
from scipy.spatial.distance import squareform

from build_marker_stability_prototype import build_records
from build_tcell_marker_cluster_summary import normalize_label
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR, build_profile_summary, split_marker_text


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

MIN_MARKERS = 3
MARKER_CLUSTER_JACCARD = 0.50
MIN_MARKER_CLUSTER_SIZE = 4
EXACT_LABEL = "T CELL"

FIGURE_PATH = FIGURE_DIR / "fig5_cluster_prototypes.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig5_cluster_prototypes.png"
CLUSTER_SUMMARY_PATH = RESULTS_DIR / "fig5_marker_cluster_summary.tsv"
CLUSTER_GENE_SCORES_PATH = RESULTS_DIR / "fig5_cluster_gene_coverage_purity.tsv"
TCELL_MEMBERSHIP_PATH = RESULTS_DIR / "fig5_exact_tcell_marker_subclusters.tsv"


def build_profiles() -> tuple[pd.DataFrame, dict[str, str]]:
    records_df = build_records()
    _profiles_df, profiles_df, _filtered_profiles, id_to_name = build_profile_summary(
        records_df,
        min_markers=MIN_MARKERS,
        feature_id_col="feature_id_std",
        feature_name_col="feature_name_std",
    )
    profiles_df = profiles_df.reset_index(drop=True)
    profiles_df["profile_idx"] = np.arange(len(profiles_df))
    profiles_df["profile_uid"] = [
        f"{row.source_corpus}|{row.paper_id}|{row.cell_type}"
        for row in profiles_df.itertuples(index=False)
    ]
    profiles_df["normalized_cell_type"] = profiles_df["cell_type"].map(normalize_label)
    profiles_df["marker_set"] = profiles_df["marker_ids"].map(lambda value: set(split_marker_text(value)))
    return profiles_df, id_to_name


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def marker_pair_edges(
    profiles_df: pd.DataFrame,
    threshold: float,
) -> list[tuple[int, int, float]]:
    gene_to_profiles: dict[str, list[int]] = defaultdict(list)
    for row in profiles_df.itertuples(index=False):
        for gene_id in row.marker_set:
            gene_to_profiles[gene_id].append(int(row.profile_idx))

    candidate_pairs: set[tuple[int, int]] = set()
    for profile_indices in gene_to_profiles.values():
        for left_idx, right_idx in combinations(sorted(set(profile_indices)), 2):
            if profiles_df.iloc[left_idx]["paper_key"] == profiles_df.iloc[right_idx]["paper_key"]:
                continue
            candidate_pairs.add((left_idx, right_idx))

    edges = []
    for left_idx, right_idx in sorted(candidate_pairs):
        similarity = jaccard(
            profiles_df.iloc[left_idx]["marker_set"],
            profiles_df.iloc[right_idx]["marker_set"],
        )
        if similarity >= threshold:
            edges.append((left_idx, right_idx, similarity))
    return edges


def connected_components(n_nodes: int, edges: list[tuple[int, int, float]]) -> list[list[int]]:
    adjacency = [set() for _ in range(n_nodes)]
    for left_idx, right_idx, _similarity in edges:
        adjacency[left_idx].add(right_idx)
        adjacency[right_idx].add(left_idx)

    components = []
    seen: set[int] = set()
    for start_idx in range(n_nodes):
        if start_idx in seen or not adjacency[start_idx]:
            continue
        stack = [start_idx]
        seen.add(start_idx)
        component = []
        while stack:
            idx = stack.pop()
            component.append(idx)
            for neighbor_idx in adjacency[idx]:
                if neighbor_idx not in seen:
                    seen.add(neighbor_idx)
                    stack.append(neighbor_idx)
        components.append(sorted(component))
    return sorted(components, key=len, reverse=True)


def summarize_marker_clusters(
    profiles_df: pd.DataFrame,
    components: list[list[int]],
    edges: list[tuple[int, int, float]],
    id_to_name: dict[str, str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    edge_lookup = {(min(left, right), max(left, right)): value for left, right, value in edges}
    cluster_rows = []
    membership_rows = []
    cluster_id = 0
    for component in components:
        if len(component) < MIN_MARKER_CLUSTER_SIZE:
            continue
        cluster_id += 1
        cluster_df = profiles_df.iloc[component].copy()
        label_counts = Counter(cluster_df["normalized_cell_type"])
        dominant_label, dominant_count = label_counts.most_common(1)[0]
        gene_counts = Counter(gene_id for idx in component for gene_id in profiles_df.iloc[idx]["marker_set"])
        core_gene_ids = [
            gene_id
            for gene_id, count in gene_counts.most_common()
            if count / len(component) >= 0.5
        ]
        if not core_gene_ids:
            core_gene_ids = [gene_id for gene_id, _count in gene_counts.most_common(6)]
        component_edges = [
            edge_lookup[(min(left, right), max(left, right))]
            for left, right in combinations(component, 2)
            if (min(left, right), max(left, right)) in edge_lookup
        ]
        labels_display = "; ".join(
            f"{label} ({count})"
            for label, count in label_counts.most_common(6)
        )
        cluster_rows.append(
            {
                "cluster": cluster_id,
                "n_profiles": len(component),
                "n_papers": cluster_df["paper_key"].nunique(),
                "n_labels": len(label_counts),
                "dominant_label": dominant_label,
                "dominant_label_fraction": dominant_count / len(component),
                "label_entropy": entropy_from_counts(label_counts),
                "mean_edge_jaccard": float(np.mean(component_edges)) if component_edges else 0.0,
                "core_genes": "; ".join(id_to_name.get(gene_id, gene_id) for gene_id in core_gene_ids[:8]),
                "top_labels": labels_display,
            }
        )
        for idx in component:
            row = profiles_df.iloc[idx]
            membership_rows.append(
                {
                    "cluster": cluster_id,
                    "profile_idx": idx,
                    "profile_uid": row["profile_uid"],
                    "paper_key": row["paper_key"],
                    "cell_type": row["cell_type"],
                    "normalized_cell_type": row["normalized_cell_type"],
                    "marker_names": row["marker_names"],
                    "marker_ids": row["marker_ids"],
                }
            )
    return pd.DataFrame(cluster_rows), pd.DataFrame(membership_rows)


def entropy_from_counts(counts: Counter[str]) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    probabilities = np.asarray(list(counts.values()), dtype=float) / total
    return float(-(probabilities * np.log2(probabilities)).sum())


def exact_label_subclusters(
    profiles_df: pd.DataFrame,
    exact_label: str,
    threshold: float = 0.20,
) -> tuple[pd.DataFrame, np.ndarray, list[int]]:
    label_df = profiles_df.loc[profiles_df["normalized_cell_type"].eq(exact_label)].copy().reset_index(drop=True)
    if label_df.empty:
        return label_df, np.empty((0, 0)), []
    n_profiles = len(label_df)
    jaccard_matrix = np.eye(n_profiles)
    for left_idx, right_idx in combinations(range(n_profiles), 2):
        similarity = jaccard(label_df.iloc[left_idx]["marker_set"], label_df.iloc[right_idx]["marker_set"])
        jaccard_matrix[left_idx, right_idx] = similarity
        jaccard_matrix[right_idx, left_idx] = similarity

    if n_profiles > 2:
        distances = 1 - jaccard_matrix
        order = leaves_list(linkage(squareform(distances, checks=False), method="average")).tolist()
    else:
        order = list(range(n_profiles))

    adjacency = [set() for _ in range(n_profiles)]
    for left_idx, right_idx in combinations(range(n_profiles), 2):
        if jaccard_matrix[left_idx, right_idx] >= threshold:
            adjacency[left_idx].add(right_idx)
            adjacency[right_idx].add(left_idx)

    subcluster = np.zeros(n_profiles, dtype=int)
    seen: set[int] = set()
    subcluster_id = 0
    for start_idx in order:
        if start_idx in seen:
            continue
        subcluster_id += 1
        stack = [start_idx]
        seen.add(start_idx)
        while stack:
            idx = stack.pop()
            subcluster[idx] = subcluster_id
            for neighbor_idx in adjacency[idx]:
                if neighbor_idx not in seen:
                    seen.add(neighbor_idx)
                    stack.append(neighbor_idx)
    label_df["subcluster"] = subcluster
    return label_df, jaccard_matrix, order


def cluster_gene_scores(
    profiles_df: pd.DataFrame,
    cluster_summary_df: pd.DataFrame,
    membership_df: pd.DataFrame,
    id_to_name: dict[str, str],
) -> pd.DataFrame:
    profile_gene_sets = profiles_df.set_index("profile_idx")["marker_set"].to_dict()
    all_profile_count = len(profiles_df)
    global_gene_counts = Counter(
        gene_id
        for marker_set in profiles_df["marker_set"]
        for gene_id in marker_set
    )
    rows = []
    for cluster in cluster_summary_df["cluster"]:
        cluster_profile_ids = set(
            membership_df.loc[membership_df["cluster"].eq(cluster), "profile_idx"].astype(int)
        )
        if not cluster_profile_ids:
            continue
        cluster_n = len(cluster_profile_ids)
        outside_n = all_profile_count - cluster_n
        cluster_gene_counts = Counter(
            gene_id
            for profile_idx in cluster_profile_ids
            for gene_id in profile_gene_sets[profile_idx]
        )
        for gene_id, in_count in cluster_gene_counts.items():
            global_count = global_gene_counts[gene_id]
            outside_count = max(global_count - in_count, 0)
            coverage = in_count / cluster_n if cluster_n else 0.0
            leakage = outside_count / outside_n if outside_n else 0.0
            purity = in_count / global_count if global_count else 0.0
            harmonic = (
                2 * coverage * purity / (coverage + purity)
                if coverage + purity > 0
                else 0.0
            )
            rows.append(
                {
                    "cluster": int(cluster),
                    "gene_id": gene_id,
                    "gene_name": id_to_name.get(gene_id, gene_id),
                    "n_profiles_cluster": cluster_n,
                    "n_profiles_with_gene_in_cluster": in_count,
                    "n_profiles_with_gene_global": global_count,
                    "coverage": coverage,
                    "outside_prevalence": leakage,
                    "purity": purity,
                    "coverage_purity_hmean": harmonic,
                }
            )
    return pd.DataFrame(rows)


def selected_clusters(cluster_summary_df: pd.DataFrame) -> list[int]:
    selected: list[int] = []
    if not cluster_summary_df.empty:
        selected.append(int(cluster_summary_df.sort_values("n_profiles", ascending=False).iloc[0]["cluster"]))
    high_purity = cluster_summary_df.loc[cluster_summary_df["dominant_label_fraction"].ge(0.75)]
    if not high_purity.empty:
        selected.append(int(high_purity.sort_values("n_profiles", ascending=False).iloc[0]["cluster"]))
    low_purity = cluster_summary_df.loc[cluster_summary_df["dominant_label_fraction"].lt(0.4)]
    if not low_purity.empty:
        selected.append(int(low_purity.sort_values("n_profiles", ascending=False).iloc[0]["cluster"]))
    for pattern in ["T CELL", "MONOCYTE", "MACROPHAGE"]:
        subset = cluster_summary_df.loc[
            cluster_summary_df["top_labels"].str.contains(pattern, case=False, regex=False)
        ]
        if not subset.empty:
            selected.append(int(subset.sort_values("n_profiles", ascending=False).iloc[0]["cluster"]))
    deduped = []
    for cluster in selected:
        if cluster not in deduped:
            deduped.append(cluster)
    return deduped[:4]


def plot_tcell_dissection(ax: plt.Axes, tcell_df: pd.DataFrame, jaccard_matrix: np.ndarray, order: list[int]) -> None:
    ax.set_title("Exact T CELL profiles reclustered by genes", loc="left", fontsize=9, fontweight="bold")
    if tcell_df.empty:
        ax.axis("off")
        return
    ordered_matrix = jaccard_matrix[np.ix_(order, order)]
    cmap = LinearSegmentedColormap.from_list("white_black", ["#ffffff", "#222222"])
    ax.imshow(ordered_matrix, cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
    ax.set_xlabel("T CELL profiles", fontsize=7)
    ax.set_ylabel("T CELL profiles", fontsize=7)
    ax.set_xticks([])
    ax.set_yticks([])
    ordered_subclusters = tcell_df.iloc[order]["subcluster"].tolist()
    subcluster_counts = Counter(ordered_subclusters)
    boundaries = [
        idx
        for idx in range(1, len(ordered_subclusters))
        if ordered_subclusters[idx] != ordered_subclusters[idx - 1]
        and (
            subcluster_counts[ordered_subclusters[idx]] >= 3
            or subcluster_counts[ordered_subclusters[idx - 1]] >= 3
        )
    ]
    for boundary in boundaries:
        ax.axhline(boundary - 0.5, color="#d95f02", linewidth=0.7)
        ax.axvline(boundary - 0.5, color="#d95f02", linewidth=0.7)


def plot_cluster_purity(ax: plt.Axes, cluster_summary_df: pd.DataFrame) -> None:
    ax.set_title("Marker-gene clusters vary in label purity", loc="left", fontsize=9, fontweight="bold")
    if cluster_summary_df.empty:
        ax.axis("off")
        return
    ax.scatter(
        cluster_summary_df["n_profiles"],
        cluster_summary_df["dominant_label_fraction"],
        s=22 + 8 * np.sqrt(cluster_summary_df["n_papers"]),
        color="#d9d9d9",
        edgecolor="#222222",
        linewidth=0.45,
    )
    ax.set_xscale("log")
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel("Profiles in marker cluster", fontsize=7.5)
    ax.set_ylabel("Dominant label fraction", fontsize=7.5)
    label_df = pd.concat(
        [
            cluster_summary_df.sort_values("n_profiles", ascending=False).head(3),
            cluster_summary_df.sort_values("dominant_label_fraction", ascending=False).head(3),
            cluster_summary_df.sort_values("dominant_label_fraction", ascending=True).head(3),
        ],
        ignore_index=True,
    ).drop_duplicates("cluster")
    for row in label_df.itertuples(index=False):
        ax.annotate(
            f"C{row.cluster}\n{row.dominant_label}",
            (row.n_profiles, row.dominant_label_fraction),
            xytext=(4, 3),
            textcoords="offset points",
            fontsize=6.0,
            arrowprops={"arrowstyle": "-", "linewidth": 0.25, "color": "#777777"},
        )
    ax.tick_params(labelsize=6.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_gene_coverage_panel(
    ax: plt.Axes,
    gene_scores_df: pd.DataFrame,
    cluster_summary_df: pd.DataFrame,
    cluster: int,
) -> None:
    cluster_genes = gene_scores_df.loc[gene_scores_df["cluster"].eq(cluster)].copy()
    cluster_row = cluster_summary_df.loc[cluster_summary_df["cluster"].eq(cluster)].iloc[0]
    ax.set_title(
        f"C{cluster}: {cluster_row.dominant_label} ({int(cluster_row.n_profiles)} profiles)",
        loc="left",
        fontsize=7.8,
        fontweight="bold",
    )
    if cluster_genes.empty:
        ax.axis("off")
        return
    ax.scatter(
        cluster_genes["coverage"],
        cluster_genes["purity"],
        s=14 + 7 * np.sqrt(cluster_genes["n_profiles_with_gene_global"]),
        color="#d9d9d9",
        edgecolor="#222222",
        linewidth=0.35,
        alpha=0.85,
    )
    label_df = cluster_genes.sort_values(
        ["coverage_purity_hmean", "n_profiles_with_gene_global"],
        ascending=[False, False],
    ).head(6)
    for idx, row in enumerate(label_df.itertuples(index=False)):
        ax.annotate(
            row.gene_name,
            (row.coverage, row.purity),
            xytext=(5, 3 if idx % 2 == 0 else -6),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=5.7,
            arrowprops={"arrowstyle": "-", "linewidth": 0.25, "color": "#777777"},
        )
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Coverage", fontsize=6.6)
    ax.set_ylabel("Purity", fontsize=6.6)
    ax.tick_params(labelsize=5.8, length=2, width=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def main() -> None:
    profiles_df, id_to_name = build_profiles()
    edges = marker_pair_edges(profiles_df, threshold=MARKER_CLUSTER_JACCARD)
    components = connected_components(len(profiles_df), edges)
    cluster_summary_df, membership_df = summarize_marker_clusters(profiles_df, components, edges, id_to_name)
    gene_scores_df = cluster_gene_scores(profiles_df, cluster_summary_df, membership_df, id_to_name)
    tcell_df, tcell_jaccard, tcell_order = exact_label_subclusters(profiles_df, EXACT_LABEL)

    cluster_summary_df.to_csv(CLUSTER_SUMMARY_PATH, sep="\t", index=False)
    gene_scores_df.to_csv(CLUSTER_GENE_SCORES_PATH, sep="\t", index=False)
    tcell_df.to_csv(TCELL_MEMBERSHIP_PATH, sep="\t", index=False)

    chosen_clusters = selected_clusters(cluster_summary_df)
    fig = plt.figure(figsize=(9.4, 8.6))
    gs = fig.add_gridspec(3, 2, height_ratios=[0.72, 1, 1], wspace=0.30, hspace=0.42)
    plot_cluster_purity(fig.add_subplot(gs[0, :]), cluster_summary_df)

    for idx, cluster in enumerate(chosen_clusters):
        row = 1 + idx // 2
        plot_gene_coverage_panel(
            fig.add_subplot(gs[row, idx % 2]),
            gene_scores_df,
            cluster_summary_df,
            cluster,
        )

    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    fig.savefig(FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)

    print(f"Profiles: {len(profiles_df):,}")
    print(f"Marker-cluster edges at J>={MARKER_CLUSTER_JACCARD}: {len(edges):,}")
    print(f"Marker clusters with >= {MIN_MARKER_CLUSTER_SIZE} profiles: {len(cluster_summary_df):,}")
    print(f"Exact {EXACT_LABEL} profiles: {len(tcell_df):,}")
    print(f"Selected clusters: {', '.join(f'C{cluster}' for cluster in chosen_clusters)}")
    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PNG_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {CLUSTER_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {CLUSTER_GENE_SCORES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {TCELL_MEMBERSHIP_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
