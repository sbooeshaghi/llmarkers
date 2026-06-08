from __future__ import annotations

import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

from cross_study_gene_space import REPO_ROOT, RESULTS_DIR


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

LOCAL_GLOBAL_PAIR_PATH = RESULTS_DIR / "local_global_marker_pair_summary.tsv"
LOCAL_GLOBAL_PAPER_PATH = RESULTS_DIR / "local_global_paper_marker_summary.tsv"
LOCAL_GLOBAL_LABEL_PATH = RESULTS_DIR / "local_global_label_coherence_summary.tsv"
LOCAL_GLOBAL_LIFTOVER_PATH = RESULTS_DIR / "local_global_profile_marker_liftover.tsv"
IDENTIFIABILITY_SUMMARY_PATH = RESULTS_DIR / "marker_identifiability_partition_summary.tsv"
IDENTIFIABILITY_SELECTED_PATH = RESULTS_DIR / "marker_identifiability_selected_genes.tsv"

PROTOTYPE_SUMMARY_PATH = RESULTS_DIR / "formal_marker_result_prototype_summary.tsv"
PROTOTYPE_REPORT_PATH = RESULTS_DIR / "formal_marker_result_prototype_report.md"
FIGURE_PATH = FIGURE_DIR / "fig_formal_marker_result_prototype.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig_formal_marker_result_prototype.png"


HIGHLIGHT_LABELS = [
    "T CELL",
    "TREG",
    "CD 4 T CELL",
    "CD 8 T CELL",
    "MACROPHAGE",
    "MONOCYTE",
    "FIBROBLAST",
    "OLIGODENDROCYTES",
    "MELANOCYTE",
]

PAIR_CATEGORY_LABELS = {
    "within_paper_different_label": "Same paper,\ndifferent label",
    "between_paper_same_exact_label": "Different paper,\nsame label",
    "between_paper_same_broad_neighborhood": "Different paper,\nsame broad label",
    "between_paper_different_broad_neighborhood": "Different paper,\ndifferent broad label",
}

ROLE_ORDER = ["essential_in_minimum_panels", "exchangeable_in_minimum_panels"]
ROLE_LABELS = {
    "essential_in_minimum_panels": "Essential",
    "exchangeable_in_minimum_panels": "Exchangeable",
}
ROLE_COLORS = {
    "essential_in_minimum_panels": "#2f6f4e",
    "exchangeable_in_minimum_panels": "#b8b8b8",
}


def load_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    required = [
        LOCAL_GLOBAL_PAIR_PATH,
        LOCAL_GLOBAL_PAPER_PATH,
        LOCAL_GLOBAL_LABEL_PATH,
        LOCAL_GLOBAL_LIFTOVER_PATH,
        IDENTIFIABILITY_SUMMARY_PATH,
        IDENTIFIABILITY_SELECTED_PATH,
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing prerequisite analysis outputs. Run "
            "`analysis/build_local_global_marker_analysis.py` and "
            "`analysis/build_marker_identifiability_analysis.py` first. Missing: "
            + ", ".join(missing)
        )

    return (
        pd.read_csv(LOCAL_GLOBAL_PAIR_PATH, sep="\t"),
        pd.read_csv(LOCAL_GLOBAL_PAPER_PATH, sep="\t"),
        pd.read_csv(LOCAL_GLOBAL_LABEL_PATH, sep="\t"),
        pd.read_csv(LOCAL_GLOBAL_LIFTOVER_PATH, sep="\t"),
        pd.read_csv(IDENTIFIABILITY_SUMMARY_PATH, sep="\t"),
        pd.read_csv(IDENTIFIABILITY_SELECTED_PATH, sep="\t"),
    )


def pct(value: float) -> str:
    return f"{100 * value:.1f}%"


def num(value: float) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return f"{value:.3f}"


