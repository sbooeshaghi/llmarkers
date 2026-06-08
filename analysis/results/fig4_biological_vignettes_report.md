# Figure 4 Biological Vignettes Prototype

This figure uses marker-derived T-cell and myeloid clusters as biological examples for the formal essential/exchangeable marker result.
Figure: `analysis/figures/fig4_biological_vignettes.pdf`

## T-cell Marker Clusters

| cluster | profiles | papers | labels | dominant_program | core_marker_genes | top_labels |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 32 | 24 | 28 | Naive/memory | CCR7; SELL; TCF7 | NAIVE T CELL (2); TCM (2); CD4+ T CELL (2); NAIVE CD4+ T CELL (2); CEFX-SPECIFIC BRAIN METASTASIS-INFILTRATING PD-1+ CD8+ T CELL (1); NAIVE T CELLS OR TCMS (1) |
| C2 | 31 | 27 | 22 | Exhaustion | CTLA4; TIGIT | TREG (10); CD8+ EXHAUSTED T CELL (TEXH) (1); EXHAUSTED CD8 T CELL (1); CD4+ T CELL (1); REGULATORY T CELL (1); EXHAUSTED T CELL (1) |
| C3 | 19 | 16 | 18 | Cytotoxic | GZMB; PRF1 | CYTOTOXIC T CELL (2); CD4-CTLS (1); MAIT (1); CD8+ T CELLS (1); GZMH+ CD8+ T CELL (1); CD8.3 (1) |
| C4 | 15 | 14 | 4 | Other | CD3D; CD3E; CD3G | T CELL (11); T CELLS (2); T-CELL (1); CD4 AND CD8 T CELLS (1) |
| C5 | 9 | 8 | 4 | Other | CD8A; CD3E; CD4 | T CELL (6); T CELL CLUSTER (1); T-CELL (1); CD4+ AND CD8+ T CELL (1) |
| C6 | 4 | 4 | 4 | Residency | CD69; ITGAE; CXCR6; ZNF683; ITGA1 | CD4+ TISSUE RESIDENT MEMORY T CELL (TRM) (1); CD8.4 (1); CD8+ T CELL (1); TISSUE RESIDENT MEMORY T (TRM) CELL (1) |
| C7 | 4 | 3 | 4 | Cytotoxic | CCL4; GZMA; IFNG; GZMH; PRF1; CCL5; CCL3; EOMES | CD4.7 (1); CD8+GZMB (1); CD8+GZMK (1); EFFECTOR CD8+ T CELLS (1) |

## Myeloid Marker Clusters

| cluster | profiles | papers | labels | dominant_program | core_marker_genes | top_labels |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 22 | 20 | 12 | Inflammatory monocyte-like | S100A8; S100A9; CD14 | MONOCYTE (7); CD14+ MONOCYTE (2); MYELOID CELL (2); MACROPHAGE (2); MONOCYTES (2); CDC2.1 (1) |
| C2 | 11 | 11 | 6 | Complement macrophage-like | C1QB; CD163 | MACROPHAGE (6); STRAD13⁺ MACROPHAGE (1); CDC2.4 (1); DONOR MACROPHAGE (1); BORDER-ASSOCIATED MACROPHAGE (1); C1QC+ MACROPHAGE (1) |
| C3 | 11 | 11 | 5 | Inflammatory monocyte-like | CD14; CD68 | MACROPHAGE (6); MONOCYTE (2); MONOCYTE CELL LINEAGE (1); MACROPHAGES (1); MACROPHAGES AND DENDRITIC CELLS (1) |
| C4 | 10 | 10 | 1 | Mast/granulocyte-like | TPSB2; TPSAB1; CPA3 | MAST CELL (10) |
| C5 | 7 | 7 | 1 | cDC1-like | CLEC9A; XCR1; CADM1 | CDC1 (7) |

## ILP-Selected Separating Genes

| example | gene_name | role_label | on_groups | mean_on_group_coverage |
| --- | --- | --- | --- | --- |
| T cell | IL7R | Essential | C1; C5 | 0.252 |
| T cell | CD3E | Essential | C4; C5 | 0.789 |
| T cell | FGFBP2 | Exchangeable | C3 | 0.211 |
| T cell | ITGA1 | Exchangeable | C6 | 0.500 |
| T cell | CCL4 | Exchangeable | C7 | 1.000 |
| Myeloid | CD14 | Essential | C1; C3 | 0.659 |
| Myeloid | CD163 | Essential | C2; C3 | 0.455 |
| Myeloid | TPSB2 | Exchangeable | C4 | 0.900 |

