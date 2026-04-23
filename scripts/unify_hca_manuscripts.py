#!/usr/bin/env python3
"""Unify HCA manuscript caches under data/hca/manuscripts.

This script:
1. moves docs/hca/manuscripts to data/hca/manuscripts
2. merges per-paper assets from data/hca/biorxiv_hca into matching HCA folders by DOI
3. normalizes the canonical readable manuscript artifact to manuscript.md
4. writes manifests summarizing the available files

The canonical paper layout after merge is:
  data/hca/manuscripts/<paper-folder>/
    metadata.json
    resolution.json
    manuscript.md
    manuscript.html / manuscript.xml / manuscript.pdf
    biorxiv_metadata.json
    biorxiv_manuscript.xml   # only when manuscript.xml already exists
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from pathlib import Path


DOCS_MANUSCRIPTS = Path("docs/hca/manuscripts")
TARGET_MANUSCRIPTS = Path("data/hca/manuscripts")
BIORXIV_HCA = Path("data/hca/biorxiv_hca")
MANIFEST_PATH = Path("data/hca/manuscripts_manifest.tsv")
BIORXIV_HELPER_MANIFEST = BIORXIV_HCA / "manifest.tsv"
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>]+", re.IGNORECASE)


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    raw = str(value).strip()
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


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload if isinstance(payload, dict) else {}


def direct_subdirs(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return sorted([entry for entry in path.iterdir() if entry.is_dir()])


def move_docs_cache(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.exists() and not target.exists():
        shutil.move(str(source), str(target))
        return
    if not source.exists():
        return
    target.mkdir(parents=True, exist_ok=True)
    for child in direct_subdirs(source):
        dest = target / child.name
        if dest.exists():
            raise FileExistsError(f"Target already exists: {dest}")
        shutil.move(str(child), str(dest))
    try:
        source.rmdir()
    except OSError:
        pass


def build_doi_index(manuscripts_dir: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for paper_dir in direct_subdirs(manuscripts_dir):
        meta_path = paper_dir / "metadata.json"
        if not meta_path.exists():
            continue
        doi = normalize_doi(load_json(meta_path).get("doi"))
        if not doi:
            continue
        if doi in index:
            raise ValueError(f"Duplicate DOI in {manuscripts_dir}: {doi}")
        index[doi] = paper_dir
    return index


def same_contents(path_a: Path, path_b: Path) -> bool:
    if not path_a.exists() or not path_b.exists():
        return False
    if path_a.stat().st_size != path_b.stat().st_size:
        return False
    return path_a.read_bytes() == path_b.read_bytes()


def copy_if_needed(source: Path, dest: Path) -> str:
    if not source.exists():
        return "missing"
    if dest.exists():
        if same_contents(source, dest):
            return "identical"
        shutil.copy2(source, dest)
        return "overwritten"
    shutil.copy2(source, dest)
    return "copied"


def load_tsv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def merge_biorxiv_sources(
    manuscripts_dir: Path,
    biorxiv_dir: Path,
    *,
    remove_merged_source_dirs: bool,
) -> dict[str, int]:
    doi_index = build_doi_index(manuscripts_dir)
    stats = {
        "source_dirs": 0,
        "matched_dirs": 0,
        "copied_md": 0,
        "copied_xml": 0,
        "copied_biorxiv_xml": 0,
        "copied_meta": 0,
        "removed_source_dirs": 0,
    }

    for source_dir in direct_subdirs(biorxiv_dir):
        stats["source_dirs"] += 1
        meta_path = source_dir / "metadata.json"
        if not meta_path.exists():
            raise FileNotFoundError(f"Missing metadata.json in {source_dir}")
        source_meta = load_json(meta_path)
        doi = normalize_doi(source_meta.get("doi"))
        if not doi:
            raise ValueError(f"Could not normalize DOI for {source_dir}")
        target_dir = doi_index.get(doi)
        if target_dir is None:
            raise KeyError(f"No matching HCA manuscript folder for DOI {doi}")

        stats["matched_dirs"] += 1

        md_status = copy_if_needed(source_dir / "manuscript.md", target_dir / "manuscript.md")
        if md_status in {"copied", "overwritten"}:
            stats["copied_md"] += 1

        source_xml = source_dir / "manuscript.xml"
        if source_xml.exists():
            dest_xml = target_dir / "manuscript.xml"
            if not dest_xml.exists():
                xml_status = copy_if_needed(source_xml, dest_xml)
                if xml_status in {"copied", "overwritten"}:
                    stats["copied_xml"] += 1
            elif not same_contents(source_xml, dest_xml):
                alt_xml = target_dir / "biorxiv_manuscript.xml"
                xml_status = copy_if_needed(source_xml, alt_xml)
                if xml_status in {"copied", "overwritten"}:
                    stats["copied_biorxiv_xml"] += 1

        meta_status = copy_if_needed(source_dir / "metadata.json", target_dir / "biorxiv_metadata.json")
        if meta_status in {"copied", "overwritten"}:
            stats["copied_meta"] += 1

        if remove_merged_source_dirs:
            shutil.rmtree(source_dir)
            stats["removed_source_dirs"] += 1

    return stats


def replace_string_values(node: object, *, old: str, new: str) -> object:
    if isinstance(node, dict):
        return {key: replace_string_values(value, old=old, new=new) for key, value in node.items()}
    if isinstance(node, list):
        return [replace_string_values(value, old=old, new=new) for value in node]
    if isinstance(node, str):
        return new if node == old else node
    return node


def normalize_text_filenames(manuscripts_dir: Path) -> dict[str, int]:
    stats = {
        "renamed_txt_to_md": 0,
        "updated_resolution_text_paths": 0,
    }
    for paper_dir in direct_subdirs(manuscripts_dir):
        txt_path = paper_dir / "manuscript.txt"
        md_path = paper_dir / "manuscript.md"
        if txt_path.exists() and not md_path.exists():
            txt_path.rename(md_path)
            stats["renamed_txt_to_md"] += 1

        resolution_path = paper_dir / "resolution.json"
        if resolution_path.exists():
            original = load_json(resolution_path)
            updated = replace_string_values(original, old="manuscript.txt", new="manuscript.md")
            if updated != original:
                with resolution_path.open("w", encoding="utf-8") as handle:
                    json.dump(updated, handle, indent=2, sort_keys=True)
                    handle.write("\n")
                stats["updated_resolution_text_paths"] += 1
    return stats


def refresh_biorxiv_helper_manifest(
    manuscripts_dir: Path,
    helper_manifest_path: Path,
) -> dict[str, int]:
    rows = load_tsv_rows(helper_manifest_path)
    if not rows:
        return {"rewritten_biorxiv_manifest_rows": 0}

    doi_index = build_doi_index(manuscripts_dir)
    rewritten_rows: list[dict[str, str]] = []
    for row in rows:
        doi = normalize_doi(row.get("doi"))
        target_dir = doi_index.get(doi or "")
        if target_dir is None:
            raise KeyError(f"No matching HCA manuscript folder for DOI {doi}")
        rewritten = dict(row)
        rewritten["markdown_path"] = str((target_dir / "manuscript.md").as_posix()) if (target_dir / "manuscript.md").exists() else ""
        rewritten["xml_path"] = str((target_dir / "manuscript.xml").as_posix()) if (target_dir / "manuscript.xml").exists() else ""
        rewritten["metadata_path"] = (
            str((target_dir / "biorxiv_metadata.json").as_posix())
            if (target_dir / "biorxiv_metadata.json").exists()
            else ""
        )
        rewritten_rows.append(rewritten)

    fieldnames = list(rewritten_rows[0].keys())
    write_tsv_rows(helper_manifest_path, fieldnames, rewritten_rows)
    return {"rewritten_biorxiv_manifest_rows": len(rewritten_rows)}


def build_manifest(manuscripts_dir: Path, manifest_path: Path) -> None:
    rows: list[dict[str, str]] = []
    for paper_dir in direct_subdirs(manuscripts_dir):
        meta = load_json(paper_dir / "metadata.json") if (paper_dir / "metadata.json").exists() else {}
        doi = normalize_doi(meta.get("doi")) or ""
        row = {
            "folder": paper_dir.name,
            "doi": doi,
            "publication_title": str(meta.get("publication_title", "")),
            "project_count": str(meta.get("project_count", "")),
            "metadata_json": str((paper_dir / "metadata.json").as_posix()),
            "resolution_json": str((paper_dir / "resolution.json").as_posix()) if (paper_dir / "resolution.json").exists() else "",
            "manuscript_path": str((paper_dir / "manuscript.md").as_posix()) if (paper_dir / "manuscript.md").exists() else "",
            "manuscript_html": str((paper_dir / "manuscript.html").as_posix()) if (paper_dir / "manuscript.html").exists() else "",
            "manuscript_xml": str((paper_dir / "manuscript.xml").as_posix()) if (paper_dir / "manuscript.xml").exists() else "",
            "biorxiv_manuscript_xml": str((paper_dir / "biorxiv_manuscript.xml").as_posix()) if (paper_dir / "biorxiv_manuscript.xml").exists() else "",
            "manuscript_pdf": str((paper_dir / "manuscript.pdf").as_posix()) if (paper_dir / "manuscript.pdf").exists() else "",
            "biorxiv_metadata_json": str((paper_dir / "biorxiv_metadata.json").as_posix()) if (paper_dir / "biorxiv_metadata.json").exists() else "",
        }
        rows.append(row)

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        "folder",
        "doi",
        "publication_title",
        "project_count",
        "metadata_json",
        "resolution_json",
        "manuscript_path",
        "manuscript_html",
        "manuscript_xml",
        "biorxiv_manuscript_xml",
        "manuscript_pdf",
        "biorxiv_metadata_json",
    ]
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-source", type=Path, default=DOCS_MANUSCRIPTS)
    parser.add_argument("--target", type=Path, default=TARGET_MANUSCRIPTS)
    parser.add_argument("--biorxiv-source", type=Path, default=BIORXIV_HCA)
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--remove-merged-source-dirs", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    move_docs_cache(args.docs_source, args.target)
    stats = merge_biorxiv_sources(
        args.target,
        args.biorxiv_source,
        remove_merged_source_dirs=args.remove_merged_source_dirs,
    )
    stats.update(normalize_text_filenames(args.target))
    build_manifest(args.target, args.manifest)
    stats.update(refresh_biorxiv_helper_manifest(args.target, BIORXIV_HELPER_MANIFEST))
    print(json.dumps(stats, indent=2, sort_keys=True))
    print(f"wrote manifest: {args.manifest}")


if __name__ == "__main__":
    main()