def build_summary_rows(
    pair_df: pd.DataFrame,
    paper_df: pd.DataFrame,
    label_df: pd.DataFrame,
    liftover_df: pd.DataFrame,
    ident_summary_df: pd.DataFrame,
    selected_df: pd.DataFrame,
) -> pd.DataFrame:
    same_label_liftover = liftover_df.loc[liftover_df["n_same_label_other_paper_profiles"].gt(0)]
    same_label_pairs = pair_df.loc[pair_df["pair_category"].eq("between_paper_same_exact_label")].iloc[0]
    background_pairs = pair_df.loc[pair_df["pair_category"].eq("between_paper_other")].iloc[0]
    within_paper_pairs = pair_df.loc[pair_df["pair_category"].eq("within_paper_different_label")].iloc[0]

    local_identifiable_fraction = float(paper_df["all_profiles_locally_identifiable"].mean())

    selected_ilp = selected_df.loc[selected_df["method"].eq("ilp_minimum")].copy()
    selected_ilp = selected_ilp.loc[
        selected_ilp["coverage_threshold"].eq(0.2)
        & selected_ilp["partition"].isin(
            ["reported_exact_labels_min5", "tcell_marker_clusters", "myeloid_marker_clusters"]
        )
    ]
    role_counts = (
        selected_ilp.groupby(["partition", "role"])
        .size()
        .reset_index(name="n_genes")
        .sort_values(["partition", "role"])
    )

    exact_ident = ident_summary_df.loc[
        ident_summary_df["partition"].eq("reported_exact_labels_min5")
        & ident_summary_df["coverage_threshold"].eq(0.2)
    ].iloc[0]

    rows = [
        {
            "result": "Local paper-level marker profiles are usually distinguishable",
            "value": pct(local_identifiable_fraction),
            "detail": "Fraction of papers whose reported profiles have distinct full marker signatures",
        },
        {
            "result": "Typical local marker problem size",
            "value": f"{paper_df['n_profiles'].median():.0f} profiles, greedy panel {paper_df['greedy_local_panel_size'].median():.0f} genes",
            "detail": "Median across papers with at least two marker profiles",
        },
        {
            "result": "Same exact labels across papers are marker-enriched but sparse",
            "value": f"mean J={same_label_pairs.mean_jaccard:.3f} vs background J={background_pairs.mean_jaccard:.3f}",
            "detail": "Pairwise marker Jaccard for different-paper profile pairs",
        },
        {
            "result": "Same exact labels often fail to recover local marker profiles",
            "value": f"median liftover={same_label_liftover['marker_fraction_recovered_by_same_label_other_papers'].median():.3f}",
            "detail": "Fraction of a profile's reported markers recovered by same-label profiles in other papers",
        },
        {
            "result": "Within-paper different-label markers are highly local",
            "value": f"{pct(within_paper_pairs.pct_jaccard_eq_0)} zero-overlap pairs",
            "detail": "Same-paper, different-label profile pairs",
        },
        {
            "result": "Exact labels collapse at high coverage",
            "value": f"{int(exact_ident.n_groups)} labels -> {int(exact_ident.n_distinct_signatures)} signatures",
            "detail": "Reported exact labels, 20% within-label marker coverage threshold",
        },
    ]
    for row in role_counts.itertuples(index=False):
        rows.append(
            {
                "result": f"{row.partition}: {ROLE_LABELS.get(row.role, row.role)} genes",
                "value": int(row.n_genes),
                "detail": "Role among ILP-selected minimum separating panel genes at 20% threshold",
            }
        )
    return pd.DataFrame(rows)


def plot_local_separability(ax: plt.Axes, paper_df: pd.DataFrame) -> None:
    x = paper_df["n_profiles"].to_numpy()
    y = paper_df["greedy_local_panel_size"].to_numpy()
    identifiable = paper_df["all_profiles_locally_identifiable"].to_numpy()
    ax.scatter(x[~identifiable], y[~identifiable], s=14, facecolor="#d8d8d8", edgecolor="black", linewidth=0.35)
    ax.scatter(x[identifiable], y[identifiable], s=14, facecolor="#3f3f3f", edgecolor="black", linewidth=0.25)
    max_lim = max(float(x.max()), float(y.max())) + 1
    ax.plot([0, max_lim], [0, max_lim], color="black", linewidth=0.8, alpha=0.35)
    ax.set_xlim(0, max_lim)
    ax.set_ylim(0, max_lim)
    ax.set_xlabel("Profiles reported in paper")
    ax.set_ylabel("Greedy local panel size")
    ax.text(
        0.04,
        0.94,
        f"{100 * identifiable.mean():.1f}% locally identifiable",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
    )


def plot_liftover(ax: plt.Axes, liftover_df: pd.DataFrame) -> None:
    values = liftover_df.loc[
        liftover_df["n_same_label_other_paper_profiles"].gt(0),
        "marker_fraction_recovered_by_same_label_other_papers",
    ].dropna()
    bins = np.linspace(0, 1, 11)
    ax.hist(values, bins=bins, facecolor="#bdbdbd", edgecolor="black", linewidth=0.7)
    median = values.median()
    ax.axvline(median, color="black", linewidth=1.2)
    ax.text(
        median + 0.02,
        ax.get_ylim()[1] * 0.88,
        f"median {median:.2f}",
        ha="left",
        va="top",
        fontsize=8,
    )
    ax.set_xlim(0, 1)
    ax.set_xlabel("Same-label marker liftover")
    ax.set_ylabel("Profiles")


