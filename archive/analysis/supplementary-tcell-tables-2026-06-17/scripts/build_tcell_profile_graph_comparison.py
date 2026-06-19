from __future__ import annotations

import math
import re
from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.colors import to_rgb
from matplotlib.lines import Line2D
from matplotlib.offsetbox import AnnotationBbox, HPacker, TextArea, VPacker
from matplotlib.patches import FancyBboxPatch, Patch, Rectangle

from build_tcell_marker_cluster_summary import label_relation
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR, split_marker_text


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

MEMBERSHIP_PATH = RESULTS_DIR / "tcell_marker_cluster_membership.tsv"
SUMMARY_PATH = RESULTS_DIR / "tcell_marker_cluster_summary.tsv"
FIGURE_PATH = FIGURE_DIR / "fig_tcell_profile_graph_comparison.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig_tcell_profile_graph_comparison.png"

MARKER_JACCARD_THRESHOLD = 0.5
C2_SUBCLUSTER_THRESHOLD = 0.6
C2_MARKER_NEIGHBORS = 3
GRAPH_X_SHIFT = 0.14

COMPONENT_ORDER = [4, 5, 1, 2, 3, 6, 7]
COMPONENT_LABELS = {
    1: "C1",
    2: "C2",
    3: "C3",
    4: "C4",
    5: "C5",
    6: "C6",
    7: "C7",
}
COMPONENT_COLORS = {
    1: "#a8d8cf",
    2: "#8e6bbe",
    3: "#d97b66",
    4: "#eeeeee",
    5: "#cfcfcf",
    6: "#7a9e7e",
    7: "#c85f4b",
}
LABEL_GROUP_COLORS = {
    "Treg/regulatory": "#4c9a2a",
    "Exhausted": "#6b59a8",
    "Both": "#c0842c",
    "Other": "#bdbdbd",
}
MARKER_PROGRAM_GENES = [
    "FOXP3",
    "IL2RA",
    "IKZF2",
    "CCR8",
    "TNFRSF18",
    "LAYN",
    "CTLA4",
    "TIGIT",
    "HAVCR2",
    "LAG3",
    "PDCD1",
    "TOX",
    "CXCL13",
    "IFNG",
    "PRF1",
    "BATF",
    "ICOS",
]
TREG_PROGRAM_GENES = {"FOXP3", "IL2RA", "IKZF2", "CCR8", "TNFRSF18", "LAYN"}
EXHAUSTION_PROGRAM_GENES = {"LAG3", "HAVCR2", "PDCD1", "TOX", "CXCL13", "IFNG", "PRF1"}
LABEL_CALLOUT_OFFSETS = {
    1: (-0.58, -0.18),
    2: (0.02, -0.12),
    3: (0.02, -0.10),
    4: (-0.02, 0.00),
    5: (-0.02, -0.03),
    6: (0.03, 0.03),
    7: (-0.06, -0.04),
}
GENE_CALLOUT_OFFSETS = {
    1: (0.02, -0.10),
    2: (0.06, -0.10),
    3: (0.04, -0.10),
    4: (-0.03, -0.08),
    5: (0.02, -0.08),
    6: (0.02, -0.08),
    7: (0.02, -0.08),
}
GRAPH_BADGE_OFFSETS = {
    1: (0.02, 0.42),
    2: (0.42, 0.02),
    3: (0.30, -0.22),
    4: (-0.36, 0.06),
    5: (-0.34, -0.18),
    6: (0.26, 0.12),
    7: (-0.06, -0.32),
}


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def badge_text_color(component: int) -> str:
    if component in {2, 3, 6, 7}:
        return "white"
    return "#222222"


def load_profiles() -> pd.DataFrame:
    if not MEMBERSHIP_PATH.exists():
        raise SystemExit(f"Missing {MEMBERSHIP_PATH}. Run analysis/build_tcell_marker_cluster_summary.py first.")
    profiles_df = pd.read_csv(MEMBERSHIP_PATH, sep="\t")
    profiles_df = profiles_df.loc[profiles_df["component"].isin(COMPONENT_ORDER)].copy()
    profiles_df["node"] = [f"p{idx}" for idx in range(len(profiles_df))]
    profiles_df["marker_set"] = profiles_df["marker_ids"].map(lambda value: set(split_marker_text(value)))
    return profiles_df.reset_index(drop=True)


