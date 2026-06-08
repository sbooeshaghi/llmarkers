#!/usr/bin/env python3
"""Compute simple marker-panel experiment covering bounds.

The bounds here are intentionally combinatorial. They do not model sampling
depth, abundance, power, tissue access, assay effects, or biological feasibility.

Definitions:
- K: number of target cell types in the atlas scope.
- r: maximum number of cell types that can be jointly compared in one experiment.
- A global marker panel must separate every unordered pair of target cell types.
- One experiment containing r cell types can certify at most choose(r, 2) pairs.

Therefore any experiment design requires at least

    ceil(choose(K, 2) / choose(r, 2))

experiments. The exact optimum is a covering design number C(K, r, 2), which can
be larger than this lower bound.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, comb, log2
from pathlib import Path


@dataclass(frozen=True)
class Scenario:
    scope: str
    total_cells: str
    protein_coding_genes: str
    k_cell_types: int
    note: str
    sources: str


SCENARIOS = [
    Scenario(
        scope="C. elegans adult, high-resolution cell classes",
        total_cells="959 somatic",
        protein_coding_genes="~20,000",
        k_cell_types=146,
        note="TF atlas high-resolution classes",
        sources=(
            "https://www.ncbi.nlm.nih.gov/books/NBK26861/; "
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC4781646/; "
            "https://www.nature.com/articles/s41467-023-42677-6"
        ),
    ),
    Scenario(
        scope="Drosophila adult, Fly Cell Atlas",
        total_cells="580,000 sampled nuclei",
        protein_coding_genes="~13,900",
        k_cell_types=250,
        note="reported as >250 annotated cell types; rounded down",
        sources=(
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC8944923/; "
            "https://academic.oup.com/genetics/article/201/3/815/5930114"
        ),
    ),
    Scenario(
        scope="Human Tabula Sapiens",
        total_cells="~500,000 sampled cells",
        protein_coding_genes="~20,000",
        k_cell_types=475,
        note="distinct annotated cell types",
        sources=(
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC9812260/; "
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC6413734/"
        ),
    ),
    Scenario(
        scope="Human body, major cell-type estimate",
        total_cells="~27-37 trillion",
        protein_coding_genes="~20,000",
        k_cell_types=400,
        note="major cell-type estimate",
        sources="https://www.nature.com/articles/s41597-026-06642-4",
    ),
    Scenario(
        scope="Human body, fine cell-type estimate",
        total_cells="~27-37 trillion",
        protein_coding_genes="~20,000",
        k_cell_types=3358,
        note="fine cell-type estimate cited by HRA paper",
        sources="https://www.nature.com/articles/s41597-026-06642-4",
    ),
    Scenario(
        scope="Mouse brain, major cell types",
        total_cells=">32 million characterized",
        protein_coding_genes="~20,000-25,000",
        k_cell_types=300,
        note="mouse whole-brain major cell types",
        sources=(
            "https://alleninstitute.org/news/scientists-unveil-first-complete-cellular-map-of-adult-mouse-brain; "
            "https://www.nature.com/articles/s41586-023-06808-9; "
            "https://pubmed.ncbi.nlm.nih.gov/28838066/"
        ),
    ),
    Scenario(
        scope="Mouse brain, transcriptomic clusters",
        total_cells=">32 million characterized",
        protein_coding_genes="~20,000-25,000",
        k_cell_types=5322,
        note="mouse whole-brain clusters",
        sources=(
            "https://alleninstitute.org/news/scientists-unveil-first-complete-cellular-map-of-adult-mouse-brain; "
            "https://www.nature.com/articles/s41586-023-06812-z; "
            "https://pubmed.ncbi.nlm.nih.gov/28838066/"
        ),
    ),
]

R_VALUES = [5, 10, 20, 50, 100, 500]


def experiment_lower_bound(k: int, r: int) -> int:
    """Pair-coverage lower bound for experiments with at most r cell types."""
    if k <= 1:
        return 0
    r_eff = min(k, r)
    if r_eff < 2:
        return 0
    return ceil(comb(k, 2) / comb(r_eff, 2))


def min_binary_markers(k: int) -> int:
    """Unconstrained information-theoretic lower bound on binary markers."""
    if k <= 1:
        return 0
    return ceil(log2(k))


def main() -> None:
    out_dir = Path("analysis/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    tsv_path = out_dir / "marker_experiment_covering_bounds.tsv"
    md_path = out_dir / "marker_experiment_covering_bounds.md"

    rows = []
    for s in SCENARIOS:
        row = {
            "scope": s.scope,
            "total_cells": s.total_cells,
            "protein_coding_genes": s.protein_coding_genes,
            "k_cell_types": str(s.k_cell_types),
            "pairwise_comparisons": str(comb(s.k_cell_types, 2)),
            "min_binary_markers": str(min_binary_markers(s.k_cell_types)),
            "note": s.note,
            "sources": s.sources,
        }
        for r in R_VALUES:
            row[f"min_experiments_r{r}"] = str(experiment_lower_bound(s.k_cell_types, r))
        rows.append(row)

    headers = list(rows[0].keys())
    with tsv_path.open("w", encoding="utf-8") as handle:
        handle.write("\t".join(headers) + "\n")
        for row in rows:
            handle.write("\t".join(row[h] for h in headers) + "\n")

    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Marker experiment covering bounds\n\n")
        handle.write(
            "For `K` target cell types and experiments that jointly compare at most "
            "`r` cell types, any design that certifies all pairwise marker "
            "separations needs at least\n\n"
        )
        handle.write("```text\nceil(choose(K, 2) / choose(r, 2))\n```\n\n")
        handle.write(
            "experiments. The exact optimum is the covering design number "
            "`C(K, r, 2)`, which can be larger. The binary marker lower bound is "
            "`ceil(log2(K))`; it is an information-theoretic lower bound, not a "
            "claim that such a biological panel exists.\n\n"
        )
        handle.write("| Scope | K | Pairs | Binary markers | r=5 | r=10 | r=20 | r=50 | r=100 | r=500 |\n")
        handle.write("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            handle.write(
                f"| {row['scope']} | {row['k_cell_types']} | "
                f"{row['pairwise_comparisons']} | {row['min_binary_markers']} | "
                f"{row['min_experiments_r5']} | {row['min_experiments_r10']} | "
                f"{row['min_experiments_r20']} | {row['min_experiments_r50']} | "
                f"{row['min_experiments_r100']} | {row['min_experiments_r500']} |\n"
            )
        handle.write("\n## Scenario notes\n\n")
        for s in SCENARIOS:
            handle.write(
                f"- **{s.scope}**: total cells = {s.total_cells}; genes = "
                f"{s.protein_coding_genes}; note = {s.note}; sources = {s.sources}.\n"
            )

    print(f"Wrote {tsv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
