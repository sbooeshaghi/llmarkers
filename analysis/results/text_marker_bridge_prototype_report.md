# Text-marker bridge prototype

## Dataset

- Human profiles with at least two mapped Ensembl genes: 1,831
- Papers represented: 306
- Ensembl gene vocabulary: 2,696
- Evaluation split: grouped by paper ID, so held-out profiles come from held-out papers.

## Decision

**NO-GO.** The prototype is useful as an internal sanity check, but it should not be promoted as a final main result yet. Text-to-gene prediction is above baseline, especially with lexical TF-IDF, but the learned gene-to-text bridge does not beat the simpler raw marker-overlap neighbor.

## Cross-paper text-to-gene evaluation

| method | n_eval | mean recall at true gene count | median recall at true gene count | mean recall at 10 | mean precision at 10 | any hit at true gene count |
| --- | --- | --- | --- | --- | --- | --- |
| MiniLM text embedding + ridge | 360.0000 | 0.1351 | 0.0000 | 0.2440 | 0.0852 | 0.3730 |
| TF-IDF text + ridge | 360.0000 | 0.2437 | 0.1889 | 0.4083 | 0.1446 | 0.5518 |
| training gene popularity | 360.0000 | 0.0164 | 0.0000 | 0.0513 | 0.0178 | 0.0776 |

## Cross-paper gene-to-text evaluation

| method | n_eval | top1 exact label | top1 exact or partial label | top5 exact label | top5 exact or partial label | mean top1 marker Jaccard |
| --- | --- | --- | --- | --- | --- | --- |
| gene SVD + ridge to MiniLM text | 360.0000 | 0.0220 | 0.1597 | 0.0691 | 0.2936 | 0.1370 |
| random train profile | 360.0000 | 0.0028 | 0.0190 | 0.0066 | 0.0777 | 0.0026 |
| raw marker Jaccard neighbor | 360.0000 | 0.0490 | 0.1852 | 0.1141 | 0.3523 | 0.3965 |

## Text query examples

These examples use the strongest text-to-gene prototype, a TF-IDF text model with ridge regression to a binary Ensembl gene vector. They are qualitative face-validity checks, not held-out metrics.

