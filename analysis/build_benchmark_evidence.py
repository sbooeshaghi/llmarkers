#!/usr/bin/env python3
"""Build lossless, source-specific benchmark evidence documents."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import tempfile
from collections import Counter, OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


MANIFEST_SCHEMA = "llmarkers.benchmark-evidence-sources.v1"
CLAIMS_SCHEMA = "llmarkers.curated-claims.v1"
PROFILES_SCHEMA = "llmarkers.deg-profiles.v1"
REPORT_SCHEMA = "llmarkers.benchmark-evidence-reconciliation.v1"

HUMAN_FIELDS = {
    "organism",
    "group_label",
    "group_name",
    "group_id",
    "feature_label",
    "feature_name",
    "feature_id",
    "source_type",
    "source_rationale",
    "source_id",
    "data_id",
}
DEG_FIELDS = HUMAN_FIELDS | {"metrics_pcorr", "metrics_logfc", "metrics_rank"}
SOURCE_KINDS = {"human", "deg"}
HUMAN_EVIDENCE_TYPES = {"text", "image"}

ORGANISMS = {
    "homo_sapiens": ("Homo sapiens", "NCBITaxon:9606"),
    "mus musculus": ("Mus musculus", "NCBITaxon:10090"),
    "mus_musculus": ("Mus musculus", "NCBITaxon:10090"),
}


@dataclass(frozen=True)
class Source:
    """One immutable legacy source listed in the benchmark manifest."""

    paper_id: str
    record_set: str
    role: str
    kind: str
    manuscript: Path
    path: Path
    manuscript_label: str
    path_label: str


def canonical_json(value: Any) -> str:
    """Serialize a value deterministically for content-derived identifiers."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(value: bytes) -> str:
    """Return the digest format shared with mrkr artifacts."""

    return "sha256:" + hashlib.sha256(value).hexdigest()


def stable_id(prefix: str, *values: Any) -> str:
    payload = canonical_json(values).encode("utf-8")
    return f"{prefix}:" + hashlib.sha256(payload).hexdigest()[:20]


def clean(value: Any) -> str | None:
    """Return a readable label without changing the preserved legacy value."""

    if value is None:
        return None
    result = str(value).strip()
    return result or None


def atomic_write_text(path: Path, text: str) -> None:
    """Publish a complete file or leave the previous file untouched."""

    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def load_manifest(path: Path) -> list[Source]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != f"# schema: {MANIFEST_SCHEMA}":
        raise ValueError(f"{path}: expected {MANIFEST_SCHEMA}")

    sources: list[Source] = []
    for line_number, line in enumerate(lines, 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 6:
            raise ValueError(f"{path}:{line_number}: expected six tab-separated fields")
        paper_id, record_set, role, kind, manuscript_label, path_label = fields
        if kind not in SOURCE_KINDS:
            raise ValueError(f"{path}:{line_number}: unsupported source kind {kind!r}")
        manuscript = (path.parent / manuscript_label).resolve()
        source_path = (path.parent / path_label).resolve()
        if not manuscript.is_file():
            raise FileNotFoundError(manuscript)
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        sources.append(
            Source(
                paper_id=paper_id,
                record_set=record_set,
                role=role,
                kind=kind,
                manuscript=manuscript,
                path=source_path,
                manuscript_label=portable_label(manuscript, path),
                path_label=portable_label(source_path, path),
            )
        )

    keys = [(item.paper_id, item.record_set, item.kind) for item in sources]
    if len(keys) != len(set(keys)):
        raise ValueError(f"{path}: duplicate paper/record-set/source-kind entry")
    return sources


def portable_label(path: Path, manifest: Path) -> str:
    """Prefer a repository-relative path in generated documents."""

    repository = manifest.parent.parent.resolve()
    try:
        return path.relative_to(repository).as_posix()
    except ValueError:
        return path.as_posix()


def validate_records(source: Source, records: Any) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        raise ValueError(f"{source.path}: expected a JSON array")
    expected = HUMAN_FIELDS if source.kind == "human" else DEG_FIELDS
    allowed_types = HUMAN_EVIDENCE_TYPES if source.kind == "human" else {"deg"}
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"{source.path}[{index}]: expected an object")
        missing = expected - set(record)
        extra = set(record) - expected
        if missing or extra:
            raise ValueError(
                f"{source.path}[{index}] fields differ: "
                f"missing={sorted(missing)}, extra={sorted(extra)}"
            )
        if record["source_type"] not in allowed_types:
            raise ValueError(
                f"{source.path}[{index}]: source_type={record['source_type']!r}, "
                f"expected one of {sorted(allowed_types)}"
            )
    return records