def load_summary() -> pd.DataFrame:
    if not SUMMARY_PATH.exists():
        raise SystemExit(f"Missing {SUMMARY_PATH}. Run analysis/build_tcell_marker_cluster_summary.py first.")
    return pd.read_csv(SUMMARY_PATH, sep="\t")


def compact_item_lines(value: object, max_items: int = 3) -> str:
    items = [item.strip() for item in str(value).split(";") if item.strip()]
    shown = items[:max_items]
    if len(items) > max_items:
        shown.append(f"+{len(items) - max_items}")
    return "\n".join(shown)


def compact_top_labels(value: object, total_labels: int | None = None, max_items: int = 3) -> str:
    labels = []
    for item in [item.strip() for item in str(value).split(";") if item.strip()][:max_items]:
        item = re.sub(r"\s+\(\d+\)$", "", item)
        label = item.replace(" T CELL", " T").replace(" T CELLS", " T")
        label = label.replace("EXHAUSTED", "EXH.").replace("CYTOTOXIC", "CYTO.")
        label = label.replace("TISSUE RESIDENT MEMORY", "TRM")
        label = label.replace("CENTRAL MEMORY", "TCM")
        label = label.replace("EFFECTOR", "EFF.")
        labels.append(label)
    if total_labels is not None and total_labels > max_items:
        labels.append(f"+{total_labels - max_items}")
    return "\n".join(labels)


def display_label(value: object) -> str:
    label = re.sub(r"\s+", " ", str(value)).strip()
    replacements = {
        "BRAIN METASTASIS-INFILTRATING": "BR. MET.",
        "CEFX-SPECIFIC": "CEFX-SPEC.",
        "TISSUE RESIDENT MEMORY": "TRM",
        "CENTRAL MEMORY": "TCM",
        "EXHAUSTION-LIKE": "EXH.-LIKE",
        "EXHAUSTED": "EXH.",
        "CYTOTOXIC": "CYTO.",
        "EFFECTOR": "EFF.",
        "REGULATORY": "REG.",
        "PROLIFERATING": "PROLIF.",
        "INFILTRATING": "INFIL.",
        "METASTASIS": "MET.",
        "UNEXPANDED": "UNEXP.",
        "SUBCLUSTER": "SUBCL.",
    }
    for old, new in replacements.items():
        label = label.replace(old, new)
    label = re.sub(r"CD([48])\s*\+\s*", r"CD\1+ ", label)
    label = label.replace("CD 4", "CD4").replace("CD 8", "CD8")
    label = label.replace("CEFX-SPEC. BR. MET. PD-1+ CD8+ T CELL", "CEFX-SPEC. PD-1+ CD8+ T")
    label = label.replace("CD4 + AND CD8 + T RM CELL", "CD4+/CD8+ TRM")
    label = label.replace("CD4 + NAIVE/TCM (NV/CM)", "CD4+ NAIVE/TCM")
    label = label.replace("CD4+ AND CD8+ T CELL", "CD4+/CD8+ T CELL")
    label = label.replace("EXH. T-CELL, T-REG. CELL", "EXH. T/TREG")
    label = label.replace("REG. T CELL (TREG)", "REG. T (TREG)")
    label = label.replace("CD8+ EXH. T CELL (TEXH)", "CD8+ EXH. T (TEXH)")
    return label


def label_column_count(n_labels: int) -> int:
    if n_labels >= 24:
        return 3
    if n_labels >= 10:
        return 2
    return 1


def unique_labels(profiles_df: pd.DataFrame, component: int) -> list[str]:
    return sorted(set(profiles_df.loc[profiles_df["component"].eq(component), "cell_type"].map(display_label)))


def label_columns(labels: list[str], max_cols: int | None = None) -> list[str]:
    n_cols = label_column_count(len(labels))
    if max_cols is not None:
        n_cols = min(n_cols, max_cols)
    n_rows = math.ceil(len(labels) / n_cols)
    return [
        "\n".join(labels[col_idx * n_rows : (col_idx + 1) * n_rows])
        for col_idx in range(n_cols)
    ]


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
        if relation == "Exact":
            label_graph.add_edge(left["node"], right["node"], relation=relation)

        marker_similarity = jaccard(left["marker_set"], right["marker_set"])
        if marker_similarity >= MARKER_JACCARD_THRESHOLD:
            marker_graph.add_edge(left["node"], right["node"], weight=marker_similarity)

    return label_graph, marker_graph


