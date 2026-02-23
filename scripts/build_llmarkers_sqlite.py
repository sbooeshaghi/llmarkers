#!/usr/bin/env python3
"""Build a SQLite database for LLMarker + bioRxiv marker datasets.

Schema:
- papers
- markers
- marker_metrics
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


BENCHMARK_DATASETS = [
    "adipose_Emont2022",
    "adipose_Hildreth2021",
    "bone_He2021",
    "eye_Gautam2021",
    "lung_Adams2020",
    "ovary_Wagner2020",
    "testis_Shamis2020",
]

DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>]+", re.IGNORECASE)


@dataclass
class PaperRecord:
    doi: str
    title: str | None
    year: int | None
    license: str | None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_key(value: Any) -> str:
    return normalize_text(value).upper()


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    raw = value.strip()
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

    # Nature article URLs often omit explicit DOI prefix.
    # Example: https://www.nature.com/articles/s41590-021-00922-4
    nature_match = re.search(r"nature\.com/articles/([A-Za-z0-9\-_.]+)", raw)
    if nature_match:
        return f"10.1038/{nature_match.group(1)}".lower()

    if raw.startswith("10."):
        return raw.rstrip(". )]").lower()

    return None


def extract_year_from_text(value: str | None) -> int | None:
    if not value:
        return None
    years = re.findall(r"(?:19|20)\d{2}", value)
    if not years:
        return None
    return int(years[-1])


def infer_benchmark_year(dataset_name: str, citation: str | None) -> int | None:
    year = extract_year_from_text(citation)
    if year is not None:
        return year
    suffix = re.search(r"((?:19|20)\d{2})$", dataset_name)
    if suffix:
        return int(suffix.group(1))
    return None


def infer_title_from_citation(citation: str | None) -> str | None:
    if not citation:
        return None

    text = citation.strip()

    # Pattern 1: "... et al. Title. Journal ..."
    m = re.search(r"et al\.\s+(.+?)\.\s+[A-Z][^\.]{0,80}\d", text)
    if m:
        return m.group(1).strip()

    # Pattern 2: "..., 2020. Title. Journal ..."
    m = re.search(r"(?:19|20)\d{2}\.\s+(.+?)\.\s+[A-Z]", text)
    if m:
        return m.group(1).strip()

    # Pattern 3: take phrase before final journal segment.
    bits = [b.strip() for b in text.split(".") if b.strip()]
    if len(bits) >= 2:
        candidate = bits[-2]
        if len(candidate.split()) >= 4:
            return candidate

    return None


def infer_title_from_manuscript_txt(path: Path) -> str | None:
    if not path.exists():
        return None

    skip_prefixes = (
        "main",
        "abstract",
        "download pdf",
        "open access",
        "published:",
        "article",
        "nature",
        "you have full access",
        "show authors",
        "metrics details",
    )

    with path.open("r", encoding="utf-8", errors="ignore") as handle:
        lines = [line.strip() for line in handle.readlines()[:120]]

    for line in lines:
        if not line:
            continue
        if line.startswith("-"):
            continue
        low = line.lower()
        if any(low.startswith(prefix) for prefix in skip_prefixes):
            continue
        if len(line) < 20 or len(line) > 220:
            continue
        if line.count(" ") < 3:
            continue
        return line

    return None


def read_json_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if isinstance(data, list):
        return data
    return []


def read_json_object_relaxed(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Tolerate trailing commas in hand-edited metadata files.
        cleaned = re.sub(r",\s*([}\]])", r"\1", text)
        data = json.loads(cleaned)
    return data if isinstance(data, dict) else {}


def parse_biorxiv_xml(xml_path: Path) -> PaperRecord | None:
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError:
        return None

    doi = None
    title = None
    year = None
    license_text = None

    for node in root.findall(".//article-id"):
        if node.attrib.get("pub-id-type") == "doi" and node.text:
            doi = normalize_doi(node.text)
            if doi:
                break

    title_node = root.find(".//title-group/article-title")
    if title_node is not None:
        title = "".join(title_node.itertext()).strip() or None

    year_node = root.find(".//pub-date/year")
    if year_node is not None and year_node.text and year_node.text.strip().isdigit():
        year = int(year_node.text.strip())
    else:
        cyr = root.find(".//copyright-year")
        if cyr is not None and cyr.text and cyr.text.strip().isdigit():
            year = int(cyr.text.strip())

    lic_node = root.find(".//license")
    if lic_node is not None:
        href = lic_node.attrib.get("{http://www.w3.org/1999/xlink}href")
        p = lic_node.find("license-p")
        p_text = "".join(p.itertext()).strip() if p is not None else ""
        license_text = href or p_text or None

    if doi is None:
        return None

    return PaperRecord(doi=doi, title=title, year=year, license=license_text)


def find_biorxiv_article_xml(folder: Path) -> Path | None:
    xml_files = sorted(
        p
        for p in folder.glob("*.xml")
        if p.name not in {"directives.xml", "manifest.xml", "transfer.xml"}
    )
    return xml_files[0] if xml_files else None


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = ON;

        DROP TABLE IF EXISTS marker_metrics;
        DROP TABLE IF EXISTS markers;
        DROP TABLE IF EXISTS papers;

        CREATE TABLE papers (
            paper_id INTEGER PRIMARY KEY,
            doi TEXT UNIQUE,
            title TEXT,
            year INTEGER,
            license TEXT
        );

        CREATE TABLE markers (
            marker_id INTEGER PRIMARY KEY,
            paper_id INTEGER NOT NULL REFERENCES papers(paper_id),
            group_name TEXT NOT NULL,
            feature_name TEXT NOT NULL,
            feature_id TEXT,
            source_type TEXT NOT NULL,
            source_rationale TEXT,
            data_id TEXT
        );

        CREATE TABLE marker_metrics (
            marker_id INTEGER PRIMARY KEY REFERENCES markers(marker_id),
            lfc REAL,
            p_corr REAL,
            rank INTEGER
        );

        CREATE INDEX idx_markers_paper_id ON markers(paper_id);
        CREATE INDEX idx_markers_group_name ON markers(group_name);
        CREATE INDEX idx_markers_feature_id ON markers(feature_id);
        CREATE INDEX idx_markers_source_type ON markers(source_type);
        CREATE INDEX idx_marker_metrics_rank ON marker_metrics(rank);
        """
    )