def source_record_id(source_sha256: str, index: int, record: dict[str, Any]) -> str:
    return stable_id("record", source_sha256, index, record)


def organism_term(record: dict[str, Any]) -> dict[str, Any]:
    source_label = record["organism"]
    normalized, ontology = ORGANISMS.get(
        str(source_label), (clean(source_label), None)
    )
    return {
        "term_type": "organism",
        "source_label": source_label,
        "normalized_label": normalized,
        "ontology_term": ontology,
        "provenance": "human_curated",
    }


def target_term(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "term_type": "celltype",
        "source_label": record["group_label"],
        "normalized_label": clean(record["group_name"])
        or clean(record["group_label"]),
        "legacy_normalized_label": record["group_name"],
        "ontology_term": record["group_id"],
        "provenance": "human_curated",
    }


def subspan(literal: str, value: Any) -> tuple[str | None, list[int] | None]:
    label = clean(value)
    if not label:
        return None, None
    start = literal.find(label)
    if start < 0:
        return None, None
    return literal[start : start + len(label)], [start, start + len(label)]


def marker_term(
    record: dict[str, Any],
    *,
    source_records: list[dict[str, Any]],
    evidence_type: str,
) -> dict[str, Any]:
    literal = record["source_rationale"] if evidence_type == "text" else ""
    term_span, term_offset = subspan(literal, record["feature_label"])
    term: dict[str, Any] = {
        "term_type": "gene",
        "source_label": record["feature_label"],
        "normalized_label": clean(record["feature_name"])
        or clean(record["feature_label"]),
        "legacy_normalized_label": record["feature_name"],
        "ontology_term": record["feature_id"],
        "provenance": "human_curated" if evidence_type != "deg" else "deg_table",
        "direction": (
            "positive"
            if evidence_type != "deg" or record["metrics_logfc"] > 0
            else "negative"
        ),
        "direction_basis": (
            "curated_marker_association"
            if evidence_type != "deg"
            else "metrics_logfc"
        ),
        "sub_span": term_span,
        "sub_offset": term_offset,
        "source_records": source_records,
    }
    if evidence_type == "deg":
        term["metrics"] = {
            "pcorr": record["metrics_pcorr"],
            "logfc": record["metrics_logfc"],
            "rank": record["metrics_rank"],
        }
    return term


def marker_terms(
    group: list[tuple[int, dict[str, Any]]],
    *,
    source_sha256: str,
    evidence_type: str,
) -> list[dict[str, Any]]:
    """Emit one semantic gene term while retaining duplicate source rows."""

    grouped: OrderedDict[str, list[tuple[int, dict[str, Any]]]] = OrderedDict()
    for index, record in group:
        grouped.setdefault(canonical_json(record), []).append((index, record))
    return [
        marker_term(
            rows[0][1],
            source_records=[
                {
                    "id": source_record_id(source_sha256, index, record),
                    "index": index,
                }
                for index, record in rows
            ],
            evidence_type=evidence_type,
        )
        for rows in grouped.values()
    ]


def group_key(record: dict[str, Any]) -> tuple[Any, ...]:
    """Group markers only when all non-feature legacy fields agree."""

    return (
        record["organism"],
        record["group_label"],
        record["group_name"],
        record["group_id"],
        record["source_rationale"],
        record["source_id"],
        record["data_id"],
    )


