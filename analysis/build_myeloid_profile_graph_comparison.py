from __future__ import annotations

import math
import re
from collections import Counter
from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

from build_marker_corpus import build_records
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR, build_profile_summary, split_marker_text
from marker_label_utils import connected_components, label_relation, normalize_label


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY_PATH = RESULTS_DIR / "myeloid_marker_cluster_summary.tsv"
MEMBERSHIP_PATH = RESULTS_DIR / "myeloid_marker_cluster_membership.tsv"
REPORT_PATH = RESULTS_DIR / "myeloid_marker_cluster_summary.md"
COMPARISON_PATH = RESULTS_DIR / "myeloid_c1_c3_label_marker_summary.tsv"
FIGURE_PATH = FIGURE_DIR / "fig_myeloid_profile_graph_comparison.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig_myeloid_profile_graph_comparison.png"

MIN_MARKERS = 3
JACCARD_THRESHOLD = 0.5
MIN_COMPONENT_SIZE = 4
MAX_COMPONENTS = 7
CORE_GENE_FRACTION = 0.5
COMPARE_COMPONENTS = [1, 2, 3]
LABEL_LINKED_REGION_THRESHOLD = 0.25
MARKER_JACCARD_REGION_THRESHOLD = 0.20

MYELOID_LABEL_RE = re.compile(
    r"\b("
    r"MONOCYTE|MONOCYTES|MACROPHAGE|MACROPHAGES|MAC\b|MYELOID|MDSC|MICROGLIA|"
    r"TRAM|MOAM|DENDRITIC|PDC|CDC1|CDC2|CDC\b| DC\b|NEUTROPHIL|GRANULOCYTE|"
    r"MAST CELL|MAST CELLS|BASOPHIL|EOSINOPHIL"
    r")\b"
)

COMPONENT_COLORS = {
    1: "#7fbf7b",
    2: "#8c6bb1",
    3: "#80b1d3",
    4: "#fdb462",
    5: "#b3de69",
    6: "#d9d9d9",
    7: "#fb8072",
}

PROGRAM_GENES = {
    "Inflammatory monocyte-like": {
        "CD14",
        "LYZ",
        "S100A8",
        "S100A9",
        "S100A12",
        "VCAN",
        "FCN1",
        "LST1",
        "LGALS3",
        "IL1B",
        "CXCL8",
    },
    "Complement macrophage-like": {
        "C1QA",
        "C1QB",
        "C1QC",
        "APOE",
        "CD68",
        "CD163",
        "MRC1",
        "FOLR2",
        "MERTK",
        "CSF1R",
        "MARCO",
        "TREM2",
    },
    "Chemokine macrophage-like": {
        "CCL2",
        "CCL3",
        "CCL4",
        "CXCL2",
        "CXCL3",
        "CXCL8",
        "CXCL9",
        "CXCL10",
        "TNF",
        "IL1B",
    },
    "cDC1-like": {"CLEC9A", "XCR1", "BATF3", "IRF8", "CADM1"},
    "cDC2-like": {"CD1C", "CLEC10A", "FCER1A", "CD1E", "IRF4"},
    "pDC-like": {"IL3RA", "LILRA4", "CLEC4C", "IRF7", "TCF4"},
    "Mast/granulocyte-like": {
        "TPSAB1",
        "TPSB2",
        "CPA3",
        "KIT",
        "MS4A2",
        "FCER1A",
        "CSF3R",
        "CXCR2",
        "S100A8",
        "S100A9",
    },
}

def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def display_label(value: object) -> str:
    label = re.sub(r"\s+", " ", str(value)).strip()
    replacements = [
        ("MACROPHAGES", "MAC."),
        ("MACROPHAGE", "MAC."),
        ("MONOCYTE-DERIVED", "MONO.-DER."),
        ("MONOCYTES", "MONO."),
        ("MONOCYTE", "MONO."),
        ("DENDRITIC CELL", "DC"),
        ("PLASMACYTOID", "PDC"),
        ("NON-CLASSICAL", "NON-CLASS."),
        ("INFLAMMATORY", "INFLAM."),
        ("CLASSICAL", "CLASS."),
        ("DYSFUNCTIONAL", "DYSFUNC."),
        ("MYELOID CELL", "MYELOID"),
    ]
    for old, new in replacements:
        label = label.replace(old, new)
    return label


