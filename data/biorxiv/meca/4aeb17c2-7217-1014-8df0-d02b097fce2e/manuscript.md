# easybio: an R Package for Single-Cell Annotation with CellMarker2.0

## Authors

- Wei Cui<sup>1</sup> ([ORCID: 0009-0004-8315-5899](https://orcid.org/0009-0004-8315-5899)) †

### Affiliations

1. 

† Corresponding author

## Abstract

Abstract
Single-cell RNA sequencing (scRNA-seq) allows researchers to study biological activities at the cellular level, enabling the discovery of new cell types and the analysis of intercellular interactions. However, annotating cell types in scRNA-seq data is a crucial and time-consuming process, with its quality significantly influencing downstream analyses. Accurate identification of potential cell types provides valuable insights for discovering new cell populations or identifying novel markers for known cells, which may be utilized in future research. While various methods exist for single-cell annotation, one of the most common approaches is to use known cell markers. The CellMarker2.0 database, a human-curated repository of cell markers extracted from published articles, is widely used for this purpose. However, it currently offers only a web-based tool for usage, which can be inconvenient when integrating with workflows like Seurat. To address this limitation, we introduce easybio, an R package designed to streamline single-cell annotation using the CellMarker2.0 database in conjunction with Seurat. easybio provides a suite of functions for querying the CellMarker2.0 database locally, offering insights into potential cell types for each cluster. In addition to single-cell annotation, the package also supports various bioinformatics workflows, including RNA-seq analysis, making it a versatile tool for transcriptomic research.

## Introduction

Accurately identifying the specific cell types in single-cell data is critical for many downstream analyses. Numerous methods have been developed for single-cell annotation.

Recent research has evaluated the annotation accuracy of several methods, including GPT-4, SingleR, and CellMarker2.0 [1]. The SingleR method [2], a supervised approach, relies on reference datasets for accuracy and can be time-consuming. scType [3] integrates databases like PanglaoDB [4] and the original CellMarker database [5] to annotate single cells using both positive and negative markers. However, CellMarker has been updated to version 2.0 [6], which incorporates new marker resources and is manually curated for human and mouse cell types.

While direct use of CellMarker2.0 may not always achieve the highest annotation accuracy, it offers broad applicability across diverse datasets and provides more interpretable results. However, its functionality has so far been limited to an online user interface, with no software implementation available [1].

To address this, we introduce the R package easybio [7], designed to provide convenient access to the CellMarker2.0 database for marker querying and streamlined single-cell annotation.

## R package easybio

### Query Markers in the CellMarker2.0 Database

One of the key features of the CellMarker2.0 database [6] is its ability to search for markers based on the top differentially expressed genes in each cluster, helping to determine the potential cell type for each cluster. The package also includes functions that allow users to retrieve markers along with information about their corresponding tissues, as reported in published studies. The package also supports retrieving markers directly for specific cell types.

![Figure 1:](content/609619v1_fig1.tif)

**Figure 1::** Using the R package easybio, a query for CD68 in CellMarker2.0 illustrates the distribution of this marker across different tissues and cell types

### Annotate Single-Cell Clusters with CellMarker2.0

Annotating cell clusters is a crucial step in single-cell RNA-seq analysis, helping to assign biological identities to each group of cells. Typically, this process involves comparing the differentially expressed genes (DEGs) between clusters and identifying the most enriched genes within a cluster. These enriched genes serve as markers that can be used to determine the potential cell types within each cluster.

The CellMarker2.0 database is a valuable resource for this purpose, as it provides a curated collection of cell-type markers derived from published studies. While the web-based tool allows researchers to manually search for markers by pasting gene lists, this approach can be time-consuming and may require matching one cluster at a time. For large datasets, this manual process can introduce inefficiencies and limit the speed of analysis.

To overcome these limitations, our package automates the process by directly matching the top genes from each cluster to potential cell types using the CellMarker2.0 database. This not only speeds up the annotation process but also reduces the likelihood of manual errors. The package also provides flexibility by allowing users to specify the number of top-ranked genes (n) used for matching, enabling finer control over the annotation process. This feature is particularly useful for optimizing the balance between marker specificity and sensitivity.

While it may be tempting to adopt the top-matched cell type as the definitive annotation for each cluster, we encourage users to explore additional matched cell types. In cases where multiple, distinct cell types are matched to the same cluster, it is important to investigate the biological context and the broader experimental conditions. This exploratory approach can help uncover novel or rare cell populations and ensure that the annotation is both accurate and comprehensive. By leveraging the full potential of CellMarker2.0, users can enhance the resolution of their single-cell analysis and gain deeper insights into cellular heterogeneity.

## Example Workflow

In this example workflow, we use the PBMC3K dataset and R package Seurat [8] to illustrate the process.

### Execute the Seurat PBMC3K Guided Tutorial

![Figure](content/609619v1_ufig1.tif)

![Figure 2:](content/609619v1_fig2.tif)

**Figure 2::** UMAP of raw, unannotated Clusters

![Figure](content/609619v1_ufig2.tif)

### Match with CellMarker2.0

For each cell cluster, we identify the top 50 most highly expressed genes (selecting only those with an adjusted p-value < 0.05 and ordering them by decreasing log2 fold change) and use these to query the CellMarker2.0 database for matching cell type markers. This approach allows us to align the gene expression profiles with known markers, facilitating cell type annotation.

![Figure](content/609619v1_ufig3.tif)

**Table 1:**
 The matched marker numbers for each cluster in the CellMarker2.0 database are shown.
The column labeled “N” represents the total number of matched markers, while “uniqueN” indicates the number of unique markers. Additionally, the count of each marker is also recorded.


![Figure](content/609619v1_ufig4.tif)

![Figure 3:](content/609619v1_fig3.tif)

**Figure 3::** Visualization of cell clusters and their corresponding cell types

![Figure](content/609619v1_ufig5.tif)

![Figure 4:](content/609619v1_fig4.tif)

**Figure 4::** UMAP of easy annotation using the top matched cell.

### Evaluate Additional Potential Cell Types

Although the top-matched cell type is commonly used for annotation, it is recommended to also review the expression of markers for other potential cell types. This is particularly important when a cluster is matched to several distinct cell types. Such evaluation helps to ensure more accurate and reliable annotations. To streamline the process, clusters that are close together in the UMAP plot, such as clusters 1, 5, and 7, can be examined simultaneously.

![Figure](content/609619v1_ufig6.tif)

![Figure 5:](content/609619v1_fig5.tif)

**Figure 5::** Marker expressions for potential cell types are shown for clusters 1, 5, and 7. Expressions for other clusters are omitted for brevity.

Based on the dot plot, create a named vector to assist with cell annotation.

![Figure](content/609619v1_ufig7.tif)

### Compare with SingleR

In this analysis, we use the widely-adopted R package SingleR [2] to annotate the data. This allows us to compare the annotation results obtained from CellMarker2.0 with those generated by SingleR, providing a basis for evaluating the accuracy and consistency of our annotations.

![Figure](content/609619v1_ufig8.tif)

![Figure 6:](content/609619v1_fig6.tif)

**Figure 6::** Comparation of annotation from CellMarker2.0 and SingleR

## Conclusion and Discussion

In this study, we introduced the R package easybio, designed to facilitate single-cell annotation by leveraging the CellMarker2.0 database. To our knowledge, easybio is the first R package to incorporate CellMarker2.0 for this purpose.

We assessed the package’s performance by applying it to the Seurat pbm3k tutorial dataset and comparing the resulting annotations with those obtained using the SingleR package and manual annotations through Seurat. The comparison demonstrated that annotations derived from CellMarker2.0 were consistent with those from SingleR and Seurat’s manual methods. Importantly, easybio operates independently of external reference datasets, thereby reducing the time and expertise required compared to manual annotation processes.

easybio is not limited to single-cell annotation with CellMarker2.0; it also supports a range of analyses including bulk RNA-seq and data exploration, and it facilitates integration with other databases.

Nonetheless, several limitations should be acknowledged. The effectiveness of single-cell annotation with CellMarker2.0 depends on the quality of cell clustering, which is influenced by preprocessing steps such as data quality assessment, principal component analysis (PCA), and the selection of resolution parameters. Variations in these parameters can lead to different clustering outcomes and, consequently, affect annotation results. It is recommended to experiment with different parameter settings to assess their impact. Additionally, we only evaluated performance using the pbmc3k dataset. A broader range of datasets should be tested to provide a more comprehensive assessment, and we did not employ standardized methods to rigorously evaluate accuracy.

In summary, easybio simplifies the single-cell annotation workflow by incorporating the CellMarker2.0 database, offering a more efficient and reproducible tool for researchers.