def label_group(row: pd.Series) -> str:
    label = str(row["cell_type"]).upper()
    normalized = str(row["normalized_cell_type"]).upper()
    has_treg = any(term in label or term in normalized for term in ["TREG", "T REG", "REGULATORY"])
    has_exhausted = any(term in label or term in normalized for term in ["EXHAUST", "TEXH"])
    if has_treg and has_exhausted:
        return "Both"
    if has_treg:
        return "Treg/regulatory"
    if has_exhausted:
        return "Exhausted"
    return "Other"


def marker_program(row: pd.Series) -> str:
    markers = set(str(row["marker_names"]).split(";"))
    treg_score = len(markers & TREG_PROGRAM_GENES)
    exhausted_score = len(markers & EXHAUSTION_PROGRAM_GENES)
    if treg_score >= 2 and treg_score > exhausted_score:
        return "Treg-like"
    if exhausted_score >= 2 and exhausted_score > treg_score:
        return "Exhausted-like"
    if treg_score >= 1 and exhausted_score >= 1:
        return "Mixed"
    if treg_score >= 1:
        return "Treg-like"
    if exhausted_score >= 1:
        return "Exhausted-like"
    return "Other-like"


def marker_program_sort_key(row: pd.Series) -> tuple[int, int, str, str]:
    if row["label_group"] == "Treg/regulatory":
        bucket = 0
    elif row["marker_program"] == "Treg-like":
        bucket = 1
    elif row["label_group"] == "Both":
        bucket = 2
    elif row["label_group"] == "Exhausted":
        bucket = 3
    elif row["marker_program"] in {"Exhausted-like", "Mixed"}:
        bucket = 4
    else:
        bucket = 5
    markers = set(str(row["marker_names"]).split(";"))
    signal = len(markers & (TREG_PROGRAM_GENES | EXHAUSTION_PROGRAM_GENES))
    return bucket, -signal, str(row["display_label"]), str(row["paper_key"])


def build_marker_graph_for_rows(rows_df: pd.DataFrame, threshold: float) -> nx.Graph:
    graph = nx.Graph()
    for row in rows_df.itertuples():
        graph.add_node(row.Index)
    for left_idx, right_idx in combinations(rows_df.index, 2):
        left = rows_df.loc[left_idx]
        right = rows_df.loc[right_idx]
        similarity = jaccard(left["marker_set"], right["marker_set"])
        if similarity >= threshold:
            graph.add_edge(left_idx, right_idx, weight=similarity)
    return graph


def build_marker_knn_graph_for_rows(rows_df: pd.DataFrame, k: int) -> nx.Graph:
    graph = nx.Graph()
    for row in rows_df.itertuples():
        graph.add_node(row.Index)
    for left_idx in rows_df.index:
        similarities = []
        left = rows_df.loc[left_idx]
        for right_idx in rows_df.index:
            if left_idx == right_idx:
                continue
            right = rows_df.loc[right_idx]
            similarity = jaccard(left["marker_set"], right["marker_set"])
            if similarity > 0:
                similarities.append((right_idx, similarity))
        for right_idx, similarity in sorted(similarities, key=lambda item: (-item[1], item[0]))[:k]:
            if graph.has_edge(left_idx, right_idx):
                graph[left_idx][right_idx]["weight"] = max(graph[left_idx][right_idx]["weight"], similarity)
            else:
                graph.add_edge(left_idx, right_idx, weight=similarity)
    return graph


def marker_subclusters(rows_df: pd.DataFrame, threshold: float) -> list[list[int]]:
    graph = build_marker_graph_for_rows(rows_df, threshold)
    components = [sorted(component) for component in nx.connected_components(graph)]
    return sorted(components, key=lambda component: (-len(component), component[0]))


def component_centers(radius: float = 0.98) -> dict[int, tuple[float, float]]:
    # Keep broad T-cell groups together on the left and place state-like groups
    # around the rest of the circle so the two graph panels can be compared by eye.
    circle_order = [4, 1, 6, 2, 3, 7, 5]
    start_angle = math.radians(160)
    angle_step = 2 * math.pi / len(circle_order)
    return {
        component: (
            radius * math.cos(start_angle - idx * angle_step),
            radius * math.sin(start_angle - idx * angle_step),
        )
        for idx, component in enumerate(circle_order)
    }


