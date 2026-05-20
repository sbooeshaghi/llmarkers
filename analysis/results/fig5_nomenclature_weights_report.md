# Nomenclature Gene Weights Prototype

## Assumptions

- Unit of analysis is a cross-paper pair of marker profiles that share at least one frequent mapped marker gene.
- Frequent genes are those present in at least 4 marker profiles.
- The myeloid C1-C3 subset uses a lower threshold of 2 marker profiles because it is a focused lineage subset.
- Target is whether reported labels are exact or partial matches after label normalization.
- Predictors are binary indicators for which marker genes are shared by the pair.
- Evaluation holds out papers, trains on pairs where both papers are in the training set, and tests on pairs where both papers are in the held-out set.
- The learned gene weights quantify predictability of reported nomenclature, not ground-truth cell identity.

## Counts

- Marker profiles: 3,351
- Papers: 599
- Cross-paper shared-gene pairs: 112,062
- Label-linked pair fraction: 0.095
- Genes with nonzero coefficients: 799
- Label terms scored: 125
- Exact labels scored by marker silhouette: 162
- Marker-gene clusters scored for label purity: 51
- Marker-gene clusters scored by label silhouette: 51
- Label-derived example genes scored: 87
- Marker-derived example genes scored: 98
- Label/marker example gene F1 scores compared: 140
- Myeloid C1-C3 marker profiles: 44
- Myeloid C1-C3 shared-gene pairs: 485
- Myeloid C1-C3 label-linked pair fraction: 0.326
- Myeloid C1-C3 genes with nonzero coefficients: 6
- Myeloid C1-C3 label terms scored: 4
- Myeloid C1-C3 exact labels scored by marker silhouette: 6

## Cross-Validation Metrics

| model | AUROC mean | AUROC sd | AUPRC mean | AUPRC sd |
|---|---:|---:|---:|---:|
| plain Jaccard | 0.644 | 0.023 | 0.165 | 0.017 |
| shared gene count | 0.601 | 0.012 | 0.133 | 0.021 |
| weighted shared genes | 0.707 | 0.019 | 0.217 | 0.021 |

## Outputs

- Figure: `analysis/figures/fig5_nomenclature_weights.pdf`
- Gene weights: `analysis/results/fig5_nomenclature_gene_weights.tsv`
- Pair scores: `analysis/results/fig5_nomenclature_pair_scores.tsv`
- Cross-validation metrics: `analysis/results/fig5_nomenclature_cv_metrics.tsv`
- Label token scores: `analysis/results/fig5_nomenclature_label_token_scores.tsv`
- Label silhouette scores: `analysis/results/fig5_nomenclature_label_silhouette_scores.tsv`
- Marker cluster summary: `analysis/results/fig5_nomenclature_marker_cluster_summary.tsv`
- Marker cluster membership: `analysis/results/fig5_nomenclature_marker_cluster_membership.tsv`
- Marker cluster label silhouette: `analysis/results/fig5_nomenclature_marker_cluster_label_silhouette.tsv`
- Label-derived example gene scores: `analysis/results/fig5_nomenclature_label_group_gene_scores.tsv`
- Marker-derived example gene scores: `analysis/results/fig5_nomenclature_marker_group_gene_scores.tsv`
- Label/marker example gene F1 comparison: `analysis/results/fig5_nomenclature_group_gene_f1_comparison.tsv`
- Myeloid C1-C3 gene weights: `analysis/results/fig5_myeloid_nomenclature_gene_weights.tsv`
- Myeloid C1-C3 pair scores: `analysis/results/fig5_myeloid_nomenclature_pair_scores.tsv`
- Myeloid C1-C3 label token scores: `analysis/results/fig5_myeloid_nomenclature_label_token_scores.tsv`
- Myeloid C1-C3 label silhouette scores: `analysis/results/fig5_myeloid_nomenclature_label_silhouette_scores.tsv`
