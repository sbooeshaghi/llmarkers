# Myeloid Marker Cluster Summary

## Assumptions

- Unit of analysis is one paper-celltype marker profile: a paper, a reported cell type label, and a binary vector of mapped Ensembl gene IDs.
- Profiles are restricted to human, source-verified marker records with at least three mapped marker genes.
- Myeloid profiles are selected by regex over reported labels and include monocyte/macrophage, dendritic, mast/granulocyte, microglia, MDSC, and broad myeloid labels.
- Marker groups are connected components of cross-paper profiles with marker-gene Jaccard >= 0.50.
- Program labels are heuristic marker-gene summaries used for figure orientation, not a proposed ontology.
- Region labels in the C1-C3 summary use label-linked fraction >= 0.25 and mean marker Jaccard >= 0.20 as visual thresholds.

## Outputs

- Figure: `analysis/figures/fig_myeloid_profile_graph_comparison.pdf`
- Summary table: `analysis/results/myeloid_marker_cluster_summary.tsv`
- Membership table: `analysis/results/myeloid_marker_cluster_membership.tsv`
- C1-C3 comparison table: `analysis/results/myeloid_c1_c3_label_marker_summary.tsv`

## Counts

- Myeloid profiles: 272
- Papers: 155
- Reported labels: 133
- Marker groups displayed: 5