def plot_label_coherence(ax: plt.Axes, label_df: pd.DataFrame) -> None:
    selected = label_df.loc[label_df["normalized_cell_type"].isin(HIGHLIGHT_LABELS)].copy()
    selected["display"] = selected["normalized_cell_type"].str.title()
    selected = selected.sort_values(["median_jaccard", "n_profiles"], ascending=[True, False])
    y = np.arange(len(selected))
    ax.hlines(y, 0, selected["median_jaccard"], color="#bdbdbd", linewidth=3)
    ax.scatter(
        selected["median_jaccard"],
        y,
        s=36,
        facecolor="white",
        edgecolor="black",
        linewidth=0.8,
        zorder=3,
    )
    for idx, row in enumerate(selected.itertuples(index=False)):
        ax.text(
            min(row.median_jaccard + 0.018, 0.66),
            idx,
            f"n={int(row.n_profiles)}",
            va="center",
            ha="left",
            fontsize=7,
        )
    ax.set_yticks(y)
    ax.set_yticklabels(selected["display"])
    ax.set_xlim(0, 0.7)
    ax.set_xlabel("Median marker Jaccard across papers")
    ax.set_ylabel("Recurrent label")


def plot_marker_roles(ax: plt.Axes, selected_df: pd.DataFrame) -> None:
    df = selected_df.loc[
        selected_df["method"].eq("ilp_minimum")
        & selected_df["coverage_threshold"].eq(0.2)
        & selected_df["partition"].isin(
            ["reported_exact_labels_min5", "tcell_marker_clusters", "myeloid_marker_clusters"]
        )
    ].copy()
    partition_labels = {
        "reported_exact_labels_min5": "Exact\nlabels",
        "tcell_marker_clusters": "T-cell\nclusters",
        "myeloid_marker_clusters": "Myeloid\nclusters",
    }
    partitions = list(partition_labels)
    bottoms = np.zeros(len(partitions))
    for role in ROLE_ORDER:
        counts = [
            int(((df["partition"] == partition) & (df["role"] == role)).sum())
            for partition in partitions
        ]
        ax.bar(
            np.arange(len(partitions)),
            counts,
            bottom=bottoms,
            color=ROLE_COLORS[role],
            edgecolor="black",
            linewidth=0.7,
            label=ROLE_LABELS[role],
        )
        bottoms += np.asarray(counts)
    for idx, total in enumerate(bottoms):
        ax.text(idx, total + max(bottoms) * 0.03, f"{int(total)}", ha="center", va="bottom", fontsize=8)
    ax.set_xticks(np.arange(len(partitions)))
    ax.set_xticklabels([partition_labels[p] for p in partitions])
    ax.set_ylabel("Genes in minimum panel")
    ax.legend(
        handles=[Patch(facecolor=ROLE_COLORS[role], edgecolor="black", label=ROLE_LABELS[role]) for role in ROLE_ORDER],
        frameon=False,
        fontsize=8,
        loc="upper right",
    )


def plot_pair_means(ax: plt.Axes, pair_df: pd.DataFrame) -> None:
    df = pair_df.loc[pair_df["pair_category"].isin(PAIR_CATEGORY_LABELS)].copy()
    df["display"] = df["pair_category"].map(PAIR_CATEGORY_LABELS)
    y = np.arange(len(df))
    ax.barh(y, df["mean_jaccard"], facecolor="#cfcfcf", edgecolor="black", linewidth=0.7)
    for idx, row in enumerate(df.itertuples(index=False)):
        ax.text(row.mean_jaccard + 0.003, idx, f"{row.mean_jaccard:.3f}", ha="left", va="center", fontsize=7)
    ax.set_yticks(y)
    ax.set_yticklabels(df["display"])
    ax.invert_yaxis()
    ax.set_xlim(0, max(0.12, df["mean_jaccard"].max() * 1.25))
    ax.set_xlabel("Mean marker Jaccard")


def make_figure(
    pair_df: pd.DataFrame,
    paper_df: pd.DataFrame,
    label_df: pd.DataFrame,
    liftover_df: pd.DataFrame,
    selected_df: pd.DataFrame,
) -> None:
    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.dpi": 150,
        }
    )
    fig = plt.figure(figsize=(10.5, 7.2))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.05, 1.05, 1.15], height_ratios=[1, 1], wspace=0.45, hspace=0.55)
    axes = [
        fig.add_subplot(gs[0, 0]),
        fig.add_subplot(gs[0, 1]),
        fig.add_subplot(gs[0, 2]),
        fig.add_subplot(gs[1, 0]),
        fig.add_subplot(gs[1, 1:]),
    ]
    plot_local_separability(axes[0], paper_df)
    plot_liftover(axes[1], liftover_df)
    plot_pair_means(axes[2], pair_df)
    plot_marker_roles(axes[3], selected_df)
    plot_label_coherence(axes[4], label_df)
    for letter, ax in zip("ABCDE", axes, strict=True):
        ax.text(-0.16, 1.06, letter, transform=ax.transAxes, fontsize=11, fontweight="bold")
    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    fig.savefig(FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)