def group_records(
    records: Iterable[tuple[int, dict[str, Any]]],
) -> list[list[tuple[int, dict[str, Any]]]]:
    groups: OrderedDict[tuple[Any, ...], list[tuple[int, dict[str, Any]]]] = (
        OrderedDict()
    )
    for index, record in records:
        groups.setdefault(group_key(record), []).append((index, record))
    return list(groups.values())


def all_offsets(container: str, value: str) -> list[list[int]]:
    offsets: list[list[int]] = []
    start = 0
    while value:
        index = container.find(value, start)
        if index < 0:
            break
        offsets.append([index, index + len(value)])
        start = index + 1
    return offsets


def text_evidence(record: dict[str, Any], manuscript: str) -> dict[str, Any]:
    literal = record["source_rationale"]
    offsets = all_offsets(manuscript, literal)
    if len(offsets) == 1:
        status = "exact"
        offset = offsets[0]
    elif offsets:
        status = "ambiguous"
        offset = None
    else:
        status = "unanchored"
        offset = None
    evidence: dict[str, Any] = {
        "type": "text",
        "source_id": record["source_id"],
        "data_id": record["data_id"],
        "span_literal": literal,
        "span_offset": offset,
        "anchor_status": status,
    }
    if len(offsets) > 1:
        evidence["candidate_offsets"] = offsets
    return evidence


def nontext_evidence(record: dict[str, Any], evidence_type: str) -> dict[str, Any]:
    evidence = {
        "type": evidence_type,
        "source_id": record["source_id"],
        "data_id": record["data_id"],
        "description": record["source_rationale"],
    }
    if evidence_type == "deg":
        evidence["selection"] = "unfiltered"
    return evidence


def readable_summary(record: dict[str, Any], terms: list[dict[str, Any]]) -> str:
    organism = organism_term(record)["normalized_label"] or record["organism"]
    target = target_term(record)["normalized_label"] or record["group_label"]
    genes = list(
        dict.fromkeys(
            term["normalized_label"]
            for term in terms
            if term["term_type"] == "gene" and term["normalized_label"]
        )
    )
    return f"In {organism}, {target} is marked by {', '.join(genes)}."


def source_metadata(
    source: Source,
    source_sha256: str,
    manuscript_sha256: str,
) -> dict[str, Any]:
    return {
        "id": f"benchmark/{source.paper_id}/{source.record_set}",
        "paper_id": source.paper_id,
        "record_set": source.record_set,
        "role": source.role,
        "path": source.path_label,
        "sha256": source_sha256,
        "manuscript": {
            "path": source.manuscript_label,
            "sha256": manuscript_sha256,
        },
    }


def build_claim_document(
    source: Source,
    records: list[dict[str, Any]],
    evidence_type: str,
    source_sha256: str,
    manuscript: str,
    manuscript_sha256: str,
) -> dict[str, Any]:
    claims: list[dict[str, Any]] = []
    indexed = (
        (index, record)
        for index, record in enumerate(records)
        if record["source_type"] == evidence_type
    )
    for group in group_records(indexed):
        first = group[0][1]
        genes = marker_terms(
            group, source_sha256=source_sha256, evidence_type=evidence_type
        )
        terms = [organism_term(first), target_term(first), *genes]
        evidence = (
            text_evidence(first, manuscript)
            if evidence_type == "text"
            else nontext_evidence(first, evidence_type)
        )
        claims.append(
            {
                "claim_id": stable_id(
                    "claim",
                    source.paper_id,
                    source.record_set,
                    evidence_type,
                    group_key(first),
                ),
                "summary": readable_summary(first, terms),
                "evidence": evidence,
                "terms": terms,
                "source_record_ids": [
                    record["id"] for term in genes for record in term["source_records"]
                ],
            }
        )
    return {
        "schema_version": CLAIMS_SCHEMA,
        "source": source_metadata(
            source, source_sha256=source_sha256, manuscript_sha256=manuscript_sha256
        ),
        "producer": {"name": "build_benchmark_evidence.py", "version": "1"},
        "evidence_type": evidence_type,
        "claims": claims,
    }


