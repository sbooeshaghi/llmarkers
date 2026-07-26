# Joint marker extraction and DEG-source assignment

One prompt received the full manuscript and its candidate `data_id` to cell-type-label catalog, then jointly extracted marker claims and selected one supporting DEG source.

- Papers: 7
- Model: `claude-opus-4-6`
- Raw associations: 325
- Retained claims: 152
- Mapped marker terms: 311
- Excluded unsupported or ambiguous associations: 5
- Mean exact cell type--gene F1: 0.638
- Mean exact data ID--cell type--gene F1: 0.608

| Paper | Claims | Terms | Pair F1 | Triple F1 | Source+gene F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Adams2020 | 12 | 44 | 0.687 | 0.537 | 0.514 |
| Emont2022 | 19 | 26 | 0.679 | 0.607 | 0.464 |
| Gautam2021 | 24 | 33 | 0.533 | 0.525 | 0.438 |
| He2021 | 34 | 57 | 0.527 | 0.510 | 0.559 |
| Hildreth2021 | 17 | 47 | 0.832 | 0.832 | 0.783 |
| Shamis2020 | 36 | 69 | 0.624 | 0.624 | 0.447 |
| Wagner2020 | 10 | 35 | 0.581 | 0.620 | 0.323 |