def label_group(label: object) -> str:
    text = f" {str(label).upper()} "
    monocyte = bool(re.search(r"\b(MONOCYTE|MONOCYTES|MONO)\b", text))
    macrophage = bool(re.search(r"\b(MACROPHAGE|MACROPHAGES|MAC\b|MICROGLIA|TRAM|MOAM)\b", text))
    dendritic = bool(re.search(r"\b(DENDRITIC|CDC1|CDC2|CDC\b|PDC| DC\b)", text))
    mast = bool(re.search(r"\b(MAST CELL|MAST CELLS|NEUTROPHIL|GRANULOCYTE|BASOPHIL|EOSINOPHIL)\b", text))
    if sum([monocyte, macrophage, dendritic, mast]) > 1:
        return "Mixed"
    if monocyte:
        return "Monocyte"
    if macrophage:
        return "Macrophage"
    if dendritic:
        return "Dendritic"
    if mast:
        return "Mast/granulocyte"
    return "Broad myeloid"


def marker_program(marker_names: object) -> str:
    markers = set(split_marker_text(marker_names))
    scores = {
        program: len(markers & genes)
        for program, genes in PROGRAM_GENES.items()
    }
    best_program, best_score = max(scores.items(), key=lambda item: (item[1], item[0]))
    return best_program if best_score else "Other myeloid"


def marker_sets(profiles_df: pd.DataFrame) -> list[set[str]]:
    return [set(split_marker_text(marker_ids)) for marker_ids in profiles_df["marker_ids"]]


def is_myeloid_label(value: object) -> bool:
    return bool(MYELOID_LABEL_RE.search(f" {str(value).upper()} "))


def build_myeloid_profiles() -> tuple[pd.DataFrame, dict[str, str]]:
    records_df = build_records()
    _profiles_df, filtered_profiles_df, _filtered_profiles, id_to_name = build_profile_summary(
        records_df,
        min_markers=MIN_MARKERS,
        feature_id_col="feature_id_std",
        feature_name_col="feature_name_std",
    )
    myeloid_df = filtered_profiles_df.loc[filtered_profiles_df["cell_type"].map(is_myeloid_label)].copy()
    myeloid_df = myeloid_df.reset_index(drop=True)
    myeloid_df["normalized_cell_type"] = myeloid_df["cell_type"].map(normalize_label)
    myeloid_df["marker_program"] = myeloid_df["marker_names"].map(marker_program)
    myeloid_df["label_group"] = myeloid_df["cell_type"].map(label_group)
    return myeloid_df, id_to_name


