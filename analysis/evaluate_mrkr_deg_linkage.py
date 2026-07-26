#!/usr/bin/env python3
"""Ask an LLM to link source-grounded mrkr claims to paper-specific DEG sources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import statistics
import time
import urllib.error
import urllib.request
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


LINKAGE_SCHEMA = "mrkr.deg-linkage.v1"
ONTO_MANIFEST_SCHEMA = "llmarkers.onto-manifest.v2"
CLAIMS_SCHEMA = "llmarkers.curated-claims.v1"
PROFILES_SCHEMA = "llmarkers.deg-profiles.v1"
DEFAULT_MODEL = "claude-opus-4-6"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"


@dataclass(frozen=True)
class MarkerTerm:
    """One positive marker term used in the linkage evaluation."""

    claim_id: str
    target_label: str
    gene_id: str
    data_id: str | None
    offset: tuple[int, int] | None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def portable_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def normalize_label(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def load_json(path: Path, schema: str | None = None) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if schema is not None and document.get("schema_version") != schema:
        raise ValueError(f"{path}: expected schema {schema}")
    return document


def load_onto_manifest(root: Path) -> dict[str, Path]:
    manifest = root / "onto_manifest.tsv"
    lines = manifest.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != f"# schema: {ONTO_MANIFEST_SCHEMA}":
        raise ValueError(f"{manifest}: expected {ONTO_MANIFEST_SCHEMA}")
    result: dict[str, Path] = {}
    for line_number, line in enumerate(lines, 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 6:
            raise ValueError(f"{manifest}:{line_number}: expected six fields")
        paper_id, _collection, _organism, locator, expected_hash, _source_hash = fields
        path = Path(locator)
        if not path.is_absolute():
            path = root / path
        if sha256_file(path) != expected_hash:
            raise ValueError(f"{path}: digest does not match manifest")
        result[paper_id] = path
    return result


def benchmark_paths(root: Path, paper_id: str) -> tuple[Path, Path]:
    paper = root / "papers" / paper_id / "primary"
    text = paper / "text.claims.json"
    deg = paper / "deg.profiles.json"
    if not text.is_file() or not deg.is_file():
        raise FileNotFoundError(f"missing benchmark documents for {paper_id}")
    return text, deg


def claim_target(claim: dict[str, Any]) -> dict[str, Any]:
    targets = [term for term in claim["terms"] if term["term_type"] == "celltype"]
    if len(targets) != 1:
        raise ValueError(f"{claim.get('claim_id')}: expected one celltype term")
    return targets[0]


def claim_genes(
    claim: dict[str, Any], *, positive_only: bool = False
) -> list[dict[str, Any]]:
    genes = [term for term in claim["terms"] if term["term_type"] == "gene"]
    if positive_only:
        genes = [term for term in genes if term.get("direction") == "positive"]
    return genes


def deg_catalog(document: dict[str, Any]) -> dict[str, list[str]]:
    """Return the candidate DEG source IDs and the cell-type labels in each."""

    labels: dict[str, set[str]] = defaultdict(set)
    for profile in document["profiles"]:
        data_id = profile["evidence"].get("data_id")
        if not data_id:
            raise ValueError(f"{profile.get('profile_id')}: DEG profile has no data_id")
        target = claim_target(profile)
        label = target.get("legacy_normalized_label") or target.get("normalized_label")
        if label:
            labels[data_id].add(str(label))
    return {data_id: sorted(values) for data_id, values in sorted(labels.items())}


def claim_inputs(document: dict[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for claim in document["claims"]:
        target = claim_target(claim)
        genes = claim_genes(claim)
        result.append(
            {
                "claim_id": claim["claim_id"],
                "source_span": claim["span_literal"],
                "summary": claim["summary"],
                "target": target["normalized_label"],
                "genes": [
                    {
                        "label": gene["normalized_label"],
                        "direction": gene["direction"],
                    }
                    for gene in genes
                ],
            }
        )
    return result


def build_prompt(
    paper_id: str,
    catalog: dict[str, list[str]],
    claims: list[dict[str, Any]],
) -> str:
    """Build the isolated DEG-source selection prompt for one paper."""

    return f"""You are linking reported marker evidence to differential-expression sources from one paper.

