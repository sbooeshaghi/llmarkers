# APNet, an explainable sparse deep learning model to discover differentially active drivers of severe COVID-19

## Authors

- George I. Gavriilidis<sup>1</sup> ([ORCID: 0000-0003-2575-4354](https://orcid.org/0000-0003-2575-4354)) †
- Vasileios Vasileiou<sup>1</sup> ([ORCID: 0000-0003-0145-033X](https://orcid.org/0000-0003-0145-033X))
- Stella Dimitsaki<sup>1</sup> ([ORCID: 0000-0002-6356-9531](https://orcid.org/0000-0002-6356-9531))
- George Karakatsoulis<sup>1</sup> ([ORCID: 0000-0002-8496-3087](https://orcid.org/0000-0002-8496-3087))
- Antonis Giannakakis<sup>2</sup> ([ORCID: 0000-0003-2975-0326](https://orcid.org/0000-0003-2975-0326))
- Georgios A. Pavlopoulos<sup>4</sup> ([ORCID: 0000-0002-4577-8276](https://orcid.org/0000-0002-4577-8276))
- Fotis Psomopoulos<sup>1</sup> ([ORCID: 0000-0002-0222-4273](https://orcid.org/0000-0002-0222-4273))

### Affiliations

1. Institute of Applied Biosciences, Centre for Research and Technology Hellas Thessaloniki Greece
2. Department of Molecular Biology and Genetics, Democritus University of Thrace Alexandroupolis Greece
3. University Research Institute of Maternal and Child Health and Precision Medicine, National and Kapodistrian University of Athens 11527 Athens Greece
4. Institute for Fundamental Biomedical Research, BSRC “Alexander Fleming” Vari Greece
5. Center of New Biotechnologies & Precision Medicine, Department of Medicine, School of Health Sciences, National and Kapodistrian University of Athens Athens Greece

† Corresponding author

## Abstract

Abstract

Motivation
Computational analyses of plasma proteomics provide translational insights into complex diseases such as COVID-19 by revealing molecules, cellular phenotypes, and signaling patterns that contribute to unfavorable clinical outcomes. Current in silico approaches dovetail differential expression, biostatistics, and machine learning, but often overlook nonlinear proteomic dynamics, like post-translational modifications, and provide limited biological interpretability beyond feature ranking.

Results
We introduce APNet, a novel computational pipeline that combines differential activity analysis based on SJARACNe co-expression networks with PASNet, a biologically-informed sparse deep learning model to perform explainable predictions for COVID-19 severity. The APNet driver-pathway network ingests co-expression and classification weights to aid result interpretation and hypothesis generation. APNet outperforms alternative models in patient classification across three COVID-19 proteomic datasets, identifying predictive drivers and pathways, including some confirmed in single-cell omics and highlighting under-explored biomarker circuitries in COVID-19.

Availability and Implementation
APNet’s R, Python scripts and Cytoscape methodologies are available at https://github.com/BiodataAnalysisGroup/APNet

Contact
ggeorav@certh.gr

Supplementary information
Supplementary information can be accessed in Zenodo (10.5281/zenodo.10438830).

## Introduction

Human plasma is a vital clinical specimen encompassing a broad spectrum of proteins, including tissue markers, immunoglobulins, transcription factors, kinases, metabolites, and secreted factors (Eldjarn et al., 2023; Zhong et al., 2021). With the advent of high-throughput technologies (-omics), the human plasma proteome has become a focal point for discovering novel biomarkers and therapeutic targets for complex diseases. This has been especially the cases with severe COVID-19, a condition besetting many patients infected with the SARS-CoV-2 coronavirus (Babacic et al., 2023). Plasma proteomics have provided significant biological insights into the immunopathology of severe COVID-19, which is characterized by the inflammatory “cytokine storm”, Acute Respiratory Distress Syndrome (ARDS), PANoptosis-induced cell death, and multiorgan failure (Diamond and Kanneganti, 2022). Plasma proteomics has also been explored in long-COVID-19 syndromes and vaccine response variations (Liang et al., 2023).

Many studies have measured plasma proteomics using Olink Proximity Extension Assay (PEA) in COVID-19 research due to this technology’s specificity, scalability and multiplexing benefits (Wik et al., 2021). In our recent work, we assessed pertinent Machine Learning models applied in these high-dimensional datasets like Random Forest, Gradient Boosted Decision Tree, XGBoost, Extra Tree classifiers, Logistic regression, Lasso Logistic regression, Support Vector Machine (SVM), and Deep Learning (DL) (e.g., AutoGluon-Tabular). Some models exhibited eXplainable AI (XAI) features by deploying Shapley additive explanation (SHAP) values, the minimal-optimal variables method or a random forest explainer. In the same work, we managed to dovetail an explainable, computational pipeline to benchmark a wide assortment of ML tools on predicting COVID-19 severity from Olink plasma proteomics which revealed Multi-Layer Perceptron (MLP) as the highest-performing algorithm (Dimitsaki et al., 2023).

However, most of the above studies can partially approximate proteomic non-linear dynamics (e.g., post-translational modifications, protein co-expression networks, complex formation, and subcellular localization), thus missing signaling proteins that may drive critical COVID-19 pathways. Moreover, these studies’ ML/DL findings often lack extensive external validation in large independent datasets, while their biological explainability is usually restricted to mere feature ranking (Paul et al., 2023) (Dimitsaki et al., 2023).

Acknowledging these challenges, we introduce Activity PASNet (APNet) in this manuscript. This computational DL pipeline initially uses the SJARACNe data-driven network algorithms to uncover disease drivers prioritized based on “activity,” an aggregate metric of their capacity to regulate their transcriptional targets non-linearly (Ding et al., n.d.; Dong et al., 2023). These drivers can be overt (differentially expressed and possibly active) or “hidden” (differentially active but not expressed). Next, APNet feeds these drivers into Pathway-Associated Sparse Deep Neural Network (PASNet) (Hao et al., 2018), which incorporates biological priors as hidden layers to ultimately deliver interpretable clinical classifications, validated by the eXplainable AI component of SHAP values. Finally, APNet facilitates the analysis of SJARACNe co-expression networks, equipped with the weights from the DL classification task, to streamline data exploration and the formation of mechanistic hypotheses for further biological investigation.

We extensively trained, tested, and validated APNet on activity matrices from 3 distinct Olink plasma proteomic datasets (MGH, Mayo, Stanford) (Byeon et al., 2022; Feyaerts et al., 2022; Filbin et al., 2021). APNet managed to pinpoint ground-truth drivers of severity, predicted new proteomic markers with potential theranostic potential (some of which were traced to circulating PBMCs through scRNA-seq analysis), outperformed alternative ML/DL models in demarcating severe COVID-19 cases and enabled the inference of a potential signaling network from predictive factors in the liver of individuals with severe COVID-19.

## Materials and methods

### APNet overview

APNet is a modular pipeline (Figure 1) which aims to facilitate the discovery of novel predictive drivers of severe clinical outcomes and to facilitate the formulation of mechanistic hypotheses. In this present work, we considered cases experiencing severe and non-severe COVID-19.

![Figure 1.](content/575161v1_fig1.tif)

**Figure 1.:** APNet workflow, as implemented in the herein COVID-19 multi-omic study to discover predictive drivers of severity. Image made using the Biorender toolkit.

### Brief description of APNet modular architecture

#### Module 1- Differential activity analysis for drivers of COVID-19 severity

In this module, conversions of expression values to activity values for plasma proteomics were accomplished with NetBID2 (Dong et al., 2023) toolkit whereas for scRNA-seq data with scMINER toolkit (Ding et al., 2023). For the plasma proteomics, we applied the NetBID2 algorithm, which reverse-engineers context-specific interactomes and integrates network activity inferred from large-scale multi-omics data, empowering the identification of hidden drivers that traditional analyses cannot detect. By leveraging the MSigDB database, we compiled distinct lists of Transcription Factors (TF) and signaling molecule proteins. Separate TF and signaling molecule networks were constructed using SJARACNe. These networks featured drivers (hubs) connected to their targets through protein-protein interactions, derived from their expression patterns.

To calculate the activities of driver proteins in each dataset based on protein expression, we employed the “cal.Activity” function in NetBID2. The weighted mean activity of a driver candidate protein (Driver{i}) in sample s, was computed using the following equation:



Here, the NPX count proteomics matrix, EXP{sj} represented the expression value of gene j in sample s, MI{ij} indicated the mutual information between master regulator protein i and its target protein j, and SIGN{ij} was the sign of the Spearman correlation between protein i and its target protein j. The total number of targets for DRIVER i was denoted by n.

Differential activities were then computed for Severe and Non-Severe Status across the three datasets, by using the “getDE.BID.2G” function, allowing us to identify genes exhibiting distinct regulatory patterns in response to severity variations, through Bayesian model.

Also, we deployed the scMINER workflow, based also on SJARACNe, to discover severity drivers in MGH scRNAseq data. For both differential expression and differential activity, the function get.DA was performed by using the SCT matrix and activity matrix, respectively. Data visualisation for single-cell analysis was performed through the Seurat pipeline (4.3.0).

#### Module 2- Driver-pathway mapping

To prepare input data for the biologically explainable PASNet DL model on Module 3, joint differentially active drivers of severity from the three Olink studies were mapped to biological pathways using the Enrichr KG (Evangelista et al., 2023). 30 pathways from each of the following resources were leveraged (KEGG, Reactome, GO:BP and Wikipathways 2021) for the commonly decreased and increased drivers of severity separately. Drivers were mapped to the retrieved pathways in a binary fashion with 0s and 1s, i.e. when a driver was participating in the gene set of a pathway it was assigned the value of 1 and vice versa.

#### Module 3-Deep Learning classification of Severe COVID-19 cases with biological explainability

The findings from Modules 1 and 2 served as input for Module 3, where a sparse neural network model called PASNet was used to predict COVID-19 severity. The model was trained on MGH data, validated on Mayo and tested on Mayo and Stanford datasets. A separate model was trained and tested using scMGH data. Model performance was evaluated using Area Under the Curve (AUC) and F1-scores, along with ROC curve analysis. The PASNet training phase is expressed through the following equations.

Sparsity of the PASNet sub-network function: h(l+1) = a((W(l) * M(l))h(l) + b(l))



where

Q(l) is the S-th percentile of |W(l)| if l ≠ 0

M: mask matrix for each layer

l:layer

W: weight matrix

b: vias vector

Cost-sensitive learning for imbalanced data: 



Thus, the weights and biases on the l-th layer are updated by:



where

Ck:mean error on the class k

yi:ground truth

yi:prediction

nk:number of samples in the class k

L: total cost

c(.):cost function (e.g., cross-entropy loss)

λ: regularization hyperparameter

η:learning rate

Biological explainability of the whole sparse DL model is predicated in the combination of Shapley values (SHAP) and the driver-pathway mappings that PASNet architecture offers, assigning learning weights.



N: is the set of all input features

i: feature

f: model

M: is the number of features

#### Module 4- Bipartite graph analysis

This final APNet module leverages the SJARACNe co-expression networks from each study for the joint differential active drivers and augments it by connecting drivers to pathways based on Module 2. The weights of driver-driver edges contain the Mutual Information (MI) metric and the Spearman correlation coefficient (positive values signify activation, negative values the opposite), amongst other metrics. Driver-pathway edges contain as weights the PASNet-weights that PASNet learned during training-testing tasks from Module 3. Our study used Cytoscape to perform network visualization, basic analysis for network statistics and centrality metrics (Betweenness Centrality algorithm), dimensionality reduction using tSNE (cluster signal propagation simulation (OCSANA+) and analysis for shortest paths (PathLinker tool)(Gil et al., 2017; Marazzi et al., 2020).

OCSANA+ is a Cytoscape application that analyses the structure of large-scale complex networks. It identifies nodes that drive the system towards a desired long-term behavior and ranks the combinations of interventions that are likely to be more effective. Additionally, it estimates the effects of perturbations in signaling networks. We used the Signal Flow Analysis (SFA) feature of OCSANA+ to simulate signal propagation. The SFA algorithm estimates the signal flow in a signaling network by analyzing the topological information. It employs a linear difference equation that considers a node’s previous activity, the effect and influence of incoming edges, and the initial activities of the node. The algorithm focuses on the information conveyed by a series of biological interactions represented in a signaling network (Marazzi et al., 2020).

PathLinker is a Cytoscape app based on an algorithm reconstructing interactions in a signaling pathway. It requires a directed network, a set of sources, and a set of targets as inputs. The algorithm computes the k best-scoring loopless paths and outputs the sub-network of the k best paths. The algorithm offers three choices for managing edge weights: (i) No weights: Path score is based solely on the number of edges in the path, and PathLinker identifies the k paths with the lowest scores, (ii) Additive edge weights: Path score results from the summation of edge weights, and PathLinker finds the k paths with the lowest scores in this scenario as well, (iii) Probabilistic edge weights: Common in protein interaction networks, where weight represents experimental reliability. PathLinker treats these weights as multiplicative, seeking the k paths with the highest cost, where the product of edge weights determines cost. Internally, PathLinker transforms each weight by taking the absolute value of its logarithm to map the problem to the additive case (Gil et al., 2017) (Figure 2).

![Figure 2.](content/575161v1_fig2.tif)

**Figure 2.:** Outline of APNet complex graph and the ensuing analysis with shortest path algorithms for uncovering non-intuitive connections among drivers and pathways.

### Technical benchmarking and bioinformatic validation based on COVID-19 prior knowledge

To benchmark APNet’s performance on patient classification from Olink plasma proteomics, we deployed the PASNet approach on original NPX values of Olink plasma proteomics and a Random Forest model on the transformed activity values. Firstly, for PASNet we used the expression values for training, validation and test, by using the count matrices of MGH, Mayo and Stanford, respectively. The count matrices were filtered by keeping only the common significant proteins across 3 datasets from Differential Expression analysis to perform the PASNet approach on expression data. Similarly to the APNet approach, pathways collected from EnrichR-KG, by using (KEGG, Reactome, GO:BP and Wikipathways 2021) for the commonly decreased and increased drivers of severity separately. PASNet used the count matrices across 3 datasets for training, validation, and test, by using MGH, Mayo, and Stanford respectively. Then for Random Forest, we used activity matrices from 3 datasets, by applying training, validation and test into MGH, Mayo and Staford, respectively.

Bioinformatic validation of the top 20 most predictive drivers for each experiment was pursued by mapping these drivers to the 9 curated networks regarding COVID-19 immunopathological hallmarks by SIGNOR (https://signor.uniroma2.it/covid/). Level 4 networks were obtained for each COVID-19 hallmarks and downstream processing was conducted in Cytoscape.

Finally, selective data mining for key drivers of interest was performed in the web tool https://www.covid19dataportal.org/.

### DOME recommendations

The assembly of APNet was performed considering the recently published DOME recommendations, a set of community-wide recommendations for reporting supervised machine learning–based analyses applied to biological studies (see supplementary information) (Walsh et al., 2021) (Supplementary Material 1).

## Results

### Harmonization of COVID-19 patient cohorts and assembly of plasma proteomic datasets

Initially, we harmonized patient stratification for COVID-19 severity based on WHOscore (“Severe” vs “NonSevere”) across the three Olink proteomic datasets. In particular, COVID-19 cases who had a fatal outcome or were admitted in the ICU or were intubated were designated as “severe” and the residual cases were designated as “non-severe”. In the MGH study, we designated 80 severe and 225 non-severe cases. In the Mayo study, we demarcated 268 severe and 181 non-severe COVID-19 cases. Furthermore, we determined 24 severe and 40 non-severe cases in the Stanford study. Associations with respective WHOscores and age can be seen in (Sup. Figure 1).

From all 3 Olink studies, 1463 common plasma proteins were bioinformatically studied within APNet and were used for downstream processing to uncover predictive markers of severity.

### Data preprocessing and detection of severity drivers across proteomic studies

Next, we used the NetBID2 toolkit through APNet to detect common differentially active proteins (DAPs) in severe COVID-19 cases, for all three Olink studies. Notably, for MGH, the prominent positive drivers included TACSTD2, BAG3, POLR2F, DPY30, and CAPG. Conversely, the top negative drivers for MGH were CCL22, BTC, IGFBP3, TNFSF11, and ICOSLG (Sup. Figure 2A). Similarly, in the case of Mayo, the leading positive drivers consisted of VSIG4, IL1RL1, IL27, KRT19, and JUN, while negative drivers entailed CDON, CD1C, ITGB7, TNFSF11, and LRRN1 (Sup. Figure 2B). For Stanford, the primary positive drivers were LGALS1, CSTB, MAD1L1, DDAH1, and CCL7 and the negative were EPCAM, CPA2, CDNF, DSG4, and CD1C. Pathway enrichment showed that these severe COVID-19 top-drivers were associated with cell migration, monocyte activation, methylation changes and immune cell dysregulation (Sup. Figure 2A-C).

From hereon, we focused on the commonly perturbed drivers across the three studies. APNet captured 333 common differentially active proteins (DAPs) across the three studies and encompassed 163 differentially expressed proteins (DEPs) and 170 hidden drivers (i.e., hidden in at least one of the three Olink datasets) (Figure 3A-B). Among the 333 common drivers, 150 were differentially hyper-active and 183 were hypo-active in severe COVID-19. When analyzing the STRINGdb network of common DAPs, centrality analysis prioritized DEPs like immuno-regulatory interleukins IL4-IL6, keratin modulators (KRT19), chemokines for macrophages and neutrophils (CXCL8/CCL20) and transcription factors (JUN). Other central decreased DEPs were effectors of T cell activation and proliferation (CD8A, CD28), mediators of developmental pathways like the SCF/c-Kit pathway (KIT/KITLG/IL7R/FLT3/CD34) and cellular adhesion surface molecules (ITGB1). Similarly, central hyper-active hidden drivers (“positive”) pertained to growth factors (HGF), ECM remodellers (metalloprotease inhibitor TIMP1), chemoattractants of monocytes, natural killer and T-cells (CXCL9/CXCL10/CCL3) and biomarkers of systemic organ failure (the lipocalin LCN2 indicating acute kidney injury). Other central hypo-active hidden drivers included cellular adhesion molecules (NCAM1, ITGB2, ITGAV), growth factors (FLT3LG, ligand for the FLT3 receptor found in DEPs) or cognate receptors (EGFR, receptor for the Epidermal Growth Factor) and the tumour suppressor molecule PTEN (Figure 3C).

![Figure 3.](content/575161v1_fig3.tif)

**Figure 3.:** (A) Venn diagrams showing overlapping differentially expressed proteins (DEPs) and differentially active proteins (DAGs) among the three studies. (B) SuperVenn diagram depicting the joint differentially expressed (increased/decreased) or active proteins (hyper/hypo-active) in severe COVID-19 compared to non-severe COVID-19 cases, across the three Olink studies. (C) STRINGdb protein-protein interaction networks for joint DEPs and hidden drivers of severity across the three studies (STRINGdb score > 0.4). The size of the nodes is analogous to the centrality of each protein/driver (BetweenessCentrality algorithm) and the colour denotes perturbational direction (red for increased, blue for decreased). (D-E) Bubble plots depicting over-representation analysis based on the Enrichr Knowledge Graph (Wikipathways 2021, Reactome, GO:BP, KEGG) for joint drivers with increased (D) and decreased activity (E) in severe COVID-19 cases, among the three Olink plasma proteomic studies.

Pathway enrichment through the Enrichr KG (KEGG, Wikipathways, Reactome, GO:BP) highlighted several biological ground truths involved in COVID-19 immunopathology such as increased activation of innate immunity, lung fibrosis, MAPK signaling, Sars-CoV-2 immuno-evasion, neutrophil degranulation and viral protein interaction with cytokines and cognate receptors (Figure 3D). Conversely, dwindling pathways in severe COVID-19 included the hematopoietic system, inhibitors of the PI3K-Akt signaling pathway, cellular adhesion mechanisms through integrins and the Hippo-Merlin signaling pathway, revealing an impairment of physiological proliferation and migration for circulating immune cells (Figure 3E).

To better dissect the increased perturbational space captured by APNet, distinct cellular enrichment for DEPs and hidden drivers was conducted using the GTEx_Tissues database through Enrichr. DEPs exhibited an over-representation for peripheral blood, spleen, liver, brain, and adipose tissue. Hidden drivers, conversely, implicated other organs like oesophagus, tibial nerve and the cardio-vascular system (Sup. Figure 3A-D). Ensuing pathway enrichment with WikiPathways and GO:BP uncovered an expected affiliation of DEPs with key COVID-19 molecular “landmarks” like apoptosis, viral life cycle, neutrophil degranulation, PI3K Akt signaling and impediments in synapse functionality and angiogenesis. Interestingly, the hidden drivers were skewed towards aberrant insulin signaling, cellular adhesion imbalances (L1cam interactions), propagation of hypoxia and abnormal neuronal behaviour (increased neuroinflammation, decreased neuroplasticity) (Sup. Figure 3E-F, Sup. Figure 4).

These preliminary findings underline the importance of employing activity transformations on distinct COVID-19 plasma proteomic datasets using APNet. Beyond mere differential expression, this approach identified shared, systemic damages caused by Sars-CoV-2 across multiple organs and tissues (Supplementary Material 2-3).

### APNet classifies severe COVID-19 cases among distinct plasma proteomic studies

At this point, we hypothesized that the newly discovered hidden drivers had untapped biological potential, which could enhance the clinical prediction of severe COVID-19 cases from plasma proteomics.

We used the common DAPs across the three Olink studies for the ensuing clinical predictions. After initial training in the MGH dataset (for details, see Materials and Methods), APNet accurately predicted severe COVID-19 patients during the early testing phase (MGH-Mayo experiment) with significant robustness (AUC = 0.96, F1 score = 0.9). Biological explainability highlighted the prognostic significance of various DEPs (JUN, IL6, MAPK9, TNFRSF1A, AREG, NTF4, NCF2, TNFRSF10A, FLT3, CKAP4, FLT3LG, SDC1, TNFRSF10B, TNFSF11) but also several hidden drivers (FTL3LG, LYN, PTEN, EFNA1, ACAA1, HGF, TIMP1) (top-20). The most predictive pathways involved the ground-truth “cytokine storm”, MAPK signaling, vascular damage reflected on atherosclerosis potential, protein folding (through HSP90 chaperone), and PI3K-Akt signaling pathway (Figure 4A-B).

![Figure 4.](content/575161v1_fig4.tif)

**Figure 4.:** (A-B) Bar plots for SHAP values and driver-pathway mapping from PASNet signifying the top-20 predictive drivers and their corresponding pathways, for the MGH (training) / Mayo (testing) experiment. Furthermore, the AUC and F1-score values are depicted. (C-D) Same as (A) for the MGH (training) / Stanford (testing) experiment. Class 0 refers to nonsevere and Class 1 refers to severe COVID-19 cases. (E) Hierarchical clustering of MGH, Mayo and Stanford cases on the basis on the predictive proteomic drivers, along with selected clinical covariates.

During the second testing phase (MGH-Stanford experiment), APNet once again exhibited significant predictive robustness since, on the Stanford dataset, it could foreshadow severe COVID-19 efficiently (AUC = 0.91, F1 score = 0.68). Biological explainability revealed predictive drivers of severity, many of which overlapped with the ones from the previous testing experiment (i.e. PTEN, JUN, IL6, LYN, TNFRSF1A, TNFRSF10A, TNFRSF10B, TNFSF10) but also unveiled novel ones (BAX, LTA, KDR, COL1A1, CCL7, EGFR, ERBB2, CCL22, PODXL, SEMA4D, KIT, ROBO1). The hidden drivers were PTEN, BAX, CCL22, EGFR, LYN, ROBO1 (Figure 4C).

The most predictive pathways in this experiment involved viral infection and disruption of cytokines and cognate receptors, PI3K-Akt signaling pathway, MAPK signaling, Hippo-Merlin signaling dysregulation, and intensified Interleukin signaling pathway, apoptotic TRAIL signaling, neurotoxicity concerning axonogenesis, and imbalances in lipid metabolism (Figure 4D) (Supplementary Material 4).

Hierarchical clustering on all cases across studies revealed associations of the most predictive drivers with COVID-19 severity, while in the MGH study, further associations with diabetes and kidney disease were also uncovered (Figure 4E).

### APNet bridges plasma proteomics with single-cell transcriptomics

At this point, we decided to use APNet for a joint analysis between bulk plasma proteomics (MGH dataset) and scRNA-seq data from circulating peripheral blood mononuclear cells (PBMCs, 4 severe and 10 non-severe MGH cases). We sought to (a) prioritize which predictive drivers of COVID-19 severity could be important for both-omic modalities and (b) trace the cellular origin of various predictive drivers of COVID-19 severity from all the insofar classification experiments among the PBMC cellular populations. (Figure 5A).

![Figure 5.](content/575161v1_fig5.tif)

**Figure 5.:** (B-C) Bar plots for SHAP values and driver-pathway mapping from PASNet signifying the top-20 predictive drivers and their corresponding pathways, for the MGH plasma proteomic (training) / scRNA-seq (testing) experiment. Furthermore, the AUC and F1-score values are depicted. Class 0 refers to nonsevere and Class 1 refers to severe COVID-19 cases. (D-E) Heatmaps depicting the activity and the expression of predictive drivers from all the APNet experiments, across various PBMC cell types. The scMINER toolkit and visualisation performed the activity calculations were attained through Seurat. Only the predictive drivers with positive activity values are depicted.

Initially, we deployed the scMINER toolkit to convert the typical sparse scRNA-seq expression matrix into a non-sparse activity matrix based on the SJARACNe/MICA/MINIE algorithms (see Materials and Methods for details). Single-cell differential activity analysis revealed 282 differentially active drivers (140 DEGs and 142 hidden drivers) in severe COVID-19, which were also perturbed in the MGH plasma proteomic analysis (Sup. Figure 5A). STRINGdb PPI network modeling and pathway enrichment implicated several key COVID-19 severity drivers in innate/adaptive immunity, viral replication, inflammatory signaling, cell adhesion and lipid metabolism (e.g., IL6, NCAM, LYN, PTEN, ITGB1, ITGAM) (Sup. Figure 5B-D), in line with our findings from the previous plasma proteomic analyses.

Next, we trained APNet on the MGH plasma proteomic dataset and tested it on the MGH single-cell dataset (scMGH). APNet was highly robust in classifying severe COVID-19 cases (AUC: 0.99, F1-score: 0.975). The driver-pathway heatmaps pointed towards expected inflammatory and immune pathways (e.g., IL18 signaling, TLR4 stimulation, T cell differentiation) as predictive signalling motifs of severe COVID-19. Five predictive drivers from the previous plasma proteomic experiments were found as predictive genes (MAPK9, TIMP1, JUN, IL6, TNFSF10). The other multi-omic predictive drivers were S100A12, CD63, LAMP2, BIRC2, HMOX1, LGALS1, NFATC1, IL10RA, ATP6AP2, CD4, ITGB1 (Figure 5B-C).

Lastly, we probed for the single-cell activity profile of various predictive drivers from the MGH-Mayo/MGH-Stanford/MGH-scMGH experiments. We discovered that the most active drivers in severe cases were JUN (B/T cells) and TIMP1 (all PBMCs except B cells and NKs). In contrast, in non-severe cases, it was PTEN (monocytes and platelets) and ACAA1 (all PBMCs but especially B cells). Like ACAA1, which opposed its proteomic counterpart, CKAP4 was also increased in non-severe cases (monocytes). Other active genes in all non-severe PBMCs were FLT3LG, BAX, LYN and TNFSF10, while NCF2 was mainly in severe monocytes (Figure 5D-E) (Supplementary Material 5).

Overall, these results elaborate on the cellular origins of certain predictive drivers for severe COVID-19 inferred by APNet in PBMCs and were attained through APNet’ noticeable versatility in bridging across-omic modalities.

### Benchmarking APNet against alternative ML/DL methods

To benchmark APNet’s significant performance on COVID-19 classification tasks, we initially retrieved from the literature the predictive models published by the authors of the MGH study (Filbin et al.), the Stanford study (Feyarts et al.), and of an independent study from Qatar which used the MGH study for independent validation. As shown in Table 1, APNet outperformed the MGH and Stanford models (Table 1). Although APNet showed similar performance to Qatar’s predictive model (AUC > 0.95, training-testing on the authors’ in-house data) in demarcating severe COVID-19 cases, it outperformed Qatar’s model in terms of generalizability. This was evident as the latter achieved an AUC of 0.79 when independently tested on the MGH study (Table 1).

**Table 1.**
 Published ML/DL analyzing MGH and Stanford Olink datasets


At this point, we performed more specific benchmarking experiments using (a) a variation of APNet where we provided only DEPs to the DL model instead of DAPs (PASNet-expression) and (b) an alternative variation where we substituted the PASNet architecture with one of the most widely used, explainable Machine Learning approaches like Random Forest (RF). The training, validation and testing datasets remained the same as before.

Noticeably, APNet outperformed all alternative DL/ML models based on activity or expression data regarding AUC and F1-score (Figure 6A - B). More specifically, the PASNet-expression model performed poorly on the Mayo dataset (AUC: 0.645, F1 score: 0.7475), and none of the predicted molecules were hidden drivers. Biological explainability indicated ground-truth biological pathways related to COVID-19 immunopathology were the most predictive pathways. However, some more nuanced pathways that APNet retrieved during the MGH-Mayo experiment were missing or under-represented (e.g., lipid imbalances) (Figure 6C-D).

![Figure 6.](content/575161v1_fig6.tif)

**Figure 6.:** (A) ROC curves depicting the performance of APNet and alternative approaches in classifying severe from non-severe cases in respective experiments. Distinct AUC scores are referenced also. (B) Lollipop plot depicting the F1-scores from each model from (A). (C-F) Barplots with SHAP values for the top 20 most predictive plasma proteins of COVID-19 severity and protein-pathway mapping from PASNet-expression model for MGH-Mayo experiment (C-D) and MGH-Stanford experiment (E-F). (G) Barplots with SHAP values showing top 20 most predictive drivers of severity based on the Random Forest (RF) alternative model for the various classification experiments. Class 0 refers to non-severe and Class 1 refers to severe COVID-19 cases.

The PASNet-expression model also under-performed in the Standford study compared to APNet, with an AUC of 0.89 and an F1-score of 0.54. Unsurprisingly, this expression-driven investigation in the Stanford study could only reveal a limited scope of predictive biological pathways like Cellular response to stress, positive regulation of intracellular signaling transduction, Neutrophil degradation, and viral protein response (Figure 6E-F).

The second alternative model based on Random Forest (RF) under-performed even more on Mayo and Stanford datasets than the previous one since the models were validated with AUC: 0.65, F1-score: 0.4746, and AUC: 0.7375, F1-score: 0.6486, respectively, for each dataset. Noticeably, the top-predictive proteins were almost identical across the Mayo and Stanford datasets analysis. Concerning the multi-omic experiment, we opted not to test the PASNet expression-driven model. This decision was based on the intrinsic sparsity of the scRNA-seq data’s expression and the apparent requirement for specific data harmonization or more advanced ML/DL manipulations, which were beyond the scope of our current project. Consequently, we exclusively employed the RF model on the shared perturbational space identified through activity analysis between plasma proteomics and scRNA-seq data. This approach underperformed compared to APNet, as evidenced by an AUC of 0.87 and an F1-score of 0.73 (Figure 6G).

With regards to associations with clinico-biological covariates, the most predictive proteins or drivers from the benchmarking studies exhibited correlations with COVID-19 severity but not to the extend that APNet’s results did (e.g., this is evident in the expression-PASNet MGH-Mayo/Stanford and the RF MGH-Stanford experiments). Furthermore, associations with diabetes and kidney disease were not as straightforward as in the case of APNet (Supplementary Figure 6-7) (Supplementary Material 6).

### In silico evaluation of APNet’s results based on COVID-19 curated prior knowledge

To evaluate the degree of COVID-19 ground truths that APNet and the other classification models recovered, we mapped each model’s top 20 most predictive proteins from the various experiments to the SIGNOR 3.0 COVID-19 Hallmark pathways (i.e. Virus Entry, Cytokine storm, Inflammation, Fibrosis, Apoptosis, Innate response to dsRNA, MAPK Activation, ER stress and Stress granules, https://signor.uniroma2.it/covid/). APNet’s most predictive drivers from the MGH-Mayo and the multi-omic experiments were considerably over-represented (1.5 to 2 fold) on the SIGNOR 3.0 COVID-19 Hallmark pathways than their counterparts from the PASNet-expression and RF models. Concerning the MGH-Stanford experiment, APNet and PASNet-expression exhibited almost an equal number of mappings but different in type, while the RF model was again significantly under-represented. In the case of MAPK activation, a cardinal pathway in COVID-19 pathobiology, APNet accomplished approximately twice as many mappings (8) as the expression-PASNet model (4), revealing higher robustness in connecting predictive drivers of severity with COVID-19 biological underpinnings (Table 2) (Supplementary material 7).

**Table 2.**
 Biological benchmarking of APNet vs PASNet Expression and RF-Activity.
The table measures the number of top-20 predictive drivers that were mapped to the respective SIGNOR 3.0 pathway networks, in each classification experiment (SIGNOR 3.0 COVID-19 Hallmarks).


### APNet enables the creation of weighted graph models for mechanistic hypotheses: The case of ACAA1

We postulated that combining SJARACNe co-expression networks, with pathways that APNet ingested as biological priors before classification tasks and the weights it assigned to them upon completion of demarcating severe COVID-19 could be helpful to in silico predict regulatory motifs and signaling patterns driving severe COVID-19.

To demonstrate this feature, we focused on the MGH-Mayo experiment, we assembled a multipartite graph of with driver-driver and driver-pathway connections and we sought to leverage information about ACAA1 (Acetyl-CoA Acyltransferase 1), which was one of the top 20 most predictive drivers, was designated as a hidden driver by our analysis and it was significantly hypo-active in severe PBMCs which suggested the its plasma proteomic signature derived from an alternative tissue or organ.

By retrieving the MGH SJARACNe SHAP graph (a series of small positive, coherent feedforward loops with NCF2, TIMP1, CKAP4 as sources, TNFRSF10B as a significant “sink” and FLT3 as the primary inhibitor), it was apparent that no obvious connection existed between ACAA1 and the other predictive drivers (Figure 7A). To validate the biological plausibility of the SJARACNe graph, the respective PPI network from STRINGdb was leveraged (interaction score > 0.4), indicating high interconnectivity for most of the predictive drivers. Interestingly, ACAA1 and CKAP4 remained unconnected (https://version-12-0.string-db.org/cgi/network?networkId=bmlgZrzN1Cex) (Figure 7B).

![Figure 7.](content/575161v1_fig7.tif)

**Figure 7.:** (A) SJARACNe co-expression (adj.pvalue<0.05 for MI calculation) directed network from APNet’s complex graph showing the interactions of the top 20 most predictive drivers of COVID-19 severity for the MGH-Mayo scenario. (B) STRINGdb network with (interaction score > 0.4) for the same severity drivers. (C) APNet’s complex graph after tSNE dimensionality reduction using the clusterMaker app in Cytoscape, based on the “liver” score from the TISSUES 2.0 database for each driver/node. The darkest colour denotes a higher liver-specific association. The most liver-specific cluster of drivers is designated within the circle (D) Part of APNet’s complex graph showing highly liver-specific drivers and connected pathways with high prognostic significance, based on their PASNet weights. (E) Lollipop plots showing the SFA scores from the OCSANA+ app in Cytoscape in each node, after signal propagation from SDC1, CKAP4 and HGF on the entire APNet complex graph. (F) Part of APNet’s complex graph showing shortest paths based on the PathLinker app in Cytoscape starting from CKAP4, SDC1 and HGF and extending towards ACAA1. Below, the STRINGdb equivalent PPI network (interaction score > 0.4) of the SDC1-KRT18-GRPEL1-ACAA1 path with intermediate nodes provided by STRINGdb, after k-means clustering.

Next, considering that ACAA1 is predominantly expressed in the liver based on our previous GTEx analysis, we took inspiration from representation learning (Zitnik et al., 2019) and performed dimensionality reduction on the APNet complex graph with the tSNE algorithm, looking for maximum variance in liver expression based on TISSUES 2.0 scores. A distinct cluster with highly liver-specific drivers was detected. To gain a better insight on them, we isolated their subgraph with their most prognostic connected pathways (PASNet weight > 0.5 and < -0.5). We detected a graph “island” which contained four highly predictive drivers of COVID-19 severity among other proteins (ACAA1, SDC1, HGF, CKAP4) and connected pathways involved Immune System signaling, neutrophil degranulation, MAPK signaling, chaperone activation (HSP90) and VEGF signaling (Figure 7C-D).

Based on these findings, we posited that there should be an underlying connection between ACAA1 and some of the other three predictive drivers of severity. We resorted to the OCSANA+ Cytoscape application to simulate signal propagation from SDC1, HGF and CKAP4 on the APNet complex graph. By calculating the Signal Flow Analysis (SFA, see Materials and Methods) metric, it became apparent that HGF and SDC1 signal propagation converged towards ACAA1 through various intermediate proteins. A similar effect on ACAA1 was not observed in the case of CKAP4, which did not appear to propagate any signal towards ACAA1 (Figure 7E).

To better elucidate these findings, we calculated the shortest paths from SDC1, HGF and CKAP4 towards ACAA1 using the PathwayLinker application on Cytoscape. When selecting the “additive weight method” for the MI score as edge weight, PathLinker highlighted 2 critical shortest paths: (a) a signaling cascade commencing from SDC1 and reaching ACAA1 through KRT18 and GRPEL1 and (b) an incoherent feed-forward loop starting from HGF and through inhibiting ICOSLG which activated PTPRS which inhibited ACAA1. The “unweighted method” in PathwayLinker returned the same results. Notwithstanding, when selecting the “probabilistic weight method” for the MI score as edge weight, PathwayLinker suggested a larger signaling cascade commencing from CKAP4, and extending through TRIAP1, LBR and GRPEL1 towards ACAA1 (Figure 7F).

To computationally validate these APNet shortest paths, we queried the STRINGdb database for the respective PPI networks. After 2 rounds of expansion, we retrieved a singular PPI network (14 nodes, 23 edges, https://version-12-0.string-db.org/cgi/network?networkId=b57tJ84II6T8), connecting SDC1, GRPEL1, KRT18 and ACAA1 which upon k-means clustering revealed three components relative to fatty-acid metabolism (ACAA1, ACOX1, HADHA, HSD17B4, EHHADH), mitochondrial protein transport (HSPA9, KRT18, KRT8, GRPEL1, TIMM44) and cell surface interactions (FN1, SDC1, SDCBP, FGF2). In the case of the other shortest paths, the corresponding STRINGdb queries required more than 5 cycles of expansion to produce PPI networks encompassing all drivers of interest (CKAP4: 55 nodes, 375 edges, https://version-12-0.string-db.org/cgi/network?networkId=bjbqEWsYzPw4; HGF: 44 nodes, 214 edges, https://version-12-0.string-db.org/cgi/network?networkId=bcT9lsyOCwJ7) (Sup. Figure 8).

Finally, as an additional step to assess the potential significance of these paths in a more COVID-19-specific biological context, we queried the BYCOVID19 data portal (https://www.covid19dataportal.org/) for the “COVID-19 association score” provided by the OpenTargets platform. SDC1 exhibited the highest score (0.555) with a considerable difference from some of the other drivers of severity (KRT18=0.05, LBR=0.004, CKAP4=0.006, HGF=0.025), confirming the biological prioritization of the SDC1-ACAA1 nascent connection that APNet uncovered (Supplementary Material 8-9).

## Discussion - Conclusion

In the current work, focusing on COVID-19 omics, we present APNet, a computational DL pipeline to elucidate complex biological motifs while classifying patients based on their clinical severity.

APNet is inspired by computational approaches modeling Gene Regulatory Networks (GRNs), which have been instrumental in discovering new interactions between biological entities and formulating novel scientific hypotheses. APNet combines some of the best practices in the field by combining an Information Theory model (SJARACNe algorithm) through a Bayesian scope (NetBID2/scMINER toolkits) (Delgado and Gómez-Vela, 2019) and a biologically-informed neural network with enhanced explainability (PASNet and SHAP values) for supervised patient clustering. The above bioinformatic tools have been shown independently to effectively discover potential biomarkers and druggable targets in diseases however, to the best of our knowledge, they have never been used as a unified pipeline for COVID-19 or any other disease type (Wang et al., 2021) (Ding et al., 2023) (Hao et al., 2018).

In our study, we utilized APNet to predict severe COVID-19 cases in three different Olink plasma proteomic datasets (MGH, Mayo, Stanford), and a complementary scRNA-seq study. APNet conducted biologically informed predictions using driver-pathway associations (KEGG, Reactome, GO:BP, Wikipathways) with remarkable robustness, outperforming alternative ML/DL approaches which either lacked (a) the activity transformations enabled by the NetBID2/scMINER toolkits (PASNet-expression model) or (b) the PASNet DL architecture (Random Forest classifications). Based on the biological explainability of each model (SHAP values, driver-pathway mapping with learning DL weights) and COVID-19 curated biological ground-truths (SINGOR COVID-19 pathway networks), evidently, APNet was able to better approximate the systemic nature of severe COVID-19 from the provided biological data. We posit that APNet performed so efficiently due to the sparse regularization of the hierarchical relationships of drivers and pathways after initial differential activity analysis. Hence, APNet was able to capture both well known but also more nuanced perturbations in severe COVID-19 (i.e., known drivers but also “hidden drivers” like ACAA1, FLT3) implicating several potential tissues of origin and a diverse repertoire of critical pathways. Indicatively, some of the most predictive drivers and pathways that APNet captured concerned apoptosis, dishevelled PI3K-Akt stimulation (FLT3/FLT3LG, PTEN, NTF4, KIT), neurodegeneration (EGFR, SEMAD4), cell differentiation (TNFSF11), neutrophil degranulation (ACAA1), lipid metabolism (TNFRSF10A), immune and interleukin signaling (CD63, TIMP1, JUN), T cell receptor signaling (BIRC2, NFATC1, CD4, IKBKG), oxidative phosphorylation (ATP6AP2). These signaling cascades and some of these drivers have already been implicated with COVID-19, which attests to APNet’s overall capacity to make biologically plausible predictions. (Basile et al., 2022; Chidambaram et al., 2022; Merad and Martin, 2020; Pistollato et al., 2022; Thompson et al., 2021). A paradigmatic case concerning the translational value of APNet’s findings was the implication of MAPK pathway in severe COVID-19 based on various drivers (e.g., MAPK9, AREG, KIT, JUN, FLT3LG). These drivers were not prioritized to the same extend as highly predictive by the alternative ML/DL models – if prioritized at all. This could explain in part why APNet surpassed these models as a classifier of COVID-19 severity since components of the MAPK pathway (sH-RAS, C-RAF, MAPK1, MAPK2 and ERK) have emerged as critical tenets of Sars-CoV-2 tropism in PBMCs and have been associated with adverse clinical covariates like hypoxia, dyspnoea and vascular damages (Cusato et al., 2023).

Finally, APNet extends beyond biological explainability to actionability regarding the formulation of mechanistic hypotheses, by providing the capacity to generate a weighted driver-pathway network that incorporates information from SJARACNe co-expression networks, the differential activity analysis, the PASNet DL clinical predictions and external dedicated bioinformatic databases like STRINGdb. APNet enabled through graph representation learning, shortest path detection, and signal propagation simulation the prediction of a liver-specific signaling cascade in severe COVID-19 involving ACAA1 (hidden driver with prognostic significance but no apparent connections to other predictive drivers), SDC1, KRT18, and GRPEL1. These predictions are not biologically implausible given the implication of SDC1 and KRT18 in inflammation and epithelial damage (Ghondaghsaz et al., 2023; Liao et al., 2020), the involvement of the mitochondrial GRPEL1 in host/Sars-CoV-2 interactions (Zhang et al., 2022), the clinical correlation of ACAA1 (a mediator of fatty acid oxidation in the mitochondria and the peroxisomes) with ICU-admittance in COVID-19 (Penrice-Randal et al., 2022) and a severe mitochondria dysfunction in the liver of severe COVID-19 cases (Guarnieri et al., 2023).

The work herein is not without its limitations. One limitation concerns the restricted number of studies involved and the binary assignment of drivers to pathways. Pathway activation is a dynamic process controlled by fluctuations in expression or activity changes of a protein or drivers, respectively. Outputs from more advanced pathway enrichment techniques like GSEA could be more instructive for the DL model to perform classifications more aptly. Another limitation is the need to perform several manual steps in APNet’s complex graphs to test hypotheses and leverage new insights, which might hinder data exploration and analysis. Another issue worth noting is that APNet does not include clinical covariates as clinical-biological priors, which could be addressed in the future by adopting in our pipeline the more clinically-oriented version of Cox-PASNet (Hao et al., 2019).

Overall, APNet is a robust pipeline that can simplify the extraction of intricate biological insights from complex biological data while also performing clinical predictions and testing mechanistic hypotheses. In vitro/in vivo validations should accompany future implementations of APNet to validate the pipeline’s true translational credibility. Additionally, APNet’s scalability to other multi-factorial disease-omic datasets (such as cancer and neurodegenerative diseases) should be explored along with its potential deployment in other computational tasks (like multi-omic data integration and interactions with knowledge graph pipelines).

## Supporting information
