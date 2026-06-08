#!/usr/bin/env python3
"""Build the poster appendix reference list from local corpus metadata."""

from __future__ import annotations

import csv
import html
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BIORXIV_DIR = ROOT / "data" / "biorxiv" / "meca"
HCA_DIR = ROOT / "data" / "hca" / "manuscripts"
HCA_MANIFEST = ROOT / "data" / "hca" / "manuscripts_manifest.tsv"
OUT_TSV = ROOT / "poster" / "tables" / "corpus_references.tsv"
OUT_TEX = ROOT / "poster" / "tables" / "corpus_references_body.tex"
OUT_POSTER_TEX = ROOT / "poster" / "tables" / "corpus_references_poster.tex"
OUT_BIB = ROOT / "poster" / "corpus_references.bib"

DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")


def plain_text(value: object) -> str:
    text = html.unescape(str(value or ""))
    replacements = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00a0": " ",
        "\u03b1": "alpha",
        "\u03b2": "beta",
        "\u03b3": "gamma",
        "\u03b4": "delta",
        "\u03bc": "micro",
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_author(value: str) -> str:
    text = re.sub(r"<sup>.*?</sup>", "", value)
    text = re.sub(r"\s*\(\s*\[?ORCID:.*$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\([^)]*orcid[^)]*\)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[†‡*]+", "", text)
    return plain_text(text).strip(" ,;")


def parse_markdown(path: Path) -> tuple[str, list[str], str]:
    if not path.exists():
        return "", [], ""

    raw = path.read_text(encoding="utf-8", errors="ignore")
    title = ""
    authors: list[str] = []
    in_authors = False

    for line in raw.splitlines():
        stripped = line.strip()
        if not title and stripped.startswith("# "):
            title = plain_text(stripped[2:])
            continue

        if stripped.lower() == "## authors":
            in_authors = True
            continue

        if in_authors:
            if stripped.startswith("### ") or stripped.startswith("## "):
                in_authors = False
                continue
            if stripped.startswith("- "):
                author = clean_author(stripped[2:])
                if author:
                    authors.append(author)

    return title, authors, raw[:3000]


def first_author(authors: list[str]) -> str:
    if not authors:
        return ""
    if len(authors) == 1:
        return authors[0]
    return f"{authors[0]} et al."


def valid_year(value: object) -> str:
    text = plain_text(value)
    if re.fullmatch(r"(19|20)\d{2}", text):
        year = int(text)
        if 1900 <= year <= 2026:
            return text
    return ""


def year_from_biorxiv_doi(doi: str) -> str:
    match = re.search(r"10\.1101/(20\d{2})[./]", doi)
    return match.group(1) if match else ""


