from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

from build_marker_stability_prototype import assign_neighborhood, build_records
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR, build_profile_summary, split_marker_text
from marker_label_utils import normalize_label


SUMMARY_PATH = RESULTS_DIR / "marker_identifiability_partition_summary.tsv"
SELECTED_GENES_PATH = RESULTS_DIR / "marker_identifiability_selected_genes.tsv"
DUPLICATE_SIGNATURES_PATH = RESULTS_DIR / "marker_identifiability_duplicate_signatures.tsv"
PAIR_CONSTRAINTS_PATH = RESULTS_DIR / "marker_identifiability_pair_constraints.tsv"
REPORT_PATH = RESULTS_DIR / "marker_identifiability_report.md"

TCELL_MEMBERSHIP_PATH = RESULTS_DIR / "tcell_marker_cluster_membership.tsv"
MYELOID_MEMBERSHIP_PATH = RESULTS_DIR / "myeloid_marker_cluster_membership.tsv"

COVERAGE_THRESHOLDS = [0.05, 0.10, 0.20]
ILP_MAX_CONSTRAINTS = 6000
ILP_MAX_GENES = 5000
ILP_TIME_LIMIT_SECONDS = 90


@dataclass(frozen=True)
class PartitionSpec:
    name: str
    group_col: str
    min_group_profiles: int
    source: str


def ceil_log2(n: int) -> int:
    if n <= 1:
        return 0
    return (n - 1).bit_length()


def harmonic(coverage: float, purity: float) -> float:
    if coverage + purity == 0:
        return 0.0
    return 2 * coverage * purity / (coverage + purity)


def load_profiles() -> tuple[pd.DataFrame, dict[str, str]]:
    records_df = build_records()
    _profiles_df, filtered_profiles_df, _filtered_profiles, id_to_name = build_profile_summary(
        records_df,
        min_markers=3,
        feature_id_col="feature_id_std",
        feature_name_col="feature_name_std",
    )
    profiles_df = filtered_profiles_df.copy().reset_index(drop=True)
    profiles_df["profile_uid"] = [
        f"{row.source_corpus}|{row.paper_id}|{row.cell_type}" for row in profiles_df.itertuples(index=False)
    ]
    profiles_df["marker_set"] = profiles_df["marker_ids"].map(lambda value: set(split_marker_text(value)))
    profiles_df["neighborhood"] = profiles_df["cell_type"].map(assign_neighborhood)
    profiles_df["normalized_cell_type"] = profiles_df["cell_type"].map(normalize_label)
    return profiles_df, id_to_name


def profile_uid(row: pd.Series) -> str:
    return f"{row['source_corpus']}|{row['paper_id']}|{row['cell_type']}"


def add_marker_cluster_partitions(profiles_df: pd.DataFrame) -> pd.DataFrame:
    df = profiles_df.copy()
    df["tcell_marker_cluster"] = pd.NA
    df["myeloid_marker_cluster"] = pd.NA
    for path, col in [
        (TCELL_MEMBERSHIP_PATH, "tcell_marker_cluster"),
        (MYELOID_MEMBERSHIP_PATH, "myeloid_marker_cluster"),
    ]:
        if not path.exists():
            continue
        membership_df = pd.read_csv(path, sep="\t")
        membership_df["profile_uid"] = membership_df.apply(profile_uid, axis=1)
        mapping = {
            row.profile_uid: f"C{int(row.component)}" for row in membership_df.itertuples(index=False)
        }
        df[col] = df["profile_uid"].map(mapping)
    return df


def partition_specs(profiles_df: pd.DataFrame) -> list[PartitionSpec]:
    specs = [
        PartitionSpec(
            name="broad_neighborhoods",
            group_col="neighborhood",
            min_group_profiles=20,
            source="assign_neighborhood(cell_type)",
        ),
        PartitionSpec(
            name="reported_exact_labels_min5",
            group_col="normalized_cell_type",
            min_group_profiles=5,
            source="normalized reported cell type label",
        ),
    ]
    if profiles_df["tcell_marker_cluster"].notna().any():
        specs.append(
            PartitionSpec(
                name="tcell_marker_clusters",
                group_col="tcell_marker_cluster",
                min_group_profiles=3,
                source="T-cell marker-derived clusters",
            )
        )
    if profiles_df["myeloid_marker_cluster"].notna().any():
        specs.append(
            PartitionSpec(
                name="myeloid_marker_clusters",
                group_col="myeloid_marker_cluster",
                min_group_profiles=3,
                source="myeloid marker-derived clusters",
            )
        )
    return specs


