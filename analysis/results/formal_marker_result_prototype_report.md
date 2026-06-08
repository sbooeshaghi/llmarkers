# Formal Marker Result Prototype

This prototype translates the Lean local/global marker formalization into an empirical analysis set.
The central claim is that single papers report local separating marker claims, while atlas building requires testing whether those claims lift to a global comparison set.

Figure prototype: `analysis/figures/fig_formal_marker_result_prototype.pdf`

## Candidate Result Summary

| result | value | detail |
| --- | --- | --- |
| Local paper-level marker profiles are usually distinguishable | 88.8% | Fraction of papers whose reported profiles have distinct full marker signatures |
| Typical local marker problem size | 5 profiles, greedy panel 4 genes | Median across papers with at least two marker profiles |
| Same exact labels across papers are marker-enriched but sparse | mean J=0.098 vs background J=0.002 | Pairwise marker Jaccard for different-paper profile pairs |
| Same exact labels often fail to recover local marker profiles | median liftover=0.333 | Fraction of a profile's reported markers recovered by same-label profiles in other papers |
| Within-paper different-label markers are highly local | 90.2% zero-overlap pairs | Same-paper, different-label profile pairs |
| Exact labels collapse at high coverage | 73 labels -> 67 signatures | Reported exact labels, 20% within-label marker coverage threshold |
| myeloid_marker_clusters: Essential genes | 2 | Role among ILP-selected minimum separating panel genes at 20% threshold |
| myeloid_marker_clusters: Exchangeable genes | 1 | Role among ILP-selected minimum separating panel genes at 20% threshold |
| reported_exact_labels_min5: Essential genes | 8 | Role among ILP-selected minimum separating panel genes at 20% threshold |
| reported_exact_labels_min5: Exchangeable genes | 36 | Role among ILP-selected minimum separating panel genes at 20% threshold |
| tcell_marker_clusters: Essential genes | 2 | Role among ILP-selected minimum separating panel genes at 20% threshold |
| tcell_marker_clusters: Exchangeable genes | 3 | Role among ILP-selected minimum separating panel genes at 20% threshold |

## How This Compares With Current Results

- The current cross-study joint distribution remains useful as the visual setup, but this result gives it a stronger mathematical interpretation.
- The local/global analysis can replace a weaker version of the label-versus-marker comparison because it directly states what is local, what lifts globally, and what fails.
- The essential/exchangeable marker result is stronger than a generic coverage/purity result because the gene classes are defined by a formal separation objective.
- The T-cell and myeloid examples should remain as biological vignettes, but they should support the formal result rather than carry the entire conclusion.
- The coverage/purity/F1 plots can move to the supplement or be reframed as exploratory diagnostics for marker stability.

## Label Underspecification Examples

| normalized_cell_type | n_profiles | n_papers | mean_jaccard | median_jaccard | pct_jaccard_eq_0 | pct_jaccard_ge_0_25 | example_reported_labels |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T CELL | 38 | 37 | 0.119 | 0.000 | 0.540 | 0.125 | T CELL; T-CELL; ΑΒ T CELL; ΓΔ T CELL |
| FIBROBLAST | 29 | 29 | 0.084 | 0.000 | 0.567 | 0.086 | FIBROBLAST |
| MACROPHAGE | 29 | 29 | 0.060 | 0.000 | 0.702 | 0.054 | MACROPHAGE |
| ENDOTHELIAL CELL | 28 | 28 | 0.086 | 0.000 | 0.503 | 0.087 | ENDOTHELIAL CELL |
| MONOCYTE | 24 | 24 | 0.061 | 0.000 | 0.743 | 0.083 | MONOCYTE |
| CELL | 19 | 8 | 0.044 | 0.000 | 0.593 | 0.027 | Α CELL; Α-CELL; Β CELL; Β-CELL; Γ-CELL; Δ-CELL; Ε-CELL |
| CLUSTER 2 | 19 | 19 | 0.004 | 0.000 | 0.959 | 0.000 | CLUSTER 2; CLUSTER-2 |
| MICROGLIA | 18 | 18 | 0.042 | 0.000 | 0.575 | 0.013 | MICROGLIA |
| CD 4 T CELL | 17 | 17 | 0.042 | 0.000 | 0.654 | 0.037 | CD4 + T CELL; CD4 T CELL; CD4+ T CELL; CD4+T CELL |
| NK CELL | 16 | 16 | 0.070 | 0.000 | 0.550 | 0.042 | NK CELL |
| CD 8 T CELL | 15 | 15 | 0.047 | 0.000 | 0.638 | 0.029 | CD8 + T CELL; CD8 T CELL; CD8+ T CELL; CD8+ T-CELL |
| CLUSTER 1 | 14 | 14 | 0.002 | 0.000 | 0.978 | 0.000 | CLUSTER 1; CLUSTER-1 |
| CLUSTER 3 | 12 | 12 | 0.004 | 0.000 | 0.939 | 0.000 | CLUSTER 3; CLUSTER-3 |
| CLUSTER 4 | 11 | 11 | 0.001 | 0.000 | 0.982 | 0.000 | CLUSTER 4; CLUSTER-4 |
| AT 2 | 10 | 10 | 0.059 | 0.000 | 0.689 | 0.067 | AT2 |
| MYELOID CELL | 10 | 10 | 0.087 | 0.000 | 0.511 | 0.044 | MYELOID CELL |
| CARDIOMYOCYTE | 9 | 9 | 0.031 | 0.000 | 0.639 | 0.000 | CARDIOMYOCYTE |
| CLUSTER 5 | 9 | 9 | 0.009 | 0.000 | 0.944 | 0.000 | CLUSTER 5 |
| ACINAR CELL | 7 | 7 | 0.096 | 0.000 | 0.714 | 0.143 | ACINAR CELL |
| BASAL | 7 | 7 | 0.138 | 0.000 | 0.619 | 0.143 | BASAL |