def local_member_radius(n_nodes: int) -> float:
    if n_nodes > 25:
        return 0.36
    if n_nodes > 12:
        return 0.30
    return 0.22


def component_layout(profiles_df: pd.DataFrame, marker_graph: nx.Graph) -> dict[str, tuple[float, float]]:
    centers = component_centers()
    positions = {}
    for component, component_df in profiles_df.groupby("component", sort=False):
        nodes = (
            component_df.sort_values(["paper_key", "normalized_cell_type"])["node"]
            .tolist()
        )
        center_x, center_y = centers[int(component)]
        max_radius = local_member_radius(len(nodes))
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


def callout_anchor(
    component: int,
    positions: dict[str, tuple[float, float]],
    nodes: list[str],
    distance: float = 0.64,
) -> tuple[float, float, str, str]:
    cx = sum(positions[node][0] for node in nodes) / len(nodes)
    cy = sum(positions[node][1] for node in nodes) / len(nodes)
    norm = math.hypot(cx, cy) or 1
    dx, dy = LABEL_CALLOUT_OFFSETS[component]
    x = cx + distance * cx / norm + dx
    y = cy + distance * cy / norm + dy
    ha = "center"
    va = "center"
    if cx / norm > 0.45:
        ha = "left"
    elif cx / norm < -0.45:
        ha = "right"
    if cy / norm > 0.55:
        va = "bottom"
    elif cy / norm < -0.55:
        va = "top"
    return x, y, ha, va


def draw_callout_box(
    ax,
    x: float,
    y: float,
    ha: str,
    va: str,
    title: str,
    columns: list[str],
    edge_color: str,
    body_size: float,
    footer: str | None = None,
    xycoords: str = "data",
) -> None:
    split_columns = [column.splitlines() for column in columns]
    title_area = TextArea(
        title,
        textprops={
            "fontsize": body_size + 0.35,
            "fontweight": "bold",
            "ha": "center",
        },
    )
    column_boxes = []
    for column in split_columns:
        lines = [
            TextArea(
                value,
                textprops={
                    "fontsize": body_size,
                    "family": "monospace",
                    "ha": "left",
                },
            )
            for value in column
        ]
        column_boxes.append(VPacker(children=lines, align="left", pad=0, sep=0))
    body = HPacker(children=column_boxes, align="top", pad=0, sep=8)
    children = [title_area, body]
    if footer:
        footer_area = TextArea(
            footer,
            textprops={
                "fontsize": body_size + 0.1,
                "family": "monospace",
                "ha": "center",
            },
        )
        children.append(footer_area)
    packed = VPacker(children=children, align="center", pad=0, sep=2)
    box_alignment = (
        {"left": 0, "center": 0.5, "right": 1}[ha],
        {"bottom": 0, "center": 0.5, "top": 1}[va],
    )
    annotation = AnnotationBbox(
        packed,
        (x, y),
        xycoords=xycoords,
        frameon=True,
        box_alignment=box_alignment,
        bboxprops={
            "boxstyle": "round,pad=0.18",
            "facecolor": "white",
            "edgecolor": edge_color,
            "linewidth": 0.85,
            "alpha": 0.95,
        },
        zorder=6,
    )
    annotation.set_clip_on(False)
    ax.add_artist(annotation)


