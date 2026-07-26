"""Tests for the normalized claim database."""

import importlib.util
import json
import sqlite3
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "analysis" / "build_claim_db.py"
SPEC = importlib.util.spec_from_file_location("build_claim_db", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def onto_document():
    return {
        "schema_version": "mrkr.onto.v1",
        "source": {"id": "test/paper-1", "sha256": "sha256:source"},
        "grounding": {
            "genes": {
                "provider": "offline-gene-map",
                "organism": "homo_sapiens",
                "sha256": "sha256:map",
            },
            "organism": {
                "provider": "NCBI Taxonomy",
                "label": "Homo sapiens",
                "ontology_term": "NCBITaxon:9606",
            },
            "ontology_service": {
                "provider": "OLS4",
                "endpoint": "https://example.test/ols",
                "queries": [],
            },
        },
        "claims": [
            {
                "claim_id": "claim:one",
                "span_literal": "Macrophages express CD14 in blood.",
                "span_offset": [0, 36],
                "summary": "In Homo sapiens, macrophage expresses CD14 in blood.",
                "terms": [
                    {
                        "sub_span": None,
                        "sub_offset": None,
                        "normalized_label": "Homo sapiens",
                        "term_type": "organism",
                        "provenance": "implicit",
                        "ontology_term": "NCBITaxon:9606",
                        "exact": True,
                    },
                    {
                        "sub_span": "Macrophages",
                        "sub_offset": [0, 11],
                        "normalized_label": "macrophage",
                        "term_type": "celltype",
                        "provenance": "explicit",
                        "ontology_term": "CL:0000235",
                        "exact": True,
                    },
                    {
                        "sub_span": "CD14",
                        "sub_offset": [20, 24],
                        "normalized_label": "CD14",
                        "term_type": "gene",
                        "provenance": "explicit",
                        "ontology_term": "ENSG00000170458",
                        "exact": True,
                        "direction": "positive",
                    },
                    {
                        "sub_span": "blood",
                        "sub_offset": [28, 33],
                        "normalized_label": "blood",
                        "term_type": "tissue",
                        "provenance": "explicit",
                        "ontology_term": None,
                        "exact": None,
                    },
                ],
            }
        ],
    }


def test_database_retains_claim_terms_and_unresolved_labels(tmp_path):
    onto = tmp_path / "paper.onto.json"
    onto.write_text(json.dumps(onto_document()), encoding="utf-8")
    manifest = tmp_path / "onto_manifest.tsv"
    manifest.write_text(
        f"# schema: {MODULE.ONTO_MANIFEST_SCHEMA}\n"
        f"paper-1\ttest\thomo_sapiens\tpaper.onto.json\t"
        f"{MODULE.sha256_file(onto)}\tsha256:source\n",
        encoding="utf-8",
    )
    database = tmp_path / "claims.sqlite"

    MODULE.build_database(manifest, database, exact_only=True)

    with sqlite3.connect(database) as connection:
        assert connection.execute("SELECT COUNT(*) FROM papers").fetchone()[0] == 1
        assert connection.execute("SELECT organism FROM papers").fetchone()[0] == (
            "homo_sapiens"
        )
        assert connection.execute("SELECT COUNT(*) FROM claims").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM terms").fetchone()[0] == 4
        assert connection.execute("SELECT COUNT(*) FROM marker_evidence").fetchone()[0] == 1
        tissue = connection.execute(
            "SELECT normalized_label, ontology_term FROM terms WHERE term_type='tissue'"
        ).fetchone()
        assert tissue == ("blood", None)
        organism = connection.execute(
            "SELECT normalized_label, ontology_term FROM terms "
            "WHERE term_type='organism'"
        ).fetchone()
        assert organism == ("Homo sapiens", "NCBITaxon:9606")
        marker_organism = connection.execute(
            "SELECT organism_label, organism_curie FROM marker_evidence"
        ).fetchone()
        assert marker_organism == ("Homo sapiens", "NCBITaxon:9606")
        profile = connection.execute(
            "SELECT target_label, target_curie, target_exact FROM profiles"
        ).fetchone()
        assert profile == ("macrophage", "CL:0000235", 1)
        assert connection.execute(
            "SELECT value FROM metadata WHERE key='closure_mode'"
        ).fetchone()[0] == "exact-only"
        assert connection.execute("SELECT onto_path FROM papers").fetchone()[0] == (
            "paper.onto.json"
        )


def test_database_rejects_a_manifest_document_identity_mismatch(tmp_path):
    document = onto_document()
    document["source"]["id"] = "test/different-paper"
    onto = tmp_path / "paper.onto.json"
    onto.write_text(json.dumps(document), encoding="utf-8")
    manifest = tmp_path / "onto_manifest.tsv"
    manifest.write_text(
        f"# schema: {MODULE.ONTO_MANIFEST_SCHEMA}\n"
        f"paper-1\ttest\thomo_sapiens\tpaper.onto.json\t"
        f"{MODULE.sha256_file(onto)}\tsha256:source\n",
        encoding="utf-8",
    )

    try:
        MODULE.build_database(manifest, tmp_path / "claims.sqlite", exact_only=True)
    except ValueError as error:
        assert "source.id" in str(error)
    else:
        raise AssertionError("mismatched source id was accepted")


def test_database_rejects_an_onto_digest_mismatch(tmp_path):
    onto = tmp_path / "paper.onto.json"
    onto.write_text(json.dumps(onto_document()), encoding="utf-8")
    manifest = tmp_path / "onto_manifest.tsv"
    manifest.write_text(
        f"# schema: {MODULE.ONTO_MANIFEST_SCHEMA}\n"
        "paper-1\ttest\thomo_sapiens\tpaper.onto.json\t"
        "sha256:wrong\tsha256:source\n",
        encoding="utf-8",
    )

    try:
        MODULE.build_database(manifest, tmp_path / "claims.sqlite", exact_only=True)
    except ValueError as error:
        assert "digest" in str(error)
    else:
        raise AssertionError("mismatched ontology artifact digest was accepted")
