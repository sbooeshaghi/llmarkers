#!/usr/bin/env python3
"""Recover valid claims from corpus papers with localized validation failures."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import tempfile
from pathlib import Path

from mine_corpus import (
    DEFAULT_MRKR_COMMAND,
    DEFAULT_MRKR_PROJECT,
    STATUS_SCHEMA,
    Paper,
    display_path,
    paper_dir,
    run_command,
    sha256_file,
    sha256_mrkr_source,
    utc_now,
    write_completed_manifest,
    write_json_atomic,
)


REPAIR_SCHEMA = "llmarkers.corpus-repair.v1"
CLAIM_INDEX = re.compile(r"^claims\[(\d+)\]")
GENE_MISMATCH = re.compile(
    r"gene label '([^']+)' resolves to [^,]+, but source span '([^']+)' resolves to"
)


def failed_papers(out: Path, mrkr_source_sha256: str) -> list[Paper]:
    papers: list[Paper] = []
    for status_path in sorted((out / "papers").glob("*/*/status.json")):
        status = json.loads(status_path.read_text(encoding="utf-8"))
        if status.get("status") != "failed":
            continue
        if status.get("mrkr_source_sha256") != mrkr_source_sha256:
            continue
        manuscript = Path(status["manuscript"])
        if not manuscript.is_absolute():
            manuscript = (Path(__file__).resolve().parents[1] / manuscript).resolve()
        papers.append(
            Paper(
                paper_id=status["paper_id"],
                collection=status["collection"],
                organism=status["organism"],
                manuscript=manuscript,
            )
        )
    return papers


def invalid_claim_indexes(validation: dict) -> dict[int, list[dict]]:
    invalid: dict[int, list[dict]] = {}
    for error in validation.get("errors", []):
        match = CLAIM_INDEX.match(str(error.get("path", "")))
        if match:
            invalid.setdefault(int(match.group(1)), []).append(error)
    return invalid


def drop_invalid_claims(document: dict, validation: dict) -> list[dict]:
    invalid = invalid_claim_indexes(validation)
    claims = document.get("claims", [])
    actions: list[dict] = []
    kept: list[dict] = []
    for index, claim in enumerate(claims):
        if index not in invalid:
            kept.append(claim)
            continue
        actions.append(
            {
                "action": "drop_claim",
                "claim_id": claim.get("claim_id"),
                "claim_index": index,
                "reason": invalid[index],
            }
        )
    document["claims"] = kept
    return actions


def drop_mismatched_gene(document: dict, label: str, span: str) -> list[dict]:
    actions: list[dict] = []
    kept_claims: list[dict] = []
    for claim in document.get("claims", []):
        terms = claim.get("terms", [])
        kept_terms = []
        removed = []
        for term in terms:
            if (
                term.get("term_type") == "gene"
                and term.get("normalized_label") == label
                and term.get("sub_span") == span
            ):
                removed.append(term)
            else:
                kept_terms.append(term)
        if not removed:
            kept_claims.append(claim)
            continue
        actions.append(
            {
                "action": "drop_gene_term",
                "claim_id": claim.get("claim_id"),
                "normalized_label": label,
                "source_span": span,
                "reason": "gene label and source span resolve to different genes",
            }
        )
        claim["terms"] = kept_terms
        if any(term.get("term_type") == "gene" for term in kept_terms):
            kept_claims.append(claim)
        else:
            actions.append(
                {
                    "action": "drop_claim",
                    "claim_id": claim.get("claim_id"),
                    "reason": "no marker gene remained after removing a mismatched term",
                }
            )
    document["claims"] = kept_claims
    return actions


def load_repair_source(destination: Path) -> tuple[dict, Path, list[dict]]:
    rejected = destination / "paper.claims.rejected.json"
    accepted = destination / "paper.claims.json"
    validation_path = destination / "paper.claims.validation.json"
    if rejected.is_file():
        source = rejected
    elif accepted.is_file():
        source = accepted
    else:
        raise FileNotFoundError("no retained claim document")
    document = json.loads(source.read_text(encoding="utf-8"))
    actions: list[dict] = []
    if validation_path.is_file():
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        actions.extend(drop_invalid_claims(document, validation))
    return document, source, actions


def run_ground(
    document: dict,
    paper: Paper,
    destination: Path,
    mrkr_command: list[str],
    mrkr_cwd: Path,
) -> tuple[Path, Path, list[dict]]:
    actions: list[dict] = []
    with tempfile.TemporaryDirectory(prefix="repair-", dir=destination) as temporary:
        temporary_path = Path(temporary)
        claims = temporary_path / "paper.claims.json"
        onto = temporary_path / "paper.onto.json"
        log_path = temporary_path / "repair.log.txt"
        for _ in range(10):
            write_json_atomic(claims, document)
            onto.unlink(missing_ok=True)
            with log_path.open("a", encoding="utf-8") as log:
                run_command(
                    mrkr_command
                    + ["validate", str(claims), "--manuscript", str(paper.manuscript)],
                    cwd=mrkr_cwd,
                    log=log,
                    timeout=120,
                )
                try:
                    run_command(
                        mrkr_command
                        + [
                            "ground",
                            str(claims),
                            "--output",
                            str(onto),
                            "--manuscript",
                            str(paper.manuscript),
                            "--organism",
                            paper.organism,
                        ],
                        cwd=mrkr_cwd,
                        log=log,
                        timeout=600,
                    )
                except subprocess.CalledProcessError:
                    log.flush()
                    text = log_path.read_text(encoding="utf-8")
                    mismatches = GENE_MISMATCH.findall(text)
                    new_actions: list[dict] = []
                    for label, span in mismatches:
                        new_actions.extend(drop_mismatched_gene(document, label, span))
                    if not new_actions:
                        raise
                    actions.extend(new_actions)
                    continue
                run_command(
                    mrkr_command
                    + ["validate", str(onto), "--manuscript", str(paper.manuscript)],
                    cwd=mrkr_cwd,
                    log=log,
                    timeout=120,
                )
            final_claims = destination / "paper.claims.json"
            final_onto = destination / "paper.onto.json"
            final_log = destination / "repair.log.txt"
            os.replace(claims, final_claims)
            os.replace(onto, final_onto)
            os.replace(log_path, final_log)
            return final_claims, final_onto, actions
    raise RuntimeError("grounding repair exceeded ten attempts")


def repair_paper(
    paper: Paper,
    out: Path,
    mrkr_command: list[str],
    mrkr_cwd: Path,
    mrkr_source_sha256: str,
) -> str:
    destination = paper_dir(out, paper)
    started = utc_now()
    try:
        document, source, actions = load_repair_source(destination)
        original_hash = sha256_file(source)
        claims, onto, grounding_actions = run_ground(
            document, paper, destination, mrkr_command, mrkr_cwd
        )
        actions.extend(grounding_actions)
        repair = {
            "schema_version": REPAIR_SCHEMA,
            "paper_id": paper.key,
            "source_claims": source.name,
            "source_claims_sha256": original_hash,
            "actions": actions,
            "n_claims_retained": len(document.get("claims", [])),
            "finished_at": utc_now(),
        }
        repair_path = destination / "paper.claims.repair.json"
        write_json_atomic(repair_path, repair)
        onto_document = json.loads(onto.read_text(encoding="utf-8"))
        if onto_document.get("source", {}).get("id") != paper.key:
            raise ValueError("paper.onto.json source.id does not match the corpus key")
        artifact_names = [
            "paper.claims.json",
            "paper.onto.json",
            "metrics.json",
            "paper.claims.repair.json",
            "repair.log.txt",
        ]
        if (destination / "response.json").is_file():
            artifact_names.append("response.json")
        status = {
            "schema_version": STATUS_SCHEMA,
            "status": "complete",
            "paper_id": paper.paper_id,
            "collection": paper.collection,
            "organism": paper.organism,
            "manuscript": display_path(paper.manuscript),
            "source_sha256": sha256_file(paper.manuscript),
            "mrkr_source_sha256": mrkr_source_sha256,
            "claims_reused": True,
            "claims_repaired": True,
            "artifacts": {
                name: sha256_file(destination / name) for name in artifact_names
            },
            "started_at": started,
            "finished_at": utc_now(),
        }
        write_json_atomic(destination / "status.json", status)
        return "complete"
    except Exception as exc:
        write_json_atomic(
            destination / "repair.status.json",
            {
                "schema_version": REPAIR_SCHEMA,
                "status": "failed",
                "paper_id": paper.key,
                "error": f"{type(exc).__name__}: {exc}",
                "started_at": started,
                "finished_at": utc_now(),
            },
        )
        return "failed"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--mrkr-command", default=DEFAULT_MRKR_COMMAND)
    parser.add_argument("--mrkr-cwd", type=Path, default=DEFAULT_MRKR_PROJECT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out = args.out.resolve()
    mrkr_cwd = args.mrkr_cwd.resolve()
    mrkr_command = shlex.split(args.mrkr_command)
    mrkr_source_sha256 = sha256_mrkr_source(mrkr_cwd)
    papers = failed_papers(out, mrkr_source_sha256)
    counts = {"complete": 0, "failed": 0}
    for index, paper in enumerate(papers, 1):
        result = repair_paper(
            paper, out, mrkr_command, mrkr_cwd, mrkr_source_sha256
        )
        counts[result] += 1
        print(f"[{index}/{len(papers)}] {paper.key}: {result}")
    manifest_count = write_completed_manifest(out, mrkr_source_sha256)
    write_json_atomic(
        out / "repair_run.json",
        {
            "schema_version": REPAIR_SCHEMA,
            "mrkr_source_sha256": mrkr_source_sha256,
            "counts": counts,
            "manifest_count": manifest_count,
            "finished_at": utc_now(),
        },
    )
    print(f"manifest: {manifest_count} validated papers")
    return 1 if counts["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
