from __future__ import annotations

import re
import unicodedata
from itertools import combinations

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
