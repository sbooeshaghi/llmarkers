from __future__ import annotations

import re
import unicodedata
from collections import Counter, OrderedDict
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from build_marker_stability_prototype import assign_neighborhood, build_records
from build_tcell_marker_hierarchy import STATE_MODULES, markdown_table, profile_module_scores
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR, build_profile_summary, split_marker_text


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

MIN_MARKERS = 3
JACCARD_THRESHOLD = 0.5
MIN_COMPONENT_SIZE = 4
MAX_COMPONENTS = 7
CORE_GENE_FRACTION = 0.5

FIGURE_PATH = FIGURE_DIR / "fig_tcell_marker_cluster_summary.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig_tcell_marker_cluster_summary.png"
SUMMARY_PATH = RESULTS_DIR / "tcell_marker_cluster_summary.tsv"
MEMBERSHIP_PATH = RESULTS_DIR / "tcell_marker_cluster_membership.tsv"
REPORT_PATH = RESULTS_DIR / "tcell_marker_cluster_summary.md"

GENERIC_LABEL_TOKENS = {
    "a",
    "an",
    "and",
    "cell",
    "cells",
    "cluster",
    "clusters",
    "population",
    "populations",
    "type",
    "types",
}

RELATION_ORDER = ["Exact", "Partial", "Different"]
RELATION_COLORS = {
    "Exact": "#a8d8cf",
    "Partial": "#f3dfb7",
    "Different": "#d9d9d9",
}


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def ascii_text(value: object) -> str:
    text = unicodedata.normalize("NFKD", clean_text(value))
    return text.encode("ascii", "ignore").decode("ascii")


