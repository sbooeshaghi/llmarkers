#!/usr/bin/env python3
"""Compare current mrkr claims with the source-specific LLMarkers benchmark."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ONTO_MANIFEST_SCHEMA = "llmarkers.onto-manifest.v2"
CLAIMS_SCHEMA = "llmarkers.curated-claims.v1"
ONTO_SCHEMA = "mrkr.onto.v1"

DATASET_TO_PAPER = {
    "adipose_Emont2022": "Emont2022",
    "adipose_Hildreth2021": "Hildreth2021",
    "bone_He2021": "He2021",
    "eye_Gautam2021": "Gautam2021",
    "lung_Adams2020": "Adams2020",
    "ovary_Wagner2020": "Wagner2020",
    "testis_Shamis2020": "Shamis2020",
}


@dataclass(frozen=True)
class EvidenceGene:
    """One semantic marker term with its target and source interval."""

    object_id: str
    target_label: str
    target_curie: str | None
    gene_label: str
    gene_id: str | None
    offset: tuple[int, int] | None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return "sha256:" + digest.hexdigest()


def normalize_label(value: Any) -> str:
    return " ".join(str(value or "").casefold().split())


def normalize_gene(value: Any) -> str:
    return str(value or "").strip().upper()


def normalize_curie(value: Any) -> str | None:
    if not value:
        return None
    text = str(value)
    prefix = "http://purl.obolibrary.org/obo/"
    if text.startswith(prefix):
        suffix = text.removeprefix(prefix)
        if "_" in suffix:
            namespace, identifier = suffix.split("_", 1)
            return f"{namespace}:{identifier}"
    return text


def prf(predicted: set, truth: set) -> dict[str, float]:
    intersection = len(predicted & truth)
    precision = intersection / len(predicted) if predicted else (1.0 if not truth else 0.0)
    recall = intersection / len(truth) if truth else (1.0 if not predicted else 0.0)
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    return {"precision": precision, "recall": recall, "f1": f1}


def overlaps(left: tuple[int, int] | None, right: tuple[int, int] | None) -> bool:
    if left is None or right is None:
        return False
    return left[0] < right[1] and right[0] < left[1]


def source_prf(
    predicted: list[EvidenceGene], truth: list[EvidenceGene]
) -> dict[str, float | int]:
    predicted_matches = sum(
        any(
            item.gene_id == reference.gene_id and overlaps(item.offset, reference.offset)
            for reference in truth
        )
        for item in predicted
    )
    truth_matches = sum(
        any(
            item.gene_id == reference.gene_id and overlaps(item.offset, reference.offset)
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
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "predicted_units": len(predicted),
        "truth_units": len(truth),
        "matched_predicted_units": predicted_matches,
        "matched_truth_units": truth_matches,
    }


def human_claim(claim: dict[str, Any]) -> bool:
    organism = next(
        term for term in claim["terms"] if term["term_type"] == "organism"
    )
    return organism.get("ontology_term") == "NCBITaxon:9606"


def legacy_target_label(term: dict[str, Any]) -> str:
    return normalize_label(term.get("legacy_normalized_label"))


def evidence_genes_from_benchmark(
    document: dict[str, Any], *, organism_curie: str | None = "NCBITaxon:9606"
) -> list[EvidenceGene]:
    genes: list[EvidenceGene] = []
    for claim in document["claims"]:
        if organism_curie is not None:
            organism = next(
                term for term in claim["terms"] if term["term_type"] == "organism"
            )
            if organism.get("ontology_term") != organism_curie:
                continue
        target = next(
            term for term in claim["terms"] if term["term_type"] == "celltype"
        )
        raw_offset = claim["evidence"].get("span_offset")
        offset = tuple(raw_offset) if raw_offset is not None else None
        for gene in (term for term in claim["terms"] if term["term_type"] == "gene"):
            genes.append(
                EvidenceGene(
                    object_id=claim["claim_id"],
                    target_label=legacy_target_label(target),
                    target_curie=normalize_curie(target.get("ontology_term")),
                    gene_label=normalize_gene(gene.get("normalized_label")),
                    gene_id=gene.get("ontology_term"),
                    offset=offset,
                )
            )
    return genes


def evidence_genes_from_mrkr(
    document: dict[str, Any], *, direction: str | None
) -> list[EvidenceGene]:
    genes: list[EvidenceGene] = []
    for claim in document["claims"]:
        organism = next(
            term for term in claim["terms"] if term["term_type"] == "organism"
        )
        if organism.get("ontology_term") != "NCBITaxon:9606":
            continue
        target = next(
            term for term in claim["terms"] if term["term_type"] == "celltype"
        )
        raw_offset = claim.get("span_offset")
        offset = tuple(raw_offset) if raw_offset is not None else None
        for gene in (term for term in claim["terms"] if term["term_type"] == "gene"):
            if direction is not None and gene.get("direction") != direction:
                continue
            genes.append(
                EvidenceGene(
                    object_id=claim["claim_id"],
                    target_label=normalize_label(target.get("normalized_label")),
                    target_curie=normalize_curie(target.get("ontology_term")),
                    gene_label=normalize_gene(gene.get("normalized_label")),
                    gene_id=gene.get("ontology_term"),
                    offset=offset,
                )
            )
    return genes


def facts(genes: Iterable[EvidenceGene]) -> dict[str, set]:
    items = list(genes)
    return {
        "gene_ids": {item.gene_id for item in items if item.gene_id},
        "label_pairs": {
            (item.target_label, item.gene_id)
            for item in items
            if item.target_label and item.gene_id
        },
        "curie_pairs": {
            (item.target_curie, item.gene_id)
            for item in items
            if item.target_curie and item.gene_id
        },
    }


def load_onto_manifest(root: Path) -> dict[str, Path]:
    path = root / "onto_manifest.tsv"
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != f"# schema: {ONTO_MANIFEST_SCHEMA}":
        raise ValueError(f"{path}: expected {ONTO_MANIFEST_SCHEMA}")
    result: dict[str, Path] = {}
    for line_number, line in enumerate(lines, 1):
        if not line or line.startswith("#"):
            continue
        fields = line.split("\t")
        if len(fields) != 6:
            raise ValueError(f"{path}:{line_number}: expected six fields")
        paper_id, _collection, _organism, locator, expected_hash, _source_hash = fields
        candidate = Path(locator)
        if not candidate.is_absolute():
            candidate = root / candidate
        if sha256_file(candidate) != expected_hash:
            raise ValueError(f"{candidate}: digest does not match manifest")
        result[paper_id] = candidate
    return result


def load_claim_document(path: Path, schema: str) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema_version") != schema:
        raise ValueError(f"{path}: expected {schema}")
    return document


def load_legacy_results(path: Path | None) -> dict[str, dict[str, float]]:
    if path is None:
        return {}
    result: dict[str, dict[str, float]] = {}
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream, delimiter="\t"):
            paper_id = DATASET_TO_PAPER[row["dataset"]]
            result[paper_id] = {
                "truth_pairs": int(row["truth_pairs"]),
                "precision": float(row["ext_precision"]),
                "recall": float(row["ext_recall"]),
                "f1": float(row["ext_pair_f1"]),
                "data_f1": float(row["ext_data_f1"]),
            }
    return result


def prefix(metrics: dict[str, float], name: str) -> dict[str, float]:
    return {f"{name}_{key}": value for key, value in metrics.items()}


def mean(rows: list[dict[str, Any]], field: str) -> float:
    return statistics.mean(float(row[field]) for row in rows)


def candidate_status(
    candidate: EvidenceGene,
    truth: list[EvidenceGene],
    truth_facts: dict[str, set],
) -> str:
    if not candidate.gene_id:
        return "unmapped_gene"
    if (candidate.target_label, candidate.gene_id) in truth_facts["label_pairs"]:
        return "exact_label_pair"
    if (
        candidate.target_curie
        and (candidate.target_curie, candidate.gene_id) in truth_facts["curie_pairs"]
    ):
        return "same_grounded_pair"
    if any(
        candidate.gene_id == reference.gene_id
        and overlaps(candidate.offset, reference.offset)
        for reference in truth
    ):
        return "same_gene_source_overlap"
    if candidate.gene_id in truth_facts["gene_ids"]:
        return "gene_only"
    return "not_in_text_truth"


def compare_paper(
    paper_id: str,
    mrkr_path: Path,
    benchmark_root: Path,
    legacy: dict[str, float] | None,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, set]]:
    mrkr = load_claim_document(mrkr_path, ONTO_SCHEMA)
    text_path = benchmark_root / "papers" / paper_id / "primary" / "text.claims.json"
    image_path = benchmark_root / "papers" / paper_id / "primary" / "image.claims.json"
    text = load_claim_document(text_path, CLAIMS_SCHEMA)
    image = load_claim_document(image_path, CLAIMS_SCHEMA)
    if mrkr["source"]["sha256"] != text["source"]["manuscript"]["sha256"]:
        raise ValueError(f"{paper_id}: mrkr and benchmark manuscript hashes differ")

    text_genes = evidence_genes_from_benchmark(text)
    image_genes = evidence_genes_from_benchmark(image)
    text_genes_all_organisms = evidence_genes_from_benchmark(
        text, organism_curie=None
    )
    image_genes_all_organisms = evidence_genes_from_benchmark(
        image, organism_curie=None
    )
    all_truth = [*text_genes, *image_genes]
    all_truth_all_organisms = [
        *text_genes_all_organisms,
        *image_genes_all_organisms,
    ]
    candidate_all = evidence_genes_from_mrkr(mrkr, direction=None)
    candidate_positive = evidence_genes_from_mrkr(mrkr, direction="positive")
    candidate_negative = evidence_genes_from_mrkr(mrkr, direction="negative")
    text_facts = facts(text_genes)
    all_facts = facts(all_truth)
    text_facts_all_organisms = facts(text_genes_all_organisms)
    all_facts_all_organisms = facts(all_truth_all_organisms)
    candidate_facts = facts(candidate_positive)
    source_metrics = source_prf(
        [item for item in candidate_positive if item.gene_id and item.offset],
        [item for item in text_genes if item.gene_id and item.offset],
    )

    exact_spans = sum(
        isinstance(claim.get("span_offset"), list) for claim in mrkr["claims"]
    )
    explicit_terms = sum(
        bool(target.get("sub_span")) and bool(gene.get("sub_span"))
        for claim in mrkr["claims"]
        for target in [
            next(term for term in claim["terms"] if term["term_type"] == "celltype")
        ]
        for gene in (term for term in claim["terms"] if term["term_type"] == "gene")
    )
    row: dict[str, Any] = {
        "paper_id": paper_id,
        "truth_text_records": sum(
            len(term["source_records"])
            for claim in text["claims"]
            if human_claim(claim)
            for term in claim["terms"]
            if term["term_type"] == "gene"
        ),
        "truth_text_terms": len(text_genes),
        "truth_text_pairs": len(text_facts["label_pairs"]),
        "truth_text_pairs_all_organisms": len(
            text_facts_all_organisms["label_pairs"]
        ),
        "truth_all_pairs": len(all_facts["label_pairs"]),
        "truth_all_pairs_all_organisms": len(
            all_facts_all_organisms["label_pairs"]
        ),
        "mrkr_claims": len(mrkr["claims"]),
        "mrkr_gene_terms": len(candidate_all),
        "mrkr_positive_terms": len(candidate_positive),
        "mrkr_negative_terms": len(candidate_negative),
        "mrkr_positive_mapped_pairs": len(candidate_facts["label_pairs"]),
        "mrkr_exact_span_rate": exact_spans / len(mrkr["claims"]),
        "mrkr_explicit_pair_rate": explicit_terms / len(candidate_all),
        **prefix(prf(candidate_facts["gene_ids"], text_facts["gene_ids"]), "gene"),
        **prefix(
            prf(candidate_facts["label_pairs"], text_facts["label_pairs"]),
            "strict_pair",
        ),
        **prefix(
            prf(candidate_facts["curie_pairs"], text_facts["curie_pairs"]),
            "grounded_pair",
        ),
        **prefix(
            prf(candidate_facts["label_pairs"], all_facts["label_pairs"]),
            "all_pair",
        ),
        **{f"source_gene_{key}": value for key, value in source_metrics.items()},
    }
    if legacy:
        row.update(
            {
                "legacy_truth_pairs": legacy["truth_pairs"],
                "legacy_precision": legacy["precision"],
                "legacy_recall": legacy["recall"],
                "legacy_f1": legacy["f1"],
                "legacy_data_f1": legacy["data_f1"],
            }
        )
        if row["legacy_truth_pairs"] == row["truth_text_pairs"]:
            row["legacy_truth_scope"] = "human_only"
        elif row["legacy_truth_pairs"] == row["truth_text_pairs_all_organisms"]:
            row["legacy_truth_scope"] = "all_organisms"
        else:
            row["legacy_truth_scope"] = "mismatch"

    discrepancies = [
        {
            "paper_id": paper_id,
            "claim_id": item.object_id,
            "target_label": item.target_label,
            "target_curie": item.target_curie or "",
            "gene_label": item.gene_label,
            "gene_id": item.gene_id or "",
            "direction": "positive",
            "status": candidate_status(item, text_genes, text_facts),
        }
        for item in candidate_positive
    ]
    return row, discrepancies, {
        "human": all_facts,
        "all_organisms": all_facts_all_organisms,
    }


def write_tsv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def build_summary(
    rows: list[dict[str, Any]],
    discrepancies: list[dict[str, Any]],
    all_truth_facts: list[dict[str, dict[str, set]]],
) -> dict[str, Any]:
    combined_human_pairs = set().union(
        *(item["human"]["label_pairs"] for item in all_truth_facts)
    )
    combined_all_pairs = set().union(
        *(item["all_organisms"]["label_pairs"] for item in all_truth_facts)
    )
    summary: dict[str, Any] = {
        "papers": len(rows),
        "benchmark": {
            "human_text_records": sum(row["truth_text_records"] for row in rows),
            "human_text_terms": sum(row["truth_text_terms"] for row in rows),
            "within_paper_text_pairs": sum(row["truth_text_pairs"] for row in rows),
            "cross_paper_unique_human_pairs": len(combined_human_pairs),
            "cross_paper_unique_all_organism_pairs": len(combined_all_pairs),
        },
        "mrkr": {
            "claims": sum(row["mrkr_claims"] for row in rows),
            "gene_terms": sum(row["mrkr_gene_terms"] for row in rows),
            "positive_terms": sum(row["mrkr_positive_terms"] for row in rows),
            "negative_terms": sum(row["mrkr_negative_terms"] for row in rows),
            "positive_mapped_pairs": sum(
                row["mrkr_positive_mapped_pairs"] for row in rows
            ),
            "exact_span_rate": sum(
                row["mrkr_claims"] * row["mrkr_exact_span_rate"] for row in rows
            )
            / sum(row["mrkr_claims"] for row in rows),
            "explicit_pair_rate": sum(
                row["mrkr_gene_terms"] * row["mrkr_explicit_pair_rate"] for row in rows
            )
            / sum(row["mrkr_gene_terms"] for row in rows),
        },
        "macro_mean": {
            field: mean(rows, field)
            for field in (
                "gene_precision",
                "gene_recall",
                "gene_f1",
                "strict_pair_precision",
                "strict_pair_recall",
                "strict_pair_f1",
                "grounded_pair_precision",
                "grounded_pair_recall",
                "grounded_pair_f1",
                "all_pair_precision",
                "all_pair_recall",
                "all_pair_f1",
                "source_gene_precision",
                "source_gene_recall",
                "source_gene_f1",
            )
        },
        "candidate_status": dict(
            sorted(Counter(item["status"] for item in discrepancies).items())
        ),
    }
    if "legacy_f1" in rows[0]:
        summary["legacy_macro_mean"] = {
            field: mean(rows, f"legacy_{field}")
            for field in ("precision", "recall", "f1", "data_f1")
        }
        summary["legacy_truth_scope"] = dict(
            sorted(Counter(row["legacy_truth_scope"] for row in rows).items())
        )
    return summary


def write_report(path: Path, summary: dict[str, Any]) -> None:
    benchmark = summary["benchmark"]
    mrkr = summary["mrkr"]
    macro = summary["macro_mean"]
    legacy = summary.get("legacy_macro_mean")
    lines = [
        "# mrkr versus source-specific benchmark",
        "",
        f"- Papers: {summary['papers']}",
        f"- Human text source records: {benchmark['human_text_records']}",
        f"- Human text semantic marker terms: {benchmark['human_text_terms']}",
        f"- Human text pairs summed within papers: {benchmark['within_paper_text_pairs']}",
        f"- Unique human text+image pairs across papers: "
        f"{benchmark['cross_paper_unique_human_pairs']}",
        f"- Unique all-organism text+image pairs across papers: "
        f"{benchmark['cross_paper_unique_all_organism_pairs']}",
        f"- mrkr claims: {mrkr['claims']}",
        f"- mrkr gene terms: {mrkr['gene_terms']} "
        f"({mrkr['positive_terms']} positive; {mrkr['negative_terms']} negative)",
        f"- Exact source-span rate: {mrkr['exact_span_rate']:.3f}",
        f"- Explicit target+gene rate: {mrkr['explicit_pair_rate']:.3f}",
        "",
        "## Macro-average comparison",
        "",
        "| Evaluation | Precision | Recall | F1 |",
        "| --- | ---: | ---: | ---: |",
        f"| Gene identity only | {macro['gene_precision']:.3f} | "
        f"{macro['gene_recall']:.3f} | {macro['gene_f1']:.3f} |",
        f"| Strict target label + gene | {macro['strict_pair_precision']:.3f} | "
        f"{macro['strict_pair_recall']:.3f} | {macro['strict_pair_f1']:.3f} |",
        f"| Grounded target + gene | {macro['grounded_pair_precision']:.3f} | "
        f"{macro['grounded_pair_recall']:.3f} | {macro['grounded_pair_f1']:.3f} |",
        f"| Source-anchored gene | {macro['source_gene_precision']:.3f} | "
        f"{macro['source_gene_recall']:.3f} | {macro['source_gene_f1']:.3f} |",
        f"| Strict pair against text+image | {macro['all_pair_precision']:.3f} | "
        f"{macro['all_pair_recall']:.3f} | {macro['all_pair_f1']:.3f} |",
    ]
    if legacy:
        lines.extend(
            [
                f"| Legacy reported strict pair | {legacy['precision']:.3f} | "
                f"{legacy['recall']:.3f} | {legacy['f1']:.3f} |",
                "",
                "The legacy result and current strict-pair result are different model outputs "
                "and different target-normalization pipelines. The source-anchored metric "
                "separates marker extraction from target-label normalization.",
            ]
        )
    lines.extend(
        [
            "",
            "## Candidate term disposition",
            "",
            *(
                f"- {key}: {value}"
                for key, value in summary["candidate_status"].items()
            ),
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mrkr-root", required=True, type=Path)
    parser.add_argument("--benchmark-root", required=True, type=Path)
    parser.add_argument("--legacy-results", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mrkr_paths = load_onto_manifest(args.mrkr_root.resolve())
    benchmark_root = args.benchmark_root.resolve()
    reconciliation = json.loads(
        (benchmark_root / "reconciliation.json").read_text(encoding="utf-8")
    )
    if reconciliation.get("status") != "ok":
        raise ValueError("benchmark evidence has not reconciled successfully")
    legacy = load_legacy_results(
        args.legacy_results.resolve() if args.legacy_results else None
    )
    if legacy and set(legacy) != set(mrkr_paths):
        raise ValueError("legacy result and mrkr paper sets differ")

    rows: list[dict[str, Any]] = []
    discrepancies: list[dict[str, Any]] = []
    all_truth_facts: list[dict[str, dict[str, set]]] = []
    for paper_id in sorted(mrkr_paths):
        row, paper_discrepancies, truth_facts = compare_paper(
            paper_id,
            mrkr_paths[paper_id],
            benchmark_root,
            legacy.get(paper_id) if legacy else None,
        )
        rows.append(row)
        discrepancies.extend(paper_discrepancies)
        all_truth_facts.append(truth_facts)

    summary = build_summary(rows, discrepancies, all_truth_facts)
    output = args.out.resolve()
    output.mkdir(parents=True, exist_ok=True)
    write_tsv(output / "comparison_papers.tsv", rows)
    write_tsv(output / "candidate_terms.tsv", discrepancies)
    (output / "comparison_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_report(output / "comparison_report.md", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
