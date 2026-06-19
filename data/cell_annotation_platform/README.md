# Cell Annotation Platform Ingest

This directory contains Cell Annotation Platform (CAP) source files and normalized marker records for local/global marker analyses.

## Source Files

- `cap-datasets.json`: local manifest of CAP project/dataset pages to ingest. The current file is refreshed from the live CAP datasets page and contains 109 datasets.
- `cell-labels-2026-06-10.csv`: aggregate CAP cell-label export. This is useful for label review, but it is not used as the source for local/global marker analysis because it is already aggregated across studies.
- `datasets/`: one folder per CAP project/dataset. Each folder contains:
  - `dataset_metadata.json`: manifest entry for the dataset.
  - `download_urls.json`: public CAP download URLs returned by the CAP GraphQL API.
  - `cap.json`: extracted CAP-JSON file.
  - `markers.json`: normalized LLMarkers-style marker records for that dataset.
- `markers.json`: combined normalized marker records from all per-dataset `markers.json` files.
- `cap_download_manifest.tsv`: download/extraction audit table.
- `cap_marker_summary.tsv`: per-dataset marker summary table.
- `anndata/`: ignored CAP expression downloads used by the liver local/global
  DE analysis. The expected URLs, filenames, sizes, and SHA-256 checksums are
  recorded in `anndata/README.md`.

## Normalized Schema

The CAP records are written in the flat LLMarkers marker-record format:

```json
{
  "organism": "homo_sapiens",
  "group_label": "Hepatocytes",
  "group_name": "HEPATOCYTES",
  "group_id": "CL:0000182",
  "feature_label": "BAAT",
  "feature_name": "BAAT",
  "feature_id": "ENSG00000136881",
  "source_type": "cap",
  "source_rationale": "...",
  "source_id": "https://celltype.info/project/618/dataset/1438/labelset/author_cell_type",
  "data_id": "CAP:618:1438",
  "metrics_pcorr": null,
  "metrics_logfc": null,
  "metrics_rank": null
}
```

CAP-specific provenance is preserved in underscore-prefixed fields such as `_cap_dataset_name`, `_cap_labelset_name`, `_cap_ontology_term_id`, `_cap_synonyms`, and `_cap_marker_role`.

## Gene Mapping

Human gene symbols are mapped to Ensembl IDs with the `mrkr` gene map when available at:

```bash
../mrkr/mrkr/data/gmap.txt
```

The current mapping logic only assigns Ensembl IDs for `homo_sapiens` CAP records. Mouse and mixed-organism records retain normalized gene symbols with `feature_id: null`.

## Rebuild

Download CAP-JSON files and regenerate all normalized outputs:

```bash
uv run --locked python analysis/scripts/ingest_cap_datasets.py
```

Refresh the manifest from the live CAP datasets page before rebuilding:

```bash
uv run --locked python analysis/scripts/ingest_cap_datasets.py --refresh-manifest
```

Refresh only the manifest:

```bash
uv run --locked python analysis/scripts/ingest_cap_datasets.py --refresh-manifest --manifest-only
```

Normalize files already present on disk without network access:

```bash
uv run --locked python analysis/scripts/ingest_cap_datasets.py --no-download
```

Use a different gene map:

```bash
uv run --locked python analysis/scripts/ingest_cap_datasets.py --gene-map /path/to/gmap.txt
```

## Current Ingest Summary

- Manifest datasets: 109
- Datasets with CAP JSON downloads: 104
- Datasets with normalized marker records: 99
- Combined marker records: 32,097
- Human marker records: 9,241
- Human marker records with Ensembl IDs: 8,899
- Mouse marker records: 22,680
- Mixed-organism marker records: 176

Five datasets are listed on the CAP datasets page but currently do not expose `capJsonUrlZip` through the public CAP download URL API. Five downloaded zero-record datasets have CAP `cell-labels` entries but no marker genes.
One already-extracted legacy dataset (`project_613_dataset_1426...`) lacks a
saved `download_urls.json`, so its CAP-JSON zip URL is blank in
`cap_download_manifest.tsv` until the manifest is refreshed from the live API.
