#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STANDALONE_DIR="$ROOT_DIR/docs/paper/biorxiv/tex-figures/standalone"
BUILD_DIR="$STANDALONE_DIR/build"

cd "$ROOT_DIR"
mkdir -p "$BUILD_DIR"

figures=(
  fig1_paper_celltype_joint
  fig2_marker_recovery
  fig3_cross_study_unification
  figs1_hildreth_detail
)

for figure in "${figures[@]}"; do
  latexmk \
    -pdf \
    -halt-on-error \
    -interaction=nonstopmode \
    -file-line-error \
    -outdir="$BUILD_DIR" \
    -auxdir="$BUILD_DIR" \
    "$STANDALONE_DIR/$figure.tex"
done

printf 'Standalone figure PDFs written to %s\n' "$BUILD_DIR"
