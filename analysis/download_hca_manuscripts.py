#!/usr/bin/env python3
"""Resolve HCA manuscript URLs into cached plain-text manuscripts.

Input:
  - docs/hca/hca_human_manuscript_urls.tsv

Output per paper:
  - metadata.json
  - resolution.json
  - manuscript.md
  - manuscript.xml / manuscript.html / manuscript.pdf (when available)

The resolver prefers machine-readable full text when possible:
  1. Europe PMC XML for PMC-backed articles
  2. direct publisher / DOI landing pages
  3. Unpaywall OA links (optional; requires --email)
  4. Crossref text-and-data-mining links
  5. PDF fallback
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


INPUT_TSV = Path("docs/hca/hca_human_manuscript_urls.tsv")
DEFAULT_OUTDIR = Path("data/hca/manuscripts")
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0 Safari/537.36"
)
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>]+", re.IGNORECASE)
PMCID_RE = re.compile(r"(PMC\d+)", re.IGNORECASE)
XML_MIME_HINTS = (
    "xml",
    "jats",
)
HTML_MIME_HINTS = (
    "html",
    "xhtml",
)
PDF_MIME_HINTS = (
    "pdf",
    "octet-stream",
)
MIN_TEXT_CHARS = 300
MIN_TEXT_WORDS = 40
TITLE_STOPWORDS = {
    "the",
    "and",
    "with",
    "from",
    "into",
    "using",
    "through",
    "that",
    "this",
    "these",
    "those",
    "their",
    "reveal",
    "reveals",
    "revealing",
    "single",
    "cell",
    "cells",
    "human",
    "study",
    "analysis",
    "atlas",
    "protocol",
}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


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


def split_pipe_values(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def folder_name(index: int, row: dict[str, str]) -> str:
    base = row.get("doi") or row.get("dedup_key") or row.get("publication_title") or f"paper-{index:04d}"
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", base).strip("._-")
    safe = safe[:80] if safe else f"paper-{index:04d}"
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:10]
    return f"{index:04d}_{safe}_{digest}"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def guess_charset(content_type: str | None) -> str:
    if not content_type:
        return "utf-8"
    match = re.search(r"charset=([A-Za-z0-9._-]+)", content_type, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    return "utf-8"


def fetch_url(url: str, *, accept: str | None = None, timeout: int = 90) -> dict[str, Any]:
    headers = {"User-Agent": USER_AGENT}
    if accept:
        headers["Accept"] = accept

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return {
            "requested_url": url,
            "final_url": response.geturl(),
            "content_type": response.headers.get("Content-Type", ""),
            "content_length": response.headers.get("Content-Length", ""),
            "data": response.read(),
        }


def fetch_json(url: str, *, timeout: int = 90) -> dict[str, Any]:
    response = fetch_url(url, accept="application/json", timeout=timeout)
    charset = guess_charset(response.get("content_type"))
    text = response["data"].decode(charset, errors="replace")
    payload = json.loads(text)
    return payload if isinstance(payload, dict) else {}


def parse_pmcid(value: str | None) -> str | None:
    if not value:
        return None
    match = PMCID_RE.search(value)
    return match.group(1).upper() if match else None


def strip_xml_namespaces(root: ET.Element) -> None:
    for node in root.iter():
        if isinstance(node.tag, str) and "}" in node.tag:
            node.tag = node.tag.split("}", 1)[1]


def normalize_lines(lines: list[str]) -> str:
    normalized: list[str] = []
    previous = ""
    for raw_line in lines:
        line = normalize_space(unescape(raw_line))
        if not line:
            continue
        if line == previous:
            continue
        normalized.append(line)
        previous = line
    return "\n".join(normalized).strip()


def is_usable_text(text: str) -> bool:
    if len(text) < MIN_TEXT_CHARS:
        return False
    if len(text.split()) < MIN_TEXT_WORDS:
        return False
    return True


def title_keywords(title: str | None) -> list[str]:
    if not title:
        return []
    tokens = re.findall(r"[A-Za-z0-9]+", title.lower())
    return [token for token in tokens if len(token) >= 4 and token not in TITLE_STOPWORDS]


def text_matches_title(text: str, title: str | None) -> bool:
    keywords = title_keywords(title)
    if not keywords:
        return True
    haystack = text.lower()
    hits = sum(1 for token in keywords if token in haystack)
    threshold = 2 if len(keywords) >= 2 else 1
    return hits >= threshold


def extract_xml_text(data: bytes) -> str:
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return ""

    strip_xml_namespaces(root)
    lines: list[str] = []

    title_node = root.find(".//title-group/article-title")
    if title_node is None:
        title_node = root.find(".//article-title")
    if title_node is not None:
        title = normalize_space(" ".join(title_node.itertext()))
        if title:
            lines.append(title)

    for abstract in root.findall(".//abstract"):
        for node in abstract.iter():
            if node.tag in {"title", "p", "label", "li"}:
                text = normalize_space(" ".join(node.itertext()))
                if text:
                    lines.append(text)

    body = root.find(".//body")
    search_root = body if body is not None else root
    for node in search_root.iter():
        if node.tag in {"sec", "fig", "table-wrap"}:
            continue
        if node.tag in {"title", "p", "label", "li"}:
            text = normalize_space(" ".join(node.itertext()))
            if text:
                lines.append(text)

    return normalize_lines(lines)


class VisibleHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ignore_depth = 0
        self.current: list[str] = []
        self.lines: list[str] = []
        self.in_title = False
        self.title_parts: list[str] = []

    def flush(self) -> None:
        text = normalize_space(" ".join(self.current))
        if text:
            self.lines.append(text)
        self.current = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript", "svg", "math", "iframe", "canvas"}:
            self.ignore_depth += 1
            return
        if tag == "title":
            self.in_title = True
        if tag in {
            "p",
            "div",
            "section",
            "article",
            "main",
            "header",
            "footer",
            "aside",
            "nav",
            "li",
            "br",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "tr",
        }:
            self.flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg", "math", "iframe", "canvas"}:
            self.ignore_depth = max(0, self.ignore_depth - 1)
            return
        if tag == "title":
            self.in_title = False
        if tag in {
            "p",
            "div",
            "section",
            "article",
            "main",
            "header",
            "footer",
            "aside",
            "nav",
            "li",
            "br",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "tr",
        }:
            self.flush()

    def handle_data(self, data: str) -> None:
        if self.ignore_depth:
            return
        if self.in_title:
            self.title_parts.append(data)
        self.current.append(data)


def extract_html_text(data: bytes, content_type: str | None) -> str:
    charset = guess_charset(content_type)
    text = data.decode(charset, errors="replace")
    parser = VisibleHTMLParser()
    parser.feed(text)
    parser.flush()

    lines = parser.lines
    title = normalize_space(" ".join(parser.title_parts))
    if title:
        lines = [title] + lines

    filtered: list[str] = []
    for line in lines:
        low = line.lower()
        if low in {
            "download pdf",
            "show authors",
            "metrics details",
            "article",
            "open access",
        }:
            continue
        filtered.append(line)
    return normalize_lines(filtered)


def looks_like_xml(content_type: str, data: bytes) -> bool:
    low = content_type.lower()
    if any(token in low for token in XML_MIME_HINTS):
        return True
    prefix = data[:128].lstrip()
    return prefix.startswith(b"<?xml") or prefix.startswith(b"<article") or prefix.startswith(b"<pmc-articleset")


def looks_like_html(content_type: str, data: bytes) -> bool:
    low = content_type.lower()
    if any(token in low for token in HTML_MIME_HINTS):
        return True
    prefix = data[:256].lstrip().lower()
    return prefix.startswith(b"<!doctype html") or prefix.startswith(b"<html")


def looks_like_pdf(content_type: str, data: bytes) -> bool:
    low = content_type.lower()
    if "pdf" in low:
        return True
    if "octet-stream" in low and data[:4] == b"%PDF":
        return True
    return data[:4] == b"%PDF"


def extract_pdf_text(pdf_path: Path) -> str:
    tool = shutil.which("pdftotext")
    if tool is None:
        return ""

    out_path = pdf_path.with_suffix(".pdftotext.txt")
    try:
        subprocess.run(
            [tool, "-layout", str(pdf_path), str(out_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        return ""

    if not out_path.exists():
        return ""
    return normalize_lines(out_path.read_text(encoding="utf-8", errors="ignore").splitlines())


def europe_pmc_search(doi: str) -> dict[str, Any]:
    query = urllib.parse.quote(f'DOI:"{doi}"', safe="")
    url = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        f"?query={query}&resultType=core&format=json"
    )
    return fetch_json(url)


def crossref_work(doi: str) -> dict[str, Any]:
    doi_quoted = urllib.parse.quote(doi, safe="")
    return fetch_json(f"https://api.crossref.org/works/{doi_quoted}")


def unpaywall_work(doi: str, email: str) -> dict[str, Any]:
    doi_quoted = urllib.parse.quote(doi, safe="")
    email_quoted = urllib.parse.quote(email, safe="")
    return fetch_json(f"https://api.unpaywall.org/v2/{doi_quoted}?email={email_quoted}")


def add_candidate(
    candidates: list[dict[str, str]],
    seen: set[tuple[str, str]],
    *,
    url: str | None,
    source: str,
    kind: str,
) -> None:
    clean = normalize_text(url)
    if not clean:
        return
    key = (clean, source)
    if key in seen:
        return
    seen.add(key)
    candidates.append({"url": clean, "source": source, "kind": kind})


def summarize_europepmc(payload: dict[str, Any]) -> dict[str, Any]:
    results = payload.get("resultList", {}).get("result", [])
    if not results:
        return {}
    first = results[0]
    summary = {
        "pmcid": normalize_text(first.get("pmcid")),
        "pmid": normalize_text(first.get("pmid")),
        "title": normalize_text(first.get("title")),
        "journal": normalize_text(first.get("journalTitle")),
        "pub_year": normalize_text(first.get("pubYear")),
        "is_open_access": normalize_text(first.get("isOpenAccess")),
        "in_pmc": normalize_text(first.get("inEPMC")),
    }
    urls: list[dict[str, str]] = []
    for item in first.get("fullTextUrlList", {}).get("fullTextUrl", []) or []:
        if not isinstance(item, dict):
            continue
        urls.append(
            {
                "availability": normalize_text(item.get("availability")),
                "document_style": normalize_text(item.get("documentStyle")),
                "site": normalize_text(item.get("site")),
                "url": normalize_text(item.get("url")),
            }
        )
    if urls:
        summary["full_text_urls"] = urls
    return summary


def summarize_crossref(payload: dict[str, Any]) -> dict[str, Any]:
    message = payload.get("message", {})
    summary = {
        "title": normalize_text(" ".join(message.get("title") or [])),
        "publisher": normalize_text(message.get("publisher")),
        "container_title": normalize_text(" ".join(message.get("container-title") or [])),
        "type": normalize_text(message.get("type")),
    }
    links: list[dict[str, str]] = []
    for item in message.get("link", []) or []:
        if not isinstance(item, dict):
            continue
        links.append(
            {
                "content_type": normalize_text(item.get("content-type")),
                "content_version": normalize_text(item.get("content-version")),
                "intended_application": normalize_text(item.get("intended-application")),
                "url": normalize_text(item.get("URL")),
            }
        )
    if links:
        summary["links"] = links
    return summary


def summarize_unpaywall(payload: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "doi": normalize_text(payload.get("doi")),
        "is_oa": payload.get("is_oa"),
        "journal_is_oa": payload.get("journal_is_oa"),
        "title": normalize_text(payload.get("title")),
    }
    best = payload.get("best_oa_location") or {}
    if isinstance(best, dict) and best:
        summary["best_oa_location"] = {
            "host_type": normalize_text(best.get("host_type")),
            "version": normalize_text(best.get("version")),
            "url": normalize_text(best.get("url")),
            "url_for_landing_page": normalize_text(best.get("url_for_landing_page")),
            "url_for_pdf": normalize_text(best.get("url_for_pdf")),
        }
    return summary


def build_candidates(
    row: dict[str, str],
    *,
    email: str | None,
    lookups: dict[str, Any],
) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    doi = normalize_doi(row.get("doi"))
    preferred_url = row.get("preferred_url")
    publication_urls = split_pipe_values(row.get("publication_urls"))

    pmcid = parse_pmcid(preferred_url)
    for url in publication_urls:
        pmcid = pmcid or parse_pmcid(url)

    if doi:
        europe_full_text_urls: list[dict[str, str]] = []
        try:
            europe_payload = europe_pmc_search(doi)
            lookups["europepmc"] = summarize_europepmc(europe_payload)
            results = europe_payload.get("resultList", {}).get("result", [])
            if results:
                first = results[0]
                pmcid = pmcid or parse_pmcid(normalize_text(first.get("pmcid")))
                for item in first.get("fullTextUrlList", {}).get("fullTextUrl", []) or []:
                    if not isinstance(item, dict):
                        continue
                    doc_style = normalize_text(item.get("documentStyle")).lower()
                    site = normalize_text(item.get("site"))
                    url = normalize_text(item.get("url"))
                    if not url:
                        continue
                    if "xml" in doc_style:
                        kind = "xml"
                    elif "pdf" in doc_style:
                        kind = "pdf"
                    else:
                        kind = "html"
                    europe_full_text_urls.append(
                        {
                            "url": url,
                            "kind": kind,
                            "source": f"europepmc-{site.lower() or 'full-text'}",
                            "site": site.lower(),
                            "document_style": doc_style,
                        }
                    )
        except Exception as exc:  # pragma: no cover - network failures
            lookups["europepmc_error"] = str(exc)

    if pmcid:
        add_candidate(
            candidates,
            seen,
            url=f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML",
            source="europepmc-xml",
            kind="xml",
        )
        add_candidate(
            candidates,
            seen,
            url=f"https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/",
            source="pmc-html",
            kind="html",
        )
    else:
        europe_full_text_urls = []

    if doi:
        for item in sorted(
            europe_full_text_urls,
            key=lambda entry: (
                0 if entry["site"] == "europe_pmc" else 1,
                0 if entry["kind"] == "xml" else 1 if entry["kind"] == "html" else 2,
                1 if "doi" in entry["document_style"] else 0,
            ),
        ):
            add_candidate(
                candidates,
                seen,
                url=item["url"],
                source=item["source"],
                kind=item["kind"],
            )

    add_candidate(candidates, seen, url=preferred_url, source="preferred-url", kind="html")
    for url in publication_urls:
        add_candidate(candidates, seen, url=url, source="publication-url", kind="html")

    if doi and email:
        try:
            unpaywall_payload = unpaywall_work(doi, email)
            lookups["unpaywall"] = summarize_unpaywall(unpaywall_payload)
            best = unpaywall_payload.get("best_oa_location") or {}
            if isinstance(best, dict):
                add_candidate(
                    candidates,
                    seen,
                    url=best.get("url"),
                    source="unpaywall-best",
                    kind="html",
                )
                add_candidate(
                    candidates,
                    seen,
                    url=best.get("url_for_landing_page"),
                    source="unpaywall-landing",
                    kind="html",
                )
                add_candidate(
                    candidates,
                    seen,
                    url=best.get("url_for_pdf"),
                    source="unpaywall-pdf",
                    kind="pdf",
                )
        except Exception as exc:  # pragma: no cover - network failures
            lookups["unpaywall_error"] = str(exc)

    if doi:
        try:
            crossref_payload = crossref_work(doi)
            lookups["crossref"] = summarize_crossref(crossref_payload)
            message = crossref_payload.get("message", {})
            for item in message.get("link", []) or []:
                if not isinstance(item, dict):
                    continue
                content_type = normalize_text(item.get("content-type")).lower()
                url = normalize_text(item.get("URL"))
                if "xml" in content_type:
                    kind = "xml"
                elif "pdf" in content_type:
                    kind = "pdf"
                else:
                    kind = "html"
                add_candidate(candidates, seen, url=url, source="crossref-link", kind=kind)
        except Exception as exc:  # pragma: no cover - network failures
            lookups["crossref_error"] = str(exc)

        add_candidate(
            candidates,
            seen,
            url=f"https://doi.org/{doi}",
            source="doi-landing",
            kind="html",
        )

    return candidates


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def try_candidate(
    candidate: dict[str, str],
    folder: Path,
    *,
    expected_title: str | None,
) -> tuple[dict[str, Any], bool]:
    record: dict[str, Any] = {
        "source": candidate["source"],
        "kind": candidate["kind"],
        "requested_url": candidate["url"],
    }
    try:
        response = fetch_url(candidate["url"])
    except urllib.error.HTTPError as exc:
        record["status"] = f"http_error_{exc.code}"
        record["error"] = str(exc)
        return record, False
    except Exception as exc:  # pragma: no cover - network failures
        record["status"] = "fetch_error"
        record["error"] = str(exc)
        return record, False

    data = response["data"]
    content_type = normalize_text(response.get("content_type"))
    record["status"] = "fetched"
    record["final_url"] = response.get("final_url")
    record["content_type"] = content_type
    record["content_length"] = normalize_text(response.get("content_length"))

    text = ""
    raw_path: Path | None = None

    if looks_like_xml(content_type, data) or candidate["kind"] == "xml":
        raw_path = folder / "manuscript.xml"
        raw_path.write_bytes(data)
        text = extract_xml_text(data)
        record["resolved_as"] = "xml"
    elif looks_like_pdf(content_type, data) or candidate["kind"] == "pdf":
        raw_path = folder / "manuscript.pdf"
        raw_path.write_bytes(data)
        text = extract_pdf_text(raw_path)
        record["resolved_as"] = "pdf"
    else:
        raw_path = folder / "manuscript.html"
        raw_path.write_bytes(data)
        text = extract_html_text(data, content_type)
        record["resolved_as"] = "html"

    if raw_path is not None:
        record["raw_path"] = raw_path.name

    if text:
        if not is_usable_text(text):
            record["status"] = "text_too_short"
            record["n_text_chars"] = len(text)
            return record, False
        if not text_matches_title(text, expected_title):
            record["status"] = "title_mismatch"
            record["n_text_chars"] = len(text)
            return record, False
        (folder / "manuscript.md").write_text(f"{text}\n", encoding="utf-8")
        record["text_path"] = "manuscript.md"
        record["n_text_chars"] = len(text)
        return record, True

    record["status"] = "no_text_extracted"
    return record, False


def resolve_row(
    index: int,
    row: dict[str, str],
    *,
    outdir: Path,
    email: str | None,
    delay_seconds: float,
    skip_existing: bool,
) -> dict[str, Any]:
    folder = outdir / folder_name(index, row)
    folder.mkdir(parents=True, exist_ok=True)

    metadata = dict(row)
    metadata["folder"] = folder.name
    write_json(folder / "metadata.json", metadata)

    manuscript_md = folder / "manuscript.md"
    resolution_path = folder / "resolution.json"
    if skip_existing and manuscript_md.exists() and resolution_path.exists():
        return {"status": "skipped_existing", "folder": folder.name}

    lookups: dict[str, Any] = {}
    candidates = build_candidates(row, email=email, lookups=lookups)

    attempts: list[dict[str, Any]] = []
    final: dict[str, Any] = {"status": "unresolved", "folder": folder.name}

    for candidate in candidates:
        attempt, success = try_candidate(
            candidate,
            folder,
            expected_title=row.get("publication_title"),
        )
        attempts.append(attempt)
        if success:
            final = {
                "status": "resolved",
                "folder": folder.name,
                "source": attempt.get("source"),
                "resolved_as": attempt.get("resolved_as"),
                "final_url": attempt.get("final_url"),
                "content_type": attempt.get("content_type"),
                "raw_path": attempt.get("raw_path"),
                "text_path": attempt.get("text_path"),
                "n_text_chars": attempt.get("n_text_chars"),
            }
            break
        if delay_seconds:
            time.sleep(delay_seconds)

    resolution = {
        "metadata": {
            "doi": row.get("doi"),
            "publication_title": row.get("publication_title"),
            "preferred_url": row.get("preferred_url"),
        },
        "lookups": lookups,
        "candidate_count": len(candidates),
        "attempts": attempts,
        "final": final,
    }
    write_json(resolution_path, resolution)
    return final


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT_TSV)
    parser.add_argument("--outdir", type=Path, default=DEFAULT_OUTDIR)
    parser.add_argument("--start", type=int, default=1, help="1-based row index to start from.")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of rows to process.")
    parser.add_argument("--email", type=str, default=None, help="Email for Unpaywall API lookups.")
    parser.add_argument("--delay-seconds", type=float, default=0.0)
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip papers that already have manuscript.md and resolution.json.",
    )
    args = parser.parse_args()

    rows = load_rows(args.input)
    start_index = max(args.start, 1)
    selected = rows[start_index - 1 :]
    if args.limit is not None:
        selected = selected[: args.limit]

    args.outdir.mkdir(parents=True, exist_ok=True)

    summary = Counter()
    for offset, row in enumerate(selected, start=start_index):
        result = resolve_row(
            offset,
            row,
            outdir=args.outdir,
            email=args.email,
            delay_seconds=args.delay_seconds,
            skip_existing=args.skip_existing,
        )
        summary["processed"] += 1
        summary[result["status"]] += 1
        if result.get("source"):
            summary[f"source_{result['source']}"] += 1
        if result.get("resolved_as"):
            summary[f"resolved_as_{result['resolved_as']}"] += 1

    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"Wrote manuscript cache under {args.outdir}")


if __name__ == "__main__":
    main()
