from __future__ import annotations

import math
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from build_local_global_marker_analysis import build_profiles, ceil_log2
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR


PROFILE_LIFT_PATH = RESULTS_DIR / "local_global_marker_transfer_lift.tsv"
PAPER_LIFT_PATH = RESULTS_DIR / "local_global_marker_transfer_lift_by_paper.tsv"
LABEL_LIFT_PATH = RESULTS_DIR / "local_global_marker_transfer_lift_by_label.tsv"
SUMMARY_PATH = RESULTS_DIR / "local_global_marker_transfer_lift_summary.tsv"
REPORT_PATH = RESULTS_DIR / "local_global_marker_transfer_lift_report.md"
FIGURE_PATH = REPO_ROOT / "analysis" / "figures" / "fig_local_global_marker_lift.pdf"
FIGURE_PNG_PATH = REPO_ROOT / "analysis" / "figures" / "fig_local_global_marker_lift.png"

MIN_COMPARISON_PROFILES = 2

RELATION_LABELS = {
    "same_exact_label": "Same reported label",
    "same_broad_neighborhood": "Same broad lineage",
}

SCOPE_LABELS = {
    "all_reported_markers": "All reported markers",
    "local_private_markers": "Local-only markers",
}


def safe_ratio(numerator: float, denominator: float) -> float:
    if denominator == 0 or math.isnan(denominator):
        return np.nan
    return numerator / denominator


def mean_or_nan(values: list[float]) -> float:
    if not values:
        return np.nan
    return float(np.mean(values))


def union_markers(rows: list[object]) -> set[str]:
    genes: set[str] = set()
    for row in rows:
        genes |= row.marker_set
    return genes


def marker_recall(marker_set: set[str], comparison_set: set[str]) -> float:
    if not marker_set:
        return np.nan
    return len(marker_set & comparison_set) / len(marker_set)


def expected_union_recall(marker_set: set[str], background_prevalence: dict[str, float], n_draws: int) -> float:
    if not marker_set:
        return np.nan
    expected = []
    for gene_id in marker_set:
        prevalence = background_prevalence.get(gene_id, 0.0)
        expected.append(1.0 - (1.0 - prevalence) ** n_draws)
    return float(np.mean(expected))


def expected_mean_recall(marker_set: set[str], background_prevalence: dict[str, float]) -> float:
    if not marker_set:
        return np.nan
    return float(np.mean([background_prevalence.get(gene_id, 0.0) for gene_id in marker_set]))


def build_background_prevalence(
    marker_set: set[str],
    global_gene_profile_counts: Counter,
    paper_gene_profile_counts: Counter,
    n_global_profiles: int,
    n_paper_profiles: int,
) -> dict[str, float]:
    n_background = n_global_profiles - n_paper_profiles
    if n_background <= 0:
        return {gene_id: np.nan for gene_id in marker_set}
    return {
        gene_id: (global_gene_profile_counts[gene_id] - paper_gene_profile_counts[gene_id]) / n_background
        for gene_id in marker_set
    }


