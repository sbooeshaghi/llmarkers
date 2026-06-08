#!/usr/bin/env python3
"""Deterministic atlas-scope experiment and marker lower bounds.

This table is meant to clarify the formal model, not estimate the biological
truth. It reports two lower bounds:

1. Experiment lower bound: how many experiments are needed to cover all required
   cell-type pairs if each experiment jointly compares at most r cell types.
2. Marker lower bound: how many binary marker genes are needed in the best case
   to assign distinct marker signatures within the largest required comparison
   group.
3. Local marker lower bound: how many binary marker genes are needed in the best
   case inside one experiment that jointly compares at most r cell types.

The restricted model assumes cell types are partitioned into context groups.
Only pairs within the same context group are required to be distinguished. If
f = 0.25 and K = 400, the model uses groups of about 100 cell types.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil, comb, log2
from pathlib import Path


@dataclass(frozen=True)
class OrganismScope:
    scope: str
    k_cell_types: int
    protein_coding_genes: int


SCOPES = [
    OrganismScope("C. elegans adult", 146, 20000),
    OrganismScope("Drosophila adult", 250, 13900),
    OrganismScope("Human major cell types", 400, 20000),
    OrganismScope("Human fine cell types", 3358, 20000),
    OrganismScope("Mouse brain major types", 300, 22000),
    OrganismScope("Mouse brain clusters", 5322, 22000),
]

R_VALUES = [20, 50, 100]
F_VALUES = [1.0, 0.25, 0.10, 0.05]


def choose2(n: int) -> int:
    if n < 2:
        return 0
    return comb(n, 2)


def marker_lower_bound(n: int) -> int:
    if n <= 1:
        return 0
    return ceil(log2(n))


def group_sizes(k: int, f: float) -> list[int]:
    if f >= 1.0:
        return [k]
    group_size = max(2, ceil(k * f))
    sizes = []
    remaining = k
    while remaining > 0:
        size = min(group_size, remaining)
        sizes.append(size)
        remaining -= size
    if len(sizes) > 1 and sizes[-1] == 1:
        sizes[-2] += 1
        sizes.pop()
    return sizes


def experiment_lower_bound_for_group(size: int, r: int) -> int:
    if size <= 1:
        return 0
    r_eff = min(size, r)
    return ceil(choose2(size) / choose2(r_eff))


def build_rows() -> list[dict[str, object]]:
    rows = []
    for scope in SCOPES:
        for r in R_VALUES:
            for f in F_VALUES:
                sizes = group_sizes(scope.k_cell_types, f)
                required_pairs = sum(choose2(size) for size in sizes)
                experiments_lb = sum(experiment_lower_bound_for_group(size, r) for size in sizes)
                max_group_size = max(sizes)
                marker_lb = marker_lower_bound(max_group_size)
                local_marker_lb = marker_lower_bound(min(r, max_group_size))
                rows.append(
                    {
                        "scope": scope.scope,
                        "k_cell_types": scope.k_cell_types,
                        "protein_coding_genes": scope.protein_coding_genes,
                        "r_cell_types_per_experiment": r,
                        "f_context_group_fraction": f,
                        "n_context_groups": len(sizes),
                        "max_context_group_size": max_group_size,
                        "required_pairwise_comparisons": required_pairs,
                        "required_pair_fraction": required_pairs / choose2(scope.k_cell_types),
                        "experiment_lower_bound": experiments_lb,
                        "local_binary_marker_lower_bound": local_marker_lb,
                        "binary_marker_lower_bound": marker_lb,
                        "gene_universe_to_marker_lb_ratio": scope.protein_coding_genes / marker_lb
                        if marker_lb
                        else "",
                    }
                )
    return rows


def main() -> None:
    out_dir = Path("analysis/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    headers = list(rows[0].keys())

    tsv_path = out_dir / "atlas_scope_bounds.tsv"
    md_path = out_dir / "atlas_scope_bounds.md"
    with tsv_path.open("w", encoding="utf-8") as handle:
        handle.write("\t".join(headers) + "\n")
        for row in rows:
            handle.write("\t".join(str(row[h]) for h in headers) + "\n")

    with md_path.open("w", encoding="utf-8") as handle:
        handle.write("# Atlas scope bounds\n\n")
        handle.write("This deterministic table uses a simple restricted-scope model.\n\n")
        handle.write("- `K`: target cell types.\n")
        handle.write("- `G`: protein-coding gene universe.\n")
        handle.write("- `r`: maximum cell types jointly compared in one experiment.\n")
        handle.write("- `f`: context group size as a fraction of `K`.\n")
        handle.write("- `f=1`: complete global comparison over all cell types.\n")
        handle.write("- `f<1`: cell types are partitioned into context groups of size about `fK`; only within-group pairs are required.\n\n")
        handle.write("The experiment lower bound is pair-coverage. `local marker LB` is `ceil(log2(min(r, max context group size)))`, the best-case binary-feature lower bound inside one local experiment. `atlas marker LB` is `ceil(log2(max context group size))`, the best-case lower bound for the full required scope. Neither marker value is an empirical marker-panel size.\n\n")
        handle.write("| Scope | K | G | r cell types/experiment | f | groups | max group | pairs | pair fraction | experiments LB | local marker LB | atlas marker LB |\n")
        handle.write("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for row in rows:
            handle.write(
                f"| {row['scope']} | {row['k_cell_types']} | {row['protein_coding_genes']} | "
                f"{row['r_cell_types_per_experiment']} | {row['f_context_group_fraction']:.2f} | "
                f"{row['n_context_groups']} | {row['max_context_group_size']} | "
                f"{row['required_pairwise_comparisons']} | {row['required_pair_fraction']:.3f} | "
                f"{row['experiment_lower_bound']} | {row['local_binary_marker_lower_bound']} | "
                f"{row['binary_marker_lower_bound']} |\n"
            )

    print(f"Wrote {tsv_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
