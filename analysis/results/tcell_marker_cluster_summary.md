# T-cell Marker Cluster Summary

## Assumptions

- Unit of analysis is one paper-celltype marker profile: a paper, a reported cell type label, and a binary vector of mapped Ensembl gene IDs.
- Profiles are restricted to human, source-verified marker records with at least three mapped marker genes.
- T-cell profiles are selected by the existing regex-based neighborhood assignment; mixed T/NK labels are not included in this first pass.
- Marker groups are connected components of cross-paper profiles with marker-gene Jaccard >= 0.50.
- Label relation summaries are computed across cross-paper profile pairs within each marker group.
- Dominant programs are heuristic labels based on manually specified immune-state gene modules; they are used for orientation, not as a proposed taxonomy.

## Outputs

- Figure: `analysis/figures/fig_tcell_marker_cluster_summary.pdf`
- Summary table: `analysis/results/tcell_marker_cluster_summary.tsv`
- Membership table: `analysis/results/tcell_marker_cluster_membership.tsv`

## Counts

- T-cell profiles: 256
- Papers: 132
- Reported labels: 168
- Marker groups displayed: 7

## Marker Group Summary

| component | profiles | papers | labels | dominant_program | core_marker_genes | top_labels | exact_label_fraction | partial_label_fraction | different_label_fraction | mean_internal_jaccard |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 32 | 24 | 28 | Naive/memory | CCR7; SELL; TCF7 | NAIVE T CELL (2); TCM (2); CD4+ T CELL (2); NAIVE CD4+ T CELL (2); CEFX-SPECIFIC BRAIN METASTASIS-INFILTRATING PD-1+ CD8+ T CELL (1); NAIVE T CELLS OR TCMS (1) | 0.012 | 0.469 | 0.519 | 0.448 |
| 2 | 31 | 27 | 22 | Exhaustion | CTLA4; TIGIT | TREG (10); CD8+ EXHAUSTED T CELL (TEXH) (1); EXHAUSTED CD8 T CELL (1); CD4+ T CELL (1); REGULATORY T CELL (1); EXHAUSTED T CELL (1) | 0.100 | 0.371 | 0.529 | 0.222 |
| 3 | 19 | 16 | 18 | Cytotoxic | GZMB; PRF1 | CYTOTOXIC T CELL (2); CD4-CTLS (1); MAIT (1); CD8+ T CELLS (1); GZMH+ CD8+ T CELL (1); CD8.3 (1) | 0.006 | 0.399 | 0.595 | 0.255 |
| 4 | 15 | 14 | 4 | Other | CD3D; CD3E; CD3G | T CELL (11); T CELLS (2); T-CELL (1); CD4 AND CD8 T CELLS (1) | 0.635 | 0.019 | 0.346 | 0.472 |
| 5 | 9 | 8 | 4 | Other | CD8A; CD3E; CD4 | T CELL (6); T CELL CLUSTER (1); T-CELL (1); CD4+ AND CD8+ T CELL (1) | 0.600 | 0.371 | 0.029 | 0.416 |
| 6 | 4 | 4 | 4 | Residency | CD69; ITGAE; CXCR6; ZNF683; ITGA1 | CD4+ TISSUE RESIDENT MEMORY T CELL (TRM) (1); CD8.4 (1); CD8+ T CELL (1); TISSUE RESIDENT MEMORY T (TRM) CELL (1) | 0.000 | 0.667 | 0.333 | 0.364 |
| 7 | 4 | 3 | 4 | Cytotoxic | CCL4; GZMA; IFNG; GZMH; PRF1; CCL5; CCL3; EOMES | CD4.7 (1); CD8+GZMB (1); CD8+GZMK (1); EFFECTOR CD8+ T CELLS (1) | 0.000 | 1.000 | 0.000 | 0.532 |