def get_or_create_paper(conn: sqlite3.Connection, paper: PaperRecord) -> int:
    row = conn.execute("SELECT paper_id FROM papers WHERE doi = ?", (paper.doi,)).fetchone()
    if row:
        return int(row[0])

    cur = conn.execute(
        "INSERT INTO papers (doi, title, year, license) VALUES (?, ?, ?, ?)",
        (paper.doi, paper.title, paper.year, paper.license),
    )
    return int(cur.lastrowid)


def build_deg_metric_index(deg_rows: list[dict[str, Any]]) -> tuple[dict[tuple[str, str, str], tuple[Any, Any, Any]], dict[tuple[str, str, str], tuple[Any, Any, Any]]]:
    by_feature_id: dict[tuple[str, str, str], tuple[Any, Any, Any]] = {}
    by_feature_name: dict[tuple[str, str, str], tuple[Any, Any, Any]] = {}

    for row in deg_rows:
        data_id = normalize_key(row.get("data_id"))
        group_name = normalize_key(row.get("group_name"))
        feature_id = normalize_key(row.get("feature_id"))
        feature_name = normalize_key(row.get("feature_name"))

        metrics = (
            row.get("metrics_logfc"),
            row.get("metrics_pcorr"),
            row.get("metrics_rank"),
        )

        rank_value = row.get("metrics_rank")
        try:
            rank_num = int(rank_value) if rank_value is not None else None
        except (TypeError, ValueError):
            rank_num = None

        if feature_id:
            key = (data_id, group_name, feature_id)
            existing = by_feature_id.get(key)
            if existing is None:
                by_feature_id[key] = metrics
            else:
                existing_rank = existing[2]
                try:
                    existing_rank_num = int(existing_rank) if existing_rank is not None else None
                except (TypeError, ValueError):
                    existing_rank_num = None
                if rank_num is not None and (existing_rank_num is None or rank_num < existing_rank_num):
                    by_feature_id[key] = metrics

        if feature_name:
            key = (data_id, group_name, feature_name)
            existing = by_feature_name.get(key)
            if existing is None:
                by_feature_name[key] = metrics
            else:
                existing_rank = existing[2]
                try:
                    existing_rank_num = int(existing_rank) if existing_rank is not None else None
                except (TypeError, ValueError):
                    existing_rank_num = None
                if rank_num is not None and (existing_rank_num is None or rank_num < existing_rank_num):
                    by_feature_name[key] = metrics

    return by_feature_id, by_feature_name


