from __future__ import annotations

import math
from collections.abc import Callable
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch, Rectangle

from build_local_global_marker_analysis import build_profiles, jaccard
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

FIGURE_PATH = FIGURE_DIR / "fig3_local_global_marker_identifiability.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig3_local_global_marker_identifiability.png"
PANEL_A_PATH = FIGURE_DIR / "fig3_panel_a_joint_distribution.pdf"
PANEL_A_PNG_PATH = FIGURE_DIR / "fig3_panel_a_joint_distribution.png"
PANEL_B_PATH = FIGURE_DIR / "fig3_panel_b_nomenclature_examples.pdf"
PANEL_B_PNG_PATH = FIGURE_DIR / "fig3_panel_b_nomenclature_examples.png"
PANEL_C_PATH = FIGURE_DIR / "fig3_panel_c_local_global_recovery.pdf"
PANEL_C_PNG_PATH = FIGURE_DIR / "fig3_panel_c_local_global_recovery.png"
REPORT_PATH = RESULTS_DIR / "fig3_local_global_marker_identifiability_report.md"
PAIR_VALUES_PATH = RESULTS_DIR / "fig3_local_global_pair_values_sample.tsv"
PAIR_SUMMARY_PATH = RESULTS_DIR / "fig3_local_global_pair_summary.tsv"
LABEL_LOCAL_GLOBAL_PATH = RESULTS_DIR / "fig3_label_local_global_marker_recovery.tsv"
LABEL_DISAGREEMENT_SAME_PATH = RESULTS_DIR / "fig3_same_label_weak_marker_examples.tsv"
LABEL_DISAGREEMENT_DIFFERENT_PATH = RESULTS_DIR / "fig3_different_label_shared_marker_examples.tsv"

LOCAL_GLOBAL_PAPER_PATH = RESULTS_DIR / "local_global_paper_marker_summary.tsv"
LOCAL_GLOBAL_LIFTOVER_PATH = RESULTS_DIR / "local_global_profile_marker_liftover.tsv"
LOCAL_GLOBAL_LABEL_PATH = RESULTS_DIR / "local_global_label_coherence_summary.tsv"
LOCAL_GLOBAL_TRANSFER_LABEL_PATH = RESULTS_DIR / "local_global_marker_transfer_lift_by_label.tsv"
LOCAL_GLOBAL_TRANSFER_SUMMARY_PATH = RESULTS_DIR / "local_global_marker_transfer_lift_summary.tsv"
JOINT_DISTRIBUTION_PATH = RESULTS_DIR / "cross_study_label_marker_joint_distribution.tsv"
IDENTIFIABILITY_SUMMARY_PATH = RESULTS_DIR / "marker_identifiability_partition_summary.tsv"
IDENTIFIABILITY_SELECTED_PATH = RESULTS_DIR / "marker_identifiability_selected_genes.tsv"

ROLE_ORDER = ["essential_in_minimum_panels", "exchangeable_in_minimum_panels"]
ROLE_LABELS = {
    "essential_in_minimum_panels": "Required in every\nminimum panel",
    "exchangeable_in_minimum_panels": "One of several\nvalid choices",
}
ROLE_COLORS = {
    "essential_in_minimum_panels": "#2f6f4e",
    "exchangeable_in_minimum_panels": "#b8b8b8",
}

PARTITION_LABELS = {
    "reported_exact_labels_min5": "Exact labels\n(67 signatures)",
    "tcell_marker_clusters": "T-cell\nclusters",
    "myeloid_marker_clusters": "Myeloid\nclusters",
}

LABELS_TO_ANNOTATE = [
    "T CELL",
    "MACROPHAGE",
    "MONOCYTE",
    "CD 4 T CELL",
    "CD 8 T CELL",
    "TREG",
    "MYELOID CELL",
    "FIBROBLAST",
    "MELANOCYTE",
    "OLIGODENDROCYTES",
]


def require_tables() -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    required = [
        LOCAL_GLOBAL_PAPER_PATH,
        LOCAL_GLOBAL_LIFTOVER_PATH,
        LOCAL_GLOBAL_LABEL_PATH,
        LOCAL_GLOBAL_TRANSFER_LABEL_PATH,
        LOCAL_GLOBAL_TRANSFER_SUMMARY_PATH,
        JOINT_DISTRIBUTION_PATH,
        IDENTIFIABILITY_SUMMARY_PATH,
        IDENTIFIABILITY_SELECTED_PATH,
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing prerequisite outputs. Run build_local_global_marker_analysis.py and "
            f"build_marker_identifiability_analysis.py first. Missing: {', '.join(missing)}"
        )
    return (
        pd.read_csv(LOCAL_GLOBAL_PAPER_PATH, sep="\t"),
        pd.read_csv(LOCAL_GLOBAL_LIFTOVER_PATH, sep="\t"),
        pd.read_csv(LOCAL_GLOBAL_LABEL_PATH, sep="\t"),
        pd.read_csv(LOCAL_GLOBAL_TRANSFER_LABEL_PATH, sep="\t"),
        pd.read_csv(LOCAL_GLOBAL_TRANSFER_SUMMARY_PATH, sep="\t"),
        pd.read_csv(JOINT_DISTRIBUTION_PATH, sep="\t", keep_default_na=False),
        pd.read_csv(IDENTIFIABILITY_SUMMARY_PATH, sep="\t"),
        pd.read_csv(IDENTIFIABILITY_SELECTED_PATH, sep="\t"),
    )


