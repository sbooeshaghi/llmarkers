#!/usr/bin/env python3
"""Audit and migrate marker JSON files to the flat LLMarkers record schema."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


BASE_FIELDS = [
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
]

METRIC_FIELDS = [
    "metrics_pcorr",
    "metrics_logfc",
    "metrics_rank",
]

CANONICAL_FIELDS = BASE_FIELDS
KNOWN_FIELDS = BASE_FIELDS + METRIC_FIELDS
EXTRA_FIELD_PREFIXES = ("_",)
MARKER_FILE_NAMES = {
    "markers.json",
    "extracted.json",
    "extracted_txt.json",
    "extracted_txt_rerun.json",
    "bu_extracted.json",
}


def text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def upper_or_none(value: Any) -> str | None:
    text = text_or_none(value)
    return text.upper() if text else None


def is_marker_file(path: Path) -> bool:
    if path.name in MARKER_FILE_NAMES:
        return True
    return path.name.startswith("selected") and path.suffix == ".json"


def iter_marker_paths(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.json") if is_marker_file(path))


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, separators=(",", ":"), ensure_ascii=False)
        handle.write("\n")


def classify_record(record: Any) -> str:
    if not isinstance(record, dict):
        return "non_object"

    has_flat_group = "group_label" in record or "group_name" in record
    has_flat_feature = "feature_label" in record or "feature_name" in record
    has_flat_source = "source_type" in record or "source_rationale" in record
    if has_flat_group and has_flat_feature and has_flat_source:
        missing = [field for field in CANONICAL_FIELDS if field not in record]
        return "flat" if not missing else "flat_missing_keys"

    if isinstance(record.get("extracted"), dict) or isinstance(record.get("derived"), dict):
        return "nested"

    if ("cell_type" in record or "cell_type_label" in record) and (
        "gene" in record or "feature" in record or "feature_label" in record
    ):
        return "legacy_flat"

    return "unknown"


def ordered_with_extras(record: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
    out = {field: values.get(field) for field in CANONICAL_FIELDS}
    for field in METRIC_FIELDS:
        if field in record or values.get(field) is not None:
            out[field] = values.get(field)
    for key, value in record.items():
        if key in KNOWN_FIELDS:
            continue
        if key in {"extracted", "derived", "source"}:
            continue
        if key.startswith(EXTRA_FIELD_PREFIXES):
            out[key] = value
    for key, value in record.items():
        if key in out or key in KNOWN_FIELDS or key in {"extracted", "derived", "source"}:
            continue
        out[key] = value
    return out


def normalize_flat(record: dict[str, Any]) -> dict[str, Any]:
    values = {
        "organism": text_or_none(record.get("organism")),
        "group_label": text_or_none(record.get("group_label")),
        "group_name": upper_or_none(record.get("group_name") or record.get("group_label")),
        "group_id": text_or_none(record.get("group_id")),
        "feature_label": text_or_none(record.get("feature_label")),
        "feature_name": upper_or_none(record.get("feature_name") or record.get("feature_label")),
        "feature_id": text_or_none(record.get("feature_id")),
        "source_type": text_or_none(record.get("source_type")),
        "source_rationale": text_or_none(record.get("source_rationale")),
        "source_id": text_or_none(record.get("source_id")),
        "data_id": text_or_none(record.get("data_id")),
        "metrics_pcorr": record.get("metrics_pcorr"),
        "metrics_logfc": record.get("metrics_logfc"),
        "metrics_rank": record.get("metrics_rank"),
    }
    return ordered_with_extras(record, values)


def normalize_nested(record: dict[str, Any]) -> dict[str, Any]:
    extracted = record.get("extracted") if isinstance(record.get("extracted"), dict) else {}
    derived = record.get("derived") if isinstance(record.get("derived"), dict) else {}
    source = record.get("source") if isinstance(record.get("source"), dict) else {}

    group_label = (
        extracted.get("cell_type_label")
        or extracted.get("cell_type")
        or extracted.get("group_label")
        or derived.get("cell_type_label")
        or derived.get("group_label")
        or derived.get("group_name")
    )
    feature_label = (
        extracted.get("feature_label")
        or extracted.get("feature")
        or extracted.get("gene")
        or extracted.get("gene_label")
        or derived.get("feature_label")
        or derived.get("gene")
    )
    feature_name = (
        derived.get("feature_name")
        or derived.get("gene_name")
        or derived.get("gene")
        or feature_label
    )

    values = {
        "organism": text_or_none(record.get("organism") or derived.get("organism") or extracted.get("organism")),
        "group_label": text_or_none(group_label),
        "group_name": upper_or_none(derived.get("group_name") or derived.get("cell_type_name") or group_label),
        "group_id": text_or_none(derived.get("group_id") or derived.get("cell_type_id")),
        "feature_label": text_or_none(feature_label),
        "feature_name": upper_or_none(feature_name),
        "feature_id": text_or_none(
            derived.get("feature_id")
            or derived.get("feature_identifier")
            or derived.get("gene_id")
            or extracted.get("feature_id")
            or extracted.get("gene_id")
        ),
        "source_type": text_or_none(source.get("source_type") or record.get("source_type")),
        "source_rationale": text_or_none(source.get("source_rationale") or record.get("source_rationale")),
        "source_id": text_or_none(source.get("source_id") or record.get("source_id")),
        "data_id": text_or_none(record.get("data_id") or source.get("data_id") or derived.get("data_id")),
        "metrics_pcorr": record.get("metrics_pcorr") or derived.get("metrics_pcorr"),
        "metrics_logfc": record.get("metrics_logfc") or derived.get("metrics_logfc"),
        "metrics_rank": record.get("metrics_rank") or derived.get("metrics_rank"),
    }

    out = ordered_with_extras(record, values)
    out["_legacy_record"] = {
        "extracted": extracted,
        "derived": derived,
        "source": source,
    }
    return out


def normalize_legacy_flat(record: dict[str, Any]) -> dict[str, Any]:
    source = record.get("source") if isinstance(record.get("source"), dict) else {}
    group_label = (
        record.get("group_label")
        or record.get("cell_type_label")
        or record.get("cell_type")
        or record.get("cell_state")
    )
    feature_label = record.get("feature_label") or record.get("gene") or record.get("feature")

    values = {
        "organism": text_or_none(record.get("organism")),
        "group_label": text_or_none(group_label),
        "group_name": upper_or_none(record.get("group_name") or group_label),
        "group_id": text_or_none(record.get("group_id") or record.get("cell_type_id")),
        "feature_label": text_or_none(feature_label),
        "feature_name": upper_or_none(record.get("feature_name") or feature_label),
        "feature_id": text_or_none(record.get("feature_id") or record.get("gene_id")),
        "source_type": text_or_none(record.get("source_type") or source.get("source_type")),
        "source_rationale": text_or_none(record.get("source_rationale") or source.get("source_rationale")),
        "source_id": text_or_none(record.get("source_id") or source.get("source_id")),
        "data_id": text_or_none(record.get("data_id")),
        "metrics_pcorr": record.get("metrics_pcorr"),
        "metrics_logfc": record.get("metrics_logfc"),
        "metrics_rank": record.get("metrics_rank"),
    }

    out = ordered_with_extras(record, values)
    if source:
        out["_legacy_source"] = source
    if "cell_source" in record:
        out["_legacy_cell_source"] = record.get("cell_source")
    if "cell_state" in record:
        out["_legacy_cell_state"] = record.get("cell_state")
    return out


def normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    kind = classify_record(record)
    if kind in {"flat", "flat_missing_keys"}:
        return normalize_flat(record)
    if kind == "nested":
        return normalize_nested(record)
    if kind == "legacy_flat":
        return normalize_legacy_flat(record)
    raise ValueError(f"Cannot normalize record classified as {kind}")


def extract_records(data: Any) -> tuple[list[Any] | None, str]:
    if isinstance(data, list):
        return data, "list"
    if isinstance(data, dict) and isinstance(data.get("markers"), list):
        return data["markers"], "dict_markers"
    return None, "unsupported"


def analyze_file(path: Path) -> dict[str, Any]:
    data = read_json(path)
    records, container = extract_records(data)
    result: dict[str, Any] = {
        "path": str(path),
        "container": container,
        "records": 0,
        "counts": Counter(),
        "missing_keys": Counter(),
        "required_missing": Counter(),
        "write_needed": False,
        "unsupported": False,
    }
    if records is None:
        result["unsupported"] = True
        return result

    result["records"] = len(records)
    for record in records:
        kind = classify_record(record)
        result["counts"][kind] += 1
        if kind in {"nested", "legacy_flat", "flat_missing_keys"}:
            result["write_needed"] = True
        if isinstance(record, dict):
            for field in CANONICAL_FIELDS:
                if field not in record:
                    result["missing_keys"][field] += 1
            for field in ("group_label", "group_name", "feature_label", "feature_name", "source_type"):
                if not text_or_none(record.get(field)):
                    result["required_missing"][field] += 1

    return result


def migrate_file(path: Path) -> bool:
    data = read_json(path)
    records, container = extract_records(data)
    if records is None:
        return False

    changed = False
    migrated: list[Any] = []
    for record in records:
        if not isinstance(record, dict):
            migrated.append(record)
            continue
        kind = classify_record(record)
        if kind in {"flat", "flat_missing_keys", "nested", "legacy_flat"}:
            new_record = normalize_record(record)
            migrated.append(new_record)
            if new_record != record:
                changed = True
        else:
            migrated.append(record)

    if not changed:
        return False

    if container == "list":
        write_json(path, migrated)
    else:
        data["markers"] = migrated
        write_json(path, data)
    return True


def print_summary(results: list[dict[str, Any]], root: Path) -> None:
    total_files = len(results)
    total_records = sum(int(result["records"]) for result in results)
    counts: Counter[str] = Counter()
    missing_keys: Counter[str] = Counter()
    required_missing: Counter[str] = Counter()
    unsupported = []
    write_needed = []
    unknown = []

    for result in results:
        counts.update(result["counts"])
        missing_keys.update(result["missing_keys"])
        required_missing.update(result["required_missing"])
        if result["unsupported"]:
            unsupported.append(result["path"])
        if result["write_needed"]:
            write_needed.append(result["path"])
        if result["counts"].get("unknown"):
            unknown.append(result["path"])

    print(f"Marker JSON files scanned: {total_files}")
    print(f"Marker records scanned: {total_records}")
    print("Record classes:")
    for key, value in sorted(counts.items()):
        print(f"  {key}: {value}")

    if missing_keys:
        print("Missing canonical keys:")
        for key, value in sorted(missing_keys.items()):
            print(f"  {key}: {value}")

    if required_missing:
        print("Missing required values:")
        for key, value in sorted(required_missing.items()):
            print(f"  {key}: {value}")

    if write_needed:
        print(f"Files needing migration: {len(write_needed)}")
        for path in write_needed[:20]:
            print(f"  {Path(path).relative_to(root)}")
        if len(write_needed) > 20:
            print(f"  ... {len(write_needed) - 20} more")
    else:
        print("Files needing migration: 0")

    if unknown:
        print(f"Files containing unknown records: {len(unknown)}")
        for path in unknown[:20]:
            print(f"  {Path(path).relative_to(root)}")
        if len(unknown) > 20:
            print(f"  ... {len(unknown) - 20} more")

    if unsupported:
        print(f"Unsupported candidate JSON containers: {len(unsupported)}")
        for path in unsupported[:20]:
            print(f"  {Path(path).relative_to(root)}")
        if len(unsupported) > 20:
            print(f"  ... {len(unsupported) - 20} more")


def write_report(results: list[dict[str, Any]], report_path: Path) -> None:
    rows_by_path = []
    by_directory: dict[str, Counter[str]] = defaultdict(Counter)
    for result in results:
        path = Path(result["path"])
        row = {
            "path": result["path"],
            "records": result["records"],
            "container": result["container"],
            "write_needed": result["write_needed"],
            "unsupported": result["unsupported"],
            "counts": dict(result["counts"]),
            "missing_keys": dict(result["missing_keys"]),
            "required_missing": dict(result["required_missing"]),
        }
        rows_by_path.append(row)
        by_directory[str(path.parent)].update(result["counts"])

    report = {
        "files": rows_by_path,
        "record_classes_by_directory": {
            directory: dict(counts) for directory, counts in sorted(by_directory.items())
        },
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(report_path, report)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("data"), help="Root directory to scan")
    parser.add_argument("--write", action="store_true", help="Rewrite migratable files in place")
    parser.add_argument("--report", type=Path, help="Optional JSON audit report path")
    args = parser.parse_args()

    root = args.root.resolve()
    paths = iter_marker_paths(root)
    results = [analyze_file(path) for path in paths]
    print_summary(results, root)

    if args.report:
        write_report(results, args.report)
        print(f"Wrote report: {args.report}")

    if not args.write:
        return

    changed_paths = []
    for result in results:
        if result["unsupported"] or not result["write_needed"]:
            continue
        path = Path(result["path"])
        if migrate_file(path):
            changed_paths.append(path)

    print(f"Files rewritten: {len(changed_paths)}")
    for path in changed_paths[:20]:
        print(f"  {path.relative_to(root)}")
    if len(changed_paths) > 20:
        print(f"  ... {len(changed_paths) - 20} more")


if __name__ == "__main__":
    main()