def summarize_components(
    myeloid_df: pd.DataFrame,
    profile_gene_sets: list[set[str]],
    id_to_name: dict[str, str],
    components: list[list[int]],
    edges: list[tuple[int, int, float]],
) -> pd.DataFrame:
    edge_lookup = {(min(i, j), max(i, j)): value for i, j, value in edges}
    rows = []
    for component_idx, component in enumerate(sorted(components, key=len, reverse=True), start=1):
        if len(component) < MIN_COMPONENT_SIZE:
            continue
        component_df = myeloid_df.iloc[component].copy()
        gene_counts = Counter(gene_id for idx in component for gene_id in profile_gene_sets[idx])
        core_gene_ids = [
            gene_id
            for gene_id, count in gene_counts.most_common()
            if count / len(component) >= CORE_GENE_FRACTION
        ]
        if not core_gene_ids:
            core_gene_ids = [gene_id for gene_id, _count in gene_counts.most_common(5)]
        top_gene_ids = [gene_id for gene_id, _count in gene_counts.most_common(10)]

        label_pair_count = 0
        relation_counts = Counter({"Exact": 0, "Partial": 0, "Different": 0})
        internal_jaccards = []
        normalized_labels = component_df["normalized_cell_type"].tolist()
        for local_a, local_b in combinations(range(len(component)), 2):
            idx_a = component[local_a]
            idx_b = component[local_b]
            if myeloid_df.iloc[idx_a]["paper_key"] == myeloid_df.iloc[idx_b]["paper_key"]:
                continue
            label_pair_count += 1
            relation_counts[label_relation(normalized_labels[local_a], normalized_labels[local_b])] += 1
            internal_jaccards.append(jaccard(profile_gene_sets[idx_a], profile_gene_sets[idx_b]))

        component_edges = [
            edge_lookup[(min(i, j), max(i, j))]
            for i, j in combinations(component, 2)
            if (min(i, j), max(i, j)) in edge_lookup
        ]
        label_counts = Counter(component_df["cell_type"])
        program_counts = Counter(component_df["marker_program"])
        dominant_program, dominant_program_count = program_counts.most_common(1)[0]
        rows.append(
            {
                "component": component_idx,
                "profiles": len(component),
                "papers": component_df["paper_key"].nunique(),
                "labels": component_df["cell_type"].nunique(),
                "dominant_program": dominant_program,
                "dominant_program_fraction": dominant_program_count / len(component),
                "core_marker_genes": "; ".join(id_to_name.get(gene_id, gene_id) for gene_id in core_gene_ids[:8]),
                "top_marker_genes": "; ".join(id_to_name.get(gene_id, gene_id) for gene_id in top_gene_ids),
                "top_labels": "; ".join(f"{label} ({count})" for label, count in label_counts.most_common(6)),
                "label_pairs": label_pair_count,
                "exact_label_pairs": relation_counts["Exact"],
                "partial_label_pairs": relation_counts["Partial"],
                "different_label_pairs": relation_counts["Different"],
                "exact_label_fraction": relation_counts["Exact"] / label_pair_count if label_pair_count else 0.0,
                "partial_label_fraction": relation_counts["Partial"] / label_pair_count if label_pair_count else 0.0,
                "different_label_fraction": relation_counts["Different"] / label_pair_count if label_pair_count else 0.0,
                "mean_internal_jaccard": float(np.mean(internal_jaccards)) if internal_jaccards else 0.0,
                "mean_edge_jaccard": float(np.mean(component_edges)) if component_edges else 0.0,
            }
        )
    return pd.DataFrame(rows).head(MAX_COMPONENTS)


def component_memberships(
    myeloid_df: pd.DataFrame,
    components: list[list[int]],
    summary_df: pd.DataFrame,
) -> pd.DataFrame:
    displayed_components = set(summary_df["component"].astype(int))
    rows = []
    for component_idx, component in enumerate(sorted(components, key=len, reverse=True), start=1):
        if component_idx not in displayed_components:
            continue
        for profile_idx in component:
            row = myeloid_df.iloc[profile_idx]
            rows.append(
                {
                    "component": component_idx,
                    "source_corpus": row["source_corpus"],
                    "paper_id": row["paper_id"],
                    "paper_key": row["paper_key"],
                    "cell_type": row["cell_type"],
                    "normalized_cell_type": row["normalized_cell_type"],
                    "n_markers": row["n_markers"],
                    "marker_names": row["marker_names"],
                    "marker_ids": row["marker_ids"],
                    "label_group": row["label_group"],
                    "marker_program": row["marker_program"],
                }
            )
    membership_df = pd.DataFrame(rows)
    membership_df["node"] = [f"p{idx}" for idx in range(len(membership_df))]
    membership_df["marker_set"] = membership_df["marker_ids"].map(lambda value: set(split_marker_text(value)))
    return membership_df


def build_graphs(profiles_df: pd.DataFrame) -> tuple[nx.Graph, nx.Graph]:
    label_graph = nx.Graph()
    marker_graph = nx.Graph()
    for row in profiles_df.itertuples(index=False):
        attrs = {
            "component": int(row.component),
            "cell_type": row.cell_type,
            "normalized_cell_type": row.normalized_cell_type,
            "paper_key": row.paper_key,
        }
        label_graph.add_node(row.node, **attrs)
        marker_graph.add_node(row.node, **attrs)

    for left_idx, right_idx in combinations(range(len(profiles_df)), 2):
        left = profiles_df.iloc[left_idx]
        right = profiles_df.iloc[right_idx]
        if left["paper_key"] == right["paper_key"]:
            continue
        relation = label_relation(left["normalized_cell_type"], right["normalized_cell_type"])
        if relation in {"Exact", "Partial"}:
            label_graph.add_edge(left["node"], right["node"], relation=relation)
        similarity = jaccard(left["marker_set"], right["marker_set"])
        if similarity >= JACCARD_THRESHOLD:
            marker_graph.add_edge(left["node"], right["node"], weight=similarity)
    return label_graph, marker_graph


