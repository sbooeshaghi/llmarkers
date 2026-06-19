from __future__ import annotations

import math
from collections import Counter, defaultdict
from collections.abc import Callable
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch, Rectangle

from build_cap_llmarkers_comparison import build_cap_human_profiles, marker_relation as cap_marker_relation
from build_local_global_marker_analysis import build_profiles, jaccard
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR
from marker_label_utils import label_relation, normalize_label


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

MANUSCRIPT_WRAPPER_PATH = REPO_ROOT / "docs" / "paper" / "src" / "figures" / "fig3_cross_study_unification.tex"
MANUSCRIPT_BODY_PATH = REPO_ROOT / "docs" / "paper" / "src" / "figures" / "fig3_cross_study_unification_body.tex"
PANEL_A_PATH = FIGURE_DIR / "fig3_panel_a_joint_distribution.pdf"
PANEL_A_PNG_PATH = FIGURE_DIR / "fig3_panel_a_joint_distribution.png"
PANEL_B_PATH = FIGURE_DIR / "fig3_panel_b_nomenclature_examples.pdf"
PANEL_B_PNG_PATH = FIGURE_DIR / "fig3_panel_b_nomenclature_examples.png"
PANEL_C_PATH = FIGURE_DIR / "fig3_panel_c_local_global_recovery.pdf"
PANEL_C_PNG_PATH = FIGURE_DIR / "fig3_panel_c_local_global_recovery.png"
PANEL_D_PATH = FIGURE_DIR / "fig3_panel_d_cap_joint_distribution.pdf"
PANEL_D_PNG_PATH = FIGURE_DIR / "fig3_panel_d_cap_joint_distribution.png"
PANEL_E_PATH = FIGURE_DIR / "fig3_panel_e_cap_nomenclature_examples.pdf"
PANEL_E_PNG_PATH = FIGURE_DIR / "fig3_panel_e_cap_nomenclature_examples.png"
PANEL_F_PATH = FIGURE_DIR / "fig3_panel_f_cap_local_global_recovery.pdf"
PANEL_F_PNG_PATH = FIGURE_DIR / "fig3_panel_f_cap_local_global_recovery.png"
REPORT_PATH = RESULTS_DIR / "fig3_local_global_marker_identifiability_report.md"
PAIR_VALUES_PATH = RESULTS_DIR / "fig3_local_global_pair_values_sample.tsv"
PAIR_SUMMARY_PATH = RESULTS_DIR / "fig3_local_global_pair_summary.tsv"
LABEL_LOCAL_GLOBAL_PATH = RESULTS_DIR / "fig3_label_local_global_marker_recovery.tsv"
CAP_LABEL_LOCAL_GLOBAL_PATH = RESULTS_DIR / "fig3_cap_label_local_global_marker_recovery.tsv"
CAP_ONTOLOGY_LOCAL_GLOBAL_PATH = RESULTS_DIR / "fig3_cap_ontology_local_global_marker_recovery.tsv"
CAP_JOINT_DISTRIBUTION_PATH = RESULTS_DIR / "fig3_cap_cross_project_label_marker_joint_distribution.tsv"
CAP_ONTOLOGY_JOINT_DISTRIBUTION_PATH = RESULTS_DIR / "fig3_cap_cross_project_ontology_marker_joint_distribution.tsv"
GLOBAL_RECOVERY_NULL_SUMMARY_PATH = RESULTS_DIR / "fig3_global_recovery_permutation_summary.tsv"
GLOBAL_RECOVERY_NULL_DRAWS_PATH = RESULTS_DIR / "fig3_global_recovery_permutation_draws.tsv"
GLOBAL_RECOVERY_PROFILE_VALUES_PATH = RESULTS_DIR / "fig3_global_recovery_profile_values.tsv"
SAME_LABEL_JACCARD_VALUES_PATH = RESULTS_DIR / "fig3_same_label_marker_jaccard_values.tsv"
SAME_LABEL_JACCARD_SUMMARY_PATH = RESULTS_DIR / "fig3_same_label_marker_jaccard_summary.tsv"
CAP_LABEL_DISAGREEMENT_SAME_PATH = RESULTS_DIR / "fig3_cap_same_label_weak_marker_examples.tsv"
CAP_LABEL_DISAGREEMENT_DIFFERENT_PATH = RESULTS_DIR / "fig3_cap_different_label_shared_marker_examples.tsv"
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
            "Missing prerequisite outputs. Run analysis/build_local_global_marker_analysis.py and "
            f"analysis/build_marker_identifiability_analysis.py first. Missing: {', '.join(missing)}"
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


def add_panel_title(ax: plt.Axes, title: str, subtitle: str | None = None) -> None:
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
    if subtitle:
        ax.text(
            0.5,
            1.005,
            subtitle,
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=5.7,
            color="#4d4d4d",
            clip_on=False,
        )


