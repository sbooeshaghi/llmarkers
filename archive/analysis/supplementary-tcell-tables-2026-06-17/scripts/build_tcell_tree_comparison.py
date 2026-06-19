from __future__ import annotations

import re

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Rectangle

from cross_study_gene_space import REPO_ROOT, RESULTS_DIR


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

SUMMARY_PATH = RESULTS_DIR / "tcell_marker_cluster_summary.tsv"
MEMBERSHIP_PATH = RESULTS_DIR / "tcell_marker_cluster_membership.tsv"
FIGURE_PATH = FIGURE_DIR / "fig_tcell_tree_comparison.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig_tcell_tree_comparison.png"

RELATION_COLORS = {
    "Exact": "#a8d8cf",
    "Partial": "#f3dfb7",
    "Different": "#d9d9d9",
}

PROGRAM_COLORS = {
    "T cell": "#f1f1f1",
    "Naive/memory": "#a8d8cf",
    "Cytotoxic": "#d97b66",
    "Exhaustion": "#8e6bbe",
    "Exhaustion/Treg": "#8e6bbe",
    "Regulatory": "#dda15e",
    "Residency": "#7a9e7e",
    "Other": "#eeeeee",
}

CANONICAL_ASSIGNMENTS = {
    1: "Naive/memory",
    2: "Exhaustion/Treg",
    3: "Cytotoxic",
    4: "T cell",
    5: "T cell",
    6: "Residency",
    7: "Cytotoxic",
}


def first_items(value: str, n: int = 3) -> str:
    items = [item.strip() for item in str(value).split(";") if item.strip()]
    if len(items) <= n:
        return ", ".join(items)
    return ", ".join(items[:n]) + f", +{len(items) - n}"


def label_examples(value: str, n: int = 2, max_chars: int = 36) -> str:
    items = [item.strip() for item in str(value).split(";") if item.strip()]
    labels = []
    for item in items[:n]:
        label = re.sub(r"\s+\(\d+\)$", "", item)
        label = (
            label.replace(" T CELL", " T")
            .replace(" T CELLS", " T")
            .replace("EXHAUSTED", "EXH.")
            .replace("CYTOTOXIC", "CYTO.")
            .replace("REGULATORY", "REG.")
            .replace("MEMORY", "MEM.")
            .replace("NAIVE", "NAIVE")
        )
        labels.append(label)
    text = ", ".join(labels)
    if len(text) > max_chars:
        text = text[: max_chars - 3].rstrip(" ,") + "..."
    return text


def compact_label(value: str) -> str:
    label = re.sub(r"\s+", " ", str(value)).strip()
    return (
        label.replace(" T CELL", " T")
        .replace(" T CELLS", " T")
        .replace("EXHAUSTED", "EXH.")
        .replace("CYTOTOXIC", "CYTO.")
        .replace("REGULATORY", "REG.")
        .replace("MEMORY", "MEM.")
        .replace("NAIVE", "NAIVE")
    )


def canonical_assignment(row: pd.Series) -> str:
    return CANONICAL_ASSIGNMENTS.get(int(row["component"]), str(row["dominant_program"]))


def reused_label_examples(membership_df: pd.DataFrame) -> dict[int, str]:
    if membership_df.empty:
        return {}

    distinct_labels = membership_df.drop_duplicates(["component", "normalized_cell_type"])
    label_components = distinct_labels.groupby("normalized_cell_type")["component"].agg(lambda values: sorted(set(values)))
    reused_labels = {label for label, components in label_components.items() if len(components) > 1}

    display_by_label = {}
    for normalized_label in reused_labels:
        values = membership_df.loc[membership_df["normalized_cell_type"].eq(normalized_label), "cell_type"]
        display_by_label[normalized_label] = compact_label(values.value_counts().index[0])

    examples_by_component: dict[int, str] = {}
    for component, component_df in distinct_labels.groupby("component"):
        labels = []
        for normalized_label in component_df["normalized_cell_type"]:
            if normalized_label in reused_labels:
                labels.append(display_by_label[normalized_label])
        labels = sorted(set(labels))
        if len(labels) > 3:
            examples_by_component[int(component)] = ", ".join(labels[:3]) + f", +{len(labels) - 3}"
        elif labels:
            examples_by_component[int(component)] = ", ".join(labels)
        else:
            examples_by_component[int(component)] = "-"
    return examples_by_component


def draw_ascii_line(
    ax,
    x: float,
    y: float,
    prefix: str,
    label: str,
    color: str,
    node_width: float,
    node_height: float = 0.034,
    suffix: str = "",
) -> None:
    char_w = 0.0069
    ax.text(
        x,
        y,
        prefix,
        ha="left",
        va="center",
        fontsize=7.4,
        family="monospace",
        color="#666666",
    )
    label_x = x + char_w * len(prefix)
    ax.add_patch(
        Rectangle(
            (label_x - 0.003, y - node_height / 2),
            node_width,
            node_height,
            facecolor=color,
            edgecolor="#222222",
            linewidth=0.45,
            zorder=1,
        )
    )
    ax.text(
        label_x + node_width / 2 - 0.003,
        y,
        label,
        ha="center",
        va="center",
        fontsize=6.2,
        fontweight="bold",
        zorder=2,
    )
    if suffix:
        ax.text(
            label_x + node_width + 0.006,
            y,
            suffix,
            ha="left",
            va="center",
            fontsize=5.5,
            color="#555555",
        )


