"""Tests for the updated legacy joint marker-extraction experiment."""

import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))
SCRIPT = ANALYSIS / "evaluate_mrkr_joint_deg_extraction.py"
SPEC = importlib.util.spec_from_file_location(
    "evaluate_mrkr_joint_deg_extraction", SCRIPT
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def extraction(data_id="table#immune"):
    return {
        "organism": "homo_sapiens",
        "group_label": "Naive CD4+ T cells",
        "group_name": "NAIVE CD4+ T CELL",
        "feature_label": "IL7R",
        "feature_name": "IL7R",
        "source_rationale": "Naive CD4+ T cells expressed IL7R.",
        "data_id": data_id,
    }


def test_prompt_preserves_joint_legacy_task_and_exact_source_rules():
    prompt = MODULE.build_prompt(
        "Paper2026",
        {"table#immune": ["NAIVE CD4+ T CELL", "B CELL"]},
        "Naive CD4+ T cells expressed IL7R.",
    )

    assert "Extract ALL human cell type marker gene associations" in prompt
    assert "## table#immune" in prompt
    assert "MOST SPECIFIC applicable label" in prompt
    assert "source_rationale must be copied VERBATIM" in prompt
    assert '"extractions"' in prompt


def test_validate_response_rejects_invented_data_id():
    response = {"extractions": [extraction("invented")]}

    with pytest.raises(ValueError, match="unknown data_id"):
        MODULE.validate_raw_response(response, {"table#immune"})


def test_exact_label_fallback_prefers_narrower_source():
    catalog = {
        "table#all": ["NAIVE CD4+ T CELL", "B CELL", "NK CELL"],
        "table#immune": ["NAIVE CD4+ T CELL", "B CELL"],
    }

    assert (
        MODULE.exact_label_source("naive cd4+ t cell", catalog) == "table#immune"
    )


def test_legacy_extraction_adapts_to_valid_current_mrkr_claim():
    manuscript = "Naive CD4+ T cells expressed IL7R."
    response = {"extractions": [extraction()]}

    document, links, origins, report = MODULE.prepare_document(
        response,
        manuscript_text=manuscript,
        source_id="paper.txt",
        catalog={"table#immune": ["NAIVE CD4+ T CELL"]},
        mrkr_cwd=ROOT.parent / "mrkr",
    )

    assert len(document["claims"]) == 1
    claim_id = document["claims"][0]["claim_id"]
    assert links == {claim_id: "table#immune"}
    assert origins == {claim_id: "model"}
    assert report["validation"]["errors"] == []


def test_adapter_does_not_treat_an_absent_gene_as_explicit_evidence():
    row = extraction()
    row["source_rationale"] = "Naive CD4+ T cells were identified."

    claim, _data_id, _origin = MODULE.extraction_claim(
        row, {"table#immune": ["NAIVE CD4+ T CELL"]}
    )

    gene = next(term for term in claim["terms"] if term["term_type"] == "gene")
    assert gene["sub_span"] is None


def test_ambiguous_span_with_implicit_target_is_excluded():
    sentence = "These cells expressed IL7R."
    row = extraction()
    row["group_label"] = "Naive CD4+ T cells"
    row["source_rationale"] = sentence

    document, links, origins, report = MODULE.prepare_document(
        {"extractions": [row]},
        manuscript_text=f"{sentence}\n{sentence}",
        source_id="paper.txt",
        catalog={"table#immune": ["NAIVE CD4+ T CELL"]},
        mrkr_cwd=ROOT.parent / "mrkr",
    )

    assert document["claims"] == []
    assert links == {}
    assert origins == {}
    assert report["preparation"]["strict_exclusions"][0]["reason"] == (
        "ambiguous_implicit_target"
    )


def test_pair_and_triple_metrics_use_the_same_extracted_terms():
    predicted = [
        MODULE.MarkerTerm(
            "predicted", "naive cd4+ t cell", "ENSG1", "wrong-source", (0, 20)
        )
    ]
    truth = [
        MODULE.MarkerTerm(
            "truth", "naive cd4+ t cell", "ENSG1", "table#immune", (0, 20)
        )
    ]

    result = MODULE.evaluate(predicted, truth)

    assert result["pair_f1"] == 1.0
    assert result["triple_f1"] == 0.0
    assert result["source_gene_f1"] == 0.0
