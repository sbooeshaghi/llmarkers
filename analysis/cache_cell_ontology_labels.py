#!/usr/bin/env python3
"""Audit observed Cell Ontology mappings against canonical and exact labels."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sqlite3
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


SCHEMA_VERSION = "llmarkers.cell-ontology-label-audit.v1"
EXACT_SYNONYM = re.compile(r'^synonym: "((?:[^"\\]|\\.)*)" EXACT(?: |$)')


@dataclass
class OntologyLabel:
    canonical_label: str = ""
    exact_synonyms: set[str] = field(default_factory=set)
    obsolete: bool = False


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def normalize_label(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold().strip()
    value = value.replace("\u2010", "-").replace("\u2011", "-")
    return " ".join(value.split())


def unescape_obo_string(value: str) -> str:
    return value.replace(r"\"", '"').replace(r"\\", "\\")


def parse_obo(path: Path) -> tuple[dict[str, OntologyLabel], dict[str, str]]:
    terms: dict[str, OntologyLabel] = {}
    metadata: dict[str, str] = {}
    stanza: dict[str, object] | None = None

    def finish() -> None:
        if not stanza or not stanza.get("id"):
            return
        curie = str(stanza["id"])
        if not curie.startswith("CL:"):
            return
        terms[curie] = OntologyLabel(
            canonical_label=str(stanza.get("name", "")),
            exact_synonyms=set(stanza.get("exact_synonyms", set())),
            obsolete=bool(stanza.get("obsolete", False)),
        )

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "[Term]":
            finish()
            stanza = {"exact_synonyms": set()}
            continue
        if line.startswith("["):
            finish()
            stanza = None
            continue
        if stanza is None:
            if line.startswith("ontology:"):
                metadata["ontology"] = line.split(":", 1)[1].strip()
            elif line.startswith("data-version:"):
                metadata["data_version"] = line.split(":", 1)[1].strip()
            continue
        if line.startswith("id:"):
            stanza["id"] = line.split(":", 1)[1].strip()
        elif line.startswith("name:"):
            stanza["name"] = line.split(":", 1)[1].strip()
        elif line == "is_obsolete: true":
            stanza["obsolete"] = True
        else:
            match = EXACT_SYNONYM.match(line)
            if match:
                synonyms = stanza["exact_synonyms"]
                assert isinstance(synonyms, set)
                synonyms.add(unescape_obo_string(match.group(1)))
    finish()
    return terms, metadata


def classify_label(observed: str, term: OntologyLabel) -> tuple[bool, str]:
    observed_key = normalize_label(observed)
    if observed_key == normalize_label(term.canonical_label):
        return True, "canonical"
    if observed_key in {normalize_label(value) for value in term.exact_synonyms}:
        return True, "exact_synonym"
    return False, "none"


def observed_mappings(database: Path) -> list[tuple[str, str, str, int | None]]:
    with sqlite3.connect(database) as connection:
        return connection.execute(
            """
            SELECT DISTINCT term_type, ontology_term, normalized_label, exact
            FROM terms
            WHERE term_type IN ('celltype', 'comparison')
              AND ontology_term LIKE 'CL:%'
            ORDER BY term_type, ontology_term, normalized_label
            """
        ).fetchall()


def build_audit(
    database: Path,
    ontology: Path,
    output_dir: Path,
    *,
    source_url: str = "",
) -> dict[str, object]:
    terms, ontology_metadata = parse_obo(ontology)
    mappings = observed_mappings(database)
    output_dir.mkdir(parents=True, exist_ok=True)
    audit_path = output_dir / "cell_ontology_label_audit.tsv"
    rows: list[dict[str, object]] = []
    missing_curies: set[str] = set()

    for term_type, curie, observed, current_exact in mappings:
        ontology_term = terms.get(curie)
        if ontology_term is None:
            missing_curies.add(curie)
            semantic_match, match_source = False, "missing_curie"
            canonical_label, exact_synonyms, obsolete = "", "", ""
        else:
            semantic_match, match_source = classify_label(observed, ontology_term)
            canonical_label = ontology_term.canonical_label
            exact_synonyms = " | ".join(sorted(ontology_term.exact_synonyms))
            obsolete = int(ontology_term.obsolete)
        rows.append(
            {
                "term_type": term_type,
                "curie": curie,
                "observed_label": observed,
                "current_exact": "" if current_exact is None else current_exact,
                "semantic_exact": int(semantic_match),
                "match_source": match_source,
                "canonical_label": canonical_label,
                "exact_synonyms": exact_synonyms,
                "obsolete": obsolete,
            }
        )

    columns = list(rows[0]) if rows else []
    with audit_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "schema_version": SCHEMA_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "database": str(database),
        "database_sha256": sha256_file(database),
        "ontology_source": str(ontology),
        "ontology_source_url": source_url,
        "ontology_sha256": sha256_file(ontology),
        "ontology": ontology_metadata.get("ontology", ""),
        "ontology_data_version": ontology_metadata.get("data_version", ""),
        "observed_mappings": len(rows),
        "semantic_exact_mappings": sum(int(row["semantic_exact"]) for row in rows),
        "missing_curies": sorted(missing_curies),
    }
    (output_dir / "cell_ontology_label_audit.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--ontology", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--source-url", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata = build_audit(
        args.database,
        args.ontology,
        args.out_dir,
        source_url=args.source_url,
    )
    print(
        f"observed_mappings={metadata['observed_mappings']}, "
        f"semantic_exact_mappings={metadata['semantic_exact_mappings']}, "
        f"missing_curies={len(metadata['missing_curies'])}"
    )


if __name__ == "__main__":
    main()