# Task
For every marker claim, select the one candidate data_id that most likely contains the
DEG comparison supporting that claim. Use the exact source span, target, genes, and the
cell-type labels available in each candidate source. Prefer a specific subtype source over
a broad all-markers source when the manuscript context supports that choice. Return null
when the supplied evidence does not support one candidate.

Do not invent or alter claim_id or data_id values. This is a source-selection task; do not
extract new markers.

# Output
Return only one JSON object with this shape:
{{
  "links": [
    {{"claim_id": "claim:...", "data_id": "exact candidate ID or null", "reason": "brief reason"}}
  ]
}}

Return exactly one link for every supplied claim, in the same order.

# Paper
{paper_id}

# Candidate DEG sources
{json.dumps(catalog, indent=2, ensure_ascii=True)}

# Marker claims
{json.dumps(claims, indent=2, ensure_ascii=True)}
"""


def load_env_file(path: Path | None) -> None:
    if path is None or not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def response_json(text: str) -> dict[str, Any]:
    value = text.strip()
    if "```" in value:
        lines = value.splitlines()
        start = next(
            (index + 1 for index, line in enumerate(lines) if line.strip().startswith("```")),
            None,
        )
        if start is not None:
            end = next(
                (index for index in range(start, len(lines)) if lines[index].strip() == "```"),
                None,
            )
            if end is not None:
                value = "\n".join(lines[start:end]).strip()
    first = value.find("{")
    last = value.rfind("}")
    if 0 <= first < last:
        value = value[first : last + 1]
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("model response is not a JSON object")
    return parsed


def call_anthropic(prompt: str, model: str, timeout: float) -> tuple[dict, dict]:
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is required with --run-llm")
    payload = {
        "model": model,
        "max_tokens": 12_000,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}],
    }
    request = urllib.request.Request(
        ANTHROPIC_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
            "content-type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Anthropic API returned HTTP {error.code}: {detail}") from error
    text = next(
        (block["text"] for block in raw.get("content", []) if block.get("type") == "text"),
        "",
    )
    if not text:
        raise ValueError("Anthropic response contained no text block")
    return response_json(text), raw


def validate_links(
    response: dict[str, Any],
    claim_ids: list[str],
    candidate_ids: set[str],
) -> list[dict[str, Any]]:
    links = response.get("links")
    if not isinstance(links, list):
        raise ValueError("response.links must be an array")
    found: dict[str, dict[str, Any]] = {}
    for index, link in enumerate(links):
        if not isinstance(link, dict):
            raise ValueError(f"links[{index}] must be an object")
        claim_id = link.get("claim_id")
        if claim_id not in claim_ids:
            raise ValueError(f"links[{index}] has an unknown claim_id: {claim_id}")
        if claim_id in found:
            raise ValueError(f"duplicate link for {claim_id}")
        data_id = link.get("data_id")
        if data_id is not None and data_id not in candidate_ids:
            raise ValueError(f"{claim_id}: unknown data_id: {data_id}")
        reason = link.get("reason")
        if not isinstance(reason, str):
            raise ValueError(f"{claim_id}: reason must be a string")
        found[claim_id] = {
            "claim_id": claim_id,
            "data_id": data_id,
            "reason": reason.strip(),
        }
    missing = [claim_id for claim_id in claim_ids if claim_id not in found]
    if missing:
        raise ValueError(f"response omitted {len(missing)} claim(s): {missing[:3]}")
    return [found[claim_id] for claim_id in claim_ids]


def label_baseline(
    claims: list[dict[str, Any]], catalog: dict[str, list[str]]
) -> list[dict[str, Any]]:
    """Choose the narrowest source containing an exact normalized target label."""

    normalized = {
        data_id: {normalize_label(label) for label in labels}
        for data_id, labels in catalog.items()
    }
    links: list[dict[str, Any]] = []
    for claim in claims:
        target = normalize_label(claim["target"])
        matches = [
            data_id for data_id, labels in normalized.items() if target in labels
        ]
        selected = min(matches, key=lambda item: (len(catalog[item]), item)) if matches else None
        links.append(
            {
                "claim_id": claim["claim_id"],
                "data_id": selected,
                "reason": "narrowest exact target-label source" if selected else "no exact target-label source",
            }
        )
    return links


def interval(value: Any) -> tuple[int, int] | None:
    if not isinstance(value, list) or len(value) != 2:
        return None
    return int(value[0]), int(value[1])


def predicted_terms(
    document: dict[str, Any], links: Iterable[dict[str, Any]]
) -> list[MarkerTerm]:
    by_claim = {link["claim_id"]: link["data_id"] for link in links}
    result: list[MarkerTerm] = []
    for claim in document["claims"]:
        target = normalize_label(claim_target(claim)["normalized_label"])
        data_id = by_claim[claim["claim_id"]]
        for gene in claim_genes(claim, positive_only=True):
            gene_id = gene.get("ontology_term")
            if not gene_id:
                continue
            result.append(
                MarkerTerm(
                    claim_id=claim["claim_id"],
                    target_label=target,
                    gene_id=gene_id,
                    data_id=data_id,
                    offset=interval(claim.get("span_offset")),
                )
            )
    return result


def human_terms(document: dict[str, Any]) -> list[MarkerTerm]:
    result: list[MarkerTerm] = []
    for claim in document["claims"]:
        organism = next(
            term for term in claim["terms"] if term["term_type"] == "organism"
        )
        if organism.get("ontology_term") != "NCBITaxon:9606":
            continue
        target_term = claim_target(claim)
        target = normalize_label(
            target_term.get("legacy_normalized_label")
            or target_term.get("normalized_label")
        )
        for gene in claim_genes(claim):
            gene_id = gene.get("ontology_term")
            if not gene_id:
                continue
            result.append(
                MarkerTerm(
                    claim_id=claim["claim_id"],
                    target_label=target,
                    gene_id=gene_id,
                    data_id=claim["evidence"].get("data_id"),
                    offset=interval(claim["evidence"].get("span_offset")),
                )
            )
    return result


def overlaps(left: tuple[int, int] | None, right: tuple[int, int] | None) -> bool:
    if left is None or right is None:
        return False
    return left[0] < right[1] and right[0] < left[1]


def prf(predicted: set, truth: set) -> dict[str, float]:
    matched = len(predicted & truth)
    precision = matched / len(predicted) if predicted else 0.0
    recall = matched / len(truth) if truth else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    return {"precision": precision, "recall": recall, "f1": f1}


def source_gene_prf(
    predicted: list[MarkerTerm], truth: list[MarkerTerm]
) -> dict[str, float]:
    predicted_matches = sum(
        any(
            item.data_id == reference.data_id
            and item.gene_id == reference.gene_id
            and overlaps(item.offset, reference.offset)
            for reference in truth
        )
        for item in predicted
    )
    truth_matches = sum(
        any(
            item.data_id == reference.data_id
            and item.gene_id == reference.gene_id
            and overlaps(item.offset, reference.offset)
            for item in predicted
        )
        for reference in truth
    )
    precision = predicted_matches / len(predicted) if predicted else 0.0
    recall = truth_matches / len(truth) if truth else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    return {"precision": precision, "recall": recall, "f1": f1}


def conditional_accuracy(
    predicted: list[MarkerTerm],
    truth: list[MarkerTerm],
    *,
    match_source: bool,
) -> tuple[int, int, float | None]:
    eligible = 0
    correct = 0
    for item in predicted:
        references = [
            reference
            for reference in truth
            if item.gene_id == reference.gene_id
            and (
                overlaps(item.offset, reference.offset)
                if match_source
                else item.target_label == reference.target_label
            )
            and reference.data_id is not None
        ]
        if not references:
            continue
        eligible += 1
        correct += item.data_id in {reference.data_id for reference in references}
    return eligible, correct, correct / eligible if eligible else None


def matching_data_ids(
    item: MarkerTerm,
    truth: list[MarkerTerm],
    *,
    match_source: bool,
) -> set[str]:
    return {
        reference.data_id
        for reference in truth
        if reference.data_id is not None
        and item.gene_id == reference.gene_id
        and (
            overlaps(item.offset, reference.offset)
            if match_source
            else item.target_label == reference.target_label
        )
    }


def term_review(
    paper_id: str,
    predicted: list[MarkerTerm],
    baseline: list[MarkerTerm],
    truth: list[MarkerTerm],
) -> list[dict[str, Any]]:
    if len(predicted) != len(baseline):
        raise ValueError(f"{paper_id}: LLM and baseline term counts differ")
    rows: list[dict[str, Any]] = []
    for item, reference_item in zip(predicted, baseline, strict=True):
        identity = (item.claim_id, item.target_label, item.gene_id, item.offset)
        baseline_identity = (
            reference_item.claim_id,
            reference_item.target_label,
            reference_item.gene_id,
            reference_item.offset,
        )
        if identity != baseline_identity:
            raise ValueError(f"{paper_id}: LLM and baseline term order differs")
        exact_ids = matching_data_ids(item, truth, match_source=False)
        source_ids = matching_data_ids(item, truth, match_source=True)
        rows.append(
            {
                "paper_id": paper_id,
                "claim_id": item.claim_id,
                "target_label": item.target_label,
                "gene_id": item.gene_id,
                "llm_data_id": item.data_id or "",
                "baseline_data_id": reference_item.data_id or "",
                "exact_pair_truth_data_ids": ";".join(sorted(exact_ids)),
                "source_gene_truth_data_ids": ";".join(sorted(source_ids)),
                "llm_exact_pair_correct": (
                    item.data_id in exact_ids if exact_ids else None
                ),
                "baseline_exact_pair_correct": (
                    reference_item.data_id in exact_ids if exact_ids else None
                ),
                "llm_source_gene_correct": (
                    item.data_id in source_ids if source_ids else None
                ),
                "baseline_source_gene_correct": (
                    reference_item.data_id in source_ids if source_ids else None
                ),
            }
        )
    return rows


def claim_review(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse term matches to the claim, the unit receiving one data_id."""

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(row["paper_id"], row["claim_id"])].append(row)
    result: list[dict[str, Any]] = []
    for (paper_id, claim_id), terms in grouped.items():
        exact_ids = {
            value
            for row in terms
            for value in str(row["exact_pair_truth_data_ids"]).split(";")
            if value
        }
        source_ids = {
            value
            for row in terms
            for value in str(row["source_gene_truth_data_ids"]).split(";")
            if value
        }
        llm_data_id = terms[0]["llm_data_id"]
        baseline_data_id = terms[0]["baseline_data_id"]
        result.append(
            {
                "paper_id": paper_id,
                "claim_id": claim_id,
                "target_label": terms[0]["target_label"],
                "mapped_positive_terms": len(terms),
                "llm_data_id": llm_data_id,
                "baseline_data_id": baseline_data_id,
                "exact_pair_truth_data_ids": ";".join(sorted(exact_ids)),
                "source_gene_truth_data_ids": ";".join(sorted(source_ids)),
                "llm_exact_pair_correct": (
                    llm_data_id in exact_ids if exact_ids else None
                ),
                "baseline_exact_pair_correct": (
                    baseline_data_id in exact_ids if exact_ids else None
                ),
                "llm_source_gene_correct": (
                    llm_data_id in source_ids if source_ids else None
                ),
                "baseline_source_gene_correct": (
                    baseline_data_id in source_ids if source_ids else None
                ),
            }
        )
    return result


