# Single-cell transcriptomics and machine learning reveal RNF144B and C5AR1 as immune-related biomarkers and therapeutic targets in myocardial infarction

## Authors

- Yuxin Hu<sup>1</sup>
- Lu Chen<sup>1</sup>
- Jianmei Sha<sup>3</sup>
- Caihong Shao<sup>4</sup>
- Junli Gao<sup>1</sup> †
- Jianhua Yao<sup>5</sup> †

### Affiliations

1. Cardiac Regeneration and Ageing Lab, Institute of Geriatrics (Shanghai University), Affiliated Nantong Hospital of Shanghai University (The Sixth People’s Hospital of Nantong) and School of Life Science, Shanghai University Nantong 226011 China
2. Institute of Cardiovascular Sciences, Shanghai Engineering Research Center of Organ Repair, Joint International Research Laboratory of Biomaterials and Biotechnology in Organ Repair (Ministry of Education), School of Life Science, Shanghai University Shanghai 200444 China
3. Shanghai University Hospital, Shanghai University Shanghai 200444 China
4. Department of Internal Emergency Medicine, Shanghai East Hospital, School of Medicine, Tongji University Shanghai, 200120 China
5. Department of Cardiology, Tenth People’s Hospital, School of Medicine, Tongji University Shanghai, 200090 China

† Corresponding author

## Abstract

Abstract
Background
Myocardial infarction (MI) is a life-threatening cardiovascular disease characterized by high morbidity and mortality. Although advances in clinical management have improved patient outcomes, early diagnosis and effective immunomodulatory therapies remain limited.


Methods
In this study, we integrated multiple transcriptomic datasets and applied machine learning approaches, including LASSO regression, to identify a robust 13 key genes significantly associated with MI. Gene Set Enrichment Analysis (GSEA) and Gene Set Variation Analysis (GSVA) were subsequently performed to explore their potential biological functions. The immunological relevance of these genes was evaluated by analyzing their correlations with inflammation-related genes and those involved in immune cell migration. In addition, transcription factor (Johnson, Law et al.) and microRNA (miRNA) regulatory networks were constructed to elucidate upstream regulatory mechanisms. The expression levels of the 13 key genes were validated in MI mouse model. Furthermore, molecular docking was performed to identify candidate small molecules targeting core genes.


Results
Among 11 cardiac cell populations identified, myeloid cells contributed most prominently to MI pathogenesis. A robust 13-gene predictive signature was established, with RNF144B and C5AR1 showing strong associations with immune modulation and disease severity. GSEA and GSVA further revealed that RNF144B was enriched in the neutrophil degranulation pathway, while C5AR1 was associated with the complement cascade. Correlation analysis demonstrated a significant positive relationship of RNF144B and C5AR1 with immunological roles. Both genes were also positively correlated with classical MI marker genes SERPINE1 and RUNX1. TF-gene and miRNA–mRNA regulatory networks supported the post-transcriptional regulation of these genes. In the MI mouse model, expression of the 13 genes was consistent with the risk-prediction model. Molecular docking identified CCX168 as a promising small-molecule candidate targeting RNF144B and C5AR1.


Conclusion
This study reveals immune-related transcriptional signatures and signaling pathways that drive MI progression. The identified 13-gene signature, particularly RNF144B and C5AR1, holds promise as a diagnostic biomarker and therapeutic target, providing new insights for immunomodulatory and precision medicine strategies in MI. Keywords: Immune microenvironment, myeloid cells, inflammation, RNF144B, MI, immune-targeted therapy


Highlights

A 13-gene signature was identified to predict MI risk
RNF144B and C5AR1 are key immune regulators in MI progression
GSEA and GSVA reveal immune-related pathways of RNF144B and C5AR1
CCX168 is identified as a potential small-molecule therapy for MI
Mouse model validates gene expression consistent with the prediction model

## Introduction

MI remains a leading cause of morbidity and mortality worldwide(Kathiresan and Srivastava 2012, Salari, Morddarvanjoghi et al. 2023). According to the World Health Organization, ischemic heart diseases, account for approximately 16% of all global deaths, underscoring the critical public health burden posed by this condition (Yokota, McCourt et al. 2020, Huynh, Hoffmann et al. 2024). Acute MI is commonly precipitated by sudden coronary artery thrombosis and occlusion, leading to ischemic injury, subsequent scar formation, and potential progression to heart failure(Qian 2016, Reboll, Klede et al. 2022, Virani 2023). Despite advancements in treatment, post-MI mortality rates remain significantly high, with estimates ranging from 7% to 20% within the first year following the MI event(Yokota, McCourt et al. 2020). This is associated with adverse cardiac remodeling, including ventricular dilation and fibrosis, which impairs cardiac function(Nguyen, Canseco et al. 2020, Kramann 2022).