def component_centers(components: list[int], radius: float = 0.98) -> dict[int, tuple[float, float]]:
    ordered = sorted(components)
    start_angle = math.radians(145)
    step = 2 * math.pi / max(len(ordered), 1)
    return {
        component: (radius * math.cos(start_angle - idx * step), radius * math.sin(start_angle - idx * step))
        for idx, component in enumerate(ordered)
    }


def component_layout(profiles_df: pd.DataFrame) -> dict[str, tuple[float, float]]:
    centers = component_centers(sorted(profiles_df["component"].unique()))
    positions = {}
    for component, component_df in profiles_df.groupby("component", sort=False):
        nodes = component_df.sort_values(["paper_key", "normalized_cell_type"])["node"].tolist()
        center_x, center_y = centers[int(component)]
        max_radius = 0.30 if len(nodes) > 12 else 0.22
        golden_angle = math.pi * (3 - math.sqrt(5))
        for idx, node in enumerate(nodes):
            if len(nodes) == 1:
                dx = dy = 0
            elif len(nodes) <= 6:
                angle = (2 * math.pi * idx / len(nodes)) + math.pi / 2
                dx = max_radius * math.cos(angle)
                dy = max_radius * math.sin(angle)
            else:
                angle = idx * golden_angle
                radius = max_radius * math.sqrt((idx + 0.5) / len(nodes))
                dx = radius * math.cos(angle)
                dy = radius * math.sin(angle)
            positions[node] = (center_x + dx, center_y + dy)
    return positions


def draw_graph(ax, graph: nx.Graph, positions: dict[str, tuple[float, float]]) -> None:
    ax.set_title("Myeloid-label graph", loc="left", fontsize=9.2, fontweight="bold", pad=8)
    ax.axis("off")
    ax.set_aspect("equal", adjustable="box", anchor="C")
    exact_edges = [(u, v) for u, v, data in graph.edges(data=True) if data.get("relation") == "Exact"]
    partial_edges = [(u, v) for u, v, data in graph.edges(data=True) if data.get("relation") == "Partial"]
    if partial_edges:
        nx.draw_networkx_edges(
            graph,
            positions,
            ax=ax,
            edgelist=partial_edges,
            width=0.55,
            edge_color="#777777",
            alpha=0.38,
            style="dashed",
        )
    if exact_edges:
        nx.draw_networkx_edges(
            graph,
            positions,
            ax=ax,
            edgelist=exact_edges,
            width=0.9,
            edge_color="#222222",
            alpha=0.48,
        )
    node_colors = [COMPONENT_COLORS[int(graph.nodes[node]["component"])] for node in graph.nodes]
    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=ax,
        node_color=node_colors,
        node_size=64,
        edgecolors="#222222",
        linewidths=0.45,
    )
    for component, component_df in pd.DataFrame(
        [
            {"component": int(data["component"]), "node": node}
            for node, data in graph.nodes(data=True)
        ]
    ).groupby("component"):
        nodes = component_df["node"].tolist()
        cx = sum(positions[node][0] for node in nodes) / len(nodes)
        cy = sum(positions[node][1] for node in nodes) / len(nodes)
        ax.scatter(
            [cx],
            [cy],
            s=220,
            color=COMPONENT_COLORS[component],
            edgecolor="#222222",
            linewidth=0.8,
            zorder=5,
        )
        ax.text(cx, cy, f"C{component}", ha="center", va="center", fontsize=7.0, fontweight="bold", zorder=6)


def figure_paths():
    return FIGURE_PATH, FIGURE_PNG_PATH


def comparison_profiles(profiles_df: pd.DataFrame) -> pd.DataFrame:
    return profiles_df.loc[profiles_df["component"].isin(COMPARE_COMPONENTS)].copy()