def mcnemar_exact(llm_only: int, baseline_only: int) -> float:
    discordant = llm_only + baseline_only
    if discordant == 0:
        return 1.0
    tail = sum(math.comb(discordant, value) for value in range(min(llm_only, baseline_only) + 1))
    return min(1.0, 2 * tail / (2**discordant))


def paired_summary(rows: list[dict[str, Any]], suffix: str) -> dict[str, Any]:
    llm_field = f"llm_{suffix}_correct"
    baseline_field = f"baseline_{suffix}_correct"
    evaluable = [row for row in rows if row[llm_field] is not None]
    llm_correct = sum(row[llm_field] is True for row in evaluable)
    baseline_correct = sum(row[baseline_field] is True for row in evaluable)
    llm_only = sum(
        row[llm_field] is True and row[baseline_field] is False for row in evaluable
    )
    baseline_only = sum(
        row[llm_field] is False and row[baseline_field] is True for row in evaluable
    )
    return {
        "evaluable": len(evaluable),
        "llm_correct": llm_correct,
        "llm_accuracy": llm_correct / len(evaluable) if evaluable else None,
        "baseline_correct": baseline_correct,
        "baseline_accuracy": baseline_correct / len(evaluable) if evaluable else None,
        "llm_only_correct": llm_only,
        "baseline_only_correct": baseline_only,
        "mcnemar_exact_p": mcnemar_exact(llm_only, baseline_only),
    }


