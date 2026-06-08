from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch, Rectangle

from build_marker_identifiability_analysis import add_marker_cluster_partitions, load_profiles
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

FIGURE_PATH = FIGURE_DIR / "fig4_biological_vignettes.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig4_biological_vignettes.png"
REPORT_PATH = RESULTS_DIR / "fig4_biological_vignettes_report.md"

TCELL_SUMMARY_PATH = RESULTS_DIR / "tcell_marker_cluster_summary.tsv"
MYELOID_SUMMARY_PATH = RESULTS_DIR / "myeloid_marker_cluster_summary.tsv"
SELECTED_GENES_PATH = RESULTS_DIR / "marker_identifiability_selected_genes.tsv"

PARTITIONS = {
    "tcell_marker_clusters": {
        "label": "T-cell marker clusters",
        "cluster_col": "tcell_marker_cluster",
        "summary_path": TCELL_SUMMARY_PATH,
        "title": "T-cell marker programs",
    },
    "myeloid_marker_clusters": {
        "label": "Myeloid marker clusters",
        "cluster_col": "myeloid_marker_cluster",
        "summary_path": MYELOID_SUMMARY_PATH,
        "title": "Myeloid marker programs",
    },
}

ROLE_LABELS = {
    "essential_in_minimum_panels": "Essential",
    "exchangeable_in_minimum_panels": "Exchangeable",
}
ROLE_COLORS = {
    "essential_in_minimum_panels": "#2f6f4e",
    "exchangeable_in_minimum_panels": "#b8b8b8",
}


def first_items(value: object, n: int) -> str:
    items = [item.strip() for item in str(value or "").split(";") if item.strip()]
    return "; ".join(items[:n])


def first_items_with_remainder(value: object, n: int) -> str:
    items = [item.strip() for item in str(value or "").split(";") if item.strip()]
    if len(items) <= n:
        return "; ".join(items)
    return "; ".join(items[:n]) + f"; +{len(items) - n} more"


def wrap(value: object, width: int) -> str:
    return "\n".join(textwrap.wrap(str(value), width=width, break_long_words=False))


def shorten(value: object, max_chars: int) -> str:
    text = str(value)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def compact_label_summary(top_labels: object, n_labels: int) -> str:
    first = first_items(top_labels, 1)
    first = shorten(first, 27)
    if n_labels <= 1:
        return first
    return f"{first}; +{n_labels - 1} labels"


def cluster_label(component: object) -> str:
    return f"C{int(component)}"


