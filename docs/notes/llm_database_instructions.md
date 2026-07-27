# LLMarkers SQLite guide

`llmarkers.sqlite` is a browser-ready copy of the normalized database built
from validated `mrkr.onto.v1` records. The validated `.onto` files are the
durable source artifacts; SQLite is a derived representation.

## Download

- Repository: https://github.com/sbooeshaghi/llmarkers/blob/main/docs/llmarkers.sqlite
- Direct download: https://raw.githubusercontent.com/sbooeshaghi/llmarkers/main/docs/llmarkers.sqlite

Open the file with any SQLite client. The database schema is
`llmarkers.claim-db.v3`; the browser additions are `llmarkers.web-db.v1`.

## Data model

- `papers`: one validated `.onto` document per paper
- `paper_metadata`: title, DOI when available, source URL, and manuscript path
- `claims`: one source-grounded marker statement
- `terms`: normalized genes, cell types, comparisons, tissues, and organisms
- `profiles`: one paper and normalized target-cell-type marker panel
- `profile_claims`: claims assigned to each marker panel
- `ontology_terms`, `term_labels`, `term_closure`: stable identifiers and the
  available ontology closure
- `cell_ontology_label_audit`: canonical-label and exact-synonym verification
  against the pinned Cell Ontology release used by the corpus analysis
- `claim_context`: browser-ready comparison and tissue term arrays

Two views cover common use cases:

- `web_marker_evidence`: one cell type-gene row with paper metadata, stable
  identifiers, marker direction, comparison groups, tissues, normalized text,
  and exact source text
- `profile_markers`: distinct marker genes for each paper-cell-type panel

One marker statement can name several genes. It therefore appears as several
rows in `web_marker_evidence`, all with the same `claim_key`.

## Grounding fields

Each core term has a `normalized_label`, an optional `ontology_term`, and an
`exact` value. For Cell Ontology and UBERON terms, core `exact` records whether
the OLS tagger covered the full query text. It does not by itself establish that
the label is a canonical ontology label or synonym.

The browser view therefore adds stricter fields for target cell types:

- `target_curie`: an ID accepted by the Cell Ontology label audit
- `target_candidate_curie`: the original OLS candidate, retained for audit
- `target_semantic_exact`: `1` only for a canonical label or exact synonym
- `target_match_source`: `canonical` or `exact_synonym` for accepted IDs

Use `target_curie`, not `target_candidate_curie`, when connecting cell type
labels across papers.

The language model produces source text and normalized labels. It does not
produce identifiers. Validation, identifier grounding, and Cell Ontology label
verification are separate, deterministic steps.

## Example queries

Find papers that report `CD3D` as a marker:

```sql
SELECT title, target_label, target_curie, direction, span_literal, source_url
FROM web_marker_evidence
WHERE upper(gene_symbol) = 'CD3D';
```

Find marker evidence grounded to macrophage (`CL:0000235`):

```sql
SELECT title, gene_symbol, gene_curie, span_literal
FROM web_marker_evidence
WHERE target_curie = 'CL:0000235';
```

Find claims that explicitly name monocytes as a comparison group:

```sql
SELECT DISTINCT p.title, c.summary, c.span_literal
FROM terms t
JOIN claims c ON c.claim_key = t.claim_key
JOIN papers paper ON paper.paper_key = c.paper_key
JOIN paper_metadata p ON p.paper_key = paper.paper_key
WHERE t.term_type = 'comparison'
  AND lower(t.normalized_label) = 'monocyte';
```

Find marker statements that do not report a comparison group:

```sql
SELECT p.title, c.summary, c.span_literal
FROM claims c
JOIN paper_metadata p ON p.paper_key = c.paper_key
WHERE NOT EXISTS (
  SELECT 1
  FROM terms t
  WHERE t.claim_key = c.claim_key
    AND t.term_type = 'comparison'
);
```

List the marker panel for each target in a paper:

```sql
SELECT p.paper_key, p.target_label, p.target_curie,
       group_concat(pm.gene_symbol, ', ') AS marker_genes
FROM profiles p
JOIN profile_markers pm ON pm.profile_key = p.profile_key
GROUP BY p.profile_key
ORDER BY p.paper_key, p.target_label;
```

## Provenance boundary

`span_literal` is copied exactly from the source paper. `summary` is the
normalized marker statement. Use both when evaluating a record. Stable IDs
connect labels across papers, but they do not reconstruct comparison groups
that authors did not report.
