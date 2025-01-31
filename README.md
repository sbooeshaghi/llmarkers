# Methods

## Summary

## Human Extraction

### Text
Given an scRNA-seq research paper, human readers can extract marker gene information by identifying the segment of text in which a cell type, its corresponding marker gene, and a potential state the cell is in when expressing this gene is mentioned. The human reader then populates the JSON data manually, placing the segment of text in the source_rationale field of the source object, the cell type in cell_type_label in both the derived and extracted objects, cell state in cell_state in the derived and extracted objects, and the marker gene in gene in derived and extracted objects. Other fields such as organism and cell_source are populated based on the article information. For example, if the user were to be reading an article discussing marker genes within White Adipose Tissue in humans, the organism is homo_sapiens and cell_source is White Adipose Tissue. For evidence extracted from quotes in the paper, the fields source_id and source_type are both populated with the string "text". 

Example

Quote from Text: "We identified six distinct subpopulations of human ASPCs (see Supplementary Note 1) in subclustered scRNA-seq and sNuc-seq samples, all of which express the common marker gene PDGFRA (Extended Data Fig. 7a, b)."

Corresponding JSON Object in evidence_human.json:

{\
    &emsp;"extracted": {\
      &emsp;&emsp;"organism": "homo_sapiens",\
      &emsp;&emsp;"cell_type_label": "human ASPCs",\
      &emsp;&emsp;"cell_source": "adipose",\
      &emsp;&emsp;"cell_state": "None",\
      &emsp;&emsp;"gene": "PDGFRA"\
    &emsp;},\
    &emsp;"derived": {\
      &emsp;&emsp;"organism": "homo_sapiens",\
      &emsp;&emsp;"cell_type_id": null,\
      &emsp;&emsp;"cell_type_label": "human ASPCs",\
      &emsp;&emsp;"cell_source": "adipose",\
      &emsp;&emsp;"cell_state": "None",\
      &emsp;&emsp;"gene": "PDGFRA",\
      &emsp;&emsp;"gene_id": "ENSG00000134853"\
    &emsp;},\
    &emsp;"source": {\
      &emsp;&emsp;"source_id": "text",\
      &emsp;&emsp;"source_type": "text",\
      &emsp;&emsp;"source_rationale": "We identified six distinct subpopulations of human ASPCs (see Supplementary Note 1) in subclustered scRNA-seq and sNuc-seq samples, all of which express the common marker gene PDGFRA (Extended Data Fig. 7a, b)."\
    &emsp;}\
}

### Figure
Given an scRNA-seq research paper, human readers can extract marker gene information by identifying markers displayed within figures provided in the Extended Figures or Figures section of the paper. Some common figures within papers that usually display cell types and corresponding marker genes are Pearson Correlation heatmaps, violin plots, and dot plots. The human reader then populates the JSON data manually, placing the the cell type in cell_type_label in both the derived and extracted objects and the marker gene in gene in derived and extracted objects. Other fields such as organism and cell_source are populated based on the article information. For example, if the user were to be reading an article discussing marker genes within White Adipose Tissue in humans, the organism is homo_sapiens and cell_source is White Adipose Tissue. For evidence extracted from figures in the paper, the field source_id is populated by the figure name, source_type is populated with "img", and source_rationale is populated with a sentence describing why the reader believes the figure shows this marker gene. 

Example

JSON Object in evidence_human.json:

{\
        &emsp;"extracted": {\
            &emsp;&emsp;"organism": "homo_sapiens",\
            &emsp;&emsp;"cell_type_label": "Macrophage",\
            &emsp;&emsp;"cell_source": "bone",\
            &emsp;&emsp;"cell_state": "8WPC Neural Crest",\
            &emsp;&emsp;"gene": "RUNX2"\
        &emsp;},\
        &emsp;"derived": {\
            &emsp;&emsp;"organism": "homo_sapiens",\
            &emsp;&emsp;"cell_type_id": null,\
            &emsp;&emsp;"cell_type_label": "Macrophage",\
            &emsp;&emsp;"cell_source": "bone",\
            &emsp;&emsp;"cell_state": "8WPC Neural Crest",\
            &emsp;&emsp;"gene": "RUNX2",\
            &emsp;&emsp;"gene_id": "ENSG00000124813"\
        &emsp;},\
        &emsp;"source": {\
            &emsp;&emsp;"source_type": "img",\
            &emsp;&emsp;"source_rationale": "marker shows sign of expression in figure",\
            &emsp;&emsp;"source_id": "Fig. 6b"\
        &emsp;}\
}

### Data Format
The evidence the human extracts are placed as a list of JSON objects within a file named evidence_human.json. The below JSON object describes the typical structure of how a piece of evidence can be structured into JSON format. 

JSON Object Template:

{\
        &emsp;"extracted": {\
            &emsp;&emsp;"organism": "{organism in which cell type is found, eg: homo_sapiens, mus_musculus, etc}",\
            &emsp;&emsp;"cell_type_label": "{name of cell type as mentioned in figure or text in which cell was found, eg: adipocyte}",\
            &emsp;&emsp;"cell_source": "{tissue in which the cell type was found in, eg: adipose tissue}",\
            &emsp;&emsp;"cell_state": "{if the figure or text suggests the cell was in a specific state while expressing the marker gene, place it here (null otherwise), eg: obesity, null}",\
            &emsp;&emsp;"gene": "{marker gene corresponding to cell type}"\
        &emsp;},\
        &emsp;"derived": {\
            &emsp;&emsp;"organism": "{organism in which cell type is found, eg: homo_sapiens, mus_musculus, etc}",\
            &emsp;&emsp;"cell_type_id": {ID corresponding to cell type, derived using a mapping file that maps distinct cell type labels under specific categories},\
            &emsp;&emsp;"cell_type_label": "{name of cell type as mentioned in figure or text in which cell was found, eg: adipocyte}",\
            &emsp;&emsp;"cell_source": "{tissue in which the cell type was found in, eg: adipose tissue}",\
            &emsp;&emsp;"cell_state": "{if the figure or text suggests the cell was in a specific state while expressing the marker gene, place it here (null otherwise), eg: obesity, null}",\
            &emsp;&emsp;"gene": "{marker gene corresponding to cell type}",\
            &emsp;&emsp;"gene_id": {Ensembl ID for marker gene, populated using a Python script that maps gene names to Ensembl IDs using a GTF file}\
        &emsp;},\
        &emsp;"source": {\
            &emsp;&emsp;"source_type": "{img or text}",\
            &emsp;&emsp;"source_rationale": "{quote derived from text or reasoning for why human reader believes gene is a marker based on the figure}",\
            &emsp;&emsp;"source_id": "{figure number or text}"\
        &emsp;}\
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