def build_local_global_pair_values() -> dict[str, np.ndarray]:
    profiles_df, _id_to_name = build_profiles()
    values: dict[str, list[float]] = {
        "Local: different names in same paper": [],
        "Global: same name in different papers": [],
        "Global: different names in different papers": [],
    }
    all_rows = list(profiles_df.itertuples(index=False))

    for (_source_corpus, _paper_id), paper_df in profiles_df.groupby(["source_corpus", "paper_id"], sort=True):
        paper_rows = list(paper_df.itertuples(index=False))
        for row_a, row_b in combinations(paper_rows, 2):
            if row_a.normalized_cell_type == row_b.normalized_cell_type:
                continue
            shared, union, value = jaccard(row_a.marker_set, row_b.marker_set)
            values["Local: different names in same paper"].append(value)

    for row_a, row_b in combinations(all_rows, 2):
        if row_a.paper_uid == row_b.paper_uid:
            continue
        same_name = row_a.normalized_cell_type != "" and row_a.normalized_cell_type == row_b.normalized_cell_type
        different_name = (
            row_a.normalized_cell_type != ""
            and row_b.normalized_cell_type != ""
            and row_a.normalized_cell_type != row_b.normalized_cell_type
        )
        if not same_name and not different_name:
            continue
        comparison = (
            "Global: same name in different papers"
            if same_name
            else "Global: different names in different papers"
        )
        _shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
        values[comparison].append(value)

    values_by_comparison = {label: np.asarray(items, dtype=float) for label, items in values.items()}

    rng = np.random.default_rng(7)
    sample_rows = []
    summary_rows = []
    for label, arr in values_by_comparison.items():
        sample_n = min(5000, len(arr))
        sample = rng.choice(arr, size=sample_n, replace=False) if len(arr) else np.asarray([])
        sample_rows.extend({"comparison": label, "jaccard": value} for value in sample)
        summary_rows.append(
            {
                "comparison": label,
                "n_pairs": len(arr),
                "mean_jaccard": float(arr.mean()) if len(arr) else np.nan,
                "median_jaccard": float(np.median(arr)) if len(arr) else np.nan,
                "q25_jaccard": float(np.quantile(arr, 0.25)) if len(arr) else np.nan,
                "q75_jaccard": float(np.quantile(arr, 0.75)) if len(arr) else np.nan,
                "pct_share_at_least_one_gene": float((arr > 0).mean()) if len(arr) else np.nan,
                "pct_identical_marker_sets": float((arr == 1).mean()) if len(arr) else np.nan,
            }
        )
    pd.DataFrame(sample_rows).to_csv(PAIR_VALUES_PATH, sep="\t", index=False)
    pd.DataFrame(summary_rows).to_csv(PAIR_SUMMARY_PATH, sep="\t", index=False)
    return values_by_comparison


def draw_matrix(
    ax: plt.Axes,
    x0: float,
    y0: float,
    row_labels: list[str],
    col_labels: list[str],
    values: list[list[int]],
    title: str,
    highlight_rows: set[int] | None = None,
) -> None:
    highlight_rows = highlight_rows or set()
    row_h = 0.072
    row_label_w = 0.065
    cell_w = 0.064
    ax.text(x0, y0 + row_h * (len(row_labels) + 0.55), title, ha="left", va="bottom", fontsize=6.5, fontweight="bold")
    for col_idx, col_label in enumerate(col_labels):
        ax.text(
            x0 + row_label_w + col_idx * cell_w + cell_w / 2,
            y0 + row_h * len(row_labels),
            col_label,
            ha="center",
            va="bottom",
            fontsize=5.2,
        )
    for row_idx, row_label in enumerate(row_labels):
        y = y0 + row_h * (len(row_labels) - row_idx - 1)
        ax.text(x0, y + row_h / 2, row_label, ha="left", va="center", fontsize=5.9)
        if row_idx in highlight_rows:
            ax.add_patch(
                Rectangle(
                    (x0 + row_label_w, y),
                    cell_w * len(col_labels),
                    row_h,
                    facecolor="#f1e4df",
                    edgecolor="#8d3328",
                    linewidth=0.7,
                    zorder=-2,
                )
            )
        for col_idx, value in enumerate(values[row_idx]):
            x = x0 + row_label_w + col_idx * cell_w
            ax.add_patch(
                Rectangle(
                    (x, y),
                    cell_w,
                    row_h,
                    facecolor="#3f3f3f" if value else "white",
                    edgecolor="black",
                    linewidth=0.45,
                )
            )
            ax.text(
                x + cell_w / 2,
                y + row_h / 2,
                str(value),
                ha="center",
                va="center",
                fontsize=5.7,
                color="white" if value else "black",
            )


def plot_theorem_schematic(ax: plt.Axes) -> None:
    ax.set_axis_off()
    ax.text(0.0, 1.02, "Local does not imply global", ha="left", va="bottom", fontsize=8.2, fontweight="bold", transform=ax.transAxes)
    ax.text(
        0.0,
        0.94,
        "1 = reported marker gene.",
        ha="left",
        va="top",
        fontsize=5.9,
        transform=ax.transAxes,
    )
    draw_matrix(ax, 0.02, 0.60, ["A", "B"], ["g1", "g2", "g3"], [[1, 0, 0], [0, 1, 0]], "Paper 1")
    draw_matrix(ax, 0.02, 0.34, ["C", "D"], ["g1", "g2", "g3"], [[0, 0, 1], [0, 1, 0]], "Paper 2")
    ax.text(0.43, 0.69, "locally\nseparated", ha="center", va="center", fontsize=6.0)
    ax.annotate("", xy=(0.53, 0.62), xytext=(0.35, 0.65), arrowprops={"arrowstyle": "->", "lw": 0.8})
    ax.annotate("", xy=(0.53, 0.48), xytext=(0.35, 0.44), arrowprops={"arrowstyle": "->", "lw": 0.8})
    draw_matrix(
        ax,
        0.52,
        0.42,
        ["A", "B", "C", "D"],
        ["g1", "g2", "g3"],
        [[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 0]],
        "Pooled atlas",
        highlight_rows={1, 3},
    )


def format_percent(value: float) -> str:
    if value < 0.01:
        return f"{value:.4f}%"
    if value < 1:
        return f"{value:.2f}%"
    return f"{value:.1f}%"


def add_panel_title(ax: plt.Axes, title: str) -> None:
    ax.text(
        0.5,
        1.04,
        title,
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=7.4,
        fontweight="bold",
        clip_on=False,
    )