def build_profile_lift() -> tuple[pd.DataFrame, pd.DataFrame]:
    profiles_df, id_to_name = build_profiles()
    profiles_df = profiles_df.copy()
    profiles_df["paper_n_profiles"] = profiles_df.groupby("paper_uid")["profile_uid"].transform("size")
    profiles_df["local_marker_lb_log2"] = profiles_df["paper_n_profiles"].map(ceil_log2)
    atlas_marker_lb_log2 = ceil_log2(len(profiles_df))

    rows = list(profiles_df.itertuples(index=False))
    paper_rows: dict[str, list[object]] = defaultdict(list)
    label_rows: dict[str, list[object]] = defaultdict(list)
    neighborhood_rows: dict[str, list[object]] = defaultdict(list)
    paper_gene_profile_counts: dict[str, Counter] = defaultdict(Counter)
    global_gene_profile_counts: Counter = Counter()

    for row in rows:
        paper_rows[row.paper_uid].append(row)
        if row.normalized_cell_type:
            label_rows[row.normalized_cell_type].append(row)
        if row.neighborhood:
            neighborhood_rows[row.neighborhood].append(row)
        for gene_id in row.marker_set:
            global_gene_profile_counts[gene_id] += 1
            paper_gene_profile_counts[row.paper_uid][gene_id] += 1

    output_rows = []
    for row in rows:
        paper_counter = paper_gene_profile_counts[row.paper_uid]
        local_private = {gene_id for gene_id in row.marker_set if paper_counter[gene_id] == 1}
        marker_scopes = {
            "all_reported_markers": row.marker_set,
            "local_private_markers": local_private,
        }
        relation_to_rows = {
            "same_exact_label": [
                other for other in label_rows.get(row.normalized_cell_type, [])
                if row.normalized_cell_type and other.paper_uid != row.paper_uid
            ],
            "same_broad_neighborhood": [
                other for other in neighborhood_rows.get(row.neighborhood, [])
                if row.neighborhood and other.paper_uid != row.paper_uid
            ],
        }

        for relation, comparison_rows in relation_to_rows.items():
            if not comparison_rows:
                continue
            comparison_union = union_markers(comparison_rows)
            n_comparison = len(comparison_rows)
            n_background = len(profiles_df) - len(paper_rows[row.paper_uid])

            for marker_scope, markers in marker_scopes.items():
                if not markers:
                    continue
                background_prevalence = build_background_prevalence(
                    markers,
                    global_gene_profile_counts,
                    paper_counter,
                    len(profiles_df),
                    len(paper_rows[row.paper_uid]),
                )
                observed_profile_recalls = [
                    marker_recall(markers, other.marker_set) for other in comparison_rows
                ]
                observed_mean = mean_or_nan(observed_profile_recalls)
                observed_union = marker_recall(markers, comparison_union)
                expected_mean = expected_mean_recall(markers, background_prevalence)
                expected_union = expected_union_recall(markers, background_prevalence, n_comparison)
                recovered = sorted(markers & comparison_union)
                unrecovered = sorted(markers - comparison_union)

                output_rows.append(
                    {
                        "source_corpus": row.source_corpus,
                        "paper_id": row.paper_id,
                        "paper_key": row.paper_key,
                        "cell_type": row.cell_type,
                        "normalized_cell_type": row.normalized_cell_type,
                        "neighborhood": row.neighborhood,
                        "relation": relation,
                        "relation_label": RELATION_LABELS[relation],
                        "marker_scope": marker_scope,
                        "marker_scope_label": SCOPE_LABELS[marker_scope],
                        "n_markers": len(markers),
                        "n_comparison_profiles": n_comparison,
                        "n_background_profiles": n_background,
                        "paper_n_profiles": len(paper_rows[row.paper_uid]),
                        "local_marker_lb_log2": row.local_marker_lb_log2,
                        "atlas_marker_lb_log2": atlas_marker_lb_log2,
                        "marker_lb_gap_log2": atlas_marker_lb_log2 - row.local_marker_lb_log2,
                        "observed_mean_profile_recall": observed_mean,
                        "expected_mean_profile_recall": expected_mean,
                        "mean_profile_recall_lift": safe_ratio(observed_mean, expected_mean),
                        "observed_union_recall": observed_union,
                        "expected_union_recall": expected_union,
                        "union_recall_lift": safe_ratio(observed_union, expected_union),
                        "n_recovered_markers": len(recovered),
                        "n_unrecovered_markers": len(unrecovered),
                        "recovered_marker_names": "; ".join(id_to_name.get(gene_id, gene_id) for gene_id in recovered[:40]),
                        "unrecovered_marker_names": "; ".join(id_to_name.get(gene_id, gene_id) for gene_id in unrecovered[:40]),
                    }
                )

    lift_df = pd.DataFrame(output_rows)
    paper_df = build_paper_summary(lift_df)
    return lift_df, paper_df


