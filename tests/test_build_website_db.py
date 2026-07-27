"""Tests for the browser-facing normalized claim database."""

import importlib.util
import json
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CLAIMS = load_script("build_claim_db_for_web_test", ROOT / "analysis/build_claim_db.py")
WEBSITE = load_script("build_website_db", ROOT / "analysis/build_website_db.py")


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
                "span_literal": "Macrophages express CD14 relative to monocytes in blood.",
                "span_offset": [0, 57],
                "summary": (
                    "In Homo sapiens blood, macrophage expresses CD14 relative to "
                    "monocyte."
                ),
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
                        "sub_span": "monocytes",
                        "sub_offset": [37, 46],
                        "normalized_label": "monocyte",
                        "term_type": "comparison",
                        "provenance": "explicit",
                        "ontology_term": "CL:0000576",
                        "exact": True,
                    },
                    {
                        "sub_span": "blood",
                        "sub_offset": [50, 55],
                        "normalized_label": "blood",
                        "term_type": "tissue",
                        "provenance": "explicit",
                        "ontology_term": "UBERON:0000178",
                        "exact": True,
                    },
                ],
            }
        ],
    }


def build_claim_fixture(tmp_path: Path) -> Path:
    onto = tmp_path / "paper.onto.json"
    onto.write_text(json.dumps(onto_document()), encoding="utf-8")
    manifest = tmp_path / "onto_manifest.tsv"
    manifest.write_text(
        f"# schema: {CLAIMS.ONTO_MANIFEST_SCHEMA}\n"
        f"paper-1\ttest\thomo_sapiens\tpaper.onto.json\t"
        f"{CLAIMS.sha256_file(onto)}\tsha256:source\n",
        encoding="utf-8",
    )
    database = tmp_path / "claims.sqlite"
    CLAIMS.build_database(manifest, database, exact_only=True)
    return database


def write_cell_ontology_audit(
    tmp_path: Path, *, target_semantic_exact: int = 1
) -> Path:
    audit = tmp_path / "cell_ontology_label_audit.tsv"
    audit.write_text(
        "term_type\tcurie\tobserved_label\tcurrent_exact\tsemantic_exact\t"
        "match_source\tcanonical_label\texact_synonyms\tobsolete\n"
        f"celltype\tCL:0000235\tmacrophage\t1\t{target_semantic_exact}\t"
        f"{'canonical' if target_semantic_exact else 'none'}\tmacrophage\t"
        "histiocyte\t0\n"
        "comparison\tCL:0000576\tmonocyte\t1\t1\tcanonical\tmonocyte\t\t0\n",
        encoding="utf-8",
    )
    return audit


def test_web_database_preserves_claims_and_adds_source_metadata(tmp_path):
    claims_db = build_claim_fixture(tmp_path)
    paper_index = tmp_path / "papers.tsv"
    paper_index.write_text(
        "paper_key\tpaper_id\tcollection\tmanuscript\ttitle\n"
        "test:paper-1\tpaper-1\ttest\tdata/test/paper-1/manuscript.md\t"
        "A macrophage marker study\n",
        encoding="utf-8",
    )
    hca_manifest = tmp_path / "hca.tsv"
    hca_manifest.write_text(
        "folder\tdoi\tpublication_title\n",
        encoding="utf-8",
    )
    audit = write_cell_ontology_audit(tmp_path)
    output = tmp_path / "llmarkers.sqlite"

    WEBSITE.build_database(claims_db, paper_index, hca_manifest, audit, output)

    with sqlite3.connect(output) as connection:
        assert connection.execute("SELECT COUNT(*) FROM terms").fetchone()[0] == 5
        assert connection.execute(
            "SELECT value FROM metadata WHERE key='website_schema_version'"
        ).fetchone()[0] == WEBSITE.WEB_SCHEMA_VERSION
        title, source_url = connection.execute(
            "SELECT title, source_url FROM paper_metadata"
        ).fetchone()
        assert title == "A macrophage marker study"
        assert source_url.endswith("/data/test/paper-1/manuscript.md")

        row = connection.execute(
            """
            SELECT target_label, target_curie, gene_symbol, gene_curie,
                   comparison_terms_json, tissue_terms_json, span_literal
            FROM web_marker_evidence
            """
        ).fetchone()
        assert row[:4] == (
            "macrophage",
            "CL:0000235",
            "CD14",
            "ENSG00000170458",
        )
        comparison = json.loads(row[4])[0]
        assert comparison["label"] == "monocyte"
        assert comparison["curie"] == "CL:0000576"
        assert comparison["candidate_curie"] == "CL:0000576"
        assert comparison["semantic_exact"] is True
        assert comparison["match_source"] == "canonical"
        assert json.loads(row[5])[0]["curie"] == "UBERON:0000178"
        assert row[6].startswith("Macrophages express CD14")


def test_web_database_rejects_missing_paper_metadata(tmp_path):
    claims_db = build_claim_fixture(tmp_path)
    paper_index = tmp_path / "papers.tsv"
    paper_index.write_text(
        "paper_key\tpaper_id\tcollection\tmanuscript\ttitle\n",
        encoding="utf-8",
    )
    hca_manifest = tmp_path / "hca.tsv"
    hca_manifest.write_text(
        "folder\tdoi\tpublication_title\n",
        encoding="utf-8",
    )
    audit = write_cell_ontology_audit(tmp_path)

    try:
        WEBSITE.build_database(
            claims_db,
            paper_index,
            hca_manifest,
            audit,
            tmp_path / "llmarkers.sqlite",
        )
    except ValueError as error:
        assert "paper index is missing test:paper-1" in str(error)
    else:
        raise AssertionError("missing paper metadata was accepted")


def test_web_database_does_not_promote_an_unverified_ontology_candidate(tmp_path):
    claims_db = build_claim_fixture(tmp_path)
    paper_index = tmp_path / "papers.tsv"
    paper_index.write_text(
        "paper_key\tpaper_id\tcollection\tmanuscript\ttitle\n"
        "test:paper-1\tpaper-1\ttest\tdata/test/paper-1/manuscript.md\t"
        "A macrophage marker study\n",
        encoding="utf-8",
    )
    hca_manifest = tmp_path / "hca.tsv"
    hca_manifest.write_text(
        "folder\tdoi\tpublication_title\n",
        encoding="utf-8",
    )
    audit = write_cell_ontology_audit(tmp_path, target_semantic_exact=0)
    output = tmp_path / "llmarkers.sqlite"

    WEBSITE.build_database(claims_db, paper_index, hca_manifest, audit, output)

    with sqlite3.connect(output) as connection:
        row = connection.execute(
            """
            SELECT target_curie, target_candidate_curie, target_semantic_exact,
                   target_match_source
            FROM web_marker_evidence
            """
        ).fetchone()
        assert row == (None, "CL:0000235", 0, "none")