def normalize_label(value: object) -> str:
    text = ascii_text(value).upper()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    text = re.sub(r"(?<=[A-Z])(?=[0-9])", " ", text)
    text = re.sub(r"(?<=[0-9])(?=[A-Z])", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def label_tokens(label: str) -> set[str]:
    return {
        token
        for token in label.lower().split()
        if token not in GENERIC_LABEL_TOKENS and len(token) >= 2
    }


def label_relation(label_a: str, label_b: str) -> str:
    if label_a == label_b and label_a:
        return "Exact"
    if not label_a or not label_b:
        return "Different"
    padded_a = f" {label_a} "
    padded_b = f" {label_b} "
    if padded_a in padded_b or padded_b in padded_a:
        return "Partial"
    tokens_a = label_tokens(label_a)
    tokens_b = label_tokens(label_b)
    if tokens_a and tokens_b and tokens_a.intersection(tokens_b):
        return "Partial"
    return "Different"


def build_name_to_ids(records_df: pd.DataFrame) -> dict[str, list[str]]:
    subset = records_df.loc[
        records_df["feature_name_std"].ne("") & records_df["feature_id_std"].ne(""),
        ["feature_name_std", "feature_id_std"],
    ].drop_duplicates()
    return (
        subset.groupby("feature_name_std")["feature_id_std"]
        .agg(lambda values: sorted(set(values)))
        .to_dict()
    )


def module_gene_rows(name_to_ids: dict[str, list[str]], gene_vocab: set[str]) -> pd.DataFrame:
    rows = []
    used_gene_ids: set[str] = set()
    for module, gene_names in STATE_MODULES.items():
        for gene_name in gene_names:
            matching_ids = [gene_id for gene_id in name_to_ids.get(gene_name, []) if gene_id in gene_vocab]
            for gene_id in matching_ids:
                if gene_id in used_gene_ids:
                    continue
                used_gene_ids.add(gene_id)
                rows.append({"module": module, "gene_name": gene_name, "gene_id": gene_id})
    return pd.DataFrame(rows)


def marker_sets(profiles_df: pd.DataFrame) -> list[set[str]]:
    return [set(split_marker_text(marker_ids)) for marker_ids in profiles_df["marker_ids"]]


def connected_components(
    profile_gene_sets: list[set[str]],
    paper_keys: list[str],
    threshold: float,
) -> tuple[list[list[int]], list[tuple[int, int, float]]]:
    adjacency = [set() for _ in profile_gene_sets]
    edges = []
    for idx_a, idx_b in combinations(range(len(profile_gene_sets)), 2):
        if paper_keys[idx_a] == paper_keys[idx_b]:
            continue
        genes_a = profile_gene_sets[idx_a]
        genes_b = profile_gene_sets[idx_b]
        union = genes_a | genes_b
        jaccard = len(genes_a & genes_b) / len(union) if union else 0.0
        if jaccard >= threshold:
            adjacency[idx_a].add(idx_b)
            adjacency[idx_b].add(idx_a)
            edges.append((idx_a, idx_b, jaccard))

    components = []
    seen: set[int] = set()
    for start_idx in range(len(profile_gene_sets)):
        if start_idx in seen or not adjacency[start_idx]:
            continue
        stack = [start_idx]
        seen.add(start_idx)
        component = []
        while stack:
            idx = stack.pop()
            component.append(idx)
            for neighbor_idx in adjacency[idx]:
                if neighbor_idx not in seen:
                    seen.add(neighbor_idx)
                    stack.append(neighbor_idx)
        components.append(sorted(component))
    return components, edges


def summarize_components(
    tcell_df: pd.DataFrame,
    profile_gene_sets: list[set[str]],
    id_to_name: dict[str, str],
    components: list[list[int]],
    edges: list[tuple[int, int, float]],
) -> pd.DataFrame:
    edge_lookup = {(min(i, j), max(i, j)): jaccard for i, j, jaccard in edges}
    rows = []
    for component_idx, component in enumerate(sorted(components, key=len, reverse=True), start=1):
        if len(component) < MIN_COMPONENT_SIZE:
            continue
        component_df = tcell_df.iloc[component].copy()
        gene_counts = Counter(gene_id for idx in component for gene_id in profile_gene_sets[idx])
        core_gene_ids = [
            gene_id
            for gene_id, count in gene_counts.most_common()
            if count / len(component) >= CORE_GENE_FRACTION
        ]
        if not core_gene_ids:
            core_gene_ids = [gene_id for gene_id, _ in gene_counts.most_common(5)]
        top_gene_ids = [gene_id for gene_id, _ in gene_counts.most_common(10)]

        label_counts = Counter(component_df["cell_type"])
        top_labels = label_counts.most_common(6)
        normalized_labels = component_df["cell_type"].map(normalize_label).tolist()

        relation_counts = Counter({relation: 0 for relation in RELATION_ORDER})
        label_pair_count = 0
        internal_jaccards = []
        for local_a, local_b in combinations(range(len(component)), 2):
            idx_a = component[local_a]
            idx_b = component[local_b]
            if tcell_df.iloc[idx_a]["paper_key"] == tcell_df.iloc[idx_b]["paper_key"]:
                continue
            label_pair_count += 1
            relation_counts[label_relation(normalized_labels[local_a], normalized_labels[local_b])] += 1
            genes_a = profile_gene_sets[idx_a]
            genes_b = profile_gene_sets[idx_b]
            union = genes_a | genes_b
            internal_jaccards.append(len(genes_a & genes_b) / len(union) if union else 0.0)

        component_edges = [
            edge_lookup[(min(i, j), max(i, j))]
            for i, j in combinations(component, 2)
            if (min(i, j), max(i, j)) in edge_lookup
        ]
        program_counts = Counter(component_df["dominant_module"])
        dominant_program, dominant_program_count = program_counts.most_common(1)[0]
        rows.append(
            {
                "component": component_idx,
                "profiles": len(component),
                "papers": component_df["paper_key"].nunique(),
                "labels": component_df["cell_type"].nunique(),
                "dominant_program": dominant_program,
                "dominant_program_fraction": dominant_program_count / len(component),
                "core_marker_genes": "; ".join(id_to_name.get(gene_id, gene_id) for gene_id in core_gene_ids[:8]),
                "top_marker_genes": "; ".join(id_to_name.get(gene_id, gene_id) for gene_id in top_gene_ids),
                "top_labels": "; ".join(f"{ascii_text(label)} ({count})" for label, count in top_labels),
                "label_pairs": label_pair_count,
                "exact_label_pairs": relation_counts["Exact"],
                "partial_label_pairs": relation_counts["Partial"],
                "different_label_pairs": relation_counts["Different"],
                "exact_label_fraction": relation_counts["Exact"] / label_pair_count if label_pair_count else 0.0,
                "partial_label_fraction": relation_counts["Partial"] / label_pair_count if label_pair_count else 0.0,
                "different_label_fraction": relation_counts["Different"] / label_pair_count if label_pair_count else 0.0,
                "mean_internal_jaccard": float(np.mean(internal_jaccards)) if internal_jaccards else 0.0,
                "mean_edge_jaccard": float(np.mean(component_edges)) if component_edges else 0.0,
            }
        )
    return pd.DataFrame(rows).head(MAX_COMPONENTS)


def component_memberships(
    tcell_df: pd.DataFrame,
    components: list[list[int]],
    summary_df: pd.DataFrame,
) -> pd.DataFrame:
    displayed_components = set(summary_df["component"].astype(int))
    rows = []
    for component_idx, component in enumerate(sorted(components, key=len, reverse=True), start=1):
        if component_idx not in displayed_components:
            continue
        for profile_idx in component:
            row = tcell_df.iloc[profile_idx]
            rows.append(
                {
                    "component": component_idx,
                    "source_corpus": row["source_corpus"],
                    "paper_id": row["paper_id"],
                    "paper_key": row["paper_key"],
                    "cell_type": row["cell_type"],
                    "normalized_cell_type": normalize_label(row["cell_type"]),
                    "n_markers": row["n_markers"],
                    "marker_names": row["marker_names"],
                    "marker_ids": row["marker_ids"],
                    "dominant_module": row["dominant_module"],
                }
            )
    return pd.DataFrame(rows)


def wrap_text(text: str, width: int, max_lines: int) -> str:
    words = text.split()
    lines = []
    current = []
    for word in words:
        candidate = " ".join([*current, word])
        if len(candidate) <= width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
        if len(lines) == max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(" ".join(current))
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = lines[-1].rstrip(".;") + "..."
    return "\n".join(lines)


def compact_list(text: str, max_items: int) -> str:
    items = [item.strip() for item in text.split(";") if item.strip()]
    if len(items) <= max_items:
        return ", ".join(items)
    return ", ".join(items[:max_items]) + f", +{len(items) - max_items}"


def draw_summary(summary_df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(8.4, 4.75))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, len(summary_df) + 1.25)
    ax.axis("off")

    x_cluster = 0.02
    x_genes = 0.19
    x_labels = 0.42
    x_bar = 0.73
    bar_width = 0.23

    header_y = len(summary_df) + 0.68
    ax.text(x_cluster, header_y, "Marker group", fontsize=7.6, fontweight="bold", ha="left", va="bottom")
    ax.text(x_genes, header_y, "Shared marker genes", fontsize=7.6, fontweight="bold", ha="left", va="bottom")
    ax.text(x_labels, header_y, "Most common labels", fontsize=7.6, fontweight="bold", ha="left", va="bottom")
    ax.text(x_bar, header_y, "Label relation inside marker group", fontsize=7.6, fontweight="bold", ha="left", va="bottom")

    for row_number, row in enumerate(summary_df.itertuples(index=False)):
        y = len(summary_df) - row_number
        ax.axhline(y - 0.43, color="#d0d0d0", linewidth=0.45)

        group_label = f"C{row.component}\n{row.dominant_program}\n{row.profiles} profiles, {row.papers} papers"
        ax.text(x_cluster, y, group_label, fontsize=6.8, ha="left", va="center", linespacing=1.15)
        ax.text(
            x_genes,
            y,
            wrap_text(compact_list(row.core_marker_genes, max_items=5), width=25, max_lines=3),
            fontsize=6.6,
            ha="left",
            va="center",
            linespacing=1.2,
        )
        ax.text(
            x_labels,
            y,
            wrap_text(row.top_labels.replace("; ", "; "), width=36, max_lines=3),
            fontsize=6.3,
            ha="left",
            va="center",
            linespacing=1.22,
        )

        fractions = [
            row.exact_label_fraction,
            row.partial_label_fraction,
            row.different_label_fraction,
        ]
        counts = [row.exact_label_pairs, row.partial_label_pairs, row.different_label_pairs]
        left = x_bar
        for relation, fraction, count in zip(RELATION_ORDER, fractions, counts, strict=True):
            width = bar_width * fraction
            ax.add_patch(
                plt.Rectangle(
                    (left, y - 0.115),
                    width,
                    0.23,
                    facecolor=RELATION_COLORS[relation],
                    edgecolor="#222222",
                    linewidth=0.35,
                )
            )
            if width > 0.028:
                ax.text(left + width / 2, y, str(count), fontsize=5.9, ha="center", va="center")
            left += width
        ax.add_patch(
            plt.Rectangle(
                (x_bar, y - 0.115),
                bar_width,
                0.23,
                facecolor="none",
                edgecolor="#222222",
                linewidth=0.45,
            )
        )
        ax.text(
            x_bar + bar_width + 0.012,
            y,
            f"{row.labels} labels\nJ={row.mean_internal_jaccard:.2f}",
            fontsize=6.0,
            ha="left",
            va="center",
            linespacing=1.2,
        )

    legend_y = 0.34
    legend_x = x_bar
    for idx, relation in enumerate(RELATION_ORDER):
        x = legend_x + idx * 0.085
        ax.add_patch(
            plt.Rectangle(
                (x, legend_y),
                0.018,
                0.09,
                facecolor=RELATION_COLORS[relation],
                edgecolor="#222222",
                linewidth=0.35,
            )
        )
        ax.text(x + 0.023, legend_y + 0.045, relation, fontsize=6.4, ha="left", va="center")

    fig.text(
        0.02,
        0.025,
        f"Marker groups are connected components of cross-paper T-cell profiles with marker-gene Jaccard >= {JACCARD_THRESHOLD:.2f}; label relations are scored across cross-paper profile pairs within each group.",
        ha="left",
        va="bottom",
        fontsize=6.5,
    )
    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    fig.savefig(FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)


