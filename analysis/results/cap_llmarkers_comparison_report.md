# CAP vs LLMarkers Human Marker Comparison

This analysis compares two human marker resources using the same profile-level definitions.
LLMarkers profiles are grouped by extracted paper. CAP profiles are grouped by dataset and labelset, because one dataset can carry multiple annotation schemes.
Global comparisons are made across studies; CAP pairs from the same dataset are not counted as between-study pairs.

Important caveat: marker absence means not reported as a marker in the resource, not absent expression.

## Resource Summary

| resource | human_marker_records | studies | local_contexts | marker_profiles | reported_labels | marker_genes | median_markers_per_profile | mean_markers_per_profile | local_identifiable_profiles | local_identifiable_fraction | globally_unique_marker_set_profiles | globally_unique_marker_set_fraction | globally_label_consistent_marker_set_profiles | globally_label_consistent_marker_set_fraction | local_identifiable_but_globally_label_ambiguous_profiles | local_identifiable_but_globally_label_ambiguous_fraction | recurrent_exact_labels |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAP | 8899 | 68 | 82 | 1288 | 719 | 2155 | 5.000 | 6.188 | 1260 | 0.978 | 515 | 0.400 | 1249 | 0.970 | 11 | 0.009 | 355 |
| LLMarkers | 24141 | 599 | 599 | 3351 | 2318 | 3914 | 4.000 | 5.245 | 3202 | 0.956 | 3033 | 0.905 | 3086 | 0.921 | 116 | 0.035 | 325 |

## Pairwise Marker Overlap

| resource | pair_category | n_pairs | median_jaccard | pct_jaccard_eq_0 | pct_jaccard_gt_0 | pct_jaccard_eq_1 |
| --- | --- | --- | --- | --- | --- | --- |
| CAP | within_local_context_different_label | 24535 | 0.000 | 0.910 | 0.090 | 0.001 |
| CAP | within_local_context_same_exact_label | 14 | 0.125 | 0.000 | 1.000 | 0.000 |
| CAP | same_study_different_labelset | 1871 | 0.000 | 0.933 | 0.067 | 0.008 |
| CAP | between_study_same_exact_label | 1056 | 1.000 | 0.095 | 0.905 | 0.624 |
| CAP | between_study_partial_label | 17286 | 0.000 | 0.731 | 0.269 | 0.001 |
| CAP | between_study_different_label | 784066 | 0.000 | 0.981 | 0.019 | 0.000 |
| LLMarkers | within_local_context_different_label | 15426 | 0.000 | 0.902 | 0.098 | 0.007 |
| LLMarkers | within_local_context_same_exact_label | 28 | 0.000 | 0.643 | 0.357 | 0.000 |
| LLMarkers | same_study_different_labelset | 0 |  |  |  |  |
| LLMarkers | between_study_same_exact_label | 5620 | 0.000 | 0.564 | 0.436 | 0.008 |
| LLMarkers | between_study_partial_label | 63782 | 0.000 | 0.870 | 0.130 | 0.000 |
| LLMarkers | between_study_different_label | 5528069 | 0.000 | 0.981 | 0.019 | 0.000 |

## Label-Marker Joint Distribution

| resource | label_relation | marker_relation | n_pairs | fraction_of_between_study_pairs | mean_marker_jaccard | median_marker_jaccard |
| --- | --- | --- | --- | --- | --- | --- |
| CAP | Exact | Exact | 659 | 0.001 | 1.000 | 1.000 |
| CAP | Exact | Partial | 297 | 0.000 | 0.268 | 0.200 |
| CAP | Exact | Different | 100 | 0.000 | 0.000 | 0.000 |
| CAP | Partial | Exact | 12 | 0.000 | 1.000 | 1.000 |
| CAP | Partial | Partial | 4645 | 0.006 | 0.192 | 0.143 |
| CAP | Partial | Different | 12629 | 0.016 | 0.000 | 0.000 |
| CAP | Different | Exact | 3 | 0.000 | 1.000 | 1.000 |
| CAP | Different | Partial | 14796 | 0.018 | 0.120 | 0.091 |
| CAP | Different | Different | 769267 | 0.959 | 0.000 | 0.000 |
| LLMarkers | Exact | Exact | 45 | 0.000 | 1.000 | 1.000 |
| LLMarkers | Exact | Partial | 2408 | 0.000 | 0.209 | 0.167 |
| LLMarkers | Exact | Different | 3167 | 0.001 | 0.000 | 0.000 |
| LLMarkers | Partial | Exact | 30 | 0.000 | 1.000 | 1.000 |
| LLMarkers | Partial | Partial | 8248 | 0.001 | 0.173 | 0.143 |
| LLMarkers | Partial | Different | 55504 | 0.010 | 0.000 | 0.000 |
| LLMarkers | Different | Exact | 76 | 0.000 | 1.000 | 1.000 |
| LLMarkers | Different | Partial | 102437 | 0.018 | 0.126 | 0.111 |
| LLMarkers | Different | Different | 5425556 | 0.969 | 0.000 | 0.000 |

