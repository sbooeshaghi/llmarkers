#!/usr/bin/env python3
"""Build a normalized SQLite database from validated mrkr onto documents."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import tempfile
from pathlib import Path


SCHEMA_VERSION = "llmarkers.claim-db.v2"
ONTO_SCHEMA = "mrkr.onto.v1"
ONTO_MANIFEST_SCHEMA = "llmarkers.onto-manifest.v2"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def load_manifest(
    path: Path,
) -> list[tuple[str, str, str, Path, str, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != f"# schema: {ONTO_MANIFEST_SCHEMA}":
        raise ValueError(
            f"{path}: first line must be '# schema: {ONTO_MANIFEST_SCHEMA}'"
        )
    rows: list[tuple[str, str, str, Path, str, str, str]] = []
    for line_number, line in enumerate(lines, 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 6:
            raise ValueError(
                f"{path}:{line_number}: expected paper_id, collection, organism, "
                "onto_path, onto_sha256, source_sha256"
            )
        locator = fields[3]
        onto_path = Path(locator)
        if not onto_path.is_absolute():
            onto_path = (path.parent / onto_path).resolve()
        if not onto_path.is_file():
            raise FileNotFoundError(f"{path}:{line_number}: {onto_path}")
        rows.append(
            (fields[0], fields[1], fields[2], onto_path, locator, fields[4], fields[5])
        )
    return rows


def load_onto(
    path: Path,
    *,
    organism: str,
    onto_sha256: str,
    source_sha256: str,
) -> dict:
    if sha256_file(path) != onto_sha256:
        raise ValueError(f"{path}: digest does not match the validated manifest")
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("schema_version") != ONTO_SCHEMA:
        raise ValueError(f"{path}: expected {ONTO_SCHEMA}")
    if not isinstance(document.get("source"), dict) or not document["source"].get("sha256"):
        raise ValueError(f"{path}: missing source metadata")
    if not isinstance(document.get("claims"), list):
        raise ValueError(f"{path}: claims must be an array")
    if document["source"]["sha256"] != source_sha256:
        raise ValueError(f"{path}: source digest does not match the validated manifest")
    grounded_organism = document.get("grounding", {}).get("genes", {}).get("organism")
    if grounded_organism != organism:
        raise ValueError(f"{path}: grounding organism does not match the manifest")
    return document


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE metadata(
          key TEXT PRIMARY KEY,
          value TEXT NOT NULL
        );
        CREATE TABLE papers(
          paper_key TEXT PRIMARY KEY,
          paper_id TEXT NOT NULL,
          collection TEXT NOT NULL,
          organism TEXT NOT NULL,
          source_id TEXT NOT NULL,
          source_sha256 TEXT NOT NULL,
          onto_sha256 TEXT NOT NULL,
          onto_path TEXT NOT NULL,
          UNIQUE(collection, paper_id)
        );
        CREATE TABLE claims(
          claim_key TEXT PRIMARY KEY,
          claim_id TEXT NOT NULL,
          paper_key TEXT NOT NULL REFERENCES papers(paper_key),
          span_literal TEXT NOT NULL,
          span_start INTEGER NOT NULL,
          span_end INTEGER NOT NULL,
          summary TEXT NOT NULL,
          UNIQUE(paper_key, claim_id)
        );
        CREATE TABLE terms(
          term_key TEXT PRIMARY KEY,
          claim_key TEXT NOT NULL REFERENCES claims(claim_key),
          ordinal INTEGER NOT NULL,
          term_type TEXT NOT NULL CHECK(term_type IN ('gene','celltype','comparison','tissue')),
          normalized_label TEXT NOT NULL,
          sub_span TEXT,
          sub_start INTEGER,
          sub_end INTEGER,
          provenance TEXT NOT NULL CHECK(provenance IN ('explicit','implicit')),
          ontology_term TEXT,
          exact INTEGER CHECK(exact IN (0,1) OR exact IS NULL),
          direction TEXT CHECK(direction IN ('positive','negative') OR direction IS NULL),
          UNIQUE(claim_key, ordinal)
        );
        CREATE TABLE profiles(
          profile_key TEXT PRIMARY KEY,
          paper_key TEXT NOT NULL REFERENCES papers(paper_key),
          target_label TEXT NOT NULL,
          target_curie TEXT,
          target_exact INTEGER CHECK(target_exact IN (0,1) OR target_exact IS NULL),
          UNIQUE(paper_key, target_label, target_curie, target_exact)
        );
        CREATE TABLE profile_claims(
          profile_key TEXT NOT NULL REFERENCES profiles(profile_key),
          claim_key TEXT NOT NULL REFERENCES claims(claim_key),
          PRIMARY KEY(profile_key, claim_key)
        );
        CREATE TABLE ontology_terms(
          curie TEXT PRIMARY KEY,
          ontology TEXT NOT NULL
        );
        CREATE TABLE term_labels(
          curie TEXT NOT NULL REFERENCES ontology_terms(curie),
          label TEXT NOT NULL,
          source TEXT NOT NULL,
          PRIMARY KEY(curie, label, source)
        );
        CREATE TABLE term_closure(
          curie TEXT NOT NULL REFERENCES ontology_terms(curie),
          ancestor_curie TEXT NOT NULL REFERENCES ontology_terms(curie),
          relation TEXT NOT NULL,
          PRIMARY KEY(curie, ancestor_curie)
        );
        CREATE VIEW marker_evidence AS
          SELECT c.paper_key, c.claim_key, target.normalized_label AS target_label,
                 target.ontology_term AS target_curie, target.exact AS target_exact,
                 gene.normalized_label AS gene_symbol, gene.ontology_term AS gene_curie,
                 gene.exact AS gene_exact, gene.direction,
                 c.span_literal, c.summary
          FROM claims c
          JOIN terms target ON target.claim_key = c.claim_key AND target.term_type = 'celltype'
          JOIN terms gene ON gene.claim_key = c.claim_key AND gene.term_type = 'gene';
        CREATE VIEW profile_markers AS
          SELECT DISTINCT p.profile_key, m.gene_symbol, m.gene_curie, m.direction
          FROM profiles p
          JOIN profile_claims pc ON pc.profile_key = p.profile_key
          JOIN marker_evidence m ON m.claim_key = pc.claim_key;
        CREATE INDEX idx_claims_paper ON claims(paper_key);
        CREATE INDEX idx_terms_claim ON terms(claim_key);
        CREATE INDEX idx_terms_type_curie ON terms(term_type, ontology_term);
        CREATE INDEX idx_profiles_target ON profiles(target_curie, target_exact);
        CREATE INDEX idx_closure_ancestor ON term_closure(ancestor_curie);
        """
    )


