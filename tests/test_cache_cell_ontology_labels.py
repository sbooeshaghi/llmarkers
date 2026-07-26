"""Tests for semantic auditing of Cell Ontology labels."""

import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "analysis" / "cache_cell_ontology_labels.py"
SPEC = importlib.util.spec_from_file_location("cache_cell_ontology_labels", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_parse_obo_and_classify_exact_labels(tmp_path):
    ontology = tmp_path / "cl.obo"
    ontology.write_text(
        "format-version: 1.2\n"
        "ontology: cl\n"
        "data-version: releases/2026-06-08\n\n"
        "[Term]\n"
        "id: CL:0000084\n"
        "name: T cell\n"
        'synonym: "T-cell" EXACT []\n'
        'synonym: "immature T cell" BROAD []\n\n'
        "[Term]\n"
        "id: CL:0000623\n"
        "name: natural killer cell\n"
        'synonym: "NK cell" EXACT []\n',
        encoding="utf-8",
    )

    terms, metadata = MODULE.parse_obo(ontology)

    assert metadata["data_version"] == "releases/2026-06-08"
    assert MODULE.classify_label("T CELL", terms["CL:0000084"]) == (
        True,
        "canonical",
    )
    assert MODULE.classify_label("T-cell", terms["CL:0000084"]) == (
        True,
        "exact_synonym",
    )
    assert MODULE.classify_label("CD8-positive T cell", terms["CL:0000084"]) == (
        False,
        "none",
    )
    assert MODULE.classify_label("immature T cell", terms["CL:0000084"]) == (
        False,
        "none",
    )


def test_normalize_label_preserves_semantic_punctuation():
    assert MODULE.normalize_label("  Natural   Killer Cell ") == "natural killer cell"
    assert MODULE.normalize_label("T-cell") != MODULE.normalize_label("T cell")