def draw_graph(
    ax,
    graph: nx.Graph,
    positions: dict[str, tuple[float, float]],
    title: str,
) -> None:
    ax.set_title(title, loc="left", fontsize=9.2, fontweight="bold", pad=8)
    ax.axis("off")
    ax.set_aspect("equal", adjustable="box", anchor="C")

    exact_edges = [(u, v) for u, v, data in graph.edges(data=True) if data.get("relation") == "Exact"]
    weighted_edges = [
        (u, v, data.get("weight", 0.5))
        for u, v, data in graph.edges(data=True)
        if "weight" in data
    ]

    if weighted_edges:
        nx.draw_networkx_edges(
            graph,
            positions,
            ax=ax,
            edgelist=[(u, v) for u, v, _weight in weighted_edges],
            width=[0.65 + 1.7 * weight for _u, _v, weight in weighted_edges],
            edge_color="#444444",
            alpha=0.48,
        )
    if exact_edges:
        nx.draw_networkx_edges(
            graph,
            positions,
            ax=ax,
            edgelist=exact_edges,
            width=0.75,
            edge_color="#222222",
            alpha=0.55,
        )

    node_colors = [COMPONENT_COLORS[int(graph.nodes[node]["component"])] for node in graph.nodes]
    nx.draw_networkx_nodes(
        graph,
        positions,
        ax=ax,
        node_color=node_colors,
        node_size=32,
        edgecolors="#222222",
        linewidths=0.25,
    )

    for component in COMPONENT_ORDER:
        nodes = [
            node
            for node, attrs in graph.nodes(data=True)
            if int(attrs["component"]) == component
        ]
        if not nodes:
            continue
        cx = sum(positions[node][0] for node in nodes) / len(nodes)
        cy = sum(positions[node][1] for node in nodes) / len(nodes)
        dx, dy = GRAPH_BADGE_OFFSETS[component]
        bx = cx + dx
        by = cy + dy
        ax.scatter(
            [bx],
            [by],
            s=145,
            marker="o",
            facecolor=COMPONENT_COLORS[component],
            edgecolor="#222222",
            linewidth=0.55,
            zorder=7,
        )
        ax.text(
            bx,
            by,
            f"C{component}",
            ha="center",
            va="center",
            fontsize=5.2,
            fontweight="bold",
            color=badge_text_color(component),
            zorder=8,
        )

    ax.set_xlim(-1.65, 1.55)
    ax.set_ylim(-1.55, 1.55)


def draw_cluster_label_panel(
    ax,
    profiles_df: pd.DataFrame,
    summary_df: pd.DataFrame,
) -> None:
    ax.set_title("Marker-gene clusters", loc="left", fontsize=9.2, fontweight="bold", pad=8)
    ax.axis("off")

    row_by_component = {
        int(row.component): pd.Series(row._asdict())
        for row in summary_df.itertuples(index=False)
    }
    label_columns_by_component = {
        1: 2,
        2: 2,
        3: 2,
        4: 2,
        5: 2,
        6: 2,
        7: 2,
    }
    box_width = 0.96
    box_heights = {
        1: 0.232,
        2: 0.212,
        3: 0.172,
        4: 0.090,
        5: 0.090,
        6: 0.090,
        7: 0.090,
    }
    y = 0.995
    gap = 0.002
    for component in [1, 2, 3, 4, 5, 6, 7]:
        labels = unique_labels(profiles_df, component)
        core_genes = compact_item_lines(
            row_by_component[component]["core_marker_genes"],
            max_items=4,
        ).replace("\n", "; ")
        x = 0.02
        height = box_heights[component]
        patch = FancyBboxPatch(
            (x, y - height),
            box_width,
            height,
            boxstyle="round,pad=0.006",
            transform=ax.transAxes,
            facecolor="white",
            edgecolor="#c7c7c7",
            linewidth=1.0,
            clip_on=False,
        )
        ax.add_patch(patch)
        small_box = component in {4, 5, 6, 7}
        title_size = 6.5 if small_box else 7.5
        body_size = 5.35 if small_box else 5.85
        body_y_offset = 0.044 if small_box else 0.053
        footer_y_offset = 0.014 if small_box else 0.016
        badge_x = x + 0.030
        badge_y = y - 0.027
        ax.scatter(
            [badge_x],
            [badge_y],
            s=88,
            marker="o",
            facecolor=COMPONENT_COLORS[component],
            edgecolor="#222222",
            linewidth=0.45,
            transform=ax.transAxes,
            clip_on=False,
            zorder=3,
        )
        ax.text(
            badge_x,
            badge_y,
            f"C{component}",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=4.4,
            fontweight="bold",
            color=badge_text_color(component),
            clip_on=False,
            zorder=4,
        )
        ax.text(
            x + 0.055,
            y - 0.018,
            f"labels ({len(labels)})",
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=title_size,
            fontweight="bold",
            clip_on=False,
        )
        n_cols = label_columns_by_component.get(component, 1)
        n_rows = math.ceil(len(labels) / n_cols)
        columns = [
            "\n".join(labels[col_idx * n_rows : (col_idx + 1) * n_rows])
            for col_idx in range(n_cols)
        ]
        column_width = (box_width - 0.030) / len(columns)
        for col_idx, label_text in enumerate(columns):
            ax.text(
                x + 0.014 + col_idx * column_width,
                y - body_y_offset,
                label_text,
                transform=ax.transAxes,
                ha="left",
                va="top",
                fontsize=body_size,
                family="monospace",
                linespacing=0.88 if small_box else 0.90,
                clip_on=False,
            )
        ax.text(
            x + 0.014,
            y - height + footer_y_offset,
            f"Core: {core_genes}",
            transform=ax.transAxes,
            ha="left",
            va="bottom",
            fontsize=body_size,
            family="monospace",
            clip_on=False,
        )
        y -= height + gap