Currently, the diagnosis of MI relies heavily on a combination of clinical symptoms, electrocardiographic changes, and the measurement of cardiac biomarkers such as troponins(McCarthy, Vaduganathan and Januzzi 2018). While these approaches are effective in many cases, they often lack the sensitivity and specificity required for early-stage detection or for distinguishing MI from other cardiovascular and systemic conditions(Schlotter, Huber et al. 2024). This diagnostic limitation hampers timely therapeutic interventions, which are critical for reducing myocardial damage and improving patient outcomes. Timely coronary reperfusion through interventions like stenting and coronary artery bypass grafting is standard in clinical practice to limit infraction extent. However, not all patients are suitable candidates for these therapies(Das, Goldstone et al. 2019). Therapeutic manipulation of the repair process, driven by robust tissue inflammation and its subsequent resolution, remains challenging(Prabhu and Frangogiannis 2016). Therefore, there is a pressing need to identify novel biomarkers that can enable early and accurate detection of MI and provide deeper insights into its underlying mechanisms.

In recent years, the integration of high-throughput sequencing technologies and computational analysis has revolutionized cardiovascular research(Kuppe, Ramirez Flores et al. 2022). Transcriptomic profiling has facilitated the identification of gene expression changes associated with disease states, while scRNA-seq offers unprecedented resolution to explore cellular heterogeneity and dynamics within complex tissues such as the heart (Ruiz-Villalba, Romero et al. 2020, Feng, Li et al. 2024, Wang and Dou 2024). Moreover, the application of machine learning algorithms has emerged as a powerful strategy to identify robust biomarkers and construct predictive models with high diagnostic accuracy (Martini 2023, Vergallo and Patrono 2023). These approaches hold great promise in bridging the gap between molecular research and clinical application(Kramann 2022).

In this study, we utilized scRNA-seq technology to compare cell subtypes between infracted and remote zones of MI-affected hearts, performing cell-type annotation and screening for genes closely associated with disease progression. To pinpoint key regulatory genes, we employed the LASSO regression, yielding a 13-gene predictive signature with high accuracy and stability. Among the identified genes, RNF144B emerged as a particularly promising biomarker due to its strong correlation with MI development. The correlations between these key genes and immune cells were analyzed via the single-sample gene set enrichment analysis (ssGSEA) algorithm. Additionally, the roles key genes in disease progression were investigated through gene set enrichment and transcription factor regulatory network analyses. Finally, by constructing a gene coexpression network, we validated the associations between the 13 key genes and the well-characterized MI-related genes RUNX1(McCarroll, He et al. 2018, Riddell, McBride et al. 2020, Amrute, Luo et al. 2024) and SERPINE1(Morange, Saut et al. 2007, Pu, Bao et al. 2022), thereby offering deeper insights into the pathogenesis of myocardial infarction.

Collectively, our study analyzed single-cell data from MI patients, revealing crucial cell types, key genes, immune infiltration patterns, and significant regulatory mechanisms within signaling pathways during disease development. Our integrated approach not only highlights RNF144B, C5AR1 and 11 other key genes as potential diagnostic and therapeutic targets but also provides valuable insights into the cellular and molecular mechanisms underlying MI. These findings offer a foundation for developing more effective strategies for early detection, risk assessment, and personalized treatment of myocardial infarction.

## Methods

### Data acquisition