def draw_ascii_tree(ax, x: float, y_top: float, rows: list[dict[str, object]]) -> None:
    y_step = 0.048
    for row_idx, row in enumerate(rows):
        y = y_top - row_idx * y_step
        draw_ascii_line(
            ax,
            x,
            y,
            str(row["prefix"]),
            str(row["label"]),
            str(row["color"]),
            float(row["width"]),
            suffix=str(row.get("suffix", "")),
        )


def draw_expected_tree(ax) -> None:
    rows = [
        {"prefix": "", "label": "T cell", "color": PROGRAM_COLORS["T cell"], "width": 0.080},
        {"prefix": "├── ", "label": "CD4", "color": "white", "width": 0.055},
        {"prefix": "│   ├── ", "label": "Naive/memory", "color": PROGRAM_COLORS["Naive/memory"], "width": 0.125},
        {"prefix": "│   ├── ", "label": "Treg", "color": PROGRAM_COLORS["Regulatory"], "width": 0.060},
        {"prefix": "│   └── ", "label": "Resident", "color": PROGRAM_COLORS["Residency"], "width": 0.085},
        {"prefix": "└── ", "label": "CD8", "color": "white", "width": 0.055},
        {"prefix": "    ├── ", "label": "Cytotoxic", "color": PROGRAM_COLORS["Cytotoxic"], "width": 0.095},
        {"prefix": "    └── ", "label": "Exhausted", "color": PROGRAM_COLORS["Exhaustion"], "width": 0.095},
    ]
    draw_ascii_tree(ax, x=0.045, y_top=0.785, rows=rows)


def draw_observed_tree(ax, summary_df: pd.DataFrame) -> None:
    rows = [
        {"prefix": "", "label": "T cell", "color": PROGRAM_COLORS["T cell"], "width": 0.080, "suffix": "15 profiles | 4 labels"},
        {"prefix": "├── ", "label": "T cell", "color": PROGRAM_COLORS["T cell"], "width": 0.080, "suffix": "9 profiles | 4 labels"},
        {"prefix": "│   ├── ", "label": "Naive/memory", "color": PROGRAM_COLORS["Naive/memory"], "width": 0.125, "suffix": "32 profiles | 28 labels"},
        {"prefix": "│   ├── ", "label": "Exhaustion/Treg", "color": PROGRAM_COLORS["Exhaustion/Treg"], "width": 0.135, "suffix": "31 profiles | 22 labels"},
        {"prefix": "│   └── ", "label": "Cytotoxic", "color": PROGRAM_COLORS["Cytotoxic"], "width": 0.095, "suffix": "19 profiles | 18 labels"},
        {"prefix": "│       └── ", "label": "Cytotoxic", "color": PROGRAM_COLORS["Cytotoxic"], "width": 0.095, "suffix": "4 profiles | 4 labels"},
        {"prefix": "└── ", "label": "Residency", "color": PROGRAM_COLORS["Residency"], "width": 0.085, "suffix": "4 profiles | 4 labels"},
    ]
    draw_ascii_tree(ax, x=0.545, y_top=0.785, rows=rows)


def draw_relation_bar(ax, x: float, y: float, width: float, height: float, row: pd.Series) -> None:
    left = x
    for relation, fraction in [
        ("Exact", float(row["exact_label_fraction"])),
        ("Partial", float(row["partial_label_fraction"])),
        ("Different", float(row["different_label_fraction"])),
    ]:
        seg_w = width * fraction
        ax.add_patch(
            Rectangle(
                (left, y),
                seg_w,
                height,
                facecolor=RELATION_COLORS[relation],
                edgecolor="none",
                zorder=2,
            )
        )
        left += seg_w
    ax.add_patch(Rectangle((x, y), width, height, facecolor="none", edgecolor="#222222", linewidth=0.35, zorder=3))