def grouped_profiles(profiles_df: pd.DataFrame, spec: PartitionSpec) -> pd.DataFrame:
    df = profiles_df.loc[profiles_df[spec.group_col].notna()].copy()
    df = df.loc[df[spec.group_col].astype(str).str.len().gt(0)].copy()
    counts = df[spec.group_col].value_counts()
    keep_groups = counts.loc[counts >= spec.min_group_profiles].index
    return df.loc[df[spec.group_col].isin(keep_groups)].copy()


def class_gene_sets(
    profiles_df: pd.DataFrame,
    group_col: str,
    coverage_threshold: float,
) -> tuple[dict[str, set[str]], dict[str, int], dict[tuple[str, str], int]]:
    group_to_genes: dict[str, set[str]] = {}
    group_sizes: dict[str, int] = {}
    group_gene_counts: dict[tuple[str, str], int] = {}
    for group, group_df in profiles_df.groupby(group_col, sort=True):
        group = str(group)
        group_sizes[group] = len(group_df)
        counts = Counter(gene_id for marker_set in group_df["marker_set"] for gene_id in marker_set)
        group_to_genes[group] = {
            gene_id for gene_id, count in counts.items() if count / len(group_df) >= coverage_threshold
        }
        for gene_id, count in counts.items():
            group_gene_counts[(group, gene_id)] = count
    return group_to_genes, group_sizes, group_gene_counts


def signature_key(genes: set[str], gene_vocab: list[str]) -> tuple[int, ...]:
    gene_set = set(genes)
    return tuple(1 if gene_id in gene_set else 0 for gene_id in gene_vocab)


def collapse_duplicate_signatures(
    group_to_genes: dict[str, set[str]],
    gene_vocab: list[str],
) -> tuple[dict[str, set[str]], list[dict[str, object]]]:
    signature_to_groups: dict[tuple[int, ...], list[str]] = defaultdict(list)
    for group, genes in group_to_genes.items():
        signature_to_groups[signature_key(genes, gene_vocab)].append(group)

    collapsed: dict[str, set[str]] = {}
    duplicate_rows = []
    for idx, (signature, groups) in enumerate(signature_to_groups.items(), start=1):
        representative = groups[0]
        collapsed[representative] = set(group_to_genes[representative])
        if len(groups) > 1:
            duplicate_rows.append(
                {
                    "signature_id": f"S{idx}",
                    "representative_group": representative,
                    "n_groups": len(groups),
                    "groups": "; ".join(groups),
                    "n_on_genes": int(sum(signature)),
                }
            )
    return collapsed, duplicate_rows


def build_pair_constraints(
    group_to_genes: dict[str, set[str]],
    gene_vocab: list[str],
) -> tuple[list[tuple[str, str, set[str]]], list[tuple[str, str]]]:
    groups = sorted(group_to_genes)
    constraints = []
    empty_pairs = []
    for idx_a, group_a in enumerate(groups):
        for group_b in groups[idx_a + 1 :]:
            diff = group_to_genes[group_a] ^ group_to_genes[group_b]
            if diff:
                constraints.append((group_a, group_b, diff))
            else:
                empty_pairs.append((group_a, group_b))
    return constraints, empty_pairs


def greedy_separating_panel(
    constraints: list[tuple[str, str, set[str]]],
    gene_vocab: list[str],
) -> tuple[list[str], dict[str, int]]:
    uncovered = set(range(len(constraints)))
    gene_to_pairs: dict[str, set[int]] = {gene_id: set() for gene_id in gene_vocab}
    for pair_idx, (_group_a, _group_b, diff) in enumerate(constraints):
        for gene_id in diff:
            gene_to_pairs[gene_id].add(pair_idx)

    selected = []
    selected_pair_counts = {}
    while uncovered:
        best_gene = None
        best_cover: set[int] = set()
        for gene_id, pair_indices in gene_to_pairs.items():
            cover = pair_indices & uncovered
            if len(cover) > len(best_cover) or (
                len(cover) == len(best_cover) and best_gene is not None and gene_id < best_gene
            ):
                best_gene = gene_id
                best_cover = cover
        if best_gene is None or not best_cover:
            break
        selected.append(best_gene)
        selected_pair_counts[best_gene] = len(best_cover)
        uncovered -= best_cover
    return selected, selected_pair_counts


