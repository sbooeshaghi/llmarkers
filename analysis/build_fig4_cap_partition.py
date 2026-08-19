"""Build Figure 4 (CAP liver comparison-group analysis) from committed artifacts.

Panels:
  A. Per myeloid cell type: Jaccard of the two analyses' top 100 DEGs (marginal)
     and recovery of reported markers in each analysis (butterfly).
  B. Mean recovery for the myeloid analysis and the all-cell analysis with target
     groups defined by the study's labels or by the exact myeloid barcodes.

Reads only artifacts under analysis/artifacts/, so the figure can be regenerated
without rerunning the differential-expression producers.
"""
from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/llmarkers-matplotlib")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
ART = REPO_ROOT / "analysis" / "artifacts"
FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

BLUE = "#4C78A8"


def main() -> None:
    plt.rcParams.update(
        {
            "font.size": 8,
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    summary = pd.read_csv(ART / "cap_liver_local_global_deg_summary.tsv", sep="\t")
    intervals = pd.read_csv(ART / "cap_liver_local_global_recovery_subsampling_summary.tsv", sep="\t")
    control = pd.read_csv(ART / "cap_liver_barcode_constant_recovery.tsv", sep="\t")
    lookup = intervals.set_index(["local_label", "context"])
    ordered = summary.sort_values("global_label").reset_index(drop=True)
    display = [f"{r.local_label}\n({r.global_label})" for r in ordered.itertuples(index=False)]
    y = np.arange(len(ordered))

    fig = plt.figure(figsize=(9.2, 3.45))
    gs = fig.add_gridspec(1, 3, width_ratios=[0.26, 0.86, 0.48], wspace=0.32,
                          left=0.15, right=0.98, top=0.95, bottom=0.20)
    axj = fig.add_subplot(gs[0])
    axb = fig.add_subplot(gs[1], sharey=axj)
    axc = fig.add_subplot(gs[2])

    # A marginal: rank overlap
    axj.barh(y, ordered["local_top100_vs_global_top100_jaccard"], height=0.62,
             facecolor="#D9D9D9", edgecolor="black", linewidth=0.55)
    axj.set_yticks(y)
    axj.set_yticklabels(display, fontsize=6.4)
    axj.tick_params(axis="y", length=0)
    axj.invert_yaxis()
    axj.set_xlim(0, 1.0)
    axj.set_xticks([0, 0.5, 1.0])
    axj.set_xticklabels(["0", "0.5", "1.0"], fontsize=7.0)
    axj.set_xlabel("Jaccard of\ntop 100 DEGs", fontsize=7.4)

    # A butterfly: recovery per analysis
    for i, r in enumerate(ordered.itertuples(index=False)):
        axb.barh(i, -r.local_reported_recovery_top100, height=0.62, facecolor=BLUE,
                 edgecolor="black", linewidth=0.55)
        axb.barh(i, r.global_recovery_of_local_reported_top100, height=0.62, facecolor="white",
                 edgecolor="black", linewidth=0.55)
        for context, sign in [("local", -1), ("global", 1)]:
            key = (r.local_label, context)
            if key not in lookup.index:
                continue
            row = lookup.loc[key]
            low, high = sign * float(row["q025"]), sign * float(row["q975"])
            axb.hlines(i, low, high, color="black", linewidth=0.7, zorder=5)
            axb.vlines([low, high], i - 0.14, i + 0.14, color="black", linewidth=0.7, zorder=5)
    axb.axvline(0, color="black", linewidth=0.8)
    axb.set_xlim(-1.0, 1.0)
    axb.set_xticks([-1, -0.5, 0, 0.5, 1])
    axb.set_xticklabels(["1.0", "0.5", "0", "0.5", "1.0"], fontsize=7.0)
    axb.spines["left"].set_visible(False)
    axb.tick_params(axis="y", length=0, labelleft=False)
    axb.text(-0.5, -0.125, "Myeloid DE", transform=axb.get_xaxis_transform(),
             ha="center", va="top", fontsize=7.8)
    axb.text(0.5, -0.125, "All-cell DE", transform=axb.get_xaxis_transform(),
             ha="center", va="top", fontsize=7.8)
    axb.text(0, -0.205, "Fraction of reported markers recovered in top 100 DEGs",
             transform=axb.get_xaxis_transform(), ha="center", va="top", fontsize=7.8)

    # B: barcode-constant control
    columns = [
        ("recovery_top100_local", "Myeloid DE", BLUE),
        ("recovery_top100_global_label_based", "All-cell DE\n(labels)", "white"),
        ("recovery_top100_barcode_constant", "All-cell DE\n(barcodes)", "#D9D9D9"),
    ]
    jitter = np.linspace(-0.13, 0.13, len(control))
    for i, (col, label, color) in enumerate(columns):
        values = control[col].to_numpy()
        axc.bar(i, values.mean(), width=0.58, facecolor=color,
                alpha=0.55 if color == BLUE else 1.0, edgecolor="black", linewidth=0.7, zorder=2)
        axc.scatter(np.full(len(values), i) + jitter, values, s=24,
                    color=BLUE if color == BLUE else ("white" if color == "white" else "#8A8A8A"),
                    edgecolor="black", linewidth=0.5, zorder=3)
    axc.set_xticks(range(len(columns)))
    axc.set_xticklabels([label for _, label, _ in columns], fontsize=6.6)
    axc.set_ylabel("Fraction of reported markers\nrecovered in top 100 DEGs", fontsize=7.8)
    axc.set_ylim(0, 1.05)
    axc.set_xlim(-0.55, len(columns) - 0.45)
    axc.tick_params(axis="x", length=0)
    axc.tick_params(axis="y", labelsize=7.0)

    pos_a = axj.get_position()
    pos_c = axc.get_position()
    fig.text(pos_a.x0 - 0.115, pos_a.y1 + 0.015, "A", fontsize=11, fontweight="bold")
    fig.text(pos_c.x0 - 0.055, pos_c.y1 + 0.015, "B", fontsize=11, fontweight="bold")

    fig.savefig(FIGURE_DIR / "fig4_cap_partition_v2.pdf", bbox_inches="tight")
    fig.savefig(FIGURE_DIR / "fig4_cap_partition_v2.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {FIGURE_DIR / 'fig4_cap_partition_v2.pdf'}")


if __name__ == "__main__":
    main()
