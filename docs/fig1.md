# Figure 1 source audit

Figure 1 illustrates why marker genes reported within a study are local definitions of cell type and why those definitions can become ambiguous when studies are pooled.

The current figure has four visual parts:

1. **Local -> Global**: a toy binary marker matrix. Rows are study-specific reported cell types and columns are marker genes. A row can be identifiable within a study but unidentifiable after pooling if another study reports the same marker pattern for a different row.
2. **Paper Markers**: real extracted myeloid marker profiles from the corpus.
3. **Pooled Marker Matrix**: the displayed real profiles converted to a binary marker matrix. Red marks same-label profiles with different marker sets. Orange marks different-label profiles with identical marker sets. Checks mark rows with unique displayed marker patterns; Xs mark rows whose displayed marker pattern is shared by another row.
4. **Joint Distribution**: pair counts among the displayed real profiles, stratified by reported-label relation and marker-gene-set relation.

## Assumptions

- A marker profile is one paper, one reported cell type label, and one deduplicated marker gene set.
- Reported cell type labels are author-provided strings, not ontology-normalized cell identities.
- Marker relations are computed from displayed gene symbols after deduplication. In the full analysis, marker relations are computed on mapped gene IDs.
- Label relations in Figure 1 are conservative string relations:
  - **Exact**: normalized labels are identical.
  - **Partial**: labels share a major lexical stem used in the example, such as `macrophage`.
  - **Different**: neither exact nor partial.
- The Figure 1 example is illustrative. Corpus-wide frequencies and recurrent-label statistics are reported in the main cross-study analyses.
- An X means the row is not distinguishable by the displayed marker genes alone. It does not imply that the profiles are biologically different; duplicated marker profiles can reflect the same cell type, related states, or a shared marker program.

## Displayed Profiles

| ID | Paper label | Citation key | Source | Context | Reported cell type | Reported markers | Why included |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D | DecontX 2019 | `Yang2019decontx` | `docs/llmarkers.sqlite`, profile `3618` | Ambient RNA/decontamination benchmark using PBMC-like immune labels | `"Monocyte"` | LYZ, S100A8, S100A9, CD14 | Canonical inflammatory monocyte profile; anchors same-label and different-label partial marker overlaps. |
| H | HCNetlas 2024 | `Yu2024hcnetlas` | `docs/llmarkers.sqlite`, profile `3111` | Human cell network atlas / disease genetics | `"Monocyte"` | S100A8, S100A9, CD14 | Same reported label as D with a near-subset marker profile. |
| M | Leach 2020 | `Leach2020biorxiv070839` | `analysis/results/fig5_nomenclature_marker_cluster_membership.tsv`, profile `933`; source `data/biorxiv/meca/f787a6d9-6ce3-1014-a3f6-a662a1333571/markers.json` | Cross-species pulmonary and lymph node mononuclear phagocyte comparison | `"Monocytes"` | S100A8, S100A9, CD14 | Label-name variant with exact marker match to H. |
| I | IFN response 2023 | `Rigby2023` | `docs/llmarkers.sqlite`, profile `1430` | Type I interferon signaling response | `"Monocyte"` | ISG15, IFI44, IFIT5 | Same reported label as D/H but disjoint interferon-response marker profile. |
| L | Human liver 2022 | pending reference | `analysis/results/fig5_nomenclature_marker_cluster_membership.tsv`, profile `2188` | Matched single-cell, single-nucleus, and spatial human liver atlas | `"Inflammatory macrophages"` | LYZ, S100A8, S100A9 | Different reported label with strong overlap to the monocyte inflammatory program. |
| C | Dominguez Conde 2022 | `Dominguez2022celltypist` | `analysis/results/fig5_nomenclature_marker_cluster_membership.tsv`, profile `1545` | Cross-tissue human immune atlas | `"Classical"` | S100A8, S100A9, S100A12 | Different reported label sharing an alarmin/inflammatory myeloid marker program. |
| P | Peng 2023 | `Werba2023pdac` | `analysis/results/fig5_nomenclature_marker_cluster_membership.tsv`, profile `2450` | Pancreatic adenocarcinoma tumor microenvironment after chemotherapy | `"MDSC"` | S100A8, S100A9, S100A12 | Different reported label with exact marker match to C and R. |
| R | Pelka 2021 | `Pelka2021crc` | `analysis/results/fig5_nomenclature_marker_cluster_membership.tsv`, profile `3068` | Spatial immune hubs in colorectal cancer | `"Macrophage"` | S100A8, S100A9, S100A12 | Different reported label with exact marker match to C and P. |
| G1 | Glioblastoma 2023 | local corpus reference | `docs/llmarkers.sqlite`, profile `1420` | Glioblastoma single-cell profiling and zebrafish avatars | `"Macrophage"` | CD68 | Same broad label as R with disjoint marker profile. |
| G2 | Synovium 2024 | local corpus reference | `docs/llmarkers.sqlite`, profile `1855` | Synovial mesenchymal stem cell subpopulation study | `"Macrophage"` | CD68 | Same broad label and exact marker match with G1. |

