#!/usr/bin/env python3
"""Jointly extract marker claims and select their paper-specific DEG source."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any

from evaluate_mrkr_deg_linkage import (
    ANTHROPIC_URL,
    ANTHROPIC_VERSION,
    CLAIMS_SCHEMA,
    DEFAULT_MODEL,
    MarkerTerm,
    benchmark_paths,
    deg_catalog,
    human_terms,
    normalize_label,
    prf,
    response_json,
    sha256_file,
    source_gene_prf,
)


SCHEMA = "mrkr.joint-deg-extraction.v1"
RAW_SCHEMA = "mrkr.joint-deg-extraction.raw.v1"


def load_env_file(path: Path | None) -> None:
    if path is None or not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def load_json(path: Path, schema: str | None = None) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if schema is not None and document.get("schema_version") != schema:
        raise ValueError(f"{path}: expected schema {schema}")
    return document


def manuscript_path(benchmark_document: dict[str, Any], repo_root: Path) -> Path:
    value = Path(benchmark_document["source"]["manuscript"]["path"])
    return value if value.is_absolute() else repo_root / value


def build_prompt(
    paper_id: str,
    catalog: dict[str, list[str]],
    manuscript_text: str,
) -> str:
    """Build the legacy joint task with explicit, current validation rules."""

    known_cell_types = "\n\n".join(
        "\n".join([f"## {data_id}", *(f"  - {label}" for label in labels)])
        for data_id, labels in catalog.items()
    )
    return f"""You are an expert at extracting cell type marker genes from scientific manuscripts.

# Task
Extract ALL human cell type marker gene associations from the manuscript text below. For each
association, jointly identify the candidate differential-expression data source that supports it.

# Known Cell Types from DEG Tables
Each section header is an exact data_id. The items below it are the normalized cell-type labels
found in that source.

{known_cell_types}

# Extraction Guidelines

For each human cell type and marker gene pair:
- Set organism to homo_sapiens.
- Copy the EXACT text used for the cell type as group_label.
- Copy the EXACT gene symbol as feature_label.
- Copy one or more complete, contiguous manuscript sentences that mention BOTH as
  source_rationale.
- Match group_name to the MOST SPECIFIC applicable label above. Preserve the complete subtype
  and number. Use biological and manuscript context to match naming variants. If no candidate
  matches, normalize group_label to uppercase.
- Normalize feature_name to uppercase.
- Set data_id to the exact source above that contains group_name. When several sources contain it,
  use the manuscript's figure, table, subset, or analysis context and prefer the most specific
  source. Return null when the manuscript does not support one source.

# Exact Source Rules

- source_rationale must be copied VERBATIM. Do not paraphrase, truncate, or use ellipses.
- source_rationale, group_label, and feature_label must be exact manuscript substrings.
- source_rationale must contain both group_label and feature_label.
- Do not infer marker genes that are absent from source_rationale.
- Do not invent or alter data_id values.
- Do not extract associations that apply only to another organism.

# Output
Return ONLY one valid JSON object with this exact shape:

{{
  "extractions": [
    {{
      "organism": "homo_sapiens",
      "group_label": "naive CD4+ T cells",
      "group_name": "NAIVE CD4+ T CELL",
      "feature_label": "IL7R",
      "feature_name": "IL7R",
      "source_rationale": "Naive CD4+ T cells expressed IL7R.",
      "data_id": "exact candidate ID or null"
    }}
  ]
}}

# Paper
{paper_id}

# Manuscript text
{manuscript_text}

