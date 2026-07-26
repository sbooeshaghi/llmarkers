#!/usr/bin/env python3
"""Analyze marker-panel reuse in the validated mrkr corpus database."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
import re
import sqlite3
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


SCHEMA_VERSION = "llmarkers.mrkr-corpus-analysis.v1"
DEFAULT_MIN_MARKERS = 3
RANDOM_SEED = 20260722


@dataclass(frozen=True)
class Profile:
    profile_id: str
    paper_key: str
    article_key: str
    collection: str
    target_key: str
    target_label: str
    genes: frozenset[str]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def normalize_label(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().strip()
    value = value.replace("\u2010", "-").replace("\u2011", "-")
    value = re.sub(r"[^\w]+", " ", value, flags=re.UNICODE)
    return " ".join(value.split())


def stable_id(*parts: str) -> str:
    return hashlib.sha256("\t".join(parts).encode("utf-8")).hexdigest()[:20]


def jaccard(left: set[str] | frozenset[str], right: set[str] | frozenset[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else math.nan


def stable_mean(values: list[float]) -> float:
    return math.fsum(values) / len(values) if values else math.nan


def size_bin(size: int) -> int:
    return int(math.floor(math.log2(max(size, 1))))


def read_source_manifest(path: Path, repo_root: Path) -> dict[str, Path]:
    sources: dict[str, Path] = {}
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), 1
    ):
        if not line or line.startswith("#") or line.startswith("paper_id\t"):
            continue
        fields = line.split("\t")
        if len(fields) != 5:
            raise ValueError(f"{path}:{line_number}: expected five fields")
        paper_id, collection, _, manuscript, _ = fields
        manuscript_path = Path(manuscript)
        if not manuscript_path.is_absolute():
            manuscript_path = repo_root / manuscript_path
        sources[f"{collection}:{paper_id}"] = manuscript_path
    return sources


def manuscript_title(path: Path) -> str:
    if not path.is_file():
        return ""
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            if line.startswith("# "):
                return line[2:].strip()
    return ""


def load_papers(
    connection: sqlite3.Connection,
    source_manifest: Path,
    repo_root: Path,
) -> pd.DataFrame:
    papers = pd.read_sql_query(
        "SELECT paper_key, paper_id, collection, organism, source_sha256 FROM papers",
        connection,
    )
    sources = read_source_manifest(source_manifest, repo_root)
    papers["manuscript"] = papers.paper_key.map(lambda key: str(sources.get(key, "")))
    papers["title"] = papers.paper_key.map(
        lambda key: manuscript_title(sources[key]) if key in sources else ""
    )
    papers["title_key"] = papers.title.map(normalize_label)
    papers["article_key"] = papers.apply(
        lambda row: (
            f"title:{row.title_key}" if row.title_key else f"source:{row.source_sha256}"
        ),
        axis=1,
    )
    return papers


def load_semantic_exact(path: Path) -> set[tuple[str, str]]:
    audit = pd.read_csv(path, sep="\t", dtype={"curie": str, "observed_label": str})
    audit = audit[(audit.term_type == "celltype") & (audit.semantic_exact == 1)]
    return set(zip(audit.curie, audit.observed_label, strict=False))


def ontology_audit_summary(path: Path) -> dict[str, int]:
    audit = pd.read_csv(path, sep="\t")
    targets = audit[audit.term_type == "celltype"]
    return {
        "observed_target_mappings": len(targets),
        "semantic_exact_target_mappings": int((targets.semantic_exact == 1).sum()),
        "current_exact_target_mappings": int((targets.current_exact == 1).sum()),
        "full_span_only_target_mappings": int(
            ((targets.current_exact == 1) & (targets.semantic_exact == 0)).sum()
        ),
    }


def load_marker_evidence(connection: sqlite3.Connection) -> pd.DataFrame:
    evidence = pd.read_sql_query(
        """
        SELECT paper_key, claim_key, target_label, target_curie, target_exact,
               gene_symbol, gene_curie, gene_exact, direction
        FROM marker_evidence
        """,
        connection,
    )
    evidence["target_key"] = evidence.target_label.map(normalize_label)
    return evidence


def representative_gene_symbols(evidence: pd.DataFrame) -> dict[str, str]:
    mapped = evidence[evidence.gene_curie.notna()]
    counts = (
        mapped.groupby(["gene_curie", "gene_symbol"], dropna=False)
        .size()
        .reset_index(name="n")
        .sort_values(["gene_curie", "n", "gene_symbol"], ascending=[True, False, True])
    )
    return (
        counts.drop_duplicates("gene_curie")
        .set_index("gene_curie")
        .gene_symbol.to_dict()
    )


def build_profiles(
    evidence: pd.DataFrame,
    papers: pd.DataFrame,
    *,
    target_mode: str,
    semantic_exact: set[tuple[str, str]],
    direction: str = "positive",
) -> list[Profile]:
    mapped = evidence[
        evidence.gene_curie.notna()
        & (evidence.direction.fillna("positive") == direction)
    ].copy()
    if target_mode == "label":
        mapped["analysis_target"] = mapped.target_key
    elif target_mode == "ontology":
        mapped = mapped[
            mapped.apply(
                lambda row: (row.target_curie, row.target_label) in semantic_exact,
                axis=1,
            )
        ].copy()
        mapped["analysis_target"] = mapped.target_curie
    else:
        raise ValueError(f"unknown target mode: {target_mode}")

    paper_lookup = papers.set_index("paper_key").to_dict("index")
    profiles: list[Profile] = []
    for (paper_key, target_key), group in mapped.groupby(
        ["paper_key", "analysis_target"], sort=True
    ):
        if not target_key or paper_key not in paper_lookup:
            continue
        labels = Counter(group.target_label)
        label = sorted(labels, key=lambda value: (-labels[value], value))[0]
        paper = paper_lookup[paper_key]
        profiles.append(
            Profile(
                profile_id="profile:" + stable_id(target_mode, paper_key, target_key),
                paper_key=paper_key,
                article_key=paper["article_key"],
                collection=paper["collection"],
                target_key=target_key,
                target_label=label,
                genes=frozenset(group.gene_curie),
            )
        )
    return profiles


def profile_frame(profiles: list[Profile], symbols: dict[str, str]) -> pd.DataFrame:
    rows = []
    for profile in profiles:
        genes = sorted(profile.genes)
        rows.append(
            {
                "profile_id": profile.profile_id,
                "paper_key": profile.paper_key,
                "article_key": profile.article_key,
                "collection": profile.collection,
                "target_key": profile.target_key,
                "target_label": profile.target_label,
                "marker_count": len(genes),
                "gene_curies": " | ".join(genes),
                "gene_symbols": " | ".join(symbols.get(gene, gene) for gene in genes),
            }
        )
    return pd.DataFrame(rows)


def build_same_target_pairs(
    profiles: list[Profile],
    paper_targets: dict[str, set[str]],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    grouped: dict[str, list[Profile]] = defaultdict(list)
    for profile in profiles:
        grouped[profile.target_key].append(profile)
    for target_key, group in sorted(grouped.items()):
        for left, right in itertools.combinations(group, 2):
            if left.article_key == right.article_key:
                continue
            intersection = left.genes & right.genes
            union = left.genes | right.genes
            left_context = paper_targets[left.paper_key] - {target_key}
            right_context = paper_targets[right.paper_key] - {target_key}
            rows.append(
                {
                    "pair_id": "pair:" + stable_id(left.profile_id, right.profile_id),
                    "target_key": target_key,
                    "target_label": left.target_label,
                    "target_label_a": left.target_label,
                    "target_label_b": right.target_label,
                    "profile_a": left.profile_id,
                    "profile_b": right.profile_id,
                    "paper_a": left.paper_key,
                    "paper_b": right.paper_key,
                    "collection_pair": "-".join(
                        sorted([left.collection, right.collection])
                    ),
                    "markers_a": len(left.genes),
                    "markers_b": len(right.genes),
                    "shared_markers": len(intersection),
                    "union_markers": len(union),
                    "any_shared_marker": int(bool(intersection)),
                    "marker_jaccard": len(intersection) / len(union),
                    "recovery_a_from_b": len(intersection) / len(left.genes),
                    "recovery_b_from_a": len(intersection) / len(right.genes),
                    "mean_directional_recovery": 0.5
                    * (
                        len(intersection) / len(left.genes)
                        + len(intersection) / len(right.genes)
                    ),
                    "context_a": len(left_context),
                    "context_b": len(right_context),
                    "context_jaccard": jaccard(left_context, right_context),
                }
            )
    return pd.DataFrame(rows)


def sample_matched_controls(
    same_pairs: pd.DataFrame,
    profiles: list[Profile],
    *,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    rng = random.Random(seed)
    profile_lookup = {profile.profile_id: profile for profile in profiles}
    buckets: dict[tuple[str, int], list[Profile]] = defaultdict(list)
    for profile in profiles:
        buckets[(profile.collection, size_bin(len(profile.genes)))].append(profile)

    rows = []
    for pair in same_pairs.itertuples(index=False):
        original_a = profile_lookup[pair.profile_a]
        original_b = profile_lookup[pair.profile_b]
        candidates_a = buckets[(original_a.collection, size_bin(len(original_a.genes)))]
        candidates_b = buckets[(original_b.collection, size_bin(len(original_b.genes)))]
        selected: tuple[Profile, Profile] | None = None
        for _ in range(500):
            left = rng.choice(candidates_a)
            right = rng.choice(candidates_b)
            if (
                left.article_key == right.article_key
                or left.target_key == right.target_key
            ):
                continue
            selected = left, right
            break
        if selected is None:
            continue
        left, right = selected
        intersection = left.genes & right.genes
        union = left.genes | right.genes
        rows.append(
            {
                "source_pair_id": pair.pair_id,
                "source_target_key": pair.target_key,
                "profile_a": left.profile_id,
                "profile_b": right.profile_id,
                "paper_a": left.paper_key,
                "paper_b": right.paper_key,
                "target_a": left.target_key,
                "target_b": right.target_key,
                "collection_pair": "-".join(
                    sorted([left.collection, right.collection])
                ),
                "markers_a": len(left.genes),
                "markers_b": len(right.genes),
                "shared_markers": len(intersection),
                "union_markers": len(union),
                "any_shared_marker": int(bool(intersection)),
                "marker_jaccard": len(intersection) / len(union),
                "recovery_a_from_b": len(intersection) / len(left.genes),
                "recovery_b_from_a": len(intersection) / len(right.genes),
                "mean_directional_recovery": 0.5
                * (
                    len(intersection) / len(left.genes)
                    + len(intersection) / len(right.genes)
                ),
            }
        )
    return pd.DataFrame(rows)


def summarize_pairs(pairs: pd.DataFrame, comparison: str) -> dict[str, object]:
    if pairs.empty:
        return {
            "comparison": comparison,
            "pairs": 0,
            "any_shared_marker_fraction": math.nan,
            "mean_marker_jaccard": math.nan,
            "median_marker_jaccard": math.nan,
            "mean_shared_markers": math.nan,
            "mean_directional_recovery": math.nan,
        }
    return {
        "comparison": comparison,
        "pairs": len(pairs),
        "any_shared_marker_fraction": pairs.any_shared_marker.mean(),
        "mean_marker_jaccard": pairs.marker_jaccard.mean(),
        "median_marker_jaccard": pairs.marker_jaccard.median(),
        "mean_shared_markers": pairs.shared_markers.mean(),
        "mean_directional_recovery": pairs.mean_directional_recovery.mean(),
    }


def stable_identifier_alias_summary(
    ontology_pairs: pd.DataFrame,
    *,
    bootstrap_replicates: int = 5000,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    """Summarize pairs joined by one ontology ID despite different labels."""
    columns = [
        "metric",
        "estimate",
        "uncertainty_95_lower",
        "uncertainty_95_upper",
        "pairs",
        "ontology_terms",
    ]
    if ontology_pairs.empty:
        return pd.DataFrame(columns=columns)

    pairs = ontology_pairs.copy()
    pairs["normalized_label_a"] = pairs.target_label_a.map(normalize_label)
    pairs["normalized_label_b"] = pairs.target_label_b.map(normalize_label)
    pairs = pairs[pairs.normalized_label_a != pairs.normalized_label_b]
    if pairs.empty:
        return pd.DataFrame(columns=columns)

    metrics = ["any_shared_marker", "marker_jaccard"]
    by_term = pairs.groupby("target_key")[metrics].mean()
    rng = np.random.default_rng(seed)
    term_indices = rng.integers(
        0,
        len(by_term),
        size=(bootstrap_replicates, len(by_term)),
    )
    rows = []
    for metric in metrics:
        values = by_term[metric].to_numpy()
        bootstrap = values[term_indices].mean(axis=1)
        rows.append(
            {
                "metric": metric,
                "estimate": values.mean(),
                "uncertainty_95_lower": np.quantile(bootstrap, 0.025),
                "uncertainty_95_upper": np.quantile(bootstrap, 0.975),
                "pairs": len(pairs),
                "ontology_terms": len(by_term),
            }
        )
    return pd.DataFrame(rows, columns=columns)


def identifier_recovered_pairs(ontology_pairs: pd.DataFrame) -> pd.DataFrame:
    """Return cross-paper pairs joined by an ID but missed by exact label matching."""
    pairs = ontology_pairs.copy()
    pairs["normalized_label_a"] = pairs.target_label_a.map(normalize_label)
    pairs["normalized_label_b"] = pairs.target_label_b.map(normalize_label)
    return pairs[pairs.normalized_label_a != pairs.normalized_label_b].reset_index(
        drop=True
    )


def pair_stratum(
    collection_pair: str, markers_a: int, markers_b: int
) -> tuple[str, int, int]:
    bins = sorted((size_bin(markers_a), size_bin(markers_b)))
    return collection_pair, bins[0], bins[1]


def identifier_matched_analysis(
    ontology_pairs: pd.DataFrame,
    ontology_profiles: list[Profile],
    same_label_pairs: pd.DataFrame,
    accepted_label_identifiers: dict[str, str],
    *,
    bootstrap_replicates: int = 1000,
    seed: int = RANDOM_SEED,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Compare ID-recovered pairs with size- and collection-matched references."""
    recovered = identifier_recovered_pairs(ontology_pairs)
    columns = [
        "comparison",
        "metric",
        "pairs",
        "available_pairs",
        "ontology_terms",
        "estimate",
        "uncertainty_95_lower",
        "uncertainty_95_upper",
        "uncertainty_method",
    ]
    if recovered.empty:
        return recovered, pd.DataFrame(), pd.DataFrame(columns=columns)

    recovered["stratum"] = recovered.apply(
        lambda row: pair_stratum(row.collection_pair, row.markers_a, row.markers_b),
        axis=1,
    )
    source_strata = set(recovered.stratum)

    same_label = same_label_pairs.copy()
    same_label["identifier_a"] = same_label.target_label_a.map(
        accepted_label_identifiers
    )
    same_label["identifier_b"] = same_label.target_label_b.map(
        accepted_label_identifiers
    )
    same_label["accepted_identifier"] = (
        same_label.identifier_a.notna()
        & same_label.identifier_b.notna()
        & (same_label.identifier_a == same_label.identifier_b)
    )
    same_label["stratum"] = same_label.apply(
        lambda row: pair_stratum(row.collection_pair, row.markers_a, row.markers_b),
        axis=1,
    )
    same_label_frames = {
        "same_label_same_identifier": same_label[same_label.accepted_identifier],
        "same_label_no_accepted_identifier": same_label[
            ~same_label.accepted_identifier
        ],
    }
    same_label_pools = {
        comparison: {
            key: group[["any_shared_marker", "marker_jaccard"]].to_numpy()
            for key, group in frame.groupby("stratum")
            if key in source_strata
        }
        for comparison, frame in same_label_frames.items()
    }

    different_id_pools: dict[tuple[str, int, int], list[tuple[float, float]]] = (
        defaultdict(list)
    )
    for left, right in itertools.combinations(ontology_profiles, 2):
        if left.article_key == right.article_key or left.target_key == right.target_key:
            continue
        if normalize_label(left.target_label) == normalize_label(right.target_label):
            continue
        collection_pair = "-".join(sorted([left.collection, right.collection]))
        stratum = pair_stratum(collection_pair, len(left.genes), len(right.genes))
        if stratum not in source_strata:
            continue
        intersection = left.genes & right.genes
        union = left.genes | right.genes
        different_id_pools[stratum].append(
            (int(bool(intersection)), len(intersection) / len(union))
        )

    missing_same = {
        comparison: source_strata - set(pools)
        for comparison, pools in same_label_pools.items()
        if source_strata - set(pools)
    }
    missing_different = source_strata - set(different_id_pools)
    if missing_same or missing_different:
        raise ValueError(
            "identifier matching lacks candidates for strata: "
            f"same_label={missing_same}, different_id={sorted(missing_different)}"
        )

    different_id_arrays = {
        key: np.asarray(values, dtype=float)
        for key, values in different_id_pools.items()
    }
    metrics = ["any_shared_marker", "marker_jaccard"]
    rng = np.random.default_rng(seed)
    draw_rows: list[dict[str, object]] = []
    for replicate in range(bootstrap_replicates):
        sampled = recovered.iloc[rng.integers(0, len(recovered), size=len(recovered))]
        same_values: dict[str, list[np.ndarray]] = {
            comparison: [] for comparison in same_label_pools
        }
        different_values: list[np.ndarray] = []
        for row in sampled.itertuples(index=False):
            for comparison, pools in same_label_pools.items():
                same_pool = pools[row.stratum]
                same_values[comparison].append(
                    same_pool[rng.integers(0, len(same_pool))]
                )
            different_pool = different_id_arrays[row.stratum]
            different_values.append(
                different_pool[rng.integers(0, len(different_pool))]
            )
        same_arrays = {
            comparison: np.vstack(values) for comparison, values in same_values.items()
        }
        different_array = np.vstack(different_values)
        for metric_index, metric in enumerate(metrics):
            for comparison, values in same_arrays.items():
                draw_rows.append(
                    {
                        "replicate": replicate,
                        "comparison": comparison,
                        "metric": metric,
                        "estimate": float(values[:, metric_index].mean()),
                    }
                )
            draw_rows.extend(
                [
                    {
                        "replicate": replicate,
                        "comparison": "same_identifier_different_label",
                        "metric": metric,
                        "estimate": float(sampled[metric].mean()),
                    },
                    {
                        "replicate": replicate,
                        "comparison": "different_identifier_matched_control",
                        "metric": metric,
                        "estimate": float(different_array[:, metric_index].mean()),
                    },
                ]
            )
    draws = pd.DataFrame(draw_rows)

    estimates = {
        ("same_identifier_different_label", metric): float(recovered[metric].mean())
        for metric in metrics
    }
    for comparison in (
        "same_label_same_identifier",
        "same_label_no_accepted_identifier",
        "different_identifier_matched_control",
    ):
        for metric in metrics:
            estimates[(comparison, metric)] = float(
                draws[
                    (draws.comparison == comparison) & (draws.metric == metric)
                ].estimate.mean()
            )

    rows = []
    for comparison in (
        "same_label_same_identifier",
        "same_label_no_accepted_identifier",
        "same_identifier_different_label",
        "different_identifier_matched_control",
    ):
        for metric in metrics:
            values = draws[
                (draws.comparison == comparison) & (draws.metric == metric)
            ].estimate
            lower, upper = values.quantile([0.025, 0.975])
            rows.append(
                {
                    "comparison": comparison,
                    "metric": metric,
                    "pairs": len(recovered),
                    "available_pairs": len(same_label_frames.get(comparison, recovered))
                    if comparison != "different_identifier_matched_control"
                    else len(recovered),
                    "ontology_terms": recovered.target_key.nunique(),
                    "estimate": estimates[(comparison, metric)],
                    "uncertainty_95_lower": lower,
                    "uncertainty_95_upper": upper,
                    "uncertainty_method": "pair bootstrap with matched sampling",
                }
            )
    recovered = recovered.drop(columns="stratum")
    return recovered, draws, pd.DataFrame(rows, columns=columns)