def ontology_name(curie: str) -> str:
    prefix = curie.split(":", 1)[0]
    if prefix == "CL":
        return "cl"
    if prefix == "UBERON":
        return "uberon"
    if curie.startswith("ENSG"):
        return "ensembl"
    return prefix.lower()


def add_ontology_term(
    connection: sqlite3.Connection, curie: str, label: str | None, source: str
) -> None:
    connection.execute(
        "INSERT OR IGNORE INTO ontology_terms(curie, ontology) VALUES(?, ?)",
        (curie, ontology_name(curie)),
    )
    if label:
        connection.execute(
            "INSERT OR IGNORE INTO term_labels(curie, label, source) VALUES(?, ?, ?)",
            (curie, label, source),
        )


def stable_key(*parts: object) -> str:
    value = "\t".join("" if part is None else str(part) for part in parts)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:24]


def insert_document(
    connection: sqlite3.Connection,
    paper_id: str,
    collection: str,
    organism: str,
    onto_path: Path,
    onto_locator: str,
    document: dict,
) -> None:
    paper_key = f"{collection}:{paper_id}"
    source = document["source"]
    if source["id"] != f"{collection}/{paper_id}":
        raise ValueError(
            f"{onto_path}: source.id must be {collection}/{paper_id}, got {source['id']}"
        )
    connection.execute(
        "INSERT INTO papers VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
        (
            paper_key,
            paper_id,
            collection,
            organism,
            source["id"],
            source["sha256"],
            sha256_file(onto_path),
            onto_locator,
        ),
    )

    for claim in document["claims"]:
        claim_id = claim["claim_id"]
        claim_key = f"{paper_key}:{claim_id}"
        span_start, span_end = claim["span_offset"]
        connection.execute(
            "INSERT INTO claims VALUES(?, ?, ?, ?, ?, ?, ?)",
            (
                claim_key,
                claim_id,
                paper_key,
                claim["span_literal"],
                span_start,
                span_end,
                claim["summary"],
            ),
        )

        targets = [term for term in claim["terms"] if term["term_type"] == "celltype"]
        if len(targets) != 1:
            raise ValueError(f"{onto_path}: {claim_id} has {len(targets)} target cell types")
        target = targets[0]
        profile_key = "profile:" + stable_key(
            paper_key,
            target["normalized_label"],
            target.get("ontology_term"),
            target.get("exact"),
        )
        connection.execute(
            "INSERT OR IGNORE INTO profiles VALUES(?, ?, ?, ?, ?)",
            (
                profile_key,
                paper_key,
                target["normalized_label"],
                target.get("ontology_term"),
                target.get("exact"),
            ),
        )
        connection.execute(
            "INSERT INTO profile_claims VALUES(?, ?)", (profile_key, claim_key)
        )

        for ordinal, term in enumerate(claim["terms"]):
            term_key = f"term:{stable_key(claim_key, ordinal)}"
            sub_offset = term.get("sub_offset")
            sub_start, sub_end = (sub_offset if sub_offset is not None else (None, None))
            connection.execute(
                "INSERT INTO terms VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    term_key,
                    claim_key,
                    ordinal,
                    term["term_type"],
                    term["normalized_label"],
                    term.get("sub_span"),
                    sub_start,
                    sub_end,
                    term["provenance"],
                    term.get("ontology_term"),
                    term.get("exact"),
                    term.get("direction"),
                ),
            )
            curie = term.get("ontology_term")
            if curie:
                add_ontology_term(connection, curie, term["normalized_label"], "mrkr")