## Same-Label Liftover

| resource | profiles_with_same_label_other_studies | median_marker_fraction_recovered | median_local_private_fraction_recovered |
| --- | --- | --- | --- |
| CAP | 921 | 1.000 | 1.000 |
| LLMarkers | 1352 | 0.333 | 0.333 |

## Exact-Label Pairs Split By Project

CAP project IDs are used to separate repeated or related datasets from more independent cross-project comparisons.

| resource | project_relation | n_pairs | median_jaccard | pct_jaccard_eq_0 | pct_jaccard_gt_0 | pct_jaccard_eq_1 |
| --- | --- | --- | --- | --- | --- | --- |
| CAP | same_project | 749 | 1.000 | 0.004 | 0.996 | 0.877 |
| CAP | different_project_or_unknown | 307 | 0.125 | 0.316 | 0.684 | 0.007 |
| LLMarkers | same_project | 0 |  |  |  |  |
| LLMarkers | different_project_or_unknown | 5620 | 0.000 | 0.564 | 0.436 | 0.008 |

## Study DOI/Provenance Coverage

| resource | studies | studies_with_rationale_dois | total_unique_rationale_dois |
| --- | --- | --- | --- |
| CAP | 68 | 26 | 150 |
| LLMarkers | 599 | 0 | 0 |

## Recurrent Exact Labels With Many Profiles

| resource | normalized_cell_type | n_profiles | n_studies | median_jaccard | pct_jaccard_eq_0 | example_reported_labels |
| --- | --- | --- | --- | --- | --- | --- |
| CAP | PDC | 13 | 13 | 0.300 | 0.038 | PDC; pDC |
| CAP | B CELLS | 13 | 8 | 0.600 | 0.301 | B Cells; B cells |
| CAP | CD 14 CD 16 MONOCYTES | 10 | 5 | 0.562 | 0.000 | CD14⁺CD16⁺ Monocytes; CD14⁺CD16⁻ Monocytes |
| CAP | PERICYTES | 8 | 8 | 0.081 | 0.393 | Pericytes; pericytes |
| CAP | CDC 1 | 8 | 8 | 0.286 | 0.000 | cDC1 |
| CAP | MESOTHELIAL CELLS | 8 | 5 | 1.000 | 0.000 | Mesothelial cells; mesothelial cells |
| CAP | NEUTROPHILS | 7 | 7 | 0.500 | 0.000 | Neutrophils |
| CAP | MACROPHAGES MONOCYTES | 6 | 6 | 1.000 | 0.333 | Macrophages & Monocytes; Macrophages/Monocytes |
| LLMarkers | T CELL | 38 | 37 | 0.000 | 0.540 | T CELL; T-CELL; ΑΒ T CELL; ΓΔ T CELL |
| LLMarkers | B CELL | 30 | 30 | 0.125 | 0.425 | B CELL; B-CELL |
| LLMarkers | FIBROBLAST | 29 | 29 | 0.000 | 0.567 | FIBROBLAST |
| LLMarkers | MACROPHAGE | 29 | 29 | 0.000 | 0.702 | MACROPHAGE |
| LLMarkers | ENDOTHELIAL CELL | 28 | 28 | 0.000 | 0.503 | ENDOTHELIAL CELL |
| LLMarkers | MONOCYTE | 24 | 24 | 0.000 | 0.743 | MONOCYTE |
| LLMarkers | CELL | 19 | 8 | 0.000 | 0.593 | Α CELL; Α-CELL; Β CELL; Β-CELL; Γ-CELL; Δ-CELL; Ε-CELL |
| LLMarkers | CLUSTER 2 | 19 | 19 | 0.000 | 0.959 | CLUSTER 2; CLUSTER-2 |

## Interpretation

The comparison asks whether a curated resource reduces the two issues measured in LLMarkers: variable naming and local-to-global marker transfer.
A cleaner curated resource should have stronger same-label marker overlap across studies and fewer marker-identical pairs with different labels.