def label_balanced_summary(
    same_pairs: pd.DataFrame,
    controls: pd.DataFrame,
    *,
    bootstrap_replicates: int = 5000,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    metrics = [
        "any_shared_marker",
        "marker_jaccard",
        "mean_directional_recovery",
    ]
    inputs = [
        ("same_label", same_pairs, "target_key"),
        ("matched_different_label", controls, "source_target_key"),
    ]
    rng = np.random.default_rng(seed)
    rows = []
    for comparison, frame, group_column in inputs:
        grouped = frame.groupby(group_column)[metrics].mean()
        for metric in metrics:
            values = grouped[metric].dropna().to_numpy()
            if not len(values):
                estimate = lower = upper = math.nan
            else:
                estimate = float(values.mean())
                samples = rng.choice(
                    values,
                    size=(bootstrap_replicates, len(values)),
                    replace=True,
                ).mean(axis=1)
                lower, upper = np.quantile(samples, [0.025, 0.975])
            rows.append(
                {
                    "comparison": comparison,
                    "metric": metric,
                    "labels": len(values),
                    "estimate": estimate,
                    "uncertainty_95_lower": lower,
                    "uncertainty_95_upper": upper,
                    "uncertainty_method": "label bootstrap",
                }
            )
    return pd.DataFrame(rows)


def background_seed_sensitivity(
    same_pairs: pd.DataFrame,
    profiles: list[Profile],
    *,
    replicates: int = 25,
) -> pd.DataFrame:
    rows = []
    for offset in range(replicates):
        seed = RANDOM_SEED + offset
        controls = sample_matched_controls(same_pairs, profiles, seed=seed)
        grouped = controls.groupby("source_target_key")[
            ["any_shared_marker", "marker_jaccard", "mean_directional_recovery"]
        ].mean()
        rows.append(
            {
                "seed": seed,
                "pairs": len(controls),
                "any_shared_marker_fraction": controls.any_shared_marker.mean(),
                "mean_marker_jaccard": controls.marker_jaccard.mean(),
                "mean_directional_recovery": controls.mean_directional_recovery.mean(),
                "mean_shared_markers": controls.shared_markers.mean(),
                "label_balanced_any_shared_marker_fraction": grouped.any_shared_marker.mean(),
                "label_balanced_mean_marker_jaccard": grouped.marker_jaccard.mean(),
                "label_balanced_mean_directional_recovery": grouped.mean_directional_recovery.mean(),
            }
        )
    return pd.DataFrame(rows)


def ensemble_control_summary(
    sensitivity: pd.DataFrame, pairs: int
) -> dict[str, object]:
    return {
        "comparison": "matched_different_label",
        "pairs": pairs,
        "any_shared_marker_fraction": sensitivity.any_shared_marker_fraction.mean(),
        "mean_marker_jaccard": sensitivity.mean_marker_jaccard.mean(),
        "median_marker_jaccard": 0.0,
        "mean_shared_markers": sensitivity.mean_shared_markers.mean(),
        "mean_directional_recovery": sensitivity.mean_directional_recovery.mean(),
    }


def ensemble_collection_controls(
    same_pairs: pd.DataFrame,
    profiles: list[Profile],
    *,
    replicates: int = 25,
) -> pd.DataFrame:
    rows = []
    for offset in range(replicates):
        controls = sample_matched_controls(
            same_pairs, profiles, seed=RANDOM_SEED + offset
        )
        for collection_pair, group in controls.groupby("collection_pair"):
            row = summarize_pairs(group, "matched_different_label")
            row["collection_pair"] = collection_pair
            rows.append(row)
    frame = pd.DataFrame(rows)
    metrics = [
        "pairs",
        "any_shared_marker_fraction",
        "mean_marker_jaccard",
        "median_marker_jaccard",
        "mean_shared_markers",
        "mean_directional_recovery",
    ]
    result = frame.groupby("collection_pair", as_index=False)[metrics].mean()
    result.insert(0, "comparison", "matched_different_label")
    return result


def replace_balanced_control(
    balanced: pd.DataFrame,
    sensitivity: pd.DataFrame,
) -> pd.DataFrame:
    columns = {
        "any_shared_marker": "label_balanced_any_shared_marker_fraction",
        "marker_jaccard": "label_balanced_mean_marker_jaccard",
        "mean_directional_recovery": "label_balanced_mean_directional_recovery",
    }
    result = balanced.copy()
    for metric, source_column in columns.items():
        values = sensitivity[source_column]
        mask = (result.comparison == "matched_different_label") & (
            result.metric == metric
        )
        result.loc[mask, "estimate"] = values.mean()
        result.loc[mask, "uncertainty_95_lower"] = values.quantile(0.025)
        result.loc[mask, "uncertainty_95_upper"] = values.quantile(0.975)
        result.loc[mask, "uncertainty_method"] = "matched-draw quantiles"
    return result


def target_summary(
    profiles: list[Profile],
    pairs: pd.DataFrame,
    symbols: dict[str, str],
) -> pd.DataFrame:
    pair_groups = (
        {key: group for key, group in pairs.groupby("target_key", sort=False)}
        if not pairs.empty
        else {}
    )
    grouped: dict[str, list[Profile]] = defaultdict(list)
    for profile in profiles:
        grouped[profile.target_key].append(profile)
    rows = []
    for target_key, group in sorted(grouped.items()):
        article_genes: dict[str, set[str]] = defaultdict(set)
        for profile in group:
            article_genes[profile.article_key].update(profile.genes)
        if len(article_genes) < 2:
            continue
        gene_counts: Counter[str] = Counter()
        for genes in article_genes.values():
            gene_counts.update(genes)
        union = set(gene_counts)
        intersection = set.intersection(*article_genes.values())
        recurring = {gene for gene, count in gene_counts.items() if count >= 2}
        pair_group = pair_groups.get(target_key)
        top = sorted(
            gene_counts, key=lambda gene: (-gene_counts[gene], symbols.get(gene, gene))
        )
        most_recurrent_gene = top[0]
        article_count = len(article_genes)
        rows.append(
            {
                "target_key": target_key,
                "target_label": Counter(
                    profile.target_label for profile in group
                ).most_common(1)[0][0],
                "profiles": len(group),
                "articles": article_count,
                "collections": " | ".join(
                    sorted({profile.collection for profile in group})
                ),
                "union_markers": len(union),
                "recurring_markers": len(recurring),
                "recurring_fraction": len(recurring) / len(union)
                if union
                else math.nan,
                "strict_intersection_markers": len(intersection),
                "strict_intersection_fraction": len(intersection) / len(union)
                if union
                else math.nan,
                "mean_marker_prevalence": stable_mean(
                    [gene_counts[gene] / article_count for gene in sorted(gene_counts)]
                ),
                "most_recurrent_marker": symbols.get(
                    most_recurrent_gene, most_recurrent_gene
                ),
                "most_recurrent_marker_articles": gene_counts[most_recurrent_gene],
                "maximum_marker_recurrence": gene_counts[most_recurrent_gene]
                / article_count,
                "pairwise_mean_jaccard": pair_group.marker_jaccard.mean()
                if pair_group is not None
                else math.nan,
                "pairwise_any_overlap": pair_group.any_shared_marker.mean()
                if pair_group is not None
                else math.nan,
                "intersection_genes": " | ".join(
                    symbols.get(gene, gene) for gene in sorted(intersection)
                ),
                "top_recurrent_genes": " | ".join(
                    f"{symbols.get(gene, gene)} ({gene_counts[gene]}/{article_count})"
                    for gene in top[:10]
                ),
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["articles", "pairwise_mean_jaccard", "target_key"],
        ascending=[False, False, True],
    )


def intersection_survival(targets: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for minimum_articles in range(2, 11):
        eligible = targets[targets.articles >= minimum_articles]
        nonempty = int((eligible.strict_intersection_markers > 0).sum())
        rows.append(
            {
                "minimum_articles": minimum_articles,
                "labels": len(eligible),
                "labels_with_nonempty_intersection": nonempty,
                "fraction_with_nonempty_intersection": nonempty / len(eligible)
                if len(eligible)
                else math.nan,
                "median_recurring_marker_fraction": eligible.recurring_fraction.median(),
                "median_pairwise_jaccard": eligible.pairwise_mean_jaccard.median(),
            }
        )
    return pd.DataFrame(rows)


def intersection_accumulation(
    profiles: list[Profile],
    *,
    minimum_articles: int = 10,
    maximum_articles: int = 10,
    bootstrap_replicates: int = 1_000,
    seed: int = RANDOM_SEED,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    grouped: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for profile in profiles:
        grouped[profile.target_key][profile.article_key].update(profile.genes)
    eligible = {
        target: list(article_genes.values())
        for target, article_genes in grouped.items()
        if len(article_genes) >= minimum_articles
    }
    if not eligible:
        return pd.DataFrame(), pd.DataFrame()

    targets = np.asarray(sorted(eligible), dtype=object)
    rng = np.random.default_rng(seed)
    draw_rows = []
    for replicate in range(bootstrap_replicates):
        retained = np.zeros(maximum_articles, dtype=float)
        intersection_sizes = np.zeros(maximum_articles, dtype=float)
        for target in rng.choice(targets, size=len(targets), replace=True):
            panels = eligible[target]
            order = rng.permutation(len(panels))
            intersection = set(panels[order[0]])
            retained[0] += bool(intersection)
            intersection_sizes[0] += len(intersection)
            for index in range(1, maximum_articles):
                intersection &= panels[order[index]]
                retained[index] += bool(intersection)
                intersection_sizes[index] += len(intersection)
        for index in range(maximum_articles):
            draw_rows.append(
                {
                    "replicate": replicate,
                    "papers_combined": index + 1,
                    "fraction_labels_with_shared_marker": retained[index]
                    / len(targets),
                    "mean_shared_markers": intersection_sizes[index] / len(targets),
                }
            )

    draws = pd.DataFrame(draw_rows)
    summary_rows = []
    for papers_combined, group in draws.groupby("papers_combined", sort=True):
        values = group.fraction_labels_with_shared_marker
        marker_counts = group.mean_shared_markers
        summary_rows.append(
            {
                "papers_combined": papers_combined,
                "labels": len(targets),
                "estimate": values.mean(),
                "uncertainty_95_lower": values.quantile(0.025),
                "uncertainty_95_upper": values.quantile(0.975),
                "mean_shared_markers": marker_counts.mean(),
                "mean_shared_markers_95_lower": marker_counts.quantile(0.025),
                "mean_shared_markers_95_upper": marker_counts.quantile(0.975),
                "bootstrap_replicates": bootstrap_replicates,
            }
        )
    return pd.DataFrame(summary_rows), draws


def profile_reuse_metrics(
    analysis_profiles: list[Profile],
    all_profiles: list[Profile],
) -> pd.DataFrame:
    by_paper: dict[str, list[Profile]] = defaultdict(list)
    by_target: dict[str, list[Profile]] = defaultdict(list)
    for profile in all_profiles:
        by_paper[profile.paper_key].append(profile)
    for profile in analysis_profiles:
        by_target[profile.target_key].append(profile)

    rows = []
    for profile in analysis_profiles:
        local_others = [
            other
            for other in by_paper[profile.paper_key]
            if other.target_key != profile.target_key
        ]
        local_background = (
            set().union(*(other.genes for other in local_others))
            if local_others
            else set()
        )
        local_specificity = (
            len(profile.genes - local_background) / len(profile.genes)
            if local_others
            else math.nan
        )
        global_others = [
            other
            for other in by_target[profile.target_key]
            if other.article_key != profile.article_key
        ]
        global_recovery = (
            stable_mean(
                [
                    sum(gene in other.genes for other in global_others)
                    / len(global_others)
                    for gene in sorted(profile.genes)
                ]
            )
            if global_others
            else math.nan
        )
        rows.append(
            {
                "profile_id": profile.profile_id,
                "paper_key": profile.paper_key,
                "target_key": profile.target_key,
                "target_label": profile.target_label,
                "marker_count": len(profile.genes),
                "local_comparison_profiles": len(local_others),
                "reported_panel_exclusivity": local_specificity,
                "global_same_label_profiles": len(global_others),
                "global_marker_recovery": global_recovery,
            }
        )
    return pd.DataFrame(rows)


def pair_sensitivity(
    profiles: list[Profile],
    paper_targets: dict[str, set[str]],
) -> pd.DataFrame:
    rows = []
    for threshold in (1, 3, 5, 10):
        selected = [profile for profile in profiles if len(profile.genes) >= threshold]
        pairs = build_same_target_pairs(selected, paper_targets)
        summary = summarize_pairs(pairs, "same_label")
        summary["minimum_markers"] = threshold
        summary["profiles"] = len(selected)
        summary["recurring_targets"] = (
            pairs.target_key.nunique() if not pairs.empty else 0
        )
        rows.append(summary)
    return pd.DataFrame(rows)


def intersection_threshold_sensitivity(
    profiles: list[Profile],
    paper_targets: dict[str, set[str]],
    symbols: dict[str, str],
) -> pd.DataFrame:
    rows = []
    for marker_threshold in (1, 3, 5, 10):
        selected = [
            profile for profile in profiles if len(profile.genes) >= marker_threshold
        ]
        pairs = build_same_target_pairs(selected, paper_targets)
        targets = target_summary(selected, pairs, symbols)
        for article_threshold in (2, 5, 10):
            eligible = targets[targets.articles >= article_threshold]
            rows.append(
                {
                    "minimum_markers": marker_threshold,
                    "minimum_articles": article_threshold,
                    "labels": len(eligible),
                    "labels_with_nonempty_intersection": int(
                        (eligible.strict_intersection_markers > 0).sum()
                    ),
                    "fraction_with_nonempty_intersection": (
                        (eligible.strict_intersection_markers > 0).mean()
                        if len(eligible)
                        else math.nan
                    ),
                }
            )
    return pd.DataFrame(rows)


def context_summary(pairs: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    eligible = pairs[pairs.context_jaccard.notna()].copy()
    if eligible.empty:
        return pd.DataFrame(), {}
    eligible["context_bin"] = pd.cut(
        eligible.context_jaccard,
        bins=[-1e-12, 0, 0.25, 0.5, 0.75, 1.0],
        labels=["none", "(0, 0.25]", "(0.25, 0.5]", "(0.5, 0.75]", "(0.75, 1]"],
        include_lowest=True,
    )
    summary = (
        eligible.groupby("context_bin", observed=False)
        .agg(
            pairs=("pair_id", "size"),
            mean_marker_jaccard=("marker_jaccard", "mean"),
            any_shared_marker_fraction=("any_shared_marker", "mean"),
            mean_context_jaccard=("context_jaccard", "mean"),
        )
        .reset_index()
    )
    pearson = stats.pearsonr(eligible.context_jaccard, eligible.marker_jaccard)
    spearman = stats.spearmanr(eligible.context_jaccard, eligible.marker_jaccard)
    slope, intercept = np.polyfit(eligible.context_jaccard, eligible.marker_jaccard, 1)
    context_residual = eligible.context_jaccard - eligible.groupby(
        "target_key"
    ).context_jaccard.transform("mean")
    marker_residual = eligible.marker_jaccard - eligible.groupby(
        "target_key"
    ).marker_jaccard.transform("mean")
    within_label = stats.pearsonr(context_residual, marker_residual)
    label_correlations = []
    for _, group in eligible.groupby("target_key"):
        if (
            len(group) >= 3
            and group.context_jaccard.nunique() > 1
            and group.marker_jaccard.nunique() > 1
        ):
            label_correlations.append(
                float(
                    stats.spearmanr(
                        group.context_jaccard, group.marker_jaccard
                    ).statistic
                )
            )
    metrics = {
        "pairs": float(len(eligible)),
        "pearson_r": float(pearson.statistic),
        "pearson_p": float(pearson.pvalue),
        "spearman_rho": float(spearman.statistic),
        "spearman_p": float(spearman.pvalue),
        "linear_slope": float(slope),
        "linear_intercept": float(intercept),
        "within_label_pearson_r": float(within_label.statistic),
        "within_label_pearson_p": float(within_label.pvalue),
        "labels_with_correlation": float(len(label_correlations)),
        "median_within_label_spearman": float(np.median(label_correlations)),
        "fraction_positive_within_label_spearman": float(
            np.mean(np.asarray(label_correlations) > 0)
        ),
    }
    return summary, metrics


def context_fit_band(pairs: pd.DataFrame, draws: int = 1_000) -> pd.DataFrame:
    eligible = pairs.dropna(subset=["context_jaccard", "marker_jaccard"])
    grouped = (
        eligible.assign(
            x_squared=eligible.context_jaccard**2,
            xy=eligible.context_jaccard * eligible.marker_jaccard,
        )
        .groupby("target_key")
        .agg(
            pairs=("pair_id", "size"),
            sum_x=("context_jaccard", "sum"),
            sum_y=("marker_jaccard", "sum"),
            sum_x_squared=("x_squared", "sum"),
            sum_xy=("xy", "sum"),
        )
        .reset_index(drop=True)
    )
    fit_x = np.linspace(
        eligible.context_jaccard.min(),
        eligible.context_jaccard.max(),
        100,
    )
    slope, intercept = np.polyfit(
        eligible.context_jaccard,
        eligible.marker_jaccard,
        1,
    )
    rng = np.random.default_rng(RANDOM_SEED + 23)
    bootstrap_fits = np.empty((draws, len(fit_x)), dtype=float)
    for draw in range(draws):
        sampled = grouped.iloc[rng.integers(0, len(grouped), size=len(grouped))]
        pair_count = sampled.pairs.sum()
        sum_x = sampled.sum_x.sum()
        sum_y = sampled.sum_y.sum()
        centered_x_squared = sampled.sum_x_squared.sum() - sum_x**2 / pair_count
        centered_xy = sampled.sum_xy.sum() - sum_x * sum_y / pair_count
        sampled_slope = centered_xy / centered_x_squared
        sampled_intercept = (sum_y - sampled_slope * sum_x) / pair_count
        bootstrap_fits[draw] = sampled_intercept + sampled_slope * fit_x

    lower, upper = np.quantile(bootstrap_fits, [0.025, 0.975], axis=0)
    return pd.DataFrame(
        {
            "context_jaccard": fit_x,
            "fitted_marker_jaccard": intercept + slope * fit_x,
            "label_cluster_bootstrap_95_lower": lower,
            "label_cluster_bootstrap_95_upper": upper,
            "bootstrap_draws": draws,
        }
    )


def database_summary(connection: sqlite3.Connection) -> pd.DataFrame:
    queries = {
        "papers": "SELECT COUNT(*) FROM papers",
        "papers_with_claims": "SELECT COUNT(DISTINCT paper_key) FROM claims",
        "claims": "SELECT COUNT(*) FROM claims",
        "marker_evidence_rows": "SELECT COUNT(*) FROM marker_evidence",
        "mapped_marker_evidence_rows": "SELECT COUNT(*) FROM marker_evidence WHERE gene_curie IS NOT NULL",
        "positive_marker_evidence_rows": "SELECT COUNT(*) FROM marker_evidence WHERE gene_curie IS NOT NULL AND direction='positive'",
        "negative_marker_evidence_rows": "SELECT COUNT(*) FROM marker_evidence WHERE gene_curie IS NOT NULL AND direction='negative'",
        "claims_with_comparison": "SELECT COUNT(DISTINCT claim_key) FROM terms WHERE term_type='comparison'",
        "papers_with_comparison": "SELECT COUNT(DISTINCT c.paper_key) FROM claims c JOIN terms t ON t.claim_key=c.claim_key WHERE t.term_type='comparison'",
    }
    rows = [
        {
            "scope": "all",
            "metric": metric,
            "value": connection.execute(query).fetchone()[0],
        }
        for metric, query in queries.items()
    ]
    for collection in ("biorxiv", "hca"):
        rows.extend(
            [
                {
                    "scope": collection,
                    "metric": "papers",
                    "value": connection.execute(
                        "SELECT COUNT(*) FROM papers WHERE collection=?", (collection,)
                    ).fetchone()[0],
                },
                {
                    "scope": collection,
                    "metric": "papers_with_claims",
                    "value": connection.execute(
                        "SELECT COUNT(DISTINCT c.paper_key) FROM claims c JOIN papers p ON p.paper_key=c.paper_key WHERE p.collection=?",
                        (collection,),
                    ).fetchone()[0],
                },
                {
                    "scope": collection,
                    "metric": "claims",
                    "value": connection.execute(
                        "SELECT COUNT(*) FROM claims c JOIN papers p ON p.paper_key=c.paper_key WHERE p.collection=?",
                        (collection,),
                    ).fetchone()[0],
                },
            ]
        )
    return pd.DataFrame(rows)


def term_coverage(connection: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query(
        """
        SELECT term_type,
               COUNT(*) AS terms,
               SUM(ontology_term IS NOT NULL) AS grounded,
               SUM(exact=1) AS current_exact,
               SUM(provenance='explicit') AS explicit
        FROM terms
        GROUP BY term_type
        ORDER BY term_type
        """,
        connection,
    )


def reported_targets(connection: sqlite3.Connection) -> pd.DataFrame:
    frame = pd.read_sql_query(
        """
        SELECT DISTINCT c.paper_key, target.normalized_label AS target_label
        FROM claims c
        JOIN terms target
          ON target.claim_key=c.claim_key AND target.term_type='celltype'
        ORDER BY c.paper_key, target.normalized_label
        """,
        connection,
    )
    frame["target_key"] = frame.target_label.map(normalize_label)
    return frame


def comparison_evidence(connection: sqlite3.Connection) -> pd.DataFrame:
    frame = pd.read_sql_query(
        """
        SELECT c.paper_key, c.claim_key, target.normalized_label AS target_label,
               comparison.normalized_label AS comparison_label,
               comparison.ontology_term AS comparison_curie,
               comparison.provenance, comparison.exact
        FROM claims c
        JOIN terms target
          ON target.claim_key=c.claim_key AND target.term_type='celltype'
        JOIN terms comparison
          ON comparison.claim_key=c.claim_key AND comparison.term_type='comparison'
        ORDER BY c.paper_key, c.claim_key, comparison.ordinal
        """,
        connection,
    )
    if not frame.empty:
        frame["target_key"] = frame.target_label.map(normalize_label)
    return frame


def coreported_label_pairs(paper_targets: dict[str, set[str]]) -> pd.DataFrame:
    counts: Counter[tuple[str, str]] = Counter()
    for targets in paper_targets.values():
        counts.update(itertools.combinations(sorted(targets), 2))
    rows = [
        {"label_a": left, "label_b": right, "papers": count}
        for (left, right), count in counts.items()
    ]
    if not rows:
        return pd.DataFrame(columns=["label_a", "label_b", "papers"])
    return pd.DataFrame(rows).sort_values(
        ["papers", "label_a", "label_b"], ascending=[False, True, True]
    )


def duplicate_articles(papers: pd.DataFrame) -> pd.DataFrame:
    duplicated = papers[papers.duplicated("article_key", keep=False)].copy()
    return duplicated.sort_values(["article_key", "paper_key"])[
        ["article_key", "paper_key", "collection", "title", "source_sha256"]
    ]


def write_frame(frame: pd.DataFrame, path: Path) -> None:
    frame.to_csv(path, sep="\t", index=False, na_rep="")


def make_figure(
    identifier_matched_summary: pd.DataFrame,
    identifier_pairs: pd.DataFrame,
    same_pairs: pd.DataFrame,
    context_metrics: dict[str, float],
    context_fit: pd.DataFrame,
    accumulation: pd.DataFrame,
    output_dir: Path,
) -> None:
    fig, axes = plt.subplots(
        1,
        3,
        figsize=(12.2, 3.5),
        gridspec_kw={"width_ratios": [1.35, 1, 1]},
    )

    order = [
        "same_label_same_identifier",
        "same_label_no_accepted_identifier",
        "same_identifier_different_label",
        "different_identifier_matched_control",
    ]
    panel_a = (
        identifier_matched_summary[
            identifier_matched_summary.metric == "any_shared_marker"
        ]
        .set_index("comparison")
        .loc[order]
    )
    estimates = panel_a.estimate.to_numpy()
    lowers = panel_a.uncertainty_95_lower.to_numpy()
    uppers = panel_a.uncertainty_95_upper.to_numpy()
    errors = np.vstack(
        [
            estimates - lowers,
            uppers - estimates,
        ]
    )
    axes[0].bar(
        range(4),
        estimates,
        yerr=errors,
        facecolor="white",
        edgecolor="black",
        linewidth=1.1,
        width=0.68,
        capsize=3,
        error_kw={"ecolor": "black", "elinewidth": 1.1},
    )
    axes[0].set_xticks(
        range(4),
        [
            f"Same label,\nsame ID\n(n={int(panel_a.iloc[0].available_pairs):,})",
            f"Same label,\nno accepted ID\n(n={int(panel_a.iloc[1].available_pairs):,})",
            f"Different labels,\nsame ID\n(n={len(identifier_pairs):,})",
            "Different IDs,\nmatched control",
        ],
    )
    axes[0].tick_params(axis="x", labelsize=7)
    axes[0].set_ylim(0, 1)
    axes[0].set_ylabel("Pairs sharing at least one marker")
    axes[0].set_title("A", loc="left", fontweight="bold")

    context_plot = same_pairs.dropna(subset=["context_jaccard", "marker_jaccard"])
    axes[1].scatter(
        context_plot.context_jaccard,
        context_plot.marker_jaccard,
        s=9,
        facecolors="white",
        edgecolors="black",
        alpha=0.15,
        linewidths=0.35,
        rasterized=True,
    )
    axes[1].fill_between(
        context_fit.context_jaccard,
        context_fit.label_cluster_bootstrap_95_lower,
        context_fit.label_cluster_bootstrap_95_upper,
        color="#C62828",
        alpha=0.16,
        linewidth=0,
    )
    axes[1].plot(
        context_fit.context_jaccard,
        context_fit.fitted_marker_jaccard,
        color="#C62828",
        linewidth=2,
    )
    axes[1].text(
        0.96,
        0.94,
        f"Pearson r = {context_metrics['pearson_r']:.3f}",
        transform=axes[1].transAxes,
        ha="right",
        va="top",
        fontsize=8,
    )
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].set_ylabel("Marker-panel Jaccard")
    axes[1].set_xlabel("Co-reported-label Jaccard")
    axes[1].set_title("B", loc="left", fontweight="bold")

    axes[2].fill_between(
        accumulation.papers_combined,
        accumulation.uncertainty_95_lower,
        accumulation.uncertainty_95_upper,
        color="#00A598",
        alpha=0.16,
        linewidth=0,
    )
    axes[2].plot(
        accumulation.papers_combined,
        accumulation.estimate,
        color="#00A598",
        linewidth=2,
    )
    axes[2].scatter(
        accumulation.papers_combined,
        accumulation.estimate,
        s=22,
        facecolors="white",
        edgecolors="black",
        linewidths=0.7,
        zorder=3,
    )
    axes[2].set_xlim(1, 10)
    axes[2].set_ylim(0, 1)
    axes[2].set_xticks(range(1, 11))
    axes[2].set_xlabel("Papers combined per label")
    axes[2].set_ylabel("Fraction of labels retaining a shared marker")
    axes[2].set_title("C", loc="left", fontweight="bold")

    for axis in axes:
        axis.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_dir / "fig_mrkr_corpus_reuse_v1.pdf", bbox_inches="tight")
    fig.savefig(
        output_dir / "fig_mrkr_corpus_reuse_v1.png", dpi=220, bbox_inches="tight"
    )
    plt.close(fig)


def write_report(
    output_dir: Path,
    summary: pd.DataFrame,
    pair_summary: pd.DataFrame,
    balanced_summary: pd.DataFrame,
    ontology_pair_summary: pd.DataFrame,
    identifier_summary: pd.DataFrame,
    identifier_pairs: pd.DataFrame,
    identifier_matched_summary: pd.DataFrame,
    targets: pd.DataFrame,
    label_accumulation: pd.DataFrame,
    ontology_accumulation: pd.DataFrame,
    reuse: pd.DataFrame,
    context_metrics: dict[str, float],
    duplicate_count: int,
    negative_profile_count: int,
    ontology_audit_metrics: dict[str, int],
) -> None:
    values = {(row.scope, row.metric): row.value for row in summary.itertuples()}
    same = pair_summary[pair_summary.comparison == "same_label"].iloc[0]
    control = pair_summary[pair_summary.comparison == "matched_different_label"].iloc[0]
    balanced = balanced_summary.pivot(
        index="metric", columns="comparison", values="estimate"
    )
    ontology = (
        ontology_pair_summary.iloc[0] if not ontology_pair_summary.empty else None
    )
    identifier = (
        identifier_summary.set_index("metric").loc["any_shared_marker"]
        if not identifier_summary.empty
        else None
    )
    identifier_matched = identifier_matched_summary.pivot(
        index="metric", columns="comparison", values="estimate"
    )
    strict = int((targets.strict_intersection_markers > 0).sum())
    label_accumulation_lookup = label_accumulation.set_index("papers_combined")
    ontology_accumulation_lookup = ontology_accumulation.set_index("papers_combined")
    reuse_evaluable = reuse.dropna(
        subset=["reported_panel_exclusivity", "global_marker_recovery"]
    )
    reuse_correlation = stats.spearmanr(
        reuse_evaluable.reported_panel_exclusivity,
        reuse_evaluable.global_marker_recovery,
    )
    text = f"""# mrkr corpus analysis v1

## Corpus

- {int(values[("all", "papers")]):,} validated papers ({int(values[("biorxiv", "papers")]):,} bioRxiv; {int(values[("hca", "papers")]):,} HCA).
- {int(values[("all", "papers_with_claims")]):,} papers contain at least one extracted marker statement.
- {int(values[("all", "claims")]):,} source-grounded marker statements and {int(values[("all", "positive_marker_evidence_rows")]):,} mapped positive marker-gene evidence rows.
- {int(values[("all", "claims_with_comparison")]):,} statements ({values[("all", "claims_with_comparison")] / values[("all", "claims")]:.1%}) explicitly record a comparison term.
- {negative_profile_count:,} paper--cell type combinations contain mapped negative-marker evidence; these are excluded from positive-panel reuse analyses.
- {duplicate_count:,} source records share a normalized article title with another record; cross-paper analyses exclude pairs from the same article key.

## Reuse by reported label

Each reported marker gene panel combines mapped positive markers for one normalized cell type label in one paper. The primary analysis requires at least {DEFAULT_MIN_MARKERS} markers per panel.

- {int(same.pairs):,} pairs of papers use the same cell type label and report at least {DEFAULT_MIN_MARKERS} markers for it.
- {same.any_shared_marker_fraction:.1%} share at least one marker; mean marker Jaccard is {same.mean_marker_jaccard:.3f} (median {same.median_marker_jaccard:.3f}).
- In marker-count-bin- and collection-matched pairs with different labels, {control.any_shared_marker_fraction:.1%} share a marker and mean Jaccard is {control.mean_marker_jaccard:.3f}.
- When each recurring label receives equal weight, pairs of papers using the same label share any marker at {balanced.loc["any_shared_marker", "same_label"]:.1%} versus {balanced.loc["any_shared_marker", "matched_different_label"]:.1%} in matched controls; mean Jaccard is {balanced.loc["marker_jaccard", "same_label"]:.3f} versus {balanced.loc["marker_jaccard", "matched_different_label"]:.3f}.
- {strict:,} of {len(targets):,} recurring labels have a non-empty strict intersection across every retained marker gene panel.
- In the fixed cohort of {int(label_accumulation.labels.iloc[0]):,} labels reported in at least 10 papers, the estimated fraction retaining a shared marker is {label_accumulation_lookup.loc[2, "estimate"]:.1%} after combining two papers, {label_accumulation_lookup.loc[5, "estimate"]:.1%} after five, and {label_accumulation_lookup.loc[10, "estimate"]:.1%} after ten.
- The accepted-identifier sensitivity analysis uses {int(ontology_accumulation.labels.iloc[0]):,} Cell Ontology identifiers and gives {ontology_accumulation_lookup.loc[10, "estimate"]:.1%} after ten papers.

## Local reporting and global recovery

For {len(reuse_evaluable):,} reported marker gene panels evaluable both within and across papers, median reported-panel exclusivity within the source paper is {reuse_evaluable.reported_panel_exclusivity.median():.3f}, while median leave-one-paper-out marker recovery among panels with the same label is {reuse_evaluable.global_marker_recovery.median():.3f}. Their Spearman correlation is {reuse_correlation.statistic:.3f}. Reported-panel exclusivity measures whether a marker is absent from other extracted panels in the paper; it is not an expression-based specificity estimate.

## Ontology sensitivity analysis

Cell Ontology recurrence uses only target labels equal to a canonical label or an exact synonym in the pinned ontology release. Broad, narrow, related, and matches based only on full-text coverage are excluded.

- {ontology_audit_metrics["semantic_exact_target_mappings"]:,} of {ontology_audit_metrics["observed_target_mappings"]:,} distinct reported-label-to-Cell-Ontology mappings pass this semantic exactness test; {ontology_audit_metrics["full_span_only_target_mappings"]:,} mappings marked exact by full-text coverage do not.
"""
    if ontology is not None:
        text += (
            f"- {int(ontology.pairs):,} cross-article pairs share a conservatively accepted Cell Ontology term. "
            f"{ontology.any_shared_marker_fraction:.1%} share a marker; mean Jaccard is "
            f"{ontology.mean_marker_jaccard:.3f}.\n"
        )
    if identifier is not None:
        text += (
            f"- Stable Cell Ontology identifiers link {int(identifier.pairs):,} "
            "cross-article panel pairs that use different normalized labels across "
            f"{int(identifier.ontology_terms):,} ontology terms. After balancing ontology "
            f"terms, {identifier.estimate:.1%} of these pairs share a marker.\n"
        )
    if not identifier_pairs.empty:
        text += (
            f"- Exact labels miss all {len(identifier_pairs):,} of these different-label "
            "connections. In the pair-weighted matched analysis, "
            f"{identifier_matched.loc['any_shared_marker', 'same_identifier_different_label']:.1%} "
            "of the identifier-recovered pairs share a marker, compared with "
            f"{identifier_matched.loc['any_shared_marker', 'same_label_same_identifier']:.1%} "
            "for matched same-label pairs with an accepted identifier, "
            f"{identifier_matched.loc['any_shared_marker', 'same_label_no_accepted_identifier']:.1%} "
            "for matched same-label pairs without an accepted identifier, and "
            f"{identifier_matched.loc['any_shared_marker', 'different_identifier_matched_control']:.1%} "
            "for matched pairs with different identifiers.\n"
        )
    text += "\n## Co-reported label context\n"
    if context_metrics:
        text += (
            "\nAmong pairs of papers using the same cell type label, marker Jaccard has "
            f"Pearson r={context_metrics['pearson_r']:.3f} and Spearman rho="
            f"{context_metrics['spearman_rho']:.3f} with co-reported-label Jaccard; "
            f"the fitted slope is {context_metrics['linear_slope']:.3f}. After centering "
            f"within each label, Pearson r is {context_metrics['within_label_pearson_r']:.3f}. "
            "This is a "
            "descriptive context proxy, not a reconstructed experimental contrast.\n"
        )
    text += """

## Interpretation boundary

The analysis measures recurrence of reported, source-grounded marker panels. It does not establish that a recurrent marker is a formal marker under every relevant pairwise comparison. The extracted comparison term is sparse, and manuscript text cannot reconstruct unreported contrasts or sufficient statistics.
"""
    (output_dir / "report.md").write_text(text, encoding="utf-8")


def run_analysis(
    database: Path,
    source_manifest: Path,
    ontology_audit: Path,
    output_dir: Path,
    repo_root: Path,
    *,
    min_markers: int = DEFAULT_MIN_MARKERS,
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    semantic_exact = load_semantic_exact(ontology_audit)
    ontology_audit_metrics = ontology_audit_summary(ontology_audit)
    with sqlite3.connect(database) as connection:
        papers = load_papers(connection, source_manifest, repo_root)
        evidence = load_marker_evidence(connection)
        summary = database_summary(connection)
        coverage = term_coverage(connection)
        comparisons = comparison_evidence(connection)
        reported_target_frame = reported_targets(connection)

    symbols = representative_gene_symbols(evidence)
    all_label_profiles = build_profiles(
        evidence,
        papers,
        target_mode="label",
        semantic_exact=semantic_exact,
    )
    label_profiles = [
        profile for profile in all_label_profiles if len(profile.genes) >= min_markers
    ]
    paper_targets: dict[str, set[str]] = defaultdict(set)
    for row in reported_target_frame.itertuples(index=False):
        paper_targets[row.paper_key].add(row.target_key)

    same_pairs = build_same_target_pairs(label_profiles, paper_targets)
    controls = sample_matched_controls(same_pairs, label_profiles)
    background_sensitivity = background_seed_sensitivity(same_pairs, label_profiles)
    pair_summary = pd.DataFrame(
        [
            summarize_pairs(same_pairs, "same_label"),
            ensemble_control_summary(background_sensitivity, len(same_pairs)),
        ]
    )
    balanced_summary = replace_balanced_control(
        label_balanced_summary(same_pairs, controls),
        background_sensitivity,
    )
    by_collection = []
    for collection_pair, group in same_pairs.groupby("collection_pair"):
        row = summarize_pairs(group, "same_label")
        row["collection_pair"] = collection_pair
        by_collection.append(row)
    collection_summary = pd.concat(
        [
            pd.DataFrame(by_collection),
            ensemble_collection_controls(same_pairs, label_profiles),
        ],
        ignore_index=True,
    )

    targets = target_summary(label_profiles, same_pairs, symbols)
    survival = intersection_survival(targets)
    label_accumulation, label_accumulation_draws = intersection_accumulation(
        label_profiles
    )
    reuse = profile_reuse_metrics(label_profiles, all_label_profiles)
    sensitivity = pair_sensitivity(all_label_profiles, paper_targets)
    intersection_sensitivity = intersection_threshold_sensitivity(
        all_label_profiles, paper_targets, symbols
    )
    context_bins, context_metrics = context_summary(same_pairs)
    context_fit = context_fit_band(same_pairs)
    coreport_pairs = coreported_label_pairs(paper_targets)

    negative_profiles = build_profiles(
        evidence,
        papers,
        target_mode="label",
        semantic_exact=semantic_exact,
        direction="negative",
    )

    ontology_profiles_all = build_profiles(
        evidence,
        papers,
        target_mode="ontology",
        semantic_exact=semantic_exact,
    )
    ontology_profiles = [
        profile
        for profile in ontology_profiles_all
        if len(profile.genes) >= min_markers
    ]
    ontology_paper_targets: dict[str, set[str]] = defaultdict(set)
    for profile in ontology_profiles_all:
        ontology_paper_targets[profile.paper_key].add(profile.target_key)
    ontology_pairs = build_same_target_pairs(ontology_profiles, ontology_paper_targets)
    ontology_pair_summary = pd.DataFrame(
        [summarize_pairs(ontology_pairs, "same_ontology_term")]
    )
    identifier_summary = stable_identifier_alias_summary(ontology_pairs)
    accepted_label_identifiers = {
        label: identifier for identifier, label in semantic_exact
    }
    identifier_pairs, identifier_matched_draws, identifier_matched_summary = (
        identifier_matched_analysis(
            ontology_pairs,
            ontology_profiles,
            same_pairs,
            accepted_label_identifiers,
        )
    )
    ontology_targets = target_summary(ontology_profiles, ontology_pairs, symbols)
    ontology_accumulation, ontology_accumulation_draws = intersection_accumulation(
        ontology_profiles,
        seed=RANDOM_SEED + 1,
    )

    marker_rows = []
    marker_labels: dict[str, set[str]] = defaultdict(set)
    marker_papers: dict[str, set[str]] = defaultdict(set)
    for profile in all_label_profiles:
        for gene in profile.genes:
            marker_labels[gene].add(profile.target_key)
            marker_papers[gene].add(profile.article_key)
    for gene in sorted(marker_labels):
        marker_rows.append(
            {
                "gene_curie": gene,
                "gene_symbol": symbols.get(gene, gene),
                "labels": len(marker_labels[gene]),
                "articles": len(marker_papers[gene]),
            }
        )
    marker_summary = pd.DataFrame(marker_rows).sort_values(
        ["labels", "articles", "gene_symbol"], ascending=[False, False, True]
    )

    duplicate_frame = duplicate_articles(papers)
    write_frame(summary, output_dir / "corpus_summary.tsv")
    write_frame(coverage, output_dir / "term_coverage.tsv")
    write_frame(papers, output_dir / "papers.tsv")
    write_frame(duplicate_frame, output_dir / "duplicate_article_records.tsv")
    write_frame(
        profile_frame(all_label_profiles, symbols),
        output_dir / "label_profiles_all.tsv",
    )
    write_frame(
        profile_frame(label_profiles, symbols),
        output_dir / "label_profiles_analysis.tsv",
    )
    write_frame(same_pairs, output_dir / "same_label_pairs.tsv")
    write_frame(controls, output_dir / "matched_background_pairs.tsv")
    write_frame(pair_summary, output_dir / "pair_summary.tsv")
    write_frame(balanced_summary, output_dir / "label_balanced_pair_summary.tsv")
    write_frame(
        background_sensitivity,
        output_dir / "matched_background_seed_sensitivity.tsv",
    )
    write_frame(collection_summary, output_dir / "collection_pair_summary.tsv")
    write_frame(targets, output_dir / "label_recurrence_summary.tsv")
    write_frame(survival, output_dir / "intersection_survival.tsv")
    write_frame(
        label_accumulation,
        output_dir / "label_intersection_accumulation.tsv",
    )
    write_frame(
        label_accumulation_draws,
        output_dir / "label_intersection_accumulation_bootstrap.tsv",
    )
    write_frame(reuse, output_dir / "profile_reuse_metrics.tsv")
    write_frame(sensitivity, output_dir / "minimum_marker_sensitivity.tsv")
    write_frame(
        intersection_sensitivity,
        output_dir / "intersection_threshold_sensitivity.tsv",
    )
    write_frame(context_bins, output_dir / "coreported_context_bins.tsv")
    write_frame(
        pd.DataFrame([context_metrics]),
        output_dir / "coreported_context_metrics.tsv",
    )
    write_frame(context_fit, output_dir / "coreported_context_fit.tsv")
    write_frame(coreport_pairs, output_dir / "coreported_label_pairs.tsv")
    write_frame(comparisons, output_dir / "comparison_evidence.tsv")
    write_frame(
        profile_frame(negative_profiles, symbols),
        output_dir / "negative_label_profiles.tsv",
    )
    write_frame(marker_summary, output_dir / "marker_ambiguity_summary.tsv")
    write_frame(
        profile_frame(ontology_profiles, symbols),
        output_dir / "ontology_profiles_analysis.tsv",
    )
    write_frame(ontology_pairs, output_dir / "same_ontology_pairs.tsv")
    write_frame(ontology_pair_summary, output_dir / "ontology_pair_summary.tsv")
    write_frame(
        identifier_summary, output_dir / "stable_identifier_linkage_summary.tsv"
    )
    write_frame(identifier_pairs, output_dir / "identifier_recovered_pairs.tsv")
    write_frame(
        identifier_matched_draws,
        output_dir / "identifier_recovered_matched_bootstrap.tsv",
    )
    write_frame(
        identifier_matched_summary,
        output_dir / "identifier_recovered_matched_summary.tsv",
    )
    write_frame(ontology_targets, output_dir / "ontology_recurrence_summary.tsv")
    write_frame(
        ontology_accumulation,
        output_dir / "ontology_intersection_accumulation.tsv",
    )
    write_frame(
        ontology_accumulation_draws,
        output_dir / "ontology_intersection_accumulation_bootstrap.tsv",
    )
    make_figure(
        identifier_matched_summary,
        identifier_pairs,
        same_pairs,
        context_metrics,
        context_fit,
        label_accumulation,
        output_dir,
    )
    write_report(
        output_dir,
        summary,
        pair_summary,
        balanced_summary,
        ontology_pair_summary,
        identifier_summary,
        identifier_pairs,
        identifier_matched_summary,
        targets,
        label_accumulation,
        ontology_accumulation,
        reuse,
        context_metrics,
        len(duplicate_frame),
        len(negative_profiles),
        ontology_audit_metrics,
    )

    metadata = {
        "schema_version": SCHEMA_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "database": str(database),
        "database_sha256": sha256_file(database),
        "source_manifest": str(source_manifest),
        "source_manifest_sha256": sha256_file(source_manifest),
        "ontology_audit_path": str(ontology_audit),
        "ontology_audit_sha256": sha256_file(ontology_audit),
        "minimum_markers": min_markers,
        "random_seed": RANDOM_SEED,
        "label_profiles": len(label_profiles),
        "same_label_pairs": len(same_pairs),
        "ontology_profiles": len(ontology_profiles),
        "same_ontology_pairs": len(ontology_pairs),
        "stable_identifier_alias_pairs": int(identifier_summary.pairs.iloc[0])
        if not identifier_summary.empty
        else 0,
        "stable_identifier_alias_terms": int(identifier_pairs.target_key.nunique())
        if not identifier_pairs.empty
        else 0,
        "ontology_audit": ontology_audit_metrics,
        "context_metrics": context_metrics,
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--source-manifest", required=True, type=Path)
    parser.add_argument("--ontology-audit", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--min-markers", type=int, default=DEFAULT_MIN_MARKERS)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata = run_analysis(
        args.database,
        args.source_manifest,
        args.ontology_audit,
        args.out_dir,
        args.repo_root,
        min_markers=args.min_markers,
    )
    print(
        f"label_profiles={metadata['label_profiles']}, "
        f"same_label_pairs={metadata['same_label_pairs']}, "
        f"ontology_profiles={metadata['ontology_profiles']}, "
        f"same_ontology_pairs={metadata['same_ontology_pairs']}"
    )


if __name__ == "__main__":
    main()
