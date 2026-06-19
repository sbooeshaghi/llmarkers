# Analysis

This directory contains the active analysis code, result tables, generated figures, formal Lean model, and data-processing scripts.

## Layout

- `figures/`: generated manuscript and analysis figures.
- `results/`: generated TSV/Markdown result artifacts.
- `scripts/`: data and database preparation entry points.
- `formal/`: Lean formalization for marker identifiability.
- `*.py`: figure, table, and report generation scripts.
- `*.ipynb`: exploratory notebooks retained for provenance.

Run Python scripts from the repository root so paths such as `analysis/results/` and `docs/paper/src/` resolve as written. The notebooks were authored inside this directory and use notebook-local paths such as `figures/...`; run them with `analysis/` as the working directory if regenerating notebook-only artifacts.
