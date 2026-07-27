#!/usr/bin/env python3
"""Build the browser database from the normalized mrkr claim database."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sqlite3
import tempfile
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote


CLAIM_SCHEMA_VERSION = "llmarkers.claim-db.v3"
WEB_SCHEMA_VERSION = "llmarkers.web-db.v1"
GITHUB_REPOSITORY = "https://github.com/sbooeshaghi/llmarkers/blob/main"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def read_tsv(path: Path, required_columns: set[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, delimiter="\t")
        columns = set(reader.fieldnames or [])
        missing = required_columns - columns
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(sorted(missing))}")
        return [dict(row) for row in reader]


def load_paper_index(path: Path) -> dict[str, dict[str, str]]:
    rows = read_tsv(
        path,
        {"paper_key", "paper_id", "collection", "manuscript", "title"},
    )
    papers: dict[str, dict[str, str]] = {}
    for row in rows:
        paper_key = row["paper_key"]
        if paper_key in papers:
            raise ValueError(f"{path}: duplicate paper_key {paper_key}")
        if paper_key != f"{row['collection']}:{row['paper_id']}":
            raise ValueError(f"{path}: inconsistent paper_key {paper_key}")
        papers[paper_key] = row
    return papers


def load_hca_metadata(path: Path) -> dict[str, dict[str, str]]:
    rows = read_tsv(path, {"folder", "doi", "publication_title"})
    metadata: dict[str, dict[str, str]] = {}
    for row in rows:
        folder = row["folder"]
        if folder in metadata:
            raise ValueError(f"{path}: duplicate HCA folder {folder}")
        metadata[folder] = row
    return metadata


def load_cell_ontology_audit(path: Path) -> list[dict[str, str]]:
    rows = read_tsv(
        path,
        {
            "term_type",
            "curie",
            "observed_label",
            "current_exact",
            "semantic_exact",
            "match_source",
            "canonical_label",
            "exact_synonyms",
            "obsolete",
        },
    )
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        key = (row["term_type"], row["curie"], row["observed_label"])
        if key in seen:
            raise ValueError(f"{path}: duplicate ontology audit row {key}")
        if row["term_type"] not in {"celltype", "comparison"}:
            raise ValueError(f"{path}: unsupported term_type {row['term_type']!r}")
        if row["semantic_exact"] not in {"0", "1"}:
            raise ValueError(f"{path}: invalid semantic_exact for {key}")
        seen.add(key)
    return rows


def repository_source_url(manuscript_path: str) -> str:
    encoded = "/".join(quote(part) for part in manuscript_path.split("/"))
    return f"{GITHUB_REPOSITORY}/{encoded}"


def paper_metadata_rows(
    connection: sqlite3.Connection,
    paper_index: dict[str, dict[str, str]],
    hca_metadata: dict[str, dict[str, str]],
) -> list[tuple[str, str, str | None, str, str, str]]:
    rows: list[tuple[str, str, str | None, str, str, str]] = []
    papers = connection.execute(
        "SELECT paper_key, paper_id, collection FROM papers ORDER BY paper_key"
    ).fetchall()
    for paper_key, paper_id, collection in papers:
        indexed = paper_index.get(paper_key)
        if indexed is None:
            raise ValueError(f"paper index is missing {paper_key}")
        manuscript_path = indexed["manuscript"].strip()
        title = indexed["title"].strip()
        doi: str | None = None
        metadata_source = "corpus-paper-index"

        if collection == "hca":
            hca = hca_metadata.get(paper_id)
            if hca is None:
                raise ValueError(f"HCA manifest is missing {paper_id}")
            title = hca["publication_title"].strip() or title
            doi = hca["doi"].strip() or None
            metadata_source = "hca-manuscript-manifest"

        if not title:
            raise ValueError(f"paper metadata has no title for {paper_key}")
        if not manuscript_path:
            raise ValueError(f"paper metadata has no manuscript path for {paper_key}")

        source_url = (
            f"https://doi.org/{quote(doi, safe='/')}"
            if doi
            else repository_source_url(manuscript_path)
        )
        rows.append(
            (
                paper_key,
                title,
                doi,
                source_url,
                manuscript_path,
                metadata_source,
            )
        )
    return rows


def build_claim_context(connection: sqlite3.Connection) -> None:
    context: dict[str, dict[str, list[dict[str, object]]]] = defaultdict(
        lambda: {"comparison": [], "tissue": []}
    )
    for row in connection.execute(
        """
        SELECT t.claim_key, t.term_type, t.normalized_label, t.ontology_term,
               t.exact, t.provenance, a.semantic_exact, a.match_source,
               a.canonical_label
        FROM terms t
        LEFT JOIN cell_ontology_label_audit a
          ON a.term_type=t.term_type
         AND a.curie=t.ontology_term
         AND a.observed_label=t.normalized_label
        WHERE t.term_type IN ('comparison', 'tissue')
        ORDER BY t.claim_key, t.ordinal
        """
    ):
        (
            claim_key,
            term_type,
            label,
            candidate_curie,
            tagger_exact,
            provenance,
            semantic_exact,
            match_source,
            canonical_label,
        ) = row
        accepted_curie = candidate_curie
        if term_type == "comparison":
            accepted_curie = candidate_curie if semantic_exact == 1 else None
        context[claim_key][term_type].append(
            {
                "label": label,
                "curie": accepted_curie,
                "candidate_curie": candidate_curie,
                "tagger_exact": None if tagger_exact is None else bool(tagger_exact),
                "semantic_exact": (
                    None if semantic_exact is None else bool(semantic_exact)
                ),
                "match_source": match_source,
                "canonical_label": canonical_label,
                "provenance": provenance,
            }
        )

    claim_rows = connection.execute("SELECT claim_key FROM claims ORDER BY claim_key")
    connection.executemany(
        "INSERT INTO claim_context VALUES(?, ?, ?)",
        (
            (
                claim_key,
                json.dumps(context[claim_key]["comparison"], separators=(",", ":")),
                json.dumps(context[claim_key]["tissue"], separators=(",", ":")),
            )
            for (claim_key,) in claim_rows
        ),
    )


def add_web_schema(
    connection: sqlite3.Connection,
    *,
    claims_db: Path,
    paper_index_path: Path,
    hca_manifest_path: Path,
    cell_ontology_audit_path: Path,
) -> None:
    schema_version = connection.execute(
        "SELECT value FROM metadata WHERE key='schema_version'"
    ).fetchone()
    if schema_version is None or schema_version[0] != CLAIM_SCHEMA_VERSION:
        actual = None if schema_version is None else schema_version[0]
        raise ValueError(
            f"{claims_db}: expected {CLAIM_SCHEMA_VERSION}, found {actual!r}"
        )

    paper_index = load_paper_index(paper_index_path)
    hca_metadata = load_hca_metadata(hca_manifest_path)
    cell_ontology_audit = load_cell_ontology_audit(cell_ontology_audit_path)
    connection.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE paper_metadata(
          paper_key TEXT PRIMARY KEY REFERENCES papers(paper_key),
          title TEXT NOT NULL,
          doi TEXT,
          source_url TEXT NOT NULL,
          manuscript_path TEXT NOT NULL,
          metadata_source TEXT NOT NULL
        );
        CREATE TABLE claim_context(
          claim_key TEXT PRIMARY KEY REFERENCES claims(claim_key),
          comparison_terms_json TEXT NOT NULL,
          tissue_terms_json TEXT NOT NULL
        );
        CREATE TABLE cell_ontology_label_audit(
          term_type TEXT NOT NULL CHECK(term_type IN ('celltype','comparison')),
          curie TEXT NOT NULL,
          observed_label TEXT NOT NULL,
          tagger_exact INTEGER NOT NULL CHECK(tagger_exact IN (0,1)),
          semantic_exact INTEGER NOT NULL CHECK(semantic_exact IN (0,1)),
          match_source TEXT NOT NULL,
          canonical_label TEXT NOT NULL,
          exact_synonyms TEXT NOT NULL,
          obsolete INTEGER NOT NULL CHECK(obsolete IN (0,1)),
          PRIMARY KEY(term_type, curie, observed_label)
        );
        CREATE INDEX idx_paper_metadata_title
          ON paper_metadata(title COLLATE NOCASE);
        CREATE INDEX idx_terms_label_nocase
          ON terms(normalized_label COLLATE NOCASE);
        CREATE INDEX idx_terms_curie_nocase
          ON terms(ontology_term COLLATE NOCASE);
        """
    )
    connection.executemany(
        "INSERT INTO paper_metadata VALUES(?, ?, ?, ?, ?, ?)",
        paper_metadata_rows(connection, paper_index, hca_metadata),
    )
    connection.executemany(
        "INSERT INTO cell_ontology_label_audit VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            (
                row["term_type"],
                row["curie"],
                row["observed_label"],
                int(row["current_exact"]),
                int(row["semantic_exact"]),
                row["match_source"],
                row["canonical_label"],
                row["exact_synonyms"],
                int(row["obsolete"]),
            )
            for row in cell_ontology_audit
        ),
    )
    build_claim_context(connection)
    connection.executescript(
        """
        CREATE VIEW web_marker_evidence AS
          SELECT pc.profile_key, m.paper_key, p.paper_id, p.collection,
                 pm.title, pm.doi, pm.source_url, pm.manuscript_path,
                 m.claim_key, c.claim_id,
                 m.organism_label, m.organism_curie,
                 m.target_label,
                 CASE WHEN audit.semantic_exact=1 THEN m.target_curie END AS target_curie,
                 m.target_curie AS target_candidate_curie,
                 m.target_exact AS target_tagger_exact,
                 COALESCE(audit.semantic_exact, 0) AS target_semantic_exact,
                 audit.match_source AS target_match_source,
                 audit.canonical_label AS target_canonical_label,
                 m.gene_symbol, m.gene_curie, m.gene_exact, m.direction,
                 cc.comparison_terms_json, cc.tissue_terms_json,
                 m.span_literal, m.summary
          FROM marker_evidence m
          JOIN papers p ON p.paper_key = m.paper_key
          JOIN paper_metadata pm ON pm.paper_key = m.paper_key
          JOIN claims c ON c.claim_key = m.claim_key
          JOIN claim_context cc ON cc.claim_key = m.claim_key
          JOIN profile_claims pc ON pc.claim_key = m.claim_key
          LEFT JOIN cell_ontology_label_audit audit
            ON audit.term_type='celltype'
           AND audit.curie=m.target_curie
           AND audit.observed_label=m.target_label;
        """
    )

    metadata = {
        "website_schema_version": WEB_SCHEMA_VERSION,
        "website_source_db_sha256": sha256_file(claims_db),
        "website_paper_index_sha256": sha256_file(paper_index_path),
        "website_hca_manifest_sha256": sha256_file(hca_manifest_path),
        "website_cell_ontology_audit_sha256": sha256_file(
            cell_ontology_audit_path
        ),
    }
    connection.executemany(
        "INSERT INTO metadata(key, value) VALUES(?, ?)", metadata.items()
    )