def compact_labels(value: object, max_items: int = 4) -> str:
    labels = []
    for item in [part.strip() for part in str(value).split(";") if part.strip()]:
        item = re.sub(r"\s+\(\d+\)$", "", item)
        labels.append(display_label(item))
    return "; ".join(labels[:max_items])


def pairwise_component_metrics(profiles_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for left_idx, right_idx in combinations(range(len(profiles_df)), 2):
        left = profiles_df.iloc[left_idx]
        right = profiles_df.iloc[right_idx]
        if left["paper_key"] == right["paper_key"]:
            continue
        left_component = int(left["component"])
        right_component = int(right["component"])
        component_pair = tuple(sorted((left_component, right_component)))
        relation = label_relation(left["normalized_cell_type"], right["normalized_cell_type"])
        rows.append(
            {
                "component_pair": f"C{component_pair[0]}-C{component_pair[1]}",
                "relation": relation,
                "label_linked": relation in {"Exact", "Partial"},
                "marker_jaccard": jaccard(left["marker_set"], right["marker_set"]),
            }
        )
    pairs_df = pd.DataFrame(rows)
    if pairs_df.empty:
        return pd.DataFrame(
            columns=["component_pair", "pairs", "label_linked_fraction", "mean_marker_jaccard"]
        )
    summary_rows = []
    ordered_pairs = ["C1-C1", "C2-C2", "C3-C3", "C1-C2", "C1-C3", "C2-C3"]
    for component_pair in ordered_pairs:
        pair_df = pairs_df.loc[pairs_df["component_pair"].eq(component_pair)]
        if pair_df.empty:
            continue
        relation_counts = Counter(pair_df["relation"])
        summary_rows.append(
            {
                "component_pair": component_pair,
                "pairs": len(pair_df),
                "exact_label_pairs": relation_counts["Exact"],
                "partial_label_pairs": relation_counts["Partial"],
                "different_label_pairs": relation_counts["Different"],
                "label_linked_fraction": float(pair_df["label_linked"].mean()),
                "mean_marker_jaccard": float(pair_df["marker_jaccard"].mean()),
            }
        )
    return pd.DataFrame(summary_rows)


def ordered_heatmap_profiles(profiles_df: pd.DataFrame) -> pd.DataFrame:
    return profiles_df.sort_values(
        ["component", "marker_program", "label_group", "cell_type", "paper_key"]
    ).reset_index(drop=True)


def draw_cluster_boundaries(ax, ordered_df: pd.DataFrame, show_x_labels: bool = True) -> None:
    counts = ordered_df.groupby("component", sort=True).size()
    starts = np.r_[0, np.cumsum(counts.values)[:-1]]
    centers = starts + (counts.values - 1) / 2
    labels = [f"C{component}" for component in counts.index]
    ax.set_xticks(centers)
    ax.set_yticks(centers)
    ax.set_yticklabels(labels, fontsize=7.0)
    if show_x_labels:
        ax.set_xticklabels(labels, fontsize=7.0)
    else:
        ax.set_xticklabels([])
    for boundary in np.cumsum(counts.values)[:-1]:
        ax.axhline(boundary - 0.5, color="white", linewidth=1.4)
        ax.axvline(boundary - 0.5, color="white", linewidth=1.4)
    for component, start, count in zip(counts.index, starts, counts.values, strict=True):
        ax.add_patch(
            Rectangle(
                (start - 0.5, start - 0.5),
                count,
                count,
                fill=False,
                edgecolor=COMPONENT_COLORS[int(component)],
                linewidth=1.3,
            )
        )
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)