# JSON output
"""


def call_anthropic(prompt: str, model: str, timeout: float) -> dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is required with --run-llm")
    body = json.dumps(
        {
            "model": model,
            "max_tokens": 32_000,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        ANTHROPIC_URL,
        data=body,
        headers={
            "anthropic-version": ANTHROPIC_VERSION,
            "content-type": "application/json",
            "x-api-key": api_key,
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Anthropic HTTP {error.code}: {detail}") from error
    blocks = payload.get("content") or []
    text = "".join(block.get("text", "") for block in blocks if block.get("type") == "text")
    if not text:
        raise ValueError("Anthropic response contained no text block")
    return {
        "response_id": payload.get("id"),
        "model": payload.get("model") or model,
        "stop_reason": payload.get("stop_reason"),
        "usage": payload.get("usage") or {},
        "text": text,
    }


def parsed_response(raw_response: dict[str, Any]) -> dict[str, Any]:
    return {"extractions": response_json(raw_response["text"]).get("extractions")}


def load_mrkr_helpers(mrkr_cwd: Path):
    root = str(mrkr_cwd.resolve())
    if root not in sys.path:
        sys.path.insert(0, root)
    claims = importlib.import_module("mrkr.claims")
    gene_map = importlib.import_module("mrkr.map")
    return claims, gene_map


def target_term(raw_claim: dict[str, Any]) -> dict[str, Any]:
    targets = [term for term in raw_claim.get("terms", []) if term.get("term_type") == "celltype"]
    if len(targets) != 1:
        raise ValueError("joint claim must contain exactly one celltype term")
    return targets[0]


EXTRACTION_FIELDS = {
    "organism",
    "group_label",
    "group_name",
    "feature_label",
    "feature_name",
    "source_rationale",
}


def validate_raw_response(
    response: dict[str, Any], candidate_ids: set[str]
) -> list[dict[str, Any]]:
    raw_extractions = response.get("extractions")
    if not isinstance(raw_extractions, list):
        raise ValueError("response extractions must be a list")
    validated: list[dict[str, Any]] = []
    for index, extraction in enumerate(raw_extractions):
        if not isinstance(extraction, dict):
            raise ValueError(f"extraction {index}: expected an object")
        for field in EXTRACTION_FIELDS:
            if not isinstance(extraction.get(field), str) or not extraction[field].strip():
                raise ValueError(f"extraction {index}: {field} must be a non-empty string")
        if extraction["organism"].casefold() not in {
            "homo_sapiens",
            "homo sapiens",
            "human",
        }:
            raise ValueError(f"extraction {index}: expected a human marker association")
        data_id = extraction.get("data_id")
        if data_id is not None and data_id not in candidate_ids:
            raise ValueError(f"extraction {index}: unknown data_id: {data_id}")
        validated.append(extraction)
    return validated


def exact_label_source(
    group_name: str, catalog: dict[str, list[str]]
) -> str | None:
    """Reproduce the legacy exact-label fallback with a deterministic tie break."""

    label = normalize_label(group_name)
    matches = [
        data_id
        for data_id, labels in catalog.items()
        if label in {normalize_label(item) for item in labels}
    ]
    return min(matches, key=lambda item: (len(catalog[item]), item)) if matches else None


def extraction_claim(
    extraction: dict[str, Any], catalog: dict[str, list[str]]
) -> tuple[dict[str, Any], str | None, str]:
    """Adapt one legacy extraction row to the current mrkr claim shape."""

    span = extraction["source_rationale"].strip()
    group_label = extraction["group_label"].strip()
    gene_label = extraction["feature_label"].strip()
    data_id = extraction.get("data_id")
    origin = "model"
    if data_id is None:
        data_id = exact_label_source(extraction["group_name"], catalog)
        origin = "exact_label_fallback" if data_id is not None else "unresolved"
    target = extraction["group_name"].strip()
    gene = extraction["feature_name"].strip()
    raw_claim = {
        "span_literal": span,
        "summary": f"In Homo sapiens, {target} is marked by {gene}.",
        "data_id": data_id,
        "_data_id_origin": origin,
        "terms": [
            {
                "sub_span": group_label if group_label in span else None,
                "normalized_label": target,
                "term_type": "celltype",
            },
            {
                "sub_span": None,
                "normalized_label": "Homo sapiens",
                "term_type": "organism",
            },
            {
                "sub_span": gene_label if gene_label in span else None,
                "normalized_label": gene,
                "term_type": "gene",
                "direction": "positive",
            },
        ],
    }
    return raw_claim, data_id, origin


def prepare_document(
    response: dict[str, Any],
    *,
    manuscript_text: str,
    source_id: str,
    catalog: dict[str, list[str]],
    mrkr_cwd: Path,
) -> tuple[
    dict[str, Any],
    dict[str, str | None],
    dict[str, str],
    dict[str, Any],
]:
    """Run current mrkr source alignment while retaining the jointly selected ID."""

    claims_module, _ = load_mrkr_helpers(mrkr_cwd)
    extractions = validate_raw_response(response, set(catalog))
    adapted = [extraction_claim(extraction, catalog) for extraction in extractions]
    raw_claims = [item[0] for item in adapted]
    prepared, preparation_report = claims_module.prepare_raw_claims(
        manuscript_text, raw_claims
    )
    strictly_grounded: list[dict[str, Any]] = []
    strict_exclusions: list[dict[str, Any]] = []
    for claim in prepared:
        span = claim.get("span_literal") or ""
        target = target_term(claim)
        if span not in manuscript_text:
            strict_exclusions.append(
                {"reason": "span_not_exact", "span_literal": span}
            )
            continue
        if manuscript_text.count(span) > 1 and not target.get("sub_span"):
            strict_exclusions.append(
                {"reason": "ambiguous_implicit_target", "span_literal": span}
            )
            continue
        strictly_grounded.append(claim)
    prepared = strictly_grounded
    preparation_report["strict_exclusions"] = strict_exclusions
    preparation_report["strictly_grounded_claims"] = len(prepared)
    selected_by_key: dict[tuple[str, str], set[str | None]] = defaultdict(set)
    origin_by_key: dict[tuple[str, str], set[str]] = defaultdict(set)
    for claim in prepared:
        target = target_term(claim)
        key = (claim.get("span_literal") or "", normalize_label(target.get("normalized_label")))
        selected_by_key[key].add(claim.pop("data_id", None))
        origin_by_key[key].add(claim.pop("_data_id_origin"))
    conflicts = {key: values for key, values in selected_by_key.items() if len(values) != 1}
    if conflicts:
        raise ValueError(f"conflicting data_id values after claim preparation: {conflicts}")

    document = claims_module.make_claim_document(
        source_id=source_id,
        manuscript_text=manuscript_text,
        raw_claims=prepared,
    )
    report = claims_module.validate_document(document, manuscript_text)
    if report["errors"]:
        raise ValueError(f"current mrkr validation failed: {report['errors']}")

    links: dict[str, str | None] = {}
    link_origins: dict[str, str] = {}
    for claim in document["claims"]:
        target = next(term for term in claim["terms"] if term["term_type"] == "celltype")
        key = (claim["span_literal"], normalize_label(target["normalized_label"]))
        values = selected_by_key.get(key)
        if values is None or len(values) != 1:
            raise ValueError(f"{claim['claim_id']}: no unique jointly selected data_id")
        links[claim["claim_id"]] = next(iter(values))
        origins = origin_by_key.get(key)
        if origins is None:
            raise ValueError(f"{claim['claim_id']}: no data_id origin")
        link_origins[claim["claim_id"]] = (
            next(iter(origins)) if len(origins) == 1 else "mixed"
        )
    return (
        document,
        links,
        link_origins,
        {"preparation": preparation_report, "validation": report},
    )


def resolve_gene(term: dict[str, Any], resolver, gene_map: dict[str, str | None]) -> str | None:
    normalized = resolver(term.get("normalized_label") or "", gene_map)
    source = resolver(term.get("sub_span") or "", gene_map)
    if normalized and source and normalized != source:
        raise ValueError(
            f"gene grounding conflict: {term.get('normalized_label')!r} vs {term.get('sub_span')!r}"
        )
    return normalized or source


def predicted_terms(
    document: dict[str, Any],
    links: dict[str, str | None],
    *,
    mrkr_cwd: Path,
    gene_map_path: Path,
) -> list[MarkerTerm]:
    _, map_module = load_mrkr_helpers(mrkr_cwd)
    gene_map = map_module.load_gene_map(gene_map_file=gene_map_path)
    result: list[MarkerTerm] = []
    for claim in document["claims"]:
        target = next(term for term in claim["terms"] if term["term_type"] == "celltype")
        label = normalize_label(target.get("normalized_label"))
        offset = tuple(claim["span_offset"]) if claim.get("span_offset") else None
        for gene in claim["terms"]:
            if gene.get("term_type") != "gene" or gene.get("direction") != "positive":
                continue
            gene_id = resolve_gene(gene, map_module.resolve_gene_id, gene_map)
            if not gene_id:
                continue
            result.append(
                MarkerTerm(
                    claim_id=claim["claim_id"],
                    target_label=label,
                    gene_id=gene_id,
                    data_id=links[claim["claim_id"]],
                    offset=offset,
                )
            )
    return result


def evaluate(predicted: list[MarkerTerm], truth: list[MarkerTerm]) -> dict[str, Any]:
    predicted_pairs = {(item.target_label, item.gene_id) for item in predicted}
    truth_pairs = {(item.target_label, item.gene_id) for item in truth}
    predicted_triples = {
        (item.data_id, item.target_label, item.gene_id)
        for item in predicted
        if item.data_id is not None
    }
    truth_triples = {
        (item.data_id, item.target_label, item.gene_id)
        for item in truth
        if item.data_id is not None
    }
    pair = prf(predicted_pairs, truth_pairs)
    triple = prf(predicted_triples, truth_triples)
    source = source_gene_prf(predicted, truth)
    return {
        "predicted_terms": len(predicted),
        "predicted_pairs": len(predicted_pairs),
        "predicted_triples": len(predicted_triples),
        "truth_terms": len(truth),
        "truth_pairs": len(truth_pairs),
        "truth_triples": len(truth_triples),
        "pair_precision": pair["precision"],
        "pair_recall": pair["recall"],
        "pair_f1": pair["f1"],
        "triple_precision": triple["precision"],
        "triple_recall": triple["recall"],
        "triple_f1": triple["f1"],
        "source_gene_precision": source["precision"],
        "source_gene_recall": source["recall"],
        "source_gene_f1": source["f1"],
    }


def review_rows(
    paper_id: str,
    predicted: list[MarkerTerm],
    truth: list[MarkerTerm],
    *,
    include_data_id: bool,
) -> list[dict[str, Any]]:
    """Return one inspectable row for every predicted or reference fact."""

    def fact(item: MarkerTerm) -> tuple[str, ...]:
        values = (item.target_label, item.gene_id)
        return ((item.data_id or ""), *values) if include_data_id else values

    predicted_facts = {fact(item) for item in predicted}
    truth_facts = {fact(item) for item in truth}
    rows: list[dict[str, Any]] = []
    for item in sorted(predicted_facts | truth_facts):
        is_predicted = item in predicted_facts
        is_truth = item in truth_facts
        data_id, target_label, gene_id = (
            item if include_data_id else ("", *item)
        )
        rows.append(
            {
                "paper_id": paper_id,
                "status": "true_positive"
                if is_predicted and is_truth
                else ("false_positive" if is_predicted else "false_negative"),
                "data_id": data_id,
                "target_label": target_label,
                "gene_id": gene_id,
                "predicted": is_predicted,
                "reference": is_truth,
            }
        )
    return rows


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_report(output: Path, summary: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    lines = [
        "# Joint marker extraction and DEG-source assignment",
        "",
        "One prompt received the full manuscript and its candidate `data_id` to cell-type-label "
        "catalog, then jointly extracted marker claims and selected one supporting DEG source.",
        "",
        f"- Papers: {summary['papers']}",
        f"- Model: `{summary['model']}`",
        f"- Raw associations: {summary['totals']['raw_extractions']}",
        f"- Retained claims: {summary['totals']['claims']}",
        f"- Mapped marker terms: {summary['totals']['predicted_terms']}",
        f"- Excluded unsupported or ambiguous associations: {summary['totals']['excluded_claims']}",
        f"- Mean exact cell type--gene F1: {summary['macro_mean']['pair_f1']:.3f}",
        f"- Mean exact data ID--cell type--gene F1: {summary['macro_mean']['triple_f1']:.3f}",
        "",
        "| Paper | Claims | Terms | Pair F1 | Triple F1 | Source+gene F1 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['paper_id']} | {row['claims']} | {row['predicted_terms']} | "
            f"{row['pair_f1']:.3f} | {row['triple_f1']:.3f} | "
            f"{row['source_gene_f1']:.3f} |"
        )
    (output / "joint_extraction_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark-root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--mrkr-cwd", type=Path, default=Path("../mrkr"))
    parser.add_argument("--gene-map", type=Path)
    parser.add_argument("--run-llm", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--limit", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    benchmark_root = args.benchmark_root.resolve()
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=True)
    paper_dir = output / "papers"
    paper_dir.mkdir(exist_ok=True)
    load_env_file(args.env_file)
    model = args.model or os.getenv("ANTHROPIC_MODEL") or DEFAULT_MODEL
    gene_map_path = (
        args.gene_map.resolve()
        if args.gene_map
        else (args.mrkr_cwd / "mrkr" / "data" / "gmap.txt").resolve()
    )
    if not gene_map_path.is_file():
        raise FileNotFoundError(gene_map_path)

    paper_ids = sorted(path.name for path in (benchmark_root / "papers").iterdir())
    if args.limit is not None:
        paper_ids = paper_ids[: args.limit]
    rows: list[dict[str, Any]] = []
    pair_review: list[dict[str, Any]] = []
    triple_review: list[dict[str, Any]] = []
    for paper_id in paper_ids:
        text_path, deg_path = benchmark_paths(benchmark_root, paper_id)
        truth_document = load_json(text_path, CLAIMS_SCHEMA)
        deg_document = load_json(deg_path, "llmarkers.deg-profiles.v1")
        source_path = manuscript_path(truth_document, repo_root)
        manuscript_text = source_path.read_text(encoding="utf-8")
        expected_source_hash = truth_document["source"]["manuscript"]["sha256"]
        if sha256_file(source_path) != expected_source_hash:
            raise ValueError(f"{source_path}: manuscript hash does not match benchmark")
        catalog = deg_catalog(deg_document)
        artifact_path = paper_dir / f"{paper_id}.json"
        raw_path = paper_dir / f"{paper_id}.raw.json"
        prompt = build_prompt(paper_id, catalog, manuscript_text)
        prompt_hash = "sha256:" + hashlib.sha256(prompt.encode("utf-8")).hexdigest()

        if args.run_llm and (args.force or not raw_path.exists()):
            started = time.time()
            raw_response = call_anthropic(prompt, model, args.timeout)
            raw_artifact = {
                "schema_version": RAW_SCHEMA,
                "paper_id": paper_id,
                "model": raw_response["model"],
                "response_id": raw_response["response_id"],
                "stop_reason": raw_response["stop_reason"],
                "usage": raw_response["usage"],
                "elapsed_seconds": time.time() - started,
                "prompt_sha256": prompt_hash,
                "text": raw_response["text"],
            }
            raw_path.write_text(
                json.dumps(raw_artifact, indent=2, ensure_ascii=True) + "\n",
                encoding="utf-8",
            )
        if (args.force or not artifact_path.exists()) and raw_path.exists():
            raw_artifact = load_json(raw_path, RAW_SCHEMA)
            if raw_artifact["prompt_sha256"] != prompt_hash:
                raise ValueError(f"{raw_path}: prompt changed; rerun with --force")
            response = parsed_response(raw_artifact)
            document, links, link_origins, validation = prepare_document(
                response,
                manuscript_text=manuscript_text,
                source_id=source_path.name,
                catalog=catalog,
                mrkr_cwd=args.mrkr_cwd,
            )
            artifact = {
                "schema_version": SCHEMA,
                "paper_id": paper_id,
                "model": raw_artifact["model"],
                "response_id": raw_artifact["response_id"],
                "stop_reason": raw_artifact["stop_reason"],
                "usage": raw_artifact["usage"],
                "elapsed_seconds": raw_artifact["elapsed_seconds"],
                "raw_extractions": response["extractions"],
                "inputs": {
                    "manuscript_path": str(source_path.relative_to(repo_root)),
                    "manuscript_sha256": sha256_file(source_path),
                    "benchmark_text_sha256": sha256_file(text_path),
                    "benchmark_deg_sha256": sha256_file(deg_path),
                    "gene_map_sha256": sha256_file(gene_map_path),
                    "prompt_sha256": prompt_hash,
                    "candidate_data_ids": sorted(catalog),
                },
                "claims_document": document,
                "links": links,
                "link_origins": link_origins,
                "validation": validation,
            }
            artifact_path.write_text(
                json.dumps(artifact, indent=2, ensure_ascii=True) + "\n",
                encoding="utf-8",
            )
        if not artifact_path.is_file():
            raise FileNotFoundError(
                f"{artifact_path}: run with --run-llm to create the joint extraction"
            )
        artifact = load_json(artifact_path, SCHEMA)
        if artifact["inputs"]["prompt_sha256"] != prompt_hash:
            raise ValueError(f"{artifact_path}: prompt changed; rerun with --force")
        if artifact["inputs"]["manuscript_sha256"] != sha256_file(source_path):
            raise ValueError(f"{artifact_path}: manuscript input changed")
        if artifact["inputs"]["benchmark_text_sha256"] != sha256_file(text_path):
            raise ValueError(f"{artifact_path}: benchmark text input changed")
        if artifact["inputs"]["benchmark_deg_sha256"] != sha256_file(deg_path):
            raise ValueError(f"{artifact_path}: benchmark DEG input changed")
        if artifact["inputs"]["gene_map_sha256"] != sha256_file(gene_map_path):
            raise ValueError(f"{artifact_path}: gene map changed")

        predicted = predicted_terms(
            artifact["claims_document"],
            artifact["links"],
            mrkr_cwd=args.mrkr_cwd,
            gene_map_path=gene_map_path,
        )
        truth = human_terms(truth_document)
        metrics = evaluate(predicted, truth)
        pair_review.extend(
            review_rows(paper_id, predicted, truth, include_data_id=False)
        )
        triple_review.extend(
            review_rows(paper_id, predicted, truth, include_data_id=True)
        )
        origins = list(artifact.get("link_origins", {}).values())
        preparation = artifact["validation"]["preparation"]
        rows.append(
            {
                "paper_id": paper_id,
                "raw_extractions": len(artifact["raw_extractions"]),
                "claims": len(artifact["claims_document"]["claims"]),
                "candidate_sources": len(catalog),
                "model_data_ids": origins.count("model"),
                "fallback_data_ids": origins.count("exact_label_fallback"),
                "unresolved_data_ids": origins.count("unresolved"),
                "mixed_data_ids": origins.count("mixed"),
                "validation_warnings": len(
                    artifact["validation"]["validation"]["warnings"]
                ),
                "preparation_excluded_claims": len(
                    preparation["excluded_claims"]
                ),
                "preparation_excluded_terms": len(preparation["excluded_terms"]),
                "strict_exclusions": len(preparation["strict_exclusions"]),
                **metrics,
            }
        )
        print(
            f"{paper_id}: claims={rows[-1]['claims']} pair_f1={metrics['pair_f1']:.3f} "
            f"triple_f1={metrics['triple_f1']:.3f}"
        )

    write_tsv(output / "joint_extraction_papers.tsv", rows)
    write_tsv(output / "joint_extraction_pair_review.tsv", pair_review)
    write_tsv(output / "joint_extraction_triple_review.tsv", triple_review)
    metric_fields = [
        "pair_precision",
        "pair_recall",
        "pair_f1",
        "triple_precision",
        "triple_recall",
        "triple_f1",
        "source_gene_precision",
        "source_gene_recall",
        "source_gene_f1",
    ]
    summary = {
        "schema_version": SCHEMA,
        "model": model,
        "papers": len(rows),
        "totals": {
            "raw_extractions": sum(row["raw_extractions"] for row in rows),
            "claims": sum(row["claims"] for row in rows),
            "predicted_terms": sum(row["predicted_terms"] for row in rows),
            "excluded_claims": sum(
                row["preparation_excluded_claims"] + row["strict_exclusions"]
                for row in rows
            ),
        },
        "macro_mean": {
            field: statistics.mean(row[field] for row in rows) for field in metric_fields
        },
    }
    (output / "joint_extraction_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )
    write_report(output, summary, rows)


if __name__ == "__main__":
    main()
