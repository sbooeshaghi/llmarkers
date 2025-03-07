Link to CZI DEG file posted by Max Lombardo to the CZI Slack on the 10th of January 2025 at 7:49AM.

link: https://cziscience.slack.com/archives/C8ME9JMBP/p1736524183863259?thread_ts=1715805283.863299&cid=C8ME9JMBP

```quote
hi 
@Nick Semenkovich
 - you can access a static snapshot of marker genes from cellxgene at this link (it was generated around Q2/Q3 of 2024):
https://cellguide.cellxgene.cziscience.com/1716401368/computational_marker_genes/marker_gene_data.json.gz
```

```bash
zcat marker_gene_data.json.gz | jq -r '
  # Print the header row first
  "species\ttissue\tcelltype_id\tgene\tmarker_score\tme\tpc",
  # Process the JSON structure
  keys_unsorted[] as $species |
  .[$species] | keys_unsorted[] as $tissue |
  .[$tissue] | keys_unsorted[] as $celltype |
  .[$celltype][] |
  [$species, $tissue, $celltype, .gene, .marker_score, .me, .pc] |
  @tsv
' | gzip > czi_degs.txt.gz
```
