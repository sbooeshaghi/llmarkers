"""Build Figure 3 (corpus reuse) from committed corpus-analysis artifacts.

Panels:
  A. Identifier mapping rates (genes vs cell type labels) and the label-collapse
     example ("T cell" variants onto CL:0000084).
  B. Panel pairs sharing at least one marker, by label/identifier relation.
  C. Marker-panel Jaccard vs co-reported-label Jaccard (log-density hexbin + fit).
  D. Shared-marker retention as papers accumulate, labels vs ontology identifiers.

Reads only artifacts under analysis/artifacts/mrkr_corpus_analysis_v1/, so the
figure can be regenerated without rerunning analyze_mrkr_corpus.py.
"""
from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/llmarkers-matplotlib")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch

REPO_ROOT = Path(__file__).resolve().parents[1]
ART = REPO_ROOT / "analysis" / "artifacts" / "mrkr_corpus_analysis_v1"
FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

BLUE = "#4C78A8"
LIGHT_BLUE = "#A7C7E7"
GRAYS = LinearSegmentedColormap.from_list("grays", ["#FFFFFF", "#2B2B2B"])


def mapping_numbers() -> dict:
    coverage = pd.read_csv(ART / "term_coverage.tsv", sep="\t").set_index("term_type")
    audit = pd.read_csv(ART / "cell_ontology_label_audit.tsv", sep="\t")
    celltype = audit[audit["term_type"] == "celltype"]
    accepted = celltype[celltype["semantic_exact"] == 1]
    return {
        "genes_total": int(coverage.loc["gene", "terms"]),
        "genes_mapped": int(coverage.loc["gene", "grounded"]),
        "ct_total": int(len(celltype)),
        "ct_canonical": int((accepted["match_source"] == "canonical").sum()),
        "ct_synonym": int((accepted["match_source"] == "exact_synonym").sum()),
        "accepted_labels": int(len(accepted)),
        "accepted_identifiers": int(accepted["curie"].nunique()),
    }


def draw_mapping(ax: plt.Axes, numbers: dict) -> None:
    rows = [
        (
            f"Marker genes\n(n={numbers['genes_total']:,})",
            [(numbers["genes_mapped"] / numbers["genes_total"], BLUE)],
        ),
        (
            f"Cell type labels\n(n={numbers['ct_total']:,})",
            [
                (numbers["ct_canonical"] / numbers["ct_total"], BLUE),
                (numbers["ct_synonym"] / numbers["ct_total"], LIGHT_BLUE),
            ],
        ),
    ]
    for i, (label, segments) in enumerate(rows):
        left = 0.0
        for frac, color in segments:
            ax.barh(i, frac, left=left, height=0.58, facecolor=color, edgecolor="black", linewidth=0.55)
            left += frac
        ax.barh(i, 1.0 - left, left=left, height=0.58, facecolor="white", edgecolor="black", linewidth=0.55)
        if left > 0.85:
            ax.text(left - 0.02, i, f"{left:.0%}", va="center", ha="right", fontsize=7.2, color="white")
        else:
            ax.text(left + 0.02, i, f"{left:.0%}", va="center", fontsize=7.2)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([r[0] for r in rows], fontsize=7.2)
    ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.0)
    ax.set_xticks([0, 0.5, 1.0])
    ax.set_xticklabels(["0", "0.5", "1.0"], fontsize=7.2)
    ax.set_xlabel("Fraction mapped to a stable identifier", fontsize=7.6)
    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=c, edgecolor="black", linewidth=0.55)
        for c in [BLUE, LIGHT_BLUE, "white"]
    ]
    ax.legend(handles, ["Canonical", "Exact synonym", "Unmapped"], frameon=False, fontsize=6.4,
              loc="upper center", bbox_to_anchor=(0.5, 1.45), ncol=3, columnspacing=0.8, handlelength=1.1)


