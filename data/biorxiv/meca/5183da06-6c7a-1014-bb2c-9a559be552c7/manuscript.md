# Genetic analysis of amyotrophic lateral sclerosis identifies contributing pathways and cell types

## Authors

- Sara Saez-Atienzar<sup>1</sup> ([ORCID: 0000-0002-1524-9584](https://orcid.org/0000-0002-1524-9584)) †
- Sara Bandres-Ciga<sup>2</sup>
- Rebekah G. Langston<sup>4</sup>
- Jonggeol J. Kim<sup>2</sup>
- Shing Wan Choi<sup>5</sup>
- Regina H. Reynolds<sup>6</sup>
- Yevgeniya Abramzon<sup>1</sup>
- Ramita Dewan<sup>1</sup>
- Sarah Ahmed<sup>10</sup>
- John E. Landers<sup>11</sup>
- Ruth Chia<sup>1</sup>
- Mina Ryten<sup>7</sup>
- Mark R. Cookson<sup>4</sup> ([ORCID: 0000-0002-1058-3831](https://orcid.org/0000-0002-1058-3831))
- Michael A. Nalls<sup>2</sup>
- Adriano Chiò<sup>13</sup> ([ORCID: 0000-0001-9579-5341](https://orcid.org/0000-0001-9579-5341))
- Bryan J. Traynor<sup>1</sup>

### Affiliations

1. Neuromuscular Diseases Research Section, Laboratory of Neurogenetics, National Institute on Aging, National Institutes of Health Bethesda, MD 20892 USA
2. Molecular Genetics Section, Laboratory of Neurogenetics, National Institute on Aging, National Institutes of Health Bethesda, MD 20892 USA
3. Instituto de Investigación Biosanitaria de Granada (ibs.GRANADA) Granada Spain
4. Cell Biology and Gene Expression Section, Laboratory of Neurogenetics, National Institute on Aging, National Institutes of Health Bethesda, MD 20892 USA
5. Department of Genetics and Genomic Sciences, Icahn School of Medicine Mount Sinai, 1 Gustave L. Levy Pl, New York City, NY 10029 USA
6. Department of Neurodegenerative Disease, UCL Queen Square Institute of Neurology, University College London London UK
7. NIHR Great Ormond Street Hospital Biomedical Research Centre, University College London London UK
8. Great Ormond Street Institute of Child Health, Genetics and Genomic Medicine, University College London London UK
9. Sobell Department of Motor Neuroscience and Movement Disorders, University College London, Institute of Neurology London UK
10. Neurodegenerative Diseases Research Unit, Laboratory of Neurogenetics, National Institute of Neurological Disorders and Stroke, National Institutes of Health Bethesda, MD 20892 USA
11. Department of Neurology, University of Massachusetts Medical School Worcester, MA 01605 USA
12. Data Tecnica International Glen Echo, MD 20812 USA
13. ‘Rita Levi Montalcini’ Department of Neuroscience, University of Turin Turin Italy
14. Azienda Ospedaliero Universitaria Città della Salute e della Scienza Turin Italy
15. Department of Neurology, Johns Hopkins University Baltimore, MD 21287 USA

† Corresponding author

## Abstract

ABSTRACT
Despite the considerable progress in unraveling the genetic causes of amyotrophic lateral sclerosis (ALS), we do not fully understand the molecular mechanisms underlying the disease. We analyzed genome-wide data involving 78,500 individuals using a polygenic risk score approach to identify the biological pathways and cell types involved in ALS. This data-driven approach identified multiple aspects of the biology underlying the disease that resolved into broader themes, namely neuron projection morphogenesis, membrane trafficking, and signal transduction mediated by ribonucleotides. We also found that genomic risk in ALS maps consistently to GABAergic cortical interneurons and oligodendrocytes, as confirmed in human single-nucleus RNA-seq data. Using two-sample Mendelian randomization, we nominated five differentially expressed genes (ATG16L2, ACSL5, MAP1LC3A, PLXNB2, and SCFD1) within the significant pathways as relevant to ALS. We conclude that the disparate genetic etiologies of this fatal neurological disease converge on a smaller number of final common pathways and cell types.

## INTRODUCTION

Amyotrophic lateral sclerosis (ALS, OMIM #105400) is a fatal neurological disease characterized by progressive paralysis that leads to death from respiratory failure typically within three to five years of symptom onset. Approximately 6,000 Americans and 11,000 Europeans die of the condition annually, and the number of ALS cases will increase dramatically over the next two decades, mostly due to aging of the global population (1).

Identifying the genes underlying ALS has provided critical insights into the cellular mechanisms leading to neurodegeneration, such as protein homeostasis, cytoskeleton alterations, and RNA metabolism (2). Additional efforts based on reductionist and high-throughput cell biology experiments have implicated other pathways, such as endoplasmic reticulum stress (3), nucleocytoplasmic transport (4), and autophagy defects (5). Despite these successes, our knowledge of the biological processes involved in ALS is incomplete, especially for the sporadic form of the disease.

To address this gap in our knowledge, we systematically applied polygenic risk score analysis to a genomic dataset involving 78,500 individuals to distinguish the cellular processes driving ALS. In essence, our polygenic risk score strategy determines whether a particular pathway participates in the pathogenesis of ALS by compiling the effect of multiple genetic variants across all of the genes involved in that pathway. This approach relies solely on genetic information derived from a large cohort and tests all known pathways in a data-driven manner. As such, it provides prima facie evidence of the cellular pathways responsible for the disease. Knowledge of the cell types involved in a disease process is an essential step to understanding a disorder. Recognizing this, we extended our computational approach to identify the specific cell types that are involved in ALS. To ensure accessibility, we created an online resource so that the research community can explore the contribution of the various pathways and cell types to ALS risk (https://lng-nia.shinyapps.io/ALS-Pathways/).

## RESULTS

### Pathway analysis used a three-stage study design

Overall, we evaluated the involvement of 7,347 pathways in the pathogenesis of ALS using a polygenic risk score approach (see Fig. 1A for the workflow of our analysis). To ensure the accuracy of our results, we divided the available ALS genomic data into three sections. The first of these independent datasets (hereafter known as the reference dataset) was a published genome-wide association study (GWAS) involving 12,577 ALS cases and 23,475 controls (6). We used the summary statistics from this reference dataset to define the weights of the risk allele so that greater importance was given to alleles with higher risk estimates.

![Figure 1.](content/211276v1_fig1.tif)

**Figure 1.:** Polygenic risk score analysis was used to identify (A) biological pathways and (B) cell types contributing to the risk of developing ALS. sNUC dataset was generated in house. DroNc-seq was obtained from Habid et al., 2017. sNUC-seq, single nuclei RNA sequencing; DroNc-seq, droplet single-nucleus RNA-sequencing.

These risk allele weights were then applied to our second dataset (also known as the training dataset) to generate a polygenic risk score estimate for each biological pathway. This training data consisted of individual-level genotype and phenotype data from 5,605 ALS cases and 24,110 control subjects that were genotyped in our laboratory (7). We investigated the pathways defined by the Molecular Signatures Database, a compilation of annotated gene sets designed for gene set enrichment and pathway analysis. We focused our efforts on three collections within the Molecular Signatures Database that have been previously validated (8, 9). These were the hallmark gene sets (containing 50 pathways), the curated gene sets (1,330 pathways), and the gene ontology gene sets (5,967 pathways).

To ensure the accuracy of our results and control for type I error, we attempted replication of our findings in an independent cohort. For this, we used our third independent dataset (also known as the replication dataset) consisting of individual-level genotype and phenotype data from 2,411 ALS cases and 10,322 controls that were also genotyped in our laboratory (7). The pathways that achieved significance in the training dataset (defined as a false discovery rate (FDR)-corrected p-value < 0.05) were selected for replication. Then, we report the pathways that achieved significance in the replication dataset (defined as a raw p-value < 0.05). We estimated the replication cohort’s power to be 98% based on the sample set size, the variance explained by the genetic markers in the training dataset, and the number of independent SNPs with a p-value < 0.05.

We applied a similar polygenic risk score approach to determine which cell types are associated with the ALS disease process (Fig. 1B). In essence, a cell type associated with a disease will display a pattern whereby more of the variance of the polygenic risk score is attributable to genes specifically expressed in that cell type. We applied a linear model to detect this pattern in our ALS data, using a p-value of less than 0.05 as the significance threshold. This strategy has become a standard approach for this type of analysis (10).

### Biological pathways driving the risk of ALS

We calculated the contribution to ALS risk of 7,347 gene sets and pathways listed in the Molecular Signature Database (SI Appendix, Fig. S1). This genome-wide analysis identified thirteen biological processes, twelve cellular component pathways, and two molecular function pathways with a significant risk associated with ALS in the training data (SI Appendix, Table S1). We independently confirmed a significant association with ALS risk in thirteen of these pathways in our replication cohort. These pathways included (i) seven biological processes, namely cell morphogenesis involved in neuron differentiation, neuron development, cell morphogenesis involved in differentiation, cell part morphogenesis, cellular component morphogenesis, cell development, and cell projection organization (Fig. 2A, Table 1); (ii) four cellular components, namely autophagosome, cytoskeleton, nuclear outer membrane endoplasmic reticulum (ER) membrane network, and cell projection (Fig. 2B, Table 1), and (iii) two molecular function terms, namely ribonucleotide binding and protein N-terminus binding (Fig. 2C, Table 1).

**Table 1.**
 Pathways that were significantly associated with ALS based on polygenic risk score analysis after replication.
Beta estimates, standard errors, and p-values are after Z-transformation. SE, standard error; BP, biological process; CC, cellular component; MF, molecular function


![Figure 2.](content/211276v1_fig2.tif)

**Figure 2.:** The Forest plots show polygenic risk score estimates in the replication cohort for the (A) biological processes, (B) cellular components, and (C) molecular function pathways that were significant in the training cohort. The blue squares represent the significant terms in both the training and replication datasets. The heatmaps depict semantic similarity calculated by GOSemSim among the significant (D) biological processes, (E) cellular components, and (F) molecular function. The REVIGO algorithm was used to obtain the cluster representatives. The Forest plot displays the distribution of beta estimates across pathways with the horizontal lines corresponding to 95% confidence intervals. Beta estimates for the polygenetic risk score are after Z transformation.

### Pathways central to ALS risk

There is significant functional overlap among the thirteen pathways that we identified as significantly associated with ALS risk. We sought to more broadly summarize the significant pathways by removing redundant terms. To do this, we computed semantic similarity that is a measure of the relatedness between gene ontology terms based on curated literature. We used the REVIGO algorithm to obtain cluster representatives (11). Overall, our results resolved into three central pathways as being involved in the pathogenesis of ALS, namely neuron projection morphogenesis, membrane trafficking, and signal transduction mediated by ribonucleotides (Fig. 2D-F, SI Appendix, Fig S2).

### Pathway analysis among patients carrying the pathogenic C9orf72 repeat expansion

We found that the C9orf72 gene was a member of two of our thirteen significant pathways, namely the autophagosome and the cytoskeleton pathways. We explored whether C9orf72 was the main driver of these pathways. To do this, we calculated the polygenic risk score associated with these two pathways in C9orf72 expansion carriers compared to healthy individuals, and non-C9orf72 carriers compared to healthy individuals. These cohorts consisted of 667 patients diagnosed with ALS who were C9orf72 expansion carriers, 7,040 patients with ALS who were non-carriers, and 34,232 healthy individuals.

Our analysis revealed that the cytoskeleton pathway remained significantly associated with ALS risk in C9orf72 expansion carriers and non-carriers. This finding indicated that this critical biological process is broadly involved in ALS’s pathogenesis (Fig. 3B). In contrast, only C9orf72 expansion carriers showed significant risk in the autophagosome genes (Fig. 3A), indicating that the C9orf72 locus mostly drives this pathway’s involvement in the pathogenesis of ALS and points to an autophagy-related mechanism underlying C9orf72 pathology.

![Figure 3.](content/211276v1_fig3.tif)

**Figure 3.:** The polygenic risk scores associated with (A) autophagosome and (B) cytoskeleton in ALS C9orf72 expansion carriers (n = 667) compared to healthy subjects (n = 34,232), and ALS non-carriers (n = 7,040) compared to healthy subjects (n = 34,232) are shown in this figure. The upper panels depict the cumulative genetic risk score for each group. The lower panel shows the forest plots of the beta estimates with 95% confidence intervals. Beta estimates are based on the Z-score scale. Genetic risk score mean comparisons from the ALS-non-carriers group compared to the ALS-C9orf72 carriers via t-test are summarized by asterisks with * denoting a two-sided mean difference at p-value < 0.05.

### ALS polygenic risk is due to genes other than known risk loci

We also examined the contributions of the five genetic risk loci known to be associated with ALS. These loci include TNIP1, C9orf72, KIF5A, TBK1, and UNC13A (7). To do this, we added these five loci as covariates in the analysis of the replication cohort. Our data shows that autophagosome and cell projection were no longer significant. However, the other eleven pathways were still associated, suggesting that there are risk variants contributing to the risk of ALS within these eleven pathways that remain to be discovered (SI Appendix, Table S2).

### Mendelian randomization nominates genes relevant to ALS pathogenesis

Most of the variants associated with a complex trait overlap with expression quantitative trait loci (eQTL), suggesting their involvement in gene expression regulation (12). We applied two-sample Mendelian randomization within the thirteen significant pathways (shown in Table 1) to integrate summary-level data from a large ALS GWAS (7) with data from cis-eQTLs obtained from previous studies in blood (13) and brain (14)(15)(16)(17). This approach identifies genes whose expression levels are associated with ALS because of a shared causal variant. We used multiple SNPs belonging to the thirteen significant pathways as instruments, gene expression traits as exposure, and the ALS phenotype as the outcome of interest (Fig. 4A). Our analyses identified five genes whose altered expression was significantly associated with the risk of developing ALS. These were ATG16L2, ACSL5, MAP1LC3A, PLXNB2, and SCFD1 within blood (SI Appendix, Table S3). Additionally, SCFD1 was significantly associated with ALS in brain-derived tissue (Fig. 4B)

![Figure 4.](content/211276v1_fig4.tif)

**Figure 4.:** (A) A schematic representation of the parameters used for the analysis. (B) The Forest plots display the beta estimates with the 95% confidence intervals shown as horizontal error bars. The grid on the left indicates the pathway to which the gene belongs.

### Cell types involved in the pathogenesis of ALS

We leveraged our large GWAS dataset to determine which cell types participate in the pathological processes of ALS. To do this, we generated a single-nucleus RNA-seq (sNuc-seq) dataset using the human frontal cortex collected from sixteen healthy donors. Each cell was assigned to one of thirty-four specific cell types based on the clustering of the single-nucleus RNA-seq data (Fig.5 A, B). We then determined a decile rank of expression for the thirty-four cell types based on the specificity of expression. For instance, the TREM2 gene is highly expressed only in microglia. Thus, the specificity value of TREM2 in microglia is close to 1 (0.87), and it is assigned to the tenth decile for this cell type. In contrast, the POLR1C gene is expressed widely across tissues. Consequently, it has a specificity value of 0.007, and it is assigned to the fourth decile of microglia and a similar low decile across other cell types.

The premise of this type of analysis is that, for a cell type associated with a disease, more of the variance explained by the polygenic risk score estimates will be attributable to the genes more highly expressed in that cell type. To test this hypothesis, we applied linear regression models to detect a trend of increased variance with the top deciles, a pattern indicating that a particular cell type is involved in the pathogenesis of ALS (10). This approach identified two subtypes of cortical GABAergic interneurons (PVALB and TOX-expressing neurons; and ADARB2 and RELN-expressing neurons) and oligodendrocytes (OPALIN, FCHSD2, and LAMA2 -expressing oligodendrocytes) as associated with ALS risk (Fig. 5, C).

![Figure 5.](content/211276v1_fig5.tif)

**Figure 5.:** (A) Unsupervised UMAP clustering identifies thirty-four cell types in the human cortex. (B) Heatmap representing the gene expression per cluster. (C) The y-axis corresponds to the phenotypic variance explained by the polygenic risk score (pseudo-R2), and the x-axis depicts deciles 1 to 10. The color pictures show the significant cell types and the p-values of the linear regression fit models. The semitransparent pictures show the cell types that were not significantly associated with the disease. The regression line depicts the association between PRS.R2 (pseudo R2, adjusted by prevalence) and the specificity decile in each cell type. The grey shading shows the 95% confidence interval of the regression model. Astrocyte (AST), endothelial cell (EC), excitatory neuron (ExN), inhibitory neuron (InN), microglia (MGL), oligodendrocyte (ODC), oligodendrocyte precursor (OPC).

To confirm these findings, we used an independent dataset consisting of droplet single-nucleus RNA-seq (DroNc-seq) from the human cortex and hippocampus obtained from five healthy donors (18). Our modeling in this second human dataset confirmed our previous findings: PVALB-expressing GABAergic neurons and oligodendrocytes were significantly enriched in ALS risk (see SI Appendix, Fig. S3).

Finally, we attempted to replicate our findings in a well-validated dataset based on single-cell RNA-seq (scRNA-seq) data obtained from mouse brain regions (10). The advantage of this nonhuman dataset is that it is based on single-cell RNA-seq, a difficult technique to apply to human neurons, but which captures transcripts missed by single-nucleus RNA-seq that may be important for neurological disease (10). Like the human data, cortical parvalbuminergic interneurons again showed enrichment in ALS risk using the mouse dataset (see SI Appendix, Fig. S4). Oligodendrocytes were not significantly associated with ALS in the mouse superset. However, this is likely related to the depletion of the oligodendroglia lineage in the single-cell RNA-seq data, a known issue with this technology(10).

## DISCUSSION

A striking aspect of our analysis is that it identified a relatively small number of biological pathways as central to the pathogenesis of ALS. Considering the clinicopathological and genetic heterogeneity across ALS, the finding of such a small quantity of universal themes is unexpected. Our results illustrate how multiple unrelated genetic causes can lead to a similar downstream outcome, namely motor neuron degeneration. Unraveling how disruption of these three fundamental biological processes predisposes to ALS may yield therapeutic targets that are effective across all patients with ALS.

The importance of membrane trafficking in ALS has been widely reported (19). In contrast, even though neuronal outgrowth has been explored in ALS (20), our identification of genetic risk underlying neuronal morphogenesis was novel. Indeed, the combination of membrane trafficking and neuronal morphogenesis may be a driving force of the disease pathogenesis. The defining feature of motor neurons is the length of their axons, projections that require specialized long-range transport and efficient cytoskeletal dynamics for the maintenance of synaptic connections (21). Similarly, signal transduction mediated by ribonucleotides is a broad term encompassing ion channel transport that regulates signal transmission at synapses. Disruption of this process leads to hyperexcitability, a phenomenon that has been observed in ALS patients (22). We speculate that broadly expressed genes lead to selective damage due to the high reliance of motor neurons on cellular transport, morphogenesis, and axonal ion channels compared to other cell types.

Our data did not detect biological pathways that have been previously implicated in the pathogenesis of familial ALS, such as nucleocytoplasmic transport (23) and excitotoxicity (24). These cellular processes may only operate in specific genetic forms of ALS, such as C9orf72-related or SOD1-related cases. A more likely explanation is that rare and low-frequency variants not captured by our methodology, significantly contribute to those pathways. For this reason, we cannot rule these biological processes out as relevant to the pathogenesis of ALS. Future analyses of more substantial datasets that include whole-genome sequencing data may implicate them.

One of our study’s strengths is that we were able to distinguish differential pathways operating in C9orf72 expansion carriers versus non-carriers. Interestingly, the autophagosome pathway was only significant in the analysis of the C9orf72 expansion carriers. The C9orf72 protein is a known regulator of autophagy; hence it is not surprising that a higher burden of ALS genetic risk was found within autophagy genes in C9orf72 expansion carriers versus non-carriers. This is the first time that autophagy-related processes have been implicated in C9orf72 biology from a genetic perspective. The hexanucleotide repeat expansion is known to influence the expression of the C9orf72 gene, irrespective of reported biology involving dipeptide repeats and toxic RNA species arising directly from the repeat expansion (25), which reinforces the importance of our findings. The C9orf72 protein was also recently found to play a role in neuronal and dendritic morphogenesis in ALS through the promotion of autophagy (26).

Our rigorous approach using multiple human and mouse transcriptome datasets identified cortical GABAergic interneurons and oligodendrocytes as the cell types central to ALS. These findings are consistent with published literature. For example, alteration in inhibitory signaling through GABAergic interneurons contributes to neural hyperexcitability, an early event in ALS pathogenesis (22). Oligodendrocytes from sporadic and familial SOD1 ALS exert a harmful effect on motor neurons through the secretion of toxic factors (27). Even though these cell types were previously linked with toxicity in ALS, our study indicates that oligodendrocytes incorporate a significant proportion of ALS genetic risk. This initial finding supports the idea that these cells directly contribute to the disease pathogenesis, rather than merely playing a secondary role in the disease progression.

Our results show the power of data-driven approaches to nominate aspects of the nervous system for additional scrutiny. Nevertheless, our study has limitations. Though we analyzed 78,500 individuals in the current study, our power to detect pathways remains limited. This lack of power primarily stems from the genetic architecture of ALS, which is known to conform to the rare disease-rare variant paradigm (28). By design, pathway analysis focuses on common variants with a frequency greater than 1%, but we know that the contribution of common variants to ALS risk is modest (6). Furthermore, our approach is based on intragenic variants, even though intergenic mutations can affect gene expression. We have overcome this power limitation by performing multiple rounds of replication in both the pathway analysis and cell type analysis to ensure accuracy and validity. The detected pathways and cell types represent potent aspects of the ALS disease process, but additional critical cellular mechanisms will undoubtedly be found using more extensive datasets.

Another limitation is the Molecular Signatures Database that we used to define the pathways in our analysis. This collection is incomplete, especially for neuronal and glial pathways (29). As our understanding evolves and more single-cell expression datasets become available, it may be worthwhile to reevaluate our GWAS data periodically. To facilitate this, we have made the programming code needed to perform the analysis publicly available. We also created an interactive, online resource that enables the research community to explore the contribution of pathways and cell types to ALS risk (https://lng-nia.shinyapps.io/ALS-Pathways/).

In conclusion, we demonstrate the utility of data-driven approaches to dissect the molecular basis of complex diseases such as ALS. Our stringent approach points to neuron projection morphogenesis, membrane trafficking, and signal transduction mediated by ribonucleotides as primary drivers of motor neuron degeneration in ALS. It also nominates cortical GABAergic interneurons and oligodendrocytes as central to the pathogenesis of this fatal neurological disease.

## Supporting information
