# Marker Identifiability Analysis

This analysis applies the Lean formalization in `formal/MarkerIdentifiability/Basic.lean` to the LLMarkers reported-marker matrix.
For each partition, a gene is turned on for a group if it is reported in at least the stated fraction of profiles in that group.
The Lean theorem gives the information lower bound: if `k` induced binary signatures are separated by binary markers, any separating panel needs at least `ceil(log2(k))` marker coordinates.

Important caveat: zeros in this matrix mean not reported as a marker in the corpus, not absent expression.

## Partition Summary

| partition | coverage_threshold | n_groups | n_distinct_signatures | all_groups_identifiable_with_all_genes | information_lower_bound_log2 | greedy_panel_size | ilp_panel_size | ilp_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| broad_neighborhoods | 0.05 | 8 | 8 | True | 3 | 6 | 6 | optimal |
| broad_neighborhoods | 0.1 | 8 | 8 | True | 3 | 7 | 7 | optimal |
| broad_neighborhoods | 0.2 | 8 | 5 | False | 3 | 4 | 4 | optimal |
| reported_exact_labels_min5 | 0.05 | 73 | 73 | True | 7 | 30 |  | Time limit reached. (HiGHS Status 13: Time limit reached) |
| reported_exact_labels_min5 | 0.1 | 73 | 73 | True | 7 | 35 |  | Time limit reached. (HiGHS Status 13: Time limit reached) |
| reported_exact_labels_min5 | 0.2 | 73 | 67 | False | 7 | 47 | 44 | optimal |
| tcell_marker_clusters | 0.05 | 7 | 7 | True | 3 | 4 | 4 | optimal |
| tcell_marker_clusters | 0.1 | 7 | 7 | True | 3 | 5 | 5 | optimal |
| tcell_marker_clusters | 0.2 | 7 | 7 | True | 3 | 5 | 5 | optimal |
| myeloid_marker_clusters | 0.05 | 5 | 5 | True | 3 | 3 | 3 | optimal |
| myeloid_marker_clusters | 0.1 | 5 | 5 | True | 3 | 3 | 3 | optimal |
| myeloid_marker_clusters | 0.2 | 5 | 5 | True | 3 | 3 | 3 | optimal |

## ILP-Selected Marker Panels

- **broad_neighborhoods**, threshold 0.05: CD27 (exchangeable in minimum panels), COL3A1 (exchangeable in minimum panels), MUC2 (exchangeable in minimum panels), PECAM1 (exchangeable in minimum panels), CCL3 (exchangeable in minimum panels), CCL4 (exchangeable in minimum panels)
- **broad_neighborhoods**, threshold 0.10: COL3A1 (exchangeable in minimum panels), CD19 (exchangeable in minimum panels), CD163 (exchangeable in minimum panels), KRT14 (exchangeable in minimum panels), CLEC9A (exchangeable in minimum panels), CD3E (exchangeable in minimum panels), PECAM1 (exchangeable in minimum panels)
- **broad_neighborhoods**, threshold 0.20: CD19 (exchangeable in minimum panels), CLEC9A (exchangeable in minimum panels), FCGR3A (exchangeable in minimum panels), PECAM1 (exchangeable in minimum panels)
- **reported_exact_labels_min5**, threshold 0.20: CD4 (essential in minimum panels), DCN (essential in minimum panels), CD74 (exchangeable in minimum panels), CD79A (exchangeable in minimum panels), ACTA2 (essential in minimum panels), COL1A1 (essential in minimum panels), VEGFA (exchangeable in minimum panels), GCG (essential in minimum panels), SOX9 (exchangeable in minimum panels), MYH11 (exchangeable in minimum panels), IL2RA (exchangeable in minimum panels), PDGFRA (essential in minimum panels), GLUL (essential in minimum panels), RGS5 (exchangeable in minimum panels), SPARCL1 (exchangeable in minimum panels), CD8A (exchangeable in minimum panels), KIT (exchangeable in minimum panels), CD1C (exchangeable in minimum panels), PDPN (exchangeable in minimum panels), NEUROD1 (essential in minimum panels), EOMES (exchangeable in minimum panels), FABP1 (exchangeable in minimum panels), IL7R (exchangeable in minimum panels), FASN (exchangeable in minimum panels), CD14 (exchangeable in minimum panels), MZB1 (exchangeable in minimum panels), CD34 (exchangeable in minimum panels), PCSK1 (exchangeable in minimum panels), CD163 (exchangeable in minimum panels), ASCL2 (exchangeable in minimum panels), IRF7 (exchangeable in minimum panels), PMEL (exchangeable in minimum panels), KRT14 (exchangeable in minimum panels), SEMA4A (exchangeable in minimum panels), TCF4 (exchangeable in minimum panels), SERPINA1 (exchangeable in minimum panels), MYH6 (exchangeable in minimum panels), MBP (exchangeable in minimum panels), CLEC9A (exchangeable in minimum panels), MUC2 (exchangeable in minimum panels), FCGR3A (exchangeable in minimum panels), MAFB (exchangeable in minimum panels), PRSS1 (exchangeable in minimum panels), PECAM1 (exchangeable in minimum panels)
- **tcell_marker_clusters**, threshold 0.05: LAG3 (exchangeable in minimum panels), GZMK (exchangeable in minimum panels), EOMES (exchangeable in minimum panels), IL7R (exchangeable in minimum panels)
- **tcell_marker_clusters**, threshold 0.10: EOMES (exchangeable in minimum panels), IL7R (exchangeable in minimum panels), TIGIT (exchangeable in minimum panels), CD3E (exchangeable in minimum panels), FCGR3A (exchangeable in minimum panels)
- **tcell_marker_clusters**, threshold 0.20: FGFBP2 (exchangeable in minimum panels), IL7R (essential in minimum panels), CD3E (essential in minimum panels), ITGA1 (exchangeable in minimum panels), CCL4 (exchangeable in minimum panels)
- **myeloid_marker_clusters**, threshold 0.05: CD163 (exchangeable in minimum panels), TPSB2 (exchangeable in minimum panels), AIF1 (exchangeable in minimum panels)
- **myeloid_marker_clusters**, threshold 0.10: CD14 (essential in minimum panels), CD163 (essential in minimum panels), CLEC9A (exchangeable in minimum panels)
- **myeloid_marker_clusters**, threshold 0.20: CD14 (essential in minimum panels), CD163 (essential in minimum panels), TPSB2 (exchangeable in minimum panels)

## Duplicate Signatures

- **broad_neighborhoods**, threshold 0.20, S3: T cell; epithelial; fibroblast/stromal; monocyte/macrophage
- **reported_exact_labels_min5**, threshold 0.20, S12: C 1; CLUSTER 1; CLUSTER 2; CLUSTER 3; CLUSTER 4; DENDRITIC CELL
- **reported_exact_labels_min5**, threshold 0.20, S25: EC; ENDOTHELIAL CELL