def draw_collapse(ax: plt.Axes, numbers: dict) -> None:
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    labels = ['"T cell"', '"T-cell"', '"T lymphocyte"', '"T-lymphocyte"']
    y_positions = [0.88, 0.66, 0.44, 0.22]
    for label, y in zip(labels, y_positions):
        box = FancyBboxPatch((0.02, y - 0.075), 0.34, 0.17,
                             boxstyle="round,pad=0.012,rounding_size=0.02",
                             facecolor="#F4F4F4", edgecolor="black", linewidth=0.55)
        ax.add_patch(box)
        ax.text(0.19, y, label, ha="center", va="center", fontsize=6.6)
        ax.annotate("", xy=(0.60, 0.55), xytext=(0.375, y),
                    arrowprops={"arrowstyle": "-", "color": "#9A9A9A", "linewidth": 0.7})
    id_box = FancyBboxPatch((0.62, 0.44), 0.34, 0.22,
                            boxstyle="round,pad=0.012,rounding_size=0.02",
                            facecolor="#E8EEF6", edgecolor=BLUE, linewidth=0.9)
    ax.add_patch(id_box)
    ax.text(0.79, 0.585, "CL:0000084", ha="center", va="center", fontsize=6.8, family="monospace")
    ax.text(0.79, 0.495, "T cell", ha="center", va="center", fontsize=6.6)
    ax.annotate("", xy=(0.615, 0.55), xytext=(0.60, 0.55),
                arrowprops={"arrowstyle": "-|>", "color": "#9A9A9A", "linewidth": 0.7})


def draw_sharing(ax: plt.Axes) -> None:
    df = pd.read_csv(ART / "identifier_recovered_matched_summary.tsv", sep="\t")
    df = df[df["metric"] == "any_shared_marker"].set_index("comparison")
    bars = [
        ("same_identifier_different_label", "Different labels,\nsame identifier\n(n=248)", BLUE),
        ("same_label_same_identifier", "Same label,\nsame identifier\n(n=8,848)", "white"),
        ("same_label_no_accepted_identifier", "Same label,\nno accepted identifier\n(n=1,589)", "white"),
        ("different_identifier_matched_control", "Different identifiers,\nmatched control", "#D9D9D9"),
    ]
    for i, (key, label, color) in enumerate(bars):
        row = df.loc[key]
        ax.barh(i, row["estimate"], height=0.62, facecolor=color, edgecolor="black", linewidth=0.7, zorder=2)
        ax.hlines(i, row["uncertainty_95_lower"], row["uncertainty_95_upper"], color="black", linewidth=0.8, zorder=3)
        for bound in ("uncertainty_95_lower", "uncertainty_95_upper"):
            ax.vlines(row[bound], i - 0.11, i + 0.11, color="black", linewidth=0.8, zorder=3)
    ax.set_yticks(range(len(bars)))
    ax.set_yticklabels([label for _, label, _ in bars], fontsize=6.8)
    ax.invert_yaxis()
    ax.set_xlabel("Panel pairs sharing at least one marker", fontsize=8)
    ax.set_xlim(0, 1.0)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", labelsize=7.2)