def plot_joint_distribution(ax: plt.Axes, joint_df: pd.DataFrame, subtitle: str | None = None) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    add_panel_title(ax, "Label-Marker Agreement", subtitle)

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
    table_w = 0.60
    table_h = 0.60
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
    legend_x = x0 + 0.015
    legend_y = 0.158
    legend_dy = 0.029
    legend_box = 0.026
    for idx, (fill, label, edge) in enumerate(legend_items):
        lx = legend_x
        ly = legend_y - idx * legend_dy
        ax.add_patch(
            Rectangle(
                (lx, ly - legend_box * 0.58),
                legend_box,
                legend_box,
                facecolor=fill,
                edgecolor=edge if label == "context clarifies identifiability" else "black",
                linewidth=0.55 if label == "context clarifies identifiability" else 0.25,
            )
        )
        ax.text(
            lx + 0.037,
            ly - 0.003,
            label,
            ha="left",
            va="center",
            fontsize=5.8,
            color=edge if edge != "black" else "black",
        )


def plot_global_recovery_permutation_test(
    ax: plt.Axes,
    summary_row: pd.Series,
    draws_df: pd.DataFrame,
    subtitle: str | None = None,
) -> None:
    add_panel_title(ax, "Global Recovery vs Random", subtitle)
    resource_draws = draws_df.loc[draws_df["resource"].eq(summary_row["resource"])].copy()
    draws = resource_draws["mean_label_recovery"].to_numpy(dtype=float)
    observed = float(summary_row["observed_mean_label_recovery"])
    null_mean = float(summary_row["null_mean_label_recovery"])
    null_q025 = float(summary_row["null_q025_label_recovery"])
    null_q975 = float(summary_row["null_q975_label_recovery"])
    p_value = float(summary_row["empirical_p_ge"])
    lift = float(summary_row["recovery_lift"])

    rng = np.random.default_rng(1)
    jitter = rng.normal(0, 0.035, size=len(draws))
    ax.scatter(draws, jitter, s=5, color="#bdbdbd", edgecolor="none", alpha=0.35, zorder=1)
    ax.hlines(0, null_q025, null_q975, color="#6f6f6f", linewidth=4.5, alpha=0.8, zorder=2)
    ax.scatter([null_mean], [0], s=28, facecolor="white", edgecolor="black", linewidth=0.8, zorder=4)
    ax.scatter([observed], [1], s=44, facecolor="#d55e00", edgecolor="black", linewidth=0.7, zorder=5)
    ax.plot([null_mean, observed], [0, 1], color="#9a9a9a", linewidth=0.6, linestyle="--", zorder=0)
    ax.text(
        observed,
        1.13,
        f"{observed:.2f}",
        ha="center",
        va="bottom",
        fontsize=5.4,
        color="#8d3328",
    )
    ax.text(
        null_mean,
        -0.16,
        f"{null_mean:.2f}",
        ha="center",
        va="top",
        fontsize=5.2,
        color="#555555",
    )
    p_text = f"p={p_value:.3f}" if p_value >= 0.001 else "p<0.001"
    ax.text(
        0.98,
        0.88,
        f"{lift:.1f}x lift\n{p_text}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.2,
        fontweight="bold",
    )
    ax.text(
        0.98,
        0.08,
        f"{int(summary_row['n_labels'])} labels\n{int(summary_row['n_profiles'])} profiles",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=5.2,
    )
    ax.set_xlabel("Mean label-level global recovery", fontsize=5.8)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Random", "Observed"], fontsize=5.8)
    ax.tick_params(axis="x", labelsize=5.3, length=2)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, max(0.62, observed * 1.22, float(np.nanmax(draws)) * 1.2))
    ax.set_ylim(-0.35, 1.35)
    ax.set_box_aspect(1)