def validate_web_database(connection: sqlite3.Connection) -> None:
    checks = {
        "paper metadata": (
            "SELECT COUNT(*) FROM paper_metadata",
            "SELECT COUNT(*) FROM papers",
        ),
        "claim context": (
            "SELECT COUNT(*) FROM claim_context",
            "SELECT COUNT(*) FROM claims",
        ),
        "web marker evidence": (
            "SELECT COUNT(*) FROM web_marker_evidence",
            "SELECT COUNT(*) FROM marker_evidence",
        ),
    }
    for label, (left_sql, right_sql) in checks.items():
        left = connection.execute(left_sql).fetchone()[0]
        right = connection.execute(right_sql).fetchone()[0]
        if left != right:
            raise RuntimeError(f"{label} count mismatch: {left} != {right}")
    missing_titles = connection.execute(
        "SELECT COUNT(*) FROM paper_metadata WHERE trim(title)=''"
    ).fetchone()[0]
    if missing_titles:
        raise RuntimeError(f"paper metadata contains {missing_titles} empty titles")
    missing_audit = connection.execute(
        """
        SELECT COUNT(*)
        FROM (
          SELECT DISTINCT t.term_type, t.ontology_term, t.normalized_label
          FROM terms t
          LEFT JOIN cell_ontology_label_audit a
            ON a.term_type=t.term_type
           AND a.curie=t.ontology_term
           AND a.observed_label=t.normalized_label
          WHERE t.term_type IN ('celltype','comparison')
            AND t.ontology_term IS NOT NULL
            AND a.curie IS NULL
        )
        """
    ).fetchone()[0]
    if missing_audit:
        raise RuntimeError(
            f"cell ontology audit is missing {missing_audit} mapped label-ID pairs"
        )
    integrity = connection.execute("PRAGMA integrity_check").fetchone()[0]
    if integrity != "ok":
        raise RuntimeError(f"SQLite integrity check failed: {integrity}")