def load_closure(connection: sqlite3.Connection, path: Path) -> None:
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) not in {2, 4}:
            raise ValueError(
                f"{path}:{line_number}: expected curie, ancestor_curie[, curie_label, ancestor_label]"
            )
        curie, ancestor = fields[:2]
        labels = fields[2:] if len(fields) == 4 else (None, None)
        add_ontology_term(connection, curie, labels[0], "closure")
        add_ontology_term(connection, ancestor, labels[1], "closure")
        connection.execute(
            "INSERT OR IGNORE INTO term_closure VALUES(?, ?, ?)",
            (curie, ancestor, "self" if curie == ancestor else "ancestor"),
        )


def add_reflexive_closure(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        INSERT OR IGNORE INTO term_closure(curie, ancestor_curie, relation)
        SELECT curie, curie, 'self' FROM ontology_terms
        WHERE ontology IN ('cl', 'uberon')
        """
    )


def build_database(
    manifest: Path,
    output: Path,
    *,
    closure: Path | None = None,
    exact_only: bool = False,
) -> None:
    if (closure is None) == (not exact_only):
        raise ValueError("choose exactly one of closure or exact_only")
    rows = load_manifest(manifest)
    output.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    try:
        connection = sqlite3.connect(temporary)
        try:
            create_schema(connection)
            connection.execute("INSERT INTO metadata VALUES(?, ?)", ("schema_version", SCHEMA_VERSION))
            connection.execute(
                "INSERT INTO metadata VALUES(?, ?)",
                ("closure_mode", "provided" if closure else "exact-only"),
            )
            connection.execute(
                "INSERT INTO metadata VALUES(?, ?)",
                ("manifest_sha256", sha256_file(manifest)),
            )
            for (
                paper_id,
                collection,
                organism,
                onto_path,
                onto_locator,
                onto_sha256,
                source_sha256,
            ) in rows:
                insert_document(
                    connection,
                    paper_id,
                    collection,
                    organism,
                    onto_path,
                    onto_locator,
                    load_onto(
                        onto_path,
                        organism=organism,
                        onto_sha256=onto_sha256,
                        source_sha256=source_sha256,
                    ),
                )
            if closure:
                load_closure(connection, closure)
            add_reflexive_closure(connection)
            connection.commit()
            integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
            if integrity != "ok":
                raise RuntimeError(f"SQLite integrity check failed: {integrity}")
        finally:
            connection.close()
        os.replace(temporary, output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    closure_mode = parser.add_mutually_exclusive_group(required=True)
    closure_mode.add_argument("--closure", type=Path)
    closure_mode.add_argument("--exact-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_database(
        args.manifest,
        args.out,
        closure=args.closure,
        exact_only=args.exact_only,
    )
    with sqlite3.connect(args.out) as connection:
        counts = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in ("papers", "claims", "terms", "profiles")
        }
    print(", ".join(f"{name}={count}" for name, count in counts.items()))


if __name__ == "__main__":
    main()
