# Benchmark evidence schema

The seven LLMarkers benchmark studies contain three different evidence classes. They are stored
separately because they make different assertions.

- **Text claims** are marker associations curated from manuscript prose.
- **Image claims** are marker associations curated from figures.
- **DEG profiles** are unfiltered quantitative feature tables. A DEG row is supporting evidence,
  not by itself a reported marker claim.

The derived documents use the term-centered structure introduced by `mrkr`: one organism term, one
target cell-type term, and one or more gene terms. Text and image documents contain `claims`; DEG
documents contain `profiles`. Each gene term has a `source_records` list of immutable IDs and source
indices. Exact duplicate rows therefore remain distinct in provenance without repeating the same
gene in a marker panel.

Text evidence records an exact manuscript offset when the curated rationale occurs exactly once.
An unanchored rationale is retained with `anchor_status: "unanchored"`; it is not silently changed
or discarded. Image evidence retains its figure identifier and curator description. DEG evidence
retains corrected p-value, log fold change, and rank for every row.

The original `data/*/evidence_human/extracted.json` and `data/*/evidence_deg/extracted.json` files
remain immutable sources. Build the derived representation with:

```bash
uv run python analysis/build_benchmark_evidence.py \
  --manifest analysis/benchmark_evidence_sources.tsv \
  --output-dir analysis/artifacts/benchmark_evidence_v1
```

`reconciliation.json` is written last. A successful report guarantees that every legacy row was
represented exactly once, that flattening the derived documents reproduces every source record
exactly, and that no source file changed during the build. `review.tsv` lists non-exact text anchors,
gene labels absent from their curated text span, exact duplicate rows, and source files containing
more than one organism. These are review warnings; the builder preserves the underlying annotations
without guessing a correction or silently filtering records. Legacy human-curated marker records
are represented as positive associations with `direction_basis: "curated_marker_association"`.
