# Figure 3 Local-Global Marker Identifiability

This prototype is the manuscript-facing version of the Lean-derived marker identifiability analysis.
The formal claim is that local separation within papers does not imply global atlas-scale separation.

Manuscript wrapper: `docs/paper/src/figures/fig3_cross_study_unification.tex`
Manuscript body: `docs/paper/src/figures/fig3_cross_study_unification_body.tex`

Panel PDFs: `analysis/figures/fig3_panel_a_joint_distribution.pdf` through `analysis/figures/fig3_panel_f_cap_local_global_recovery.pdf`.

Legacy composite: `analysis/figures/fig3_local_global_marker_identifiability.pdf` when `LLMARKERS_WRITE_LEGACY_FIGURES=1`.

## Summary

| claim | value |
| --- | --- |
| Same reported label with non-identical marker sets | 5,575/5,620 pairs (99.2%) |
| Different reported labels sharing marker genes | 102,445 cross-study pairs |
| Papers usually contain locally distinguishable reported-marker profiles | 88.8% |
| Median local problem size | 5 profiles, 4 genes |
| Median same-label marker liftover across papers | 0.333 |
| Same-label marker transfer above background | 8.03x lift |
| Exact labels at 20% marker coverage | 73 labels collapse to 67 signatures |
| Exact-label selected separating panel | 44 genes (8 essential, 36 exchangeable) |
| Most recurrent exact labels have median cross-paper marker Jaccard | 0.000 |

## Annotated Recurrent Labels

| normalized_cell_type | n_profiles | n_papers | mean_jaccard | median_jaccard | fraction_pairs_with_shared_marker_gene |
| --- | --- | --- | --- | --- | --- |
| T CELL | 38 | 37 | 0.119 | 0.000 | 0.460 |
| FIBROBLAST | 29 | 29 | 0.084 | 0.000 | 0.433 |
| MACROPHAGE | 29 | 29 | 0.060 | 0.000 | 0.298 |
| MONOCYTE | 24 | 24 | 0.061 | 0.000 | 0.257 |
| CD 4 T CELL | 17 | 17 | 0.042 | 0.000 | 0.346 |
| CD 8 T CELL | 15 | 15 | 0.047 | 0.000 | 0.362 |
| MYELOID CELL | 10 | 10 | 0.087 | 0.000 | 0.489 |
| TREG | 15 | 15 | 0.200 | 0.182 | 0.800 |
| MELANOCYTE | 7 | 7 | 0.389 | 0.400 | 1.000 |
| OLIGODENDROCYTES | 4 | 4 | 0.573 | 0.586 | 1.000 |

## Annotated Marker Transfer Labels

| normalized_cell_type | n_profiles | n_papers | median_observed_union_recall | median_expected_union_recall | median_union_recall_lift |
| --- | --- | --- | --- | --- | --- |
| T CELL | 38 | 37 | 0.929 | 0.261 | 3.535 |
| B CELL | 30 | 30 | 0.708 | 0.137 | 5.440 |
| MACROPHAGE | 29 | 29 | 0.667 | 0.216 | 2.819 |
| MONOCYTE | 24 | 24 | 0.333 | 0.176 | 2.449 |
| CD 4 T CELL | 17 | 17 | 0.545 | 0.121 | 4.431 |
| PLASMA CELL | 16 | 16 | 1.000 | 0.047 | 12.981 |
| MAST CELL | 15 | 15 | 1.000 | 0.040 | 21.612 |
| TREG | 15 | 15 | 0.750 | 0.112 | 6.690 |
| CD 8 T CELL | 15 | 15 | 0.500 | 0.117 | 4.331 |
| CLUSTER 1 | 14 | 14 | 0.000 | 0.052 | 0.000 |
| DENDRITIC CELL | 7 | 7 | 0.000 | 0.011 | 0.000 |

## Selected Separating Genes