def insert_marker(
    conn: sqlite3.Connection,
    paper_id: int,
    row: dict[str, Any],
    metrics: tuple[Any, Any, Any] | None = None,
) -> None:
    group_name = normalize_text(row.get("group_name"))
    feature_name = normalize_text(row.get("feature_name"))
    source_type = normalize_text(row.get("source_type"))

    if not group_name or not feature_name or not source_type:
        return

    cur = conn.execute(
        """
        INSERT INTO markers (
            paper_id,
            group_name,
            feature_name,
            feature_id,
            source_type,
            source_rationale,
            data_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            paper_id,
            group_name,
            feature_name,
            normalize_text(row.get("feature_id")) or None,
            source_type,
            normalize_text(row.get("source_rationale")) or None,
            normalize_text(row.get("data_id")) or None,
        ),
    )
    marker_id = int(cur.lastrowid)

    lfc = p_corr = rank = None
    if metrics is not None:
        lfc, p_corr, rank = metrics
    else:
        lfc = row.get("metrics_logfc")
        p_corr = row.get("metrics_pcorr")
        rank = row.get("metrics_rank")

    has_metric = lfc is not None or p_corr is not None or rank is not None
    if not has_metric:
        return

    rank_int = None
    if rank is not None:
        try:
            rank_int = int(rank)
        except (TypeError, ValueError):
            rank_int = None

    lfc_float = None
    if lfc is not None:
        try:
            lfc_float = float(lfc)
        except (TypeError, ValueError):
            lfc_float = None

    pcorr_float = None
    if p_corr is not None:
        try:
            pcorr_float = float(p_corr)
        except (TypeError, ValueError):
            pcorr_float = None

    conn.execute(
        "INSERT INTO marker_metrics (marker_id, lfc, p_corr, rank) VALUES (?, ?, ?, ?)",
        (marker_id, lfc_float, pcorr_float, rank_int),
    )


def ingest_benchmark(conn: sqlite3.Connection, data_dir: Path) -> None:
    for dataset in BENCHMARK_DATASETS:
        dataset_dir = data_dir / dataset
        metadata_path = dataset_dir / "metadata.json"
        metadata = read_json_object_relaxed(metadata_path)

        doi = normalize_doi(metadata.get("doi"))
        if doi is None:
            raise ValueError(f"Could not parse DOI for benchmark dataset: {dataset}")

        citation = metadata.get("citation")
        title = infer_title_from_citation(citation)
        if title is None:
            title = infer_title_from_manuscript_txt(dataset_dir / "manuscript" / "manuscript.txt")
        year = infer_benchmark_year(dataset, citation)

        paper = PaperRecord(doi=doi, title=title, year=year, license=None)
        paper_id = get_or_create_paper(conn, paper)

        human_rows = read_json_list(dataset_dir / "evidence_human" / "extracted.json")
        deg_rows = read_json_list(dataset_dir / "evidence_deg" / "extracted.json")
        deg_by_id, deg_by_name = build_deg_metric_index(deg_rows)

        for row in human_rows:
            data_id = normalize_key(row.get("data_id"))
            group_name = normalize_key(row.get("group_name"))
            feature_id = normalize_key(row.get("feature_id"))
            feature_name = normalize_key(row.get("feature_name"))

            metrics = None
            if feature_id:
                metrics = deg_by_id.get((data_id, group_name, feature_id))
            if metrics is None and feature_name:
                metrics = deg_by_name.get((data_id, group_name, feature_name))

            insert_marker(conn, paper_id, row, metrics=metrics)


def ingest_biorxiv(conn: sqlite3.Connection, biorxiv_dir: Path) -> None:
    meca_dir = biorxiv_dir / "meca"
    if not meca_dir.exists():
        return

    for folder in sorted(p for p in meca_dir.iterdir() if p.is_dir()):
        markers_path = folder / "markers.json"
        if not markers_path.exists():
            continue

        article_xml = find_biorxiv_article_xml(folder)
        if article_xml is None:
            continue

        paper = parse_biorxiv_xml(article_xml)
        if paper is None:
            continue

        paper_id = get_or_create_paper(conn, paper)
        marker_rows = read_json_list(markers_path)
        for row in marker_rows:
            insert_marker(conn, paper_id, row, metrics=None)


def summarize(conn: sqlite3.Connection) -> dict[str, int]:
    def scalar(query: str) -> int:
        row = conn.execute(query).fetchone()
        return int(row[0]) if row and row[0] is not None else 0

    return {
        "papers": scalar("SELECT COUNT(*) FROM papers"),
        "benchmark_papers": scalar(
            """
            SELECT COUNT(*) FROM papers p
            WHERE EXISTS (
                SELECT 1 FROM markers m
                WHERE m.paper_id = p.paper_id
                AND m.data_id IS NOT NULL
                AND m.data_id <> ''
            )
            """
        ),
        "biorxiv_papers": scalar(
            """
            SELECT COUNT(*) FROM papers p
            WHERE NOT EXISTS (
                SELECT 1 FROM markers m
                WHERE m.paper_id = p.paper_id
                AND m.data_id IS NOT NULL
                AND m.data_id <> ''
            )
            """
        ),
        "markers": scalar("SELECT COUNT(*) FROM markers"),
        "marker_metrics": scalar("SELECT COUNT(*) FROM marker_metrics"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build LLMarker SQLite database")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Path to repository data directory",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/llmarkers.sqlite"),
        help="Output SQLite file path",
    )
    args = parser.parse_args()

    output_path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        output_path.unlink()

    conn = sqlite3.connect(output_path)
    try:
        create_schema(conn)
        ingest_benchmark(conn, args.data_dir)
        ingest_biorxiv(conn, args.data_dir / "biorxiv")
        conn.commit()

        stats = summarize(conn)
        print("Built:", output_path)
        for key, value in stats.items():
            print(f"  {key}: {value}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