def draw_label_callouts(
    ax,
    graph: nx.Graph,
    positions: dict[str, tuple[float, float]],
    profiles_df: pd.DataFrame,
    summary_df: pd.DataFrame,
) -> None:
    row_by_component = {
        int(row.component): pd.Series(row._asdict())
        for row in summary_df.itertuples(index=False)
    }
    for component in COMPONENT_ORDER:
        nodes = [node for node, attrs in graph.nodes(data=True) if int(attrs["component"]) == component]
        if not nodes:
            continue
        x, y, ha, va = callout_anchor(component, positions, nodes)
        labels = unique_labels(profiles_df, component)
        core_genes = compact_item_lines(row_by_component[component]["core_marker_genes"], max_items=4).replace("\n", "; ")
        draw_callout_box(
            ax,
            x,
            y,
            ha,
            va,
            f"C{component} labels ({len(labels)})",
            label_columns(labels),
            COMPONENT_COLORS[component],
            body_size=3.55,
            footer=f"Core: {core_genes}",
        )


def draw_gene_callouts(
    ax,
    graph: nx.Graph,
    positions: dict[str, tuple[float, float]],
    summary_df: pd.DataFrame,
) -> None:
    row_by_component = {
        int(row.component): pd.Series(row._asdict())
        for row in summary_df.itertuples(index=False)
    }
    for component in COMPONENT_ORDER:
        nodes = [node for node, attrs in graph.nodes(data=True) if int(attrs["component"]) == component]
        if not nodes:
            continue
        xs = [positions[node][0] for node in nodes]
        ys = [positions[node][1] for node in nodes]
        cx = sum(xs) / len(xs)
        y_anchor = min(ys)
        dx, dy = GENE_CALLOUT_OFFSETS[component]
        row = row_by_component[component]
        detail = compact_item_lines(row["core_marker_genes"], max_items=3)
        draw_callout_box(
            ax,
            cx + dx,
            y_anchor + dy,
            "center",
            "top",
            f"C{component}",
            [detail],
            COMPONENT_COLORS[component],
            body_size=4.6,
        )


def draw_c2_subgraph(ax, profiles_df: pd.DataFrame) -> None:
    c2_df = profiles_df.loc[profiles_df["component"].eq(2)].copy()
    c2_df["label_group"] = c2_df.apply(label_group, axis=1)
    c2_df["display_label"] = c2_df["cell_type"].map(display_label)
    c2_df["marker_program"] = c2_df.apply(marker_program, axis=1)
    c2_df = c2_df.loc[c2_df["label_group"].isin(["Treg/regulatory", "Exhausted"])].copy()
    pair_groups = [
        ("Treg-Treg", "Treg/regulatory", "Treg/regulatory", "#e7f3e2"),
        ("Exh.-Exh.", "Exhausted", "Exhausted", "#ece8f5"),
        ("Treg-Exh.", "Treg/regulatory", "Exhausted", "#f0f0f0"),
    ]
    values_by_group = {label: [] for label, *_ in pair_groups}
    for left_idx, right_idx in combinations(range(len(c2_df)), 2):
        left = c2_df.iloc[left_idx]
        right = c2_df.iloc[right_idx]
        if left["paper_key"] == right["paper_key"]:
            continue
        pair = {left["label_group"], right["label_group"]}
        for label, left_group, right_group, _color in pair_groups:
            if left_group == right_group:
                if left["label_group"] == right["label_group"] == left_group:
                    values_by_group[label].append(jaccard(left["marker_set"], right["marker_set"]))
            elif pair == {left_group, right_group}:
                values_by_group[label].append(jaccard(left["marker_set"], right["marker_set"]))

    ax.set_title("C2 pairwise marker similarity", loc="left", fontsize=8.3, fontweight="bold", pad=5)
    x = np.arange(len(pair_groups))
    means = [
        np.mean(values_by_group[label]) if values_by_group[label] else 0.0
        for label, *_ in pair_groups
    ]
    colors = [color for *_groups, color in pair_groups]
    ax.bar(x, means, width=0.50, color=colors, edgecolor="#222222", linewidth=0.7, zorder=1)
    rng = np.random.default_rng(2)
    for idx, (label, *_rest) in enumerate(pair_groups):
        values = np.asarray(values_by_group[label])
        jitter = rng.uniform(-0.13, 0.13, size=len(values))
        ax.scatter(
            np.full(len(values), idx) + jitter,
            values,
            s=7,
            color="#222222",
            alpha=0.42,
            linewidth=0,
            zorder=2,
        )
        ax.text(
            idx,
            min(means[idx] + 0.04, 0.95),
            f"{means[idx]:.2f}",
            ha="center",
            va="bottom",
            fontsize=5.9,
            color="#222222",
        )
    ax.set_xticks(x)
    ax.set_xticklabels(
        [f"{label}\n(n={len(values_by_group[label])})" for label, *_ in pair_groups],
        fontsize=6.1,
    )
    ax.set_ylabel("Marker Jaccard", fontsize=6.6)
    ax.set_xlim(-0.45, len(pair_groups) - 0.55)
    ax.set_ylim(0, 1.0)
    ax.tick_params(axis="y", labelsize=5.8, length=2, width=0.5)
    ax.tick_params(axis="x", length=0, pad=2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.5)
    ax.spines["bottom"].set_linewidth(0.5)


