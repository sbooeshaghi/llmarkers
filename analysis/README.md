# Analysis

This directory contains the code and outputs required by the current
manuscript.

## Layout

- `figures/`: generated manuscript figure panels.
- `artifacts/`: generated result tables, reports, and validated corpus files.
- `formal/`: Lean formalization for marker identifiability.
- `*.py`: benchmark, corpus, CAP, figure, and data-ingestion scripts.
- `*.sh`: helper shell entry points.
- `*.ipynb`: benchmark notebooks cited by the manuscript.

The active figure and result dependencies are listed in
`docs/paper/biorxiv/figure_manifest.md`. Run Python scripts from the repository
root so paths such as `analysis/artifacts/` and `docs/paper/biorxiv/` resolve as
written. Run the notebooks with `analysis/` as the working directory.

`build_website_db.py` is the active builder for `docs/llmarkers.sqlite`. It
derives the browser database from the normalized claim database and the pinned
Cell Ontology label audit used by the corpus analysis.

Exploratory analyses and superseded manuscript pipelines are kept outside the
versioned tree under the local `archive/` directory.