def draw_breakdown_table(ax, summary_df: pd.DataFrame, membership_df: pd.DataFrame) -> None:
    row_by_component = {int(row.component): pd.Series(row._asdict()) for row in summary_df.itertuples(index=False)}
    reused_by_component = reused_label_examples(membership_df)
    components = [4, 5, 1, 2, 3, 6, 7]
    table_y_top = 0.275
    row_h = 0.030
    x_node = 0.025
    x_assignment = 0.080
    x_markers = 0.175
    x_labels = 0.310
    x_reused = 0.645
    x_bar = 0.835

    ax.text(x_node, table_y_top + 0.022, "Node", fontsize=6.2, fontweight="bold", ha="left", va="bottom")
    ax.text(x_assignment, table_y_top + 0.022, "Group", fontsize=6.2, fontweight="bold", ha="left", va="bottom")
    ax.text(x_markers, table_y_top + 0.022, "Core markers", fontsize=6.2, fontweight="bold", ha="left", va="bottom")
    ax.text(x_labels, table_y_top + 0.022, "Unique reported labels", fontsize=6.2, fontweight="bold", ha="left", va="bottom")
    ax.text(x_reused, table_y_top + 0.022, "Also used in other nodes", fontsize=6.2, fontweight="bold", ha="left", va="bottom")
    ax.text(x_bar, table_y_top + 0.022, "Label relation", fontsize=6.2, fontweight="bold", ha="left", va="bottom")
    ax.axhline(table_y_top + 0.018, xmin=0.02, xmax=0.98, color="#222222", linewidth=0.45)

    for row_idx, component in enumerate(components):
        row = row_by_component[component]
        y = table_y_top - row_idx * row_h
        assignment = canonical_assignment(row)
        color = PROGRAM_COLORS.get(assignment, "#eeeeee")
        ax.axhline(y - 0.016, xmin=0.02, xmax=0.98, color="#dddddd", linewidth=0.35)
        ax.text(x_node, y, f"C{component}", fontsize=5.55, fontweight="bold", ha="left", va="center")
        ax.add_patch(Rectangle((x_assignment, y - 0.007), 0.011, 0.014, facecolor=color, edgecolor="#222222", linewidth=0.35))
        ax.text(x_assignment + 0.016, y, assignment, fontsize=5.45, ha="left", va="center")
        ax.text(x_markers, y, first_items(row["core_marker_genes"], n=3), fontsize=5.35, family="monospace", ha="left", va="center")
        label_text = label_examples(row["top_labels"], n=3, max_chars=50)
        ax.text(x_labels, y, f"{int(row['labels'])} labels: {label_text}", fontsize=5.25, ha="left", va="center")
        ax.text(x_reused, y, reused_by_component.get(component, "-"), fontsize=5.15, ha="left", va="center")
        draw_relation_bar(ax, x_bar, y - 0.006, 0.078, 0.012, row)
        exact = 100 * float(row["exact_label_fraction"])
        partial = 100 * float(row["partial_label_fraction"])
        different = 100 * float(row["different_label_fraction"])
        ax.text(x_bar + 0.084, y, f"{exact:.0f}/{partial:.0f}/{different:.0f}%", fontsize=4.9, ha="left", va="center")


def draw_legend(ax) -> None:
    x0, y0 = 0.805, 0.035
    ax.text(x0, y0 + 0.022, "Label relation: exact / partial / different", fontsize=5.8, ha="left", va="bottom")
    for idx, relation in enumerate(["Exact", "Partial", "Different"]):
        x = x0 + idx * 0.075
        ax.add_patch(Rectangle((x, y0), 0.014, 0.014, facecolor=RELATION_COLORS[relation], edgecolor="#222222", linewidth=0.3))
        ax.text(x + 0.018, y0 + 0.007, relation, fontsize=5.5, ha="left", va="center")


def main() -> None:
    if not SUMMARY_PATH.exists():
        raise SystemExit(f"Missing {SUMMARY_PATH}. Run analysis/build_tcell_marker_cluster_summary.py first.")
    summary_df = pd.read_csv(SUMMARY_PATH, sep="\t")
    membership_df = pd.read_csv(MEMBERSHIP_PATH, sep="\t") if MEMBERSHIP_PATH.exists() else pd.DataFrame()

    fig, ax = plt.subplots(figsize=(11.2, 5.4))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.02, 0.965, "Expected immune marker structure", fontsize=8.8, fontweight="bold", ha="left", va="top")
    ax.text(0.51, 0.965, "Marker-derived marker groups", fontsize=8.8, fontweight="bold", ha="left", va="top")
    ax.text(
        0.02,
        0.925,
        "Known marker programs used as an interpretation guide",
        fontsize=6.2,
        color="#444444",
        ha="left",
        va="top",
    )
    ax.text(
        0.51,
        0.925,
        "Cross-paper T-cell profiles grouped by marker-gene Jaccard >= 0.5",
        fontsize=6.2,
        color="#444444",
        ha="left",
        va="top",
    )
    ax.axvline(0.485, ymin=0.34, ymax=0.93, color="#d0d0d0", linewidth=0.7)

    draw_expected_tree(ax)
    draw_observed_tree(ax, summary_df)
    draw_breakdown_table(ax, summary_df, membership_df)
    draw_legend(ax)

    fig.text(
        0.02,
        0.012,
        "Canonical colors are assigned from core marker genes. The table shows how each marker-derived node collects reported labels and exposes where label names are coherent, broad, or state-dependent.",
        ha="left",
        va="bottom",
        fontsize=5.8,
    )
    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    fig.savefig(FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)

    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PNG_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
