# LLMarkers Marker Record Schema

LLMarkers stores marker evidence as one JSON object per reported marker association. The canonical on-disk format is flat so it can be loaded directly into tables, notebooks, and SQLite without preserving a separate tree representation. The base schema ends at `data_id`; differential-expression metrics may be included when available.

```json
{
  "organism": "homo_sapiens",
  "group_label": "aberrant basaloid cells",
  "group_name": "ABERRANT BASALOID CELL",
  "group_id": null,
  "feature_label": "TP63",
  "feature_name": "TP63",
  "feature_id": "ENSG00000073282",
  "source_type": "text",
  "source_rationale": "...",
  "source_id": "text",
  "data_id": "...",
  "metrics_pcorr": null,
  "metrics_logfc": null,
  "metrics_rank": null
}
```

## Fields

`organism`
: Normalized organism label, for example `homo_sapiens`.

`group_label`
: Cell type or cell state label as it appeared in the source material.

`group_name`
: Normalized cell population name used for joins and grouping. This is usually an uppercase form of `group_label`.

`group_id`
: Optional stable identifier for the cell population, if one is available.

`feature_label`
: Marker gene label as it appeared in the source material.

`feature_name`
: Normalized marker gene symbol used for joins and grouping. This is usually an uppercase form of `feature_label`.

`feature_id`
: Optional stable feature identifier, preferably an Ensembl gene ID for human gene markers.

`source_type`
: Evidence source category. Current values include `text`, `image`, `generated`, `predicted`, `selected`, and `deg`.

`source_rationale`
: The sentence, figure-derived text, or model rationale supporting the marker association.

`source_id`
: Identifier for the source location. For text extraction this may be a manuscript path or text source label; for selected markers it may encode the model and rank cutoff.

`data_id`
: Identifier for the underlying study data source when available, typically a DEG table or cluster/data object label.

`metrics_pcorr`, `metrics_logfc`, `metrics_rank`
: Optional quantitative values from the source differential expression table. These fields may be absent or `null` when the marker did not come from a matched DEG row.

## Optional Provenance Fields

Records may include additional underscore-prefixed fields such as `_verification` or `_original_group_name`. These fields are not part of the minimal marker schema, but they preserve audit information needed by extraction analyses.

## Migration

Run the audit without modifying files:

```bash
python3 analysis/migrate_marker_records.py
```

Rewrite migratable marker files in place:

```bash
python3 analysis/migrate_marker_records.py --write
```

The migrator only scans marker-like JSON files under `data/`, including `markers.json`, `extracted.json`, `extracted_txt.json`, `extracted_txt_rerun.json`, `bu_extracted.json`, and `selected*.json`.