def draw_marker_similarity_blocks(ax, ordered_df: pd.DataFrame, cax=None) -> None:
    marker_sets_list = ordered_df["marker_set"].tolist()
    matrix = np.zeros((len(ordered_df), len(ordered_df)))
    for row_idx, left in enumerate(marker_sets_list):
        for col_idx, right in enumerate(marker_sets_list):
            matrix[row_idx, col_idx] = jaccard(left, right)

    image = ax.imshow(matrix, cmap="Greys", vmin=0, vmax=1, interpolation="nearest")
    ax.set_title("Marker-gene similarity", loc="left", fontsize=9.2, fontweight="bold", pad=8)
    ax.set_ylabel("Marker-profile cluster", fontsize=7.0, labelpad=3)
    draw_cluster_boundaries(ax, ordered_df, show_x_labels=False)
    if cax is None:
        cbar = ax.figure.colorbar(image, ax=ax, fraction=0.047, pad=0.025)
    else:
        cbar = ax.figure.colorbar(image, cax=cax)
    cbar.ax.tick_params(labelsize=5.8, length=2, width=0.5)
    cbar.set_label("Jaccard", fontsize=6.2)


def draw_label_link_blocks(ax, ordered_df: pd.DataFrame) -> None:
    matrix = np.zeros((len(ordered_df), len(ordered_df)))
    for row_idx, left in ordered_df.iterrows():
        for col_idx, right in ordered_df.iterrows():
            if row_idx == col_idx:
                matrix[row_idx, col_idx] = 1.0
            elif left["paper_key"] == right["paper_key"]:
                matrix[row_idx, col_idx] = np.nan
            else:
                relation = label_relation(left["normalized_cell_type"], right["normalized_cell_type"])
                if relation == "Exact":
                    matrix[row_idx, col_idx] = 1.0
                elif relation == "Partial":
                    matrix[row_idx, col_idx] = 0.5
                else:
                    matrix[row_idx, col_idx] = 0.0

    cmap = ListedColormap(["#ffffff", "#bdbdbd", "#222222"])
    cmap.set_bad("#f6f6f6")
    norm = BoundaryNorm([-0.1, 0.25, 0.75, 1.1], cmap.N)
    ax.imshow(matrix, cmap=cmap, norm=norm, interpolation="nearest")
    ax.set_title("Celltype-label relation", loc="left", fontsize=9.2, fontweight="bold", pad=8)
    ax.set_xlabel("Marker-profile cluster", fontsize=7.0, labelpad=3)
    ax.set_ylabel("Marker-profile cluster", fontsize=7.0, labelpad=3)
    draw_cluster_boundaries(ax, ordered_df, show_x_labels=True)


def draw_label_marker_summary(ax, profiles_df: pd.DataFrame) -> None:
    metrics_df = pairwise_component_metrics(profiles_df)
    ax.set_title("Label linkage vs marker overlap", loc="left", fontsize=8.5, fontweight="bold", pad=6)
    x_cut = LABEL_LINKED_REGION_THRESHOLD
    y_cut = MARKER_JACCARD_REGION_THRESHOLD
    regions = [
        (0, 0, x_cut, y_cut, "#ededed", "Likely\ndifferent"),
        (x_cut, 0, 1 - x_cut, y_cut, "#fff1a8", "Label-linked,\nmarker split"),
        (0, y_cut, x_cut, 1 - y_cut, "#dcecf7", "Marker-linked,\nlabel drift"),
        (x_cut, y_cut, 1 - x_cut, 1 - y_cut, "#dff0d8", "Likely\nsame"),
    ]
    for x0, y0, width, height, color, label in regions:
        ax.add_patch(
            Rectangle(
                (x0, y0),
                width,
                height,
                facecolor=color,
                edgecolor="none",
                alpha=0.58,
                zorder=0,
            )
        )
        ax.text(
            x0 + width / 2,
            y0 + height / 2,
            label,
            fontsize=5.8,
            ha="center",
            va="center",
            color="#555555",
            alpha=0.88,
            zorder=1,
        )
    ax.axvline(x_cut, color="#777777", linewidth=0.65, alpha=0.85, zorder=1)
    ax.axhline(y_cut, color="#777777", linewidth=0.65, alpha=0.85, zorder=1)
    within = metrics_df["component_pair"].str.split("-").map(lambda parts: parts[0] == parts[1])
    colors = [
        COMPONENT_COLORS[int(pair[1])]
        if is_within
        else "#d0d0d0"
        for pair, is_within in zip(metrics_df["component_pair"], within, strict=True)
    ]
    ax.scatter(
        metrics_df["label_linked_fraction"],
        metrics_df["mean_marker_jaccard"],
        s=48,
        color=colors,
        edgecolor="#222222",
        linewidth=0.6,
        zorder=3,
    )
    for row in metrics_df.itertuples(index=False):
        dx = 0.018 if row.label_linked_fraction < 0.70 else -0.03
        ha = "left" if row.label_linked_fraction < 0.70 else "right"
        ax.text(
            row.label_linked_fraction + dx,
            row.mean_marker_jaccard + 0.018,
            row.component_pair,
            fontsize=6.1,
            ha=ha,
            va="bottom",
        )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Label-linked pairs", fontsize=6.7)
    ax.set_ylabel("Mean marker Jaccard", fontsize=6.7)
    ax.tick_params(labelsize=5.8, length=2, width=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)