def plot_joint_distribution(ax: plt.Axes, joint_df: pd.DataFrame) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    add_panel_title(ax, "Label-Marker Agreement")

    label_order = ["Exact", "Partial", "Different"]
    marker_order = ["Exact", "Partial", "None"]
    marker_labels = ["Exact\n$J=1$", "Partial\n$0<J<1$", "None\n$J=0$"]
    colors = {
        "same_profile": "#d9ead3",
        "same_label_diff_markers": "#e6f0f8",
        "alias": "#f4e5ef",
        "neutral": "#ffffff",
        "different_profile": "#e7e7e7",
        "context": "#d62728",
    }
    table = {
        (row.label_relation, row.marker_relation): row
        for row in joint_df.itertuples(index=False)
    }

    x0 = 0.24
    y0 = 0.25
    table_w = 0.66
    table_h = 0.54
    cell_w = table_w / 3
    cell_h = table_h / 3

    ax.text(
        x0 + table_w / 2,
        y0 + table_h + 0.095,
        "Marker Identifiability$^*$",
        ha="center",
        va="bottom",
        fontsize=6.4,
        fontstyle="italic",
    )
    ax.text(
        x0 - 0.16,
        y0 + table_h / 2,
        "Reported Labels",
        rotation=90,
        ha="center",
        va="center",
        fontsize=6.4,
        fontstyle="italic",
    )

    for col_idx, col_label in enumerate(marker_labels):
        ax.text(
            x0 + col_idx * cell_w + cell_w / 2,
            y0 + table_h + 0.018,
            col_label,
            ha="center",
            va="bottom",
            fontsize=5.5,
            linespacing=0.9,
        )

    for row_idx, label_relation in enumerate(label_order):
        y = y0 + table_h - (row_idx + 1) * cell_h
        ax.text(
            x0 - 0.035,
            y + cell_h / 2,
            label_relation,
            ha="right",
            va="center",
            fontsize=5.7,
        )
        for col_idx, marker_relation in enumerate(marker_order):
            x = x0 + col_idx * cell_w
            key = (label_relation, marker_relation)
            row = table[key]
            if key == ("Exact", "Exact"):
                facecolor = colors["same_profile"]
            elif key in {("Exact", "Partial"), ("Exact", "None")}:
                facecolor = colors["same_label_diff_markers"]
            elif key in {("Partial", "Exact"), ("Different", "Exact")}:
                facecolor = colors["alias"]
            elif key == ("Different", "None"):
                facecolor = colors["different_profile"]
            else:
                facecolor = colors["neutral"]
            ax.add_patch(
                Rectangle(
                    (x, y),
                    cell_w,
                    cell_h,
                    facecolor=facecolor,
                    edgecolor="black",
                    linewidth=0.55,
                )
            )
            ax.text(
                x + cell_w / 2,
                y + cell_h * 0.58,
                f"{int(row.pairs):,}",
                ha="center",
                va="center",
                fontsize=5.8,
                fontweight="bold",
            )
            ax.text(
                x + cell_w / 2,
                y + cell_h * 0.34,
                format_percent(float(row.percent)),
                ha="center",
                va="center",
                fontsize=5.0,
            )

    # Match the Figure 1 table: context-dependent cells are outlined, not filled.
    red_segments = [
        ((x0 + cell_w, y0 + 2 * cell_h), (x0 + 3 * cell_w, y0 + 2 * cell_h)),
        ((x0 + 3 * cell_w, y0 + 2 * cell_h), (x0 + 3 * cell_w, y0 + cell_h)),
        ((x0 + 3 * cell_w, y0 + cell_h), (x0 + 2 * cell_w, y0 + cell_h)),
        ((x0 + 2 * cell_w, y0 + cell_h), (x0 + 2 * cell_w, y0)),
        ((x0 + 2 * cell_w, y0), (x0 + cell_w, y0)),
        ((x0 + cell_w, y0), (x0 + cell_w, y0 + 2 * cell_h)),
    ]
    for (x_start, y_start), (x_end, y_end) in red_segments:
        ax.plot(
            [x_start, x_end],
            [y_start, y_end],
            color=colors["context"],
            linewidth=1.0,
            solid_capstyle="butt",
            zorder=5,
        )

    ax.text(
        x0 + table_w / 2,
        y0 - 0.04,
        r"$^*J=|G_1\cap G_2|/|G_1\cup G_2|$",
        ha="center",
        va="top",
        fontsize=5.0,
        style="italic",
    )

    legend_items = [
        (colors["same_profile"], "same profile", "black"),
        (colors["same_label_diff_markers"], "same label, different markers", "#0072B2"),
        (colors["alias"], "alias / naming variation", "#B83280"),
        ("#ffffff", "context clarifies identifiability", colors["context"]),
        (colors["different_profile"], "different profile", "black"),
    ]
    legend_x = x0 + 0.02
    legend_y = 0.145
    legend_dy = 0.031
    for idx, (fill, label, edge) in enumerate(legend_items):
        lx = legend_x
        ly = legend_y - idx * legend_dy
        ax.add_patch(
            Rectangle(
                (lx, ly - 0.014),
                0.022,
                0.022,
                facecolor=fill,
                edgecolor=edge if label == "context clarifies identifiability" else "black",
                linewidth=0.55 if label == "context clarifies identifiability" else 0.25,
            )
        )
        ax.text(
            lx + 0.032,
            ly - 0.003,
            label,
            ha="left",
            va="center",
            fontsize=4.2,
            color=edge if edge != "black" else "black",
        )


