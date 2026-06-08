#!/usr/bin/env python3
"""Prototype ontology-neighbor consistency with marker-gene neighbors.

This analysis asks whether Cell Ontology mappings produce neighborhoods that
are more consistent with marker-gene profiles than raw reported labels. It is
designed for the small ontology pilot outputs, not as a final full-corpus
analysis.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import sqlite3
import unicodedata
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from build_cell_ontology_mapping import DEFAULT_DB, DEFAULT_ONTOLOGY, RESULTS_DIR, parse_obo


DEFAULT_MAPPINGS = RESULTS_DIR / "profile_cell_ontology_pilot18_mappings.jsonl"
DEFAULT_OUT_PREFIX = RESULTS_DIR / "profile_cell_ontology_pilot18_neighbor_consistency"
DEFAULT_FIGURE = Path(__file__).resolve().parents[1] / "analysis" / "figures" / "fig_ontology_neighbor_consistency_pilot18.pdf"

GENERIC_LABEL_TOKENS = {
    "a",
    "an",
    "and",
    "cell",
    "cells",
    "cluster",
    "clusters",
    "group",
    "high",
    "low",
    "positive",
    "population",
    "populations",
    "type",
    "types",
}


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_label(value: object) -> str:
    text = unicodedata.normalize("NFKD", clean_text(value)).encode("ascii", "ignore").decode("ascii")
    text = text.upper()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    text = re.sub(r"(?<=[A-Z])(?=[0-9])", " ", text)
    text = re.sub(r"(?<=[0-9])(?=[A-Z])", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def label_tokens(label: str) -> set[str]:
    return {
        token.lower()
        for token in normalize_label(label).split()
        if token.lower() not in GENERIC_LABEL_TOKENS and len(token) >= 2
    }


def label_similarity(left: str, right: str) -> float:
    left_norm = normalize_label(left)
    right_norm = normalize_label(right)
    if left_norm and left_norm == right_norm:
        return 1.0
    if not left_norm or not right_norm:
        return 0.0

    padded_left = f" {left_norm} "
    padded_right = f" {right_norm} "
    if padded_left in padded_right or padded_right in padded_left:
        return 0.75

    left_tokens = label_tokens(left)
    right_tokens = label_tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def load_mappings(path: Path, *, basis: str) -> pd.DataFrame:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("basis") != basis:
                continue
            rows.append(
                {
                    "profile_id": int(row["profile_id"]),
                    "paper_id": int(row["paper_id"]),
                    "collection": row.get("collection"),
                    "reported_label": row.get("reported_label"),
                    "gene_names": row.get("gene_names") or [],
                    "cl_id": row.get("cl_id"),
                    "cl_label": row.get("cl_label"),
                    "confidence": row.get("confidence"),
                    "doi": row.get("doi"),
                    "title": row.get("title"),
                    "year": row.get("year"),
                }
            )
    return pd.DataFrame(rows).sort_values("profile_id").reset_index(drop=True)


def add_gene_ids_from_db(mappings_df: pd.DataFrame, db_path: Path) -> pd.DataFrame:
    profile_ids = mappings_df["profile_id"].astype(int).tolist()
    if not profile_ids:
        return mappings_df.assign(gene_ids=[[] for _ in range(len(mappings_df))])
    placeholders = ",".join("?" for _ in profile_ids)
    query = f"SELECT profile_id, gene_ids_json FROM profiles WHERE profile_id IN ({placeholders})"
    with sqlite3.connect(db_path) as conn:
        gene_json = {int(row[0]): row[1] for row in conn.execute(query, profile_ids)}
    mappings_df = mappings_df.copy()
    mappings_df["gene_ids"] = [
        sorted({clean_text(value) for value in json.loads(gene_json.get(int(profile_id), "[]")) if clean_text(value)})
        for profile_id in mappings_df["profile_id"]
    ]
    return mappings_df


def ancestor_distances(cl_id: str | None, parents: dict[str, list[str]]) -> dict[str, int]:
    if not cl_id or cl_id not in parents:
        return {}
    distances = {cl_id: 0}
    queue = deque([cl_id])
    while queue:
        current = queue.popleft()
        for parent in parents.get(current, []):
            if parent not in distances:
                distances[parent] = distances[current] + 1
                queue.append(parent)
    return distances


def ontology_similarity(left_id: str | None, right_id: str | None, parents: dict[str, list[str]]) -> tuple[float, str | None, int | None]:
    if not left_id or not right_id:
        return 0.0, None, None
    left_anc = ancestor_distances(left_id, parents)
    right_anc = ancestor_distances(right_id, parents)
    if not left_anc or not right_anc:
        return 0.0, None, None
    shared = set(left_anc) & set(right_anc)
    if not shared:
        return 0.0, None, None
    common = min(shared, key=lambda cl_id: (left_anc[cl_id] + right_anc[cl_id], max(left_anc[cl_id], right_anc[cl_id])))
    graph_distance = left_anc[common] + right_anc[common]
    if common == "CL:0000000" and graph_distance > 0:
        return 0.0, common, graph_distance
    return 1.0 / (1.0 + graph_distance), common, graph_distance


def jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def ontology_relation(row: pd.Series) -> str:
    if not row.cl_id_i or not row.cl_id_j or pd.isna(row.cl_id_i) or pd.isna(row.cl_id_j):
        return "unmapped"
    if row.cl_id_i == row.cl_id_j:
        return "same_term"
    if pd.notna(row.ontology_graph_distance) and row.ontology_graph_distance <= 2:
        return "close_parent_child"
    if row.ontology_similarity > 0:
        return "shared_ancestor"
    return "different_branch"


def marker_relation(marker_jaccard: float) -> str:
    if math.isclose(marker_jaccard, 1.0):
        return "exact"
    if marker_jaccard > 0:
        return "partial"
    return "none"


def rank_neighbors(pair_df: pd.DataFrame, score_col: str, *, k: int) -> dict[int, list[int]]:
    neighbors: dict[int, list[tuple[int, float, float, int]]] = defaultdict(list)
    for row in pair_df.itertuples(index=False):
        left = int(row.profile_i)
        right = int(row.profile_j)
        score = float(getattr(row, score_col))
        marker_score = float(row.marker_jaccard)
        if score <= 0:
            continue
        neighbors[left].append((right, score, marker_score, right))
        neighbors[right].append((left, score, marker_score, left))
    ranked = {}
    for profile_idx, values in neighbors.items():
        values = sorted(values, key=lambda item: (-item[1], -item[2], item[3]))
        ranked[profile_idx] = [neighbor_idx for neighbor_idx, _score, _marker_score, _tie in values[:k]]
    return ranked


def random_neighbor_sets(profile_indices: list[int], eligible: dict[int, list[int]], *, k: int, seed: int) -> dict[int, list[int]]:
    rng = random.Random(seed)
    random_sets = {}
    for profile_idx in profile_indices:
        candidates = eligible[profile_idx]
        if len(candidates) < k:
            continue
        random_sets[profile_idx] = rng.sample(candidates, k)
    return random_sets


def compare_neighbor_sets(
    profiles_df: pd.DataFrame,
    pair_lookup: dict[tuple[int, int], dict[str, float]],
    source_neighbors: dict[int, list[int]],
    gene_neighbors: dict[int, list[int]],
    random_neighbors: dict[int, list[int]],
    *,
    k: int,
    source_name: str,
) -> list[dict[str, object]]:
    rows = []
    for profile_idx, source_set_list in source_neighbors.items():
        if profile_idx not in gene_neighbors or len(source_set_list) < k or len(gene_neighbors[profile_idx]) < k:
            continue
        gene_set = set(gene_neighbors[profile_idx][:k])
        source_set = set(source_set_list[:k])
        random_set = set(random_neighbors.get(profile_idx, [])[:k])
        for comparison, neighbor_set in (("Observed", source_set), ("Random", random_set)):
            if len(neighbor_set) < k:
                continue
            overlap_n = len(neighbor_set & gene_set)
            union_n = len(neighbor_set | gene_set)
            marker_scores = []
            ontology_scores = []
            for neighbor_idx in neighbor_set:
                pair = tuple(sorted((profile_idx, neighbor_idx)))
                if pair in pair_lookup:
                    marker_scores.append(pair_lookup[pair]["marker_jaccard"])
                    ontology_scores.append(pair_lookup[pair]["ontology_similarity"])
            row = profiles_df.iloc[profile_idx]
            rows.append(
                {
                    "source": source_name,
                    "comparison": comparison,
                    "k": k,
                    "profile_index": profile_idx,
                    "profile_id": int(row.profile_id),
                    "reported_label": row.reported_label,
                    "cl_id": row.cl_id,
                    "cl_label": row.cl_label,
                    "overlap_n": overlap_n,
                    "overlap_at_k": overlap_n / k,
                    "jaccard_at_k": overlap_n / union_n if union_n else 0.0,
                    "mean_marker_jaccard_to_neighbors": float(np.mean(marker_scores)) if marker_scores else 0.0,
                    "mean_ontology_similarity_to_neighbors": float(np.mean(ontology_scores)) if ontology_scores else 0.0,
                }
            )
    return rows


def summarize_neighbors(rows: list[dict[str, object]]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return (
        df.groupby(["source", "comparison", "k"], sort=True)
        .agg(
            profiles=("profile_id", "nunique"),
            mean_overlap_at_k=("overlap_at_k", "mean"),
            median_overlap_at_k=("overlap_at_k", "median"),
            mean_jaccard_at_k=("jaccard_at_k", "mean"),
            mean_marker_jaccard_to_neighbors=("mean_marker_jaccard_to_neighbors", "mean"),
            median_marker_jaccard_to_neighbors=("mean_marker_jaccard_to_neighbors", "median"),
            mean_ontology_similarity_to_neighbors=("mean_ontology_similarity_to_neighbors", "mean"),
        )
        .reset_index()
    )


def summarize_pair_relations(pair_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pair_df.copy()
    df["ontology_relation"] = df.apply(ontology_relation, axis=1)
    df["marker_relation"] = df["marker_jaccard"].map(marker_relation)
    joint_df = (
        df.groupby(["ontology_relation", "marker_relation"], sort=True)
        .agg(
            n_pairs=("marker_jaccard", "size"),
            mean_marker_jaccard=("marker_jaccard", "mean"),
            median_marker_jaccard=("marker_jaccard", "median"),
        )
        .reset_index()
    )
    relation_df = (
        df.groupby("ontology_relation", sort=True)
        .agg(
            n_pairs=("marker_jaccard", "size"),
            n_marker_positive=("marker_jaccard", lambda values: int((values > 0).sum())),
            fraction_marker_positive=("marker_jaccard", lambda values: float((values > 0).mean())),
            mean_marker_jaccard=("marker_jaccard", "mean"),
            median_marker_jaccard=("marker_jaccard", "median"),
        )
        .reset_index()
        .sort_values(["mean_marker_jaccard", "fraction_marker_positive"], ascending=False)
    )
    return joint_df, relation_df


def rank_correlation(left: np.ndarray, right: np.ndarray) -> float:
    if len(left) < 3:
        return float("nan")
    left_rank = pd.Series(left).rank(method="average").to_numpy()
    right_rank = pd.Series(right).rank(method="average").to_numpy()
    if np.std(left_rank) == 0 or np.std(right_rank) == 0:
        return float("nan")
    return float(np.corrcoef(left_rank, right_rank)[0, 1])


def make_pair_df(profiles_df: pd.DataFrame, terms: dict) -> pd.DataFrame:
    parents = {cl_id: term.parents for cl_id, term in terms.items()}
    rows = []
    gene_sets = [set(value) for value in profiles_df["gene_ids"]]
    for left, right in combinations(range(len(profiles_df)), 2):
        left_row = profiles_df.iloc[left]
        right_row = profiles_df.iloc[right]
        marker_j = jaccard(gene_sets[left], gene_sets[right])
        ontology_sim, common_id, graph_distance = ontology_similarity(left_row.cl_id, right_row.cl_id, parents)
        label_sim = label_similarity(left_row.reported_label, right_row.reported_label)
        rows.append(
            {
                "profile_i": left,
                "profile_j": right,
                "profile_id_i": int(left_row.profile_id),
                "profile_id_j": int(right_row.profile_id),
                "label_i": left_row.reported_label,
                "label_j": right_row.reported_label,
                "cl_id_i": left_row.cl_id,
                "cl_id_j": right_row.cl_id,
                "cl_label_i": left_row.cl_label,
                "cl_label_j": right_row.cl_label,
                "marker_jaccard": marker_j,
                "ontology_similarity": ontology_sim,
                "ontology_common_id": common_id,
                "ontology_graph_distance": graph_distance,
                "label_similarity": label_sim,
                "same_paper": int(left_row.paper_id) == int(right_row.paper_id),
            }
        )
    return pd.DataFrame(rows)


def write_tsv(path: Path, df: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, sep="\t", index=False)


def make_figure(summary_df: pd.DataFrame, pair_df: pd.DataFrame, figure_path: Path) -> None:
    if summary_df.empty:
        return
    figure_path.parent.mkdir(parents=True, exist_ok=True)
    k = int(summary_df["k"].max())
    plot_df = summary_df.loc[summary_df["k"].eq(k)].copy()
    sources = ["Ontology", "Label"]
    observed = [
        plot_df.loc[(plot_df["source"].eq(source)) & (plot_df["comparison"].eq("Observed")), "mean_overlap_at_k"].mean()
        for source in sources
    ]
    random_values = [
        plot_df.loc[(plot_df["source"].eq(source)) & (plot_df["comparison"].eq("Random")), "mean_overlap_at_k"].mean()
        for source in sources
    ]

    fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.7), gridspec_kw={"width_ratios": [1.0, 1.15]})

    x = np.arange(len(sources))
    width = 0.36
    axes[0].bar(x - width / 2, observed, width, label="Observed", color="#9ecae1", edgecolor="black", linewidth=0.7)
    axes[0].bar(x + width / 2, random_values, width, label="Random", color="#d9d9d9", edgecolor="black", linewidth=0.7)
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(sources)
    axes[0].set_ylim(0, 1)
    axes[0].set_ylabel(f"Mean overlap with\ngene neighbors@{k}")
    axes[0].legend(frameon=False, fontsize=7)
    axes[0].spines[["top", "right"]].set_visible(False)

    axes[1].scatter(
        pair_df["ontology_similarity"],
        pair_df["marker_jaccard"],
        s=24,
        color="#737373",
        edgecolor="black",
        linewidth=0.3,
    )
    axes[1].set_xlim(-0.02, 1.02)
    axes[1].set_ylim(-0.02, 1.02)
    axes[1].set_xlabel("Ontology similarity")
    axes[1].set_ylabel("Marker-gene Jaccard")
    axes[1].spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(figure_path, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mappings", type=Path, default=DEFAULT_MAPPINGS)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--ontology", type=Path, default=DEFAULT_ONTOLOGY)
    parser.add_argument("--out-prefix", type=Path, default=DEFAULT_OUT_PREFIX)
    parser.add_argument("--figure-out", type=Path, default=DEFAULT_FIGURE)
    parser.add_argument("--basis", default="full_context", choices=["full_context", "label_context", "marker_context"])
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--include-same-paper", action="store_true")
    args = parser.parse_args()

    terms = parse_obo(args.ontology)
    profiles_df = add_gene_ids_from_db(load_mappings(args.mappings, basis=args.basis), args.db)
    pair_df = make_pair_df(profiles_df, terms)
    if not args.include_same_paper:
        pair_df = pair_df.loc[~pair_df["same_paper"]].reset_index(drop=True)

    profile_indices = sorted(set(pair_df["profile_i"]) | set(pair_df["profile_j"]))
    eligible = {
        profile_idx: sorted(
            {
                int(row.profile_j if int(row.profile_i) == profile_idx else row.profile_i)
                for row in pair_df.loc[(pair_df["profile_i"].eq(profile_idx)) | (pair_df["profile_j"].eq(profile_idx))].itertuples(index=False)
            }
        )
        for profile_idx in profile_indices
    }
    pair_lookup = {
        tuple(sorted((int(row.profile_i), int(row.profile_j)))): {
            "marker_jaccard": float(row.marker_jaccard),
            "ontology_similarity": float(row.ontology_similarity),
            "label_similarity": float(row.label_similarity),
        }
        for row in pair_df.itertuples(index=False)
    }

    gene_neighbors = rank_neighbors(pair_df, "marker_jaccard", k=args.k)
    ontology_neighbors = rank_neighbors(pair_df, "ontology_similarity", k=args.k)
    label_neighbors = rank_neighbors(pair_df, "label_similarity", k=args.k)
    random_neighbors = random_neighbor_sets(profile_indices, eligible, k=args.k, seed=args.seed)

    rows = []
    rows.extend(
        compare_neighbor_sets(
            profiles_df,
            pair_lookup,
            ontology_neighbors,
            gene_neighbors,
            random_neighbors,
            k=args.k,
            source_name="Ontology",
        )
    )
    rows.extend(
        compare_neighbor_sets(
            profiles_df,
            pair_lookup,
            label_neighbors,
            gene_neighbors,
            random_neighbors,
            k=args.k,
            source_name="Label",
        )
    )

    neighbor_df = pd.DataFrame(rows)
    summary_df = summarize_neighbors(rows)
    joint_relation_df, relation_summary_df = summarize_pair_relations(pair_df)
    pair_summary_df = pd.DataFrame(
        [
            {
                "n_profiles": len(profiles_df),
                "n_pairs": len(pair_df),
                "n_pairs_marker_positive": int((pair_df["marker_jaccard"] > 0).sum()),
                "n_pairs_ontology_positive": int((pair_df["ontology_similarity"] > 0).sum()),
                "spearman_marker_vs_ontology": rank_correlation(pair_df["marker_jaccard"].to_numpy(), pair_df["ontology_similarity"].to_numpy()),
                "spearman_marker_vs_label": rank_correlation(pair_df["marker_jaccard"].to_numpy(), pair_df["label_similarity"].to_numpy()),
                "mean_marker_jaccard_when_ontology_positive": float(pair_df.loc[pair_df["ontology_similarity"] > 0, "marker_jaccard"].mean()),
                "mean_marker_jaccard_when_label_positive": float(pair_df.loc[pair_df["label_similarity"] > 0, "marker_jaccard"].mean()),
                "mean_marker_jaccard_all_pairs": float(pair_df["marker_jaccard"].mean()),
            }
        ]
    )

    write_tsv(args.out_prefix.with_suffix(".pairs.tsv"), pair_df)
    write_tsv(args.out_prefix.with_suffix(".neighbors.tsv"), neighbor_df)
    write_tsv(args.out_prefix.with_suffix(".summary.tsv"), summary_df)
    write_tsv(args.out_prefix.with_suffix(".joint_relations.tsv"), joint_relation_df)
    write_tsv(args.out_prefix.with_suffix(".relation_summary.tsv"), relation_summary_df)
    write_tsv(args.out_prefix.with_suffix(".pair_summary.tsv"), pair_summary_df)
    make_figure(summary_df, pair_df, args.figure_out)

    print(f"Wrote pairs: {args.out_prefix.with_suffix('.pairs.tsv')}")
    print(f"Wrote neighbors: {args.out_prefix.with_suffix('.neighbors.tsv')}")
    print(f"Wrote summary: {args.out_prefix.with_suffix('.summary.tsv')}")
    print(f"Wrote joint relations: {args.out_prefix.with_suffix('.joint_relations.tsv')}")
    print(f"Wrote relation summary: {args.out_prefix.with_suffix('.relation_summary.tsv')}")
    print(f"Wrote pair summary: {args.out_prefix.with_suffix('.pair_summary.tsv')}")
    print(f"Wrote figure: {args.figure_out}")
    print(pair_summary_df.to_string(index=False))
    if not summary_df.empty:
        print(summary_df.to_string(index=False))
    print(relation_summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