The data used in this study were obtained from the Gene Expression Omnibus (GEO) database (https://www.ncbi.nlm.nih.gov/geo/) and Zenodo repository. The single-cell data file Zenodo data was used for single-cell analysis with 31 samples and 23 patients(Kuppe, Ramirez Flores et al. 2022). The dataset GSE214611 samples were collected from MI mouse model(Calcagno, Taghdiri et al. 2022). The GSE216211 dataset was annotated by the GPL24247 platform(Xu, Jiang et al. 2023).

### Single-cell analysis

Cells expressing fewer than 200 or more than 10,000 genes were excluded to remove noncellular debris and potential cell aggregates. The data were log-normalized, and highly variable genes were identified via the FindVariableFeatures function. Subsequent analyses, including data scaling and principal component analysis (PCA), were conducted via the ScaleData and RunPCA functions, respectively. Cell clustering was performed with the FindNeighbors and FindClusters functions, and uniform manifold approximation and projection (UMAP) was used for cluster visualization, implemented in the Seurat R package as per the official vignettes (https://satijalab.org/seurat/articles/get_started.html). Cluster annotation was performed on the basis of known cell markers.

### Immuno infiltration analysis

ssGSEA is extensively used to assess the types of immune cells within microenvironments. This approach identifies 22 immune cell phenotypes, encompassing T cells, B cells, and NK cells, among others. In this study, the ssGSEA algorithm was applied to quantify immune cells within the expression profile, thereby estimating the relative abundances of 22 different types of infiltrating immune cells.

### Construction of the prediction model

To select marker genes of key cells, we used the GSE214611 dataset as the training set, while the GSE216211 dataset was used as the validation set. The prediction-related models were constructed using machine learning LASSO regression. Following the integration of the expression value for each gene, a risk score formula was established for each individual and weighted according to the regression coefficient estimated through LASSO regression analysis. The risk score formula was applied to calculate the score for each patient. The precision of the model predictions was assessed by a receiver operating characteristic (ROC) curve.

### Contribution of different cell subpopulations to DFU

To evaluate the contributions of distinct cell subsets to disease development, both changes in cell abundance and gene expression profiles were examined. Initially, marker genes for each subset were identified through differential expression analysis. This involved selecting the top 100 genes with the highest expression in the control versus disease groups, which served as representative genes for each condition. Following this, the expression differences and relative proportions of these genes within each cell type were quantified. Finally, the contribution of each cell subset to the disease was calculated using the square root of the product of fold change and proportion (FC × PctProp).

### Gene set enrichment analysis (GSEA)

Patients were categorized into high and low expression groups based on their gene expression levels. To further explore differences in signaling pathways between these groups, gene set enrichment analysis (GSEA) was performed. The reference gene sets were sourced from the Molecular Signatures Database (MsigDB), specifically focusing on annotated subtype-related pathways. Differential expression analysis was applied to compare pathway activity across subtypes. Significantly enriched gene sets were identified using consistency scores with an adjusted p-value threshold of < 0.05. GSEA is commonly utilized in research that integrates disease classification with underlying biological mechanisms.

### Regulatory network analysis of key genes

The prediction of transcription factors was performed using the R package ‘RcisTarget,’ which bases its calculations entirely on motif data. The normalized enrichment score (NES) assigned to each motif depends on the total number of motifs present in the database. Beyond the motifs originally annotated in the dataset, additional annotations were inferred through analyses of motif similarity and gene sequence information. To assess motif enrichment within a gene set, the area under the curve (AUC) was computed for each motif-to-motif set comparison, utilizing recovery curve analysis that evaluates the gene set relative to the motif rankings. Subsequently, the NES for each motif was calculated from the distribution of AUC values across all motifs in the gene set. For the gene motif ranking database, this study used RcisTarget.hg19.motifDBs.cisbpOnly.500bp.

### Gene set variation analysis (GSVA)

Gene set variation analysis (GSVA) is a nonparametric and unsupervised method designed to assess the enrichment of predefined gene sets within transcriptomic datasets. By aggregating gene-level changes into pathway-level shifts, GSVA provides insight into the functional biology of samples through comprehensive scoring of targeted gene sets. In this study, gene sets were obtained from the Molecular Signatures Database (MSigDB, version 7.0), and GSVA was employed to calculate enrichment scores for each set with precision. This methodology facilitated the evaluation of potential differences in biological processes across distinct samples.

### Statistical analysis

All statistical analyses were performed using R software (version 4.3). The dataset underwent thorough preprocessing steps, including imputation of missing data and logarithmic transformation, to enhance comparability across groups and improve analytical accuracy. For comparisons between two groups, the Wilcoxon rank-sum test was applied, appropriate for data not following a normal distribution, with statistical significance defined at p < 0.05. Furthermore, to develop a reliable predictive model, feature selection was conducted using the LASSO regression technique. The model’s diagnostic capability and stability were evaluated by receiver operating characteristic (ROC) curves and the corresponding area under the curve (AUC) metrics.

### Animal studies

For this study, 8-week-old male C57BL/6J mice were used. The anesthesia agent used in the animal experiments was ketamine hydrochloride. All animal procedures were performed in accordance with protocols approved by Shanghai University Committee on Scientific Ethics.

### Expression Validation of Key Genes via Quantitative PCR

To validate the expression of key genes identified through bioinformatics analysis between myocytes and normal tissue, transcriptomes from 4 Sham mice and 4 MI mice were analyzed. Total RNA was extracted from heart tissues via TRIzol reagent (Invitrogen, USA), followed by reverse transcription into cDNA via the PrimeScript RT Master Mix (Takara, Japan). Quantitative PCR (qPCR) was performed via a SYBR Premix Ex Taq II kit (Takara, Japan). Gene expression levels were normalized to that of GAPDH, which was used as the internal control.

## Results

### scRNA-seq analysis identify contribution of different cell subpopulations to MI

To identify novel predictive and therapeutic factors associated with MI, we conducted data mining using high quality scRNA-seq datasets. The primary scRNA-seq datasets were obtained from the Zenodo data repository (DOI: 10.5281/zenodo.6578047), comprising 31 samples from 23 MI patients. The dataset includes three distinct regions: infarct zone (IZ), border zone (BZ), and remote zone (RZ). In addition, fibrotic zone (FZ) samples-typically representing fibrotic tissue-were collected 30-200 days post-MI.

The dataset underwent standard preprocessing steps, including normalization, scaling, and principal component analysis (PCA), followed by batch correction using Harmony (Fig. S1d, e). Dimensionality reduction and clustering were performed using UMAP, which identified 11 distinct cell subpopulations (Fig. 1b). Based on the expression of known marker genes, the clusters were assigned to the following cell types: cardiac muscle myoblasts, cardiac fibroblasts, cardiac endothelial cells, immature innate lymphoid cells, pericytes, lymphoid lineage–restricted progenitor cells, smooth muscle myoblasts, neuronal receptor cells, myeloid cells, epicardial adipocytes from the left ventricle, and others. A bar plot showing the expression levels of classical marker genes across these 11 cell types is presented in Fig. 2d.

![Fig. 1](content/673891v1_fig1.tif)

**Fig. 1:** a. Schematic illustration of regional partitioning for single-cell sequencing in MI tissues. RZ: remote zone; BZ: border zone; IZ: ischemic zone; FZ: fibrotic zone (30—200 days after MI).b. UMAP clustering analysis of single-cell sequencing data, identifying 11 distinct cell clusters.c. Distribution of cell clusters across different MI regions.d. Proportional changes in cell types across different MI regions.e-g. Contribution of different cell types to the pathological progression of MI.

![Fig. 2](content/673891v1_fig2.tif)

**Fig. 2:** a. Tenfold cross-validation was performed using the LASSO model to ascertain the minimum lambda value for parameter tuning.b. The distribution of LASSO coefficients and the gene combinations at the minimum lambda value were examined.c. The coefficients of the LASSO genes were analysed.d-e. Receiver operating characteristic curves of the model were generated.

To quantify the contribution of each cell type to disease pathology, we used the square root of (fold change × expression proportion) as a composite metric. Three pairwise comparisons were conducted: IZ vs. BZ, IZ vs. RZ, and BZ vs. RZ. To evaluate cell-type-specific contributions to disease progression, we first identified the top 100 highly expressed genes in both control and disease samples (total sample). We then calculated the differential expression and proportional expression of these genes within each cell subtype.

Among all subtypes, cardiac muscle myoblast, epicardial adipocytes of the left ventricle and myeloid cells exhibited the highest contribution scores across all three comparisons (Fig. 1e-g). Considering the limited abundance of epicardial adipocytes in cardiac tissue (constituting ∼504 cells at baseline) and their significant downregulation post-MI (reduction factor ∼0.5), we prioritized myeloid cells for subsequent analyses due to their greater cellular prevalence (∼701 cells at baseline) and marked upregulation following MI (induction factor ∼1.5). The IZ region represents the core area most affected by MI and reflects the most significant pathological alterations. Therefore, we selected IZ and RZ as the primary regions for further investigation.

We also explored the differences in metabolic pathway activity in myeloid cells between the IZ and RZ regions. The results revealed significant alterations in several pathways, including butanoate metabolism, beta-alanine metabolism, sulfur metabolism, fatty acid metabolism, ether lipid metabolism, and selenoamino acid metabolism, among others (Fig. S2d).

### Construction of 13-gene prediction model of MI

To training the prediction model, we selected the GSE214611 dataset was used as the training set, while GSE216211 served as the validation set. Marker genes from 701 myeloid cells were identified and subjected to LASSO regression for feature selection. This process resulted in the identification of 13 genes characteristic of MI, which were subsequently used to construct a predictive model (Fig. 2a, b).

The model formula was defined as follows:

Risk score = –3.932573 + 0.958126 × FN1 – 1.091915 × POSTN + 0.118292 × RBM47 + 0.890296 × COL1A1 + 0.666463 × TBC1D8 + 0.198664 × RNF213 – 0.324249 × SDC2 + 0.414865 × ABR – 0.023176 × COL6A3 – 0.814206 × DPYSL3 – 1.516445 × RNF144B + 0.925670 × C5AR1 + 0.380113 × GPC6 (Fig. 2c).

The model exhibited strong diagnostic performance, with an area under the curve (AUC) of 0.897 in the training set (Fig. 2d). Validation using the external GSE216211 dataset confirmed the robustness of the model, achieving an AUC of 0.788 (Fig. 2e). The final 13 key genes included: FN1, POSTN, RBM47, COL1A1, TBC1D8, RNF213, SDC2, ABR, COL6A3, DPYSL3, RNF144B, C5AR1, and GPC6.

### Immune cell infiltration in MI

As mentioned before, we found that immune cell myeloid strongly contribute to the pathological process of MI. To explore how immune system effects the MI progression, we analyzed immune cell infiltration patterns in the MI dataset.

Our results revealed the distribution of immune cell types across individual patients and uncovered the correlations among different immune cell populations (Fig. 3a, b). Notably, significant differences in the abundance of myeloid cells, including dendritic cells (DCs), M2 macrophages, and natural killer (NK) cells were observed between the two groups (Fig. 3c).

![Fig. 3](content/673891v1_fig3.tif)

**Fig. 3:** a. Relative percentages of 22 immune cell subgroups.b. Pearson correlation coefficients for 22 types of immune cells, where blue signifies a negative correlation and red signifies a positive correlation. c. Variations in immune cell composition between the two samples. d. Correlations between key genes and immune cells. e. Correlation map of key gene expressions.

Furthermore, correlation analysis between the 13 key genes and immune cell types demonstrated strong associations. Specifically: FN1 and COL6A3 showed a strong positive correlation with T follicular helper (TFH) cells; POSTN and TBC1D8 exhibited a significant negative correlation with T cells; RBM47, ABR, and RNF144B were positively correlated with macrophages; COL1A1 and DPYSL3 showed positive correlations with B cells; SDC2, C5AR1, and GPC6 were positively correlated with dendritic cells (Fig. 3d). A strong inter-gene correlation was observed among the 13 key genes, suggesting potential co-regulation or shared biological functions (Fig. 3e).

These findings provide insight into the immunological landscape of MI and suggest potential pathways through which the identified key genes may contribute to disease pathogenesis via modulation of immune responses.

### Pathway enrichment analyses identify immune-related key genes RNF144B and C5AR1 in MI

To elucidate the mechanisms through which the 13 key genes may influence MI progression, we first performed Gene Set Enrichment Analysis (GSEA). Notably, multiple genes—including C5AR1 and RNF144B—were significantly enriched in the B cell receptor (BCR) signaling complex, suggesting potential involvement in B cell–mediated immune responses (Fig. 4). Additionally, RNF144B was also enriched in PIP3 signaling in B lymphocytes, indicating a broader role in immune regulation. The BCR signaling pathway is directly interconnected with myeloid cells. Myeloid cells—such as dendritic cells and macrophages—can phagocytose pathogens, process antigens, and present antigenic peptides to B cells via MHC class II molecules, thereby promoting BCR-mediated antigen recognition, activation, and clonal expansion. Additionally, myeloid cells secrete cytokines such as IL-6, BAFF, and APRIL, which further enhance BCR signaling and promote the differentiation of B cells into plasma cells.

![Fig. 4](content/673891v1_fig4.tif)

**Fig. 4:** a-d. Gene Set Enrichment Analysis (GSEA) illustrating key genes involved in Kyoto Encyclopedia of Genes and Genomes (KEGG) signaling pathways, pathway regulation, and related genes. e-f. Gene Set Variation Analysis (GSVA). Blue indicates signaling pathways associated with high gene expression, while green represents pathways linked to low gene expression.

Complementary Gene Set Variation Analysis (GSVA) further supported immune pathway involvement. Specifically, RNF144B expression was positively associated with neutrophil degranulation, and C5AR1 was linked to the complement cascade (Fig. 4). These findings consistently highlight C5AR1 and RNF144B as key immune-related genes that may modulate the inflammatory microenvironment in MI.

### RNF144B and C5AR1 are primarily involved in immune cells and pathways, and are positively correlated with MI-associated marker genes SERPINE1 and RUNX1

To further investigate the functional relevance of the key genes, we retrieved inflammation-related factors and immune cell migration–associated genes from the GeneCards database (https://www.genecards.org/). Correlation analyses were then performed between these functional gene sets and RNF144B and C5AR1 (Fig. 5, Fig. S6, Fig. S7).

![Fig. 5](content/673891v1_fig5.tif)

**Fig. 5:** a-b. Differences in the expression levels of C5AR1/RNF144B and inflammatory pathways, where red indicates high expression and blue represents low expression. c. co-expression analysis between C5AR1 and SERPINE1. d. co-expression analysis between RNF144B and SERPINE1. e. co-expression analysis between C5AR1 and RUNX1. f. co-expression analysis between RNF144B and RUNX1.

The results revealed that RNF144B expression was positively correlated with both inflammation-related factors and genes involved in immune cell migration. In contrast, C5AR1 exhibited a paradoxical pattern: its expression was downregulated in cells where inflammation and immune cell migration pathways were upregulated. This may reflect the cell type–specific functions of C5AR1—while it promotes pro-inflammatory responses in M1 macrophages and neutrophils, it exerts anti-inflammatory effects in M2 macrophages and myeloid-derived suppressor cells (MDSCs). Notably, both RNF144B and C5AR1 were positively correlated with two well-established MI marker genes, SERPINE1 and RUNX1, further supporting their potential involvement in MI-related immune regulation.

### Regulatory network analysis of the 13 key genes

To explore the upstream regulatory mechanisms of the 13 key genes, we performed transcription factor (Johnson, Law et al.) enrichment analysis based on cumulative distribution curves. Motif annotation and enrichment analysis revealed several TF-binding motifs significantly associated with these genes. Among them, the motif taipale_tf_pairs_FOXO1_ELK3_RTMAACAGGAAGTN_CAP exhibited the highest normalized enrichment score (NES = 5.89), indicating a strong potential regulatory effect. All significantly enriched motifs and their corresponding transcription factors predicted to regulate the key genes are shown in Fig. 6a–c.

![Fig. 6](content/673891v1_fig6.tif)

**Fig. 6:** a. Transcriptional regulatory networks of key genes. b. All the enriched motifs, together with transcription factors associated with key genes. c-d. miRNA networks of key genes, with yellow representing mRNAs and green representing miRNAs.

In addition, a miRNA–mRNA regulatory network was constructed using the miRWalk database. A total of 224 predicted miRNA–mRNA interaction pairs involving the 13 key genes were identified and visualized with Cytoscape (Fig. 6d).

Together, these findings provide important insights into the transcriptional and post-transcriptional regulatory landscape of the key genes, highlighting their complex control in the context of myocardial infarction.

### Validation of RNF144B and C5AR1 Expression and Molecular Docking Analysis in the MI Mouse Model

To validate the expression of the 13-gene predictive model, particularly RNF144B and C5AR1, qPCR was performed using MI mouse heart tissue (Fig. 7a–d). As predicted by the model, C5AR1 expression was significantly upregulated in the MI heart, whereas RNF144B expression was downregulated. The expression patterns of the remaining 11 genes were generally consistent with the model, with the exception of POSTN. This discrepancy may be attributed to the fact that the MI heart tissue was harvested 24 hours post-surgery, a time point at which fibrotic remodeling may not yet be fully established.

![Figure 7.](content/673891v1_fig7.tif)

**Figure 7.:** a–c. Quantitative PCR (qPCR) validation of C5AR1 and RNF144B expression in the myocardial infarction (MI) mouse model. d. Expression levels of the remaining 11 signature genes in the MI model. e–f. Molecular docking of CCX168 with RNF144B and C5AR1. Protein structures are displayed as blue ribbons, and the docked ligands (CCX168) are shown in grey. g. Binding affinities between CCX168 and the core target proteins.

To further investigate potential interactions between the core target proteins (RNF144B and C5AR1) and candidate small-molecule compounds, molecular docking analysis was conducted. Candidate molecules were screened using the DIDB database, and CCX168 emerged as a promising ligand for both targets. CCX168 is the world’s first oral, selective inhibitor of the complement C5a receptor (C5aR), and has been approved for the treatment of two subtypes of ANCA-associated vasculitis (AAV): granulomatosis with polyangiitis (GPA) and microscopic polyangiitis (MPA). However, it has not yet been approved for use in cardiovascular or myocardial diseases.

Molecular docking analysis revealed that CCX168 exhibited strong binding affinities with both C5AR1 (Vina score: −9.3 kcal/mol) and RNF144B (Vina score: −8.8 kcal/mol) (Fig. 7e-g). A binding energy threshold of −5 kcal/mol was applied to indicate favorable interactions. The three-dimensional structures of RNF144B and C5AR1 were obtained from the AlphaFold Protein Structure Database. Docking simulations demonstrated stable and favorable binding of CCX168 to both targets. Notably, the binding site of CCX168 on RNF144B was located between amino acid residues 115–135, corresponding to the RING2 domain. This domain plays an essential role in stabilizing E2–Ub interactions and enhancing the catalytic ubiquitination activity of the RING1 domain. We hypothesize that CCX168 binding to the RING2 domain may enhance RNF144B’s E3 ligase activity by allosterically promoting RING1 function. The predicted binding pockets of RNF144B and C5AR1 are illustrated in Figure 7.

In summary, the expression of the 13-gene model was successfully validated in the MI mouse model, particularly RNF144B and C5AR1. Moreover, molecular docking analysis identified CCX168 as a potential candidate molecule for targeting these proteins, providing preliminary evidence for its possible therapeutic application in MI.

## Discussion

MI arises from the occlusion of coronary arteries, depriving cardiac tissue of oxygen and leading to cell death, inflammation, and tissue remodeling. This intricate process involves the coordinated activity of multiple cell types, including cellular migration, proliferation, extracellular matrix deposition, and structural remodeling.

Our study revealed region-specific alterations in cellular composition within the heart tissue of MI patients. Notably, there was a marked increase in myeloid cells, immature innate lymphoid cells, and fibroblasts, accompanied by a reduction in cardiac myoblasts, pericytes, and neuronal receptor cells.

Among these, myeloid lineage cells—particularly macrophages, dendritic cells (DCs), granulocytes (neutrophils, eosinophils, basophils), monocytes, and mast cells—orchestrate indispensable functions across all stages of cardiac injury response, from initial inflammation to tissue repair and remodeling. In the setting of MI, macrophages show heightened inflammatory cytokine production and an altered M1/M2 polarization, skewed toward a proinflammatory M1 phenotype. Single-cell RNA sequencing (scRNA-seq) of mononuclear phagocytes in infarcted myocardium at day 11 post-ligation demonstrated the persistence of the four homeostatic macrophage clusters alongside four newly identified populations(Dick, Macklin et al. 2019). These MI-specific populations were enriched in pathways associated with inflammation, including TNF signaling, cell adhesion and migration, and hypoxia response(Peet, Ivetic et al. 2020).

Cardiac metabolism plays a central role in maintaining tissue homeostasis and orchestrating phenotypic changes in cells. The heart relies heavily on metabolic flexibility not only for ATP production to support contraction but also to drive biosynthetic processes essential for cell maintenance and regeneration. Disruptions in metabolic pathways during MI contribute to pathological remodeling, mediated by altered gene expression, redox imbalance, and impaired metabolic efficiency(Gibb and Hill 2018). Our findings align with previous studies showing that inefficient substrate utilization and diminished anabolic activity are proximate drivers of maladaptive cardiac remodeling.

To identify critical cellular contributors to MI, we screened for the top 100 highly expressed genes across cell types and assessed their expression and proportion changes. Myeloid cells emerged as the dominant contributors, underscoring their central role in post-infarction wound healing. We employed the LASSO regression algorithm, a robust machine learning tool for feature selection in high-dimensional datasets, to construct a predictive model based on myeloid-specific markers. Thirteen genes were identified and integrated into a diagnostic model that demonstrated strong performance and stability.

Among these genes, FN1, RBM47, COL1A1, TBC1D8, RNF213, ABR, C5AR1, and GPC6 were significantly downregulated in the infarct zone (IZ), while POSTN, SDC2, COL6A3, DPYSL3, and RNF144B were upregulated. Co-expression analysis highlighted strong correlations between FN1 and COL6A3, GPC6 and COL1A1, FN1 and DPYSL3, and FN1 and POSTN, suggesting that these gene pairs may cooperatively modulate inflammatory responses, hypoxia adaptation, and angiogenesis during MI progression.

Among these, RNF144B (Ring Finger Protein 144B) is a gene encoding a member of the RING-type E3 ubiquitin ligase family (Abad, Sandoz et al. 2024). These proteins are involved in the ubiquitination process, which tags proteins for degradation via the proteasome pathway. RNF144B is characterized by the presence of a RING finger domain, which facilitates its function in mediating protein-protein interactions and catalyzing the transfer of ubiquitin molecules. RNF144B has been implicated in various cellular processes, including apoptosis, immune response regulation(Li, Zhang et al. 2024), and tumorigenesis(Zhuang, Zhang et al. 2024). Emerging evidence suggests that RNF144B plays a role in modulating signaling pathways such as NF-κB and STAT, thereby influencing inflammation and immune homeostasis.

C5AR1 was the most significantly downregulated gene, indicating its pivotal role in MI pathogenesis. C5AR1, along with C5AR2, serves as a receptor for C5a, a central component of the complement cascade(Fattahi, Frydrych et al. 2018, Desai, Kumar et al. 2023, Liu, Chen et al. 2023). Beyond extracellular complement-mediated immunity, intracellular complement signaling—referred to as the “complosome”—has emerged as a key regulator of immunometabolism(Arbore, West et al. 2016, Nording, Baron et al. 2021). Macrophages can autonomously generate C5a, which activates C5AR1 on mitochondrial membranes, shifting energy production toward anaerobic glycolysis and reactive oxygen species generation, ultimately promoting IL-1β synthesis. Loss of macrophage-specific C5AR1 has been shown to alleviate cardiovascular disease and inflammation in various models, highlighting its potential as a therapeutic target in MI(Natarajan, Abbas et al. 2018, Niyonzima, Rahman et al. 2021). Therefore, C5AR1 is expected to become a potential therapeutic target for MI.

Periostin (POSTN), a 90-kDa matricellular protein, is minimally expressed in healthy adult myocardium but re-expressed following MI(Amrute, Luo et al. 2024). Although POSTN contributes to fibrosis and adverse remodeling, it has also been implicated in promoting cardiomyocyte proliferation and myocardial regeneration(Kanisicak, Khalil et al. 2016, Li, Lou et al. 2023). Administration of recombinant POSTN post-MI has been shown to enhance ventricular function, reduce infarct size, and increase angiogenesis, indicating a dual role in cardiac pathology and repair(Hudson and Porrello 2017).

Despite advances in medical management, current therapies for MI often fall short, partly due to an incomplete understanding of its underlying mechanisms. MI is characterized by excessive inflammation, ischemia, and hypoxia, all of which disrupt the immune microenvironment and cytokine homeostasis(Zhao, Williamson et al. 2024). Our immune infiltration analysis revealed substantial differences in immune cell subsets, including dendritic cells, macrophages, T follicular helper (TFH) cells, effector memory T (Tem) cells, NK cells, and monocytes between infarct (IZ) and remote zones (RZ). We also identified significant correlations between key genes and specific immune cell populations. T cells, in particular, serve as pivotal regulators of immune reactivity and tolerance(Fan, Tao et al. 2019, Jia, Chen et al. 2022). The MI microenvironment is marked by chronic inflammation and immune dysregulation, making targeted immunotherapy—particularly aimed at reducing inflammatory cell infiltration—a compelling strategy for future MI treatment.

GSEA further demonstrated that the key genes are predominantly enriched in the BCR and IL4R signaling pathways. The BCR pathway is central to antigen recognition, B cell activation, and humoral immunity IL4R signaling mediates type 2 immune responses, influencing B cell survival, class switching, and anti-inflammatory actions. Notably, IL4Rα signaling has shown cardioprotective effects in both mice and humans following ischemic injury(Alvarez-Argote, Almeida et al. 2024). These findings suggest that dysregulated BCR and IL4R signaling may contribute to impaired healing and persistent inflammation in MI.

This study has several limitations. The predictive model was constructed using the LASSO algorithm, which, while effective, may introduce bias if used in isolation. Incorporating additional machine learning methods (e.g., Random Forest, Support Vector Machine) could enhance model accuracy and generalizability. Moreover, although we identified key genes and pathways potentially involved in MI, our conclusions are primarily based on bioinformatics analyses and correlation-based inferences. Functional validation through in vitro and in vivo experiments is necessary to elucidate the precise roles and mechanisms of these genes in MI pathogenesis. Future work will focus on experimental validation and mechanistic exploration at the cellular and tissue levels.

### Clinical Relevance

Through single-cell RNA sequencing and transcriptomic analysis, a set of 13 genes were identified as pivotal contributors to the onset and progression of MI. Additionally, a prediction model was constructed using the LASSO regression algorithm. Finally, analysis of immune infiltration and signaling pathways revealed the potential mechanisms underlying MI development. The aforementioned findings offer innovative perspectives and avenues for forthcoming clinical investigations and therapeutic approaches.

## Supporting information