def write_report(summary_df: pd.DataFrame, tcell_df: pd.DataFrame) -> None:
    report = [
        "# T-cell Marker Cluster Summary",
        "",
        "## Assumptions",
        "",
        "- Unit of analysis is one paper-celltype marker profile: a paper, a reported cell type label, and a binary vector of mapped Ensembl gene IDs.",
        "- Profiles are restricted to human, source-verified marker records with at least three mapped marker genes.",
        "- T-cell profiles are selected by the existing regex-based neighborhood assignment; mixed T/NK labels are not included in this first pass.",
        f"- Marker groups are connected components of cross-paper profiles with marker-gene Jaccard >= {JACCARD_THRESHOLD:.2f}.",
        "- Label relation summaries are computed across cross-paper profile pairs within each marker group.",
        "- Dominant programs are heuristic labels based on manually specified immune-state gene modules; they are used for orientation, not as a proposed taxonomy.",
        "",
        "## Outputs",
        "",
        f"- Figure: `{FIGURE_PATH.relative_to(REPO_ROOT)}`",
        f"- Summary table: `{SUMMARY_PATH.relative_to(REPO_ROOT)}`",
        f"- Membership table: `{MEMBERSHIP_PATH.relative_to(REPO_ROOT)}`",
        "",
        "## Counts",
        "",
        f"- T-cell profiles: {len(tcell_df):,}",
        f"- Papers: {tcell_df['paper_key'].nunique():,}",
        f"- Reported labels: {tcell_df['cell_type'].nunique():,}",
        f"- Marker groups displayed: {len(summary_df):,}",
        "",
        "## Marker Group Summary",
        "",
        markdown_table(
            summary_df[
                [
                    "component",
                    "profiles",
                    "papers",
                    "labels",
                    "dominant_program",
                    "core_marker_genes",
                    "top_labels",
                    "exact_label_fraction",
                    "partial_label_fraction",
                    "different_label_fraction",
                    "mean_internal_jaccard",
                ]
            ]
        ),
        "",
    ]
    REPORT_PATH.write_text("\n".join(report))


