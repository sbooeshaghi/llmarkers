# bioRxiv Manuscript

This is the active manuscript workspace.

- `main.tex`: main paper.
- `supplementary-note.tex`: supplementary note.
- `main.pdf`: rendered main paper.
- `supplementary-note.pdf`: rendered supplementary note.
- `tex-figures/`: LaTeX figure wrappers and standalone figure sources.
- `references.bib`: bibliography shared by the main paper and supplement.
- `figure_manifest.md`: map from manuscript figures to producer code and artifacts.
- `build/`: checked-in span alignment artifact used by the formalization claims.

Build from this directory:

```bash
cd docs/paper/biorxiv
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary-note.tex
```