| query | rank | gene_symbol | gene_id | score |
| --- | --- | --- | --- | --- |
| regulatory_t_cell | 1 | FOXP3 | ENSG00000049768 | 0.5799 |
| regulatory_t_cell | 2 | CTLA4 | ENSG00000163599 | 0.5613 |
| regulatory_t_cell | 3 | CD4 | ENSG00000010610 | 0.2934 |
| regulatory_t_cell | 4 | IL7R | ENSG00000168685 | 0.2371 |
| regulatory_t_cell | 5 | TIGIT | ENSG00000181847 | 0.2101 |
| regulatory_t_cell | 6 | CCR7 | ENSG00000126353 | 0.1904 |
| regulatory_t_cell | 7 | CD28 | ENSG00000178562 | 0.1724 |
| regulatory_t_cell | 8 | IL2RA | ENSG00000134460 | 0.1578 |
| regulatory_t_cell | 9 | LEF1 | ENSG00000138795 | 0.1543 |
| regulatory_t_cell | 10 | CD8A | ENSG00000153563 | 0.1516 |
| exhausted_cd8_t_cell | 1 | PDCD1 | ENSG00000188389 | 0.5045 |
| exhausted_cd8_t_cell | 2 | HAVCR2 | ENSG00000135077 | 0.3651 |
| exhausted_cd8_t_cell | 3 | CD8A | ENSG00000153563 | 0.3326 |
| exhausted_cd8_t_cell | 4 | TOX | ENSG00000198846 | 0.2803 |
| exhausted_cd8_t_cell | 5 | LAG3 | ENSG00000089692 | 0.2203 |
| exhausted_cd8_t_cell | 6 | CXCL13 | ENSG00000156234 | 0.1950 |
| exhausted_cd8_t_cell | 7 | CTLA4 | ENSG00000163599 | 0.1942 |
| exhausted_cd8_t_cell | 8 | PRF1 | ENSG00000180644 | 0.1782 |
| exhausted_cd8_t_cell | 9 | TIGIT | ENSG00000181847 | 0.1699 |
| exhausted_cd8_t_cell | 10 | CXCR3 | ENSG00000186810 | 0.1535 |
| classical_monocyte | 1 | S100A8 | ENSG00000143546 | 0.7207 |
| classical_monocyte | 2 | S100A9 | ENSG00000163220 | 0.7183 |
| classical_monocyte | 3 | CD14 | ENSG00000170458 | 0.6070 |
| classical_monocyte | 4 | LYZ | ENSG00000090382 | 0.2910 |
| classical_monocyte | 5 | VCAN | ENSG00000038427 | 0.1969 |
| classical_monocyte | 6 | S100A12 | ENSG00000163221 | 0.1585 |
| classical_monocyte | 7 | CD16 | ENSG00000203747 | 0.1342 |
| classical_monocyte | 8 | CCL2 | ENSG00000108691 | 0.0869 |
| classical_monocyte | 9 | MMP9 | ENSG00000100985 | 0.0842 |
| classical_monocyte | 10 | FCN1 | ENSG00000085265 | 0.0805 |
| macrophage | 1 | C1QA | ENSG00000173372 | 0.2593 |
| macrophage | 2 | C1QB | ENSG00000173369 | 0.2526 |
| macrophage | 3 | APOE | ENSG00000130203 | 0.2380 |
| macrophage | 4 | LYZ | ENSG00000090382 | 0.2038 |
| macrophage | 5 | CD68 | ENSG00000129226 | 0.1735 |
| macrophage | 6 | C1QC | ENSG00000159189 | 0.1522 |
| macrophage | 7 | SPP1 | ENSG00000154832 | 0.0989 |
| macrophage | 8 | CD74 | ENSG00000019582 | 0.0968 |
| macrophage | 9 | MRC1 | ENSG00000260314 | 0.0933 |
| macrophage | 10 | AIF1 | ENSG00000204472 | 0.0919 |
| b_cell | 1 | MS4A1 | ENSG00000156738 | 0.5216 |
| b_cell | 2 | CD79A | ENSG00000105369 | 0.4278 |
| b_cell | 3 | CD19 | ENSG00000177455 | 0.3190 |
| b_cell | 4 | CD79B | ENSG00000007312 | 0.2453 |
| b_cell | 5 | CD38 | ENSG00000004468 | 0.0959 |
| b_cell | 6 | PTPRC | ENSG00000081237 | 0.0687 |
| b_cell | 7 | JCHAIN | ENSG00000132465 | 0.0628 |
| b_cell | 8 | PAX5 | ENSG00000196092 | 0.0614 |
| b_cell | 9 | IGLL1 | ENSG00000128322 | 0.0491 |
| b_cell | 10 | BANK1 | ENSG00000153064 | 0.0479 |

## Gene-set query examples

For each input marker set, the learned bridge is compared to direct raw marker-overlap retrieval. If the learned bridge is not better than raw marker overlap, the model is not yet adding a new final result.