def build_paper_summary(lift_df: pd.DataFrame) -> pd.DataFrame:
    if lift_df.empty:
        return pd.DataFrame()
    eligible = lift_df.loc[lift_df["n_comparison_profiles"] >= MIN_COMPARISON_PROFILES].copy()
    if eligible.empty:
        return pd.DataFrame()
    grouped = eligible.groupby(
        ["source_corpus", "paper_id", "paper_key", "relation", "relation_label", "marker_scope", "marker_scope_label"],
        sort=True,
    )
    rows = []
    for keys, group in grouped:
        source_corpus, paper_id, paper_key, relation, relation_label, marker_scope, marker_scope_label = keys
        rows.append(
            {
                "source_corpus": source_corpus,
                "paper_id": paper_id,
                "paper_key": paper_key,
                "relation": relation,
                "relation_label": relation_label,
                "marker_scope": marker_scope,
                "marker_scope_label": marker_scope_label,
                "n_profiles_with_comparison": len(group),
                "paper_n_profiles": int(group["paper_n_profiles"].iloc[0]),
                "local_marker_lb_log2": int(group["local_marker_lb_log2"].iloc[0]),
                "atlas_marker_lb_log2": int(group["atlas_marker_lb_log2"].iloc[0]),
                "marker_lb_gap_log2": int(group["marker_lb_gap_log2"].iloc[0]),
                "median_observed_union_recall": float(group["observed_union_recall"].median()),
                "median_expected_union_recall": float(group["expected_union_recall"].median()),
                "median_union_recall_lift": float(group["union_recall_lift"].replace([np.inf, -np.inf], np.nan).median()),
                "median_observed_mean_profile_recall": float(group["observed_mean_profile_recall"].median()),
                "median_expected_mean_profile_recall": float(group["expected_mean_profile_recall"].median()),
                "median_mean_profile_recall_lift": float(group["mean_profile_recall_lift"].replace([np.inf, -np.inf], np.nan).median()),
            }
        )
    return pd.DataFrame(rows).sort_values(["relation", "marker_scope", "median_union_recall_lift"], ascending=[True, True, False])


