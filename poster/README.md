# LLMarkers Poster

This folder contains a standalone LaTeX poster draft for the conference poster.

## Files

- `main.tex`: 36 in x 48 in portrait poster scaffold.
- `corpus_references.tex`: multi-column appendix listing the extracted bioRxiv and HCA corpus references.
- `corpus_references.bib`: generated BibTeX reference artifact for the extracted corpus.
- `scripts/build_corpus_references.py`: generates the corpus reference table from local metadata and manuscript files.
- `tables/corpus_references.tsv`: generated tabular reference metadata.
- `tables/corpus_references_body.tex`: generated LaTeX body used by `corpus_references.tex`.
- `tables/corpus_references_poster.tex`: generated compact native-LaTeX reference strip used at the bottom of `main.tex`.
- `tables/immune_celltype_prompt.tex`: editable interactive table for attendee annotations.
- `tables/immune_celltype_prompt_mapping.tsv`: internal mapping from poster prompt labels to atlas label classes for post-conference analysis.
- `Makefile`: builds the poster with `latexmk`.

The poster references figures directly from `../analysis/figures/` to avoid duplicating assets.

## Build

```bash
cd poster
make
```

The outputs are `poster/main.pdf` and `poster/corpus_references.pdf`.

To rebuild only the corpus reference metadata:

```bash
cd poster
make corpus-references-data
```

## Design Notes

The current layout has two vertical sections:

- Top section: three-column scientific narrative with motivation, LLMarkers/expert curation, LLM marker curation, and cross-study unification.
- Bottom section: full-width interactive annotation table for expert synonyms and marker genes.

The interactive table is intentionally easy to edit. Add or remove cell type labels in `tables/immune_celltype_prompt.tex` as the design settles, and update `tables/immune_celltype_prompt_mapping.tsv` when prompt labels should be mapped back to exact atlas labels, broader buckets, or expert-only prompts.
