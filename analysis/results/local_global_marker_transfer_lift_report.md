# Local-to-Global Marker Transfer Lift

This analysis asks whether marker genes reported for a cell type in one paper transfer to related profiles in other papers more often than expected by corpus background frequency.

For a reported profile with marker set `S`, observed recovery is the fraction of genes in `S` found in outside-paper profiles with the same reported label or same broad lineage. Expected recovery is computed from outside-paper gene prevalence in LLMarkersDB. Lift is `observed / expected`.

The union metric asks whether a marker is recovered in any related outside-paper profile. The mean-profile metric asks how much of the marker set is recovered in an average related profile.

Caveat: absence means not reported as a marker in this corpus, not absent expression.

## Headline

- Same-label outside-paper profiles recovered a median 0.400 of all reported markers, versus 0.026 expected from background prevalence (median lift 8.03x).
- For locally private markers, same-label profiles recovered a median 0.429, versus 0.024 expected (median lift 7.92x).

## Summary

| relation | relation_label | marker_scope | marker_scope_label | n_profiles | median_n_markers | median_n_comparison_profiles | median_observed_union_recall | median_expected_union_recall | median_union_recall_lift | pct_union_lift_gt_1 | median_observed_mean_profile_recall | median_expected_mean_profile_recall | median_mean_profile_recall_lift | pct_mean_lift_gt_1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| same_broad_neighborhood | Same broad lineage | all_reported_markers | All reported markers | 1010 | 4.000 | 148.500 | 0.833 | 0.489 | 1.381 | 0.862 | 0.045 | 0.006 | 6.651 | 0.911 |
| same_broad_neighborhood | Same broad lineage | local_private_markers | Local-only markers | 909 | 3.000 | 148.000 | 0.875 | 0.453 | 1.448 | 0.843 | 0.040 | 0.006 | 6.576 | 0.882 |
| same_exact_label | Same reported label | all_reported_markers | All reported markers | 1026 | 4.000 | 6.000 | 0.400 | 0.026 | 8.029 | 0.764 | 0.133 | 0.005 | 22.162 | 0.762 |
| same_exact_label | Same reported label | local_private_markers | Local-only markers | 955 | 3.000 | 6.000 | 0.429 | 0.024 | 7.923 | 0.739 | 0.130 | 0.004 | 23.491 | 0.737 |

## Highest Same-Label Paper-Level Lift

| paper_key | n_profiles_with_comparison | paper_n_profiles | local_marker_lb_log2 | marker_lb_gap_log2 | median_observed_union_recall | median_expected_union_recall | median_union_recall_lift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hca:0081_10.1038_s41598-020-66092-9_e23219ced0 | 4 | 7 | 3 | 9 | 0.450 | 0.002 | 305.420 |
| hca:0082_10.1016_j.cell.2020.08.013_e864ee2cef | 5 | 12 | 4 | 8 | 0.167 | 0.001 | 222.693 |
| hca:0493_10.1161_circulationaha.119.045401_814f085618 | 4 | 6 | 3 | 9 | 0.833 | 0.008 | 126.247 |
| biorxiv:e7144333-745a-1014-ab12-e9455a30c9da | 3 | 5 | 3 | 9 | 0.667 | 0.011 | 69.707 |
| hca:0497_10.1016_j.cell.2016.03.023_1e72ea1d04 | 3 | 3 | 2 | 10 | 0.417 | 0.010 | 67.068 |
| hca:0008_10.1016_j.cels.2016.09.002_fd6b21337a | 3 | 3 | 2 | 10 | 0.562 | 0.011 | 64.095 |
| hca:0317_10.1016_j.celrep.2019.02.043_aed04e8aae | 5 | 7 | 3 | 9 | 0.625 | 0.016 | 63.130 |
| hca:0448_10.1101_2022.02.15.480622_6cb3eae5b8 | 3 | 3 | 2 | 10 | 0.750 | 0.013 | 57.745 |
| biorxiv:4c59ca94-6c5e-1014-84d0-e9a5aa46ffef | 4 | 4 | 2 | 10 | 0.550 | 0.009 | 57.368 |
| hca:0090_10.1038_s41586-021-03852-1_eec89a5e36 | 5 | 27 | 5 | 7 | 0.750 | 0.014 | 47.514 |

## Recurrent Labels With High Transfer Lift

| normalized_cell_type | n_profiles | n_papers | median_observed_union_recall | median_expected_union_recall | median_union_recall_lift | example_reported_labels |
| --- | --- | --- | --- | --- | --- | --- |
| ADIPOCYTE | 5 | 5 | 0.667 | 0.005 | 138.657 | ADIPOCYTE |
| ACINAR CELL | 7 | 7 | 0.333 | 0.006 | 131.492 | ACINAR CELL |
| TUFT CELL | 5 | 5 | 0.500 | 0.007 | 128.117 | TUFT CELL |
| ENTEROCYTE | 6 | 6 | 0.633 | 0.007 | 87.659 | ENTEROCYTE |
| EXCITATORY NEURON | 5 | 5 | 0.222 | 0.004 | 83.650 | EXCITATORY NEURON |
| HEPATOCYTE | 5 | 5 | 0.429 | 0.006 | 76.351 | HEPATOCYTE |
| DELTA CELL | 5 | 5 | 0.625 | 0.007 | 74.927 | DELTA CELL |
| MELANOCYTE | 7 | 7 | 1.000 | 0.020 | 49.650 | MELANOCYTE |
| ALPHA CELL | 6 | 6 | 0.513 | 0.014 | 47.796 | ALPHA CELL |
| HSC | 5 | 5 | 0.400 | 0.010 | 44.086 | HSC |

## Recurrent Labels With Low Transfer Lift

| normalized_cell_type | n_profiles | n_papers | median_observed_union_recall | median_expected_union_recall | median_union_recall_lift | example_reported_labels |
| --- | --- | --- | --- | --- | --- | --- |
| T CELLS | 5 | 5 | 0.000 | 0.030 | 0.000 | T CELLS; ΑΒ T CELLS; ΓΔ T CELLS |
| CLUSTER 4 | 11 | 11 | 0.000 | 0.054 | 0.000 | CLUSTER 4; CLUSTER-4 |
| CLUSTER 5 | 9 | 9 | 0.000 | 0.029 | 0.000 | CLUSTER 5 |
| PC | 5 | 5 | 0.000 | 0.014 | 0.000 | PC; PΑC |
| DENDRITIC CELL | 7 | 7 | 0.000 | 0.011 | 0.000 | DENDRITIC CELL |
| IMMUNE CELL | 7 | 7 | 0.000 | 0.028 | 0.000 | IMMUNE CELL |
| C 1 | 6 | 6 | 0.000 | 0.018 | 0.000 | C1 |
| CLUSTER 1 | 14 | 14 | 0.000 | 0.052 | 0.000 | CLUSTER 1; CLUSTER-1 |
| CLUSTER 0 | 5 | 5 | 0.000 | 0.018 | 0.000 | CLUSTER 0 |
| DC | 5 | 5 | 0.000 | 0.011 | 0.000 | DC |