def build_label_summary(lift_df: pd.DataFrame) -> pd.DataFrame:
    eligible = lift_df.loc[
        lift_df["relation"].eq("same_exact_label")
        & (lift_df["n_comparison_profiles"] >= MIN_COMPARISON_PROFILES)
        & lift_df["normalized_cell_type"].ne("")
    ].copy()
    if eligible.empty:
        return pd.DataFrame()

    rows = []
    grouped = eligible.groupby(["normalized_cell_type", "marker_scope", "marker_scope_label"], sort=True)
    for (label, marker_scope, marker_scope_label), group in grouped:
        finite_lift = group["union_recall_lift"].replace([np.inf, -np.inf], np.nan).dropna()
        mean_lift = group["mean_profile_recall_lift"].replace([np.inf, -np.inf], np.nan).dropna()
        rows.append(
            {
                "normalized_cell_type": label,
                "marker_scope": marker_scope,
                "marker_scope_label": marker_scope_label,
                "n_profiles": len(group),
                "n_papers": group["paper_key"].nunique(),
                "example_reported_labels": "; ".join(sorted(group["cell_type"].unique())[:8]),
                "median_n_markers": float(group["n_markers"].median()),
                "median_observed_union_recall": float(group["observed_union_recall"].median()),
                "median_expected_union_recall": float(group["expected_union_recall"].median()),
                "median_union_recall_lift": float(finite_lift.median()) if len(finite_lift) else np.nan,
                "pct_union_lift_gt_1": float((finite_lift > 1.0).mean()) if len(finite_lift) else np.nan,
                "median_observed_mean_profile_recall": float(group["observed_mean_profile_recall"].median()),
                "median_expected_mean_profile_recall": float(group["expected_mean_profile_recall"].median()),
                "median_mean_profile_recall_lift": float(mean_lift.median()) if len(mean_lift) else np.nan,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["marker_scope", "n_profiles", "median_union_recall_lift"],
        ascending=[True, False, False],
    )


def build_summary(lift_df: pd.DataFrame) -> pd.DataFrame:
    eligible = lift_df.loc[lift_df["n_comparison_profiles"] >= MIN_COMPARISON_PROFILES].copy()
    rows = []
    for (relation, marker_scope), group in eligible.groupby(["relation", "marker_scope"], sort=True):
        finite_lift = group["union_recall_lift"].replace([np.inf, -np.inf], np.nan).dropna()
        mean_lift = group["mean_profile_recall_lift"].replace([np.inf, -np.inf], np.nan).dropna()
        rows.append(
            {
                "relation": relation,
                "relation_label": RELATION_LABELS[relation],
                "marker_scope": marker_scope,
                "marker_scope_label": SCOPE_LABELS[marker_scope],
                "n_profiles": len(group),
                "median_n_markers": float(group["n_markers"].median()),
                "median_n_comparison_profiles": float(group["n_comparison_profiles"].median()),
                "median_observed_union_recall": float(group["observed_union_recall"].median()),
                "median_expected_union_recall": float(group["expected_union_recall"].median()),
                "median_union_recall_lift": float(finite_lift.median()) if len(finite_lift) else np.nan,
                "pct_union_lift_gt_1": float((finite_lift > 1.0).mean()) if len(finite_lift) else np.nan,
                "median_observed_mean_profile_recall": float(group["observed_mean_profile_recall"].median()),
                "median_expected_mean_profile_recall": float(group["expected_mean_profile_recall"].median()),
                "median_mean_profile_recall_lift": float(mean_lift.median()) if len(mean_lift) else np.nan,
                "pct_mean_lift_gt_1": float((mean_lift > 1.0).mean()) if len(mean_lift) else np.nan,
            }
        )
    return pd.DataFrame(rows)


def markdown_table(df: pd.DataFrame) -> str:
    display_df = df.fillna("").astype(str)
    header = "| " + " | ".join(display_df.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(display_df.columns)) + " |"
    rows = ["| " + " | ".join(row) + " |" for row in display_df.itertuples(index=False, name=None)]
    return "\n".join([header, separator, *rows])


def format_float(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{value:.3f}"


def write_report(
    lift_df: pd.DataFrame,
    paper_df: pd.DataFrame,
    label_df: pd.DataFrame,
    summary_df: pd.DataFrame,
) -> None:
    summary_display = summary_df.copy()
    for col in [
        "median_n_markers",
        "median_n_comparison_profiles",
        "median_observed_union_recall",
        "median_expected_union_recall",
        "median_union_recall_lift",
        "pct_union_lift_gt_1",
        "median_observed_mean_profile_recall",
        "median_expected_mean_profile_recall",
        "median_mean_profile_recall_lift",
        "pct_mean_lift_gt_1",
    ]:
        summary_display[col] = summary_display[col].map(format_float)

    same_label = summary_df.loc[
        summary_df["relation"].eq("same_exact_label")
        & summary_df["marker_scope"].eq("all_reported_markers")
    ]
    local_private = summary_df.loc[
        summary_df["relation"].eq("same_exact_label")
        & summary_df["marker_scope"].eq("local_private_markers")
    ]

    headline_lines = []
    if not same_label.empty:
        row = same_label.iloc[0]
        headline_lines.append(
            f"- Same-label outside-paper profiles recovered a median {row.median_observed_union_recall:.3f} of all reported markers, "
            f"versus {row.median_expected_union_recall:.3f} expected from background prevalence "
            f"(median lift {row.median_union_recall_lift:.2f}x)."
        )
    if not local_private.empty:
        row = local_private.iloc[0]
        headline_lines.append(
            f"- For locally private markers, same-label profiles recovered a median {row.median_observed_union_recall:.3f}, "
            f"versus {row.median_expected_union_recall:.3f} expected "
            f"(median lift {row.median_union_recall_lift:.2f}x)."
        )

    paper_display = paper_df.loc[
        paper_df["relation"].eq("same_exact_label")
        & paper_df["marker_scope"].eq("all_reported_markers")
        & (paper_df["n_profiles_with_comparison"] >= 3)
        & (paper_df["paper_n_profiles"] >= 3)
    ].copy()
    if not paper_display.empty:
        paper_display = paper_display.sort_values("median_union_recall_lift", ascending=False).head(10)
        paper_display = paper_display[
            [
                "paper_key",
                "n_profiles_with_comparison",
                "paper_n_profiles",
                "local_marker_lb_log2",
                "marker_lb_gap_log2",
                "median_observed_union_recall",
                "median_expected_union_recall",
                "median_union_recall_lift",
            ]
        ].copy()
        for col in [
            "median_observed_union_recall",
            "median_expected_union_recall",
            "median_union_recall_lift",
        ]:
            paper_display[col] = paper_display[col].map(format_float)

    label_display = label_df.loc[label_df["marker_scope"].eq("all_reported_markers")].copy()
    label_high = pd.DataFrame()
    label_low = pd.DataFrame()
    if not label_display.empty:
        label_display = label_display.loc[label_display["n_profiles"] >= 5].copy()
        label_cols = [
            "normalized_cell_type",
            "n_profiles",
            "n_papers",
            "median_observed_union_recall",
            "median_expected_union_recall",
            "median_union_recall_lift",
            "example_reported_labels",
        ]
        label_high = label_display.sort_values("median_union_recall_lift", ascending=False).head(10)[label_cols].copy()
        label_low = label_display.sort_values("median_union_recall_lift", ascending=True).head(10)[label_cols].copy()
        for table in [label_high, label_low]:
            for col in [
                "median_observed_union_recall",
                "median_expected_union_recall",
                "median_union_recall_lift",
            ]:
                table[col] = table[col].map(format_float)

    lines = [
        "# Local-to-Global Marker Transfer Lift",
        "",
        "This analysis asks whether marker genes reported for a cell type in one paper transfer to related profiles in other papers more often than expected by corpus background frequency.",
        "",
        "For a reported profile with marker set `S`, observed recovery is the fraction of genes in `S` found in outside-paper profiles with the same reported label or same broad lineage. Expected recovery is computed from outside-paper gene prevalence in LLMarkersDB. Lift is `observed / expected`.",
        "",
        "The union metric asks whether a marker is recovered in any related outside-paper profile. The mean-profile metric asks how much of the marker set is recovered in an average related profile.",
        "",
        "Caveat: absence means not reported as a marker in this corpus, not absent expression.",
        "",
        "## Headline",
        "",
        *headline_lines,
        "",
        "## Summary",
        "",
        markdown_table(summary_display),
        "",
        "## Highest Same-Label Paper-Level Lift",
        "",
        markdown_table(paper_display) if not paper_display.empty else "_No eligible rows._",
        "",
        "## Recurrent Labels With High Transfer Lift",
        "",
        markdown_table(label_high) if not label_high.empty else "_No eligible rows._",
        "",
        "## Recurrent Labels With Low Transfer Lift",
        "",
        markdown_table(label_low) if not label_low.empty else "_No eligible rows._",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_scatter(ax: plt.Axes, lift_df: pd.DataFrame, relation: str, title: str) -> None:
    df = lift_df.loc[
        lift_df["relation"].eq(relation)
        & lift_df["marker_scope"].eq("all_reported_markers")
        & (lift_df["n_comparison_profiles"] >= MIN_COMPARISON_PROFILES)
    ].copy()
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["expected_union_recall", "observed_union_recall", "union_recall_lift"])
    if df.empty:
        ax.set_axis_off()
        return
    lift = df["union_recall_lift"].clip(lower=0, upper=5)
    sc = ax.scatter(
        df["expected_union_recall"],
        df["observed_union_recall"],
        c=lift,
        cmap="viridis",
        s=10,
        alpha=0.72,
        linewidth=0,
    )
    ax.plot([0, 1], [0, 1], color="#777777", linewidth=0.7, linestyle="--")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(title, fontsize=9, fontweight="bold")
    ax.set_xlabel("Expected marker recovery")
    ax.set_ylabel("Observed marker recovery")
    median_lift = df["union_recall_lift"].median()
    ax.text(
        0.04,
        0.94,
        f"median lift = {median_lift:.2f}x",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=7,
    )
    return sc


def plot_lift_distribution(ax: plt.Axes, lift_df: pd.DataFrame) -> None:
    eligible = lift_df.loc[lift_df["n_comparison_profiles"] >= MIN_COMPARISON_PROFILES].copy()
    eligible = eligible.replace([np.inf, -np.inf], np.nan).dropna(subset=["union_recall_lift"])
    order = [
        ("same_exact_label", "all_reported_markers"),
        ("same_exact_label", "local_private_markers"),
        ("same_broad_neighborhood", "all_reported_markers"),
        ("same_broad_neighborhood", "local_private_markers"),
    ]
    labels = [
        "Same label\nall",
        "Same label\nlocal-only",
        "Same lineage\nall",
        "Same lineage\nlocal-only",
    ]
    rng = np.random.default_rng(11)
    for idx, (relation, marker_scope) in enumerate(order, start=1):
        values = eligible.loc[
            eligible["relation"].eq(relation)
            & eligible["marker_scope"].eq(marker_scope),
            "union_recall_lift",
        ].dropna()
        values = values.loc[values > 0]
        if values.empty:
            continue
        log_values = np.log2(values)
        x = idx + rng.uniform(-0.16, 0.16, size=len(log_values))
        ax.scatter(x, log_values, s=5, alpha=0.20, color="#4a4a4a", linewidth=0)
        q1, med, q3 = np.quantile(log_values, [0.25, 0.5, 0.75])
        ax.plot([idx - 0.24, idx + 0.24], [med, med], color="#b33630", linewidth=1.4)
        ax.add_patch(
            plt.Rectangle(
                (idx - 0.18, q1),
                0.36,
                q3 - q1,
                facecolor="#d9d9d9",
                edgecolor="#333333",
                linewidth=0.6,
                alpha=0.75,
            )
        )
    ax.axhline(0, color="#777777", linewidth=0.8, linestyle="--")
    ax.set_xticks(range(1, len(labels) + 1), labels, rotation=20, ha="right")
    ax.tick_params(axis="x", labelsize=7)
    ax.set_ylabel("log2 lift\n(observed / expected)")
    ax.set_title("Marker transfer lift", fontsize=9, fontweight="bold")


def plot_figure(lift_df: pd.DataFrame) -> None:
    FIGURE_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 3, figsize=(10.2, 3.3), constrained_layout=True)
    sc = plot_scatter(axes[0], lift_df, "same_exact_label", "Same reported label")
    plot_scatter(axes[1], lift_df, "same_broad_neighborhood", "Same broad lineage")
    plot_lift_distribution(axes[2], lift_df)
    if sc is not None:
        cbar = fig.colorbar(sc, ax=axes[:2], shrink=0.72, pad=0.02)
        cbar.set_label("Lift, clipped at 5x")
    fig.savefig(FIGURE_PATH)
    fig.savefig(FIGURE_PNG_PATH, dpi=250)
    plt.close(fig)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    lift_df, paper_df = build_profile_lift()
    label_df = build_label_summary(lift_df)
    summary_df = build_summary(lift_df)
    lift_df.to_csv(PROFILE_LIFT_PATH, sep="\t", index=False)
    paper_df.to_csv(PAPER_LIFT_PATH, sep="\t", index=False)
    label_df.to_csv(LABEL_LIFT_PATH, sep="\t", index=False)
    summary_df.to_csv(SUMMARY_PATH, sep="\t", index=False)
    write_report(lift_df, paper_df, label_df, summary_df)
    plot_figure(lift_df)
    print(f"Wrote {PROFILE_LIFT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PAPER_LIFT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {LABEL_LIFT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {FIGURE_PNG_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
