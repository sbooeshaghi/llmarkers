#!/usr/bin/env python3
"""Run mrkr over the LLMarkers corpora with atomic, auditable outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CORPUS_GLOBS = {
    "biorxiv": "data/biorxiv/meca/*/manuscript.md",
    "hca": "data/hca/manuscripts/*/manuscript.md",
}
CORPUS_ORGANISMS = {
    "biorxiv": "homo_sapiens",
    "hca": "homo_sapiens",
}
DEFAULT_MRKR_PROJECT = REPO.parent / "mrkr"
DEFAULT_MRKR_COMMAND = "uv run --project . --locked mrkr"
SOURCE_MANIFEST_SCHEMA = "llmarkers.source-manifest.v2"
ONTO_MANIFEST_SCHEMA = "llmarkers.onto-manifest.v2"
STATUS_SCHEMA = "llmarkers.corpus-status.v1"
RUN_SCHEMA = "llmarkers.corpus-run.v1"
SOURCE_SNAPSHOT_SCHEMA = "llmarkers.source-snapshot.v1"


@dataclass(frozen=True)
class Paper:
    paper_id: str
    collection: str
    organism: str
    manuscript: Path

    @property
    def key(self) -> str:
        return f"{self.collection}/{self.paper_id}"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def sha256_mrkr_source(project: Path) -> str:
    """Fingerprint the code, prompts, packaged data, and lock file used by mrkr."""

    paths = [project / "pyproject.toml", project / "uv.lock"]
    package = project / "mrkr"
    if package.is_dir():
        paths.extend(
            path
            for path in package.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        )
    digest = hashlib.sha256()
    for path in sorted(paths):
        if not path.is_file():
            continue
        relative = path.relative_to(project).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def enumerate_papers(collections: list[str]) -> list[Paper]:
    """Enumerate source manuscripts without consulting prior extraction outputs."""

    papers: list[Paper] = []
    for collection in collections:
        organism = CORPUS_ORGANISMS[collection]
        for manuscript in sorted(REPO.glob(CORPUS_GLOBS[collection])):
            papers.append(
                Paper(manuscript.parent.name, collection, organism, manuscript)
            )
    return papers


def source_set_sha256(papers: list[Paper]) -> str:
    digest = hashlib.sha256()
    for paper in sorted(papers, key=lambda item: item.key):
        digest.update(paper.key.encode("utf-8"))
        digest.update(b"\0")
        digest.update(paper.organism.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(paper.manuscript).encode("ascii"))
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def write_source_snapshot(out: Path, papers: list[Paper]) -> Path:
    rows = [
        f"# schema: {SOURCE_SNAPSHOT_SCHEMA}\n",
        "paper_id\tcollection\torganism\tmanuscript\tsource_sha256\n",
    ]
    for paper in sorted(papers, key=lambda item: item.key):
        rows.append(
            f"{paper.paper_id}\t{paper.collection}\t{paper.organism}\t"
            f"{display_path(paper.manuscript)}\t{sha256_file(paper.manuscript)}\n"
        )
    destination = out / "source_manifest.tsv"
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tsv.tmp")
    temporary.write_text("".join(rows), encoding="utf-8")
    os.replace(temporary, destination)
    return destination


def load_manifest(path: Path) -> list[Paper]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != f"# schema: {SOURCE_MANIFEST_SCHEMA}":
        raise ValueError(
            f"{path}: first line must be '# schema: {SOURCE_MANIFEST_SCHEMA}'"
        )
    papers: list[Paper] = []
    for line_number, line in enumerate(lines, 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 4:
            raise ValueError(
                f"{path}:{line_number}: expected paper_id, collection, organism, manuscript"
            )
        if fields[2] != "homo_sapiens":
            raise ValueError(
                f"{path}:{line_number}: corpus runner currently supports homo_sapiens"
            )
        manuscript = Path(fields[3])
        if not manuscript.is_absolute():
            manuscript = (path.parent / manuscript).resolve()
        if not manuscript.is_file():
            raise FileNotFoundError(f"{path}:{line_number}: {manuscript}")
        papers.append(Paper(fields[0], fields[1], fields[2], manuscript))
    return papers


def paper_dir(out: Path, paper: Paper) -> Path:
    return out / "papers" / paper.collection / paper.paper_id


def completed_status(
    out: Path, paper: Paper, mrkr_source_sha256: str | None = None
) -> dict | None:
    directory = paper_dir(out, paper)
    status_path = directory / "status.json"
    if not status_path.is_file():
        return None
    try:
        status = json.loads(status_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if status.get("schema_version") != STATUS_SCHEMA:
        return None
    if status.get("status") != "complete":
        return None
    if any(
        status.get(field) != expected
        for field, expected in (
            ("paper_id", paper.paper_id),
            ("collection", paper.collection),
            ("organism", paper.organism),
        )
    ):
        return None
    if status.get("source_sha256") != sha256_file(paper.manuscript):
        return None
    if mrkr_source_sha256 is not None and status.get(
        "mrkr_source_sha256"
    ) != mrkr_source_sha256:
        return None
    artifacts = status.get("artifacts")
    if not isinstance(artifacts, dict):
        return None
    for name in ("paper.claims.json", "paper.onto.json"):
        artifact = directory / name
        if not artifact.is_file() or artifacts.get(name) != sha256_file(artifact):
            return None
    for name, expected_hash in artifacts.items():
        artifact = directory / name
        if not artifact.is_file() or expected_hash != sha256_file(artifact):
            return None
    return status


def display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO))
    except ValueError:
        return str(path.resolve())


def run_command(command: list[str], *, cwd: Path, log, timeout: int) -> None:
    environment = os.environ.copy()
    environment.pop("VIRTUAL_ENV", None)
    subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        stdout=log,
        stderr=subprocess.STDOUT,
        check=True,
        timeout=timeout,
    )


def reusable_claims(
    destination: Path,
    paper: Paper,
    source_sha256: str,
    mrkr_source_sha256: str,
) -> Path | None:
    """Return a source-matched, previously accepted claim document."""

    status_path = destination / "status.json"
    if not status_path.is_file():
        return None
    try:
        status = json.loads(status_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        status.get("schema_version") != STATUS_SCHEMA
        or status.get("source_sha256") != source_sha256
        or status.get("mrkr_source_sha256") != mrkr_source_sha256
    ):
        return None

    for name in ("paper.claims.json",):
        candidate = destination / name
        if not candidate.is_file():
            continue
        try:
            document = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if (
            document.get("schema_version") == "mrkr.claims.v1"
            and document.get("source", {}).get("id") == paper.key
            and document.get("source", {}).get("sha256") == source_sha256
            and document.get("producer", {}).get("name") == "mrkr"
            and str(
                document.get("extraction", {}).get("prompt_template_sha256", "")
            ).startswith("sha256:")
        ):
            return candidate
    return None


def run_paper(
    paper: Paper,
    out: Path,
    mrkr_command: list[str],
    mrkr_cwd: Path,
    mrkr_source_sha256: str,
    extract_timeout: int,
) -> tuple[Paper, str]:
    if completed_status(out, paper, mrkr_source_sha256):
        return paper, "skip"

    destination = paper_dir(out, paper)
    destination.mkdir(parents=True, exist_ok=True)
    source_sha = sha256_file(paper.manuscript)
    started = utc_now()
    reusable = reusable_claims(
        destination, paper, source_sha, mrkr_source_sha256
    )

    with tempfile.TemporaryDirectory(prefix="mrkr-", dir=destination) as temporary:
        temporary_path = Path(temporary)
        claims = temporary_path / "paper.claims.json"
        onto = temporary_path / "paper.onto.json"
        metrics = temporary_path / "metrics.json"
        response = temporary_path / "response.json"
        log_path = temporary_path / "log.txt"
        try:
            with log_path.open("w", encoding="utf-8") as log:
                if reusable is not None:
                    log.write(f"Reusing canonical claims: {reusable.name}\n")
                    log.flush()
                    shutil.copy2(reusable, claims)
                    prior_metrics = destination / "metrics.json"
                    if prior_metrics.is_file():
                        shutil.copy2(prior_metrics, metrics)
                    else:
                        write_json_atomic(
                            metrics,
                            {"reused_claims": True, "source": reusable.name},
                        )
                    prior_response = destination / "response.json"
                    if prior_response.is_file():
                        shutil.copy2(prior_response, response)
                    run_command(
                        mrkr_command
                        + [
                            "validate",
                            str(claims),
                            "--manuscript",
                            str(paper.manuscript),
                        ],
                        cwd=mrkr_cwd,
                        log=log,
                        timeout=120,
                    )
                else:
                    run_command(
                        mrkr_command
                        + [
                            "extract",
                            "--manuscript",
                            str(paper.manuscript),
                            "--output",
                            str(claims),
                            "--source-id",
                            paper.key,
                            "--organism",
                            paper.organism,
                            "--metrics",
                            str(metrics),
                            "--response",
                            str(response),
                        ],
                        cwd=mrkr_cwd,
                        log=log,
                        timeout=extract_timeout,
                    )
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
                run_command(
                    mrkr_command
                    + ["validate", str(onto), "--manuscript", str(paper.manuscript)],
                    cwd=mrkr_cwd,
                    log=log,
                    timeout=120,
                )

            for name in (
                "paper.claims.json",
                "paper.onto.json",
                "metrics.json",
                "response.json",
                "log.txt",
            ):
                source = temporary_path / name
                if source.exists():
                    os.replace(source, destination / name)
            for stale in (
                "paper.claims.rejected.json",
                "paper.claims.validation.json",
            ):
                (destination / stale).unlink(missing_ok=True)
            onto_document = json.loads(
                (destination / "paper.onto.json").read_text(encoding="utf-8")
            )
            if onto_document.get("source", {}).get("id") != paper.key:
                raise ValueError("paper.onto.json source.id does not match the corpus key")
            artifact_names = [
                "paper.claims.json",
                "paper.onto.json",
                "metrics.json",
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
                "source_sha256": source_sha,
                "mrkr_source_sha256": mrkr_source_sha256,
                "claims_reused": reusable is not None,
                "artifacts": {
                    name: sha256_file(destination / name) for name in artifact_names
                },
                "started_at": started,
                "finished_at": utc_now(),
            }
            write_json_atomic(destination / "status.json", status)
            return paper, "complete"
        except Exception as exc:
            for stale in ("paper.claims.json", "paper.onto.json"):
                (destination / stale).unlink(missing_ok=True)
            for source in temporary_path.iterdir():
                if source.is_file():
                    os.replace(source, destination / source.name)
            status = {
                "schema_version": STATUS_SCHEMA,
                "status": "failed",
                "paper_id": paper.paper_id,
                "collection": paper.collection,
                "organism": paper.organism,
                "manuscript": display_path(paper.manuscript),
                "source_sha256": source_sha,
                "mrkr_source_sha256": mrkr_source_sha256,
                "started_at": started,
                "finished_at": utc_now(),
                "error": f"{type(exc).__name__}: {exc}",
            }
            write_json_atomic(destination / "status.json", status)
            return paper, "failed"


def completed_papers_from_statuses(out: Path) -> list[Paper]:
    """Recover all corpus papers represented by completed status records."""

    papers: list[Paper] = []
    for status_path in sorted((out / "papers").glob("*/*/status.json")):
        try:
            status = json.loads(status_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        manuscript = Path(status.get("manuscript") or "")
        if not manuscript.is_absolute():
            manuscript = (REPO / manuscript).resolve()
        if not manuscript.is_file():
            continue
        if not all(
            isinstance(status.get(field), str) and status.get(field)
            for field in ("paper_id", "collection", "organism")
        ):
            continue
        papers.append(
            Paper(
                status["paper_id"],
                status["collection"],
                status["organism"],
                manuscript,
            )
        )
    return papers


def write_completed_manifest(out: Path, mrkr_source_sha256: str) -> int:
    rows = [f"# schema: {ONTO_MANIFEST_SCHEMA}\n"]
    for paper in completed_papers_from_statuses(out):
        status = completed_status(out, paper, mrkr_source_sha256)
        if status:
            onto = paper_dir(out, paper) / "paper.onto.json"
            onto_hash = status["artifacts"]["paper.onto.json"]
            rows.append(
                f"{paper.paper_id}\t{paper.collection}\t{paper.organism}\t"
                f"{onto.relative_to(out)}\t{onto_hash}\t{status['source_sha256']}\n"
            )
    manifest = out / "onto_manifest.tsv"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    temporary = manifest.with_suffix(".tsv.tmp")
    temporary.write_text("".join(rows), encoding="utf-8")
    os.replace(temporary, manifest)
    return len(rows) - 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--manifest", type=Path)
    source.add_argument("--corpus", choices=["biorxiv", "hca", "both"], default="both")
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--mrkr-command", default=DEFAULT_MRKR_COMMAND)
    parser.add_argument("--mrkr-cwd", type=Path, default=DEFAULT_MRKR_PROJECT)
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-partial", action="store_true")
    parser.add_argument("--extract-timeout", type=int, default=1200)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.jobs < 1:
        raise ValueError("--jobs must be at least 1")
    if args.manifest:
        papers = load_manifest(args.manifest)
    else:
        collections = ["biorxiv", "hca"] if args.corpus == "both" else [args.corpus]
        papers = enumerate_papers(collections)
    if args.limit is not None:
        papers = papers[: args.limit]
    keys = [paper.key for paper in papers]
    if len(keys) != len(set(keys)):
        raise ValueError("paper_id must be unique within each collection")

    command = shlex.split(args.mrkr_command)
    if not command:
        raise ValueError("--mrkr-command cannot be empty")
    mrkr_cwd = args.mrkr_cwd.resolve()
    if not mrkr_cwd.is_dir():
        raise FileNotFoundError(f"mrkr working directory not found: {mrkr_cwd}")
    mrkr_source_sha256 = sha256_mrkr_source(mrkr_cwd)
    selected_source_sha256 = source_set_sha256(papers)

    out = args.out.resolve()
    complete_before = sum(
        completed_status(out, paper, mrkr_source_sha256) is not None
        for paper in papers
    )
    print(f"papers: {len(papers)}; complete: {complete_before}; pending: {len(papers) - complete_before}")
    print(f"source set: {selected_source_sha256}")
    if args.dry_run:
        print("dry-run: no files were changed")
        return 0

    source_snapshot = write_source_snapshot(out, papers)

    counts = {"complete": 0, "skip": 0, "failed": 0}
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {
            executor.submit(
                run_paper,
                paper,
                out,
                command,
                mrkr_cwd,
                mrkr_source_sha256,
                args.extract_timeout,
            ): paper
            for paper in papers
        }
        for index, future in enumerate(as_completed(futures), 1):
            paper, status = future.result()
            counts[status] += 1
            print(f"[{index}/{len(papers)}] {paper.key}: {status}")

    run_record = {
        "schema_version": RUN_SCHEMA,
        "finished_at": utc_now(),
        "mrkr_command": command,
        "mrkr_source_sha256": mrkr_source_sha256,
        "source_set_sha256": selected_source_sha256,
        "source_snapshot": display_path(source_snapshot),
        "source_snapshot_sha256": sha256_file(source_snapshot),
        "source_manifest_sha256": (
            sha256_file(args.manifest) if args.manifest else None
        ),
        "n_requested": len(papers),
        "counts": counts,
        "allow_partial": args.allow_partial,
    }
    write_json_atomic(out / "run.json", run_record)
    if counts["failed"] and not args.allow_partial:
        (out / "onto_manifest.tsv").unlink(missing_ok=True)
        print("corpus run failed; manifest was not updated", file=sys.stderr)
        return 1
    n_manifest = write_completed_manifest(out, mrkr_source_sha256)
    print(f"manifest: {n_manifest} validated papers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
