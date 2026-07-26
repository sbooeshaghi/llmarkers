# mrkr corpus analysis v1

## Corpus

- 979 validated papers (504 bioRxiv; 475 HCA).
- 721 papers contain at least one extracted marker statement.
- 11,336 source-grounded marker statements and 25,657 mapped positive marker-gene evidence rows.
- 586 statements (5.2%) explicitly record a comparison term.
- 651 paper--cell type combinations contain mapped negative-marker evidence; these are excluded from positive-panel reuse analyses.
- 0 source records share a normalized article title with another record; cross-paper analyses exclude pairs from the same article key.

## Reuse by reported label

Each reported marker gene panel combines mapped positive markers for one normalized cell type label in one paper. The primary analysis requires at least 3 markers per panel.

- 10,437 pairs of papers use the same cell type label and report at least 3 markers for it.
- 51.4% share at least one marker; mean marker Jaccard is 0.121 (median 0.059).
- In marker-count-bin- and collection-matched pairs with different labels, 1.8% share a marker and mean Jaccard is 0.003.
- When each recurring label receives equal weight, pairs of papers using the same label share any marker at 56.3% versus 1.9% in matched controls; mean Jaccard is 0.167 versus 0.003.
- 117 of 312 recurring labels have a non-empty strict intersection across every retained marker gene panel.
- In the fixed cohort of 37 labels reported in at least 10 papers, the estimated fraction retaining a shared marker is 51.8% after combining two papers, 11.3% after five, and 1.7% after ten.
- The accepted-identifier sensitivity analysis uses 27 Cell Ontology identifiers and gives 1.4% after ten papers.

## Local reporting and global recovery

For 1,568 reported marker gene panels evaluable both within and across papers, median reported-panel exclusivity within the source paper is 1.000, while median leave-one-paper-out marker recovery among panels with the same label is 0.185. Their Spearman correlation is 0.093. Reported-panel exclusivity measures whether a marker is absent from other extracted panels in the paper; it is not an expression-based specificity estimate.

## Ontology sensitivity analysis

Cell Ontology recurrence uses only target labels equal to a canonical label or an exact synonym in the pinned ontology release. Broad, narrow, related, and matches based only on full-text coverage are excluded.

- 406 of 3,355 distinct reported-label-to-Cell-Ontology mappings pass this semantic exactness test; 130 mappings marked exact by full-text coverage do not.
- 9,082 cross-article pairs share a conservatively accepted Cell Ontology term. 50.4% share a marker; mean Jaccard is 0.119.
- Stable Cell Ontology identifiers link 248 cross-article panel pairs that use different normalized labels across 12 ontology terms. After balancing ontology terms, 60.0% of these pairs share a marker.
- Exact labels miss all 248 of these different-label connections. In the pair-weighted matched analysis, 45.6% of the identifier-recovered pairs share a marker, compared with 49.2% for matched same-label pairs with an accepted identifier, 54.1% for matched same-label pairs without an accepted identifier, and 1.6% for matched pairs with different identifiers.

## Co-reported label context

Among pairs of papers using the same cell type label, marker Jaccard has Pearson r=0.149 and Spearman rho=0.165 with co-reported-label Jaccard; the fitted slope is 0.322. After centering within each label, Pearson r is 0.146. This is a descriptive context proxy, not a reconstructed experimental contrast.


## Interpretation boundary

The analysis measures recurrence of reported, source-grounded marker panels. It does not establish that a recurrent marker is a formal marker under every relevant pairwise comparison. The extracted comparison term is sparse, and manuscript text cannot reconstruct unreported contrasts or sufficient statistics.
