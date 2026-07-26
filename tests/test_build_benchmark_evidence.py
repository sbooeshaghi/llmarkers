"""Tests for the lossless benchmark evidence cutover."""

import importlib.util
import json
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[1] / "analysis" / "build_benchmark_evidence.py"
SPEC = importlib.util.spec_from_file_location("build_benchmark_evidence", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def human_record(source_type, gene="CD14", rationale="Macrophages express CD14."):
    return {
        "organism": "homo_sapiens",
        "group_label": " macrophages ",
        "group_name": "MACROPHAGE",
        "group_id": "CL:0000235",
        "feature_label": f" {gene} ",
        "feature_name": gene,
        "feature_id": f"ENSG-{gene}",
        "source_type": source_type,
        "source_rationale": rationale,
        "source_id": "manuscript.txt" if source_type == "text" else "Fig. 1a",
        "data_id": None,
    }


def deg_record(gene, logfc, rank):
    record = human_record("deg", gene=gene, rationale="unfiltered")
    record.update(
        {
            "source_id": "table-1",
            "data_id": "table-1",
            "metrics_pcorr": 0.01,
            "metrics_logfc": logfc,
            "metrics_rank": rank,
        }
    )
    return record


def write_manifest(tmp_path, human, deg, manuscript_text):
    manuscript = tmp_path / "manuscript.txt"
    manuscript.write_text(manuscript_text, encoding="utf-8")
    human_path = tmp_path / "human.json"
    human_path.write_text(json.dumps(human), encoding="utf-8")
    deg_path = tmp_path / "deg.json"
    deg_path.write_text(json.dumps(deg), encoding="utf-8")
    manifest = tmp_path / "sources.tsv"
    manifest.write_text(
        f"# schema: {MODULE.MANIFEST_SCHEMA}\n"
        "paper-1\tprimary\tground_truth\thuman\tmanuscript.txt\thuman.json\n"
        "paper-1\tprimary\tsupporting_data\tdeg\tmanuscript.txt\tdeg.json\n",
        encoding="utf-8",
    )
    return manifest, human_path, deg_path


def test_builder_separates_modalities_and_roundtrips_exactly(tmp_path):
    text = human_record("text")
    image = human_record("image", gene="LYZ", rationale="Dot plot markers.")
    human = [text, text.copy(), image]
    deg = [deg_record("CD14", 2.5, 1), deg_record("FCGR3A", -1.0, 2)]
    manifest, human_path, deg_path = write_manifest(
        tmp_path, human, deg, "Macrophages express CD14."
    )
    human_before = human_path.read_bytes()
    deg_before = deg_path.read_bytes()
    output = tmp_path / "derived"

    report = MODULE.build(manifest, output)

    text_document = json.loads(
        (output / "papers/paper-1/primary/text.claims.json").read_text()
    )
    image_document = json.loads(
        (output / "papers/paper-1/primary/image.claims.json").read_text()
    )
    deg_document = json.loads(
        (output / "papers/paper-1/primary/deg.profiles.json").read_text()
    )
    assert text_document["schema_version"] == MODULE.CLAIMS_SCHEMA
    assert image_document["evidence_type"] == "image"
    assert deg_document["schema_version"] == MODULE.PROFILES_SCHEMA
    assert len(text_document["claims"]) == 1
    text_genes = [
        term
        for term in text_document["claims"][0]["terms"]
        if term["term_type"] == "gene"
    ]
    assert len(text_genes) == 1
    assert len(text_genes[0]["source_records"]) == 2
    assert text_genes[0]["source_records"][0]["id"] != text_genes[0]["source_records"][1]["id"]
    assert text_document["claims"][0]["evidence"]["anchor_status"] == "exact"
    deg_genes = [
        term
        for term in deg_document["profiles"][0]["terms"]
        if term["term_type"] == "gene"
    ]
    assert [term["direction"] for term in deg_genes] == ["positive", "negative"]
    assert deg_genes[0]["metrics"] == {"pcorr": 0.01, "logfc": 2.5, "rank": 1}
    assert report["totals"] == {
        "source_records": 5,
        "derived_records": 5,
        "documents": 3,
        "review_warnings": 1,
    }
    assert report["checks"]["all_records_roundtrip_exactly"] is True
    assert human_path.read_bytes() == human_before
    assert deg_path.read_bytes() == deg_before
    review = (output / "review.tsv").read_text()
    assert "source.duplicate_records" in review


def test_unanchored_text_is_flagged_but_preserved(tmp_path):
    human = [human_record("text", rationale="A curator-normalized sentence.")]
    manifest, _, _ = write_manifest(
        tmp_path, human, [deg_record("CD14", 1.0, 1)], "Different manuscript text."
    )
    output = tmp_path / "derived"

    MODULE.build(manifest, output)

    document = json.loads(
        (output / "papers/paper-1/primary/text.claims.json").read_text()
    )
    evidence = document["claims"][0]["evidence"]
    assert evidence["anchor_status"] == "unanchored"
    assert evidence["span_offset"] is None
    assert evidence["span_literal"] == "A curator-normalized sentence."
    review = (output / "review.tsv").read_text()
    assert "text.anchor_unresolved" in review
    assert "text.gene_unanchored" in review


def test_builder_rejects_unexpected_human_source_type(tmp_path):
    human = [human_record("generated")]
    manifest, _, _ = write_manifest(
        tmp_path, human, [deg_record("CD14", 1.0, 1)], "text"
    )

    with pytest.raises(ValueError, match="source_type='generated'"):
        MODULE.build(manifest, tmp_path / "derived")
