# Marker Program Source Review

## Scope

This review traces the current marker-program examples back to source-linked marker records. The review uses source-verified human marker records from the bioRxiv and HCA corpora, the Figure 3 marker-program score table, and the myeloid marker-cluster tables.

Primary inputs:

- `analysis/results/fig5_nomenclature_group_gene_f1_comparison.tsv`
- `analysis/results/fig5_nomenclature_marker_cluster_membership.tsv`
- `analysis/results/myeloid_marker_cluster_summary.tsv`
- `analysis/results/myeloid_marker_cluster_membership.tsv`
- `analysis/results/myeloid_c1_c3_label_marker_summary.tsv`

## TREG / Exhaustion Program

### Summary

The source evidence supports a TREG-containing suppressive/exhaustion marker program, not a pure TREG lineage-marker story. This is useful for the manuscript because it demonstrates exactly the ambiguity we want to expose: exact cell type labels recover canonical TREG-associated genes, while marker-defined neighborhoods pull in checkpoint/exhaustion programs that appear under multiple T-cell labels.

### Strong claims supported by the source records

- `FOXP3` behaves like the clearest TREG-associated anchor. It appears repeatedly in exact TREG or regulatory T-cell contexts and remains strong in the marker-defined cluster.
- `IL2RA`, `CTLA4`, and `TIGIT` are TREG-associated in some source records, but they also appear in activated, suppressive, or exhausted T-cell contexts. They should not be described as lineage-specific.
- `HAVCR2`, `LAG3`, `PDCD1`, `CXCL13`, and `TOX` are better interpreted as exhaustion/checkpoint/state-associated genes. They are enriched in the marker-defined cluster relative to the exact TREG label group.
- `BATF`, `TNFRSF4`, `CCR8`, `LAYN`, and `IKZF2` are plausible Treg-state or tumor-associated regulatory markers, but they need more careful source-by-source treatment before serving as headline examples.
- `RAB33A` should not be used as a main biological example without additional review.

### Source evidence pattern

Representative source-linked claims:

- `FOXP3`, `IKZF2`, `IL2RA`, and `CTLA4` are directly listed as characteristic Treg markers in a lung cancer progression study.
- `TIGIT`, `TNFRSF4`, `CTLA4`, and `IL2RA` are listed as immunosuppressive markers of Treg cells in a tumor-tissue context.
- `CXCL13`, `LAG3`, `CTLA4`, and `HAVCR2` are listed as higher in dysfunctional CD8 T-cell states.
- `PDCD1`, `CTLA4`, `HAVCR2`, and `LAG3` are listed as co-inhibitory or exhaustion-associated genes in terminally differentiated CD8 T-cell populations.
- `CTLA4`, `PDCD1`, `HAVCR2`, and `TIGIT` are listed as exhaustion markers in CD4 T cells in melanoma.

### Recommended interpretation

The strongest wording is:

> A marker-defined T-cell neighborhood linked exact TREG labels to broader suppressive and exhausted T-cell states. In this neighborhood, `FOXP3` remained the clearest TREG-associated anchor, while checkpoint genes such as `HAVCR2`, `LAG3`, `PDCD1`, `TIGIT`, and `CXCL13` were more strongly recovered by the marker-defined group than by exact TREG labels alone.

This is defensible because it does not claim that the checkpoint genes are TREG lineage markers. It says that the marker graph uses them to reveal a broader program that crosses labels.

## Myeloid Programs

### Summary

The myeloid examples are more conservative and probably easier to defend biologically. The clusters separate inflammatory monocyte-like profiles from complement/macrophage-like profiles, while preserving the fact that authors often use overlapping labels such as monocyte, macrophage, myeloid cell, and MDSC.

### Component 1: inflammatory monocyte-like

Core genes: `S100A8`, `S100A9`, `CD14`; frequent additional genes include `LYZ`, `VCAN`, and `S100A12`.

Supported interpretation:

- These records are repeatedly linked to monocyte, CD14+ monocyte, monocyte-derived cell, inflammatory monocyte, dysfunctional CD14 monocyte, MDSC, or broad myeloid labels.
- Source records explicitly group `S100A8`, `S100A9`, `VCAN`, and `CD14` with CD14+ monocytes or inflammatory myeloid cells.
- `S100A12` appears in dysfunctional CD14 monocyte and MDSC contexts, making it more state/context-associated than broadly canonical.

Representative source evidence:

- A PBMC marker list links `CD14`, `LYZ`, `LGALS3`, and `S100A8` to CD14+ monocytes.
- A PBMC study reports CD14+ monocytes and macrophages expressing higher `S100A8`, `S100A9`, `VCAN`, `CD14`, and `CD163` than FCGR3A+ monocytes.
- A lung cancer study describes an inflammatory score for cDC2.1 using `CD14`, `S100A8`, `S100A9`, and `VCAN`.
- An HCA-linked pancreatic cancer study lists MDSC markers as `S100A8`, `S100A9`, and `S100A12`.

### Component 2: complement/macrophage-like

Core genes: `C1QB`, `CD163`; frequent additional genes include `C1QA`, `C1QC`, `MRC1`, and `MSR1`.

Supported interpretation:

- These records are repeatedly linked to macrophage, donor macrophage, border-associated macrophage, C1QC+ macrophage, and related macrophage-like contexts.
- Complement genes `C1QA`, `C1QB`, and `C1QC` are repeatedly reported together.
- `CD163`, `MRC1`, and `MSR1` support a macrophage/border-associated macrophage axis.

Representative source evidence:

- A lung cancer study lists `STARD13`, `CD163`, and `MRC1` for STRAD13+ macrophages.
- An HCA-linked ABMR kidney study reports donor macrophages differentially expressing `C1QA`, `C1QB`, and `C1QC`.
- A pancreatic cancer study lists C1QC+ macrophage markers as `C1QA`, `C1QB`, and `C1QC`.
- A brain glia study identifies border-associated macrophages as positive for `CD163`, `LYVE1`, and `MRC1`.

### Component 3: monocyte/macrophage bridge

Core genes: `CD14`, `CD68`; frequent additional genes include `FCGR3A`, `CD163`, `ITGAX`, `CSF1R`, `VCAN`, and `C1QB`.

Supported interpretation:

- This component is a mixed monocyte/macrophage bridge rather than a clean cell type.
- Several source records explicitly use combinations of `CD14`, `FCGR3A`, `CD68`, and `CD163` to distinguish or annotate myeloid populations.
- The component includes cases where the same label, especially macrophage, is supported by different marker programs.

Representative source evidence:

- A head-and-neck cancer atlas says `CD14` and `FCGR3A` separated monocytes and macrophages within the myeloid group.
- A COVID-19 nasopharyngeal atlas reports macrophages marked by `CD14`, `FCGR3A`, and `VCAN`.
- A dermal macrophage study reports `CD14`, `CD68`, and `CD163` as macrophage markers.
- A dental pulp study reports `CD163`, `CSF1R`, and `CD14` as identifying monocyte cell lineage.

## Recommendation

Use the TREG/exhaustion example as the main figure example only if the figure and text make clear that this is a TREG-containing suppressive/exhaustion program. It is the more compelling biology-first example because it directly touches cell type versus cell state.

Use the myeloid result as the more conservative validation. It shows that the same framework separates well-established inflammatory monocyte-like and complement/macrophage-like programs, even when labels overlap across papers.

Avoid saying that the analysis has resolved a stable taxonomy. The safer claim is that marker profiles create source-linked neighborhoods that nominate where labels behave like canonical cell-type labels and where they behave like context- or state-associated programs.
