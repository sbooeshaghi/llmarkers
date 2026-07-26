# mrkr versus source-specific benchmark

- Papers: 7
- Human text source records: 867
- Human text semantic marker terms: 469
- Human text pairs summed within papers: 401
- Unique human text+image pairs across papers: 1550
- Unique all-organism text+image pairs across papers: 1560
- mrkr claims: 153
- mrkr gene terms: 394 (370 positive; 24 negative)
- Exact source-span rate: 1.000
- Explicit target+gene rate: 0.916

## Macro-average comparison

| Evaluation | Precision | Recall | F1 |
| --- | ---: | ---: | ---: |
| Gene identity only | 0.787 | 0.761 | 0.744 |
| Strict target label + gene | 0.373 | 0.397 | 0.358 |
| Grounded target + gene | 0.316 | 0.272 | 0.278 |
| Source-anchored gene | 0.619 | 0.727 | 0.630 |
| Strict pair against text+image | 0.397 | 0.128 | 0.176 |
| Legacy reported strict pair | 0.712 | 0.724 | 0.685 |

The legacy result and current strict-pair result are different model outputs and different target-normalization pipelines. The source-anchored metric separates marker extraction from target-label normalization.

## Candidate term disposition

- exact_label_pair: 140
- gene_only: 41
- not_in_text_truth: 75
- same_gene_source_overlap: 64
- same_grounded_pair: 49
- unmapped_gene: 1