def draw_marker_program_table(ax, summary_df: pd.DataFrame) -> None:
    table_df = summary_df.loc[summary_df["component"].isin(COMPARE_COMPONENTS)].copy()
    ax.set_title("Core genes and common labels", loc="left", fontsize=8.5, fontweight="bold", pad=6)
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    columns = [
        (0.02, 0.13, "Cluster"),
        (0.22, 0.52, "Core genes"),
        (0.62, 0.98, "Common labels"),
    ]
    header_y = 0.88
    row_ys = [0.66, 0.42, 0.18]
    for x0, _x1, label in columns:
        ax.text(x0, header_y, label, fontsize=6.4, fontweight="bold", va="center", ha="left")
    ax.plot([0.02, 0.98], [0.80, 0.80], color="#222222", linewidth=0.7)
    for y in [0.54, 0.30, 0.06]:
        ax.plot([0.02, 0.98], [y, y], color="#cfcfcf", linewidth=0.45)

    for y, row in zip(row_ys, table_df.itertuples(index=False), strict=True):
        component = int(row.component)
        ax.scatter(
            [0.065],
            [y],
            s=190,
            color=COMPONENT_COLORS[component],
            edgecolor="#222222",
            linewidth=0.6,
            zorder=2,
        )
        ax.text(0.065, y, f"C{component}", fontsize=6.2, fontweight="bold", ha="center", va="center", zorder=3)
        ax.text(0.22, y, str(row.core_marker_genes).replace("; ", "\n"), fontsize=6.6, va="center", ha="left")
        ax.text(0.62, y, compact_labels(row.top_labels, max_items=4).replace("; ", "\n"), fontsize=6.0, va="center", ha="left")


def draw_legends(fig) -> None:
    fig.legend(
        handles=[
            Line2D([0], [0], color="#222222", linewidth=0.9, label="Exact label"),
            Line2D([0], [0], color="#777777", linewidth=0.7, linestyle="--", label="Partial label"),
            Patch(facecolor=COMPONENT_COLORS[1], edgecolor="#222222", label="C1"),
            Patch(facecolor=COMPONENT_COLORS[2], edgecolor="#222222", label="C2"),
            Patch(facecolor=COMPONENT_COLORS[3], edgecolor="#222222", label="C3"),
        ],
        loc="lower center",
        bbox_to_anchor=(0.49, 0.018),
        ncol=5,
        frameon=False,
        fontsize=5.8,
        handlelength=1.6,
        handletextpad=0.45,
        columnspacing=0.9,
    )