def constraint_matrix(
    constraints: list[tuple[str, str, set[str]]],
    gene_vocab: list[str],
) -> coo_matrix:
    gene_to_col = {gene_id: idx for idx, gene_id in enumerate(gene_vocab)}
    rows = []
    cols = []
    data = []
    for row_idx, (_group_a, _group_b, diff) in enumerate(constraints):
        for gene_id in diff:
            col_idx = gene_to_col.get(gene_id)
            if col_idx is None:
                continue
            rows.append(row_idx)
            cols.append(col_idx)
            data.append(1.0)
    return coo_matrix((data, (rows, cols)), shape=(len(constraints), len(gene_vocab))).tocsr()


def solve_ilp_panel(
    constraints: list[tuple[str, str, set[str]]],
    gene_vocab: list[str],
    forbidden_gene: str | None = None,
) -> tuple[str, list[str], float | None]:
    if not constraints:
        return "trivial", [], 0.0
    c = np.ones(len(gene_vocab), dtype=float)
    integrality = np.ones(len(gene_vocab), dtype=int)
    lb = np.zeros(len(gene_vocab), dtype=float)
    ub = np.ones(len(gene_vocab), dtype=float)
    if forbidden_gene is not None:
        try:
            ub[gene_vocab.index(forbidden_gene)] = 0.0
        except ValueError:
            pass
    A = constraint_matrix(constraints, gene_vocab)
    linear_constraint = LinearConstraint(
        A,
        lb=np.ones(len(constraints), dtype=float),
        ub=np.full(len(constraints), np.inf, dtype=float),
    )
    result = milp(
        c=c,
        integrality=integrality,
        bounds=Bounds(lb, ub),
        constraints=linear_constraint,
        options={"time_limit": ILP_TIME_LIMIT_SECONDS, "mip_rel_gap": 0.0},
    )
    if not result.success or result.x is None:
        return str(result.message), [], None
    selected = [
        gene_id for gene_id, value in zip(gene_vocab, result.x, strict=True) if value >= 0.5
    ]
    return "optimal" if result.mip_gap == 0 else "feasible", selected, float(result.fun)


