# LLMarkers

Data and analysis for the paper *Automatic extraction and evaluation of marker genes*.

## Overview

LLMarkers studies how marker genes are reported in single-cell studies and how well LLMs can recover them.

The repository has two main parts:

- A curated benchmark from 7 human scRNA-seq studies
- A large text-extraction corpus from 504 bioRxiv preprints

The benchmark links each marker to its manuscript evidence and DEG context. This makes marker claims auditable and quantitatively grounded.

## Core dataset

LLMarkers benchmark (7 studies):

- 1,560 unique (cell type, gene) pairs
- 168 cell types
- 641 genes (Ensembl IDs)

bioRxiv extraction corpus:

- 504 preprints
- 12,501 extracted marker records
- 2,720 unique cell type names

## Repository layout

```text
data/
  adipose_Emont2022/
  adipose_Hildreth2021/
  bone_He2021/
  eye_Gautam2021/
  lung_Adams2020/
  ovary_Wagner2020/
  testis_Shamis2020/
  biorxiv/

analysis/
  benchmark_verification.ipynb
  lfc_comparison.ipynb
  selection_analysis.ipynb
  gen_strength.ipynb
  llm_extraction_eval.ipynb
  biorxiv_summary.ipynb
  biorxiv_celltype_matching.ipynb

paper/
  main.tex

docs/
  index.html
  app.js
  styles.css
  llmarkers.sqlite
```

## Website

The website is a static app in `docs/` that reads `docs/llmarkers.sqlite` directly in the browser.

It includes:

- Summary counters
- Filters for collection and source type
- Search over paper title/DOI/cell type/gene/context
- Table rows with click-to-expand context evidence

### Run locally

From repo root:

```bash
python3 scripts/build_llmarkers_sqlite.py
python3 -m http.server 8000 -d docs
```

Open:

- `http://localhost:8000`

## Deploy online (GitHub Pages)

1. Go to repo settings: `https://github.com/sbooeshaghi/llmarkers/settings/pages`
2. Under **Build and deployment**:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/docs`
3. Save

Your site will be served at:

- `https://sbooeshaghi.github.io/llmarkers/`

## SQLite build pipeline

Build command:

```bash
python3 scripts/build_llmarkers_sqlite.py
```

Output:

- `docs/llmarkers.sqlite`

Schema:

- `papers(paper_id, doi, title, year, license)`
- `markers(marker_id, paper_id, group_name, feature_name, feature_id, source_type, source_rationale, data_id)`
- `marker_metrics(marker_id, lfc, p_corr, rank)`

Current ingestion scope:

- Benchmark: `evidence_human/extracted.json` (+ DEG-linked metrics when matched)
- bioRxiv: `data/biorxiv/meca/*/markers.json`

Note: full DEG tables are not loaded into the website DB. The site is marker-focused by design.

## Data notes

- `source_type` in benchmark includes both `text` and `image`.
- bioRxiv extraction is text-based, so those rows are `text`.
- `feature_id` (Ensembl) can be missing when a paper reports aliases/protein markers or unmappable symbols.
- `Context` in the website is the evidence sentence/snippet used for each marker association.

## Related repositories

- [mrkr](https://github.com/sbooeshaghi/mrkr): LLM extraction and verification CLI
- [taln](https://github.com/sbooeshaghi/taln): token alignment utilities used in verification
