"""Tests for the analysis-only DEG-source linkage experiment."""

import importlib.util
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[1] / "analysis" / "evaluate_mrkr_deg_linkage.py"
SPEC = importlib.util.spec_from_file_location("evaluate_mrkr_deg_linkage", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def target(label):
    return {
        "term_type": "celltype",
        "normalized_label": label,
        "legacy_normalized_label": label,
    }


def test_deg_catalog_keeps_source_specific_cell_type_sets():
    document = {
        "profiles": [
            {
                "profile_id": "p1",
                "evidence": {"data_id": "all markers"},
                "terms": [target("T CELL")],
            },
            {
                "profile_id": "p2",
                "evidence": {"data_id": "immune subtypes"},
                "terms": [target("CD8 T CELL")],
            },
            {
                "profile_id": "p3",
                "evidence": {"data_id": "immune subtypes"},
                "terms": [target("CD4 T CELL")],
            },
        ]
    }

    assert MODULE.deg_catalog(document) == {
        "all markers": ["T CELL"],
        "immune subtypes": ["CD4 T CELL", "CD8 T CELL"],
    }


def test_validate_links_rejects_invented_source_ids():
    response = {
        "links": [
            {"claim_id": "claim:1", "data_id": "invented", "reason": "guess"}
        ]
    }

    with pytest.raises(ValueError, match="unknown data_id"):
        MODULE.validate_links(response, ["claim:1"], {"table-1"})


def test_label_baseline_prefers_narrower_exact_match():
    claims = [{"claim_id": "claim:1", "target": "T cell"}]
    catalog = {
        "all markers": ["T CELL", "B CELL", "NK CELL"],
        "lymphoid": ["T CELL", "B CELL"],
    }

    links = MODULE.label_baseline(claims, catalog)

    assert links[0]["data_id"] == "lymphoid"


def test_evaluation_separates_label_normalization_from_source_selection():
    predicted = [
        MODULE.MarkerTerm(
            "candidate", "t-cell", "ENSG1", "immune-table", (10, 30)
        )
    ]
    truth = [
        MODULE.MarkerTerm(
            "truth", "t cell", "ENSG1", "immune-table", (20, 40)
        )
    ]

    result = MODULE.evaluate(predicted, truth)

    assert result["triple_f1"] == 0.0
    assert result["source_gene_f1"] == 1.0
    assert result["exact_pair_evaluable"] == 0
    assert result["source_gene_evaluable"] == 1
    assert result["source_gene_link_accuracy"] == 1.0


def test_paired_summary_counts_discordant_linkage_results():
    rows = [
        {"llm_source_gene_correct": True, "baseline_source_gene_correct": False},
        {"llm_source_gene_correct": True, "baseline_source_gene_correct": True},
        {"llm_source_gene_correct": False, "baseline_source_gene_correct": True},
        {"llm_source_gene_correct": True, "baseline_source_gene_correct": False},
        {"llm_source_gene_correct": None, "baseline_source_gene_correct": None},
    ]

    result = MODULE.paired_summary(rows, "source_gene")

    assert result["evaluable"] == 4
    assert result["llm_correct"] == 3
    assert result["baseline_correct"] == 2
    assert result["llm_only_correct"] == 2
    assert result["baseline_only_correct"] == 1


def test_claim_review_counts_one_link_decision_for_multiple_genes():
    terms = [
        {
            "paper_id": "paper",
            "claim_id": "claim:1",
            "target_label": "t cell",
            "llm_data_id": "immune",
            "baseline_data_id": "",
            "exact_pair_truth_data_ids": "immune",
            "source_gene_truth_data_ids": "immune",
        },
        {
            "paper_id": "paper",
            "claim_id": "claim:1",
            "target_label": "t cell",
            "llm_data_id": "immune",
            "baseline_data_id": "",
            "exact_pair_truth_data_ids": "immune",
            "source_gene_truth_data_ids": "immune",
        },
    ]

    claims = MODULE.claim_review(terms)

    assert len(claims) == 1
    assert claims[0]["mapped_positive_terms"] == 2
    assert claims[0]["llm_source_gene_correct"] is True
