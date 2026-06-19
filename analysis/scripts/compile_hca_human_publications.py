#!/usr/bin/env python3
"""Compile HCA human-study publication links from the Azul projects index.

Outputs:
  - docs/hca/hca_human_project_publications.tsv
  - docs/hca/hca_human_manuscript_urls.tsv

The raw table keeps one row per (project, publication) association.
The deduplicated table collapses publications across projects, preferring:
  1. PMC-like full-text URLs
  2. DOI URLs synthesized from the DOI field
  3. cleaned publication URLs from HCA metadata
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit


API_URL = "https://service.azul.data.humancellatlas.org/index/projects?size=75"
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>]+", re.IGNORECASE)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None

    raw = normalize_text(value)
    if not raw:
        return None

    lower = raw.lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if lower.startswith(prefix):
            raw = raw[len(prefix):]
            lower = raw.lower()
            break

    match = DOI_RE.search(raw)
    if match:
        return match.group(0).rstrip(". )]").lower()

    if raw.startswith("10."):
        return raw.rstrip(". )]").lower()

    return None


def clean_url(value: str | None) -> str | None:
    raw = normalize_text(value)
    if not raw:
        return None

    parts = urlsplit(raw)
    if not parts.scheme or not parts.netloc:
        return raw

    path = parts.path or ""
    cleaned = urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, "", ""))
    return cleaned.rstrip("/") if path not in ("", "/") else cleaned


def classify_url(url: str | None) -> str:
    if not url:
        return "none"

    low = url.lower()
    if "pmc/articles" in low or "pmc.ncbi.nlm.nih.gov" in low:
        return "pmc"
    if "pubmed" in low or "ncbi.nlm.nih.gov/pubmed" in low:
        return "pubmed"
    if "doi.org/" in low:
        return "doi"
    return "publisher"


def canonical_doi_url(doi: str | None) -> str | None:
    if not doi:
        return None
    return f"https://doi.org/{doi}"


def walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for child in value.values():
            strings.extend(walk_strings(child))
        return strings
    if isinstance(value, list):
        strings: list[str] = []
        for child in value:
            strings.extend(walk_strings(child))
        return strings
    return []


def hit_is_human(hit: dict[str, Any]) -> bool:
    return any(text.strip().lower() == "homo sapiens" for text in walk_strings(hit))


def split_supplementary_links(values: list[Any] | None) -> list[str]:
    links: list[str] = []
    for value in values or []:
        text = normalize_text(value)
        if not text:
            continue
        parts = [part.strip() for part in text.split(";")]
        links.extend(part for part in parts if part)
    return sorted(set(links))


def encode_accessions(values: list[dict[str, Any]] | None) -> list[str]:
    accessions = []
    for accession in values or []:
        namespace = normalize_text(accession.get("namespace"))
        code = normalize_text(accession.get("accession"))
        if not namespace and not code:
            continue
        accessions.append(f"{namespace}:{code}" if namespace else code)
    return sorted(set(accessions))


def normalize_title_key(title: str | None) -> str | None:
    text = normalize_text(title)
    if not text:
        return None
    return re.sub(r"\s+", " ", text).strip().lower()


def fetch_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "llmarkers-hca-harvester/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


def choose_preferred_url(
    doi_values: set[str],
    publication_urls: set[str],
) -> tuple[str | None, str]:
    pmc_urls = sorted(url for url in publication_urls if classify_url(url) == "pmc")
    if pmc_urls:
        return pmc_urls[0], "pmc"

    if doi_values:
        return canonical_doi_url(sorted(doi_values)[0]), "doi"

    if publication_urls:
        first = sorted(publication_urls)[0]
        return first, classify_url(first)

    return None, "none"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("docs/hca"),
        help="Directory for TSV outputs.",
    )
    args = parser.parse_args()

    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    raw_path = outdir / "hca_human_project_publications.tsv"
    dedup_path = outdir / "hca_human_manuscript_urls.tsv"
    missing_path = outdir / "hca_human_publications_missing_urls.tsv"

    hits: list[dict[str, Any]] = []
    next_url: str | None = API_URL
    while next_url:
        page = fetch_json(next_url)
        hits.extend(page["hits"])
        next_url = page["pagination"].get("next")

    total_projects = len(hits)
    human_hits = [hit for hit in hits if hit_is_human(hit)]

    raw_rows: list[dict[str, str]] = []
    dedup: dict[str, dict[str, Any]] = {}
    dedup_order = 0

    for hit in human_hits:
        for project in hit.get("projects", []):
            project_id = normalize_text(project.get("projectId"))
            project_title = normalize_text(project.get("projectTitle"))
            supplementary_links = split_supplementary_links(project.get("supplementaryLinks"))
            accessions = encode_accessions(project.get("accessions"))
            publications = project.get("publications") or []
            for publication in publications:
                if not isinstance(publication, dict):
                    continue

                title = normalize_text(publication.get("publicationTitle"))
                raw_url = clean_url(publication.get("publicationUrl"))
                doi = normalize_doi(publication.get("doi") or publication.get("publicationUrl"))
                doi_url = canonical_doi_url(doi)
                official = bool(publication.get("officialHcaPublication"))

                dedup_key = (
                    f"doi:{doi}"
                    if doi
                    else f"url:{raw_url}"
                    if raw_url
                    else f"title:{normalize_title_key(title)}"
                )
                if dedup_key.endswith("None"):
                    continue

                raw_rows.append(
                    {
                        "project_id": project_id,
                        "project_title": project_title,
                        "publication_title": title,
                        "doi": doi or "",
                        "doi_url": doi_url or "",
                        "publication_url": raw_url or "",
                        "publication_url_type": classify_url(raw_url),
                        "official_hca_publication": "true" if official else "false",
                        "accessions": "|".join(accessions),
                        "supplementary_links": "|".join(supplementary_links),
                    }
                )

                if dedup_key not in dedup:
                    dedup_order += 1
                    dedup[dedup_key] = {
                        "order": dedup_order,
                        "titles": [],
                        "doi_values": set(),
                        "publication_urls": set(),
                        "project_ids": set(),
                        "project_titles": set(),
                        "supplementary_links": set(),
                        "accessions": set(),
                        "official_hca_publication_any": False,
                    }

                record = dedup[dedup_key]
                if title:
                    record["titles"].append(title)
                if doi:
                    record["doi_values"].add(doi)
                if raw_url:
                    record["publication_urls"].add(raw_url)
                record["project_ids"].add(project_id)
                record["project_titles"].add(project_title)
                record["supplementary_links"].update(supplementary_links)
                record["accessions"].update(accessions)
                record["official_hca_publication_any"] = (
                    record["official_hca_publication_any"] or official
                )

    raw_rows.sort(key=lambda row: (row["project_title"], row["publication_title"], row["doi"]))

    dedup_rows_all: list[dict[str, str]] = []
    for key, record in sorted(dedup.items(), key=lambda item: item[1]["order"]):
        title = max(record["titles"], key=len) if record["titles"] else ""
        preferred_url, preferred_url_type = choose_preferred_url(
            record["doi_values"],
            record["publication_urls"],
        )
        dedup_rows_all.append(
            {
                "dedup_key": key,
                "publication_title": title,
                "preferred_url": preferred_url or "",
                "preferred_url_type": preferred_url_type,
                "doi": sorted(record["doi_values"])[0] if record["doi_values"] else "",
                "doi_url": canonical_doi_url(sorted(record["doi_values"])[0])
                if record["doi_values"]
                else "",
                "publication_urls": "|".join(sorted(record["publication_urls"])),
                "official_hca_publication_any": "true"
                if record["official_hca_publication_any"]
                else "false",
                "project_count": str(len(record["project_ids"])),
                "project_ids": "|".join(sorted(record["project_ids"])),
                "project_titles": "|".join(sorted(record["project_titles"])),
                "accessions": "|".join(sorted(record["accessions"])),
                "supplementary_links": "|".join(sorted(record["supplementary_links"])),
            }
        )

    dedup_rows = [row for row in dedup_rows_all if row["preferred_url"]]
    missing_rows = [row for row in dedup_rows_all if not row["preferred_url"]]

    with raw_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "project_id",
                "project_title",
                "publication_title",
                "doi",
                "doi_url",
                "publication_url",
                "publication_url_type",
                "official_hca_publication",
                "accessions",
                "supplementary_links",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(raw_rows)

    with dedup_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "dedup_key",
                "publication_title",
                "preferred_url",
                "preferred_url_type",
                "doi",
                "doi_url",
                "publication_urls",
                "official_hca_publication_any",
                "project_count",
                "project_ids",
                "project_titles",
                "accessions",
                "supplementary_links",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(dedup_rows)

    with missing_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "dedup_key",
                "publication_title",
                "preferred_url",
                "preferred_url_type",
                "doi",
                "doi_url",
                "publication_urls",
                "official_hca_publication_any",
                "project_count",
                "project_ids",
                "project_titles",
                "accessions",
                "supplementary_links",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(missing_rows)

    summary = Counter()
    summary["total_projects"] = total_projects
    summary["human_projects"] = len(human_hits)
    summary["raw_project_publication_rows"] = len(raw_rows)
    summary["deduplicated_manuscripts"] = len(dedup_rows_all)
    summary["deduplicated_manuscripts_with_url"] = len(dedup_rows)
    summary["deduplicated_manuscripts_missing_url"] = len(missing_rows)
    for row in dedup_rows:
        summary[f"preferred_{row['preferred_url_type']}"] += 1
        if row["preferred_url"]:
            summary["with_preferred_url"] += 1

    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"Wrote {raw_path}")
    print(f"Wrote {dedup_path}")
    print(f"Wrote {missing_path}")


if __name__ == "__main__":
    main()