| partition | gene_name | role | on_groups | mean_on_group_coverage |
| --- | --- | --- | --- | --- |
| reported_exact_labels_min5 | CD4 | essential_in_minimum_panels | CD 4 T CELL; IMMUNE CELL | 0.349 |
| reported_exact_labels_min5 | DCN | essential_in_minimum_panels | FIBROBLAST; FIBROBLASTS | 0.474 |
| reported_exact_labels_min5 | CD74 | exchangeable_in_minimum_panels | CLUSTER 7; LYMPHOCYTE; MAC 2; MICROGLIA | 0.219 |
| reported_exact_labels_min5 | CD79A | exchangeable_in_minimum_panels | B CELL; B CELLS; PLASMA CELL | 0.461 |
| reported_exact_labels_min5 | ACTA2 | essential_in_minimum_panels | CLUSTER 7; FB 2; MYOFIBROBLAST; MYOFIBROBLASTS; PERICYTE; PERICYTES; SMC; SMOOTH MUSCLE CELL | 0.475 |
| reported_exact_labels_min5 | COL1A1 | essential_in_minimum_panels | FB 1; FB 2; FIBROBLAST; MESENCHYMAL; MYOFIBROBLASTS | 0.332 |
| reported_exact_labels_min5 | VEGFA | exchangeable_in_minimum_panels | DC; PODOCYTE | 0.314 |
| reported_exact_labels_min5 | GCG | essential_in_minimum_panels | ALPHA CELL; CELL; ENTEROENDOCRINE CELL | 0.461 |
| reported_exact_labels_min5 | SOX9 | exchangeable_in_minimum_panels | DUCTAL CELL; EPITHELIAL CELL; OPC; STEM CELL | 0.279 |
| reported_exact_labels_min5 | MYH11 | exchangeable_in_minimum_panels | MYOFIBROBLASTS; SMC; SMOOTH MUSCLE CELL | 0.511 |
| reported_exact_labels_min5 | IL2RA | exchangeable_in_minimum_panels | MEMORY B CELL; TREG | 0.333 |
| reported_exact_labels_min5 | PDGFRA | essential_in_minimum_panels | FIBROBLAST; MESENCHYMAL; OPC; PC | 0.466 |
| reported_exact_labels_min5 | GLUL | essential_in_minimum_panels | ASTROCYTES; HEPATOCYTE | 0.267 |
| reported_exact_labels_min5 | RGS5 | exchangeable_in_minimum_panels | PC; PERICYTE; PERICYTES; SMC | 0.343 |
| reported_exact_labels_min5 | SPARCL1 | exchangeable_in_minimum_panels | ASTROCYTE | 0.250 |
| reported_exact_labels_min5 | CD8A | exchangeable_in_minimum_panels | CD 8 T CELL; T CELL | 0.285 |
| reported_exact_labels_min5 | KIT | exchangeable_in_minimum_panels | LYMPHOCYTE; MAST CELL; MELANOCYTE; TUFT CELL | 0.238 |
| reported_exact_labels_min5 | CD1C | exchangeable_in_minimum_panels | CDC 2; MYELOID CELL | 0.544 |
| reported_exact_labels_min5 | PDPN | exchangeable_in_minimum_panels | BASAL CELL; PERICYTES | 0.243 |
| reported_exact_labels_min5 | NEUROD1 | essential_in_minimum_panels | ENTEROENDOCRINE CELL; EXCITATORY NEURON | 0.386 |
| reported_exact_labels_min5 | EOMES | exchangeable_in_minimum_panels | CD 8 T CELL; NK CELL | 0.225 |
| reported_exact_labels_min5 | FABP1 | exchangeable_in_minimum_panels | ENTEROCYTE; HEPATOCYTE | 0.267 |
| reported_exact_labels_min5 | IL7R | exchangeable_in_minimum_panels | CD 4 T CELL; T CELLS | 0.247 |
| reported_exact_labels_min5 | FASN | exchangeable_in_minimum_panels | ADIPOCYTE; MEMORY B CELL | 0.200 |
| reported_exact_labels_min5 | CD14 | exchangeable_in_minimum_panels | MACROPHAGE; MACROPHAGES; MONOCYTE; TUFT CELL | 0.338 |
| reported_exact_labels_min5 | MZB1 | exchangeable_in_minimum_panels | PC; PLASMA CELL | 0.287 |
| reported_exact_labels_min5 | CD34 | exchangeable_in_minimum_panels | ENDOTHELIAL; HSC; LYMPHOCYTE | 0.267 |
| reported_exact_labels_min5 | PCSK1 | exchangeable_in_minimum_panels | BETA CELL; DELTA CELL | 0.300 |
| reported_exact_labels_min5 | CD163 | exchangeable_in_minimum_panels | MAC 2; MACROPHAGE | 0.290 |
| reported_exact_labels_min5 | ASCL2 | exchangeable_in_minimum_panels | STEM CELL | 0.571 |
| reported_exact_labels_min5 | IRF7 | exchangeable_in_minimum_panels | CLUSTER 0; DUCTAL CELL | 0.200 |
| reported_exact_labels_min5 | PMEL | exchangeable_in_minimum_panels | MELANOCYTE | 0.571 |
| reported_exact_labels_min5 | KRT14 | exchangeable_in_minimum_panels | BASAL; BASAL CELL | 0.429 |
| reported_exact_labels_min5 | SEMA4A | exchangeable_in_minimum_panels | B CELLS | 0.200 |
| reported_exact_labels_min5 | TCF4 | exchangeable_in_minimum_panels | CLUSTER 5 | 0.222 |
| reported_exact_labels_min5 | SERPINA1 | exchangeable_in_minimum_panels | AT 2; DELTA CELL | 0.200 |
| reported_exact_labels_min5 | MYH6 | exchangeable_in_minimum_panels | CARDIOMYOCYTE | 0.222 |
| reported_exact_labels_min5 | MBP | exchangeable_in_minimum_panels | OLIGODENDROCYTE | 0.429 |
| reported_exact_labels_min5 | CLEC9A | exchangeable_in_minimum_panels | CDC 1; DC | 0.509 |
| reported_exact_labels_min5 | MUC2 | exchangeable_in_minimum_panels | GOBLET CELL | 0.875 |
| reported_exact_labels_min5 | FCGR3A | exchangeable_in_minimum_panels | MACROPHAGES; MYELOID CELL; NK CELLS | 0.244 |
| reported_exact_labels_min5 | MAFB | exchangeable_in_minimum_panels | CELL; PODOCYTE | 0.372 |
| reported_exact_labels_min5 | PRSS1 | exchangeable_in_minimum_panels | ACINAR CELL | 0.286 |
| reported_exact_labels_min5 | PECAM1 | exchangeable_in_minimum_panels | EC; ENDOTHELIAL | 0.514 |
| tcell_marker_clusters | FGFBP2 | exchangeable_in_minimum_panels | C3 | 0.211 |
| tcell_marker_clusters | IL7R | essential_in_minimum_panels | C1; C5 | 0.252 |
| tcell_marker_clusters | CD3E | essential_in_minimum_panels | C4; C5 | 0.789 |
| tcell_marker_clusters | ITGA1 | exchangeable_in_minimum_panels | C6 | 0.500 |
| tcell_marker_clusters | CCL4 | exchangeable_in_minimum_panels | C7 | 1.000 |
| myeloid_marker_clusters | CD14 | essential_in_minimum_panels | C1; C3 | 0.659 |
| myeloid_marker_clusters | CD163 | essential_in_minimum_panels | C2; C3 | 0.455 |
| myeloid_marker_clusters | TPSB2 | exchangeable_in_minimum_panels | C4 | 0.900 |

