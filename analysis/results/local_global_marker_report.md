# Local vs Global Marker Analysis

This analysis quantifies the distinction between local marker claims within a paper and global marker reuse across papers.
A same-paper pair approximates the local comparison set used to report markers. A different-paper pair approximates the atlas-scale comparison problem.

Important caveat: marker absence means not reported as a marker in this corpus, not absent expression.

## Headline

- Within-paper different-label pairs have median marker Jaccard 0.000.
- Between-paper same-exact-label pairs have median marker Jaccard 0.000.
- The median paper has 5 reported profiles and a greedy local separating panel of 4 genes.
- Across profiles with same-label matches in other papers, the median fraction of markers recovered by same-label profiles elsewhere is 0.333.

## Pairwise Marker Overlap

| pair_category | n_pairs | median_jaccard | mean_jaccard | pct_jaccard_eq_0 | pct_jaccard_ge_0_25 |
| --- | --- | --- | --- | --- | --- |
| within_paper_different_label | 15426 | 0.000 | 0.028 | 0.902 | 0.036 |
| within_paper_same_exact_label | 28 | 0.000 | 0.049 | 0.643 | 0.071 |
| between_paper_same_exact_label | 5620 | 0.000 | 0.098 | 0.564 | 0.116 |
| between_paper_same_broad_neighborhood | 77048 | 0.000 | 0.026 | 0.849 | 0.027 |
| between_paper_different_broad_neighborhood | 426381 | 0.000 | 0.002 | 0.985 | 0.001 |
| between_paper_other | 5088422 | 0.000 | 0.002 | 0.982 | 0.001 |

## Largest Local Marker Problems

| paper_key | n_profiles | n_distinct_marker_signatures | information_lower_bound_log2 | greedy_local_panel_size | median_jaccard |
| --- | --- | --- | --- | --- | --- |
| hca:0148_10.1113_jp287812_fd3137bc12 | 30 | 28 | 5 | 26 | 0.000 |
| hca:0364_10.1161_circulationaha.120.046528_00aa2deb4c | 29 | 27 | 5 | 22 | 0.000 |
| hca:0290_10.1101_235499_566cff6e3c | 29 | 28 | 5 | 20 | 0.000 |
| hca:0090_10.1038_s41586-021-03852-1_eec89a5e36 | 27 | 27 | 5 | 26 | 0.000 |
| hca:0089_10.1038_s41586-020-2797-4_6e65d21b5d | 26 | 26 | 5 | 25 | 0.000 |
| hca:0350_10.1038_s41421-020-0157-z_3083f6da26 | 26 | 26 | 5 | 21 | 0.000 |
| biorxiv:219b21d9-7007-1014-9157-ab439216a355 | 24 | 23 | 5 | 21 | 0.000 |
| hca:0465_10.1016_j.cell.2020.12.016_af8ed7d941 | 24 | 24 | 5 | 21 | 0.000 |
| hca:0109_10.7554_elife.91792.1_056dda27be | 24 | 24 | 5 | 20 | 0.000 |
| hca:0085_10.1073_pnas.2200914119_3dd916fb05 | 23 | 23 | 5 | 18 | 0.000 |
| hca:0384_10.1038_s41422-021-00529-2_d6c8237ebe | 22 | 22 | 5 | 16 | 0.000 |
| hca:0284_10.1002_hep4.1854_fe09f5fe1e | 21 | 20 | 5 | 18 | 0.000 |

## Most Underspecified Recurrent Labels

| normalized_cell_type | n_profiles | n_papers | median_jaccard | global_label_underspecification_score | example_reported_labels |
| --- | --- | --- | --- | --- | --- |
| T CELL | 38 | 37 | 0.000 | 1.000 | T CELL; T-CELL; ΑΒ T CELL; ΓΔ T CELL |
| FIBROBLAST | 29 | 29 | 0.000 | 1.000 | FIBROBLAST |
| MACROPHAGE | 29 | 29 | 0.000 | 1.000 | MACROPHAGE |
| ENDOTHELIAL CELL | 28 | 28 | 0.000 | 1.000 | ENDOTHELIAL CELL |
| MONOCYTE | 24 | 24 | 0.000 | 1.000 | MONOCYTE |
| CELL | 19 | 8 | 0.000 | 1.000 | Α CELL; Α-CELL; Β CELL; Β-CELL; Γ-CELL; Δ-CELL; Ε-CELL |
| CLUSTER 2 | 19 | 19 | 0.000 | 1.000 | CLUSTER 2; CLUSTER-2 |
| MICROGLIA | 18 | 18 | 0.000 | 1.000 | MICROGLIA |
| CD 4 T CELL | 17 | 17 | 0.000 | 1.000 | CD4 + T CELL; CD4 T CELL; CD4+ T CELL; CD4+T CELL |
| NK CELL | 16 | 16 | 0.000 | 1.000 | NK CELL |
| CD 8 T CELL | 15 | 15 | 0.000 | 1.000 | CD8 + T CELL; CD8 T CELL; CD8+ T CELL; CD8+ T-CELL |
| CLUSTER 1 | 14 | 14 | 0.000 | 1.000 | CLUSTER 1; CLUSTER-1 |
| CLUSTER 3 | 12 | 12 | 0.000 | 1.000 | CLUSTER 3; CLUSTER-3 |
| CLUSTER 4 | 11 | 11 | 0.000 | 1.000 | CLUSTER 4; CLUSTER-4 |
| AT 2 | 10 | 10 | 0.000 | 1.000 | AT2 |

## Interpretation

Local markers are selected in a paper-specific comparison set. They often separate the cell types reported in that paper, but the same label across papers does not necessarily recover the same marker set.
This is the empirical version of the formal distinction between a local binary marker matrix `X_i` and a global atlas-scale marker matrix `X`.