def plot_local_global_similarity(ax: plt.Axes, values_by_comparison: dict[str, np.ndarray]) -> None:
    order = [
        "Local: different names in same paper",
        "Global: same name in different papers",
        "Global: different names in different papers",
    ]
    data = [values_by_comparison[label] for label in order]
    positions = np.arange(len(order))
    box = ax.boxplot(
        data,
        positions=positions,
        widths=0.55,
        patch_artist=True,
        showfliers=False,
        whis=(5, 95),
        medianprops={"color": "black", "linewidth": 1.0},
        boxprops={"facecolor": "#d9d9d9", "edgecolor": "black", "linewidth": 0.8},
        whiskerprops={"color": "black", "linewidth": 0.8},
        capprops={"color": "black", "linewidth": 0.8},
    )
    rng = np.random.default_rng(7)
    for idx, values in enumerate(data):
        sample_n = min(450, len(values))
        sample = rng.choice(values, size=sample_n, replace=False)
        x = rng.normal(positions[idx], 0.055, size=sample_n)
        ax.scatter(x, sample, s=5, facecolor="#4d4d4d", edgecolor="none", alpha=0.35, zorder=2)
        mean = float(np.mean(values))
        separated = float((values < 1).mean())
        shared = float((values > 0).mean())
        ax.scatter([positions[idx]], [mean], s=34, facecolor="white", edgecolor="black", linewidth=0.9, zorder=4)
        ax.text(positions[idx], mean + 0.055, f"{mean:.3f}", ha="center", va="bottom", fontsize=5.8)
    ax.set_xticks(positions)
    ax.set_xticklabels(["Local\ndiff. names\nsame paper", "Global\nsame name\ndiff. papers", "Global\ndiff. names\ndiff. papers"], fontsize=6.2)
    ax.set_xlim(-0.55, 2.55)
    ax.set_ylim(0, 1.02)
    ax.set_title("Local and global marker sharing", fontsize=7.4, fontweight="bold")
    ax.set_ylabel("Marker gene set Jaccard")
    ax.set_box_aspect(1)


def build_label_local_global_recovery(liftover_df: pd.DataFrame) -> pd.DataFrame:
    df = liftover_df.loc[
        liftover_df["normalized_cell_type"].ne("")
        & liftover_df["n_same_label_other_paper_profiles"].gt(0)
    ].dropna(
        subset=[
            "local_private_fraction",
            "local_private_fraction_recovered_by_same_label_other_papers",
            "marker_fraction_recovered_by_same_label_other_papers",
        ]
    )
    summary = (
        df.groupby("normalized_cell_type", sort=True)
        .agg(
            n_profiles=("cell_type", "size"),
            n_papers=("paper_key", "nunique"),
            mean_local_marker_specificity=("local_private_fraction", "mean"),
            median_local_marker_specificity=("local_private_fraction", "median"),
            mean_global_recovery_of_local_markers=(
                "local_private_fraction_recovered_by_same_label_other_papers",
                "mean",
            ),
            median_global_recovery_of_local_markers=(
                "local_private_fraction_recovered_by_same_label_other_papers",
                "median",
            ),
            mean_global_recovery_of_all_markers=(
                "marker_fraction_recovered_by_same_label_other_papers",
                "mean",
            ),
            median_global_recovery_of_all_markers=(
                "marker_fraction_recovered_by_same_label_other_papers",
                "median",
            ),
        )
        .reset_index()
    )
    summary = summary.loc[summary["n_profiles"].ge(5)].copy()
    summary["local_to_global_gap"] = (
        summary["mean_local_marker_specificity"]
        - summary["mean_global_recovery_of_local_markers"]
    )
    summary.to_csv(LABEL_LOCAL_GLOBAL_PATH, sep="\t", index=False)
    return summary


def plot_label_local_global_recovery(ax: plt.Axes, label_recovery_df: pd.DataFrame) -> None:
    df = label_recovery_df.copy()
    add_panel_title(ax, "Globally Identifiable Markers")
    immune_terms = {
        "T CELL",
        "TREG",
        "B CELL",
        "B CELLS",
        "CD 4 T CELL",
        "CD 8 T CELL",
        "MACROPHAGE",
        "MONOCYTE",
        "DENDRITIC CELL",
        "NK CELL",
        "MAST CELL",
        "PLASMA CELL",
        "CDC 1",
        "CDC 2",
    }
    df["is_immune"] = df["normalized_cell_type"].isin(immune_terms)
    df["point_size"] = 12 + 2.0 * np.sqrt(df["n_profiles"])

    ax.axhspan(0.5, 1.0, 0.5, 1.0, color="#edf6ec", zorder=0)
    ax.axhspan(0.0, 0.5, 0.5, 1.0, color="#f6ece8", zorder=0)
    ax.axvspan(0.0, 0.5, color="#f3f3f3", zorder=-1)
    ax.axhline(0.5, color="#9a9a9a", linewidth=0.65, linestyle="--", zorder=1)
    ax.axvline(0.5, color="#9a9a9a", linewidth=0.65, linestyle="--", zorder=1)

    other = df.loc[~df["is_immune"]]
    immune = df.loc[df["is_immune"]]
    ax.scatter(
        other["mean_local_marker_specificity"],
        other["mean_global_recovery_of_local_markers"],
        s=other["point_size"],
        facecolor="#cfcfcf",
        edgecolor="black",
        linewidth=0.35,
        alpha=0.85,
        zorder=2,
        label="Other labels",
    )
    ax.scatter(
        immune["mean_local_marker_specificity"],
        immune["mean_global_recovery_of_local_markers"],
        s=immune["point_size"],
        facecolor="#f2b45c",
        edgecolor="black",
        linewidth=0.45,
        alpha=0.95,
        zorder=3,
        label="Immune labels",
    )

    label_positions = {
        "T CELL": (0.56, 0.88),
        "TREG": (0.52, 0.77),
        "B CELL": (0.53, 0.69),
        "MACROPHAGE": (0.53, 0.61),
        "MONOCYTE": (0.52, 0.43),
        "DENDRITIC CELL": (0.36, 0.08),
        "CLUSTER 1": (0.34, 0.18),
        "CD 4 T CELL": (0.26, 0.55),
        "CD 8 T CELL": (0.29, 0.47),
    }
    for label, (text_x, text_y) in label_positions.items():
        rows = df.loc[df["normalized_cell_type"].eq(label)]
        if rows.empty:
            continue
        row = rows.iloc[0]
        display = label.title().replace("Cd ", "CD ").replace("Treg", "Treg")
        ax.annotate(
            display,
            xy=(
                row["mean_local_marker_specificity"],
                row["mean_global_recovery_of_local_markers"],
            ),
            xytext=(text_x, text_y),
            fontsize=5.7,
            arrowprops={"arrowstyle": "-", "lw": 0.42, "color": "black"},
            ha="left",
            va="center",
            zorder=4,
        )

    ax.set(
        xlim=(0, 1.02),
        ylim=(0, 1.02),
        xlabel="Local marker specificity",
        ylabel="Global recovery of local markers",
    )
    ax.legend(frameon=False, fontsize=5.4, loc="lower left", handletextpad=0.2)
    ax.set_box_aspect(1)


