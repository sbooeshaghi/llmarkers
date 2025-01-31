# Methods

## Summary

## Human Extraction

### Text
Given an scRNA-seq research paper, human readers can extract marker gene information by identifying the segment of text in which a cell type, its corresponding marker gene, and a potential state the cell is in when expressing this gene is mentioned. The human reader then populates the JSON data manually, placing the segment of text in the source_rationale field of the source object, the cell type in cell_type_label in both the derived and extracted objects, cell state in cell_state in the derived and extracted objects, and the marker gene in gene in derived and extracted objects. Other fields such as organism and cell_source are populated based on the article information. For example, if the user were to be reading an article discussing marker genes within White Adipose Tissue in humans, the organism is homo_sapiens and cell_source is White Adipose Tissue. For evidence extracted from quotes in the paper, the fields source_id and source_type are both populated with the string "text". 

Example

Quote from Text: "We identified six distinct subpopulations of human ASPCs (see Supplementary Note 1) in subclustered scRNA-seq and sNuc-seq samples, all of which express the common marker gene PDGFRA (Extended Data Fig. 7a, b)."

Corresponding JSON Object in evidence_human.json: 
{
    "extracted": {
      "organism": "homo_sapiens",
      "cell_type_label": "human ASPCs",
      "cell_source": "adipose",
      "cell_state": "None",
      "gene": "PDGFRA"
    },
    "derived": {
      "organism": "homo_sapiens",
      "cell_type_id": null,
      "cell_type_label": "human ASPCs",
      "cell_source": "adipose",
      "cell_state": "None",
      "gene": "PDGFRA",
      "gene_id": "ENSG00000134853"
    },
    "source": {
      "source_id": "text",
      "source_type": "text",
      "source_rationale": "We identified six distinct subpopulations of human ASPCs (see Supplementary Note 1) in subclustered scRNA-seq and sNuc-seq samples, all of which express the common marker gene PDGFRA (Extended Data Fig. 7a, b)."
    }
}

### Figure
Given an scRNA-seq research paper, human readers can extract marker gene information by identifying markers displayed within figures provided in the Extended Figures or Figures section of the paper. Some common figures within papers that usually display cell types and corresponding marker genes are Pearson Correlation heatmaps, violin plots, and dot plots. The human reader then populates the JSON data manually, placing the the cell type in cell_type_label in both the derived and extracted objects and the marker gene in gene in derived and extracted objects. Other fields such as organism and cell_source are populated based on the article information. For example, if the user were to be reading an article discussing marker genes within White Adipose Tissue in humans, the organism is homo_sapiens and cell_source is White Adipose Tissue. For evidence extracted from figures in the paper, the field source_id is populated by the figure name, source_type is populated with "img", and source_rationale is populated with a sentence describing why the reader believes the figure shows this marker gene. 

Example

JSON Object in evidence_human.json:
{
        "extracted": {
            "organism": "homo_sapiens",
            "cell_type_label": "Macrophage",
            "cell_source": "bone",
            "cell_state": "8WPC Neural Crest",
            "gene": "RUNX2"
        },
        "derived": {
            "organism": "homo_sapiens",
            "cell_type_id": null,
            "cell_type_label": "Macrophage",
            "cell_source": "bone",
            "cell_state": "8WPC Neural Crest",
            "gene": "RUNX2",
            "gene_id": "ENSG00000124813"
        },
        "source": {
            "source_type": "img",
            "source_rationale": "marker shows sign of expression in figure",
            "source_id": "Fig. 6b"
        }
}

### Data Format
The evidence the human extracts are placed as a list of JSON objects within a file named evidence_human.json. The below JSON object describes the typical structure of how a piece of evidence can be structured into JSON format. 

JSON Object Template:
{
        "extracted": {
            "organism": "{organism in which cell type is found, eg: homo_sapiens, mus_musculus, etc}",
            "cell_type_label": "{name of cell type as mentioned in figure or text in which cell was found, eg: adipocyte}",
            "cell_source": "{tissue in which the cell type was found in, eg: adipose tissue}",
            "cell_state": "{if the figure or text suggests the cell was in a specific state while expressing the marker gene, place it here (null otherwise), eg: obesity, null}",
            "gene": "{marker gene corresponding to cell type}"
        },
        "derived": {
            "organism": "{organism in which cell type is found, eg: homo_sapiens, mus_musculus, etc}",
            "cell_type_id": {ID corresponding to cell type, derived using a mapping file that maps distinct cell type labels under specific categories},
            "cell_type_label": "{name of cell type as mentioned in figure or text in which cell was found, eg: adipocyte}",
            "cell_source": "{tissue in which the cell type was found in, eg: adipose tissue}",
            "cell_state": "{if the figure or text suggests the cell was in a specific state while expressing the marker gene, place it here (null otherwise), eg: obesity, null}",
            "gene": "{marker gene corresponding to cell type}",
            "gene_id": {Ensembl ID for marker gene, populated using a Python script that maps gene names to Ensembl IDs using a GTF file}
        },
        "source": {
            "source_type": "{img or text}",
            "source_rationale": "{quote derived from text or reasoning for why human reader believes gene is a marker based on the figure}",
            "source_id": "{figure number or text}"
        }
}

## Deg Extraction

link to specific easy table
- column names choosing
- unfiltered vs filtered (criterion)
- running gfix command (importance)
- add code when necessary
- link to notebooks that do the processing (future)

### Data Format
- include an example of an element from JSON file (what are the keys)
- how evidence_deg.json is also structured 

## LLM Extraction