def selected_gene_rows(
    selected: list[str],
    selected_pair_counts: dict[str, int],
    method: str,
    partition: str,
    threshold: float,
    group_to_genes: dict[str, set[str]],
    group_sizes: dict[str, int],
    group_gene_counts: dict[tuple[str, str], int],
    global_gene_counts: Counter,
    id_to_name: dict[str, str],
    constraints: list[tuple[str, str, set[str]]],
    role_by_gene: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    rows = []
    groups = sorted(group_to_genes)
    for rank, gene_id in enumerate(selected, start=1):
        on_groups = [group for group in groups if gene_id in group_to_genes[group]]
        coverage_values = []
        for group in on_groups:
            coverage_values.append(group_gene_counts.get((group, gene_id), 0) / group_sizes[group])
        covered_pairs = sum(1 for _a, _b, diff in constraints if gene_id in diff)
        rows.append(
            {
                "partition": partition,
                "coverage_threshold": threshold,
                "method": method,
                "rank": rank,
                "gene_id": gene_id,
                "gene_name": id_to_name.get(gene_id, gene_id),
                "role": (role_by_gene or {}).get(gene_id, "not_tested"),
                "pair_constraints_covered": covered_pairs,
                "new_pair_constraints_covered_greedy": selected_pair_counts.get(gene_id),
                "n_on_groups": len(on_groups),
                "n_groups": len(groups),
                "mean_on_group_coverage": float(np.mean(coverage_values)) if coverage_values else 0.0,
                "global_profile_count": int(global_gene_counts.get(gene_id, 0)),
                "on_groups": "; ".join(on_groups[:30]),
            }
        )
    return rows


def test_selected_gene_roles(
    selected: list[str],
    optimum_size: int | None,
    constraints: list[tuple[str, str, set[str]]],
    gene_vocab: list[str],
) -> dict[str, str]:
    if optimum_size is None or not selected:
        return {gene_id: "not_tested" for gene_id in selected}
    roles = {}
    for gene_id in selected:
        status, alt_selected, objective = solve_ilp_panel(constraints, gene_vocab, forbidden_gene=gene_id)
        if objective is None or status not in {"optimal", "feasible", "trivial"}:
            roles[gene_id] = "essential_in_minimum_panels"
        elif int(round(objective)) > optimum_size:
            roles[gene_id] = "essential_in_minimum_panels"
        else:
            roles[gene_id] = "exchangeable_in_minimum_panels"
    return roles


def analyze_partition(
    partition_df: pd.DataFrame,
    spec: PartitionSpec,
    threshold: float,
    id_to_name: dict[str, str],
    global_gene_counts: Counter,
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    group_to_genes, group_sizes, group_gene_counts = class_gene_sets(
        partition_df,
        spec.group_col,
        threshold,
    )
    gene_vocab = sorted(set().union(*group_to_genes.values())) if group_to_genes else []
    collapsed_group_to_genes, duplicate_rows = collapse_duplicate_signatures(group_to_genes, gene_vocab)
    duplicate_rows = [
        {
            "partition": spec.name,
            "coverage_threshold": threshold,
            **row,
        }
        for row in duplicate_rows
    ]
    constraints, empty_pairs = build_pair_constraints(collapsed_group_to_genes, gene_vocab)
    greedy_selected, greedy_pair_counts = greedy_separating_panel(constraints, gene_vocab)

    ilp_status = "skipped"
    ilp_selected: list[str] = []
    ilp_objective = None
    ilp_roles: dict[str, str] = {}
    if len(constraints) <= ILP_MAX_CONSTRAINTS and len(gene_vocab) <= ILP_MAX_GENES and not empty_pairs:
        ilp_status, ilp_selected, ilp_objective = solve_ilp_panel(constraints, gene_vocab)
        if ilp_objective is not None and ilp_status in {"optimal", "feasible", "trivial"}:
            ilp_roles = test_selected_gene_roles(
                ilp_selected,
                int(round(ilp_objective)),
                constraints,
                gene_vocab,
            )

    selected_rows = []
    selected_rows.extend(
        selected_gene_rows(
            greedy_selected,
            greedy_pair_counts,
            "greedy_set_cover",
            spec.name,
            threshold,
            collapsed_group_to_genes,
            group_sizes,
            group_gene_counts,
            global_gene_counts,
            id_to_name,
            constraints,
        )
    )
    if ilp_selected:
        selected_rows.extend(
            selected_gene_rows(
                ilp_selected,
                {},
                "ilp_minimum",
                spec.name,
                threshold,
                collapsed_group_to_genes,
                group_sizes,
                group_gene_counts,
                global_gene_counts,
                id_to_name,
                constraints,
                ilp_roles,
            )
        )

    pair_rows = []
    for group_a, group_b, diff in constraints:
        pair_rows.append(
            {
                "partition": spec.name,
                "coverage_threshold": threshold,
                "group_a": group_a,
                "group_b": group_b,
                "n_separating_genes": len(diff),
                "separating_gene_names": "; ".join(id_to_name.get(gene_id, gene_id) for gene_id in sorted(diff)[:25]),
            }
        )

    summary = {
        "partition": spec.name,
        "source": spec.source,
        "coverage_threshold": threshold,
        "min_group_profiles": spec.min_group_profiles,
        "n_groups": len(group_to_genes),
        "n_profiles": len(partition_df),
        "n_gene_columns": len(gene_vocab),
        "n_distinct_signatures": len(collapsed_group_to_genes),
        "n_groups_in_duplicate_signatures": sum(row["n_groups"] for row in duplicate_rows),
        "all_groups_identifiable_with_all_genes": len(duplicate_rows) == 0,
        "n_pair_constraints": len(constraints),
        "n_empty_pairs_original": len(empty_pairs),
        "information_lower_bound_log2": ceil_log2(len(collapsed_group_to_genes)),
        "greedy_panel_size": len(greedy_selected),
        "ilp_status": ilp_status,
        "ilp_panel_size": len(ilp_selected) if ilp_selected else pd.NA,
        "ilp_objective": ilp_objective if ilp_objective is not None else pd.NA,
    }
    return summary, selected_rows, duplicate_rows, pair_rows


def write_report(summary_df: pd.DataFrame, selected_df: pd.DataFrame, duplicate_df: pd.DataFrame) -> None:
    def markdown_table(df: pd.DataFrame) -> str:
        string_df = df.fillna("").astype(str)
        header = "| " + " | ".join(string_df.columns) + " |"
        separator = "| " + " | ".join(["---"] * len(string_df.columns)) + " |"
        rows = [
            "| " + " | ".join(row) + " |"
            for row in string_df.itertuples(index=False, name=None)
        ]
        return "\n".join([header, separator, *rows])

    lines = [
        "# Marker Identifiability Analysis",
        "",
        "This analysis applies the Lean formalization in `analysis/formal/MarkerIdentifiability/Basic.lean` to the LLMarkers reported-marker matrix.",
        "For each partition, a gene is turned on for a group if it is reported in at least the stated fraction of profiles in that group.",
        "The Lean theorem gives the information lower bound: if `k` induced binary signatures are separated by binary markers, any separating panel needs at least `ceil(log2(k))` marker coordinates.",
        "",
        "Important caveat: zeros in this matrix mean not reported as a marker in the corpus, not absent expression.",
        "",
        "## Partition Summary",
        "",
    ]
    display_cols = [
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
    lines.append(markdown_table(summary_df[display_cols]))
    lines.extend(["", "## ILP-Selected Marker Panels", ""])
    ilp_df = selected_df.loc[selected_df["method"].eq("ilp_minimum")].copy()
    if ilp_df.empty:
        lines.append("No ILP panels were solved.")
    else:
        for (partition, threshold), group_df in ilp_df.groupby(["partition", "coverage_threshold"], sort=False):
            panel = ", ".join(
                f"{row.gene_name} ({row.role.replace('_', ' ')})" for row in group_df.itertuples(index=False)
            )
            lines.append(f"- **{partition}**, threshold {threshold:.2f}: {panel}")
    lines.extend(["", "## Duplicate Signatures", ""])
    if duplicate_df.empty:
        lines.append("No duplicate class signatures were found at the evaluated thresholds.")
    else:
        for row in duplicate_df.head(20).itertuples(index=False):
            lines.append(
                f"- **{row.partition}**, threshold {row.coverage_threshold:.2f}, {row.signature_id}: "
                f"{row.groups}"
            )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    profiles_df, id_to_name = load_profiles()
    profiles_df = add_marker_cluster_partitions(profiles_df)
    global_gene_counts = Counter(gene_id for marker_set in profiles_df["marker_set"] for gene_id in marker_set)

    summary_rows = []
    selected_rows = []
    duplicate_rows = []
    pair_rows = []
    for spec in partition_specs(profiles_df):
        partition_df = grouped_profiles(profiles_df, spec)
        if partition_df.empty:
            continue
        for threshold in COVERAGE_THRESHOLDS:
            summary, selected, duplicates, pairs = analyze_partition(
                partition_df,
                spec,
                threshold,
                id_to_name,
                global_gene_counts,
            )
            summary_rows.append(summary)
            selected_rows.extend(selected)
            duplicate_rows.extend(duplicates)
            pair_rows.extend(pairs)

    summary_df = pd.DataFrame(summary_rows)
    selected_df = pd.DataFrame(selected_rows)
    duplicate_df = pd.DataFrame(duplicate_rows)
    pair_df = pd.DataFrame(pair_rows)

    summary_df.to_csv(SUMMARY_PATH, sep="\t", index=False)
    selected_df.to_csv(SELECTED_GENES_PATH, sep="\t", index=False)
    duplicate_df.to_csv(DUPLICATE_SIGNATURES_PATH, sep="\t", index=False)
    pair_df.to_csv(PAIR_CONSTRAINTS_PATH, sep="\t", index=False)
    write_report(summary_df, selected_df, duplicate_df)

    print(f"Wrote {SUMMARY_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SELECTED_GENES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {DUPLICATE_SIGNATURES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PAIR_CONSTRAINTS_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