def plot_marker_transfer_lift(ax: plt.Axes, transfer_label_df: pd.DataFrame) -> None:
    df = transfer_label_df.loc[
        transfer_label_df["marker_scope"].eq("all_reported_markers")
        & transfer_label_df["n_profiles"].ge(5)
    ].copy()
    df = df.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["median_observed_union_recall", "median_expected_union_recall", "median_union_recall_lift"]
    )
    df["log2_lift"] = np.log2(df["median_union_recall_lift"].clip(lower=1e-3))
    df["point_size"] = 9 + 1.4 * np.sqrt(df["n_profiles"])
    high_transfer = df["median_union_recall_lift"] > 1

    x_grid = np.linspace(0, 1, 200)
    ax.fill_between(
        x_grid,
        x_grid,
        1,
        facecolor="#edf6ec",
        edgecolor="none",
        alpha=0.65,
        zorder=0,
    )
    ax.fill_between(
        x_grid,
        0,
        x_grid,
        facecolor="#f1f1f1",
        edgecolor="none",
        alpha=0.70,
        zorder=0,
    )

    ax.scatter(
        df.loc[~high_transfer, "median_expected_union_recall"],
        df.loc[~high_transfer, "median_observed_union_recall"],
        s=df.loc[~high_transfer, "point_size"],
        facecolor="#c9c9c9",
        edgecolor="black",
        linewidth=0.3,
        alpha=0.9,
        zorder=2,
    )
    sc = ax.scatter(
        df.loc[high_transfer, "median_expected_union_recall"],
        df.loc[high_transfer, "median_observed_union_recall"],
        s=df.loc[high_transfer, "point_size"],
        c=df.loc[high_transfer, "log2_lift"].clip(0, 6),
        cmap="YlGn",
        edgecolor="black",
        linewidth=0.35,
        alpha=0.95,
        zorder=3,
    )
    ax.plot([0, 1], [0, 1], color="#777777", linewidth=0.8, linestyle="--", zorder=1)

    label_positions = {
        "T CELL": (0.43, 0.88),
        "TREG": (0.43, 0.80),
        "B CELL": (0.43, 0.73),
        "MACROPHAGE": (0.43, 0.66),
        "MONOCYTE": (0.43, 0.31),
        "DENDRITIC CELL": (0.23, 0.065),
        "CLUSTER 1": (0.23, 0.12),
    }
    labels_to_annotate = [
        "T CELL",
        "TREG",
        "B CELL",
        "MACROPHAGE",
        "MONOCYTE",
        "DENDRITIC CELL",
        "CLUSTER 1",
    ]
    for label in labels_to_annotate:
        rows = df.loc[df["normalized_cell_type"].eq(label)]
        if rows.empty:
            continue
        row = rows.iloc[0]
        text_x, text_y = label_positions[label]
        display = label.title().replace("Cd ", "CD ").replace("Treg", "Treg")
        ax.annotate(
            display,
            xy=(row["median_expected_union_recall"], row["median_observed_union_recall"]),
            xytext=(text_x, text_y),
            fontsize=6.2,
            arrowprops={"arrowstyle": "-", "lw": 0.45, "color": "black"},
            va="center",
        )

    ax.set_title("Same-label marker transfer", fontsize=7.4, fontweight="bold")
    ax.text(
        0.66,
        0.91,
        "Above background\ntransfer",
        ha="center",
        va="center",
        fontsize=6.2,
        color="#2f6f4e",
    )
    ax.text(
        0.76,
        0.18,
        "Below background",
        ha="center",
        va="center",
        fontsize=6.2,
        color="#555555",
    )
    ax.annotate(
        "Low expected,\nhigh observed",
        xy=(0.06, 0.66),
        xytext=(0.64, 0.74),
        ha="left",
        va="center",
        fontsize=6.2,
        color="#2f6f4e",
        arrowprops={"arrowstyle": "-", "lw": 0.45, "color": "#2f6f4e"},
    )
    ax.annotate(
        "Low expected,\nlow observed",
        xy=(0.05, 0.055),
        xytext=(0.52, 0.07),
        ha="left",
        va="center",
        fontsize=6.2,
        color="#555555",
        arrowprops={"arrowstyle": "-", "lw": 0.45, "color": "#555555"},
    )
    ax.set(
        xlim=(-0.02, 1.02),
        ylim=(-0.02, 1.02),
        xlabel="Expected marker transfer",
        ylabel="Observed marker transfer",
    )
    ax.set_box_aspect(1)


def is_interpretable_label(label: str) -> bool:
    if not label or label in {"CELL", "CELLS"}:
        return False
    bad_prefixes = (
        "CLUSTER",
        "C ",
        "CT ",
        "NC ",
        "FB ",
        "MAC ",
        "MDC ",
        "STRO ",
    )
    if label.startswith(bad_prefixes):
        return False
    if "MARKER" in label:
        return False
    return True


def compact_label(label: str) -> str:
    replacements = {
        "REGULATORY T CELL": "Treg",
        "ENDOTHELIAL CELL": "Endothelial",
        "ENDOTHELIAL CELLS": "Endothelial cells",
        "EPITHELIAL": "Epi.",
        "EPITHELIAL CELL": "Epithelial",
        "OLIGODENDROCYTES": "Oligo. cells",
        "OLIGODENDROCYTE": "Oligo.",
        "ERYTHROCYTE": "RBC",
        "ERYTHROID CELL": "Erythroid",
        "VASCULAR SMOOTH MUSCLE CELL": "VSMC",
        "SMOOTH MUSCLE MYOFIBROBLAST": "SM/myofibro.",
        "NAIVE T CELL": "Naive T",
        "NAIVE T CELLS": "Naive T cells",
        "NAIVE MEMORY": "Naive/memory",
        "CD 4 T CELL": "CD4 T",
        "CD 8 T CELL": "CD8 T",
        "CD 8 GZMK": "CD8 GZMK",
        "TAM MRC 1": "TAM MRC1",
    }
    if label in replacements:
        return replacements[label]
    text = label.title()
    for old, new in {
        "Treg": "Treg",
        "T Cell": "T cell",
        "B Cell": "B cell",
        "Nk Cell": "NK cell",
        "Mait": "MAIT",
        "Tcm": "TCM",
        "Rbc": "RBC",
        "Ecm": "ECM",
        "Ipsc": "iPSC",
    }.items():
        text = text.replace(old, new)
    return text


