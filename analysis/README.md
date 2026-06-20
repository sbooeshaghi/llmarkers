# Analysis

This directory contains the active analysis code, generated artifacts, figures, formal Lean model, and data-processing scripts.

## Layout

- `figures/`: generated manuscript and analysis figures.
- `artifacts/`: generated TSV, Markdown, and table artifacts.
- `formal/`: Lean formalization for marker identifiability.
- `*.py`: figure, table, report, data-ingestion, and database generation scripts.
- `*.sh`: helper shell entry points.
- `*.ipynb`: exploratory notebooks retained for provenance.

Run Python scripts from the repository root so paths such as `analysis/artifacts/` and `docs/paper/biorxiv/src/` resolve as written. The notebooks were authored inside this directory and use notebook-local paths such as `figures/...`; run them with `analysis/` as the working directory if regenerating notebook-only artifacts.
