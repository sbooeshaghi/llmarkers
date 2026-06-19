#!/usr/bin/env python3
"""Prototype T-cell gene stability ratios.

This script compares how strongly a gene is supported by T-cell marker-gene
clusters versus repeated reported T-cell labels. It is meant as a diagnostic
for the closing result, not as a resolved biological classifier.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from build_fig5_nomenclature_weights import (
    FIGURE_DIR,
    RESULTS_DIR,
    build_profiles,
    group_gene_scores,
)


DEFAULT_MEMBERSHIP = RESULTS_DIR / "tcell_marker_cluster_membership.tsv"
DEFAULT_CLUSTER_SUMMARY = RESULTS_DIR / "tcell_marker_cluster_summary.tsv"
DEFAULT_CLUSTER_TABLE = RESULTS_DIR / "tcell_gene_f1_ratio_by_cluster.tsv"
DEFAULT_GENE_SUMMARY = RESULTS_DIR / "tcell_gene_f1_ratio_gene_summary.tsv"
DEFAULT_FIGURE = FIGURE_DIR / "fig_tcell_gene_f1_ratio.pdf"
DEFAULT_FIGURE_PNG = FIGURE_DIR / "fig_tcell_gene_f1_ratio.png"

PSEUDOCOUNT = 0.02


def membership_uid(row: pd.Series) -> str:
    source_corpus = str(row["source_corpus"])
    paper_id = str(row["paper_id"])
    cell_type = str(row["cell_type"])
    return f"{source_corpus}|{paper_id}|{cell_type}"


def ratio(marker_f1: float, label_f1: float) -> float:
    if label_f1 == 0:
        return math.inf if marker_f1 > 0 else 1.0
    return marker_f1 / label_f1


def log2_ratio(marker_f1: float, label_f1: float, pseudocount: float = PSEUDOCOUNT) -> float:
    return math.log2((marker_f1 + pseudocount) / (label_f1 + pseudocount))


def classify_shift(marker_f1: float, label_f1: float) -> str:
    if marker_f1 >= 0.25 and label_f1 >= 0.25:
        return "high in both"
    if marker_f1 >= 0.12 and marker_f1 >= label_f1 * 1.5:
        return "marker-cluster enriched"
    if label_f1 >= 0.12 and label_f1 >= marker_f1 * 1.5:
        return "label enriched"
    return "weak or similar"


def build_label_gene_reference(
    profiles_df: pd.DataFrame,
    tcell_profile_indices: set[int],
    id_to_name: dict[str, str],
    *,
    min_label_profiles: int,
) -> pd.DataFrame:
    """Best exact-label F1 for each gene among repeated T-cell labels."""
    tcell_df = profiles_df.loc[profiles_df["profile_idx"].isin(tcell_profile_indices)].copy()
    label_counts = tcell_df["normalized_cell_type"].value_counts()
    eligible_labels = label_counts.loc[label_counts >= min_label_profiles].index.tolist()

    label_tables = []
    for label in eligible_labels:
        label_profile_indices = set(
            profiles_df.loc[profiles_df["normalized_cell_type"].eq(label), "profile_idx"].astype(int)
        )
        scores_df = group_gene_scores(
            profiles_df,
            label_profile_indices,
            id_to_name,
            f"label {label}",
        )
        if scores_df.empty:
            continue
        scores_df["label_group"] = label
        label_tables.append(scores_df)

    if not label_tables:
        return pd.DataFrame(
            columns=[
                "gene_id",
                "gene_name",
                "best_label_group",
                "best_label_f1",
                "best_label_coverage",
                "best_label_purity",
                "best_label_n_profiles",
            ]
        )

    all_scores = pd.concat(label_tables, ignore_index=True)
    best_rows = (
        all_scores.sort_values(
            ["coverage_purity_hmean", "coverage", "purity", "n_profiles_group"],
            ascending=[False, False, False, False],
        )
        .drop_duplicates("gene_id")
        .rename(
            columns={
                "label_group": "best_label_group",
                "coverage_purity_hmean": "best_label_f1",
                "coverage": "best_label_coverage",
                "purity": "best_label_purity",
                "n_profiles_group": "best_label_n_profiles",
            }
        )
    )
    return best_rows[
        [
            "gene_id",
            "gene_name",
            "best_label_group",
            "best_label_f1",
            "best_label_coverage",
            "best_label_purity",
            "best_label_n_profiles",
        ]
    ]


def build_cluster_gene_table(
    profiles_df: pd.DataFrame,
    id_to_name: dict[str, str],
    membership_df: pd.DataFrame,
    cluster_summary_df: pd.DataFrame,
    label_reference_df: pd.DataFrame,
) -> pd.DataFrame:
    uid_to_profile_idx = profiles_df.set_index("profile_uid")["profile_idx"].astype(int).to_dict()
    membership_df = membership_df.copy()
    membership_df["profile_uid"] = membership_df.apply(membership_uid, axis=1)
    membership_df["global_profile_idx"] = membership_df["profile_uid"].map(uid_to_profile_idx)
    membership_df = membership_df.dropna(subset=["global_profile_idx"])
    membership_df["global_profile_idx"] = membership_df["global_profile_idx"].astype(int)

    label_reference = label_reference_df.set_index("gene_id").to_dict("index") if not label_reference_df.empty else {}
    summary_by_component = cluster_summary_df.set_index("component").to_dict("index")

    rows = []
    for component, component_df in membership_df.groupby("component", sort=True):
        profile_indices = set(component_df["global_profile_idx"].astype(int))
        marker_scores = group_gene_scores(
            profiles_df,
            profile_indices,
            id_to_name,
            f"T-cell marker cluster C{component}",
        )
        if marker_scores.empty:
            continue
        summary = summary_by_component.get(component, {})
        for row in marker_scores.itertuples(index=False):
            label_ref = label_reference.get(row.gene_id, {})
            best_label_f1 = float(label_ref.get("best_label_f1", 0.0) or 0.0)
            marker_f1 = float(row.coverage_purity_hmean)
            rows.append(
                {
                    "component": int(component),
                    "dominant_program": summary.get("dominant_program"),
                    "n_profiles_cluster": int(row.n_profiles_group),
                    "n_papers_cluster": summary.get("papers"),
                    "n_labels_cluster": summary.get("labels"),
                    "top_labels": summary.get("top_labels"),
                    "core_marker_genes": summary.get("core_marker_genes"),
                    "gene_id": row.gene_id,
                    "gene_name": row.gene_name,
                    "marker_cluster_f1": marker_f1,
                    "marker_cluster_coverage": row.coverage,
                    "marker_cluster_purity": row.purity,
                    "marker_cluster_gene_count": int(row.n_profiles_with_gene_in_group),
                    "global_gene_count": int(row.n_profiles_with_gene_global),
                    "best_label_f1": best_label_f1,
                    "best_label_group": label_ref.get("best_label_group"),
                    "best_label_coverage": label_ref.get("best_label_coverage", 0.0),
                    "best_label_purity": label_ref.get("best_label_purity", 0.0),
                    "best_label_n_profiles": label_ref.get("best_label_n_profiles", 0),
                    "marker_to_label_f1_ratio": ratio(marker_f1, best_label_f1),
                    "log2_marker_to_label_f1_ratio": log2_ratio(marker_f1, best_label_f1),
                    "shift_class": classify_shift(marker_f1, best_label_f1),
                }
            )
    return pd.DataFrame(rows).sort_values(
        ["component", "log2_marker_to_label_f1_ratio", "marker_cluster_f1"],
        ascending=[True, False, False],
    )


def build_gene_summary(cluster_table_df: pd.DataFrame) -> pd.DataFrame:
    if cluster_table_df.empty:
        return pd.DataFrame()
    return (
        cluster_table_df.sort_values(
            ["marker_cluster_f1", "log2_marker_to_label_f1_ratio"],
            ascending=[False, False],
        )
        .drop_duplicates("gene_id")
        .sort_values(["log2_marker_to_label_f1_ratio", "marker_cluster_f1"], ascending=[False, False])
        .reset_index(drop=True)
    )


def annotate_points(ax: plt.Axes, plot_df: pd.DataFrame) -> None:
    label_df = pd.concat(
        [
            plot_df.sort_values("log2_marker_to_label_f1_ratio", ascending=False).head(6),
            plot_df.sort_values("marker_cluster_f1", ascending=False).head(6),
            plot_df.sort_values("log2_marker_to_label_f1_ratio", ascending=True).head(4),
        ],
        ignore_index=True,
    ).drop_duplicates("gene_id")
    for idx, row in enumerate(label_df.itertuples(index=False)):
        y_offset = 4 if idx % 2 == 0 else -7
        ax.annotate(
            row.gene_name,
            (row.best_label_f1, row.marker_cluster_f1),
            xytext=(5, y_offset),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=6,
            arrowprops={"arrowstyle": "-", "linewidth": 0.25, "color": "#777777"},
        )


def make_figure(gene_summary_df: pd.DataFrame, cluster_table_df: pd.DataFrame, figure_path: Path, figure_png_path: Path) -> None:
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw={"width_ratios": [1.0, 1.18]})

    ax = axes[0]
    colors = {
        "marker-cluster enriched": "#7fbf7b",
        "label enriched": "#ef8a62",
        "high in both": "#67a9cf",
        "weak or similar": "#d9d9d9",
    }
    for shift_class, group_df in gene_summary_df.groupby("shift_class", sort=False):
        ax.scatter(
            group_df["best_label_f1"],
            group_df["marker_cluster_f1"],
            s=22,
            color=colors.get(shift_class, "#d9d9d9"),
            edgecolor="#222222",
            linewidth=0.35,
            alpha=0.9,
            label=shift_class,
        )
    ax.plot([0, 1], [0, 1], color="#777777", linewidth=0.7, linestyle="--")
    ax.set_xlim(-0.03, 1.03)
    ax.set_ylim(-0.03, 1.03)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("Best F1 in repeated T-cell label")
    ax.set_ylabel("Best F1 in T-cell marker cluster")
    ax.spines[["top", "right"]].set_visible(False)
    annotate_points(ax, gene_summary_df)

    ax = axes[1]
    top_clusters = []
    for component, group_df in cluster_table_df.groupby("component", sort=True):
        top = group_df.sort_values(["log2_marker_to_label_f1_ratio", "marker_cluster_f1"], ascending=[False, False]).head(4)
        for row in top.itertuples(index=False):
            top_clusters.append(
                {
                    "component": component,
                    "label": f"C{component}: {row.gene_name}",
                    "value": row.log2_marker_to_label_f1_ratio,
                    "program": row.dominant_program,
                }
            )
    bar_df = pd.DataFrame(top_clusters)
    if not bar_df.empty:
        bar_df = bar_df.sort_values(["component", "value"], ascending=[True, True]).reset_index(drop=True)
        y = np.arange(len(bar_df))
        ax.barh(y, bar_df["value"], color="#bdbdbd", edgecolor="#222222", linewidth=0.4)
        ax.axvline(0, color="#777777", linewidth=0.7)
        ax.set_yticks(y)
        ax.set_yticklabels(bar_df["label"], fontsize=6)
        ax.set_xlabel("log2((marker F1 + 0.02) / (label F1 + 0.02))")
        ax.spines[["top", "right"]].set_visible(False)
    else:
        ax.axis("off")

    handles, labels = axes[0].get_legend_handles_labels()
    axes[0].legend(handles, labels, frameon=False, fontsize=6, loc="lower right")
    fig.tight_layout()
    fig.savefig(figure_path, bbox_inches="tight")
    fig.savefig(figure_png_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--membership", type=Path, default=DEFAULT_MEMBERSHIP)
    parser.add_argument("--cluster-summary", type=Path, default=DEFAULT_CLUSTER_SUMMARY)
    parser.add_argument("--cluster-table-out", type=Path, default=DEFAULT_CLUSTER_TABLE)
    parser.add_argument("--gene-summary-out", type=Path, default=DEFAULT_GENE_SUMMARY)
    parser.add_argument("--figure-out", type=Path, default=DEFAULT_FIGURE)
    parser.add_argument("--figure-png-out", type=Path, default=DEFAULT_FIGURE_PNG)
    parser.add_argument("--min-label-profiles", type=int, default=3)
    args = parser.parse_args()

    profiles_df, id_to_name = build_profiles()
    membership_df = pd.read_csv(args.membership, sep="\t")
    cluster_summary_df = pd.read_csv(args.cluster_summary, sep="\t")
    uid_to_profile_idx = profiles_df.set_index("profile_uid")["profile_idx"].astype(int).to_dict()
    membership_df = membership_df.copy()
    membership_df["profile_uid"] = membership_df.apply(membership_uid, axis=1)
    tcell_profile_indices = set(membership_df["profile_uid"].map(uid_to_profile_idx).dropna().astype(int))

    label_reference_df = build_label_gene_reference(
        profiles_df,
        tcell_profile_indices,
        id_to_name,
        min_label_profiles=args.min_label_profiles,
    )
    cluster_table_df = build_cluster_gene_table(
        profiles_df,
        id_to_name,
        membership_df,
        cluster_summary_df,
        label_reference_df,
    )
    gene_summary_df = build_gene_summary(cluster_table_df)

    args.cluster_table_out.parent.mkdir(parents=True, exist_ok=True)
    cluster_table_df.to_csv(args.cluster_table_out, sep="\t", index=False)
    gene_summary_df.to_csv(args.gene_summary_out, sep="\t", index=False)
    make_figure(gene_summary_df, cluster_table_df, args.figure_out, args.figure_png_out)

    print(f"T-cell profiles in displayed marker clusters: {len(tcell_profile_indices)}")
    print(f"Repeated T-cell label groups used: {label_reference_df['best_label_group'].nunique() if not label_reference_df.empty else 0}")
    print(f"Cluster-gene rows: {len(cluster_table_df)}")
    print(f"Genes summarized: {len(gene_summary_df)}")
    print(cluster_table_df.groupby(["component", "shift_class"]).size().unstack(fill_value=0).to_string())
    print(f"Wrote {args.cluster_table_out}")
    print(f"Wrote {args.gene_summary_out}")
    print(f"Wrote {args.figure_out}")


if __name__ == "__main__":
    main()
