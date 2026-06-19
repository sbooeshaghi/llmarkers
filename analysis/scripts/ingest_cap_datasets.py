from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
import time
import unicodedata
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[2]
CAP_DIR = REPO_ROOT / "data" / "cell_annotation_platform"
DEFAULT_MANIFEST = CAP_DIR / "cap-datasets.json"
DEFAULT_OUT_DIR = CAP_DIR / "datasets"
DEFAULT_COMBINED_MARKERS = CAP_DIR / "markers.json"
DEFAULT_SUMMARY = CAP_DIR / "cap_marker_summary.tsv"
DEFAULT_STUDY_METADATA = CAP_DIR / "cap_study_metadata.tsv"
DEFAULT_DOWNLOAD_MANIFEST = CAP_DIR / "cap_download_manifest.tsv"
DEFAULT_GENE_MAP = REPO_ROOT.parent / "mrkr" / "mrkr" / "data" / "gmap.txt"

DOWNLOAD_URLS_QUERY = """query DownloadUrls($datasetId: ID!) {
  downloadUrls(datasetId: $datasetId) {
    isAnnDataUrlUpToDate
    annDataUrl
    seuratUrl
    capJsonUrlZip
    capJsonUrlTar
    __typename
  }
}"""

SEARCH_DATASETS_QUERY = """query SearchDatasets($options: DatasetSearchOptions, $search: LookupDatasetsSearchInput, $filter: LookupDatasetsFiltersInput, $labelsetNames: [String!]) {
  results: lookupDatasets(options: $options, search: $search, filter: $filter) {
    id
    name
    ...DatasetResult
    __typename
  }
}

fragment ProjectAuthors_project on Project {
  version
  owner {
    uid
    displayName
    avatarUrl
    __typename
  }
  permissions {
    id
    role
    isActive
    isContactPerson
    user {
      uid
      displayName
      avatarUrl
      __typename
    }
    __typename
  }
  externalAuthors {
    uid
    name
    email
    isContactPerson
    __typename
  }
  __typename
}

fragment DatasetResult on Dataset {
  id
  name
  consortiumTags {
    id
    title
    logoUrl
    sortOrder
    __typename
  }
  cellCount
  labelsets(names: $labelsetNames) {
    id
    name
    labels {
      id
      name
      count
      __typename
    }
    __typename
  }
  scores {
    total
    __typename
  }
  project {
    id
    name
    createdAt
    ...ProjectAuthors_project
    __typename
  }
  __typename
}"""


ORGANISM_LABELS = {
    "Homo sapiens": "homo_sapiens",
    "Mus musculus": "mus_musculus",
    "Macaca mulatta": "macaca_mulatta",
    "Rattus norvegicus": "rattus_norvegicus",
    "Danio rerio": "danio_rerio",
}

GREEK_CHAR_MAP = str.maketrans(
    {
        "Α": "A",
        "α": "A",
        "Β": "B",
        "β": "B",
        "Γ": "G",
        "γ": "G",
    }
)

DASH_CHAR_MAP = str.maketrans(
    {
        "‐": "-",
        "‑": "-",
        "‒": "-",
        "–": "-",
        "—": "-",
        "−": "-",
    }
)

GENE_ALIASES = {
    "ADAR-P150": "ADAR",
    "BDCA-2": "CLEC4C",
    "DESMIN": "DES",
    "DNASE13": "DNASE1L3",
    "ECAD": "CDH1",
    "KI67": "MKI67",
    "MIK67": "MKI67",
    "NEPHRIN": "NPHS1",
    "PECAM": "PECAM1",
    "PDGRB": "PDGFRB",
    "RSG10": "RGS10",
    "SCL17A7": "SLC17A7",
    "VISG4": "VSIG4",
}

DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s,;\"'<>]+", re.IGNORECASE)
DOI_MISSING_LEADING_ONE_RE = re.compile(r"\b0\.(?=\d{4,9}/)", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Cell Annotation Platform CAP-JSON files and normalize marker records."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--combined-markers", type=Path, default=DEFAULT_COMBINED_MARKERS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--study-metadata", type=Path, default=DEFAULT_STUDY_METADATA)
    parser.add_argument("--download-manifest", type=Path, default=DEFAULT_DOWNLOAD_MANIFEST)
    parser.add_argument(
        "--gene-map",
        type=Path,
        default=DEFAULT_GENE_MAP if DEFAULT_GENE_MAP.exists() else None,
        help="Optional mrkr gmap.txt file for human gene symbol to Ensembl ID mapping.",
    )
    parser.add_argument("--no-download", action="store_true", help="Only normalize CAP JSON files already on disk.")
    parser.add_argument("--force-download", action="store_true", help="Re-download CAP JSON zip files.")
    parser.add_argument(
        "--refresh-manifest",
        action="store_true",
        help="Refresh the manifest from the public CAP datasets search before ingesting.",
    )
    parser.add_argument(
        "--manifest-only",
        action="store_true",
        help="Refresh/write the manifest and exit without downloading or normalizing datasets.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Limit the number of manifest datasets processed.")
    parser.add_argument("--sleep", type=float, default=0.15, help="Delay between network requests in seconds.")
    return parser.parse_args()


def read_json(path: Path) -> Any:
    with path.open() as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as handle:
        json.dump(data, handle, indent=2, sort_keys=False)
        handle.write("\n")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def normalize_group_name(value: Any) -> str | None:
    text = normalize_text(value)
    return text.upper() if text else None


def normalize_gene_name(value: Any) -> str | None:
    text = normalize_text(value)
    if not text:
        return None
    return text.upper()


def normalize_gene_key(value: str) -> str:
    key = unicodedata.normalize("NFKC", value or "")
    key = key.translate(DASH_CHAR_MAP)
    key = key.translate(GREEK_CHAR_MAP)
    key = key.upper().strip()
    key = " ".join(key.split())
    return key


def extract_dois(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        raw_values = value
    else:
        raw_values = [value]

    dois: list[str] = []
    seen: set[str] = set()
    for raw_value in raw_values:
        text = normalize_text(raw_value)
        if not text or text.upper() == "NA":
            continue
        text = DOI_MISSING_LEADING_ONE_RE.sub("10.", text)
        for match in DOI_RE.finditer(text):
            doi = match.group(0).strip().rstrip(".);]")
            if doi and doi not in seen:
                seen.add(doi)
                dois.append(doi)
    return dois


def candidate_gene_keys(value: str) -> list[str]:
    base = normalize_gene_key(value)
    if not base:
        return []
    candidates: list[str] = []

    def add(key: str) -> None:
        if key and key not in candidates:
            candidates.append(key)

    add(base)
    compact = base.replace(" ", "")
    add(compact)
    if "-" in compact:
        add(compact.replace("-", ""))
    for key in list(candidates):
        alias = GENE_ALIASES.get(key)
        if alias:
            add(normalize_gene_key(alias))
    return candidates


def load_gene_map(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
    gene_map: dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 2:
                continue
            gene_name, ensembl_id = parts
            gene_map[normalize_gene_key(gene_name)] = ensembl_id
    return gene_map


def resolve_gene_id(gene_name: str, gene_map: dict[str, str]) -> str | None:
    if gene_name.startswith("ENSG"):
        return gene_name
    for key in candidate_gene_keys(gene_name):
        ensembl_id = gene_map.get(key)
        if ensembl_id:
            return ensembl_id
    return None


def normalize_organism(values: list[str]) -> str:
    names = [ORGANISM_LABELS.get(value, normalize_text(value).lower().replace(" ", "_")) for value in values if value]
    unique = sorted(set(names))
    if len(unique) == 1:
        return unique[0]
    if unique:
        return "mixed"
    return "unknown"


def slugify(value: str, max_len: int = 80) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug[:max_len].strip("-") or "dataset"


def dataset_ids(url: str) -> tuple[str, str]:
    match = re.search(r"/project/([^/]+)/dataset/([^/?#]+)", url)
    if not match:
        raise ValueError(f"Could not parse CAP project/dataset IDs from URL: {url}")
    return match.group(1), match.group(2)


def dataset_dir(out_dir: Path, entry: dict[str, Any]) -> Path:
    project_id, dataset_id = dataset_ids(entry["url"])
    return out_dir / f"project_{project_id}_dataset_{dataset_id}_{slugify(entry['name'])}"


def post_graphql(
    operation_name: str,
    query: str,
    variables: dict[str, Any],
    extensions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = json.dumps(
        {
            "operationName": operation_name,
            "query": query,
            "variables": variables,
            **({"extensions": extensions} if extensions else {}),
        }
    ).encode()
    request = urllib.request.Request(
        "https://celltype.info/graphql",
        data=payload,
        headers={
            "content-type": "application/json",
            "origin": "https://celltype.info",
            "referer": "https://celltype.info/",
            "user-agent": "llmarkers-cap-ingest/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode())


def labelset_values(dataset: dict[str, Any], name: str) -> list[str]:
    values: list[str] = []
    for labelset in dataset.get("labelsets") or []:
        if labelset.get("name") != name:
            continue
        for label in labelset.get("labels") or []:
            label_name = normalize_text(label.get("name"))
            if label_name:
                values.append(label_name)
    return values


def cap_dataset_manifest_entry(dataset: dict[str, Any]) -> dict[str, Any]:
    project = dataset.get("project") or {}
    project_id = normalize_text(project.get("id"))
    dataset_id = normalize_text(dataset.get("id"))
    return {
        "name": normalize_text(dataset.get("name")),
        "organisms": labelset_values(dataset, "organism"),
        "tissue": labelset_values(dataset, "tissue"),
        "assay": labelset_values(dataset, "assay"),
        "disease": labelset_values(dataset, "disease"),
        "cell_count": dataset.get("cellCount"),
        "feedback_count": (dataset.get("scores") or {}).get("total"),
        "project_id": project_id,
        "dataset_id": dataset_id,
        "project_name": normalize_text(project.get("name")),
        "project_created_at": normalize_text(project.get("createdAt")),
        "url": f"https://celltype.info/project/{project_id}/dataset/{dataset_id}",
    }


def fetch_cap_datasets_manifest(limit: int = 120) -> list[dict[str, Any]]:
    variables = {
        "options": {"limit": limit, "offset": 0, "sort": []},
        "search": {"name": ""},
        "filter": {"metadata": []},
        "labelsetNames": ["organism", "tissue", "disease", "assay"],
    }
    response = post_graphql(
        "SearchDatasets",
        SEARCH_DATASETS_QUERY,
        variables,
        extensions={"clientLibrary": {"name": "@apollo/client", "version": "4.0.9"}},
    )
    if response.get("errors"):
        raise RuntimeError(json.dumps(response["errors"]))
    results = response["data"]["results"]
    entries = [cap_dataset_manifest_entry(dataset) for dataset in results]
    # Stable de-duplication in case the backend ever returns duplicate rows.
    unique_entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for entry in entries:
        if entry["url"] in seen:
            continue
        seen.add(entry["url"])
        unique_entries.append(entry)
    return unique_entries


def download_file(url: str, path: Path) -> None:
    request = urllib.request.Request(url, headers={"user-agent": "llmarkers-cap-ingest/1.0"})
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request, timeout=180) as response, path.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def find_local_download(url: str) -> Path | None:
    basename = Path(urlparse(url).path).name
    candidate = CAP_DIR / basename
    if candidate.exists():
        return candidate
    return None


def extract_cap_json(zip_path: Path, cap_json_path: Path) -> str:
    with zipfile.ZipFile(zip_path) as archive:
        json_names = [name for name in archive.namelist() if name.endswith(".json")]
        if not json_names:
            raise ValueError(f"No JSON file found inside {zip_path}")
        # CAP zip files should contain one JSON file. If there are several, the largest is most likely the dataset.
        json_name = max(json_names, key=lambda name: archive.getinfo(name).file_size)
        cap_json_path.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(json_name) as source, cap_json_path.open("wb") as target:
            shutil.copyfileobj(source, target)
        return json_name


def load_dataset_organisms(cap_json: dict[str, Any], manifest_entry: dict[str, Any]) -> list[str]:
    organisms = [normalize_text(value) for value in manifest_entry.get("organisms", []) if normalize_text(value)]
    for labelset in cap_json.get("labelsets", []):
        if labelset.get("name") != "organism":
            continue
        for label in labelset.get("labels") or []:
            name = normalize_text(label.get("name"))
            if name:
                organisms.append(name)
    return sorted(set(organisms))


def split_marker_genes(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        raw_values = value
    else:
        raw_values = re.split(r"[,;]", str(value))
    genes: list[str] = []
    seen: set[str] = set()
    for raw in raw_values:
        gene = normalize_gene_name(raw)
        if not gene or gene == "UNKNOWN":
            continue
        if gene not in seen:
            seen.add(gene)
            genes.append(gene)
    return genes


def normalize_markers(
    cap_json: dict[str, Any],
    manifest_entry: dict[str, Any],
    gene_map: dict[str, str],
) -> list[dict[str, Any]]:
    project_id, dataset_id = dataset_ids(manifest_entry["url"])
    organisms = load_dataset_organisms(cap_json, manifest_entry)
    organism = normalize_organism(organisms)
    tissues = [normalize_text(value) for value in manifest_entry.get("tissue", []) if normalize_text(value)]
    dataset_name = normalize_text(cap_json.get("name")) or normalize_text(manifest_entry["name"])
    dataset_url = normalize_text(manifest_entry["url"])
    data_id = f"CAP:{project_id}:{dataset_id}"

    records: list[dict[str, Any]] = []
    for labelset in cap_json.get("labelsets", []):
        if labelset.get("mode") != "cell-labels":
            continue
        labelset_name = normalize_text(labelset.get("name"))
        source_id = f"{dataset_url}/labelset/{labelset_name}" if labelset_name else dataset_url

        for label in labelset.get("labels") or []:
            group_label = normalize_text(label.get("name"))
            if not group_label:
                continue
            marker_genes = split_marker_genes(label.get("markerGenes"))
            if not marker_genes:
                continue
            canonical_marker_genes = set(split_marker_genes(label.get("canonicalMarkerGenes")))
            group_id = normalize_text(label.get("ontologyTermId")) or None
            rationale = normalize_text(label.get("rationale")) or None
            raw_rationale_dois = label.get("rationaleDois") or []
            normalized_rationale_dois = extract_dois(raw_rationale_dois)

            for gene in marker_genes:
                feature_id = resolve_gene_id(gene, gene_map) if organism == "homo_sapiens" else None
                record = {
                    "organism": organism,
                    "group_label": group_label,
                    "group_name": normalize_group_name(group_label),
                    "group_id": group_id,
                    "feature_label": gene,
                    "feature_name": gene,
                    "feature_id": feature_id,
                    "source_type": "cap",
                    "source_rationale": rationale,
                    "source_id": source_id,
                    "data_id": data_id,
                    "metrics_pcorr": None,
                    "metrics_logfc": None,
                    "metrics_rank": None,
                    "_cap_project_id": project_id,
                    "_cap_dataset_id": dataset_id,
                    "_cap_dataset_name": dataset_name,
                    "_cap_dataset_url": dataset_url,
                    "_cap_cell_count": cap_json.get("cellCount"),
                    "_cap_gene_count": cap_json.get("geneCount"),
                    "_cap_organisms": organisms,
                    "_cap_tissues": tissues,
                    "_cap_labelset_name": labelset_name or None,
                    "_cap_label_count": label.get("count"),
                    "_cap_label_color": label.get("color"),
                    "_cap_label_full_name": normalize_text(label.get("fullName")) or None,
                    "_cap_ontology_term_exists": label.get("ontologyTermExists"),
                    "_cap_ontology_term_id": group_id,
                    "_cap_ontology_term": normalize_text(label.get("ontologyTerm")) or None,
                    "_cap_category_full_name": normalize_text(label.get("categoryFullName")) or None,
                    "_cap_category_ontology_term_id": normalize_text(label.get("categoryOntologyTermId")) or None,
                    "_cap_category_ontology_term": normalize_text(label.get("categoryOntologyTerm")) or None,
                    "_cap_synonyms": label.get("synonyms") or [],
                    "_cap_rationale_dois": raw_rationale_dois,
                    "_cap_rationale_dois_normalized": normalized_rationale_dois,
                    "_cap_marker_role": "canonical" if gene in canonical_marker_genes else "reported",
                }
                records.append(record)
    return records


def process_download(entry: dict[str, Any], study_dir: Path, force: bool) -> dict[str, Any]:
    project_id, dataset_id = dataset_ids(entry["url"])
    download_info_path = study_dir / "download_urls.json"
    cap_json_path = study_dir / "cap.json"
    status: dict[str, Any] = {
        "project_id": project_id,
        "dataset_id": dataset_id,
        "name": entry["name"],
        "url": entry["url"],
        "study_dir": str(study_dir.relative_to(REPO_ROOT)),
        "cap_json": str(cap_json_path.relative_to(REPO_ROOT)) if cap_json_path.exists() else "",
        "cap_json_zip_url": "",
        "cap_json_zip": "",
        "download_status": "not_requested",
        "error": "",
    }

    if cap_json_path.exists() and not force:
        status["download_status"] = "already_extracted"
        status["cap_json"] = str(cap_json_path.relative_to(REPO_ROOT))
        fill_download_info_from_disk(study_dir, status)
        return status

    try:
        response = post_graphql("DownloadUrls", DOWNLOAD_URLS_QUERY, {"datasetId": dataset_id})
        if response.get("errors"):
            raise RuntimeError(json.dumps(response["errors"]))
        urls = response["data"]["downloadUrls"]
        write_json(download_info_path, urls)
        zip_url = urls.get("capJsonUrlZip")
        status["cap_json_zip_url"] = zip_url or ""
        if not zip_url:
            status["download_status"] = "missing_cap_json_url"
            return status

        zip_name = Path(urlparse(zip_url).path).name
        zip_path = study_dir / zip_name
        if zip_path.exists() and not force:
            status["download_status"] = "already_downloaded"
        else:
            local_download = find_local_download(zip_url)
            if local_download and not force:
                shutil.copy2(local_download, zip_path)
                status["download_status"] = "copied_existing_root_download"
            else:
                download_file(zip_url, zip_path)
                status["download_status"] = "downloaded"
        extract_cap_json(zip_path, cap_json_path)
        status["cap_json_zip"] = str(zip_path.relative_to(REPO_ROOT))
        status["cap_json"] = str(cap_json_path.relative_to(REPO_ROOT))
    except (urllib.error.URLError, TimeoutError, RuntimeError, KeyError, ValueError, zipfile.BadZipFile) as exc:
        status["download_status"] = "failed"
        status["error"] = str(exc)
    return status


def process_existing(entry: dict[str, Any], study_dir: Path) -> dict[str, Any]:
    project_id, dataset_id = dataset_ids(entry["url"])
    cap_json_path = study_dir / "cap.json"
    status = {
        "project_id": project_id,
        "dataset_id": dataset_id,
        "name": entry["name"],
        "url": entry["url"],
        "study_dir": str(study_dir.relative_to(REPO_ROOT)),
        "cap_json": str(cap_json_path.relative_to(REPO_ROOT)) if cap_json_path.exists() else "",
        "cap_json_zip_url": "",
        "cap_json_zip": "",
        "download_status": "not_found",
        "error": "",
    }
    if cap_json_path.exists():
        status["download_status"] = "already_extracted"
        fill_download_info_from_disk(study_dir, status)
        return status

    root_json_candidates = sorted(CAP_DIR.glob(f"*_{dataset_id}.h5ad.json"))
    if root_json_candidates:
        shutil.copy2(root_json_candidates[0], cap_json_path)
        status["download_status"] = "copied_existing_root_json"
        status["cap_json"] = str(cap_json_path.relative_to(REPO_ROOT))
        return status

    root_zip_candidates = sorted(CAP_DIR.glob(f"*_{dataset_id}.h5ad.json.zip"))
    if root_zip_candidates:
        zip_path = study_dir / root_zip_candidates[0].name
        shutil.copy2(root_zip_candidates[0], zip_path)
        extract_cap_json(zip_path, cap_json_path)
        status["download_status"] = "copied_existing_root_zip"
        status["cap_json_zip"] = str(zip_path.relative_to(REPO_ROOT))
        status["cap_json"] = str(cap_json_path.relative_to(REPO_ROOT))
    return status


def fill_download_info_from_disk(study_dir: Path, status: dict[str, Any]) -> None:
    download_info_path = study_dir / "download_urls.json"
    if download_info_path.exists():
        try:
            urls = json.loads(download_info_path.read_text())
        except json.JSONDecodeError as exc:
            status["error"] = f"could not parse download_urls.json: {exc}"
        else:
            status["cap_json_zip_url"] = urls.get("capJsonUrlZip") or ""

    if not status.get("cap_json_zip"):
        zip_candidates = sorted(study_dir.glob("*.json.zip"))
        if zip_candidates:
            status["cap_json_zip"] = str(zip_candidates[0].relative_to(REPO_ROOT))


def write_download_manifest(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "project_id",
        "dataset_id",
        "name",
        "url",
        "study_dir",
        "cap_json",
        "cap_json_zip_url",
        "cap_json_zip",
        "download_status",
        "error",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_summary(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "project_id",
        "dataset_id",
        "dataset_name",
        "organism",
        "n_labelsets",
        "n_labels_with_markers",
        "n_marker_records",
        "n_unique_groups",
        "n_unique_features",
        "markers_path",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_study_metadata(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "project_id",
        "dataset_id",
        "project_name",
        "dataset_name",
        "url",
        "organism",
        "organisms",
        "tissues",
        "assays",
        "diseases",
        "cell_count",
        "gene_count",
        "n_labelsets",
        "n_labels_with_markers",
        "n_marker_records",
        "n_unique_groups",
        "n_unique_features",
        "n_rationale_dois",
        "rationale_dois",
        "markers_path",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    if args.refresh_manifest:
        manifest = fetch_cap_datasets_manifest()
        write_json(args.manifest, manifest)
        print(f"Wrote {len(manifest):,} CAP dataset manifest entries to {args.manifest.relative_to(REPO_ROOT)}")
        if args.manifest_only:
            return

    manifest = read_json(args.manifest)
    if args.limit is not None:
        manifest = manifest[: args.limit]

    all_records: list[dict[str, Any]] = []
    download_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    study_metadata_rows: list[dict[str, Any]] = []
    gene_map = load_gene_map(args.gene_map)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    for idx, entry in enumerate(manifest, start=1):
        study_dir = dataset_dir(args.out_dir, entry)
        study_dir.mkdir(parents=True, exist_ok=True)
        write_json(study_dir / "dataset_metadata.json", entry)

        if args.no_download:
            download_status = process_existing(entry, study_dir)
        else:
            download_status = process_download(entry, study_dir, args.force_download)
        download_rows.append(download_status)

        cap_json_path = study_dir / "cap.json"
        if not cap_json_path.exists():
            print(f"[{idx}/{len(manifest)}] missing CAP JSON: {entry['name']}", file=sys.stderr)
            if not args.no_download and args.sleep:
                time.sleep(args.sleep)
            continue

        cap_json = read_json(cap_json_path)
        records = normalize_markers(cap_json, entry, gene_map)
        write_json(study_dir / "markers.json", records)
        all_records.extend(records)

        project_id, dataset_id = dataset_ids(entry["url"])
        organisms = load_dataset_organisms(cap_json, entry)
        tissues = [normalize_text(value) for value in entry.get("tissue", []) if normalize_text(value)]
        assays = [normalize_text(value) for value in entry.get("assay", []) if normalize_text(value)]
        diseases = [normalize_text(value) for value in entry.get("disease", []) if normalize_text(value)]
        labelsets = [labelset for labelset in cap_json.get("labelsets", []) if labelset.get("mode") == "cell-labels"]
        labels_with_markers = {
            (labelset.get("name"), label.get("name"))
            for labelset in labelsets
            for label in (labelset.get("labels") or [])
            if split_marker_genes(label.get("markerGenes"))
        }
        summary_rows.append(
            {
                "project_id": project_id,
                "dataset_id": dataset_id,
                "dataset_name": normalize_text(cap_json.get("name")) or normalize_text(entry["name"]),
                "organism": normalize_organism(organisms),
                "n_labelsets": len(labelsets),
                "n_labels_with_markers": len(labels_with_markers),
                "n_marker_records": len(records),
                "n_unique_groups": len({record["group_name"] for record in records}),
                "n_unique_features": len({record["feature_name"] for record in records}),
                "markers_path": str((study_dir / "markers.json").relative_to(REPO_ROOT)),
            }
        )
        rationale_dois = sorted(
            {
                doi
                for record in records
                for doi in record.get("_cap_rationale_dois_normalized", [])
            }
        )
        study_metadata_rows.append(
            {
                "project_id": project_id,
                "dataset_id": dataset_id,
                "project_name": normalize_text(entry.get("project_name")),
                "dataset_name": normalize_text(cap_json.get("name")) or normalize_text(entry["name"]),
                "url": normalize_text(entry.get("url")),
                "organism": normalize_organism(organisms),
                "organisms": "; ".join(organisms),
                "tissues": "; ".join(tissues),
                "assays": "; ".join(assays),
                "diseases": "; ".join(diseases),
                "cell_count": cap_json.get("cellCount"),
                "gene_count": cap_json.get("geneCount"),
                "n_labelsets": len(labelsets),
                "n_labels_with_markers": len(labels_with_markers),
                "n_marker_records": len(records),
                "n_unique_groups": len({record["group_name"] for record in records}),
                "n_unique_features": len({record["feature_name"] for record in records}),
                "n_rationale_dois": len(rationale_dois),
                "rationale_dois": "; ".join(rationale_dois),
                "markers_path": str((study_dir / "markers.json").relative_to(REPO_ROOT)),
            }
        )
        print(f"[{idx}/{len(manifest)}] normalized {len(records):,} marker records: {entry['name']}")

        if not args.no_download and args.sleep:
            time.sleep(args.sleep)

    write_json(args.combined_markers, all_records)
    write_download_manifest(args.download_manifest, download_rows)
    write_summary(args.summary, summary_rows)
    write_study_metadata(args.study_metadata, study_metadata_rows)

    print(f"Wrote {len(all_records):,} CAP marker records to {args.combined_markers.relative_to(REPO_ROOT)}")
    print(f"Wrote download manifest to {args.download_manifest.relative_to(REPO_ROOT)}")
    print(f"Wrote summary to {args.summary.relative_to(REPO_ROOT)}")
    print(f"Wrote study metadata to {args.study_metadata.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
