# Construction of a solid Cox model for AML patients based on multiomics bioinformatic analysis

## Authors

- Fu Li<sup>1</sup>
- Jiao Cai<sup>2</sup>
- Jia Liu<sup>1</sup>
- Shi-cang Yu<sup>3</sup>
- Xi Zhang<sup>1</sup>
- Yi Su<sup>2</sup> †
- Lei Gao<sup>1</sup> ([ORCID: 0000-0003-2336-976X](https://orcid.org/0000-0003-2336-976X)) †

### Affiliations

1. Medical Center of Hematology, Xinqiao Hospital, Army Medical University Chongqing China
2. Department of Hematology and Hematopoietic Stem Cell Transplantation Centre, The General Hospital of Western Theater Command Chengdu China
3. Department of Stem Cell and Regenerative Medicine, Southwest Hospital, Army Medical University Chongqing China

† Corresponding author

## Abstract

Abstract
Acute myeloid leukemia (AML) is a highly heterogeneous hematological malignancy. The bone marrow (BM) microenvironment in AML plays an important role in leukemogenesis, drug resistance and leukemia relapse. In this study, we aimed to identify reliable immune-related biomarkers for AML prognosis by multiomics analysis. We obtained expression profiles from The Cancer Genome Atlas (TCGA) database and constructed a LASSO-Cox regression model to predict the prognosis of AML using multiomics bioinformatic analysis data. This was followed by independent validation of the model in the GSE106291 (n=251), GSE12417 (n=163) and GSE37642 (n=137) datasets and mutated genes in clinical samples for predicting overall survival (OS). Molecular docking was performed to predict the most optimal ligands to these hub genes. The single-cell RNA sequence dataset GSE116256 was used to clarify the expression of the hub genes in different immune cell types. According to their significant differences in immune gene signatures and survival trends, we concluded that the immune infiltration-lacking subtype (IL type) is associated with better prognosis than the immune infiltration-rich subtype (IR type). Using the LASSO model, we built a classifier based on 5 hub genes to predict the prognosis of AML (risk score = −0.086×ADAMTS3 + 0.180×CD52 + 0.472×CLCN5 - 0.356×HAL + 0.368×ICAM3). In summary, we constructed a prognostic model of AML using integrated multiomics bioinformatic analysis that could serve as a therapeutic classifier.

## Introduction

Acute myeloid leukemia (AML) is a highly heterogeneous group of hematological malignancies that are characterized by various cytogenetic and molecular heterogeneities (Dohner, Weisdorf, & Bloomfield, 2015; Short, Rytting, & Cortes, 2018). Although substantial progress has been achieved with combinatorial therapies including radiation, chemotherapy, immunotherapy and/or targeted therapy, the cure rate of patients remains only 35%-40% in younger patients (age< 60 years) and 5%-15% in older patients (age< 60 years)(Döhner et al., 2010). Relapse and refractory disease continue to be major obstacles in the treatment of AML, with 29% or fewer patients living beyond 5 years.

Several studies have shown that changes in the bone marrow (BM) microenvironment in AML largely promote distinct biological processes in leukemogenesis, drug resistance and leukemia relapse(Ghobrial, Detappe, Anderson, & Steensma, 2018). Thus, insights into BMM action may provide better diagnosis and treatment strategies for AML patients.

The BM microenvironment in AML is comprised of leukemia cells, stromal cells, endothelial cells and distinct immune cell subsets. Among them, vascular endothelial cells (ECs) promote leukemia cell proliferation, drug resistance, and recurrence through paracrine vascular endothelial growth factor (VEGF), adhesion, and fusion with leukemia cells, resulting in poor prognosis (Aguayo et al., 1999; Cogle et al., 2016; Padró et al., 2002; Wegiel, Ekberg, Talasila, Jalili, & Persson, 2009). Stromal cells can promote chemotherapy resistance in leukemia cells through ligand-receptor interactions (Hazlehurst & Dalton, 2001) such as SDF-1/CXCR4 (Tabe et al., 2007) and VLA-4/VCAM-1 (Jacamo et al., 2014). Adipocytes promote the proliferation, growth and chemotherapeutic resistance of leukemia cells by breaking down stored triglycerides into free fatty acids(Shafat et al., 2017) and secreting tumor-related proinflammatory cytokines (Ye et al., 2016).

The leukemia immune microenvironment presents with immune dysregulation and suppression, leading to an imbalance of suppressor T cells and effector T cells, T cell exhaustion and an increase in myeloid-derived suppressor cells (MDSCs) and leukemia-supporting macrophages compared to normal bone marrow tissue(Mendez, Posey, & Pandolfi, 2019). Recent studies on the characterization of the leukemia immune microenvironment could aid in the search for novel prognostic biomarkers and potential therapeutic targets (Vadakekolathu et al., 2020; Yan et al., 2019). In addition, treatments such as chemotherapy, immunotherapy, and combination therapy to alter the immune microenvironment of AML have been widely used (Allie, Zhang, Tsai, Noelle, & Usherwood, 2013; Assi, Kantarjian, Ravandi, & Daver, 2018). However, different immune cells have different effects in AML. Therefore, understanding the distribution and function of immune-related genes in different immune cells is of great significance to further explore the BM immune microenvironment of AML patients.

Here, we investigated the impact and potential mechanisms of immune-related genes on the prognosis of AML. We are the first group to screen for hub genes in this disease using multiomics analysis. We constructed a LASSO-Cox regression model to predict the prognosis of AML according to the characterization of the leukemia immune microenvironment. The distribution of hub genes in immune cells was revealed through single-cell sequencing data and may provide the potential for precise patient stratification and treatment.

## Materials and Methods

### Datasets

The test cohort of acute myelocytic leukemia (AML) was downloaded from The Cancer Genome Atlas (TCGA) database (https://www.cancer.gov/) and includes mRNA data from 151 cases (RNASeq V2), miRNA data from188 cases (Illumina HiSeq miRNAseq) and Illumina Human Methylation450 Bead Array data from 140 cases. Samples were selected for the study according to the following criteria: 1) acute myelocytic leukemia was pathologically diagnosed, 2) all three kinds of data were available for the patient, and 3) the clinical information was complete. Finally, 97 patients were selected for our following study.

The other datasets were obtained from the Gene Expression Omnibus (GEO) database (https://www.ncbi.nlm.nih.gov/geo/). A total of 4 AML patient datasets were employed as independent validation cohorts: GSE12417, containing 2 datasets in which 163 samples were analyzed using the GPL96 (Affymetrix Human Genome U133A Array) platform and 80 samples were analyzed using GPL570 (Affymetrix Human Genome U133 Plus 2.0 Array) platform; the GSE106291 dataset (251 samples), which was generated using the GPL18460 (Illumina HiSeq 1500, Homo sapiens) platform; and the GSE37642 dataset (137 samples), which was generated using the GPL570 (Affymetrix Human Genome U133 Plus 2.0 Array) platform.

The single-cell RNA sequence dataset GSE116256, including 16 untreated samples (D0), was used to reveal the distribution of hub genes in immune cell types. The immune gene set, including 776 genes, was acquired from a previous study (Charoentong et al., 2017).

### Screening of candidate genes and hierarchical clustering

Differential mRNA and miRNA expression were analyzed by the DESeq2 (Love, Huber, & Anders, 2014) function (P<0.05, |logFC|>1). For each probe in the methylation data, the value shown is the β value (β =U/(M+U+1)), where M is the methylated probe signal strength and U is the unmethylated probe signal value. The methylmix package (Gevaert, 2015) was used to analyze the correlation between the gene methylation level and mRNA expression value (Pearson correlation coefficient test, R>0.5, P<0.05). Unsupervised hierarchical clustering was performed (Euclidean distances and complete linkage method) based on SIGs to establish an immunogenomic classification of TCGA-AML patients.

### Immune infiltration analysis

The enrichment scores of 28 immune signatures in each AML sample were quantified using single-sample gene set enrichment analysis (ssGSEA) (Subramanian et al., 2005). Stromal, immune, and estimate scores were further calculated to evaluate tumor purity and immune cell infiltration in tumor tissues based on the mRNA expression data using the ESTIMATE (Estimation of STromal and Immune cells in MAlignant Tumor tissues using Expression data) algorithm (Yoshihara et al., 2013).

### Protein–protein interaction (PPI) network construction and gene ontology (GO) functional enrichment analysis

mRNA interaction data were obtained from the STRING database (https://string-db.org/) (Szklarczyk et al., 2019). The PPI network was established using Cytoscape software (Shannon et al., 2003). The Database for Annotation, Visualization and Integrated Discovery (DAVID, https://david.ncifcrf.gov/) (Huang da, Sherman, & Lempicki, 2009a, 2009b) was used for GO enrichment analysis (P < 0.05), and the results were plotted by the GO plot package (Walter, Sánchez-Cabo, & Ricote, 2015).

### Survival analysis and prognostic model construction

A Cox regression model was constructed to identify immune-related genes that significantly correlated with the OS (SIGs) of AML patients in TCGA. The genes that met the standard of P < 0.05 were used for subsequent study. Least absolute shrinkage selection operator (LASSO)-penalized Cox regression analysis (Friedman, Hastie, & Tibshirani, 2010; Simon, Friedman, Hastie, & Tibshirani, 2011) was applied to distinguish the most important SIGs and to construct a prognostic model for AML based on a linear combination of the regression coefficients. Kaplan-Meier survival curves and receiver operating characteristic (ROC) curves were used to test and validate the performance of the classifier.

### scRNA dataset analysis

We employed the Seurat (Butler, Hoffman, Smibert, Papalexi, & Satija, 2018; Stuart et al., 2019) and SingleR (Aran et al., 2019) packages to generate Uniform Manifold Approximation and Projection (UMAP) plots and reveal the distribution of hub genes in each immune cell type.

### Patients and samples

A total of 55 patients with newly diagnosed AML were enrolled between Jan 2016 to Dec 2020 at the Xinqiao Hospital of the Army Medical University in China. Samples were selected for the study according to the following criteria: 1) acute myelocytic leukemia diagnoses were based on morphological findings, karyotype, and immunophenotypic features of leukemia cells by consultant hematologist, 2) patients were newly diagnosed, and remained untreated at the time of collection, 3) the clinical information was complete, and 4) a total of 38 genes mutation and SNP were detected using next-generation sequencing (NGS) technology.

### Molecular Docking

The virtual screening of molecular docking was performed using AutoDock Vina 1.1.2 (Trott & Olson, 2010 Jan 30) to predict the most likely optimal ligands. The three-dimensional structure of CD52 (PDB ID: 6OBD), CLCN5 (PDB ID: 2J9L) and ICAM3 (PDB ID: 1T0P) were retrieved from the Protein Data Bank (https://www.rcsb.org/). A library of 2115 FDA approved compounds were extracted from ZINC15 druglike database (http://zinc.docking.org/). The visualization of active interactions between proteins and compounds was performed by Discovery Studio Visualizer v4.5.0 (BIOVIA).

## Results

### Classification of AML based on immune-related genes that significantly affect patient prognosis

For a more extensive study of immune genes in AML, we retrieved transcriptome, microRNA, and DNA methylation profile data and integrated clinical information for 97 samples from TCGA database (Table S1). A Cox proportional hazard regression model was employed to analyze 776 immune-related genes (Charoentong et al., 2017) in the mRNA expression data of 97 samples (P<0.05), and 98 survival-related immune genes (SIGs) that significantly affected the survival of AML patients were identified (Table S2).

Using unsupervised clustering analysis (Euclidean statistics and complete linkage method) of 98 SIGs, those 97 samples were clustered into three distinct immune subtypes (Im1: immune cluster 1, Im2: immune cluster 2, Im3: immune cluster 3) based on the gene expression signature (Figure 1A). As shown in immune gene heatmaps, most of the SIGs were highly expressed in the Im1 and Im3 clusters but expressed at low levels in the Im2 cluster (Figure 1B). Kaplan-Meier survival analysis revealed that the prognosis of the Im2 cohort was significantly better than that of the Im1 and Im3 cohorts (Figure 1C, log-rank test, P=0.0008).

![Figure 1.](content/460430v1_fig1.tif)

**Figure 1.:** Unsupervised clustering analysis of AML patients based on 98 survival-related immune genes. A. All 97 TCGA-AML patients were divided into 3 clusters (green: Im1 cluster, red: Im2 cluster, blue: Im3 cluster). B. Heatmap of 98 survival-related immune genes in different AML clusters. C. The Kaplan-Meier survival analyses along with the Log-rank test were used to compare the overall survival (OS) of the Im1, Im2 and Im3 clusters.

### The immune infiltration was significantly different in different cluster

As the immune microenvironment was significantly correlated with the occurrence and development of AML, a single-sample gene set enrichment (ssGSEA) algorithm was utilized to explore differences in the immune microenvironment among the three immune clusters. The results showed that the Im2 cluster had fewer infiltrating immune cells than the Im1 and Im3 clusters (Figure 2A), and the specific infiltration of immune cells in different clusters is shown in Figure S1. Consistent findings demonstrated that the immune scores were significantly lower in the Im2 cluster (Figure 2B, unpaired t test, P < 0.001), while tumor purity was significantly higher in the Im2 cluster but significantly lower in the Im1 and Im3 clusters (Figure 2C, unpaired t test, P < 0.001). Generally, we can conclude that patients with less immune infiltration and lower immune scores may have a better prognosis than those with more immune infiltration and higher immune scores.

![Figure 2.](content/460430v1_fig2.tif)

**Figure 2.:** Immune functional characters of 3 AML patients clusters. A. Heatmap of the Im1, Im2 and Im3 cohorts of 97 TCGA-AML patients using ssGSEA scores from 28 immune cell types. Violin plots depict the immune score (B) and tumor purity (C) of the Im1, Im2 and Im3 cohorts.

### 42 DEG-SIGs were screened by mRNA expression data analyzing

Based on the significant differences in immune infiltration and survival trends between the Im2 cluster and Im1/3 cluster, we defined Im2 as the immune infiltration-lacking subtype (IL type) and Im1/3 as the immune infiltration-rich subtype (IR type). To reveal the potential mechanisms of different prognoses between IL and IR subtypes, an elaborate analysis of the mRNA expression profiles of the two types of AML patients was implemented. We performed differentially expressed gene analyses and identified 1936 differentially expressed genes (DEGs) with significant differences between IL and IR subtypes. There were 42 SIG-DEGs which were common members of 1936 DEGs and 98 SIGs (P < 0.05, |Fold Change|≥2) (Table 1) (Figure 3A, B).

**Table 1.**
 Common 42 intersecting genes of differentially expressed genes (DEGs) and survival-related immune genes (SIGs) between immune infiltration-lacking subtype (IL type) and immune infiltration-rich subtype (IR type) (P < 0.05, | Fold Change |≥2).


![Figure 3.](content/460430v1_fig3.tif)

**Figure 3.:** Difference analysis of the mRNA expression dataset from TCGA-AML patients. A. Volcano plot of differentially expressed genes between immune infiltration-lacking subtype (IL type) and immune infiltration-rich subtype (IR type). B. Venn plot of the intersecting genes between differentially expressed genes (DEGs) and survival-related immune genes (SIGs). C. PPI network of 42 overlap genes DEG-SIGs. D. The bubble plot represents the GO functional enrichment analysis of 42 DEG-SIGs.

To elucidate the mechanism of prognosis difference between IL and IR subtype we analyzed the interaction on the STRING website (https://string-db.org/) and constructed protein-protein interaction (PPI) networks to draw visualized interactome maps of the 42 DEG-SIGs (Figure 3C). Gene ontology (GO) functional enrichment analysis distinguished some enriched terms in three subontologies: biological processes (BP), cellular component (CC), and molecular function (MF) (Figure 3D). For BP, 42 DEG-SIGs were enriched in defense response, inflammatory response, and immune system process. With regard to CC, 42 DEG-SIGs were enriched in integrin complex, external side of plasma membrane, and cell surface. For MF, 42 DEG-SIGs were enriched in cell part, tertiary granule, and whole membrane. These results may partially illustrate the potential mechanisms of 42 DEG-SIGs affecting the prognosis of AML patients.

### 19 hub genes were screened by integrated analysis of mRNA expression data, miRNA expression data and methylation data

Considering the complex mechanism of leukemogenesis and progression, we next conducted integrated multiomics analysis to identify hub genes that were associated with prognosis. Comparing the miRNA expression profiles of patients between IL and IR subtypes, we revealed 93 miRNAs that were significantly differentially expressed (P<0.05, |FC|≥2) (Figure 4A). A total of 7294 target miRNA genes (TDEmiRs) were identified using DIANO TOOLS/microT-CDS (threshold=0.9). Through integrated bioinformatics analysis, we selected 15 commonly differentially expressed genes from 42 DEG-SIGs and 7294 TDEmiRs between the IL and IR subtypes (Figure 4C).

![Figure 4.](content/460430v1_fig4.tif)

**Figure 4.:** Multiomics analysis of 97 TCGA-AML patients. A. Volcano plot of differentially expressed miRNAs between IL and IR types. B. Correlation between mRNA expression and DNA methylation level of 6 DEG & MethylCor genes. C. Venn plot of the intersection of DEGs, SIGs, targets of DEmiRs and MethylCor gene set.

Combined analysis of mRNA and methylation profiles indicated that there were significantly negative correlations between mRNA expression level and degree of methylation for 355 genes (R < - 0.5, p< 0.05). When these 355 methylation correlation genes (MethylCor) were cross-referenced with the 42 DEG-SIGs, we identified 6 common genes associated with immune infiltration and differential expression, methylation and prognosis between IL and IR subtypes (Figure 4B, C).

### A prognostic model based on 5 hub genes was constructed

Having observed significant differences in immune infiltration, gene expression and clinical behavior between IL and IR types, we next developed a LASSO-Cox proportional hazards regression model based on 19 immune-correlated DEGs by combining microRNA and epigenetic regulation data. Using the LASSO model, we built a classifier based on the 5 hub genes to predict the prognosis of AML (risk score = −0.086×ADAMTS3 + 0.180×CD52 + 0.472×CLCN5 - 0.356×HAL + 0.368×ICAM3) (Figure 5A, B). Kaplan-Meier plots displayed OS differences between patients in various subtypes (P=3.931×10-06) (Figure 5C), and the ROC curve suggested that the model can effectively predict the 1-, 3- and 5-year prognosis of AML (AUC=0.82, 0.83, 0.99, respectively) (Figure 5D). Consistent with earlier analysis, we found similar predictive performance for 151 mRNA samples of the TCGA-AML profile (P=3.369×10-06, AUC=0.63, 0.74, 0.83) (Figure 5E, F).

![Figure 5.](content/460430v1_fig5.tif)

**Figure 5.:** Construction of the COX regression model. A. LASSO coefficient profiles of 19 candidate SIGs. B. Tuning parameter (λ) selection cross-validation error curve. The vertical lines were drawn at the optimal values determined by the minimum criteria and the 1-SE criteria. C, E. OS in patients with high vs. low risk scores depicted by Kaplan-Meier plots in the TCGA-AML-97 and TCGA-AML-151 cohorts. D, F. ROC curves depicting the accuracy of the Cox regression model in identifying AML subtypes with poor prognosis in the TCGA-AML-97 and TCGA-AML-151 cohorts.

### The prognostic model can still predict the prognosis of AML patients effectively in various validation cohorts

Since APL can achieve good therapeutic effects with the application of ATRA and ATO, we performed predictive tests separately in APL and non-APL patients. Surprisingly, we observed the same conclusions in APL (log-rank test, P=0.3618, AUC=0.85, 0.88, 0.78) and non-APL (log-rank test, P=0.01396, AUC=0.6, 0.68, 0.82) (Figure 6A, B). To test this model further, validation cohorts were obtained from the GEO database. Kaplan-Meier plots and ROC curves at 1, 3 and 5 years confirmed the prognostic value of the 5-hub-gene-based model: GSE106291 (log-rank test, P=3.311×10-06, AUC=0.66, 0.66, 0.61), GSE12417-GPL96 (log-rank test, P=3.377×10-02, AUC=0.61, 0.6, NA), GSE12417-GPL570 (log-rank test, P=3.763×10-02, AUC=0.56, 0.64, NA), and GSE37642 (log-rank test, P=3.966×10-02, AUC=0.51, 0.57, 0.6) (Figure 6C, D, E, F). After stratification by disease classification, the results showed that the risk score of the IL type was significantly lower than that of the IR type (Figure S2). These evaluations demonstrated that the 5-hub-gene-based model could identify a group of high-risk patients within conventionally assigned risk groups and may guide clinical practice.

![Figure 6.](content/460430v1_fig6.tif)

**Figure 6.:** Validation of the prognostic model. A, B. Kaplan-Meier plots and ROC curves of TCGA-AML-APL and TCGA-AML-nonAPL cohorts. C, D, E, F. Kaplan-Meier plots and ROC curves of 3 GEO cohorts.

### The better efficacy of the prognostic model for the prognosis of AML patients was further verified by clinical samples

For verifying the prognostic value in the 5-hub-gene-based model, we collected 6575 genes mutation detected in 200 newly diagnosed AML patients (TCGA.LAML.mutect.somatic.maf, https://portal.gdc.cancer.gov/files/27f42413-6d8f-401f-9d07-d019def8939e) and 38 genes mutation detected in 55 newly diagnosed AML patients (Xinqiao Hostpital). The common mutated genes were DNMT3A, IDH1, NRAS, RUNX1 and TET2. In this model classification, the high risk was significantly associated with the mutation of RUNX1 (p=0.015) and TET2 (p=0.054) considered by chi-square test (Table 2). Kaplan-Meier analyses of 55 patients with prognostic information indicated that patients with mutation of RUNX1 (Figure 7A, p=0.0001) and TET2 (Figure 7B, p=0.2257) were correlated with a poor prognosis and had a shorter median survival duration.

**Table 2.**
 Results of Chi-square test to 5 common mutated genes based on regrouping LASSO model in TCGA-AML database.


![Figure 7.](content/460430v1_fig7.tif)

**Figure 7.:** Analysis of hub genes and mutated genes in AML. A. Kaplan-Meier estimates of the OS according to RUNX1 mutation status. B. Kaplan-Meier estimates of the OS according to TET2 mutation status. (wt: wild type, mut: mutation)

### The diverse distribution of hub genes in immune cells of AML patients

To explore the value of these five hub genes in AML pathogenesis, we further identified the single-cell sequencing dataset GSE116256 to describe the distribution of the 5 hub genes in immune cells using the Seurat package for clustering and the SingleR package for annotation (Figure 8A). As shown in the scatter plot (Figure 8B) and violin plot (Figure 8C), CD52, ICAM3 and CLCN5 were widely expressed in granulocytes, monocytes, T lymphocytes, B lymphocytes, dendritic cells and NK cells, whereas ADAMTS3 was rarely expressed in those cells. HAL is highly expressed in granulocytes and monocytes but rarely expressed in other immune cells. Accordingly, we hypothesized that these hub genes play various roles through the regulation of gene expression in specific cells. The hub gene expression of blood cells in the Protein Atlas database (https://www.proteinatlas.org/) further confirmed this result (Figure S3).

![Figure 8.](content/460430v1_fig8.tif)

**Figure 8.:** scRNA analysis of hub genes. A. Clustering analysis of the UMAP plot, color coded based on cell types. B. Overlaying gene expression on UMAP clusters to illustrate the distribution of hub genes in each cell type. C. Violin plots of hub genes in each cell type.

### Investigation of best-fitting compounds on hub genes

To investigate best-fitting compounds, we performed virtual screening of molecular docking using the three-dimensional structure of CD52 (PDB ID: 6OBD), CLCN5(PDB ID: 2J9L), ICAM3(PDB ID: 1T0P) and 2115 FDA approved compounds in ZINC15 database. The predicted binding affinities of the top 2 hit compounds against respective targets are ranked from highest to lowest. Binding energy (Kcal/mol) for interaction of proteins and compounds are as follows: CD52 with ZINC164528615 (Glecaprevir) (−6.4 Kcal/mol), CD52 with ZINC3938684 (Toposar) (−6.3 Kcal/mol); ICAM3 with ZINC52955754 (Ergotamine) (−8.3 Kcal/mol), ICAM3 with ZINC1612996 (Irinotecan) (−8.2 Kcal/mol); CLCN5 with ZINC3978005 (Dihydroergotamine) (−11.8 Kcal/mol), CLCN5 with ZINC52955754 (Ergotamine) (−11.5 Kcal/mol). 2D visualization of the most probable interactions of these proteins and candidate compounds are represented in Figure 9.

![Figure 9.](content/460430v1_fig9.tif)

**Figure 9.:** Shows 2D interaction representations of the best pose of A. CD52 with ZINC164528615 (Glecaprevir), B. CD52 with ZINC3938684 (Toposar); C. ICAM3 with ZINC52955754 (Ergotamine), D. ICAM3 with ZINC1612996 (Irinotecan); E. CLCN5 with ZINC3978005 (Dihydroergotamine), F. CLCN5 with ZINC52955754 (Ergotamine).

## Discussion

AML is a highly heterogeneous malignant tumor with poor prognosis. A large number of studies have demonstrated that the immune microenvironment of AML patients is altered significantly to promote leukemogenesis in AML(Mittal, Gubin, Schreiber, & Smyth, 2014; Teague & Kline, 2013). In this study, we classified AML patients according to the difference in the SIG expression signature. The results showed that the prognosis of AML patients with immune infiltration deficiency (IL subtype) was significantly better than that of patients with immune infiltration enrichment (IR subtype), which was contrary to the effect of the immune infiltration degree in solid tumors (Thorsson et al., 2018). Recent studies have shown that the heterogeneity of immune infiltration may be affected by the components of cytokines in the microenvironment(Benci et al., 2016; J. Li et al., 2018) and the expression of tumor driver genes(Bezzi et al., 2018). These heterogeneities were significantly associated with immunotherapeutic effects.

We further compared the gene expression profiles of IL and IR patients and found that the functions of genes with differential expression between the two subtypes were mainly enriched in defense response, inflammatory response and immune system process (BP); integrin complex, plasma membrane and cell surface (CC); and cellular partial, tertiary granules, and whole membrane (MF). Consistent with our results, several studies have confirmed that the biological functional diversity of the immune system is significantly altered in the BM immune microenvironment.

Previous studies have constructed many prognostic models on the basis of diverse omics data. Hu et al. constructed a DNA methylation-based prognostic model for AML patients(Hu et al., 2019), but the accuracy of the model (AUC=0.67-0.75) was lower than that of our model (AUC=0.82-0.99). A three-miRNA signature was built for non-M3 AML patients by Xue et al., but due to the lack of validation by any independent data, its clinical application value may need further verification (Xue et al., 2019). A four-gene-based prognostic model from Huang et al. (Huang, Liao, & Li, 2017) was also less accurate (AUC=0.66-0.71) than our model.

These conventional prognostic analyses generally consider only mRNA, miRNA, or methylation data. To the best of our knowledge, this is the only study to date to construct a prognostic model through the integrated analysis of multiple omics datasets (mRNA, miRNA and methylation data). The TCGA-AML test dataset and three independent GEO-AML validation datasets confirm that the model is very effective in predicting the prognosis of AML patients. The model consists of five hub genes: ADAMTS3, CD52, CLCN5, ICAM3 and HAL.

ADAMTS3 is a member of the ADAMTS family and plays an important role in the genesis and development of a variety of tumors(Gomis-Rüth, 2009; Rocks et al., 2008). Previous studies demonstrated that ADAMTS3 is expressed in mast cells(Charoentong et al., 2017), and mast cells have both tumor-promoting and tumor-inhibiting effects(Oldford & Marshall, 2015), thus leading to different prognoses in different tumors(Fleischmann et al., 2009; Groot Kormelink, Abudukelimu, & Redegeld, 2009; Rajput et al., 2008). Our study confirmed that ADAMTS3 expression was significantly negatively correlated with the prognosis of AML and is rarely expressed in other immune cells. Therefore, we will pursue further in-depth analysis of how ADAMTS3 exerts its antitumor effect through mast cells to explore its potential therapeutic value.

CLCN5 (chloride voltage gated channel 5) is a member of the chloride channel family. It is widely expressed in a variety of tumor cells(Ernest, Weaver, Van Duyn, & Sontheimer, 2005) and can enhance the chemotherapy resistance of chronic lymphocytic leukemia and multiple myeloma(Ruiz-Lafuente et al., 2015; Zhang et al., 2018). Hsa-let-7c-5p and hsa-mir-495-3p, two miRNAs that target CLCN5, were found to be involved in the occurrence and development of a variety of tumors(Liao et al., 2020; Wu et al., 2020). Our study confirmed that CLCN5 plays a role in promoting tumorigenesis in AML, but its specific mechanism needs deeper investigation.

HAL (histidine ammonia lyase) is the rate-limiting enzyme of histidine catabolism(Brand Lm Fau - Harper & Harper, 1976). Kanarek et al. found that tumor cells with higher HAL expression levels possess higher sensitivity to methotrexate. Acute lymphocyte leukemia (ALL) patients with higher HAL expression were more likely to benefit from methotrexate treatment(Kanarek et al., 2018). In our study, we found that the expression level of HAL was significantly correlated with the degree of gene methylation. However, as a demethylation agent, hypomethylating agent (HMA) alone has difficulty achieving the intended effect in the clinical treatment of AML(Duchmann & Itzykson, 2019). We speculated that the combination of methotrexate and HMA may achieve better efficacy when changes in HAL expression are detected. Surprisingly, we found that HAL was only expressed in granulocytes and monocytes. Consistent with AML cells, granulocytes and monocytes originate from myeloid precursor cells(Mendez et al., 2019). Therefore, insight into the methylation mechanism of HAL and its effect on the innate immune response and AML cells will be conducive to improving the therapeutic effect of demethylation agents. We also assessed the interaction between HAL and hsa-miR-582-3p, which has been previously indicated as a tumor suppressor miRNA in AML (H. Li et al., 2019). Thus, deeper investigation of the relationship between HAL and miR-582-3p will be helpful to further understand the potential mechanism of malignant progression of AML.

Our study found that CD52 was widely expressed in leukemia cells and all types of immune cells. Evidence has revealed the high expression of CD52 in CD34+ stem cells of AML (5q-) patients and a significantly negative correlation between the CD52 expression value and the prognosis of AML (Blatt et al., 2014), which is consistent with our results. ICAM-3 (intercellular adhesion molecule 3, CD50) belongs to the ICAM (intercellular adhesion molecule) immunoglobulin superfamily and plays important roles in immune response and tumor development(Cavallaro & Christofori, 2004; Xiao, Mruk, & Cheng, 2013). Consistent with our scRNA sequencing results, ICAM-3 is expressed in granulocytes, monocytes and lymphocytes(de Fougerolles & Springer, 1992). In vivo and in vitro experiments confirmed that ICAM-3 participates in the proliferation, stemness and radiotherapy resistance of various tumors through the FAK pathway, PI3K/Akt pathway or other mechanisms(Chung et al., 2005; Kim et al., 2006; Shen et al., 2018). Interestingly, we found that the expression levels of CD52 and ICAM-3 were both significantly correlated with the degree of methylation but had opposite impacts on the prognosis of AML patients. Therefore, the roles of CD52 and ICAM-3 should be considered in HMA reagent treatment.

In conclusion, using a multiomics analysis and validation approach, we constructed and validated a novel, 5-hub-gene-based model that allows robust risk stratification and facilitates the identification of prognosis in AML. The distribution of the 5 hub genes in immune cells was revealed through scRNA sequencing analysis. Furthermore, we preliminarily explored the possible mechanisms of these hub genes in the leukemogenesis of AML. These findings may provide novel therapeutic targets for AML. Our study also provided new insight into the use of demethylation drugs in AML. Of course, this study is limited to bioinformatics analysis, and the proposed approaches need to be further tested in the clinic.
