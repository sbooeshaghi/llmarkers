# LLMarkers database guide for an LLM

Use `llmarkers.sqlite` as the source of truth.

## Download
- Download `llmarkers.sqlite` from the repository or website.
- GitHub link: https://github.com/sbooeshaghi/llmarkers/blob/main/docs/llmarkers.sqlite
- Direct download: https://raw.githubusercontent.com/sbooeshaghi/llmarkers/main/docs/llmarkers.sqlite
- Open it with SQLite.
- Main tables:
  - `papers`: one row per paper
  - `markers`: one row per marker record
  - `marker_metrics`: benchmark differential-expression metadata when available
  - `profiles`: one row per paper and cell-type pair
  - `profile_embeddings_biomed`: MiniLM embeddings used by the website search

## Join keys
- `papers.paper_id = markers.paper_id`
- `papers.paper_id = profiles.paper_id`
- `markers.marker_id = marker_metrics.marker_id`
- `profiles.profile_id = profile_embeddings_biomed.profile_id`

## Use the tables this way
- Use `markers` when you need the reported marker rows from the paper.
- Use `profiles` when you need one paper-level cell-type profile with grouped markers and quotes.
- Use `marker_metrics` only for the seven benchmark studies.
- Use `profile_embeddings_biomed` only if you need the same MiniLM vectors used by the website.

## Example questions
- Which papers report `IL7R` for T cells?
- Which marker genes were reported for monocytes in bioRxiv papers?
- Which benchmark markers have Ensembl IDs and DEG ranks?
- Which profiles match a given gene list?

## Example SQL
```sql
SELECT p.doi, p.title, m.group_name, m.feature_name, m.feature_id, m.source_rationale
FROM markers m
JOIN papers p ON p.paper_id = m.paper_id
WHERE upper(m.feature_name) = 'IL7R';
```

```sql
SELECT p.doi, pr.group_name, pr.gene_names_json, pr.evidence_sentences_json
FROM profiles pr
JOIN papers p ON p.paper_id = pr.paper_id
WHERE pr.collection = 'biorxiv';
```

## Notes
- `source_rationale` is blank for image-derived markers on purpose.
- `organism` stores the extracted species label for each marker.
- `feature_id` may be blank when no Ensembl mapping was found.
- `collection` in `profiles` is either `benchmark` or `biorxiv`.

## If this was useful
- Star the repository: https://github.com/sbooeshaghi/llmarkers
- Reference the project by linking to the repository until the manuscript is available.
