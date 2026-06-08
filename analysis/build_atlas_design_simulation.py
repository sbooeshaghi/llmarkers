#!/usr/bin/env python3
"""Simulate atlas-scale marker-design constraints.

This script is deliberately simple. It separates three quantities:

1. Cell-type pair coverage.
2. Tissue/admissibility constraints on which pairs need to be compared.
3. Marker-gene sufficiency under a random pairwise-difference model.

The simulation does not try to estimate real biological cell-type ontologies.
It asks how the formal bounds behave under plausible organism-scale sizes and
toy tissue-membership assumptions.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from math import ceil, comb, log, log2
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/llmarkers-mpl")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


RESULTS_DIR = Path("analysis/results")
FIGURE_DIR = Path("analysis/figures")

R_VALUES = [10, 20, 50, 100]
Q_VALUES = [0.5, 0.1, 0.02]
DELTA = 0.05
N_REPS = 25
RNG_SEED = 20260603


@dataclass(frozen=True)
class Scenario:
    scope: str
    k_cell_types: int
    protein_coding_genes: int
    n_tissues: int
    shared_fraction: float
    extra_tissues_mean: float
    tissue_dirichlet_alpha: float
    note: str


SCENARIOS = [
    Scenario(
        scope="C. elegans adult",
        k_cell_types=146,
        protein_coding_genes=20000,
        n_tissues=12,
        shared_fraction=0.08,
        extra_tissues_mean=2.0,
        tissue_dirichlet_alpha=2.0,
        note="small organism, modest tissue constraint",
    ),
    Scenario(
        scope="Drosophila adult",
        k_cell_types=250,
        protein_coding_genes=13900,
        n_tissues=20,
        shared_fraction=0.10,
        extra_tissues_mean=2.5,
        tissue_dirichlet_alpha=1.5,
        note="whole adult atlas scale",
    ),
    Scenario(
        scope="Human major cell types",
        k_cell_types=400,
        protein_coding_genes=20000,
        n_tissues=45,
        shared_fraction=0.15,
        extra_tissues_mean=4.0,
        tissue_dirichlet_alpha=1.2,
        note="major cell-type estimate, many shared immune/stromal types",
    ),
    Scenario(
        scope="Human fine cell types",
        k_cell_types=3358,
        protein_coding_genes=20000,
        n_tissues=70,
        shared_fraction=0.08,
        extra_tissues_mean=5.0,
        tissue_dirichlet_alpha=0.9,
        note="fine cell-type estimate, tissue-constrained comparisons",
    ),
    Scenario(
        scope="Mouse brain major types",
        k_cell_types=300,
        protein_coding_genes=22000,
        n_tissues=25,
        shared_fraction=0.12,
        extra_tissues_mean=3.0,
        tissue_dirichlet_alpha=1.4,
        note="brain regions as admissibility contexts",
    ),
    Scenario(
        scope="Mouse brain clusters",
        k_cell_types=5322,
        protein_coding_genes=22000,
        n_tissues=80,
        shared_fraction=0.06,
        extra_tissues_mean=4.0,
        tissue_dirichlet_alpha=0.8,
        note="whole-brain transcriptomic-cluster scale",
    ),
]


def choose2(n: int) -> int:
    if n < 2:
        return 0
    return comb(n, 2)


def binary_lower_bound(k: int) -> int:
    if k <= 1:
        return 0
    return ceil(log2(k))


def random_panel_sufficient_bound(n_edges: int, q: float, delta: float = DELTA) -> int:
    """Union-bound sufficient size for a random marker panel.

    If a random gene separates any fixed admissible pair with probability q,
    then m genes fail on that pair with probability (1-q)^m. Union bounding over
    n_edges gives n_edges * (1-q)^m <= delta.
    """
    if n_edges <= 0:
        return 0
    if q <= 0 or q >= 1:
        raise ValueError("q must satisfy 0 < q < 1")
    return ceil((log(delta) - log(n_edges)) / log(1.0 - q))


def simulate_tissue_memberships(s: Scenario, rng: np.random.Generator) -> list[np.ndarray]:
    """Return cell-type IDs present in each tissue/admissibility context."""
    k = s.k_cell_types
    t = s.n_tissues
    tissue_prob = rng.dirichlet(np.full(t, s.tissue_dirichlet_alpha))
    primary = rng.choice(t, size=k, p=tissue_prob)

    memberships: list[set[int]] = [set() for _ in range(t)]
    for cell_id, tissue_id in enumerate(primary):
        memberships[int(tissue_id)].add(cell_id)

    n_shared = int(round(k * s.shared_fraction))
    shared_cells = rng.choice(k, size=n_shared, replace=False) if n_shared > 0 else np.array([], dtype=int)
    for cell_id in shared_cells:
        n_extra = int(max(1, rng.poisson(s.extra_tissues_mean)))
        n_extra = min(n_extra, max(0, t - 1))
        current = primary[cell_id]
        choices = np.array([idx for idx in range(t) if idx != current])
        if n_extra > 0:
            for tissue_id in rng.choice(choices, size=n_extra, replace=False):
                memberships[int(tissue_id)].add(int(cell_id))

    return [np.fromiter(sorted(m), dtype=np.int32) for m in memberships if len(m) > 1]


def edge_count_from_memberships(k: int, memberships: list[np.ndarray]) -> int:
    """Count unique admissible cell-type pairs induced by tissue memberships."""
    edges: set[int] = set()
    for cells in memberships:
        if cells.size < 2:
            continue
        ii, jj = np.triu_indices(cells.size, k=1)
        u = cells[ii].astype(np.int64)
        v = cells[jj].astype(np.int64)
        keys = u * k + v
        edges.update(keys.tolist())
    return len(edges)


def experiment_lower_bound(n_edges: int, max_edges_per_experiment: int) -> int:
    if n_edges <= 0:
        return 0
    if max_edges_per_experiment <= 0:
        return 0
    return ceil(n_edges / max_edges_per_experiment)


def summarize_replicate(s: Scenario, rep: int, rng: np.random.Generator) -> dict[str, object]:
    memberships = simulate_tissue_memberships(s, rng)
    tissue_sizes = [int(x.size) for x in memberships]
    max_tissue_size = max(tissue_sizes)
    median_tissue_size = float(np.median(tissue_sizes))
    admissible_edges = edge_count_from_memberships(s.k_cell_types, memberships)
    complete_edges = choose2(s.k_cell_types)

    row: dict[str, object] = {
        "scope": s.scope,
        "replicate": rep,
        "k_cell_types": s.k_cell_types,
        "protein_coding_genes": s.protein_coding_genes,
        "n_tissues": s.n_tissues,
        "n_nonempty_contexts": len(memberships),
        "max_tissue_cell_types": max_tissue_size,
        "median_tissue_cell_types": median_tissue_size,
        "complete_edges": complete_edges,
        "admissible_edges": admissible_edges,
        "admissible_edge_fraction": admissible_edges / complete_edges,
        "binary_lower_complete": binary_lower_bound(s.k_cell_types),
        "binary_lower_admissible_clique": binary_lower_bound(max_tissue_size),
        "note": s.note,
    }

    for r in R_VALUES:
        row[f"complete_experiment_lower_r{r}"] = experiment_lower_bound(complete_edges, choose2(min(r, s.k_cell_types)))
        max_edges = max(choose2(min(r, size)) for size in tissue_sizes)
        row[f"admissible_experiment_lower_r{r}"] = experiment_lower_bound(admissible_edges, max_edges)
        row[f"per_context_lower_sum_r{r}"] = sum(
            experiment_lower_bound(choose2(size), choose2(min(r, size))) for size in tissue_sizes
        )

    for q in Q_VALUES:
        row[f"random_panel_sufficient_complete_q{q:g}"] = random_panel_sufficient_bound(complete_edges, q)
        row[f"random_panel_sufficient_admissible_q{q:g}"] = random_panel_sufficient_bound(admissible_edges, q)
    return row


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    metric_cols = [
        col
        for col in df.columns
        if col
        not in {
            "scope",
            "replicate",
            "note",
        }
    ]
    grouped = df.groupby("scope", sort=False)
    rows = []
    for scope, sub in grouped:
        out: dict[str, object] = {"scope": scope, "n_replicates": len(sub)}
        for col in metric_cols:
            if pd.api.types.is_numeric_dtype(sub[col]):
                out[f"{col}_median"] = sub[col].median()
                out[f"{col}_p10"] = sub[col].quantile(0.10)
                out[f"{col}_p90"] = sub[col].quantile(0.90)
            else:
                out[col] = sub[col].iloc[0]
        rows.append(out)
    return pd.DataFrame(rows)


def write_markdown(summary: pd.DataFrame, path: Path) -> None:
    display_cols = [
        "scope",
        "k_cell_types_median",
        "n_tissues_median",
        "max_tissue_cell_types_median",
        "admissible_edges_median",
        "admissible_edge_fraction_median",
        "admissible_experiment_lower_r20_median",
        "admissible_experiment_lower_r50_median",
        "complete_experiment_lower_r50_median",
        "binary_lower_admissible_clique_median",
        "random_panel_sufficient_admissible_q0.1_median",
        "random_panel_sufficient_admissible_q0.02_median",
    ]
    label = {
        "scope": "Scope",
        "k_cell_types_median": "K",
        "n_tissues_median": "Contexts",
        "max_tissue_cell_types_median": "Max context K",
        "admissible_edges_median": "Admissible pairs",
        "admissible_edge_fraction_median": "Pair fraction",
        "admissible_experiment_lower_r20_median": "Exp LB r=20",
        "admissible_experiment_lower_r50_median": "Exp LB r=50",
        "complete_experiment_lower_r50_median": "Complete LB r=50",
        "binary_lower_admissible_clique_median": "Binary marker LB",
        "random_panel_sufficient_admissible_q0.1_median": "Random genes q=.1",
        "random_panel_sufficient_admissible_q0.02_median": "Random genes q=.02",
    }

    with path.open("w", encoding="utf-8") as handle:
        handle.write("# Atlas design simulation\n\n")
        handle.write(
            "This simulation starts with organism-scale cell-type counts, assigns "
            "cell types to tissue/admissibility contexts, and computes three "
            "quantities: admissible pair count, experiment lower bounds, and "
            "marker-gene sufficiency estimates. The cell-type distributions are "
            "assumptions, not empirical ontology claims.\n\n"
        )
        handle.write("## Model\n\n")
        handle.write("- Cell types have one primary context.\n")
        handle.write("- A fraction of cell types is shared across additional contexts.\n")
        handle.write("- Two cell types are admissibly comparable if they share a context.\n")
        handle.write("- An experiment can jointly compare at most `r` cell types from one context.\n")
        handle.write(
            "- The marker-gene estimate uses a random-gene model: each candidate "
            "gene separates any admissible pair with probability `q`.\n\n"
        )
        handle.write(
            "The experiment values are lower bounds. The random-gene marker "
            "values are sufficient sizes under a union bound and are not minimum "
            "hitting-set optima.\n\n"
        )
        handle.write("| " + " | ".join(label[col] for col in display_cols) + " |\n")
        handle.write("|" + "|".join(["---"] + ["---:"] * (len(display_cols) - 1)) + "|\n")
        for row in summary[display_cols].itertuples(index=False):
            values = []
            for col, value in zip(display_cols, row):
                if col == "scope":
                    values.append(str(value))
                elif col == "admissible_edge_fraction_median":
                    values.append(f"{value:.3f}")
                else:
                    values.append(f"{value:.0f}")
            handle.write("| " + " | ".join(values) + " |\n")
        handle.write("\n## Interpretation\n\n")
        handle.write(
            "Tissue/admissibility constraints can reduce the comparison graph by "
            "orders of magnitude relative to the complete graph. They do not "
            "remove the marker-selection problem; they define which pairwise "
            "difference constraints must be hit by a marker panel.\n"
        )


def plot_summary(summary: pd.DataFrame, path: Path) -> None:
    scopes = summary["scope"].tolist()
    y = np.arange(len(scopes))

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.2))

    ax = axes[0]
    ax.barh(y, summary["admissible_edge_fraction_median"], color="#d0d0d0", edgecolor="black", linewidth=0.7)
    ax.set_yticks(y, scopes)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Admissible pair fraction")

    ax = axes[1]
    h = 0.34
    ax.barh(
        y - h / 2,
        summary["admissible_experiment_lower_r50_median"],
        height=h,
        label="admissible r=50",
        color="#99c2a2",
        edgecolor="black",
        linewidth=0.6,
    )
    ax.barh(
        y + h / 2,
        summary["complete_experiment_lower_r50_median"],
        height=h,
        label="complete r=50",
        color="#d7d7d7",
        edgecolor="black",
        linewidth=0.6,
    )
    ax.set_yticks(y, [])
    ax.set_xscale("log")
    ax.set_xlabel("Experiment lower bound")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[2]
    ax.barh(
        y - h / 2,
        summary["random_panel_sufficient_admissible_q0.1_median"],
        height=h,
        label="q=0.1",
        color="#c9d6ea",
        edgecolor="black",
        linewidth=0.6,
    )
    ax.barh(
        y + h / 2,
        summary["random_panel_sufficient_admissible_q0.02_median"],
        height=h,
        label="q=0.02",
        color="#f2d6a2",
        edgecolor="black",
        linewidth=0.6,
    )
    ax.set_yticks(y, [])
    ax.set_xlabel("Random marker panel sufficient size")
    ax.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    fig.savefig(path)
    fig.savefig(path.with_suffix(".png"), dpi=220)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(RNG_SEED)
    rows = []
    for scenario in SCENARIOS:
        for rep in range(N_REPS):
            rows.append(summarize_replicate(scenario, rep, rng))
    df = pd.DataFrame(rows)
    summary = summarize(df)

    detail_path = RESULTS_DIR / "atlas_design_simulation_replicates.tsv"
    summary_path = RESULTS_DIR / "atlas_design_simulation_summary.tsv"
    report_path = RESULTS_DIR / "atlas_design_simulation.md"
    figure_path = FIGURE_DIR / "fig_atlas_design_simulation.pdf"

    df.to_csv(detail_path, sep="\t", index=False)
    summary.to_csv(summary_path, sep="\t", index=False)
    write_markdown(summary, report_path)
    plot_summary(summary, figure_path)

    print(f"Wrote {detail_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {report_path}")
    print(f"Wrote {figure_path}")
    print(f"Wrote {figure_path.with_suffix('.png')}")


if __name__ == "__main__":
    main()