def markdown_table(df: pd.DataFrame) -> str:
    string_df = df.fillna("").astype(str)
    header = "| " + " | ".join(string_df.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(string_df.columns)) + " |"
    rows = ["| " + " | ".join(row) + " |" for row in string_df.itertuples(index=False, name=None)]
    return "\n".join([header, separator, *rows])


def write_report(
    summary_df: pd.DataFrame,
    label_df: pd.DataFrame,
    ident_summary_df: pd.DataFrame,
    selected_df: pd.DataFrame,
) -> None:
    label_display = label_df[
        [
            "normalized_cell_type",
            "n_profiles",
            "n_papers",
            "mean_jaccard",
            "median_jaccard",
            "pct_jaccard_eq_0",
            "pct_jaccard_ge_0_25",
            "example_reported_labels",
        ]
    ].head(20).copy()
    for col in ["mean_jaccard", "median_jaccard", "pct_jaccard_eq_0", "pct_jaccard_ge_0_25"]:
        label_display[col] = label_display[col].map(num)

    selected_display = selected_df.loc[
        selected_df["method"].eq("ilp_minimum")
        & selected_df["coverage_threshold"].eq(0.2)
        & selected_df["partition"].isin(["tcell_marker_clusters", "myeloid_marker_clusters"])
    ][["partition", "gene_name", "role", "on_groups", "mean_on_group_coverage"]].copy()
    selected_display["mean_on_group_coverage"] = selected_display["mean_on_group_coverage"].map(num)

    ident_display = ident_summary_df[
        [
            "partition",
            "coverage_threshold",
            "n_groups",
            "n_distinct_signatures",
            "all_groups_identifiable_with_all_genes",
            "information_lower_bound_log2",
            "greedy_panel_size",
            "ilp_panel_size",
            "ilp_status",
        ]
    ].copy()

    lines = [
        "# Formal Marker Result Prototype",
        "",
        "This prototype translates the Lean local/global marker formalization into an empirical analysis set.",
        "The central claim is that single papers report local separating marker claims, while atlas building requires testing whether those claims lift to a global comparison set.",
        "",
        f"Figure prototype: `{FIGURE_PATH.relative_to(REPO_ROOT)}`",
        "",
        "## Candidate Result Summary",
        "",
        markdown_table(summary_df),
        "",
        "## How This Compares With Current Results",
        "",
        "- The current cross-study joint distribution remains useful as the visual setup, but this result gives it a stronger mathematical interpretation.",
        "- The local/global analysis can replace a weaker version of the label-versus-marker comparison because it directly states what is local, what lifts globally, and what fails.",
        "- The essential/exchangeable marker result is stronger than a generic coverage/purity result because the gene classes are defined by a formal separation objective.",
        "- The T-cell and myeloid examples should remain as biological vignettes, but they should support the formal result rather than carry the entire conclusion.",
        "- The coverage/purity/F1 plots can move to the supplement or be reframed as exploratory diagnostics for marker stability.",
        "",
        "## Label Underspecification Examples",
        "",
        markdown_table(label_display),
        "",
        "## Identifiability Summary",
        "",
        markdown_table(ident_display),
        "",
        "## Essential And Exchangeable Genes In Immune Marker Clusters",
        "",
        markdown_table(selected_display),
        "",
        "## Recommended Manuscript Use",
        "",
        "Use this as the closing result after large-scale extraction. The flow would be: extracted marker claims form a global binary matrix; papers define local comparison sets; local marker claims often do not lift cleanly to the global matrix; the formalization lets us identify underspecified labels and classify markers as essential or exchangeable for a chosen partition.",
    ]
    PROTOTYPE_REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    pair_df, paper_df, label_df, liftover_df, ident_summary_df, selected_df = load_tables()
    summary_df = build_summary_rows(pair_df, paper_df, label_df, liftover_df, ident_summary_df, selected_df)
    summary_df.to_csv(PROTOTYPE_SUMMARY_PATH, sep="\t", index=False)
    make_figure(pair_df, paper_df, label_df, liftover_df, selected_df)
    write_report(summary_df, label_df, ident_summary_df, selected_df)
    print(f"Wrote {PROTOTYPE_SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PROTOTYPE_REPORT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PNG_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