def main() -> None:
    records_df = build_records()
    profiles_df, filtered_profiles_df, _filtered_profiles, id_to_name = build_profile_summary(
        records_df,
        min_markers=MIN_MARKERS,
        feature_id_col="feature_id_std",
        feature_name_col="feature_name_std",
    )
    filtered_profiles_df["neighborhood"] = filtered_profiles_df["cell_type"].map(assign_neighborhood)
    tcell_df = filtered_profiles_df.loc[filtered_profiles_df["neighborhood"].eq("T cell")].copy().reset_index(drop=True)

    profile_gene_sets = marker_sets(tcell_df)
    gene_vocab = sorted(set().union(*profile_gene_sets))
    name_to_ids = build_name_to_ids(records_df)
    module_genes_df = module_gene_rows(name_to_ids, set(gene_vocab))
    module_scores_df = profile_module_scores(profile_gene_sets, module_genes_df)
    tcell_df["profile_index"] = np.arange(len(tcell_df))
    tcell_df = tcell_df.merge(module_scores_df, on="profile_index", how="left")

    components, edges = connected_components(
        profile_gene_sets,
        tcell_df["paper_key"].tolist(),
        threshold=JACCARD_THRESHOLD,
    )
    summary_df = summarize_components(tcell_df, profile_gene_sets, id_to_name, components, edges)
    membership_df = component_memberships(tcell_df, components, summary_df)
    summary_df.to_csv(SUMMARY_PATH, sep="\t", index=False)
    membership_df.to_csv(MEMBERSHIP_PATH, sep="\t", index=False)
    draw_summary(summary_df)
    write_report(summary_df, tcell_df)

    print(f"T-cell profiles: {len(tcell_df):,}")
    print(f"Components displayed: {len(summary_df):,}")
    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MEMBERSHIP_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