def draw_c2_marker_programs(ax, profiles_df: pd.DataFrame) -> None:
    c2_df = profiles_df.loc[profiles_df["component"].eq(2)].copy()
    c2_df["label_group"] = c2_df.apply(label_group, axis=1)
    c2_df["display_label"] = c2_df["cell_type"].map(display_label)
    c2_df["marker_program"] = c2_df.apply(marker_program, axis=1)
    c2_df["sort_key"] = c2_df.apply(marker_program_sort_key, axis=1)
    c2_df = c2_df.sort_values("sort_key").copy()
    gene_counts = {}
    for value in c2_df["marker_names"]:
        for gene in str(value).split(";"):
            gene_counts[gene] = gene_counts.get(gene, 0) + 1
    program_order = {gene: idx for idx, gene in enumerate(MARKER_PROGRAM_GENES)}
    treg_genes = sorted(
        [gene for gene in gene_counts if gene in TREG_PROGRAM_GENES],
        key=lambda gene: (program_order.get(gene, len(program_order)), gene),
    )
    exhaustion_genes = sorted(
        [gene for gene in gene_counts if gene in EXHAUSTION_PROGRAM_GENES],
        key=lambda gene: (program_order.get(gene, len(program_order)), gene),
    )
    remaining_genes = sorted(
        [
            gene
            for gene in gene_counts
            if gene not in TREG_PROGRAM_GENES and gene not in EXHAUSTION_PROGRAM_GENES
        ],
        key=lambda gene: (-gene_counts[gene], gene),
    )
    genes = treg_genes + exhaustion_genes + remaining_genes
    gene_group_boxes = [
        ("Treg markers", treg_genes, LABEL_GROUP_COLORS["Treg/regulatory"], "#e7f3e2"),
        ("Exhaustion markers", exhaustion_genes, LABEL_GROUP_COLORS["Exhausted"], "#ece8f5"),
    ]
    matrix = []
    row_labels = []
    row_groups = []
    row_programs = []
    for row in c2_df.itertuples():
        marker_names = set(str(row.marker_names).split(";"))
        row = []
        for gene in genes:
            row.append(1 if gene in marker_names else 0)
        matrix.append(row)
    for row in c2_df.itertuples():
        row_labels.append(row.display_label)
        row_groups.append(row.label_group)
        row_programs.append(row.marker_program)

    matrix = np.asarray(matrix)
    image = np.ones((matrix.shape[0], matrix.shape[1], 3))
    image[:, :, :] = to_rgb("#f0f0f0")
    x_start = 0
    for _label, group_genes, _edgecolor, facecolor in gene_group_boxes:
        if group_genes:
            image[:, x_start : x_start + len(group_genes), :] = to_rgb(facecolor)
            x_start += len(group_genes)
    image[matrix == 1] = to_rgb("#000000")

    ax.set_title("C2 marker profiles by reported label", loc="left", fontsize=9.2, fontweight="bold", pad=6)
    ax.imshow(image, aspect="auto")
    ax.set_xticks(range(len(genes)))
    ax.set_xticklabels(genes, rotation=90, fontsize=6.2)
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=5.9)
    for tick, group in zip(ax.get_yticklabels(), row_groups):
        tick.set_color(LABEL_GROUP_COLORS[group])
    x_start = 0
    for label, group_genes, edgecolor, facecolor in gene_group_boxes:
        if not group_genes:
            continue
        x_start += len(group_genes)
    box_specs = [
        (
            [
                idx
                for idx, (group, program) in enumerate(zip(row_groups, row_programs))
                if (
                    group == "Both"
                    or (group == "Other" and program in {"Treg-like", "Exhausted-like"})
                )
            ],
            "#c9342f",
            1.8,
        ),
    ]
    for rows, edgecolor, linewidth in box_specs:
        if not rows:
            continue
        start = rows[0]
        previous = rows[0]
        for row_idx in rows[1:] + [None]:
            if row_idx is not None and row_idx == previous + 1:
                previous = row_idx
                continue
            ax.add_patch(
                Rectangle(
                    (-0.5, start - 0.5),
                    len(genes),
                    previous - start + 1,
                    fill=False,
                    edgecolor=edgecolor,
                    linewidth=linewidth,
                    zorder=5,
                    clip_on=False,
                )
            )
            if row_idx is not None:
                start = row_idx
                previous = row_idx
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xlabel("Marker gene", fontsize=7.0, labelpad=3)
    ax.set_ylabel("")