def build_database(
    claims_db: Path,
    paper_index: Path,
    hca_manifest: Path,
    cell_ontology_audit: Path,
    output: Path,
) -> None:
    for path in (claims_db, paper_index, hca_manifest, cell_ontology_audit):
        if not path.is_file():
            raise FileNotFoundError(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    os.close(handle)
    temporary = Path(temporary_name)
    try:
        source = sqlite3.connect(f"file:{claims_db}?mode=ro", uri=True)
        destination = sqlite3.connect(temporary)
        try:
            source.backup(destination)
            add_web_schema(
                destination,
                claims_db=claims_db,
                paper_index_path=paper_index,
                hca_manifest_path=hca_manifest,
                cell_ontology_audit_path=cell_ontology_audit,
            )
            destination.commit()
            validate_web_database(destination)
            destination.execute("PRAGMA optimize")
            destination.execute("VACUUM")
        finally:
            source.close()
            destination.close()
        os.replace(temporary, output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build docs/llmarkers.sqlite from the normalized claim database."
    )
    parser.add_argument("--claims-db", required=True, type=Path)
    parser.add_argument("--paper-index", required=True, type=Path)
    parser.add_argument("--hca-manifest", required=True, type=Path)
    parser.add_argument("--cell-ontology-audit", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_database(
        args.claims_db,
        args.paper_index,
        args.hca_manifest,
        args.cell_ontology_audit,
        args.out,
    )
    with sqlite3.connect(args.out) as connection:
        counts = {
            name: connection.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
            for name in ("papers", "claims", "terms", "profiles", "web_marker_evidence")
        }
    print(", ".join(f"{name}={count}" for name, count in counts.items()))


if __name__ == "__main__":
    main()