## Displayed Marker Matrix

The pooled marker matrix uses the following columns:

`LYZ`, `S100A8`, `S100A9`, `CD14`, `S100A12`, `ISG15`, `IFI44`, `IFIT5`, `CD68`

Binary rows:

| ID | LYZ | S100A8 | S100A9 | CD14 | S100A12 | ISG15 | IFI44 | IFIT5 | CD68 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| D | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| H | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| M | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| I | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 |
| L | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| C | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| P | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| R | 0 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| G1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| G2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |

Identifiability status in the displayed matrix:

| ID | Status | Reason |
| --- | --- | --- |
| D | identifiable | Unique marker pattern among displayed profiles. |
| H | unidentifiable | Shares the displayed marker pattern `S100A8, S100A9, CD14` with M. |
| M | unidentifiable | Shares the displayed marker pattern `S100A8, S100A9, CD14` with H. |
| I | identifiable | Unique marker pattern among displayed profiles. |
| L | identifiable | Unique marker pattern among displayed profiles. |
| C | unidentifiable | Shares the displayed marker pattern `S100A8, S100A9, S100A12` with P and R. |
| P | unidentifiable | Shares the displayed marker pattern `S100A8, S100A9, S100A12` with C and R. |
| R | unidentifiable | Shares the displayed marker pattern `S100A8, S100A9, S100A12` with C and P. |
| G1 | unidentifiable | Shares the displayed marker pattern `CD68` with G2. |
| G2 | unidentifiable | Shares the displayed marker pattern `CD68` with G1. |

## Pair Counts

Pair counts are unordered pairs among the ten displayed profiles.

Label relation:

- **Exact**: same normalized reported label.
- **Partial**: shared major label stem or simple name variant. In this example, `"Monocyte"`/`"Monocytes"` and `"Inflammatory macrophages"`/`"Macrophage"` are partial label matches.
- **Different**: all other label pairs.

Marker relation:

- **Exact**: identical marker set, `J = 1`.
- **Partial**: nonzero but incomplete marker overlap, `0 < J < 1`.
- **None**: disjoint marker sets, `J = 0`.

Joint distribution:

| Label relation | Exact markers | Partial markers | No markers |
| --- | ---: | ---: | ---: |
| Exact label | 1 | 1 | 4 |
| Partial label | 1 | 2 | 3 |
| Different label | 3 | 14 | 16 |

Notable pairs:

| Pair | Label relation | Marker relation | Shared genes | Jaccard | Interpretation |
| --- | --- | --- | --- | ---: | --- |
| D--H | Exact | Partial | S100A8, S100A9, CD14 | 0.75 | Same label, near-subset inflammatory monocyte markers. |
| H--M | Partial | Exact | S100A8, S100A9, CD14 | 1.00 | Simple label-name variant with the same marker profile. |
| D--I | Exact | None | none | 0.00 | Same label, different interferon-response marker program. |
| G1--G2 | Exact | Exact | CD68 | 1.00 | Same broad macrophage label and same marker. |
| L--R | Partial | Partial | S100A8, S100A9 | 0.50 | Macrophage-related labels with overlapping inflammatory markers. |
| C--P | Different | Exact | S100A8, S100A9, S100A12 | 1.00 | Different labels sharing the same alarmin/inflammatory myeloid marker program. |
| P--R | Different | Exact | S100A8, S100A9, S100A12 | 1.00 | Disease-context MDSC label and macrophage label sharing the same marker program. |

## Source Files

- Figure body: `paper/src/figures/fig_paper_celltype_joint_body.tex`
- Figure wrapper and caption: `paper/src/figures/fig_paper_celltype_joint.tex`
- Standalone wrapper: `paper/src/figures/standalone/fig1_paper_celltype_joint.tex`
- Corpus database: `docs/llmarkers.sqlite`
- Cross-study cluster membership table: `analysis/results/fig5_nomenclature_marker_cluster_membership.tsv`
- Reviewed cross-study context comparisons: `analysis/results/cross_study_context_comparison_review_anchored.tsv`