def build_profile_document(
    source: Source,
    records: list[dict[str, Any]],
    source_sha256: str,
    manuscript_sha256: str,
) -> dict[str, Any]:
    profiles: list[dict[str, Any]] = []
    for group in group_records(enumerate(records)):
        first = group[0][1]
        genes = marker_terms(group, source_sha256=source_sha256, evidence_type="deg")
        profiles.append(
            {
                "profile_id": stable_id(
                    "profile", source.paper_id, source.record_set, group_key(first)
                ),
                "evidence": nontext_evidence(first, "deg"),
                "terms": [organism_term(first), target_term(first), *genes],
                "source_record_ids": [
                    record["id"] for term in genes for record in term["source_records"]
                ],
            }
        )
    return {
        "schema_version": PROFILES_SCHEMA,
        "source": source_metadata(
            source, source_sha256=source_sha256, manuscript_sha256=manuscript_sha256
        ),
        "producer": {"name": "build_benchmark_evidence.py", "version": "1"},
        "evidence_type": "deg",
        "profiles": profiles,
    }


def flatten_document(document: dict[str, Any]) -> list[tuple[int, dict[str, Any]]]:
    """Reconstruct legacy records exactly for migration reconciliation."""

    evidence_type = document["evidence_type"]
    container = "profiles" if evidence_type == "deg" else "claims"
    result: list[tuple[int, dict[str, Any]]] = []
    for item in document[container]:
        evidence = item["evidence"]
        organism = next(term for term in item["terms"] if term["term_type"] == "organism")
        target = next(term for term in item["terms"] if term["term_type"] == "celltype")
        for gene in (term for term in item["terms"] if term["term_type"] == "gene"):
            record = {
                "organism": organism["source_label"],
                "group_label": target["source_label"],
                "group_name": target["legacy_normalized_label"],
                "group_id": target["ontology_term"],
                "feature_label": gene["source_label"],
                "feature_name": gene["legacy_normalized_label"],
                "feature_id": gene["ontology_term"],
                "source_type": evidence_type,
                "source_rationale": (
                    evidence["span_literal"]
                    if evidence_type == "text"
                    else evidence["description"]
                ),
                "source_id": evidence["source_id"],
                "data_id": evidence["data_id"],
            }
            if evidence_type == "deg":
                record.update(
                    {
                        "metrics_pcorr": gene["metrics"]["pcorr"],
                        "metrics_logfc": gene["metrics"]["logfc"],
                        "metrics_rank": gene["metrics"]["rank"],
                    }
                )
            result.extend((source["index"], record.copy()) for source in gene["source_records"])
    return sorted(result)


def document_statistics(document: dict[str, Any]) -> dict[str, Any]:
    evidence_type = document["evidence_type"]
    container = "profiles" if evidence_type == "deg" else "claims"
    items = document[container]
    terms = [term for item in items for term in item["terms"]]
    exact = sum(
        item["evidence"].get("anchor_status") == "exact" for item in items
    )
    ambiguous = sum(
        item["evidence"].get("anchor_status") == "ambiguous" for item in items
    )
    unanchored = sum(
        item["evidence"].get("anchor_status") == "unanchored" for item in items
    )
    unanchored_genes = sum(
        term["term_type"] == "gene" and term["sub_offset"] is None
        for item in items
        for term in item["terms"]
    )
    return {
        "evidence_type": evidence_type,
        "objects": len(items),
        "records": sum(
            len(term["source_records"])
            for term in terms
            if term["term_type"] == "gene"
        ),
        "marker_terms": sum(term["term_type"] == "gene" for term in terms),
        "exact_text_objects": exact,
        "ambiguous_text_objects": ambiguous,
        "unanchored_text_objects": unanchored,
        "unanchored_text_genes": unanchored_genes if evidence_type == "text" else 0,
    }