def draw_context(fig: plt.Figure, ax: plt.Axes) -> None:
    pairs = pd.read_csv(ART / "same_label_pairs.tsv", sep="\t",
                        usecols=["context_jaccard", "marker_jaccard"]).dropna()
    fit = pd.read_csv(ART / "coreported_context_fit.tsv", sep="\t")
    pearson = float(np.corrcoef(pairs["context_jaccard"], pairs["marker_jaccard"])[0, 1])
    hb = ax.hexbin(pairs["context_jaccard"], pairs["marker_jaccard"], gridsize=34,
                   bins="log", cmap=GRAYS, linewidths=0.1, extent=(0, 1, 0, 1), mincnt=1)
    ax.fill_between(fit["context_jaccard"], fit["label_cluster_bootstrap_95_lower"],
                    fit["label_cluster_bootstrap_95_upper"], color=BLUE, alpha=0.25,
                    linewidth=0, zorder=3)
    ax.plot(fit["context_jaccard"], fit["fitted_marker_jaccard"], color=BLUE, linewidth=1.6, zorder=4)
    ax.text(0.97, 0.93, f"Pearson r = {pearson:.3f}", transform=ax.transAxes, ha="right", fontsize=7.4)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Co-reported-label Jaccard", fontsize=8)
    ax.set_ylabel("Marker-panel Jaccard", fontsize=8)
    ax.tick_params(axis="both", labelsize=7.2)
    cbar = fig.colorbar(hb, ax=ax, shrink=0.75, pad=0.02, aspect=24)
    cbar.set_label("Panel pairs", fontsize=7.0)
    cbar.ax.tick_params(labelsize=6.2)
    cbar.outline.set_linewidth(0.55)


def draw_decay(ax: plt.Axes) -> None:
    labels = pd.read_csv(ART / "label_intersection_accumulation.tsv", sep="\t")
    onto = pd.read_csv(ART / "ontology_intersection_accumulation.tsv", sep="\t")
    ax.fill_between(labels["papers_combined"], labels["uncertainty_95_lower"],
                    labels["uncertainty_95_upper"], color=BLUE, alpha=0.18, linewidth=0)
    ax.plot(labels["papers_combined"], labels["estimate"], color=BLUE, linewidth=1.7, zorder=3,
            label="Normalized labels (37)")
    ax.scatter(labels["papers_combined"], labels["estimate"], s=18, facecolor="white",
               edgecolor=BLUE, linewidth=0.9, zorder=4)
    ax.plot(onto["papers_combined"], onto["estimate"], color="#555555", linewidth=1.2,
            linestyle=(0, (3, 2)), zorder=2, label="Cell Ontology identifiers (27)")
    ax.set_xlim(1, 10)
    ax.set_ylim(0, 1.0)
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("Papers combined per label", fontsize=8)
    ax.set_ylabel("Fraction of labels retaining\na shared marker", fontsize=8)
    ax.tick_params(axis="both", labelsize=7.2)
    ax.legend(frameon=False, fontsize=6.6, loc="upper right", handlelength=1.8)


def main() -> None:
    plt.rcParams.update(
        {
            "font.size": 8,
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    numbers = mapping_numbers()
    fig = plt.figure(figsize=(7.6, 6.2))
    outer = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.50, width_ratios=[1.0, 0.82],
                             left=0.13, right=0.95, top=0.93, bottom=0.08)
    panel_a = outer[0, 0].subgridspec(2, 1, height_ratios=[1.0, 1.3], hspace=0.55)
    ax_map = fig.add_subplot(panel_a[0])
    ax_collapse = fig.add_subplot(panel_a[1])
    ax_sharing = fig.add_subplot(outer[0, 1])
    ax_context = fig.add_subplot(outer[1, 0])
    ax_decay = fig.add_subplot(outer[1, 1])

    draw_mapping(ax_map, numbers)
    draw_collapse(ax_collapse, numbers)
    draw_sharing(ax_sharing)
    draw_context(fig, ax_context)
    draw_decay(ax_decay)

    for ax, letter in [(ax_map, "A"), (ax_sharing, "B"), (ax_context, "C"), (ax_decay, "D")]:
        pos = ax.get_position()
        fig.text(pos.x0 - 0.105, pos.y1 + 0.015, letter, fontsize=11, fontweight="bold")

    fig.savefig(FIGURE_DIR / "fig3_corpus_reuse_v2.pdf", bbox_inches="tight")
    fig.savefig(FIGURE_DIR / "fig3_corpus_reuse_v2.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {FIGURE_DIR / 'fig3_corpus_reuse_v2.pdf'}")
    print("mapping numbers:", numbers)


if __name__ == "__main__":
    main()