def evaluate(
    predicted: list[MarkerTerm], truth: list[MarkerTerm]
) -> dict[str, float | int | None]:
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
    triple = prf(predicted_triples, truth_triples)
    source = source_gene_prf(predicted, truth)
    exact_n, exact_correct, exact_accuracy = conditional_accuracy(
        predicted, truth, match_source=False
    )
    source_n, source_correct, source_accuracy = conditional_accuracy(
        predicted, truth, match_source=True
    )
    return {
        "linked_terms": sum(item.data_id is not None for item in predicted),
        "terms": len(predicted),
        "link_rate": (
            sum(item.data_id is not None for item in predicted) / len(predicted)
            if predicted
            else 0.0
        ),
        "triple_precision": triple["precision"],
        "triple_recall": triple["recall"],
        "triple_f1": triple["f1"],
        "source_gene_precision": source["precision"],
        "source_gene_recall": source["recall"],
        "source_gene_f1": source["f1"],
        "exact_pair_evaluable": exact_n,
        "exact_pair_correct": exact_correct,
        "exact_pair_link_accuracy": exact_accuracy,
        "source_gene_evaluable": source_n,
        "source_gene_correct": source_correct,
        "source_gene_link_accuracy": source_accuracy,
    }


def macro(rows: list[dict[str, Any]], prefix: str) -> dict[str, float]:
    fields = [
        "link_rate",
        "claim_link_rate",
        "triple_precision",
        "triple_recall",
        "triple_f1",
        "source_gene_precision",
        "source_gene_recall",
        "source_gene_f1",
        "exact_pair_link_accuracy",
        "source_gene_link_accuracy",
        "claim_exact_pair_link_accuracy",
        "claim_source_gene_link_accuracy",
    ]
    result: dict[str, float] = {}
    for field in fields:
        values = [row[prefix + field] for row in rows if row[prefix + field] is not None]
        result[field] = statistics.mean(values) if values else 0.0
    return result


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_report(output: Path, summary: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    llm = summary["macro_mean"]["llm"]
    baseline = summary["macro_mean"]["label_baseline"]
    lines = [
        "# mrkr DEG-source linkage experiment",
        "",
        "This analysis is separate from the `mrkr` extraction schema. The LLM selected one "
        "paper-specific DEG source for each validated marker claim from a catalog containing "
        "only source IDs and their cell-type labels.",
        "",
        f"- Papers: {summary['papers']}",
        f"- Claims: {summary['claims']}",
        f"- Positive mapped gene terms: {summary['positive_mapped_terms']}",
        f"- Model: `{summary['model']}`",
        "",
        "## Macro-average results",
        "",
        "| Method | Claim link rate | Exact triple F1 | Source+gene F1 | Claim source-link accuracy |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| LLM | {llm['claim_link_rate']:.3f} | {llm['triple_f1']:.3f} | "
        f"{llm['source_gene_f1']:.3f} | {llm['claim_source_gene_link_accuracy']:.3f} |",
        f"| Exact-label baseline | {baseline['claim_link_rate']:.3f} | "
        f"{baseline['triple_f1']:.3f} | {baseline['source_gene_f1']:.3f} | "
        f"{baseline['claim_source_gene_link_accuracy']:.3f} |",
        "",
        "## Pooled claim-level linkage",
        "",
        "| Matching evidence | LLM | Exact-label baseline | Paired exact p |",
        "| --- | ---: | ---: | ---: |",
    ]
    for label, key in (
        ("Exact target+gene", "exact_pair"),
        ("Source-overlapping gene", "source_gene"),
    ):
        item = summary["pooled_conditional_claims"][key]
        lines.append(
            f"| {label} | {item['llm_correct']}/{item['evaluable']} "
            f"({item['llm_accuracy']:.1%}) | {item['baseline_correct']}/{item['evaluable']} "
            f"({item['baseline_accuracy']:.1%}) | {item['mcnemar_exact_p']:.3g} |"
        )
    lines.extend(
        [
            "",
            "The claim-level analysis is primary because the model selects one `data_id` per claim. "
            "Exact triple F1 requires the selected `data_id`, normalized target label, and gene. "
            "Source+gene F1 requires the selected `data_id` and gene to overlap the human-curated "
            "source span without requiring the normalized target label. Conditional linkage "
            "accuracy is calculated only for claims already matched to human evidence by at least "
            "one marker term, so it isolates source selection from extraction coverage. The paired "
            "exact test is descriptive because claims within a paper are not independent.",
            "",
            "## Per-paper results",
            "",
            "| Paper | Claims | Sources | LLM triple F1 | LLM source+gene F1 | LLM claim link accuracy | Baseline claim link accuracy |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        def shown(value: Any) -> str:
            return "--" if value is None else f"{value:.3f}"

        lines.append(
            f"| {row['paper_id']} | {row['claims']} | {row['candidate_sources']} | "
            f"{row['llm_triple_f1']:.3f} | {row['llm_source_gene_f1']:.3f} | "
            f"{shown(row['llm_claim_source_gene_link_accuracy'])} | "
            f"{shown(row['baseline_claim_source_gene_link_accuracy'])} |"
        )
    (output / "linkage_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mrkr-root", required=True, type=Path)
    parser.add_argument("--benchmark-root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--run-llm", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument("--limit", type=int)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    load_env_file(args.env_file)
    model = args.model or os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)
    candidate_paths = load_onto_manifest(args.mrkr_root.resolve())
    papers = sorted(candidate_paths)
    if args.limit is not None:
        papers = papers[: args.limit]
    output = args.out.resolve()
    links_dir = output / "links"
    links_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    link_rows: list[dict[str, Any]] = []
    review_rows: list[dict[str, Any]] = []
    claim_review_rows: list[dict[str, Any]] = []
    total_claims = 0
    total_terms = 0
    for paper_id in papers:
        candidate_path = candidate_paths[paper_id]
        human_path, deg_path = benchmark_paths(args.benchmark_root.resolve(), paper_id)
        candidate = load_json(candidate_path, "mrkr.onto.v1")
        human = load_json(human_path, CLAIMS_SCHEMA)
        deg = load_json(deg_path, PROFILES_SCHEMA)
        catalog = deg_catalog(deg)
        claims = claim_inputs(candidate)
        claim_ids = [claim["claim_id"] for claim in claims]
        output_path = links_dir / f"{paper_id}.json"

        started = time.monotonic()
        if args.run_llm and (args.force or not output_path.is_file()):
            parsed, raw = call_anthropic(
                build_prompt(paper_id, catalog, claims), model, args.timeout
            )
            links = validate_links(parsed, claim_ids, set(catalog))
            usage = raw.get("usage", {})
            artifact = {
                "schema_version": LINKAGE_SCHEMA,
                "paper_id": paper_id,
                "model": raw.get("model", model),
                "source": {
                    "mrkr_claims": {
                        "path": portable_path(candidate_path),
                        "sha256": sha256_file(candidate_path),
                    },
                    "benchmark_deg": {
                        "path": portable_path(deg_path),
                        "sha256": sha256_file(deg_path),
                    },
                },
                "candidate_data_ids": sorted(catalog),
                "usage": {
                    "input_tokens": usage.get("input_tokens"),
                    "output_tokens": usage.get("output_tokens"),
                },
                "elapsed_seconds": time.monotonic() - started,
                "links": links,
            }
            output_path.write_text(
                json.dumps(artifact, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        else:
            artifact = load_json(output_path, LINKAGE_SCHEMA)
            if artifact["source"]["mrkr_claims"]["sha256"] != sha256_file(candidate_path):
                raise ValueError(f"{output_path}: mrkr claim digest is stale")
            if artifact["source"]["benchmark_deg"]["sha256"] != sha256_file(deg_path):
                raise ValueError(f"{output_path}: DEG profile digest is stale")
            links = validate_links(artifact, claim_ids, set(catalog))

        baseline_links = label_baseline(claims, catalog)
        predicted = predicted_terms(candidate, links)
        baseline = predicted_terms(candidate, baseline_links)
        truth = human_terms(human)
        llm_metrics = evaluate(predicted, truth)
        baseline_metrics = evaluate(baseline, truth)
        paper_term_review = term_review(paper_id, predicted, baseline, truth)
        paper_claim_review = claim_review(paper_term_review)
        review_rows.extend(paper_term_review)
        claim_review_rows.extend(paper_claim_review)
        llm_claim_exact = paired_summary(paper_claim_review, "exact_pair")
        llm_claim_source = paired_summary(paper_claim_review, "source_gene")
        row: dict[str, Any] = {
            "paper_id": paper_id,
            "claims": len(claims),
            "candidate_sources": len(catalog),
        }
        row.update({f"llm_{key}": value for key, value in llm_metrics.items()})
        row.update({f"baseline_{key}": value for key, value in baseline_metrics.items()})
        row.update(
            {
                "llm_claim_link_rate": sum(link["data_id"] is not None for link in links)
                / len(links),
                "baseline_claim_link_rate": sum(
                    link["data_id"] is not None for link in baseline_links
                )
                / len(baseline_links),
                "llm_claim_exact_pair_link_accuracy": llm_claim_exact["llm_accuracy"],
                "baseline_claim_exact_pair_link_accuracy": llm_claim_exact[
                    "baseline_accuracy"
                ],
                "llm_claim_source_gene_link_accuracy": llm_claim_source["llm_accuracy"],
                "baseline_claim_source_gene_link_accuracy": llm_claim_source[
                    "baseline_accuracy"
                ],
            }
        )
        rows.append(row)
        total_claims += len(claims)
        total_terms += len(predicted)
        for link in links:
            link_rows.append({"paper_id": paper_id, **link})
        print(
            f"{paper_id}: {len(claims)} claims, {len(catalog)} sources, "
            f"source-link accuracy={llm_metrics['source_gene_link_accuracy']}"
        )

    summary = {
        "schema_version": LINKAGE_SCHEMA,
        "papers": len(rows),
        "claims": total_claims,
        "positive_mapped_terms": total_terms,
        "model": model,
        "macro_mean": {
            "llm": macro(rows, "llm_"),
            "label_baseline": macro(rows, "baseline_"),
        },
        "pooled_conditional_claims": {
            "exact_pair": paired_summary(claim_review_rows, "exact_pair"),
            "source_gene": paired_summary(claim_review_rows, "source_gene"),
        },
        "pooled_conditional_terms": {
            "exact_pair": paired_summary(review_rows, "exact_pair"),
            "source_gene": paired_summary(review_rows, "source_gene"),
        },
    }
    write_tsv(output / "linkage_papers.tsv", rows)
    write_tsv(output / "linkage_claims.tsv", link_rows)
    write_tsv(output / "linkage_claim_review.tsv", claim_review_rows)
    write_tsv(output / "linkage_term_review.tsv", review_rows)
    (output / "linkage_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(output, summary, rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
