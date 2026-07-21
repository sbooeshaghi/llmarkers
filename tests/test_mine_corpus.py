"""Tests for atomic corpus run bookkeeping."""

import importlib.util
import json
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "analysis" / "mine_corpus.py"
SPEC = importlib.util.spec_from_file_location("mine_corpus", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_completed_status_requires_matching_hashes(tmp_path):
    manuscript = tmp_path / "manuscript.md"
    manuscript.write_text("Macrophages express CD14.", encoding="utf-8")
    paper = MODULE.Paper("paper-1", "test", "homo_sapiens", manuscript)
    destination = MODULE.paper_dir(tmp_path / "out", paper)
    destination.mkdir(parents=True)
    artifact_names = (
        "paper.claims.json",
        "paper.onto.json",
        "metrics.json",
    )
    for name in artifact_names:
        (destination / name).write_text("{}\n", encoding="utf-8")
    status = {
        "schema_version": MODULE.STATUS_SCHEMA,
        "status": "complete",
        "paper_id": paper.paper_id,
        "collection": paper.collection,
        "organism": paper.organism,
        "manuscript": str(manuscript),
        "source_sha256": MODULE.sha256_file(manuscript),
        "mrkr_source_sha256": "sha256:mrkr",
        "artifacts": {
            name: MODULE.sha256_file(destination / name) for name in artifact_names
        },
    }
    (destination / "status.json").write_text(json.dumps(status), encoding="utf-8")

    assert MODULE.completed_status(tmp_path / "out", paper, "sha256:mrkr") == status
    status.pop("schema_version")
    (destination / "status.json").write_text(json.dumps(status), encoding="utf-8")
    assert MODULE.completed_status(tmp_path / "out", paper, "sha256:mrkr") is None

    status["schema_version"] = MODULE.STATUS_SCHEMA
    (destination / "status.json").write_text(json.dumps(status), encoding="utf-8")
    manuscript.write_text("Changed.", encoding="utf-8")
    assert MODULE.completed_status(tmp_path / "out", paper) is None


def test_manifest_uses_collection_to_avoid_id_collisions(tmp_path):
    manuscript = tmp_path / "manuscript.md"
    manuscript.write_text("text", encoding="utf-8")
    papers = [
        MODULE.Paper("same-id", "one", "homo_sapiens", manuscript),
        MODULE.Paper("same-id", "two", "homo_sapiens", manuscript),
    ]
    out = tmp_path / "out"
    for paper in papers:
        destination = MODULE.paper_dir(out, paper)
        destination.mkdir(parents=True)
        artifact_names = (
            "paper.claims.json",
            "paper.onto.json",
            "metrics.json",
        )
        for name in artifact_names:
            (destination / name).write_text("{}\n", encoding="utf-8")
        status = {
            "schema_version": MODULE.STATUS_SCHEMA,
            "status": "complete",
            "paper_id": paper.paper_id,
            "collection": paper.collection,
            "organism": paper.organism,
            "manuscript": str(manuscript),
            "source_sha256": MODULE.sha256_file(manuscript),
            "mrkr_source_sha256": "sha256:mrkr",
            "artifacts": {
                name: MODULE.sha256_file(destination / name)
                for name in artifact_names
            },
        }
        (destination / "status.json").write_text(json.dumps(status), encoding="utf-8")

    assert MODULE.write_completed_manifest(out, "sha256:mrkr") == 2
    rows = (out / "onto_manifest.tsv").read_text(encoding="utf-8").splitlines()
    assert rows[0] == f"# schema: {MODULE.ONTO_MANIFEST_SCHEMA}"
    assert "\tone\thomo_sapiens\tpapers/one/same-id/paper.onto.json\t" in rows[1]
    assert "\ttwo\thomo_sapiens\tpapers/two/same-id/paper.onto.json\t" in rows[2]


def test_source_manifest_requires_declared_schema(tmp_path):
    manifest = tmp_path / "sources.tsv"
    manuscript = tmp_path / "paper.md"
    manuscript.write_text("paper", encoding="utf-8")
    manifest.write_text(
        f"paper\ttest\thomo_sapiens\t{manuscript}\n", encoding="utf-8"
    )

    try:
        MODULE.load_manifest(manifest)
    except ValueError as error:
        assert MODULE.SOURCE_MANIFEST_SCHEMA in str(error)
    else:
        raise AssertionError("manifest without schema was accepted")


def test_reusable_claims_requires_matching_source_identity(tmp_path):
    manuscript = tmp_path / "paper.md"
    manuscript.write_text("paper", encoding="utf-8")
    paper = MODULE.Paper("paper-1", "test", "homo_sapiens", manuscript)
    destination = tmp_path / "paper-output"
    destination.mkdir()
    candidate = destination / "paper.claims.rejected.json"
    candidate.write_text(
        json.dumps(
            {
                "schema_version": "mrkr.claims.v1",
                "source": {
                    "id": paper.key,
                    "sha256": MODULE.sha256_file(manuscript),
                },
                "claims": [],
            }
        ),
        encoding="utf-8",
    )

    assert MODULE.reusable_claims(
        destination, paper, MODULE.sha256_file(manuscript)
    ) == candidate
    assert MODULE.reusable_claims(destination, paper, "sha256:different") is None