def write_report(myeloid_df: pd.DataFrame, summary_df: pd.DataFrame, figure_path) -> None:
    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Myeloid Marker Cluster Summary",
                "",
                "## Assumptions",
                "",
                "- Unit of analysis is one paper-celltype marker profile: a paper, a reported cell type label, and a binary vector of mapped Ensembl gene IDs.",
                "- Profiles are restricted to human, source-verified marker records with at least three mapped marker genes.",
                "- Myeloid profiles are selected by regex over reported labels and include monocyte/macrophage, dendritic, mast/granulocyte, microglia, MDSC, and broad myeloid labels.",
                f"- Marker groups are connected components of cross-paper profiles with marker-gene Jaccard >= {JACCARD_THRESHOLD:.2f}.",
                "- Program labels are heuristic marker-gene summaries used for figure orientation, not a proposed ontology.",
                f"- Region labels in the C1-C3 summary use label-linked fraction >= {LABEL_LINKED_REGION_THRESHOLD:.2f} and mean marker Jaccard >= {MARKER_JACCARD_REGION_THRESHOLD:.2f} as visual thresholds.",
                "",
                "## Outputs",
                "",
                f"- Figure: `{figure_path.relative_to(REPO_ROOT)}`",
                f"- Summary table: `{SUMMARY_PATH.relative_to(REPO_ROOT)}`",
                f"- Membership table: `{MEMBERSHIP_PATH.relative_to(REPO_ROOT)}`",
                f"- C1-C3 comparison table: `{COMPARISON_PATH.relative_to(REPO_ROOT)}`",
                "",
                "## Counts",
                "",
                f"- Myeloid profiles: {len(myeloid_df):,}",
                f"- Papers: {myeloid_df['paper_key'].nunique():,}",
                f"- Reported labels: {myeloid_df['cell_type'].nunique():,}",
                f"- Marker groups displayed: {len(summary_df):,}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    figure_path, figure_png_path = figure_paths()
    myeloid_df, id_to_name = build_myeloid_profiles()
    profile_gene_sets = marker_sets(myeloid_df)
    components, edges = connected_components(
        profile_gene_sets,
        myeloid_df["paper_key"].tolist(),
        threshold=JACCARD_THRESHOLD,
    )
    summary_df = summarize_components(myeloid_df, profile_gene_sets, id_to_name, components, edges)
    membership_df = component_memberships(myeloid_df, components, summary_df)
    summary_df.to_csv(SUMMARY_PATH, sep="\t", index=False)
    membership_df.drop(columns=["node", "marker_set"]).to_csv(MEMBERSHIP_PATH, sep="\t", index=False)
    write_report(myeloid_df, summary_df, figure_path)

    comparison_df = comparison_profiles(membership_df)
    comparison_metrics_df = pairwise_component_metrics(comparison_df)
    comparison_metrics_df.to_csv(COMPARISON_PATH, sep="\t", index=False)
    label_graph, _marker_graph = build_graphs(comparison_df)
    positions = component_layout(comparison_df)

    ordered_comparison_df = ordered_heatmap_profiles(comparison_df)

    fig = plt.figure(figsize=(11.8, 6.35))
    grid = fig.add_gridspec(
        2,
        3,
        width_ratios=[0.92, 0.92, 0.78],
        height_ratios=[0.62, 0.38],
        wspace=0.24,
        hspace=0.28,
        left=0.04,
        right=0.985,
        top=0.91,
        bottom=0.13,
    )
    ax_graph = fig.add_subplot(grid[:, 0])
    heatmap_grid = grid[:, 1].subgridspec(
        2,
        2,
        width_ratios=[1, 0.045],
        height_ratios=[1, 1],
        wspace=0.06,
        hspace=0.22,
    )
    ax_marker_blocks = fig.add_subplot(heatmap_grid[0, 0])
    ax_label_blocks = fig.add_subplot(heatmap_grid[1, 0])
    ax_marker_cbar = fig.add_subplot(heatmap_grid[0, 1])
    ax_label_spacer = fig.add_subplot(heatmap_grid[1, 1])
    ax_label_spacer.axis("off")
    ax_summary = fig.add_subplot(grid[0, 2])
    ax_programs = fig.add_subplot(grid[1, 2])

    draw_graph(ax_graph, label_graph, positions)
    draw_marker_similarity_blocks(ax_marker_blocks, ordered_comparison_df, cax=ax_marker_cbar)
    draw_label_link_blocks(ax_label_blocks, ordered_comparison_df)
    draw_label_marker_summary(ax_summary, comparison_df)
    draw_marker_program_table(ax_programs, summary_df)
    draw_legends(fig)

    fig.savefig(figure_path, bbox_inches="tight")
    fig.savefig(figure_png_path, bbox_inches="tight", dpi=300)
    plt.close(fig)

    print(f"Myeloid profiles: {len(myeloid_df):,}")
    print(f"Components displayed: {len(summary_df):,}")
    print(f"Wrote {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MEMBERSHIP_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {COMPARISON_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {figure_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {figure_png_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
