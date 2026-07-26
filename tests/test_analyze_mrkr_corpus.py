"""Tests for canonical corpus marker-panel analysis."""

import importlib.util
import sys
from pathlib import Path

import pandas as pd


SCRIPT = Path(__file__).parents[1] / "analysis" / "analyze_mrkr_corpus.py"
SPEC = importlib.util.spec_from_file_location("analyze_mrkr_corpus", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def profile(name, paper, article, target, genes, collection="hca", label=None):
    return MODULE.Profile(
        profile_id=name,
        paper_key=paper,
        article_key=article,
        collection=collection,
        target_key=target,
        target_label=label or target,
        genes=frozenset(genes),
    )


def test_same_target_pairs_exclude_duplicate_articles_and_measure_context():
    profiles = [
        profile("p1", "paper1", "article1", "t cell", {"A", "B", "C"}),
        profile("p2", "paper2", "article2", "t cell", {"B", "C", "D"}),
        profile("p3", "paper3", "article1", "t cell", {"A", "B", "C"}),
    ]
    contexts = {
        "paper1": {"t cell", "b cell"},
        "paper2": {"t cell", "b cell", "nk cell"},
        "paper3": {"t cell"},
    }

    pairs = MODULE.build_same_target_pairs(profiles, contexts)

    assert len(pairs) == 2
    row = pairs[(pairs.paper_a == "paper1") & (pairs.paper_b == "paper2")].iloc[0]
    assert row.shared_markers == 2
    assert row.marker_jaccard == 0.5
    assert row.context_jaccard == 0.5


def test_target_summary_reports_intersection_and_recurrence():
    profiles = [
        profile("p1", "paper1", "article1", "t cell", {"A", "B", "C"}),
        profile("p2", "paper2", "article2", "t cell", {"B", "C", "D"}),
        profile("p3", "paper3", "article3", "t cell", {"C", "D", "E"}),
    ]
    pairs = MODULE.build_same_target_pairs(
        profiles,
        {profile.paper_key: {"t cell"} for profile in profiles},
    )

    summary = MODULE.target_summary(profiles, pairs, {gene: gene for gene in "ABCDE"})

    assert len(summary) == 1
    row = summary.iloc[0]
    assert row.union_markers == 5
    assert row.recurring_markers == 3
    assert row.strict_intersection_markers == 1
    assert row.intersection_genes == "C"


def test_intersection_accumulation_is_monotone_within_each_draw():
    profiles = [
        profile("t1", "paper1", "article1", "t cell", {"A", "B", "C"}),
        profile("t2", "paper2", "article2", "t cell", {"A", "D", "E"}),
        profile("t3", "paper3", "article3", "t cell", {"A", "F", "G"}),
        profile("b1", "paper1", "article1", "b cell", {"H", "I", "J"}),
        profile("b2", "paper2", "article2", "b cell", {"H", "K", "L"}),
        profile("b3", "paper3", "article3", "b cell", {"M", "N", "O"}),
    ]

    summary, draws = MODULE.intersection_accumulation(
        profiles,
        minimum_articles=3,
        maximum_articles=3,
        bootstrap_replicates=20,
        seed=1,
    )

    assert summary.labels.unique().tolist() == [2]
    assert summary.iloc[0].estimate == 1
    for _, group in draws.groupby("replicate"):
        values = group.sort_values("papers_combined").fraction_labels_with_shared_marker
        assert values.is_monotonic_decreasing


def test_pair_summary_handles_an_empty_frame():
    result = MODULE.summarize_pairs(pd.DataFrame(), "same_label")
    assert result["pairs"] == 0


def test_stable_identifier_summary_links_different_labels():
    profiles = [
        profile("p1", "paper1", "article1", "CL:1", {"A", "B"}, label="T-cell"),
        profile("p2", "paper2", "article2", "CL:1", {"B", "C"}, label="T lymphocyte"),
        profile("p3", "paper3", "article3", "CL:1", {"A", "D"}, label="T-cell"),
    ]
    pairs = MODULE.build_same_target_pairs(
        profiles,
        {item.paper_key: {"CL:1"} for item in profiles},
    )

    summary = MODULE.stable_identifier_alias_summary(
        pairs,
        bootstrap_replicates=100,
        seed=1,
    ).set_index("metric")

    assert summary.loc["any_shared_marker", "pairs"] == 2
    assert summary.loc["any_shared_marker", "ontology_terms"] == 1
    assert summary.loc["any_shared_marker", "estimate"] == 0.5
    assert summary.loc["marker_jaccard", "estimate"] == 1 / 6