def draw_legends(fig) -> None:
    edge_handles = [
        Line2D([0], [0], color="#222222", linewidth=0.9, label="Exact label"),
    ]
    gene_group_handles = [
        Patch(facecolor="#e7f3e2", edgecolor="none", label="Treg markers"),
        Patch(facecolor="#ece8f5", edgecolor="none", label="Exhaustion markers"),
        Patch(facecolor="#f0f0f0", edgecolor="none", label="Other C2 markers"),
        Patch(facecolor="white", edgecolor="#c9342f", linewidth=1.2, label="Ambiguous label"),
    ]
    fig.legend(
        handles=edge_handles,
        loc="lower center",
        bbox_to_anchor=(0.30, 0.018),
        ncol=1,
        frameon=False,
        fontsize=5.8,
        handlelength=1.6,
        columnspacing=0.9,
    )
    fig.legend(
        handles=gene_group_handles,
        loc="lower center",
        bbox_to_anchor=(0.73, 0.018),
        ncol=4,
        frameon=False,
        fontsize=5.8,
        handlelength=1.0,
        handletextpad=0.35,
        columnspacing=0.75,
    )


def match_axis_width(source_ax, target_ax) -> None:
    source_pos = source_ax.get_position()
    target_pos = target_ax.get_position()
    target_ax.set_position([source_pos.x0, target_pos.y0, source_pos.width, target_pos.height])


def main() -> None:
    profiles_df = load_profiles()
    summary_df = load_summary()
    label_graph, marker_graph = build_graphs(profiles_df)
    positions = component_layout(profiles_df, marker_graph)
    positions = {
        node: (x - GRAPH_X_SHIFT, y)
        for node, (x, y) in positions.items()
    }

    fig = plt.figure(figsize=(11.8, 6.4))
    grid = fig.add_gridspec(
        1,
        2,
        width_ratios=[0.72, 1.0],
        wspace=0.12,
        left=0.04,
        right=0.985,
        top=0.92,
        bottom=0.145,
    )
    graph_grid = grid[0, 0].subgridspec(
        2,
        1,
        height_ratios=[0.57, 0.43],
        hspace=0.18,
    )
    ax_label = fig.add_subplot(graph_grid[0, 0])
    ax_c2_graph = fig.add_subplot(graph_grid[1, 0])
    ax_c2_programs = fig.add_subplot(grid[0, 1])

    draw_graph(
        ax_label,
        label_graph,
        positions,
        "Celltype-label graph",
    )
    draw_c2_subgraph(ax_c2_graph, profiles_df)
    draw_c2_marker_programs(ax_c2_programs, profiles_df)
    fig.canvas.draw()
    match_axis_width(ax_label, ax_c2_graph)
    draw_legends(fig)

    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    fig.savefig(FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PNG_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