def build_label_disagreement_examples(
    label_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    same = label_df.loc[
        label_df["n_profiles"].ge(8)
        & label_df["n_papers"].ge(8)
        & label_df["normalized_cell_type"].map(is_interpretable_label)
    ].copy()
    same["score"] = same["pct_jaccard_eq_0"] * np.log1p(same["n_profiles"])
    same = same.sort_values(["score", "n_profiles"], ascending=[False, False]).head(6)
    same = same[
        [
            "normalized_cell_type",
            "n_profiles",
            "n_papers",
            "n_pairs",
            "pct_jaccard_eq_0",
            "mean_jaccard",
            "median_jaccard",
        ]
    ].copy()
    same.to_csv(LABEL_DISAGREEMENT_SAME_PATH, sep="\t", index=False)

    profiles_df, id_to_name = build_profiles()
    rows = list(profiles_df.itertuples(index=False))
    gene_to_indices: dict[str, list[int]] = defaultdict(list)
    for idx, row in enumerate(rows):
        if not row.normalized_cell_type or not is_interpretable_label(row.normalized_cell_type):
            continue
        for gene_id in row.marker_set:
            gene_to_indices[gene_id].append(idx)

    candidate_pairs: set[tuple[int, int]] = set()
    for indices in gene_to_indices.values():
        if len(indices) < 2:
            continue
        for left, right in combinations(indices, 2):
            if left > right:
                left, right = right, left
            candidate_pairs.add((left, right))

    pair_records: dict[tuple[str, str], dict[str, object]] = {}
    for left, right in candidate_pairs:
        row_a = rows[left]
        row_b = rows[right]
        if row_a.paper_uid == row_b.paper_uid:
            continue
        if row_a.normalized_cell_type == row_b.normalized_cell_type:
            continue
        label_pair = tuple(sorted([row_a.normalized_cell_type, row_b.normalized_cell_type]))
        shared, union, value = jaccard(row_a.marker_set, row_b.marker_set)
        if shared < 3:
            continue
        existing = pair_records.get(label_pair)
        if existing is None or (value, shared) > (existing["max_jaccard"], existing["max_shared_genes"]):
            shared_genes = "; ".join(
                id_to_name.get(gene_id, gene_id)
                for gene_id in sorted(row_a.marker_set & row_b.marker_set)[:8]
            )
            pair_records[label_pair] = {
                "label_a": label_pair[0],
                "label_b": label_pair[1],
                "max_jaccard": float(value),
                "max_shared_genes": int(shared),
                "max_union_genes": int(union),
                "n_pairs_with_shared_marker": 0,
                "example_label_a": row_a.cell_type,
                "example_label_b": row_b.cell_type,
                "shared_genes": shared_genes,
            }
        pair_records[label_pair]["n_pairs_with_shared_marker"] += 1

    different = pd.DataFrame(pair_records.values())
    if not different.empty:
        different = different.loc[different["n_pairs_with_shared_marker"].ge(2)].copy()
        different = different.sort_values(
            ["max_jaccard", "max_shared_genes", "n_pairs_with_shared_marker"],
            ascending=[False, False, False],
        ).head(6)
    different.to_csv(LABEL_DISAGREEMENT_DIFFERENT_PATH, sep="\t", index=False)
    return same, different


def plot_labeling_disagreement_examples(
    ax: plt.Axes,
    same_df: pd.DataFrame,
    different_df: pd.DataFrame,
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    add_panel_title(ax, "Inconsistent Pairwise Labels")
    ax.text(
        0.02,
        0.91,
        "Same label pairs with $J=0$",
        ha="left",
        va="center",
        fontsize=6.0,
        fontweight="bold",
    )
    bar_left = 0.34
    bar_width = 0.46
    y_start = 0.84
    row_h = 0.055
    same_plot = same_df.sort_values("pct_jaccard_eq_0", ascending=True)
    for idx, row in enumerate(same_plot.itertuples(index=False)):
        y = y_start - idx * row_h
        value = float(row.pct_jaccard_eq_0)
        zero_pairs = int(round(value * int(row.n_pairs)))
        ax.text(0.02, y, compact_label(row.normalized_cell_type), ha="left", va="center", fontsize=5.7)
        ax.add_patch(
            Rectangle(
                (bar_left, y - 0.014),
                bar_width,
                0.028,
                facecolor="#efefef",
                edgecolor="none",
            )
        )
        ax.add_patch(
            Rectangle(
                (bar_left, y - 0.014),
                bar_width * value,
                0.028,
                facecolor="#8a8a8a",
                edgecolor="black",
                linewidth=0.25,
            )
        )
        ax.text(
            bar_left + bar_width + 0.025,
            y,
            f"{100 * value:.0f}% ({zero_pairs}/{int(row.n_pairs)})",
            ha="left",
            va="center",
            fontsize=5.0,
        )
    ax.text(bar_left, 0.49, "0", ha="center", va="top", fontsize=4.8)
    ax.text(bar_left + bar_width, 0.49, "100%", ha="center", va="top", fontsize=4.8)
    ax.text(
        bar_left + bar_width / 2,
        0.45,
        "% cross-paper profile pairs",
        ha="center",
        va="top",
        fontsize=4.9,
    )

    ax.text(
        0.02,
        0.37,
        "Different labels, high marker overlap",
        ha="left",
        va="center",
        fontsize=6.3,
        fontweight="bold",
    )
    table_x = 0.02
    table_y = 0.305
    col_x = [table_x, 0.52, 0.72, 0.92]
    ax.text(col_x[0], table_y, "Reported labels", ha="left", va="bottom", fontsize=5.1, fontweight="bold")
    ax.text(col_x[1], table_y, "J", ha="center", va="bottom", fontsize=5.1, fontweight="bold")
    ax.text(col_x[2], table_y, "Shared/union", ha="center", va="bottom", fontsize=4.9, fontweight="bold")
    ax.text(col_x[3], table_y, "Pairs", ha="center", va="bottom", fontsize=4.9, fontweight="bold")
    ax.plot([0.02, 0.98], [table_y - 0.01, table_y - 0.01], color="black", linewidth=0.45)

    y_start = 0.265
    row_h = 0.049
    diff_plot = different_df.sort_values(
        ["max_jaccard", "max_shared_genes", "n_pairs_with_shared_marker"],
        ascending=[False, False, False],
    )
    for idx, row in enumerate(diff_plot.itertuples(index=False)):
        y = y_start - idx * row_h
        label = f"{compact_label(row.label_a)} / {compact_label(row.label_b)}"
        if idx % 2 == 0:
            ax.add_patch(
                Rectangle(
                    (0.02, y - row_h * 0.38),
                    0.96,
                    row_h * 0.72,
                    facecolor="#f5f5f5",
                    edgecolor="none",
                    zorder=-1,
                )
            )
        ax.text(col_x[0], y, label, ha="left", va="center", fontsize=4.8)
        ax.text(col_x[1], y, f"{float(row.max_jaccard):.2f}", ha="center", va="center", fontsize=4.8)
        ax.text(
            col_x[2],
            y,
            f"{int(row.max_shared_genes)}/{int(row.max_union_genes)}",
            ha="center",
            va="center",
            fontsize=4.8,
        )
        ax.text(
            col_x[3],
            y,
            f"{int(row.n_pairs_with_shared_marker)}",
            ha="center",
            va="center",
            fontsize=4.8,
        )


def plot_marker_roles(ax: plt.Axes, summary_df: pd.DataFrame, selected_df: pd.DataFrame) -> None:
    partitions = list(PARTITION_LABELS)
    selected = selected_df.loc[
        selected_df["method"].eq("ilp_minimum")
        & selected_df["coverage_threshold"].eq(0.2)
        & selected_df["partition"].isin(partitions)
    ].copy()
    bottoms = np.zeros(len(partitions), dtype=float)
    x = np.arange(len(partitions))
    for role in ROLE_ORDER:
        counts = [
            int(((selected["partition"] == partition) & (selected["role"] == role)).sum())
            for partition in partitions
        ]
        ax.bar(
            x,
            counts,
            bottom=bottoms,
            color=ROLE_COLORS[role],
            edgecolor="black",
            linewidth=0.6,
            width=0.7,
            label=ROLE_LABELS[role],
        )
        bottoms += np.asarray(counts)
    lower_bounds = []
    for partition in partitions:
        row = summary_df.loc[
            summary_df["partition"].eq(partition) & summary_df["coverage_threshold"].eq(0.2)
        ].iloc[0]
        lower_bounds.append(int(row["information_lower_bound_log2"]))
    ax.scatter(x, lower_bounds, s=28, facecolor="white", edgecolor="black", linewidth=0.8, zorder=4, label="Binary lower bound")
    for idx, total in enumerate(bottoms):
        ax.text(idx, total + 1.0, f"{int(total)}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x)
    ax.set_xticklabels([PARTITION_LABELS[p] for p in partitions])
    ax.set_ylabel("Marker genes needed\nto separate groups")
    ax.set_ylim(0, max(bottoms) * 1.22)
    ax.legend(frameon=False, fontsize=6.5, loc="upper right")


def make_summary(
    paper_df: pd.DataFrame,
    liftover_df: pd.DataFrame,
    label_df: pd.DataFrame,
    transfer_summary_df: pd.DataFrame,
    joint_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    selected_df: pd.DataFrame,
) -> pd.DataFrame:
    liftover_values = liftover_df.loc[
        liftover_df["n_same_label_other_paper_profiles"].gt(0),
        "marker_fraction_recovered_by_same_label_other_papers",
    ].dropna()
    exact_row = summary_df.loc[
        summary_df["partition"].eq("reported_exact_labels_min5") & summary_df["coverage_threshold"].eq(0.2)
    ].iloc[0]
    same_label_transfer = transfer_summary_df.loc[
        transfer_summary_df["relation"].eq("same_exact_label")
        & transfer_summary_df["marker_scope"].eq("all_reported_markers")
    ].iloc[0]
    selected_exact = selected_df.loc[
        selected_df["method"].eq("ilp_minimum")
        & selected_df["coverage_threshold"].eq(0.2)
        & selected_df["partition"].eq("reported_exact_labels_min5")
    ]
    joint_lookup = {
        (row.label_relation, row.marker_relation): row
        for row in joint_df.itertuples(index=False)
    }
    exact_total = sum(int(joint_lookup[("Exact", marker)].pairs) for marker in ["Exact", "Partial", "None"])
    exact_nonidentical = exact_total - int(joint_lookup[("Exact", "Exact")].pairs)
    different_shared = int(joint_lookup[("Different", "Exact")].pairs) + int(joint_lookup[("Different", "Partial")].pairs)
    rows = [
        {
            "claim": "Same reported label with non-identical marker sets",
            "value": f"{exact_nonidentical:,}/{exact_total:,} pairs ({100 * exact_nonidentical / exact_total:.1f}%)",
        },
        {
            "claim": "Different reported labels sharing marker genes",
            "value": f"{different_shared:,} cross-study pairs",
        },
        {
            "claim": "Papers usually contain locally distinguishable reported-marker profiles",
            "value": f"{100 * paper_df['all_profiles_locally_identifiable'].mean():.1f}%",
        },
        {
            "claim": "Median local problem size",
            "value": f"{paper_df['n_profiles'].median():.0f} profiles, {paper_df['greedy_local_panel_size'].median():.0f} genes",
        },
        {
            "claim": "Median same-label marker liftover across papers",
            "value": f"{liftover_values.median():.3f}",
        },
        {
            "claim": "Same-label marker transfer above background",
            "value": f"{same_label_transfer.median_union_recall_lift:.2f}x lift",
        },
        {
            "claim": "Exact labels at 20% marker coverage",
            "value": f"{int(exact_row.n_groups)} labels collapse to {int(exact_row.n_distinct_signatures)} signatures",
        },
        {
            "claim": "Exact-label selected separating panel",
            "value": f"{len(selected_exact)} genes ({(selected_exact['role'] == 'essential_in_minimum_panels').sum()} essential, {(selected_exact['role'] == 'exchangeable_in_minimum_panels').sum()} exchangeable)",
        },
        {
            "claim": "Most recurrent exact labels have median cross-paper marker Jaccard",
            "value": f"{label_df.loc[label_df['n_profiles'].ge(5), 'median_jaccard'].median():.3f}",
        },
    ]
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    text_df = df.fillna("").astype(str)
    header = "| " + " | ".join(text_df.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(text_df.columns)) + " |"
    rows = ["| " + " | ".join(row) + " |" for row in text_df.itertuples(index=False, name=None)]
    return "\n".join([header, separator, *rows])


def write_report(
    summary: pd.DataFrame,
    label_df: pd.DataFrame,
    transfer_label_df: pd.DataFrame,
    selected_df: pd.DataFrame,
) -> None:
    labels = label_df.loc[label_df["normalized_cell_type"].isin(LABELS_TO_ANNOTATE)].copy()
    labels["fraction_pairs_with_shared_marker_gene"] = 1 - labels["pct_jaccard_eq_0"]
    labels = labels[
        [
            "normalized_cell_type",
            "n_profiles",
            "n_papers",
            "mean_jaccard",
            "median_jaccard",
            "fraction_pairs_with_shared_marker_gene",
        ]
    ]
    for col in ["mean_jaccard", "median_jaccard", "fraction_pairs_with_shared_marker_gene"]:
        labels[col] = labels[col].map(lambda value: f"{float(value):.3f}")

    transfer_labels = transfer_label_df.loc[
        transfer_label_df["marker_scope"].eq("all_reported_markers")
        & transfer_label_df["normalized_cell_type"].isin(
            [
                "T CELL",
                "B CELL",
                "MACROPHAGE",
                "MONOCYTE",
                "CD 4 T CELL",
                "CD 8 T CELL",
                "TREG",
                "PLASMA CELL",
                "MAST CELL",
                "DENDRITIC CELL",
                "CLUSTER 1",
            ]
        )
    ][
        [
            "normalized_cell_type",
            "n_profiles",
            "n_papers",
            "median_observed_union_recall",
            "median_expected_union_recall",
            "median_union_recall_lift",
        ]
    ].copy()
    for col in ["median_observed_union_recall", "median_expected_union_recall", "median_union_recall_lift"]:
        transfer_labels[col] = transfer_labels[col].map(lambda value: f"{float(value):.3f}")

    selected = selected_df.loc[
        selected_df["method"].eq("ilp_minimum")
        & selected_df["coverage_threshold"].eq(0.2)
        & selected_df["partition"].isin(PARTITION_LABELS)
    ][["partition", "gene_name", "role", "on_groups", "mean_on_group_coverage"]].copy()
    selected["mean_on_group_coverage"] = selected["mean_on_group_coverage"].map(lambda value: f"{float(value):.3f}")

    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Figure 3 Local-Global Marker Identifiability",
                "",
                "This prototype is the manuscript-facing version of the Lean-derived marker identifiability analysis.",
                "The formal claim is that local separation within papers does not imply global atlas-scale separation.",
                "",
                f"Figure: `{FIGURE_PATH.relative_to(REPO_ROOT)}`",
                "",
                "## Summary",
                "",
                markdown_table(summary),
                "",
                "## Annotated Recurrent Labels",
                "",
                markdown_table(labels),
                "",
                "## Annotated Marker Transfer Labels",
                "",
                markdown_table(transfer_labels),
                "",
                "## Selected Separating Genes",
                "",
                markdown_table(selected),
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def save_panel(
    pdf_path: Path,
    png_path: Path,
    draw: Callable[[plt.Axes], None],
    figsize: tuple[float, float] = (3.35, 3.25),
) -> None:
    fig, ax = plt.subplots(figsize=figsize)
    draw(ax)
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close(fig)


def main() -> None:
    (
        paper_df,
        liftover_df,
        label_df,
        transfer_label_df,
        transfer_summary_df,
        joint_df,
        ident_summary_df,
        selected_df,
    ) = require_tables()
    label_recovery_df = build_label_local_global_recovery(liftover_df)
    same_label_examples_df, different_label_examples_df = build_label_disagreement_examples(label_df)
    summary = make_summary(paper_df, liftover_df, label_df, transfer_summary_df, joint_df, ident_summary_df, selected_df)

    plt.rcParams.update(
        {
            "font.size": 7.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
        }
    )

    save_panel(
        PANEL_A_PATH,
        PANEL_A_PNG_PATH,
        lambda ax: plot_joint_distribution(ax, joint_df),
    )
    save_panel(
        PANEL_B_PATH,
        PANEL_B_PNG_PATH,
        lambda ax: plot_labeling_disagreement_examples(ax, same_label_examples_df, different_label_examples_df),
    )
    save_panel(
        PANEL_C_PATH,
        PANEL_C_PNG_PATH,
        lambda ax: plot_label_local_global_recovery(ax, label_recovery_df),
    )

    fig = plt.figure(figsize=(10.6, 3.65))
    gs = fig.add_gridspec(
        1,
        3,
        width_ratios=[1.0, 1.0, 1.0],
        wspace=0.55,
    )
    axes = [
        fig.add_subplot(gs[0, 0]),
        fig.add_subplot(gs[0, 1]),
        fig.add_subplot(gs[0, 2]),
    ]
    plot_joint_distribution(axes[0], joint_df)
    plot_labeling_disagreement_examples(axes[1], same_label_examples_df, different_label_examples_df)
    plot_label_local_global_recovery(axes[2], label_recovery_df)

    for letter, ax in zip("ABC", axes, strict=True):
        ax.text(-0.14, 1.07, letter, transform=ax.transAxes, fontsize=12, fontweight="bold", ha="left", va="bottom")

    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    fig.savefig(FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)
    write_report(summary, label_df, transfer_label_df, selected_df)

    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PNG_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PANEL_A_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PANEL_B_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PANEL_C_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