def hca_year(row: dict[str, str], folder: Path) -> str:
    resolution_path = ROOT / row["resolution_json"] if row.get("resolution_json") else folder / "resolution.json"
    if not resolution_path.exists():
        return year_from_biorxiv_doi(row.get("doi", ""))
    try:
        data = json.loads(resolution_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return year_from_biorxiv_doi(row.get("doi", ""))

    candidates = [
        data.get("lookups", {}).get("europepmc", {}).get("pub_year", ""),
        data.get("lookups", {}).get("crossref", {}).get("published-print", {}).get("date-parts", [[""]])[0][0],
        data.get("lookups", {}).get("crossref", {}).get("published-online", {}).get("date-parts", [[""]])[0][0],
        year_from_biorxiv_doi(row.get("doi", "")),
    ]
    for candidate in candidates:
        year = valid_year(candidate)
        if year:
            return year
    return ""


def latex_escape(value: object) -> str:
    text = plain_text(value)
    text = text.replace("\\", r"\textbackslash{}")
    for src, dst in {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }.items():
        text = text.replace(src, dst)
    return text


def bib_escape(value: object) -> str:
    return latex_escape(value)


def bib_key(corpus: str, folder: str) -> str:
    prefix = "biorxiv" if corpus == "bioRxiv" else "hca"
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", folder).strip("_")
    return f"{prefix}_{cleaned}"


def hca_manifest_by_folder() -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    with HCA_MANIFEST.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            rows[row["folder"]] = row
    return rows


def build_biorxiv_entries() -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for folder in sorted(BIORXIV_DIR.iterdir()):
        if not (folder / "markers.json").exists():
            continue
        title, authors, header = parse_markdown(folder / "manuscript.md")
        doi_match = DOI_RE.search(header)
        doi = doi_match.group(0).rstrip(".,);") if doi_match else ""
        title = title or folder.name
        entries.append(
            {
                "corpus": "bioRxiv",
                "key": bib_key("bioRxiv", folder.name),
                "folder": folder.name,
                "doi": doi,
                "year": year_from_biorxiv_doi(doi),
                "author": first_author(authors),
                "n_authors": str(len(authors)),
                "title": title,
                "locator": f"doi:{doi}" if doi else f"local:{folder.name}",
            }
        )
    return sorted(entries, key=lambda row: (row["title"].lower(), row["folder"]))


def build_hca_entries() -> list[dict[str, str]]:
    manifest = hca_manifest_by_folder()
    entries: list[dict[str, str]] = []
    for folder in sorted(HCA_DIR.iterdir()):
        if not (folder / "markers.json").exists():
            continue
        row = manifest.get(folder.name, {})
        manifest_md = ROOT / row["manuscript_path"] if row.get("manuscript_path") else folder / "manuscript.md"
        title, authors, _ = parse_markdown(manifest_md)
        doi = plain_text(row.get("doi", ""))
        title = title or plain_text(row.get("publication_title", "")) or folder.name
        entries.append(
            {
                "corpus": "HCA",
                "key": bib_key("HCA", folder.name),
                "folder": folder.name,
                "doi": doi,
                "year": hca_year(row, folder),
                "author": first_author(authors),
                "n_authors": str(len(authors)),
                "title": title,
                "locator": f"doi:{doi}" if doi else f"local:{folder.name}",
            }
        )
    return sorted(entries, key=lambda row: (row["title"].lower(), row["folder"]))


def tex_entry(entry: dict[str, str]) -> str:
    index = latex_escape(entry["index"])
    corpus = latex_escape(entry["corpus"])
    author = latex_escape(entry["author"])
    year = latex_escape(entry["year"])
    title = latex_escape(entry["title"])
    locator = latex_escape(entry["locator"])
    if author and year:
        byline = f"{author} ({year})"
    elif author:
        byline = author
    elif year:
        byline = year
    else:
        byline = ""
    return rf"\corpusref{{{index}}}{{{corpus}}}{{{byline}}}{{{title}}}{{{locator}}}"


def poster_citation(entry: dict[str, str]) -> tuple[str, str]:
    byline = ""
    if entry["author"]:
        byline = entry["author"]
    if entry["year"]:
        byline = f"{byline} ({entry['year']})" if byline else entry["year"]
    separator = " " if byline.endswith(".") and not entry["year"] else ". "
    citation = f"{byline}{separator}{entry['title']}" if byline else entry["title"]
    locator = entry["doi"] or entry["folder"][:8]
    return citation, locator


def poster_entry(entry: dict[str, str]) -> str:
    index = latex_escape(entry["index"])
    citation, locator = poster_citation(entry)
    return rf"\posterref{{{index}.}}{{{latex_escape(citation)}}}{{{latex_escape(locator)}}}"


def bib_entry(entry: dict[str, str]) -> str:
    fields = {
        "title": "{" + bib_escape(entry["title"]) + "}",
        "note": bib_escape(f"{entry['corpus']} corpus; {entry['locator']}"),
    }
    if entry["author"]:
        fields["author"] = "{" + bib_escape(entry["author"]) + "}"
    if entry["year"]:
        fields["year"] = bib_escape(entry["year"])
    if entry["doi"]:
        fields["doi"] = bib_escape(entry["doi"])

    lines = [f"@misc{{{entry['key']},"]
    for name in ["author", "title", "year", "doi", "note"]:
        if name in fields:
            lines.append(f"  {name} = {{{fields[name]}}},")
    lines.append("}")
    return "\n".join(lines)


def write_outputs(entries: list[dict[str, str]]) -> None:
    for index, entry in enumerate(entries, start=1):
        entry["index"] = str(index)

    OUT_TSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_TSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["index", "corpus", "key", "folder", "doi", "year", "author", "n_authors", "title", "locator"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(entries)

    biorxiv = [row for row in entries if row["corpus"] == "bioRxiv"]
    hca = [row for row in entries if row["corpus"] == "HCA"]
    lines = [
        "% Generated by poster/scripts/build_corpus_references.py; do not edit by hand.",
        rf"\corpussection{{bioRxiv corpus}}{{{len(biorxiv)} extracted manuscripts}}",
    ]
    lines.extend(tex_entry(row) for row in biorxiv)
    lines.append(rf"\corpussection{{HCA corpus}}{{{len(hca)} extracted publications}}")
    lines.extend(tex_entry(row) for row in hca)
    OUT_TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")

    poster_lines = [
        "% Generated by poster/scripts/build_corpus_references.py; do not edit by hand.",
    ]
    poster_lines.extend(poster_entry(row) for row in entries)
    OUT_POSTER_TEX.write_text("\n".join(poster_lines) + "\n", encoding="utf-8")
    OUT_BIB.write_text(
        "% Generated by poster/scripts/build_corpus_references.py; do not edit by hand.\n\n"
        + "\n\n".join(bib_entry(row) for row in entries)
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    entries = build_biorxiv_entries() + build_hca_entries()
    write_outputs(entries)
    n_biorxiv = sum(row["corpus"] == "bioRxiv" for row in entries)
    n_hca = sum(row["corpus"] == "HCA" for row in entries)
    n_missing_author = sum(not row["author"] for row in entries)
    print(f"Wrote {OUT_TSV.relative_to(ROOT)}")
    print(f"Wrote {OUT_TEX.relative_to(ROOT)}")
    print(f"Wrote {OUT_POSTER_TEX.relative_to(ROOT)}")
    print(f"Wrote {OUT_BIB.relative_to(ROOT)}")
    print(f"References: {n_biorxiv} bioRxiv, {n_hca} HCA, {n_missing_author} missing parsed authors")


if __name__ == "__main__":
    main()