## Identifiability Summary

| partition | coverage_threshold | n_groups | n_distinct_signatures | all_groups_identifiable_with_all_genes | information_lower_bound_log2 | greedy_panel_size | ilp_panel_size | ilp_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| broad_neighborhoods | 0.05 | 8 | 8 | True | 3 | 6 | 6.0 | optimal |
| broad_neighborhoods | 0.1 | 8 | 8 | True | 3 | 7 | 7.0 | optimal |
| broad_neighborhoods | 0.2 | 8 | 5 | False | 3 | 4 | 4.0 | optimal |
| reported_exact_labels_min5 | 0.05 | 73 | 73 | True | 7 | 30 |  | Time limit reached. (HiGHS Status 13: Time limit reached) |
| reported_exact_labels_min5 | 0.1 | 73 | 73 | True | 7 | 35 |  | Time limit reached. (HiGHS Status 13: Time limit reached) |
| reported_exact_labels_min5 | 0.2 | 73 | 67 | False | 7 | 47 | 44.0 | optimal |
| tcell_marker_clusters | 0.05 | 7 | 7 | True | 3 | 4 | 4.0 | optimal |
| tcell_marker_clusters | 0.1 | 7 | 7 | True | 3 | 5 | 5.0 | optimal |
| tcell_marker_clusters | 0.2 | 7 | 7 | True | 3 | 5 | 5.0 | optimal |
| myeloid_marker_clusters | 0.05 | 5 | 5 | True | 3 | 3 | 3.0 | optimal |
| myeloid_marker_clusters | 0.1 | 5 | 5 | True | 3 | 3 | 3.0 | optimal |
| myeloid_marker_clusters | 0.2 | 5 | 5 | True | 3 | 3 | 3.0 | optimal |

## Essential And Exchangeable Genes In Immune Marker Clusters

| partition | gene_name | role | on_groups | mean_on_group_coverage |
| --- | --- | --- | --- | --- |
| tcell_marker_clusters | FGFBP2 | exchangeable_in_minimum_panels | C3 | 0.211 |
| tcell_marker_clusters | IL7R | essential_in_minimum_panels | C1; C5 | 0.252 |
| tcell_marker_clusters | CD3E | essential_in_minimum_panels | C4; C5 | 0.789 |
| tcell_marker_clusters | ITGA1 | exchangeable_in_minimum_panels | C6 | 0.500 |
| tcell_marker_clusters | CCL4 | exchangeable_in_minimum_panels | C7 | 1.000 |
| myeloid_marker_clusters | CD14 | essential_in_minimum_panels | C1; C3 | 0.659 |
| myeloid_marker_clusters | CD163 | essential_in_minimum_panels | C2; C3 | 0.455 |
| myeloid_marker_clusters | TPSB2 | exchangeable_in_minimum_panels | C4 | 0.900 |

## Recommended Manuscript Use

Use this as the closing result after large-scale extraction. The flow would be: extracted marker claims form a global binary matrix; papers define local comparison sets; local marker claims often do not lift cleanly to the global matrix; the formalization lets us identify underspecified labels and classify markers as essential or exchangeable for a chosen partition.