def build_same_label_marker_jaccard_distribution(
    profiles_df: pd.DataFrame,
    resource: str,
    context_col: str,
    label_col: str = "normalized_cell_type",
    max_random_pairs: int = 100_000,
    max_plot_pairs: int = 8_000,
    seed: int = 11,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    profiles = profiles_df.loc[profiles_df[label_col].fillna("").astype(str).str.strip().ne("")].copy()
    profiles = profiles.reset_index(drop=True)
    rows = list(profiles.itertuples(index=False))

    same_label_values: list[float] = []
    labels_with_pairs: set[str] = set()
    for label, label_df in profiles.groupby(label_col, sort=True):
        if len(label_df) < 2 or label_df[context_col].nunique() < 2:
            continue
        for row_a, row_b in combinations(label_df.itertuples(index=False), 2):
            if getattr(row_a, context_col) == getattr(row_b, context_col):
                continue
            _shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
            same_label_values.append(value)
            labels_with_pairs.add(str(label))

    random_values: list[float] = []
    n_profiles = len(rows)
    attempts = 0
    max_attempts = max_random_pairs * 8
    while len(random_values) < max_random_pairs and attempts < max_attempts:
        attempts += 1
        idx_a, idx_b = rng.integers(0, n_profiles, size=2)
        if idx_a == idx_b:
            continue
        row_a = rows[int(idx_a)]
        row_b = rows[int(idx_b)]
        if getattr(row_a, context_col) == getattr(row_b, context_col):
            continue
        if getattr(row_a, label_col) == getattr(row_b, label_col):
            continue
        _shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
        random_values.append(value)

    value_rows = []
    for comparison, values in [
        ("Same label", same_label_values),
        ("Random different labels", random_values),
    ]:
        arr = np.asarray(values, dtype=float)
        if len(arr) > max_plot_pairs:
            arr = rng.choice(arr, size=max_plot_pairs, replace=False)
        value_rows.extend(
            {"resource": resource, "comparison": comparison, "marker_jaccard": float(value)}
            for value in arr
        )

    summary_rows = []
    for comparison, values in [
        ("Same label", same_label_values),
        ("Random different labels", random_values),
    ]:
        arr = np.asarray(values, dtype=float)
        summary_rows.append(
            {
                "resource": resource,
                "comparison": comparison,
                "n_pairs": len(arr),
                "n_labels_with_pairs": len(labels_with_pairs) if comparison == "Same label" else np.nan,
                "mean_jaccard": float(arr.mean()) if len(arr) else np.nan,
                "median_jaccard": float(np.median(arr)) if len(arr) else np.nan,
                "q25_jaccard": float(np.quantile(arr, 0.25)) if len(arr) else np.nan,
                "q75_jaccard": float(np.quantile(arr, 0.75)) if len(arr) else np.nan,
                "pct_jaccard_eq_0": float((arr == 0).mean()) if len(arr) else np.nan,
                "pct_jaccard_gt_0": float((arr > 0).mean()) if len(arr) else np.nan,
                "pct_jaccard_ge_0_25": float((arr >= 0.25).mean()) if len(arr) else np.nan,
                "pct_jaccard_eq_1": float((arr == 1).mean()) if len(arr) else np.nan,
            }
        )

    return pd.DataFrame(value_rows), pd.DataFrame(summary_rows)


def plot_same_label_marker_jaccard_swarm(
    ax: plt.Axes,
    values_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    resource: str,
    subtitle: str | None = None,
    title: str | None = "Same-Label Marker Sharing",
    same_tick_label: str = "Same\nlabel",
    set_square: bool = True,
) -> None:
    if title:
        add_panel_title(ax, title, subtitle)
    order = ["Random different labels", "Same label"]
    labels = ["Random\ndiff. labels", same_tick_label]
    colors = {
        "Random different labels": "#B83280",
        "Same label": "#2f6f4e",
    }
    rng = np.random.default_rng(19)
    for idx, comparison in enumerate(order):
        subset = values_df.loc[
            values_df["resource"].eq(resource) & values_df["comparison"].eq(comparison),
            "marker_jaccard",
        ].to_numpy(dtype=float)
        sample_n = min(650, len(subset))
        sample = rng.choice(subset, size=sample_n, replace=False) if len(subset) else np.asarray([])
        x = rng.normal(idx, 0.075, size=len(sample))
        ax.scatter(
            x,
            sample,
            s=6,
            facecolor=colors[comparison],
            edgecolor="none",
            alpha=0.28 if comparison.startswith("Random") else 0.42,
            rasterized=True,
        )
        summary_row = summary_df.loc[
            summary_df["resource"].eq(resource) & summary_df["comparison"].eq(comparison)
        ].iloc[0]
        mean = float(summary_row["mean_jaccard"])
        ax.scatter([idx], [mean], s=38, facecolor="white", edgecolor="black", linewidth=0.8, zorder=5)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(labels, fontsize=5.8)
    ax.set_xlim(-0.48, 1.48)
    ax.set_ylim(-0.03, 1.03)
    ax.set_ylabel("Marker gene set Jaccard", fontsize=5.8)
    ax.tick_params(axis="y", labelsize=5.4, length=2)
    ax.tick_params(axis="x", length=0)
    if set_square:
        ax.set_box_aspect(1)


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


def normalize_marker_relation_for_plot(relation: str) -> str:
    return "None" if relation in {"Different", "None"} else relation


def cap_profiles_with_ontology_terms(cap_profiles_df: pd.DataFrame) -> pd.DataFrame:
    profiles = cap_profiles_df.copy()
    ontology_terms = profiles["cap_ontology_term"].fillna("").astype(str).str.strip()
    ontology_ids = profiles["cap_ontology_term_id"].fillna("").astype(str).str.strip()
    profiles = profiles.loc[ontology_terms.ne("") & ontology_ids.str.startswith("CL:")].copy()
    profiles["cell_type"] = profiles["cap_ontology_term"]
    profiles["normalized_cell_type"] = profiles["cap_ontology_term"].map(normalize_label)
    return profiles


def build_cap_cross_project_joint_distribution(
    cap_profiles_df: pd.DataFrame,
    output_path: Path = CAP_JOINT_DISTRIBUTION_PATH,
) -> pd.DataFrame:
    rows = list(cap_profiles_df.itertuples(index=False))
    counts: dict[tuple[str, str], int] = defaultdict(int)
    total = 0
    for idx_a, idx_b in combinations(range(len(rows)), 2):
        row_a = rows[idx_a]
        row_b = rows[idx_b]
        if row_a.project_id == row_b.project_id:
            continue
        _shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
        label_rel = label_relation(row_a.normalized_cell_type, row_b.normalized_cell_type)
        marker_rel = normalize_marker_relation_for_plot(cap_marker_relation(value))
        counts[(label_rel, marker_rel)] += 1
        total += 1

    out_rows = []
    for label_rel in ["Exact", "Partial", "Different"]:
        for marker_rel in ["Exact", "Partial", "None"]:
            pairs = counts[(label_rel, marker_rel)]
            out_rows.append(
                {
                    "label_relation": label_rel,
                    "marker_relation": marker_rel,
                    "pairs": pairs,
                    "fraction": pairs / total if total else np.nan,
                    "percent": 100 * pairs / total if total else np.nan,
                }
            )
    out = pd.DataFrame(out_rows)
    out.to_csv(output_path, sep="\t", index=False)
    return out


def build_global_recovery_permutation_test(
    profiles_df: pd.DataFrame,
    resource: str,
    label_basis: str,
    local_context_col: str,
    comparison_context_col: str,
    min_profiles: int,
    n_permutations: int = 1000,
    seed: int = 17,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    profiles = profiles_df.loc[profiles_df["normalized_cell_type"].ne("")].copy().reset_index(drop=True)
    marker_sets = list(profiles["marker_set"])
    labels = list(profiles["normalized_cell_type"])
    local_contexts = list(profiles[local_context_col])
    comparison_contexts = list(profiles[comparison_context_col])

    local_gene_counts: dict[str, Counter] = {}
    label_to_indices: dict[str, list[int]] = defaultdict(list)
    for context, context_df in profiles.groupby(local_context_col, sort=False):
        local_gene_counts[context] = Counter(
            gene_id for marker_set in context_df["marker_set"] for gene_id in marker_set
        )
    for idx, label in enumerate(labels):
        label_to_indices[label].append(idx)

    eligible_labels = {
        label
        for label, indices in label_to_indices.items()
        if len(indices) >= min_profiles
        and len({comparison_contexts[idx] for idx in indices}) >= 2
    }

    profile_records = []
    for idx, row in enumerate(profiles.itertuples(index=False)):
        label = labels[idx]
        if label not in eligible_labels:
            continue
        markers = marker_sets[idx]
        local_private = {
            gene_id
            for gene_id in markers
            if local_gene_counts[local_contexts[idx]][gene_id] == 1
        }
        if not local_private:
            continue
        comparison_indices = [
            other_idx
            for other_idx in label_to_indices[label]
            if comparison_contexts[other_idx] != comparison_contexts[idx]
        ]
        if not comparison_indices:
            continue
        comparison_union: set[str] = set()
        for other_idx in comparison_indices:
            comparison_union |= marker_sets[other_idx]
        observed = len(local_private & comparison_union) / len(local_private)
        background_indices = np.asarray(
            [
                other_idx
                for other_idx in range(len(profiles))
                if comparison_contexts[other_idx] != comparison_contexts[idx]
            ],
            dtype=int,
        )
        if len(background_indices) == 0:
            continue
        profile_records.append(
            {
                "resource": resource,
                "label_basis": label_basis,
                "profile_idx": idx,
                "normalized_cell_type": label,
                "cell_type": row.cell_type,
                "context_uid": getattr(row, "context_uid", ""),
                "comparison_context": comparison_contexts[idx],
                "n_local_markers": len(local_private),
                "n_comparison_profiles": len(comparison_indices),
                "observed_global_recovery": observed,
                "local_private_set": local_private,
                "background_indices": background_indices,
            }
        )

    profile_df_internal = pd.DataFrame(profile_records)
    if profile_df_internal.empty:
        raise ValueError(f"No eligible profiles for global recovery permutation test: {resource}")

    observed_by_label = (
        profile_df_internal.groupby("normalized_cell_type")["observed_global_recovery"]
        .mean()
        .rename("label_mean_observed_global_recovery")
    )
    observed_statistic = float(observed_by_label.mean())

    rng = np.random.default_rng(seed)
    draw_rows = []
    internal_rows = list(profile_df_internal.itertuples(index=False))
    for permutation in range(n_permutations):
        label_to_values: dict[str, list[float]] = defaultdict(list)
        for record in internal_rows:
            background_indices = record.background_indices
            n_draw = min(int(record.n_comparison_profiles), len(background_indices))
            sampled = rng.choice(background_indices, size=n_draw, replace=False)
            sampled_union: set[str] = set()
            for sampled_idx in sampled:
                sampled_union |= marker_sets[int(sampled_idx)]
            value = len(record.local_private_set & sampled_union) / len(record.local_private_set)
            label_to_values[record.normalized_cell_type].append(value)
        label_means = [float(np.mean(values)) for values in label_to_values.values()]
        draw_rows.append(
            {
                "resource": resource,
                "label_basis": label_basis,
                "permutation": permutation,
                "mean_label_recovery": float(np.mean(label_means)),
                "median_label_recovery": float(np.median(label_means)),
            }
        )

    draws_df = pd.DataFrame(draw_rows)
    null_values = draws_df["mean_label_recovery"].to_numpy(dtype=float)
    p_ge = (1 + int((null_values >= observed_statistic).sum())) / (n_permutations + 1)
    summary_df = pd.DataFrame(
        [
            {
                "resource": resource,
                "label_basis": label_basis,
                "n_profiles": len(profile_df_internal),
                "n_labels": profile_df_internal["normalized_cell_type"].nunique(),
                "n_permutations": n_permutations,
                "observed_mean_label_recovery": observed_statistic,
                "observed_median_label_recovery": float(observed_by_label.median()),
                "null_mean_label_recovery": float(null_values.mean()),
                "null_median_label_recovery": float(np.median(null_values)),
                "null_q025_label_recovery": float(np.quantile(null_values, 0.025)),
                "null_q975_label_recovery": float(np.quantile(null_values, 0.975)),
                "recovery_lift": observed_statistic / float(null_values.mean()) if null_values.mean() else np.nan,
                "empirical_p_ge": p_ge,
            }
        ]
    )
    profile_df = profile_df_internal.drop(columns=["local_private_set", "background_indices"])
    return summary_df, draws_df, profile_df


def build_label_local_global_recovery_from_profiles(
    profiles_df: pd.DataFrame,
    output_path: Path,
    min_profiles: int = 3,
) -> pd.DataFrame:
    context_gene_counts: dict[str, Counter] = {}
    label_to_rows: dict[str, list[object]] = defaultdict(list)

    for context_uid, context_df in profiles_df.groupby("context_uid", sort=False):
        context_gene_counts[context_uid] = Counter(
            gene_id for marker_set in context_df["marker_set"] for gene_id in marker_set
        )
    for row in profiles_df.itertuples(index=False):
        if row.normalized_cell_type:
            label_to_rows[row.normalized_cell_type].append(row)

    profile_rows = []
    for row in profiles_df.itertuples(index=False):
        local_private = {
            gene_id
            for gene_id in row.marker_set
            if context_gene_counts[row.context_uid][gene_id] == 1
        }
        same_label_other_project_union: set[str] = set()
        same_label_other_project_profiles = 0
        for other in label_to_rows.get(row.normalized_cell_type, []):
            if other.project_id == row.project_id:
                continue
            same_label_other_project_profiles += 1
            same_label_other_project_union |= other.marker_set
        if not same_label_other_project_profiles:
            continue
        profile_rows.append(
            {
                "normalized_cell_type": row.normalized_cell_type,
                "cell_type": row.cell_type,
                "project_id": row.project_id,
                "local_private_fraction": len(local_private) / len(row.marker_set) if row.marker_set else np.nan,
                "local_private_fraction_recovered_by_same_label_other_projects": (
                    len(local_private & same_label_other_project_union) / len(local_private)
                    if local_private
                    else np.nan
                ),
                "marker_fraction_recovered_by_same_label_other_projects": (
                    len(row.marker_set & same_label_other_project_union) / len(row.marker_set)
                    if row.marker_set
                    else np.nan
                ),
            }
        )

    profile_df = pd.DataFrame(profile_rows).dropna(
        subset=[
            "local_private_fraction",
            "local_private_fraction_recovered_by_same_label_other_projects",
            "marker_fraction_recovered_by_same_label_other_projects",
        ]
    )
    if profile_df.empty:
        out = pd.DataFrame(
            columns=[
                "normalized_cell_type",
                "n_profiles",
                "n_papers",
                "mean_local_marker_specificity",
                "median_local_marker_specificity",
                "mean_global_recovery_of_local_markers",
                "median_global_recovery_of_local_markers",
                "mean_global_recovery_of_all_markers",
                "median_global_recovery_of_all_markers",
                "local_to_global_gap",
            ]
        )
        out.to_csv(output_path, sep="\t", index=False)
        return out

    summary = (
        profile_df.groupby("normalized_cell_type", sort=True)
        .agg(
            n_profiles=("cell_type", "size"),
            n_papers=("project_id", "nunique"),
            mean_local_marker_specificity=("local_private_fraction", "mean"),
            median_local_marker_specificity=("local_private_fraction", "median"),
            mean_global_recovery_of_local_markers=(
                "local_private_fraction_recovered_by_same_label_other_projects",
                "mean",
            ),
            median_global_recovery_of_local_markers=(
                "local_private_fraction_recovered_by_same_label_other_projects",
                "median",
            ),
            mean_global_recovery_of_all_markers=(
                "marker_fraction_recovered_by_same_label_other_projects",
                "mean",
            ),
            median_global_recovery_of_all_markers=(
                "marker_fraction_recovered_by_same_label_other_projects",
                "median",
            ),
        )
        .reset_index()
    )
    summary = summary.loc[summary["n_profiles"].ge(min_profiles)].copy()
    summary["local_to_global_gap"] = (
        summary["mean_local_marker_specificity"]
        - summary["mean_global_recovery_of_local_markers"]
    )
    summary.to_csv(output_path, sep="\t", index=False)
    return summary


def build_label_disagreement_examples_from_profiles(
    profiles_df: pd.DataFrame,
    same_output_path: Path,
    different_output_path: Path,
    min_same_profiles: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = list(profiles_df.itertuples(index=False))
    label_values: dict[str, list[float]] = defaultdict(list)
    label_projects: dict[str, set[str]] = defaultdict(set)
    label_profile_counts: Counter[str] = Counter()
    for row in rows:
        if row.normalized_cell_type and is_interpretable_label(row.normalized_cell_type):
            label_profile_counts[row.normalized_cell_type] += 1
            label_projects[row.normalized_cell_type].add(row.project_id)

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
    same_label_seen: set[tuple[int, int]] = set()
    for left, right in combinations(range(len(rows)), 2):
        row_a = rows[left]
        row_b = rows[right]
        if row_a.project_id == row_b.project_id:
            continue
        if row_a.normalized_cell_type != row_b.normalized_cell_type:
            continue
        if not is_interpretable_label(row_a.normalized_cell_type):
            continue
        _shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
        label_values[row_a.normalized_cell_type].append(value)
        same_label_seen.add((left, right))

    same_rows = []
    for label, values in label_values.items():
        if label_profile_counts[label] < min_same_profiles:
            continue
        arr = np.asarray(values, dtype=float)
        same_rows.append(
            {
                "normalized_cell_type": label,
                "n_profiles": label_profile_counts[label],
                "n_papers": len(label_projects[label]),
                "n_pairs": len(arr),
                "pct_jaccard_eq_0": float((arr == 0).mean()),
                "mean_jaccard": float(arr.mean()),
                "median_jaccard": float(np.median(arr)),
            }
        )
    same = pd.DataFrame(same_rows)
    if not same.empty:
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
    same.to_csv(same_output_path, sep="\t", index=False)

    for left, right in candidate_pairs:
        row_a = rows[left]
        row_b = rows[right]
        if row_a.project_id == row_b.project_id:
            continue
        if row_a.normalized_cell_type == row_b.normalized_cell_type:
            continue
        label_pair = tuple(sorted([row_a.normalized_cell_type, row_b.normalized_cell_type]))
        shared, union, value = jaccard(row_a.marker_set, row_b.marker_set)
        if shared < 3:
            continue
        existing = pair_records.get(label_pair)
        if existing is None or (value, shared) > (existing["max_jaccard"], existing["max_shared_genes"]):
            pair_records[label_pair] = {
                "label_a": label_pair[0],
                "label_b": label_pair[1],
                "max_jaccard": float(value),
                "max_shared_genes": int(shared),
                "max_union_genes": int(union),
                "n_pairs_with_shared_marker": 0,
                "example_label_a": row_a.cell_type,
                "example_label_b": row_b.cell_type,
            }
        pair_records[label_pair]["n_pairs_with_shared_marker"] += 1

    different = pd.DataFrame(pair_records.values())
    if not different.empty:
        different = different.loc[different["n_pairs_with_shared_marker"].ge(1)].copy()
        different = different.sort_values(
            ["max_jaccard", "max_shared_genes", "n_pairs_with_shared_marker"],
            ascending=[False, False, False],
        ).head(6)
    different.to_csv(different_output_path, sep="\t", index=False)
    return same, different


def plot_label_local_global_recovery(
    ax: plt.Axes,
    label_recovery_df: pd.DataFrame,
    subtitle: str | None = None,
    label_positions: dict[str, tuple[float, float]] | None = None,
) -> None:
    df = label_recovery_df.copy()
    add_panel_title(ax, "Globally Identifiable Markers", subtitle)
    immune_terms = {
        "T CELL",
        "REGULATORY T CELL",
        "TREG",
        "B CELL",
        "B CELLS",
        "CD 4 T CELL",
        "CD 8 T CELL",
        "MACROPHAGE",
        "MONOCYTE",
        "DENDRITIC CELL",
        "CONVENTIONAL DENDRITIC CELL",
        "PLASMACYTOID DENDRITIC CELL",
        "NK CELL",
        "MAST CELL",
        "PLASMA CELL",
        "NEUTROPHIL",
        "CD 4 POSITIVE ALPHA BETA REGULATORY T CELL",
        "CD 14 LOW CD 16 POSITIVE MONOCYTE",
        "CDC 1",
        "CDC 2",
        "PDC",
        "NEUTROPHILS",
        "MACROPHAGES MONOCYTES",
        "CD 4 TREG",
        "CD 14 CD 16 MONOCYTES",
        "CONVENTIONAL DENDRITIC CELLS",
    }
    df["is_immune"] = df["normalized_cell_type"].isin(immune_terms)
    df["point_size"] = 12 + 2.0 * np.sqrt(df["n_profiles"])

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

    if label_positions is None:
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
        display = compact_label(label)
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
        "BEST 4 EPITHELIAL": "BEST4 epithelial",
        "COLONOCYTES BEST 4": "BEST4 colonocytes",
        "COLONOCYTES BEST4": "BEST4 colonocytes",
        "INTERSTITIAL MPH PERIVASCULAR": "Interstitial Mph",
        "PVMAC": "PvMac",
        "B CELLS": "B cells",
        "MACROPHAGES MONOCYTES": "Mac./mono.",
        "CD 4 TREG": "CD4 Treg",
        "CD 14 CD 16 MONOCYTES": "CD14/CD16 mono.",
        "LYMPHATIC ENDOTHELIUM": "Lymph. endo.",
        "CONVENTIONAL DENDRITIC CELLS": "Conv. DCs",
        "NEUTROPHILS": "Neutrophils",
        "NEUTROPHIL": "Neutrophil",
        "ENTEROCYTES": "Enterocytes",
        "PDC": "pDC",
        "PLASMACYTOID DENDRITIC CELL": "pDC",
        "CONVENTIONAL DENDRITIC CELL": "cDC",
        "CD 4 POSITIVE ALPHA BETA REGULATORY T CELL": "CD4 Treg",
        "CD 14 LOW CD 16 POSITIVE MONOCYTE": "CD14low/CD16 mono.",
        "CDC 1": "cDC1",
        "CDC 2": "cDC2",
        "DC 2": "DC2",
        "CDC 2 B": "cDC2B",
        "TYPE 2 CDCS": "type 2 cDCs",
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
    values_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    resource: str,
    subtitle: str | None = None,
    same_tick_label: str = "Same\nlabel",
) -> None:
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    add_panel_title(ax, "Inconsistent Pairwise Labels", subtitle)
    ax.text(
        0.02,
        0.89,
        "Same-label marker sharing",
        ha="left",
        va="center",
        fontsize=6.0,
        fontweight="bold",
    )
    swarm_ax = ax.inset_axes([0.12, 0.51, 0.76, 0.32])
    plot_same_label_marker_jaccard_swarm(
        swarm_ax,
        values_df,
        summary_df,
        resource,
        title=None,
        same_tick_label=same_tick_label,
        set_square=False,
    )

    ax.text(
        0.02,
        0.40,
        "Different labels, high marker overlap",
        ha="left",
        va="center",
        fontsize=6.3,
        fontweight="bold",
    )
    table_x = 0.02
    table_y = 0.335
    col_x = [table_x, 0.58, 0.78, 0.95]
    ax.text(col_x[0], table_y, "Reported labels", ha="left", va="bottom", fontsize=5.1, fontweight="bold")
    ax.text(col_x[1], table_y, "J", ha="center", va="bottom", fontsize=5.1, fontweight="bold")
    ax.text(col_x[2], table_y, "Shared", ha="center", va="bottom", fontsize=4.9, fontweight="bold")
    ax.text(col_x[3], table_y, "Pairs", ha="center", va="bottom", fontsize=4.9, fontweight="bold")
    ax.plot([0.02, 0.98], [table_y - 0.01, table_y - 0.01], color="black", linewidth=0.45)

    y_start = 0.295
    row_h = 0.046
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
        ax.text(col_x[0], y, label, ha="left", va="center", fontsize=4.5)
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
                "This report summarizes the manuscript-facing Lean-derived marker identifiability analysis.",
                "The formal claim is that local separation within papers does not imply global atlas-scale separation.",
                "",
                f"Manuscript wrapper: `{MANUSCRIPT_WRAPPER_PATH.relative_to(REPO_ROOT)}`",
                f"Manuscript body: `{MANUSCRIPT_BODY_PATH.relative_to(REPO_ROOT)}`",
                "",
                "Panel PDFs: `analysis/figures/fig3_panel_a_joint_distribution.pdf` through "
                "`analysis/figures/fig3_panel_f_cap_local_global_recovery.pdf`.",
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
    cap_profiles_df, _cap_records_df, _cap_id_to_name = build_cap_human_profiles()
    cap_ontology_profiles_df = cap_profiles_with_ontology_terms(cap_profiles_df)
    cap_joint_df = build_cap_cross_project_joint_distribution(cap_profiles_df, CAP_JOINT_DISTRIBUTION_PATH)
    build_cap_cross_project_joint_distribution(
        cap_ontology_profiles_df,
        CAP_ONTOLOGY_JOINT_DISTRIBUTION_PATH,
    )
    cap_ontology_recovery_df = build_label_local_global_recovery_from_profiles(
        cap_ontology_profiles_df,
        CAP_ONTOLOGY_LOCAL_GLOBAL_PATH,
        min_profiles=3,
    )
    llmarkers_profiles_df, _llmarkers_id_to_name = build_profiles()
    llmarkers_jaccard_values_df, llmarkers_jaccard_summary_df = build_same_label_marker_jaccard_distribution(
        llmarkers_profiles_df,
        resource="LLMarkers",
        context_col="paper_uid",
        max_random_pairs=100_000,
        seed=17,
    )
    cap_jaccard_values_df, cap_jaccard_summary_df = build_same_label_marker_jaccard_distribution(
        cap_profiles_df,
        resource="CAP labels",
        context_col="project_id",
        max_random_pairs=100_000,
        seed=23,
    )
    same_label_jaccard_values_df = pd.concat(
        [llmarkers_jaccard_values_df, cap_jaccard_values_df],
        ignore_index=True,
    )
    same_label_jaccard_summary_df = pd.concat(
        [llmarkers_jaccard_summary_df, cap_jaccard_summary_df],
        ignore_index=True,
    )
    same_label_jaccard_values_df.to_csv(SAME_LABEL_JACCARD_VALUES_PATH, sep="\t", index=False)
    same_label_jaccard_summary_df.to_csv(SAME_LABEL_JACCARD_SUMMARY_PATH, sep="\t", index=False)
    cap_same_label_examples_df, cap_different_label_examples_df = build_label_disagreement_examples_from_profiles(
        cap_profiles_df,
        CAP_LABEL_DISAGREEMENT_SAME_PATH,
        CAP_LABEL_DISAGREEMENT_DIFFERENT_PATH,
        min_same_profiles=3,
    )
    cap_label_positions = {
        "REGULATORY T CELL": (0.50, 0.91),
        "NEUTROPHIL": (0.50, 0.82),
        "PLASMACYTOID DENDRITIC CELL": (0.50, 0.73),
        "CONVENTIONAL DENDRITIC CELL": (0.50, 0.64),
        "B CELL": (0.50, 0.55),
        "MONOCYTE": (0.26, 0.66),
        "MACROPHAGE": (0.25, 0.53),
        "T CELL": (0.25, 0.40),
        "DENDRITIC CELL": (0.25, 0.28),
    }

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
        lambda ax: plot_labeling_disagreement_examples(
            ax,
            same_label_examples_df,
            different_label_examples_df,
            same_label_jaccard_values_df,
            same_label_jaccard_summary_df,
            "LLMarkers",
        ),
    )
    save_panel(
        PANEL_C_PATH,
        PANEL_C_PNG_PATH,
        lambda ax: plot_label_local_global_recovery(ax, label_recovery_df),
    )
    save_panel(
        PANEL_D_PATH,
        PANEL_D_PNG_PATH,
        lambda ax: plot_joint_distribution(ax, cap_joint_df, "CAP human profiles, cross-project"),
    )
    save_panel(
        PANEL_E_PATH,
        PANEL_E_PNG_PATH,
        lambda ax: plot_labeling_disagreement_examples(
            ax,
            cap_same_label_examples_df,
            cap_different_label_examples_df,
            same_label_jaccard_values_df,
            same_label_jaccard_summary_df,
            "CAP labels",
            "CAP human profiles, cross-project",
        ),
    )
    save_panel(
        PANEL_F_PATH,
        PANEL_F_PNG_PATH,
        lambda ax: plot_label_local_global_recovery(
            ax,
            cap_ontology_recovery_df,
            "CAP ontology terms, cross-project",
            label_positions=cap_label_positions,
        ),
    )

    write_report(summary, label_df, transfer_label_df, selected_df)

    print(f"Wrote {PANEL_A_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PANEL_B_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PANEL_C_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PANEL_D_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PANEL_E_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PANEL_F_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