def serialize_document(document: dict[str, Any]) -> str:
    return canonical_json(document) + "\n"


def review_document(document: dict[str, Any]) -> list[dict[str, Any]]:
    """Return curator-review warnings without changing any annotation."""

    if document["evidence_type"] != "text":
        return []
    warnings: list[dict[str, Any]] = []
    source = document["source"]
    for claim in document["claims"]:
        target = next(
            term for term in claim["terms"] if term["term_type"] == "celltype"
        )
        evidence = claim["evidence"]
        if evidence["anchor_status"] != "exact":
            warnings.append(
                {
                    "code": "text.anchor_unresolved",
                    "paper_id": source["paper_id"],
                    "record_set": source["record_set"],
                    "evidence_type": "text",
                    "object_id": claim["claim_id"],
                    "source_record_id": "",
                    "source_record_index": "",
                    "target": target["normalized_label"],
                    "gene": "",
                    "source_id": evidence["source_id"],
                    "detail": evidence["anchor_status"],
                }
            )
        for gene in (
            term for term in claim["terms"] if term["term_type"] == "gene"
        ):
            if gene["sub_offset"] is not None:
                continue
            warnings.append(
                {
                    "code": "text.gene_unanchored",
                    "paper_id": source["paper_id"],
                    "record_set": source["record_set"],
                    "evidence_type": "text",
                    "object_id": claim["claim_id"],
                    "source_record_id": gene["source_records"][0]["id"],
                    "source_record_index": gene["source_records"][0]["index"],
                    "target": target["normalized_label"],
                    "gene": gene["normalized_label"],
                    "source_id": evidence["source_id"],
                    "detail": "feature_label is absent from the curated text span",
                }
            )
    return warnings


