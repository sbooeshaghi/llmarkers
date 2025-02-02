# Methods

## Summary

## Human Extraction

### Text
Given an scRNA-seq research paper, human readers can extract marker gene information by identifying the segment of text in which a cell type, its corresponding marker gene, and a potential state the cell is in when expressing this gene is mentioned. The human reader then populates the JSON data manually, placing the segment of text in the source_rationale field of the source object, the cell type in cell_type_label in both the derived and extracted objects, cell state in cell_state in the derived and extracted objects, and the marker gene in gene in derived and extracted objects. Other fields such as organism and cell_source are populated based on the article information. For example, if the user were to be reading an article discussing marker genes within White Adipose Tissue in humans, the organism is homo_sapiens and cell_source is White Adipose Tissue. For evidence extracted from quotes in the paper, the fields source_id and source_type are both populated with the string "text". 

#### Example

##### Quote from Text: "We identified six distinct subpopulations of human ASPCs (see Supplementary Note 1) in subclustered scRNA-seq and sNuc-seq samples, all of which express the common marker gene PDGFRA (Extended Data Fig. 7a, b)."

##### Corresponding JSON Object in evidence_human/evidence.json:

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

#### Example

##### JSON Object in evidence_human/evidence.json:

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
The evidence the human extracts are placed as a list of JSON objects within a file evidence_human/evidence.json. The below JSON object describes the typical structure of how a piece of evidence can be structured into JSON format. 

#### JSON Object Template:

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
Accompanied with scRNA-seq papers are supplementary tables which list differentially expressed genes (DEGs) identified within the file. On top of DEGs, the columns identify accompanying features including the p value, log fold change, rank. 

Once downloading the supplementary tables files, it is essential to run them through the [gfix](https://github.com/sbooeshaghi/gfix) command, producing a clean_degs.xlsx. This command line tool fixes Excel-converted gene names in spreadsheets. "Excel automatically converts some gene names (like MARCH1, SEPT2) to dates - this tool converts them back."

What differentiates DEGs from cell marker genes is the filtering performed on the cleaned up DEGs. Using the p value, log fold change, and rank, which corresponds to column names "p_val_adj", "avg_log2FC", and "pct.1", respectively, we cut down the DEGs to solely genes that are expressed the most compared to other genes for a given cell type and have an expression value that is greater than a certain threshold. With this filtering, we can ensure that we are extracting soleley marker genes from the supplementary tables. 

#### Example Filtering Code:

col_pval = "p_val_adj"\
col_lfc = "avg_log2FC"\
col_gene = "gene"\
col_ct = "cell_type_label"\
col_rank = "pct.1"\
min_mean = 100\
max_pval = 1e-10\
min_lfc = 0.7\
max_gene_shares = 4\
max_per_celltype = 20

##### filter by pval and lfc
dfc = df.query(f"{col_pval} <= {max_pval} & {col_lfc} >= {min_lfc}")

##### mask out genes that are shared between max_gene_shares cell types
non_repeat_genes = dfc[col_gene].value_counts()[dfc[col_gene].value_counts() < max_gene_shares].index.values

if col_rank:
    m = dfc[dfc[col_gene].isin(non_repeat_genes)].sort_values(col_rank, ascending = True)
else:
    m = dfc[dfc[col_gene].isin(non_repeat_genes)]

##### max number to sample is equal to the min number of genes across all celltype
n_sample = min(m[col_ct].value_counts().max(), max_per_celltype)

##### sample n_sample genes
markers = m.groupby(col_ct).tail(n_sample)
markers_dict = markers.groupby(col_ct)[col_gene].apply(lambda x: list(x)).to_dict()

After finding the markers, listed in a Pandas Dataframe format, we then save the extracted evidence from DEG files into a JSON file named evidence.json.

#### Example Code: 

df = markers[[col_ct, col_gene]].rename(columns={col_ct : "cell_type_label", col_gene: "gene"})\
df["organism"] = organism\
df["cell_source"] = cell_source\
df["cell_state"] = cell_state\
df["gene_id"] = df["gene"]\
df["gene_id"] = df["gene_id"].apply(run)\
save = df.to_dict(orient = "records")\
with open("evidence.json", "w") as f:\
    &emsp;json.dump(save, f, indent = 4)

By filtering and comparing to evidence_human/evidence.json, we can determine whether or not paper authors correctly described/mentioned marker genes within the paper itself. If filtering resulted in genes appearing in evidence_human/evidence.json but not evidence_deg/evidence.json, this suggests authors described genes as if they were markers for cells within the paper, but their experimental results suggest otherwise. 

### Data Format
JSON Object Format:

{\
        "cell_type_label": "{name of cell type as mentioned in figure or text in which cell was found, eg: adipocyte}",\
        "gene": "{marker gene corresponding to cell type}",\
        "organism": "{organism in which cell type is found, eg: homo_sapiens, mus_musculus, etc}",\
        "cell_source": "{tissue in which the cell type was found in, eg: adipose tissue}",\
        "cell_state": {if the figure or text suggests the cell was in a specific state while expressing the marker gene, place it here (null otherwise), eg: obesity, null},\
        "gene_id": "{Ensembl ID for marker gene, populated using a Python script that maps gene names to Ensembl IDs using a GTF file}"\
}

## LLM Extraction
