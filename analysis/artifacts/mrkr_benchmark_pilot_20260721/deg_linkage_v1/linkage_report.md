# mrkr DEG-source linkage experiment

This analysis is separate from the `mrkr` extraction schema. The LLM selected one paper-specific DEG source for each validated marker claim from a catalog containing only source IDs and their cell-type labels.

- Papers: 7
- Claims: 153
- Positive mapped gene terms: 369
- Model: `claude-opus-4-6`

## Macro-average results

| Method | Claim link rate | Exact triple F1 | Source+gene F1 | Claim source-link accuracy |
| --- | ---: | ---: | ---: | ---: |
| LLM | 0.966 | 0.313 | 0.527 | 0.847 |
| Exact-label baseline | 0.565 | 0.341 | 0.250 | 0.374 |

## Pooled claim-level linkage

| Matching evidence | LLM | Exact-label baseline | Paired exact p |
| --- | ---: | ---: | ---: |
| Exact target+gene | 50/59 (84.7%) | 36/59 (61.0%) | 0.000519 |
| Source-overlapping gene | 82/91 (90.1%) | 28/91 (30.8%) | 1.58e-15 |

The claim-level analysis is primary because the model selects one `data_id` per claim. Exact triple F1 requires the selected `data_id`, normalized target label, and gene. Source+gene F1 requires the selected `data_id` and gene to overlap the human-curated source span without requiring the normalized target label. Conditional linkage accuracy is calculated only for claims already matched to human evidence by at least one marker term, so it isolates source selection from extraction coverage. The paired exact test is descriptive because claims within a paper are not independent.

## Per-paper results

| Paper | Claims | Sources | LLM triple F1 | LLM source+gene F1 | LLM claim link accuracy | Baseline claim link accuracy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Adams2020 | 18 | 8 | 0.466 | 0.457 | 0.667 | 0.500 |
| Emont2022 | 17 | 6 | 0.111 | 0.607 | 0.692 | 0.154 |
| Gautam2021 | 29 | 7 | 0.242 | 0.330 | 1.000 | 0.500 |
| He2021 | 28 | 5 | 0.365 | 0.530 | 1.000 | 0.200 |
| Hildreth2021 | 24 | 4 | 0.276 | 0.806 | 1.000 | 0.300 |
| Shamis2020 | 20 | 6 | 0.117 | 0.513 | 1.000 | 0.250 |
| Wagner2020 | 17 | 3 | 0.611 | 0.447 | 0.571 | 0.714 |
