# LLMarker

Data and analysis for "Automatic extraction and evaluation of marker genes".

## Motivation

In single-cell biology, marker genes are reported as binary associations, e.g. gene X marks cell type Y. This is practical but lossy---the quantitative evidence behind each marker (fold change, rank, which DEG table it came from) is discarded. When different studies use different names for the same cell type, or the same name for different biology, the binary form makes it hard to tell what a marker actually means.

## What is LLMarker?

LLMarker is a benchmark of **1,560 cell type--gene pairs** from seven human scRNA-seq studies across six tissues. Each pair is linked to:

- The **sentence or figure** where the authors reported it
- The **specific DEG table** it was derived from, with fold change and rank

This lets us ask how strong are the markers that authors choose to highlight? And can LLMs recover them?

## Key findings

- Authors select strong markers (median rank 40 in DEG lists), but a simple rank cutoff recovers at best half of them. Marker selection is not reducible to a threshold.
- LLMs encode real cell type--gene associations, but **generating** or **selecting** markers from DEG lists yields low agreement with author-curated markers (mean pair F1 ~0.2).
- LLM-based **extraction** from manuscript text recovers author-specific markers with much higher fidelity (mean pair F1 ~0.67).
- Applied to 504 bioRxiv preprints, extraction yielded 12,501 marker associations across 2,720 cell type names. Clustering on extracted markers recovered known immune cell hierarchies despite variable nomenclature.

## Repository structure

```
data/
  adipose_Emont2022/       # 7 benchmark datasets
  adipose_Hildreth2021/
  bone_He2021/
  eye_Gautam2021/
  lung_Adams2020/
  ovary_Wagner2020/
  testis_Shamis2020/
  biorxiv/                 # 504 bioRxiv preprint extractions

analysis/                  # Jupyter notebooks and scripts
  benchmark_verification.ipynb   # Table 1: benchmark statistics
  lfc_comparison.ipynb           # Figures 1-2: marker strength analysis
  selection_analysis.ipynb       # Figure 3: LLM curation tradeoff
  gen_strength.ipynb             # Generation analysis
  llm_extraction_eval.ipynb      # Extraction evaluation
  biorxiv_celltype_matching.ipynb # bioRxiv clustering analysis
  biorxiv_summary.ipynb          # bioRxiv summary statistics
  make_fig_selection.py          # Selection sweep figure
```

## Dataset structure

Each benchmark dataset contains:

```
evidence_human/      # Human-curated markers (text + figure)
evidence_deg/        # DEG tables from supplementary data
evidence_llm/        # LLM-extracted markers from manuscript text
evidence_generated/  # LLM-generated markers (no manuscript)
evidence_selected/   # LLM-selected markers from top-N DEGs
evidence_predicted/  # LLM cell type predictions
manuscript/          # Manuscript text and figures
metadata.json        # DOI and citation
spec.tsv             # DEG table → cell type mapping
```

Evidence files use a shared JSON schema with fields: `organism`, `group_label`, `group_name`, `group_id`, `feature_label`, `feature_name`, `feature_id`, `source_type`, `source_rationale`, `source_id`, `data_id`, and `metrics_*` (rank, log fold change, p-value from the matched DEG entry).

## Related repositories

- [mrkr](https://github.com/sbooeshaghi/mrkr) -- CLI tool for LLM-based marker gene extraction and verification
- [taln](https://github.com/sbooeshaghi/taln) -- Token alignment library used to verify extracted text against source manuscripts