| query | input_symbols | resolved_gene_ids | method | rank | score | profile_id | label | paper_title | year | doi | profile_genes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | gene SVD + ridge to MiniLM text | 1 | 0.8336 | 2270 | TREG | Unveiling the influence of tumor and immune signatures on immune checkpoint therapy in advanced lung cancer | 2024 | 10.1101/2024.04.15.589544 | FOXP3, CTLA4, ICOS, BATF |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | gene SVD + ridge to MiniLM text | 2 | 0.8198 | 3469 | CD4.4 | Acquisition of discrete immune suppressive barriers contributes to the initiation and progression of preinvasive to invasive human lung cancer | 2025 | 10.1101/2024.12.31.630523 | FOXP3, IKZF2, IL2RA, CTLA4 |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | gene SVD + ridge to MiniLM text | 3 | 0.8026 | 208 | CD4+ REGULATORY T CELL (TREG) | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | FOXP3, CTLA4 |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | gene SVD + ridge to MiniLM text | 4 | 0.7837 | 2639 | TREG | Massively parallel single-cell chromatin landscapes of human immune cell development and intratumoral T cell exhaustion | 2019 | 10.1101/610550 | FOXP3, CTLA4 |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | gene SVD + ridge to MiniLM text | 5 | 0.7825 | 3499 | TREG.1 | Acquisition of discrete immune suppressive barriers contributes to the initiation and progression of preinvasive to invasive human lung cancer | 2025 | 10.1101/2024.12.31.630523 | LEF1, SELL, CCR7, TCF7 |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | raw marker Jaccard neighbor | 1 | 0.7500 | 3469 | CD4.4 | Acquisition of discrete immune suppressive barriers contributes to the initiation and progression of preinvasive to invasive human lung cancer | 2025 | 10.1101/2024.12.31.630523 | FOXP3, IKZF2, IL2RA, CTLA4 |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | raw marker Jaccard neighbor | 2 | 0.6667 | 3816 | CD4T_FOXP3 | Single-cell transcriptomics reveals immunosuppressive microenvironment and highlights stumor-promoting macrophage cells in Glioblastoma | 2024 | 10.1101/2024.05.15.594316 | FOXP3, CTLA4, TIGHT |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | raw marker Jaccard neighbor | 3 | 0.6667 | 2639 | TREG | Massively parallel single-cell chromatin landscapes of human immune cell development and intratumoral T cell exhaustion | 2019 | 10.1101/610550 | FOXP3, CTLA4 |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | raw marker Jaccard neighbor | 4 | 0.6667 | 2410 | CD4 GLYCOLIPID-SPECIFIC T CELL | CD4 and CD8 co-receptors modulate functional avidity of CD1b-restricted T cells | 2020 | 10.1101/2020.10.17.332072 | CTLA4, FOXP3 |
| treg_core | FOXP3, IL2RA, CTLA4 | ENSG00000049768, ENSG00000134460, ENSG00000163599 | raw marker Jaccard neighbor | 5 | 0.6667 | 208 | CD4+ REGULATORY T CELL (TREG) | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | FOXP3, CTLA4 |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | gene SVD + ridge to MiniLM text | 1 | 0.8234 | 213 | CD8+ EXHAUSTED T CELL (TEXH) | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | PDCD1, LAG3, HAVCR2 |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | gene SVD + ridge to MiniLM text | 2 | 0.8183 | 214 | CD8+ PROLIFERATING EXHAUSTED T CELL | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | HAVCR2, MKI67, TOP2A |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | gene SVD + ridge to MiniLM text | 3 | 0.8117 | 3463 | EXHAUSTION-LIKE CD8+ CAR-T CELL | Identifying Distinct Molecular Response of CAR-T cells to Solid Tumors by Synthetic Single-Cell Transcriptomic Analyses | 2025 | 10.1101/2025.09.17.676755 | TNFRSF9, CCL3, TIM3, HAVCR2, TIGIT, CTLA4 |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | gene SVD + ridge to MiniLM text | 4 | 0.7915 | 3478 | CD8.8 | Acquisition of discrete immune suppressive barriers contributes to the initiation and progression of preinvasive to invasive human lung cancer | 2025 | 10.1101/2024.12.31.630523 | CXCL13, CTLA4, ENTPD1, HAVCR2, LAG3, TOX, PDCD1, ITGAE, ITGA1, CD69, CXCR6 |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | gene SVD + ridge to MiniLM text | 5 | 0.7899 | 2268 | TEX | Unveiling the influence of tumor and immune signatures on immune checkpoint therapy in advanced lung cancer | 2024 | 10.1101/2024.04.15.589544 | HAVCR2, PDCD1, PRF1, IFNG, CXCR3, CXCL13 |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | raw marker Jaccard neighbor | 1 | 1.0000 | 213 | CD8+ EXHAUSTED T CELL (TEXH) | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | PDCD1, LAG3, HAVCR2 |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | raw marker Jaccard neighbor | 2 | 0.6667 | 3698 | CYTOTOXIC T CELL | Spatialproteomics - an interoperable toolbox for analyzing highly multiplexed fluorescence image data | 2025 | 10.1101/2025.04.29.651202 | PD1, TIM3 |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | raw marker Jaccard neighbor | 3 | 0.6667 | 3821 | CD8T_LAG3 | Single-cell transcriptomics reveals immunosuppressive microenvironment and highlights stumor-promoting macrophage cells in Glioblastoma | 2024 | 10.1101/2024.05.15.594316 | LAG3, PDCD1 |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | raw marker Jaccard neighbor | 4 | 0.5000 | 635 | TERMINALLY-DIFFERENTIATED | The CD8+ T cell landscape of human brain metastases | 2021 | 10.1101/2021.08.03.455000 | PD-1, CTLA-4, CD39, TIM-3, TOX, CTLA4, ENTPD1, HAVCR2, LAG3 |
| exhaustion_checkpoint | PDCD1, HAVCR2, LAG3 | ENSG00000188389, ENSG00000135077, ENSG00000089692 | raw marker Jaccard neighbor | 5 | 0.4000 | 636 | TERMINALLY-DIFFERENTIATED PHENOTYPE OF CD8+ T CELL | The CD8+ T cell landscape of human brain metastases | 2021 | 10.1101/2021.08.03.455000 | HAVCR2, LAG3, CXCL13, GZMB |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | gene SVD + ridge to MiniLM text | 1 | 0.8055 | 227 | MONOCYTE | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | VCAN, APOBEC3A |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | gene SVD + ridge to MiniLM text | 2 | 0.7864 | 231 | NEUTROPHIL | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | FCGR3B, S100A8 |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | gene SVD + ridge to MiniLM text | 3 | 0.7817 | 236 | PLASMACYTOID DC (PDCS) | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | PTCRA, CLEC4C |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | gene SVD + ridge to MiniLM text | 4 | 0.7726 | 2824 | MONOCYTE | Single-cell integration and multi-modal profiling reveals phenotypes and spatial organization of neutrophils in colorectal cancer | 2024 | 10.1101/2024.08.26.609563 | VCAN, CD14 |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | gene SVD + ridge to MiniLM text | 5 | 0.7705 | 216 | CONVENTIONAL DENDRITIC CELL (CDCS) | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | CD86, CD1C, CLEC10 |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | raw marker Jaccard neighbor | 1 | 0.8000 | 3618 | MONOCYTE | Decontamination of ambient RNA in single-cell RNA-seq with DecontX | 2019 | 10.1101/704015 | LYZ, S100A8, S100A9, CD14 |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | raw marker Jaccard neighbor | 2 | 0.6000 | 2962 | MONOCYTE | Comparative Analysis of Feature Selection Methods for Single-Cell RNA Sequencing Data | 2025 | 10.64898/2025.12.02.691907 | CD14, LYZ, S100A9 |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | raw marker Jaccard neighbor | 3 | 0.6000 | 3111 | MONOCYTE | HCNetlas: Human cell network atlas enabling cell type-resolved disease genetics | 2024 | 10.1101/2024.06.07.597878 | S100A8, S100A9, CD14 |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | raw marker Jaccard neighbor | 4 | 0.6000 | 3863 | MONOCYTES | Human and mouse transcriptome profiling identifies cross-species homology in pulmonary and lymph node mononuclear phagocytes | 2020 | 10.1101/2020.04.30.070839 | S100A8, S100A9, CD14 |
| classical_monocyte | CD14, LST1, S100A8, S100A9, FCN1, LYZ | ENSG00000170458, ENSG00000143546, ENSG00000163220, ENSG00000085265, ENSG00000090382 | raw marker Jaccard neighbor | 5 | 0.6000 | 3291 | MONOCYTE | Spatial and Single-Cell Transcriptomics Decipher the Crosstalk Environment of DEFB1+ Cancer Cells and IFI30+ Macrophages in Intrahepatic Cholangiocarcinoma | 2025 | 10.1101/2025.11.22.689892 | FCN1, S100A8, S100A9 |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | gene SVD + ridge to MiniLM text | 1 | 0.8103 | 227 | MONOCYTE | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | VCAN, APOBEC3A |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | gene SVD + ridge to MiniLM text | 2 | 0.7944 | 236 | PLASMACYTOID DC (PDCS) | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | PTCRA, CLEC4C |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | gene SVD + ridge to MiniLM text | 3 | 0.7926 | 243 | TREM2HIGH MACROPHAGE | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | TREM2, APOE, C1QA, SPP1 |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | gene SVD + ridge to MiniLM text | 4 | 0.7908 | 231 | NEUTROPHIL | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | FCGR3B, S100A8 |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | gene SVD + ridge to MiniLM text | 5 | 0.7879 | 239 | STRAD13⁺ MACROPHAGE | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | STARD13, CD163, MRC1 |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | raw marker Jaccard neighbor | 1 | 0.4000 | 3370 | DOMAIN 4 | Characterizing intra- and inter-tumor heterogeneity in Ovarian high-grade serous carcinoma subtypes using single-cell and spatial transcriptomics | 2025 | 10.1101/2025.09.15.676244 | LYZ, CD68 |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | raw marker Jaccard neighbor | 2 | 0.4000 | 2821 | MACROPHAGE | Single-cell integration and multi-modal profiling reveals phenotypes and spatial organization of neutrophils in colorectal cancer | 2024 | 10.1101/2024.08.26.609563 | C1QA, C1QB |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | raw marker Jaccard neighbor | 3 | 0.4000 | 228 | MYELOID CELL | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | LYZ, CD68 |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | raw marker Jaccard neighbor | 4 | 0.4000 | 3289 | MACROPHAGE | Spatial and Single-Cell Transcriptomics Decipher the Crosstalk Environment of DEFB1+ Cancer Cells and IFI30+ Macrophages in Intrahepatic Cholangiocarcinoma | 2025 | 10.1101/2025.11.22.689892 | C1QA, C1QB |
| macrophage | CD68, APOE, C1QA, C1QB, LYZ | ENSG00000129226, ENSG00000130203, ENSG00000173372, ENSG00000173369, ENSG00000090382 | raw marker Jaccard neighbor | 5 | 0.3333 | 244 | TREM2LOW | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | APOE, C1QA, C1QC |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | gene SVD + ridge to MiniLM text | 1 | 0.8003 | 2956 | B CELL | Comparative Analysis of Feature Selection Methods for Single-Cell RNA Sequencing Data | 2025 | 10.64898/2025.12.02.691907 | MS4A1, CD79A |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | gene SVD + ridge to MiniLM text | 2 | 0.7786 | 235 | PLASMA CELL | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | IGHG4, JCHAIN, MZB1 |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | gene SVD + ridge to MiniLM text | 3 | 0.7711 | 202 | B CELL | Deciphering Tumor Microenvironment Dynamics in Tumorigenesis and Lymph Node Metastasis of Esophageal Squamous Cell Carcinoma using Single-cell RNA Sequencing | 2025 | 10.1101/2025.11.27.690370 | MS4A1, CD79A |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | gene SVD + ridge to MiniLM text | 4 | 0.7649 | 1011 | B CELL | A literature-derived knowledge graph augments the interpretation of single cell RNA-seq datasets | 2021 | 10.1101/2021.04.01.438124 | CD19, CD20 |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | gene SVD + ridge to MiniLM text | 5 | 0.7638 | 3267 | B CELL | Spatial and Single-Cell Transcriptomics Decipher the Crosstalk Environment of DEFB1+ Cancer Cells and IFI30+ Macrophages in Intrahepatic Cholangiocarcinoma | 2025 | 10.1101/2025.11.22.689892 | MS4A1, CD79A |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | raw marker Jaccard neighbor | 1 | 1.0000 | 3612 | B-CELL | Decontamination of ambient RNA in single-cell RNA-seq with DecontX | 2019 | 10.1101/704015 | CD79A, CD79B, MS4A1 |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | raw marker Jaccard neighbor | 2 | 0.7500 | 877 | B CELL | Celda: A Bayesian model to perform bi-clustering of genes into modules and cells into subpopulations using single-cell RNA-seq data | 2020 | 10.1101/2020.11.16.373274 | CD79A, CD79B, MS4A1, CD19 |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | raw marker Jaccard neighbor | 3 | 0.6667 | 645 | B CELL | Accurate highly variable gene selection using RECODE in scRNA-seq data analysis | 2025 | 10.1101/2025.06.23.661026 | MS4A1, CD79A |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | raw marker Jaccard neighbor | 4 | 0.6667 | 2527 | B CELL | A multi-gene predictive model for the radiation sensitivity of nasopharyngeal carcinoma based on machine learning | 2024 | 10.1101/2024.06.10.598247 | MS4A1, CD79A |
| b_cell | MS4A1, CD79A, CD79B | ENSG00000156738, ENSG00000105369, ENSG00000007312 | raw marker Jaccard neighbor | 5 | 0.6667 | 2956 | B CELL | Comparative Analysis of Feature Selection Methods for Single-Cell RNA Sequencing Data | 2025 | 10.64898/2025.12.02.691907 | MS4A1, CD79A |