def load_cluster_summary(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t")
    df["cluster"] = df["component"].map(cluster_label)
    df["display_markers"] = df["core_marker_genes"].map(lambda value: first_items_with_remainder(value, 3))
    df["display_labels"] = df.apply(lambda row: compact_label_summary(row["top_labels"], int(row["labels"])), axis=1)
    return df


def selected_genes(partition: str) -> pd.DataFrame:
    df = pd.read_csv(SELECTED_GENES_PATH, sep="\t")
    selected = df.loc[
        df["partition"].eq(partition)
        & df["coverage_threshold"].eq(0.2)
        & df["method"].eq("ilp_minimum")
    ].copy()
    selected["role_label"] = selected["role"].map(ROLE_LABELS).fillna(selected["role"])
    return selected.sort_values(["role", "rank"]).reset_index(drop=True)


def coverage_matrix(
    profiles_df: pd.DataFrame,
    partition: str,
    selected_df: pd.DataFrame,
    summary_df: pd.DataFrame,
) -> pd.DataFrame:
    cluster_col = PARTITIONS[partition]["cluster_col"]
    clusters = summary_df["cluster"].tolist()
    rows = []
    for gene in selected_df.itertuples(index=False):
        row = {"gene_name": gene.gene_name, "gene_id": gene.gene_id, "role": gene.role}
        for cluster in clusters:
            group_df = profiles_df.loc[profiles_df[cluster_col].eq(cluster)]
            if group_df.empty:
                row[cluster] = np.nan
            else:
                row[cluster] = float(group_df["marker_set"].map(lambda marker_set: gene.gene_id in marker_set).mean())
        rows.append(row)
    return pd.DataFrame(rows)


def draw_cluster_table(ax: plt.Axes, summary_df: pd.DataFrame, title: str) -> None:
    ax.set_axis_off()
    ax.text(0.0, 1.03, title, ha="left", va="bottom", fontsize=10, fontweight="bold", transform=ax.transAxes)

    headers = ["Cluster", "Program", "Core markers", "Unique labels", "n"]
    x_positions = [0.00, 0.12, 0.39, 0.72, 0.96]
    y_top = 0.94
    row_h = 0.105 if len(summary_df) > 5 else 0.145

    for x, header in zip(x_positions, headers, strict=True):
        ha = "right" if header == "n" else "left"
        ax.text(x, y_top, header, ha=ha, va="center", fontsize=7.3, fontweight="bold", transform=ax.transAxes)
    ax.plot([0, 1], [y_top - 0.025, y_top - 0.025], color="black", linewidth=0.8, transform=ax.transAxes)

    for idx, row in enumerate(summary_df.itertuples(index=False)):
        y = y_top - 0.055 - idx * row_h
        if idx % 2 == 0:
            ax.add_patch(
                Rectangle(
                    (0, y - row_h + 0.01),
                    1,
                    row_h - 0.01,
                    facecolor="#f4f4f4",
                    edgecolor="none",
                    transform=ax.transAxes,
                    zorder=-1,
                )
            )
        ax.text(x_positions[0], y, row.cluster, ha="left", va="top", fontsize=7.2, fontweight="bold", transform=ax.transAxes)
        ax.text(x_positions[1], y, wrap(row.dominant_program, 17), ha="left", va="top", fontsize=6.8, transform=ax.transAxes)
        ax.text(x_positions[2], y, wrap(row.display_markers, 24), ha="left", va="top", fontsize=6.6, transform=ax.transAxes)
        ax.text(x_positions[3], y, str(int(row.labels)), ha="left", va="top", fontsize=6.8, transform=ax.transAxes)
        ax.text(x_positions[4], y, str(int(row.profiles)), ha="right", va="top", fontsize=6.8, transform=ax.transAxes)


def draw_coverage_heatmap(
    ax: plt.Axes,
    matrix_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    title: str,
) -> None:
    clusters = summary_df["cluster"].tolist()
    data = matrix_df[clusters].to_numpy(dtype=float)
    cmap = LinearSegmentedColormap.from_list("marker_coverage", ["#f7f7f7", "#595959"])
    im = ax.imshow(data, vmin=0, vmax=1, cmap=cmap, aspect="auto")

    ax.set_xticks(np.arange(len(clusters)))
    ax.set_xticklabels(clusters, fontsize=7)
    gene_labels = []
    for row in matrix_df.itertuples(index=False):
        prefix = "*" if row.role == "essential_in_minimum_panels" else ""
        gene_labels.append(f"{prefix}{row.gene_name}")
    ax.set_yticks(np.arange(len(matrix_df)))
    ax.set_yticklabels(gene_labels, fontsize=7)
    ax.set_xlabel("Marker cluster", fontsize=8)
    ax.set_title(title, fontsize=9.2, fontweight="bold", loc="left", pad=8)

    for y_idx, row in enumerate(data):
        for x_idx, value in enumerate(row):
            if np.isnan(value):
                continue
            text_color = "white" if value >= 0.55 else "black"
            ax.text(x_idx, y_idx, f"{value:.2f}", ha="center", va="center", fontsize=6.2, color=text_color)

    for y_idx, role in enumerate(matrix_df["role"]):
        color = ROLE_COLORS.get(role, "#ffffff")
        ax.add_patch(
            Rectangle(
                (-0.58, y_idx - 0.5),
                0.08,
                1.0,
                facecolor=color,
                edgecolor="black",
                linewidth=0.4,
                clip_on=False,
            )
        )

    ax.set_xticks(np.arange(-0.5, len(clusters), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(matrix_df), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.2)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return im


def write_report(
    tcell_summary: pd.DataFrame,
    myeloid_summary: pd.DataFrame,
    tcell_selected: pd.DataFrame,
    myeloid_selected: pd.DataFrame,
) -> None:
    def markdown_table(df: pd.DataFrame) -> str:
        string_df = df.fillna("").astype(str)
        header = "| " + " | ".join(string_df.columns) + " |"
        separator = "| " + " | ".join(["---"] * len(string_df.columns)) + " |"
        rows = ["| " + " | ".join(row) + " |" for row in string_df.itertuples(index=False, name=None)]
        return "\n".join([header, separator, *rows])

    tcell_display = tcell_summary[["cluster", "profiles", "papers", "labels", "dominant_program", "core_marker_genes", "top_labels"]]
    myeloid_display = myeloid_summary[["cluster", "profiles", "papers", "labels", "dominant_program", "core_marker_genes", "top_labels"]]
    selected_display = pd.concat(
        [
            tcell_selected.assign(example="T cell"),
            myeloid_selected.assign(example="Myeloid"),
        ],
        ignore_index=True,
    )[["example", "gene_name", "role_label", "on_groups", "mean_on_group_coverage"]]
    selected_display["mean_on_group_coverage"] = selected_display["mean_on_group_coverage"].map(lambda v: f"{float(v):.3f}")

    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Figure 4 Biological Vignettes Prototype",
                "",
                "This figure uses marker-derived T-cell and myeloid clusters as biological examples for the formal essential/exchangeable marker result.",
                f"Figure: `{FIGURE_PATH.relative_to(REPO_ROOT)}`",
                "",
                "## T-cell Marker Clusters",
                "",
                markdown_table(tcell_display),
                "",
                "## Myeloid Marker Clusters",
                "",
                markdown_table(myeloid_display),
                "",
                "## ILP-Selected Separating Genes",
                "",
                markdown_table(selected_display),
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    profiles_df, _id_to_name = load_profiles()
    profiles_df = add_marker_cluster_partitions(profiles_df)

    tcell_summary = load_cluster_summary(TCELL_SUMMARY_PATH)
    myeloid_summary = load_cluster_summary(MYELOID_SUMMARY_PATH)
    tcell_selected = selected_genes("tcell_marker_clusters")
    myeloid_selected = selected_genes("myeloid_marker_clusters")
    tcell_matrix = coverage_matrix(profiles_df, "tcell_marker_clusters", tcell_selected, tcell_summary)
    myeloid_matrix = coverage_matrix(profiles_df, "myeloid_marker_clusters", myeloid_selected, myeloid_summary)

    plt.rcParams.update(
        {
            "font.size": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
        }
    )
    fig = plt.figure(figsize=(10.6, 6.45))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.9, 1.0], height_ratios=[1.12, 0.88], wspace=0.18, hspace=0.42)

    axes = [
        fig.add_subplot(gs[0, 0]),
        fig.add_subplot(gs[0, 1]),
        fig.add_subplot(gs[1, 0]),
        fig.add_subplot(gs[1, 1]),
    ]
    draw_cluster_table(axes[0], tcell_summary, "Marker-derived T-cell groups")
    draw_coverage_heatmap(axes[1], tcell_matrix, tcell_summary, "T-cell separating genes")
    draw_cluster_table(axes[2], myeloid_summary, "Marker-derived myeloid groups")
    draw_coverage_heatmap(axes[3], myeloid_matrix, myeloid_summary, "Myeloid separating genes")

    for label, ax in zip(["A", "B", "C", "D"], axes, strict=True):
        ax.text(-0.06, 1.08, label, transform=ax.transAxes, fontsize=12, fontweight="bold", ha="left", va="bottom")

    legend_handles = [
        Patch(facecolor=ROLE_COLORS["essential_in_minimum_panels"], edgecolor="black", label="Essential in minimum panels"),
        Patch(facecolor=ROLE_COLORS["exchangeable_in_minimum_panels"], edgecolor="black", label="Exchangeable in minimum panels"),
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=2,
        frameon=False,
        bbox_to_anchor=(0.53, -0.01),
        fontsize=8,
    )
    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    fig.savefig(FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)

    write_report(tcell_summary, myeloid_summary, tcell_selected, myeloid_selected)

    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PNG_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
