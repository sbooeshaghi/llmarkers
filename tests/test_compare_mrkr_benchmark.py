"""Unit tests for the modality-aware mrkr benchmark comparison."""

import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "analysis" / "compare_mrkr_benchmark.py"
SPEC = importlib.util.spec_from_file_location("compare_mrkr_benchmark", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_precision_recall_f1_uses_prediction_and_truth_roles():
    result = MODULE.prf({"A", "B"}, {"B", "C", "D"})
    assert result == {"precision": 0.5, "recall": 1 / 3, "f1": 0.4}


def test_source_metric_matches_gene_and_overlapping_interval():
    item = MODULE.EvidenceGene("p", "t", None, "G", "ENSG1", (10, 20))
    same = MODULE.EvidenceGene("h1", "x", None, "G", "ENSG1", (15, 30))
    wrong_gene = MODULE.EvidenceGene("h2", "x", None, "H", "ENSG2", (15, 30))
    disjoint = MODULE.EvidenceGene("h3", "x", None, "G", "ENSG1", (30, 40))

    result = MODULE.source_prf([item], [same, wrong_gene, disjoint])

    assert result["precision"] == 1.0
    assert result["recall"] == 1 / 3
    assert result["f1"] == 0.5


def test_normalizes_legacy_ontology_urls():
    value = "http://purl.obolibrary.org/obo/CL_0000235"
    assert MODULE.normalize_curie(value) == "CL:0000235"