def build(manifest: Path, output_dir: Path) -> dict[str, Any]:
    sources = load_manifest(manifest)
    report_sources: list[dict[str, Any]] = []
    report_documents: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []

    for source in sources:
        source_bytes = source.path.read_bytes()
        source_sha256 = sha256_bytes(source_bytes)
        manuscript_bytes = source.manuscript.read_bytes()
        manuscript = manuscript_bytes.decode("utf-8")
        manuscript_sha256 = sha256_bytes(manuscript_bytes)
        records = validate_records(source, json.loads(source_bytes))

        documents = (
            [
                build_claim_document(
                    source,
                    records,
                    evidence_type,
                    source_sha256,
                    manuscript,
                    manuscript_sha256,
                )
                for evidence_type in ("text", "image")
            ]
            if source.kind == "human"
            else [
                build_profile_document(
                    source, records, source_sha256, manuscript_sha256
                )
            ]
        )

        recovered: list[tuple[int, dict[str, Any]]] = []
        for document in documents:
            evidence_type = document["evidence_type"]
            suffix = "claims" if evidence_type != "deg" else "profiles"
            relative_output = (
                Path("papers")
                / source.paper_id
                / source.record_set
                / f"{evidence_type}.{suffix}.json"
            )
            output = output_dir / relative_output
            serialized = serialize_document(document)
            atomic_write_text(output, serialized)
            recovered.extend(flatten_document(document))
            stats = document_statistics(document)
            review_rows.extend(review_document(document))
            report_documents.append(
                {
                    "paper_id": source.paper_id,
                    "record_set": source.record_set,
                    "role": source.role,
                    "path": relative_output.as_posix(),
                    "schema_version": document["schema_version"],
                    "sha256": sha256_bytes(serialized.encode("utf-8")),
                    **stats,
                }
            )

        recovered_records = [record for _, record in sorted(recovered)]
        if recovered_records != records:
            raise ValueError(f"{source.path}: derived documents fail exact round-trip")
        if sha256_bytes(source.path.read_bytes()) != source_sha256:
            raise RuntimeError(f"{source.path}: source changed during the build")
        record_ids = [
            source_record_id(source_sha256, index, record)
            for index, record in enumerate(records)
        ]
        if len(record_ids) != len(set(record_ids)):
            raise ValueError(f"{source.path}: source record identifiers are not unique")
        exact_duplicates = len(records) - len({canonical_json(record) for record in records})
        organism_counts = dict(
            sorted(Counter(str(record["organism"]) for record in records).items())
        )
        if exact_duplicates:
            review_rows.append(
                {
                    "code": "source.duplicate_records",
                    "paper_id": source.paper_id,
                    "record_set": source.record_set,
                    "evidence_type": source.kind,
                    "object_id": "",
                    "source_record_id": "",
                    "source_record_index": "",
                    "target": "",
                    "gene": "",
                    "source_id": source.path_label,
                    "detail": f"{exact_duplicates} exact duplicate rows preserved",
                }
            )
        if len(organism_counts) > 1:
            review_rows.append(
                {
                    "code": "source.multiple_organisms",
                    "paper_id": source.paper_id,
                    "record_set": source.record_set,
                    "evidence_type": source.kind,
                    "object_id": "",
                    "source_record_id": "",
                    "source_record_index": "",
                    "target": "",
                    "gene": "",
                    "source_id": source.path_label,
                    "detail": canonical_json(organism_counts),
                }
            )
        report_sources.append(
            {
                "paper_id": source.paper_id,
                "record_set": source.record_set,
                "role": source.role,
                "kind": source.kind,
                "path": source.path_label,
                "sha256": source_sha256,
                "records": len(records),
                "organisms": organism_counts,
                "exact_duplicate_records": exact_duplicates,
                "roundtrip_equal": True,
                "source_unchanged": True,
            }
        )

    report = {
        "schema_version": REPORT_SCHEMA,
        "status": "ok",
        "manifest": portable_label(manifest, manifest),
        "checks": {
            "all_sources_unchanged": True,
            "all_records_roundtrip_exactly": True,
            "every_source_record_represented_once": True,
        },
        "sources": report_sources,
        "documents": report_documents,
        "totals": {
            "source_records": sum(item["records"] for item in report_sources),
            "derived_records": sum(item["records"] for item in report_documents),
            "documents": len(report_documents),
            "review_warnings": len(review_rows),
        },
    }
    atomic_write_text(
        output_dir / "reconciliation.json",
        json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
    )
    write_summary(output_dir / "summary.tsv", report_documents)
    write_review(output_dir / "review.tsv", review_rows)
    return report


def write_summary(path: Path, documents: list[dict[str, Any]]) -> None:
    rows = [
        [
            item["paper_id"],
            item["record_set"],
            item["role"],
            item["evidence_type"],
            item["objects"],
            item["marker_terms"],
            item["records"],
            item["exact_text_objects"],
            item["ambiguous_text_objects"],
            item["unanchored_text_objects"],
            item["unanchored_text_genes"],
        ]
        for item in documents
    ]
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temporary = Path(handle.name)
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(
            [
                "paper_id",
                "record_set",
                "role",
                "evidence_type",
                "objects",
                "marker_terms",
                "records",
                "exact_text_objects",
                "ambiguous_text_objects",
                "unanchored_text_objects",
                "unanchored_text_genes",
            ]
        )
        writer.writerows(rows)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def write_review(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "code",
        "paper_id",
        "record_set",
        "evidence_type",
        "object_id",
        "source_record_id",
        "source_record_index",
        "target",
        "gene",
        "source_id",
        "detail",
    ]
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        temporary = Path(handle.name)
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = build(args.manifest.resolve(), args.output_dir.resolve())
    totals = report["totals"]
    print(
        f"reconciled {totals['source_records']} records into "
        f"{totals['documents']} documents"
    )


if __name__ == "__main__":
    main()
