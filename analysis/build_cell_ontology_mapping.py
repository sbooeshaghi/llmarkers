#!/usr/bin/env python3
"""Prototype profile-to-Cell-Ontology mapping.

This script maps each marker profile to Cell Ontology (CL) three ways:

1. full_context: reported label + marker genes + paper/source context
2. label_context: reported label + paper/source context, with markers hidden
3. marker_context: marker genes + paper context, with the reported label hidden

The LLM is bounded to a deterministic candidate list from CL names, synonyms,
definitions, and marker-program heuristics. It must choose a candidate CL term
or return unmapped.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import re
import sqlite3
import textwrap
import unicodedata
import urllib.request
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = REPO_ROOT / "docs" / "llmarkers.sqlite"
DEFAULT_ONTOLOGY = REPO_ROOT / "analysis" / "cache" / "cl-basic.obo"
RESULTS_DIR = REPO_ROOT / "analysis" / "results"
DEFAULT_MAPPINGS = RESULTS_DIR / "profile_cell_ontology_mappings.jsonl"
DEFAULT_COMPARISON = RESULTS_DIR / "profile_cell_ontology_comparison.tsv"
DEFAULT_SUMMARY = RESULTS_DIR / "profile_cell_ontology_summary.tsv"
DEFAULT_ABLATION = RESULTS_DIR / "profile_cell_ontology_ablation.tsv"
DEFAULT_COSTS = RESULTS_DIR / "profile_cell_ontology_costs.tsv"
DEFAULT_PILOT = RESULTS_DIR / "profile_cell_ontology_pilot_profiles.tsv"

CL_BASIC_URL = "https://purl.obolibrary.org/obo/cl/cl-basic.obo"

MODEL_PRICE_PER_MTOK = {
    # Anthropic Claude Sonnet 4/4.5 API list price, USD per million tokens.
    # Cache prices are included so cost accounting remains correct if the API
    # response includes cache write/read usage.
    "sonnet": {
        "input": 3.00,
        "output": 15.00,
        "cache_creation": 3.75,
        "cache_read": 0.30,
    },
    "haiku": {
        "input": 0.80,
        "output": 4.00,
        "cache_creation": 1.00,
        "cache_read": 0.08,
    },
    "opus": {
        "input": 15.00,
        "output": 75.00,
        "cache_creation": 18.75,
        "cache_read": 1.50,
    },
}

GENERIC_TOKENS = {
    "a",
    "an",
    "and",
    "cell",
    "cells",
    "cluster",
    "clusters",
    "component",
    "components",
    "from",
    "group",
    "high",
    "human",
    "low",
    "marker",
    "markers",
    "of",
    "population",
    "populations",
    "positive",
    "program",
    "reported",
    "study",
    "the",
    "type",
    "types",
}

IMMUNE_LABEL_RE = re.compile(
    r"\b("
    r"treg|regulatory|t[\s_-]?cell|cd4|cd8|exhaust|tex|naive|memory|"
    r"macrophage|monocyte|myeloid|tam|trem2|spp1|apoe|dendritic|"
    r"nk|b[\s_-]?cell|plasma|neutrophil|mast"
    r")\b",
    flags=re.IGNORECASE,
)

MARKER_PROGRAMS: list[tuple[str, set[str], tuple[str, ...]]] = [
    ("regulatory T cell", {"FOXP3", "IL2RA", "CTLA4", "IKZF2", "CCR8"}, ("regulatory T cell", "T cell")),
    ("CD8-positive T cell", {"CD8A", "CD8B", "GZMB", "PRF1", "NKG7"}, ("CD8-positive T cell", "cytotoxic T cell", "T cell")),
    ("CD4-positive T cell", {"CD4", "IL7R", "CCR7", "TCF7", "LEF1"}, ("CD4-positive T cell", "T cell")),
    ("exhausted T cell", {"PDCD1", "HAVCR2", "LAG3", "TOX", "CXCL13", "TIGIT"}, ("exhausted T cell", "T cell")),
    ("T cell", {"CD3D", "CD3E", "TRAC", "TRBC1", "TRBC2"}, ("T cell",)),
    ("natural killer cell", {"NKG7", "GNLY", "KLRD1", "KLRF1", "FCGR3A", "TYROBP"}, ("natural killer cell", "lymphocyte")),
    ("B cell", {"MS4A1", "CD79A", "CD79B", "BANK1", "CD19"}, ("B cell",)),
    ("plasma cell", {"MZB1", "XBP1", "JCHAIN", "IGHG1", "IGHM"}, ("plasma cell", "B cell")),
    ("monocyte", {"CD14", "FCN1", "S100A8", "S100A9", "VCAN", "LST1", "LYZ"}, ("monocyte", "myeloid cell")),
    ("macrophage", {"CD68", "CD163", "MRC1", "C1QA", "C1QB", "C1QC", "APOE", "TREM2", "SPP1"}, ("macrophage", "myeloid cell")),
    ("dendritic cell", {"FCER1A", "CLEC10A", "CD1C", "CLEC9A", "XCR1", "LAMP3", "CCR7"}, ("dendritic cell", "myeloid cell")),
    ("neutrophil", {"S100A8", "S100A9", "FCGR3B", "CXCR2", "CSF3R"}, ("neutrophil", "granulocyte")),
    ("mast cell", {"TPSAB1", "TPSB2", "KIT", "CPA3"}, ("mast cell",)),
    ("endothelial cell", {"PECAM1", "VWF", "KDR", "CLDN5", "ESAM"}, ("endothelial cell",)),
    ("fibroblast", {"COL1A1", "COL1A2", "DCN", "LUM", "PDGFRA"}, ("fibroblast",)),
    ("epithelial cell", {"EPCAM", "KRT8", "KRT18", "KRT19", "KRT5"}, ("epithelial cell",)),
]

LABEL_EXPANSIONS: list[tuple[re.Pattern[str], tuple[str, ...]]] = [
    (re.compile(r"\bTEXH?\b|EXHAUST", re.IGNORECASE), ("exhausted T cell", "CD8-positive exhausted alpha-beta T cell", "T cell")),
    (re.compile(r"\bTCM\b|CENTRAL MEMORY", re.IGNORECASE), ("central memory T cell", "memory T cell", "T cell")),
    (re.compile(r"\bTN\b|NAIVE", re.IGNORECASE), ("naive T cell", "T cell")),
    (re.compile(r"\bTREG\b|REGULATORY", re.IGNORECASE), ("regulatory T cell", "T cell")),
    (re.compile(r"\bTAM\b|TUMO(U)?R[- ]ASSOCIATED MACROPHAGE", re.IGNORECASE), ("tumor-associated macrophage", "macrophage", "myeloid cell")),
    (re.compile(r"TREM2", re.IGNORECASE), ("TREM2-positive macrophage", "macrophage", "myeloid cell")),
    (re.compile(r"CD8", re.IGNORECASE), ("CD8-positive T cell", "CD8-positive alpha-beta T cell", "T cell")),
    (re.compile(r"CD4", re.IGNORECASE), ("CD4-positive T cell", "CD4-positive alpha-beta T cell", "T cell")),
]


@dataclass
class CLTerm:
    cl_id: str
    name: str = ""
    definition: str = ""
    synonyms: list[str] = field(default_factory=list)
    parents: list[str] = field(default_factory=list)
    obsolete: bool = False


@dataclass
class Profile:
    profile_id: int
    paper_id: int
    collection: str
    organism: str
    group_name: str
    text_blob: str
    paper_context_blob: str
    gene_names: list[str]
    gene_ids: list[str]
    evidence_sentences: list[str]
    doi: str
    title: str
    year: int | None
    abstract: str


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_token_text(value: object) -> str:
    text = unicodedata.normalize("NFKD", clean_text(value)).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def tokens(value: object) -> set[str]:
    return {
        token
        for token in normalize_token_text(value).split()
        if token and token not in GENERIC_TOKENS and (len(token) >= 3 or token in {"b", "t", "nk", "cd4", "cd8"})
    }


def gene_symbols(profile: Profile) -> set[str]:
    symbols = set()
    for gene in profile.gene_names:
        for part in re.split(r"[/,;\s]+", gene):
            part = re.sub(r"[^A-Za-z0-9-]", "", part).upper()
            if part:
                symbols.add(part)
    return symbols


def parse_obo(path: Path) -> dict[str, CLTerm]:
    terms: dict[str, CLTerm] = {}
    current: CLTerm | None = None
    in_term = False

    def flush() -> None:
        nonlocal current
        if current and current.cl_id.startswith("CL:") and not current.obsolete:
            terms[current.cl_id] = current
        current = None

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line == "[Term]":
                flush()
                current = CLTerm(cl_id="")
                in_term = True
                continue
            if line.startswith("[") and line != "[Term]":
                flush()
                in_term = False
                continue
            if not in_term or current is None or not line:
                continue

            if line.startswith("id: "):
                current.cl_id = line.removeprefix("id: ").strip()
            elif line.startswith("name: "):
                current.name = line.removeprefix("name: ").strip()
            elif line.startswith("def: "):
                match = re.match(r'def: "(.+?)"', line)
                current.definition = match.group(1) if match else line.removeprefix("def: ").strip()
            elif line.startswith("synonym: "):
                match = re.match(r'synonym: "(.+?)"', line)
                if match:
                    current.synonyms.append(match.group(1))
            elif line.startswith("is_a: "):
                parent = line.removeprefix("is_a: ").split()[0]
                if parent.startswith("CL:"):
                    current.parents.append(parent)
            elif line == "is_obsolete: true":
                current.obsolete = True
    flush()
    return terms


def build_term_index(terms: dict[str, CLTerm]) -> dict[str, set[str]]:
    index: dict[str, set[str]] = defaultdict(set)
    for term in terms.values():
        fields = [term.name, term.definition, *term.synonyms]
        for field_text in fields:
            for token in tokens(field_text):
                index[token].add(term.cl_id)
    return index


def search_terms(
    query_text: str,
    *,
    terms: dict[str, CLTerm],
    index: dict[str, set[str]],
    limit: int = 40,
) -> list[CLTerm]:
    query_tokens = tokens(query_text)
    scores: dict[str, float] = defaultdict(float)
    for token in query_tokens:
        for cl_id in index.get(token, set()):
            scores[cl_id] += 1.0

    # Exact phrase/name boosts. Names beat synonyms; both beat definition token
    # matches. This avoids cases such as "macrophage" ranking below historical
    # synonym matches like plasmatocyte.
    query_norm = normalize_token_text(query_text)
    query_core = " ".join(token for token in query_norm.split() if not token.isdigit())
    query_variants = {variant for variant in (query_norm, query_core) if variant}
    for term in terms.values():
        name_norm = normalize_token_text(term.name)
        if name_norm in query_variants:
            scores[term.cl_id] += 30.0
        elif name_norm and any(name_norm in variant or variant in name_norm for variant in query_variants):
            scores[term.cl_id] += 10.0

        for synonym in term.synonyms:
            synonym_norm = normalize_token_text(synonym)
            if synonym_norm in query_variants:
                scores[term.cl_id] += 18.0
            elif synonym_norm and any(synonym_norm in variant or variant in synonym_norm for variant in query_variants):
                scores[term.cl_id] += 6.0

    ranked_ids = [
        cl_id
        for cl_id, _score in sorted(
            scores.items(),
            key=lambda item: (
                -item[1],
                len(terms[item[0]].name.split()),
                terms[item[0]].name,
                item[0],
            ),
        )[:limit]
    ]
    return [terms[cl_id] for cl_id in ranked_ids if cl_id in terms]


def marker_seed_terms(profile: Profile, *, terms: dict[str, CLTerm], index: dict[str, set[str]]) -> list[CLTerm]:
    profile_genes = gene_symbols(profile)
    phrases: list[str] = []
    for _program_name, marker_set, candidate_phrases in MARKER_PROGRAMS:
        if profile_genes & marker_set:
            phrases.extend(candidate_phrases)
    # Paper context can add tissue/disease but should not leak the reported label.
    context = f"{profile.title} {profile.abstract[:800]} {profile.paper_context_blob[:800]}"
    phrases.extend(sorted(tokens(context) & {"immune", "lymphocyte", "myeloid", "tumor", "cancer", "blood"}))

    seen = set()
    candidates = []
    for phrase in phrases:
        for term in search_terms(phrase, terms=terms, index=index, limit=12):
            if term.cl_id not in seen:
                seen.add(term.cl_id)
                candidates.append(term)
    return candidates[:50]


def label_seed_terms(profile: Profile, *, terms: dict[str, CLTerm], index: dict[str, set[str]]) -> list[CLTerm]:
    phrases: list[str] = []
    for pattern, expansions in LABEL_EXPANSIONS:
        if pattern.search(profile.group_name):
            phrases.extend(expansions)

    seen = set()
    candidates = []
    for phrase in phrases:
        for term in search_terms(phrase, terms=terms, index=index, limit=12):
            if term.cl_id not in seen:
                seen.add(term.cl_id)
                candidates.append(term)
    return candidates


def merge_candidates(*candidate_lists: Iterable[CLTerm], limit: int) -> list[CLTerm]:
    seen = set()
    merged = []
    for candidate_list in candidate_lists:
        for term in candidate_list:
            if term.cl_id in seen:
                continue
            seen.add(term.cl_id)
            merged.append(term)
            if len(merged) >= limit:
                return merged
    return merged


def load_profiles(
    db_path: Path,
    *,
    limit: int | None,
    immune_only: bool,
    profile_ids: set[int] | None = None,
) -> list[Profile]:
    query = """
        SELECT
            p.profile_id,
            p.paper_id,
            p.collection,
            p.organism,
            p.group_name,
            p.text_blob,
            p.paper_context_blob,
            p.gene_names_json,
            p.gene_ids_json,
            p.evidence_sentences_json,
            pa.doi,
            pa.title,
            pa.year,
            pa.abstract
        FROM profiles AS p
        JOIN papers AS pa ON pa.paper_id = p.paper_id
        WHERE p.organism = 'homo_sapiens'
          AND p.n_gene_ids >= 3
        ORDER BY p.paper_id, p.profile_id
    """
    profiles = []
    with sqlite3.connect(db_path) as conn:
        for row in conn.execute(query):
            profile = Profile(
                profile_id=int(row[0]),
                paper_id=int(row[1]),
                collection=clean_text(row[2]),
                organism=clean_text(row[3]),
                group_name=clean_text(row[4]),
                text_blob=clean_text(row[5]),
                paper_context_blob=clean_text(row[6]),
                gene_names=json.loads(row[7] or "[]"),
                gene_ids=json.loads(row[8] or "[]"),
                evidence_sentences=json.loads(row[9] or "[]"),
                doi=clean_text(row[10]),
                title=clean_text(row[11]),
                year=int(row[12]) if row[12] is not None else None,
                abstract=clean_text(row[13]),
            )
            if profile_ids is not None and profile.profile_id not in profile_ids:
                continue
            if immune_only:
                haystack = " ".join([profile.group_name, " ".join(profile.gene_names), profile.title, profile.text_blob[:500]])
                if not IMMUNE_LABEL_RE.search(haystack):
                    continue
            profiles.append(profile)
            if limit and len(profiles) >= limit:
                break
    return profiles


def profile_family(profile: Profile) -> str:
    label = profile.group_name.lower()
    genes = gene_symbols(profile)
    haystack = " ".join([label, " ".join(sorted(genes))]).lower()
    if "treg" in haystack or "regulatory" in haystack or {"FOXP3", "IL2RA", "CTLA4"} & genes:
        return "treg"
    if "exhaust" in haystack or "tex" in haystack or {"PDCD1", "HAVCR2", "LAG3", "TOX"} & genes:
        return "exhausted_t"
    if "naive" in haystack or "memory" in haystack or "tcm" in haystack or {"CCR7", "SELL", "TCF7", "LEF1"} & genes:
        return "naive_memory_t"
    if "cd4" in haystack or "cd8" in haystack or "t cell" in haystack or "t-cell" in haystack or {"CD3D", "CD3E", "TRAC"} & genes:
        return "other_t"
    if "macrophage" in haystack or "tam" in haystack or "trem2" in haystack or {"TREM2", "APOE", "C1QA", "SPP1"} & genes:
        return "macrophage"
    if "monocyte" in haystack or {"CD14", "FCN1", "S100A8", "S100A9"} & genes:
        return "monocyte"
    if re.search(r"\b(dendritic|c?dc[0-9]?|pdc)\b", haystack) or {"FCER1A", "CD1C", "CLEC9A", "LAMP3"} & genes:
        return "dendritic"
    if "nk" in haystack or "natural killer" in haystack or {"NKG7", "GNLY", "KLRD1"} & genes:
        return "nk"
    if "b cell" in haystack or "b-cell" in haystack or "plasma" in haystack or {"MS4A1", "CD79A", "JCHAIN", "MZB1"} & genes:
        return "b_plasma"
    if "neutrophil" in haystack or "mast" in haystack:
        return "other_immune"
    return "other"


def select_pilot_profiles(profiles: list[Profile], *, pilot_size: int, seed: int) -> list[Profile]:
    """Select a deterministic, balanced immune pilot.

    The pilot is meant to stress ontology consistency, not estimate corpus-wide
    rates. We therefore balance across immune families, then fill the remainder
    from the largest remaining families.
    """
    rng = random.Random(seed)
    by_family: dict[str, list[Profile]] = defaultdict(list)
    for profile in profiles:
        by_family[profile_family(profile)].append(profile)

    family_order = [
        "exhausted_t",
        "treg",
        "naive_memory_t",
        "other_t",
        "macrophage",
        "monocyte",
        "dendritic",
        "nk",
        "b_plasma",
        "other_immune",
        "other",
    ]
    for family_profiles in by_family.values():
        rng.shuffle(family_profiles)

    selected: list[Profile] = []
    selected_ids: set[int] = set()
    active_families = [family for family in family_order if by_family.get(family) and family != "other"]
    if not active_families:
        active_families = [family for family in family_order if by_family.get(family)]
    per_family = max(1, pilot_size // max(1, len(active_families)))

    for family in active_families:
        for profile in by_family[family][:per_family]:
            selected.append(profile)
            selected_ids.add(profile.profile_id)
            if len(selected) >= pilot_size:
                return sorted(selected, key=lambda profile: profile.profile_id)

    family_cursors = {family: per_family for family in active_families}
    while len(selected) < pilot_size:
        progressed = False
        for family in active_families:
            cursor = family_cursors[family]
            candidates = by_family[family]
            if cursor >= len(candidates):
                continue
            profile = candidates[cursor]
            family_cursors[family] += 1
            if profile.profile_id in selected_ids:
                continue
            selected.append(profile)
            selected_ids.add(profile.profile_id)
            progressed = True
            if len(selected) >= pilot_size:
                break
        if not progressed:
            if by_family.get("other") and "other" not in active_families:
                active_families.append("other")
                family_cursors["other"] = 0
                progressed = True
                continue
            break
    return sorted(selected, key=lambda profile: profile.profile_id)


def write_pilot_profiles(path: Path, profiles: list[Profile]) -> None:
    rows = []
    for profile in profiles:
        rows.append(
            {
                "profile_id": profile.profile_id,
                "paper_id": profile.paper_id,
                "collection": profile.collection,
                "family": profile_family(profile),
                "reported_label": profile.group_name,
                "n_genes": len(profile.gene_names),
                "gene_names": profile.gene_names,
                "doi": profile.doi,
                "title": profile.title,
                "year": profile.year,
            }
        )
    write_tsv(path, rows)


def candidate_payload(candidates: Iterable[CLTerm]) -> list[dict[str, object]]:
    payload = []
    for term in candidates:
        payload.append(
            {
                "cl_id": term.cl_id,
                "name": term.name,
                "definition": term.definition[:260],
                "synonyms": term.synonyms[:6],
                "parents": term.parents[:4],
            }
        )
    return payload


def extract_json(text: str) -> dict[str, object]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    decoder = json.JSONDecoder()
    start = text.find("{")
    if start == -1:
        raise json.JSONDecodeError("No JSON object found", text, 0)
    parsed, _end = decoder.raw_decode(text[start:])
    return parsed


def call_llm(prompt: str, *, model: str, max_tokens: int = 1000, timeout: float = 60.0) -> tuple[dict[str, object], dict[str, int]]:
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")
    client = anthropic.Anthropic(api_key=api_key, timeout=timeout, max_retries=2)
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}],
    )
    usage = getattr(message, "usage", None)
    usage_dict = {
        "input_tokens": int(getattr(usage, "input_tokens", 0) or 0),
        "output_tokens": int(getattr(usage, "output_tokens", 0) or 0),
        "cache_creation_input_tokens": int(getattr(usage, "cache_creation_input_tokens", 0) or 0),
        "cache_read_input_tokens": int(getattr(usage, "cache_read_input_tokens", 0) or 0),
    }
    return extract_json(message.content[0].text), usage_dict


def infer_price_rates(model: str) -> dict[str, float]:
    model_lower = model.lower()
    for key, rates in MODEL_PRICE_PER_MTOK.items():
        if key in model_lower:
            return rates
    return MODEL_PRICE_PER_MTOK["sonnet"]


def estimate_cost_usd(usage: dict[str, int], rates: dict[str, float]) -> float:
    cost = 0.0
    cost += usage.get("input_tokens", 0) * rates["input"] / 1_000_000
    cost += usage.get("output_tokens", 0) * rates["output"] / 1_000_000
    cost += usage.get("cache_creation_input_tokens", 0) * rates["cache_creation"] / 1_000_000
    cost += usage.get("cache_read_input_tokens", 0) * rates["cache_read"] / 1_000_000
    return cost


def add_cost_fields(mapping: dict[str, object], usage: dict[str, int], rates: dict[str, float]) -> dict[str, object]:
    cost = estimate_cost_usd(usage, rates)
    mapping.update(
        {
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "cache_creation_input_tokens": usage.get("cache_creation_input_tokens", 0),
            "cache_read_input_tokens": usage.get("cache_read_input_tokens", 0),
            "total_billed_tokens": sum(usage.values()),
            "estimated_cost_usd": round(cost, 8),
            "input_price_per_mtok": rates["input"],
            "output_price_per_mtok": rates["output"],
            "cache_creation_price_per_mtok": rates["cache_creation"],
            "cache_read_price_per_mtok": rates["cache_read"],
        }
    )
    return mapping


def build_prompt(profile: Profile, basis: str, candidates: list[CLTerm]) -> str:
    if basis == "full_context":
        evidence = {
            "reported_label": profile.group_name,
            "paper_title": profile.title,
            "paper_abstract": profile.abstract[:1000],
            "source_sentences": profile.evidence_sentences[:3],
            "marker_genes": profile.gene_names[:40],
        }
    elif basis == "label_context":
        evidence = {
            "reported_label": profile.group_name,
            "paper_title": profile.title,
            "paper_abstract": profile.abstract[:1000],
            "source_sentences": profile.evidence_sentences[:3],
            "marker_genes": "HIDDEN",
        }
    elif basis == "marker_context":
        evidence = {
            "reported_label": "HIDDEN",
            "paper_title": profile.title,
            "paper_abstract": profile.abstract[:1000],
            "marker_genes": profile.gene_names[:40],
            "source_sentences": [],
        }
    else:
        raise ValueError(f"unknown basis: {basis}")

    return textwrap.dedent(
        f"""
        Map one marker profile to one Cell Ontology term.

        Choose only from the candidate_terms list. If no candidate is justified,
        return cl_id=null and cl_label=null. Do not invent ontology IDs.

        basis: {basis}
        profile_id: {profile.profile_id}
        evidence:
        {json.dumps(evidence, indent=2)}

        candidate_terms:
        {json.dumps(candidate_payload(candidates), indent=2)}

        Return only JSON with this schema:
        {{
          "profile_id": {profile.profile_id},
          "basis": "{basis}",
          "cl_id": "CL:0000000 or null",
          "cl_label": "candidate term name or null",
          "confidence": "high|medium|low|unmapped",
          "mapping_relation": "exact|broad|narrow|related|unmapped",
          "rationale": "one short sentence",
          "alternative_ids": ["CL:..."]
        }}
        """
    ).strip()


def ensure_valid_mapping(mapping: dict[str, object], *, candidates: list[CLTerm], profile: Profile, basis: str) -> dict[str, object]:
    valid_ids = {term.cl_id: term for term in candidates}
    cl_id = mapping.get("cl_id")
    if cl_id is not None and cl_id not in valid_ids:
        cl_id = None
    term = valid_ids.get(cl_id) if cl_id else None
    confidence = clean_text(mapping.get("confidence")) if term else "unmapped"
    mapping_relation = clean_text(mapping.get("mapping_relation")) if term else "unmapped"
    return {
        "profile_id": profile.profile_id,
        "paper_id": profile.paper_id,
        "collection": profile.collection,
        "doi": profile.doi,
        "title": profile.title,
        "year": profile.year,
        "reported_label": profile.group_name,
        "gene_names": profile.gene_names,
        "basis": basis,
        "cl_id": term.cl_id if term else None,
        "cl_label": term.name if term else None,
        "confidence": confidence,
        "mapping_relation": mapping_relation,
        "rationale": clean_text(mapping.get("rationale")),
        "alternative_ids": [alt for alt in mapping.get("alternative_ids", []) if alt in valid_ids],
        "candidate_ids": [candidate.cl_id for candidate in candidates],
        "candidate_labels": [candidate.name for candidate in candidates],
    }


def ancestor_distances(cl_id: str | None, terms: dict[str, CLTerm]) -> dict[str, int]:
    if not cl_id or cl_id not in terms:
        return {}
    distances = {cl_id: 0}
    queue = deque([cl_id])
    while queue:
        current = queue.popleft()
        for parent in terms[current].parents:
            if parent in terms and parent not in distances:
                distances[parent] = distances[current] + 1
                queue.append(parent)
    return distances


def compare_terms(label_id: str | None, marker_id: str | None, terms: dict[str, CLTerm]) -> tuple[str, str | None, str | None]:
    if not label_id and not marker_id:
        return "both_unmapped", None, None
    if not label_id:
        return "label_unmapped", None, None
    if not marker_id:
        return "marker_unmapped", None, None
    if label_id == marker_id:
        return "same_term", label_id, terms[label_id].name

    label_anc = ancestor_distances(label_id, terms)
    marker_anc = ancestor_distances(marker_id, terms)
    if marker_id in label_anc:
        return "marker_is_ancestor", marker_id, terms[marker_id].name
    if label_id in marker_anc:
        return "marker_is_descendant", label_id, terms[label_id].name

    shared = set(label_anc) & set(marker_anc)
    if not shared:
        return "different_branch", None, None
    shared_parent = min(shared, key=lambda cl_id: label_anc[cl_id] + marker_anc[cl_id])
    if shared_parent == "CL:0000000":
        return "different_branch", shared_parent, terms[shared_parent].name
    return "shared_parent", shared_parent, terms[shared_parent].name


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def append_jsonl(path: Path, row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")
        handle.flush()


def load_jsonl(path: Path) -> list[dict[str, object]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys, delimiter="\t")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value) if isinstance(value, (list, dict)) else value for key, value in row.items()})


def compare_mappings(
    mappings: list[dict[str, object]],
    terms: dict[str, CLTerm],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    by_profile: dict[int, dict[str, dict[str, object]]] = defaultdict(dict)
    for row in mappings:
        by_profile[int(row["profile_id"])][str(row["basis"])] = row

    comparison_rows = []
    ablation_rows = []
    for profile_id, basis_rows in sorted(by_profile.items()):
        full_row = basis_rows.get("full_context")
        label_row = basis_rows.get("label_context")
        marker_row = basis_rows.get("marker_context")
        if not label_row or not marker_row:
            continue
        relation, common_id, common_label = compare_terms(label_row.get("cl_id"), marker_row.get("cl_id"), terms)
        comparison_rows.append(
            {
                "profile_id": profile_id,
                "paper_id": label_row["paper_id"],
                "collection": label_row["collection"],
                "reported_label": label_row["reported_label"],
                "gene_names": label_row["gene_names"],
                "label_cl_id": label_row.get("cl_id"),
                "label_cl_label": label_row.get("cl_label"),
                "label_confidence": label_row.get("confidence"),
                "marker_cl_id": marker_row.get("cl_id"),
                "marker_cl_label": marker_row.get("cl_label"),
                "marker_confidence": marker_row.get("confidence"),
                "ontology_relation": relation,
                "common_cl_id": common_id,
                "common_cl_label": common_label,
                "label_rationale": label_row.get("rationale"),
                "marker_rationale": marker_row.get("rationale"),
                "doi": label_row.get("doi"),
                "title": label_row.get("title"),
                "year": label_row.get("year"),
            }
        )
        if full_row:
            for ablation_name, ablation_row in (("label_context", label_row), ("marker_context", marker_row)):
                ablation_relation, ablation_common_id, ablation_common_label = compare_terms(
                    full_row.get("cl_id"),
                    ablation_row.get("cl_id"),
                    terms,
                )
                ablation_rows.append(
                    {
                        "profile_id": profile_id,
                        "paper_id": full_row["paper_id"],
                        "collection": full_row["collection"],
                        "reported_label": full_row["reported_label"],
                        "gene_names": full_row["gene_names"],
                        "ablation": ablation_name,
                        "full_cl_id": full_row.get("cl_id"),
                        "full_cl_label": full_row.get("cl_label"),
                        "full_confidence": full_row.get("confidence"),
                        "ablation_cl_id": ablation_row.get("cl_id"),
                        "ablation_cl_label": ablation_row.get("cl_label"),
                        "ablation_confidence": ablation_row.get("confidence"),
                        "ablation_relation_to_full": ablation_relation,
                        "common_cl_id": ablation_common_id,
                        "common_cl_label": ablation_common_label,
                        "full_rationale": full_row.get("rationale"),
                        "ablation_rationale": ablation_row.get("rationale"),
                        "doi": full_row.get("doi"),
                        "title": full_row.get("title"),
                        "year": full_row.get("year"),
                    }
                )

    relation_counts = Counter(row["ontology_relation"] for row in comparison_rows)
    summary_rows = []
    total = sum(relation_counts.values())
    for relation, count in sorted(relation_counts.items()):
        summary_rows.append(
            {
                "ontology_relation": relation,
                "n_profiles": count,
                "fraction": count / total if total else 0.0,
            }
        )
    for ablation_name in ("label_context", "marker_context"):
        ablation_counts = Counter(
            row["ablation_relation_to_full"]
            for row in ablation_rows
            if row["ablation"] == ablation_name
        )
        ablation_total = sum(ablation_counts.values())
        for relation, count in sorted(ablation_counts.items()):
            summary_rows.append(
                {
                    "ontology_relation": f"{ablation_name}_vs_full:{relation}",
                    "n_profiles": count,
                    "fraction": count / ablation_total if ablation_total else 0.0,
                }
            )
    return comparison_rows, summary_rows, ablation_rows


def summarize_costs(mappings: list[dict[str, object]]) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    groups["all"] = mappings
    for row in mappings:
        groups[str(row.get("basis", "unknown"))].append(row)

    rows = []
    for group_name, group_rows in sorted(groups.items()):
        n_calls = len(group_rows)
        total_cost = sum(float(row.get("estimated_cost_usd") or 0.0) for row in group_rows)
        input_tokens = sum(int(row.get("input_tokens") or 0) for row in group_rows)
        output_tokens = sum(int(row.get("output_tokens") or 0) for row in group_rows)
        cache_creation = sum(int(row.get("cache_creation_input_tokens") or 0) for row in group_rows)
        cache_read = sum(int(row.get("cache_read_input_tokens") or 0) for row in group_rows)
        profile_ids = {row.get("profile_id") for row in group_rows}
        rows.append(
            {
                "group": group_name,
                "n_calls": n_calls,
                "n_profiles": len(profile_ids),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cache_creation_input_tokens": cache_creation,
                "cache_read_input_tokens": cache_read,
                "estimated_cost_usd": round(total_cost, 6),
                "estimated_cost_per_profile_usd": round(total_cost / len(profile_ids), 6) if profile_ids else 0.0,
                "estimated_cost_per_call_usd": round(total_cost / n_calls, 6) if n_calls else 0.0,
            }
        )
    return rows


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--ontology", type=Path, default=DEFAULT_ONTOLOGY)
    parser.add_argument("--out", type=Path, default=DEFAULT_MAPPINGS)
    parser.add_argument("--comparison-out", type=Path, default=DEFAULT_COMPARISON)
    parser.add_argument("--summary-out", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--ablation-out", type=Path, default=DEFAULT_ABLATION)
    parser.add_argument("--cost-out", type=Path, default=DEFAULT_COSTS)
    parser.add_argument("--pilot-out", type=Path, default=DEFAULT_PILOT)
    parser.add_argument("--env-file", type=Path, default=REPO_ROOT.parent / "mrkr" / ".env")
    parser.add_argument("--model", default=None)
    parser.add_argument("--limit", type=int, default=24)
    parser.add_argument("--pilot-size", type=int, default=None, help="Select a deterministic, balanced immune pilot of this size.")
    parser.add_argument("--pilot-seed", type=int, default=7)
    parser.add_argument(
        "--profile-ids",
        default="",
        help="Comma-separated profile IDs. When provided, these profiles are mapped instead of the first --limit profiles.",
    )
    parser.add_argument("--candidate-limit", type=int, default=40)
    parser.add_argument("--input-price-per-mtok", type=float, default=None)
    parser.add_argument("--output-price-per-mtok", type=float, default=None)
    parser.add_argument("--cache-creation-price-per-mtok", type=float, default=None)
    parser.add_argument("--cache-read-price-per-mtok", type=float, default=None)
    parser.add_argument("--request-timeout", type=float, default=60.0)
    parser.add_argument("--immune-only", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--download-ontology", action="store_true", help=f"Download CL basic OBO from {CL_BASIC_URL} if --ontology is missing")
    parser.add_argument("--reuse", action="store_true", help="Reuse existing mapping JSONL and only rebuild comparison files")
    parser.add_argument("--resume-partial", action="store_true", help="Load existing rows from --out and skip already completed profile/basis pairs.")
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if not args.ontology.exists():
        if args.download_ontology:
            args.ontology.parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(CL_BASIC_URL, args.ontology)
        else:
            args.ontology.parent.mkdir(parents=True, exist_ok=True)
            raise FileNotFoundError(
                f"Cell Ontology OBO not found: {args.ontology}\n"
                f"Download with: curl -fsSL -o {args.ontology} {CL_BASIC_URL}\n"
                f"or rerun with --download-ontology"
            )

    terms = parse_obo(args.ontology)
    index = build_term_index(terms)

    if args.reuse:
        mappings = load_jsonl(args.out)
        mapping_status = "Read mappings"
    else:
        load_env_file(args.env_file)
        model = args.model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
        rates = dict(infer_price_rates(model))
        if args.input_price_per_mtok is not None:
            rates["input"] = args.input_price_per_mtok
        if args.output_price_per_mtok is not None:
            rates["output"] = args.output_price_per_mtok
        if args.cache_creation_price_per_mtok is not None:
            rates["cache_creation"] = args.cache_creation_price_per_mtok
        if args.cache_read_price_per_mtok is not None:
            rates["cache_read"] = args.cache_read_price_per_mtok
        profile_ids = {int(value) for value in re.split(r"[,\\s]+", args.profile_ids.strip()) if value} or None
        profiles = load_profiles(
            args.db,
            limit=None if profile_ids or args.pilot_size else args.limit,
            immune_only=args.immune_only,
            profile_ids=profile_ids,
        )
        if args.pilot_size and profile_ids is None:
            profiles = select_pilot_profiles(profiles, pilot_size=args.pilot_size, seed=args.pilot_seed)
        write_pilot_profiles(args.pilot_out, profiles)
        mappings = load_jsonl(args.out) if args.resume_partial and args.out.exists() else []
        completed = {(int(row["profile_id"]), str(row["basis"])) for row in mappings}
        if not args.resume_partial and args.out.exists():
            args.out.unlink()
        for profile in profiles:
            label_candidates = merge_candidates(
                label_seed_terms(profile, terms=terms, index=index),
                search_terms(profile.group_name, terms=terms, index=index, limit=args.candidate_limit),
                marker_seed_terms(profile, terms=terms, index=index),
                search_terms(
                    f"{profile.title} {profile.abstract[:500]} {profile.text_blob[:500]}",
                    terms=terms,
                    index=index,
                    limit=args.candidate_limit,
                ),
                limit=args.candidate_limit,
            )
            marker_candidates = marker_seed_terms(profile, terms=terms, index=index)[: args.candidate_limit]

            full_candidates = merge_candidates(label_candidates, marker_candidates, limit=args.candidate_limit)

            for basis, candidates in (
                ("full_context", full_candidates),
                ("label_context", label_candidates),
                ("marker_context", marker_candidates),
            ):
                if (profile.profile_id, basis) in completed:
                    continue
                usage = {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cache_creation_input_tokens": 0,
                    "cache_read_input_tokens": 0,
                }
                if args.dry_run:
                    mapping = {
                        "profile_id": profile.profile_id,
                        "paper_id": profile.paper_id,
                        "collection": profile.collection,
                        "doi": profile.doi,
                        "title": profile.title,
                        "year": profile.year,
                        "reported_label": profile.group_name,
                        "gene_names": profile.gene_names,
                        "basis": basis,
                        "cl_id": candidates[0].cl_id if candidates else None,
                        "cl_label": candidates[0].name if candidates else None,
                        "confidence": "candidate_preview" if candidates else "unmapped",
                        "mapping_relation": "candidate_preview" if candidates else "unmapped",
                        "rationale": "dry run candidate preview",
                        "alternative_ids": [],
                        "candidate_ids": [candidate.cl_id for candidate in candidates],
                        "candidate_labels": [candidate.name for candidate in candidates],
                    }
                else:
                    if not candidates:
                        raw_mapping = {
                            "cl_id": None,
                            "confidence": "unmapped",
                            "mapping_relation": "unmapped",
                            "rationale": "No candidate Cell Ontology terms were retrieved.",
                            "alternative_ids": [],
                        }
                        mapping = ensure_valid_mapping(raw_mapping, candidates=candidates, profile=profile, basis=basis)
                    else:
                        prompt = build_prompt(profile, basis, candidates)
                        raw_mapping, usage = call_llm(prompt, model=model, timeout=args.request_timeout)
                        mapping = ensure_valid_mapping(raw_mapping, candidates=candidates, profile=profile, basis=basis)
                mapping = add_cost_fields(mapping, usage, rates)
                mapping["model"] = model if not args.dry_run else "dry_run"
                mapping["ontology_file"] = str(args.ontology)
                mappings.append(mapping)
                append_jsonl(args.out, mapping)
                completed.add((profile.profile_id, basis))
                print(
                    f"{basis}\tprofile={profile.profile_id}\tlabel={profile.group_name}\t"
                    f"mapped={mapping.get('cl_id')} {mapping.get('cl_label')}",
                    flush=True,
                )

        write_jsonl(args.out, mappings)
        mapping_status = "Wrote mappings"

    comparison_rows, summary_rows, ablation_rows = compare_mappings(mappings, terms)
    write_tsv(args.comparison_out, comparison_rows)
    write_tsv(args.summary_out, summary_rows)
    write_tsv(args.ablation_out, ablation_rows)
    write_tsv(args.cost_out, summarize_costs(mappings))
    print(f"{mapping_status}: {args.out}")
    print(f"Wrote comparison: {args.comparison_out}")
    print(f"Wrote ablation: {args.ablation_out}")
    print(f"Wrote summary: {args.summary_out}")
    print(f"Wrote costs: {args.cost_out}")


if __name__ == "__main__":
    main()
