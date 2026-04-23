Single-cell transcriptomic analyses provide insights into the developmental origins of neuroblastoma | Nature Genetics
Skip to main content
Thank you for visiting nature.com. You are using a browser version with limited support for CSS. To obtain the best experience, we recommend you use a more up to date browser (or turn off compatibility mode in Internet Explorer). In the meantime, to ensure continued support, we are displaying the site without styles and JavaScript.
Advertisement
View all journals
Search
Log in
Content Explore content
About the journal
Publish with us
Sign up for alerts
RSS feed
nature
nature genetics
articles
Single-cell transcriptomic analyses provide insights into the developmental origins of neuroblastoma
Published: 25 March 2021
Single-cell transcriptomic analyses provide insights into the developmental origins of neuroblastoma
Selina Jansky ORCID: orcid.org/0000-0003-4227-0298 1 , 2 , 3 ,
Ashwini Kumar Sharma ORCID: orcid.org/0000-0001-7883-7888 4 ,
Verena Körber 5 ,
Andrés Quintero ORCID: orcid.org/0000-0002-3959-805X 4 , 3 ,
Umut H. Toprak 1 , 2 ,
Elisa M. Wecht 1 , 2 ,
Moritz Gartlgruber 1 , 2 ,
Alessandro Greco 5 , 3 ,
Elad Chomsky 6 ,
Thomas G. P. Grünewald ORCID: orcid.org/0000-0003-0920-7377 1 , 7 , 8 ,
Kai-Oliver Henrich 1 , 2 ,
Amos Tanay ORCID: orcid.org/0000-0001-9419-3824 6 ,
Carl Herrmann 4 ,
Thomas Höfer ORCID: orcid.org/0000-0003-3560-8780 5 &
…
Frank Westermann ORCID: orcid.org/0000-0003-1584-3636 1 , 2
Nature Genetics volume 53 , pages 683–693 ( 2021 ) Cite this article
32k Accesses
284 Citations
60 Altmetric
Subjects
Cancer
Developmental biology
Abstract
Neuroblastoma is a pediatric tumor of the developing sympathetic nervous system. However, the cellular origin of neuroblastoma has yet to be defined. Here we studied the single-cell transcriptomes of neuroblastomas and normal human developing adrenal glands at various stages of embryonic and fetal development. We defined normal differentiation trajectories from Schwann cell precursors over intermediate states to neuroblasts or chromaffin cells and showed that neuroblastomas transcriptionally resemble normal fetal adrenal neuroblasts. Importantly, neuroblastomas with varying clinical phenotypes matched different temporal states along normal neuroblast differentiation trajectories, with the degree of differentiation corresponding to clinical prognosis. Our work highlights the roles of oncogenic MYCN and loss of TFAP2B in blocking differentiation and may provide the basis for designing therapeutic interventions to overcome differentiation blocks.
You have full access to this article via California Institute of Technology .
Similar content being viewed by others
Single-nuclei transcriptomes from human adrenal gland reveal distinct cellular identities of low and high-risk neuroblastoma tumors
Article Open access 07 September 2021
Comparison of human pluripotent stem cell differentiation protocols to generate neuroblastoma tumors
Article Open access 04 October 2024
Simultaneous single-nucleus RNA sequencing and single-nucleus ATAC sequencing of neuroblastoma cell lines
Article Open access 07 November 2024
Main
Neuroblastoma is the most common extracranial solid tumor in early childhood 1 . Tumors are grouped into high-risk neuroblastomas, harboring the amplified MYCN oncogene, rearrangements of the TERT locus or alternative lengthening of telomeres and intermediate or low-risk tumors lacking telomere maintenance 2 , 3 , 4 . Neuroblastomas also harbor recurrent mutations in ALK 5 , 6 . Furthermore, two types of neuroblastoma cells, undifferentiated mesenchymal cells and committed adrenergic cells, can be distinguished based on their transcriptomic and epigenetic profiles 7 , 8 . Neuroblastomas arise most frequently in the adrenal gland and sympathetic ganglia and are thought to originate from neural crest-derived precursor cells of sympathetic neurons and adrenal chromaffin cells during development 9 , 10 . However, a recent study of the developing adrenal gland in mice called this concept into question since it did not find a common progenitor of sympathetic neurons and adrenal chromaffin cells and thus suggested an early split of the two lineages 11 . Still, studies on human adrenal gland development, which may shed light on the cellular origin of neuroblastoma, are lacking.
In this study, we defined the cell types in the developing adrenal medulla and their lineage trajectories during various stages of embryonic and fetal development using single-nucleus RNA sequencing (snRNA-seq) and compared them to neuroblastoma cell transcriptomes to elucidate the developmental programs and cell types resembling childhood neuroblastoma.
Results
Cellular diversity in the developing human adrenal gland
To examine the molecular features of cells during normal development of the human adrenal gland, where most neuroblastomas arise, we studied 17 fresh-frozen human adrenal glands spanning 7 developmental time points by droplet-based snRNA-seq (Fig. 1a and Supplementary Table 1 ). The developmental time points covered Carnegie stages CS18 and CS19, corresponding to 7 weeks postconception and CS20 and CS23, corresponding to 8 weeks postconception, which is shortly after the first neural crest-derived cells appear in the adrenal anlage, and further time points during the maturation of adrenal medullary cells until 17 weeks postconception. During this time, the adrenal medulla has been described to comprise neural crest-derived progenitors, neuroblasts and chromaffin cells and later also sympathetic ganglion cells 12 , 13 , 14 , 15 . Presence of chromaffin cells and neuroblasts inside the analyzed adrenal glands was confirmed by immunohistochemical staining for the neuroblast markers ALK and ISL1 and the chromaffin cell marker CHGA (Extended Data Fig. 1a,b ). After quality control, we clustered all cells and assigned them to major cell types (Fig. 1b , Extended Data Fig. 2a and Supplementary Tables 2 – 4 ). Within major cell types, cells co-clustered by developmental time point but not by individual sample (Extended Data Fig. 2b,c ). This cell atlas of adrenal gland development comprised CYP11A1 + adrenal cortical cells, PTPRB + endothelial cells, COL1A1 + mesenchymal cells, ACTA2 + myofibroblasts, ALB + hepatocytes, PAX7 + muscle progenitor cells, MYH3 + myocytes, PTPRC + immune cells, HBA2 + erythrocytes, SOX10 + neural crest-derived progenitors termed Schwann cell precursors (SCPs), ISL1 + neuroblasts and DBH + chromaffin cells (Extended Data Fig. 2d ). Most cell types were found across all time points, except for small numbers of cells that were probably derived from neighboring tissue and hence restricted to individual samples, including hepatocytes and myocytes (Fig. 1b and Extended Data Fig. 2c ). To focus on adrenal medullary cells, the presumed origin of neuroblastoma, in more depth, we selected and re-embedded the transcriptomes of SCPs, chromaffin cells and neuroblasts (Fig. 1c and Extended Data Fig. 2e,f ). SCPs were marked by the expression of CDH19 , SOX10 , PLP1 and ERBB3 and split into a cluster comprising cells from 7 and 8 weeks postconception and a cluster comprising cells from later time points (11, 14, 17 weeks postconception; late SCPs) (Fig. 1d,e and Supplementary Table 5 ). Expression of the chromaffin markers TH , DBH, DDC and CHGA marked adrenal chromaffin cells. Chromaffin cells from later developmental time points formed a distinct cluster harboring cells that additionally expressed PNMT , encoding the enzyme catalyzing methylation of norepinephrine to form epinephrine (Fig. 1e ). An ERBB4 + , ASCL1 + bridge population connected SCPs and chromaffin cells. Expression of the neuroblast markers NEFM , GAP43 , STMN2 , ISL1 and ALK identified sympathetic neuroblasts. At later time points, neuroblasts showed increased expression of the differentiation markers SYN3 and IL7 , whereas expression of the early neuroblast marker ALK declined. A cell population, which we termed connecting progenitor cells, spanned the transcriptional space between bridge, chromaffin and neuroblast populations. These cells expressed sympathoadrenal markers but at lower levels than chromaffin cells and neuroblasts. Importantly, connecting progenitor cells and bridge cells were almost exclusively derived from samples at 7 and 8 weeks postconception, indicating that they are transient populations in development (Fig. 1f ). Hence, individual samples from 7 and 8 weeks postconception showed connections between all medullary cell populations (Fig. 1g and Extended Data Fig. 2g ), while the populations were completely separated at later developmental time points (Fig. 1h and Extended Data Fig. 2g ). Remarkably, neuroblasts and SCPs harbored distinct subpopulations of cycling cells, marked by the expression of MKI67 and TOP2A , whereas no such population was present in chromaffin or bridge cells (Fig. 1c,e ). Quantification of cells in cell cycle phases showed that SCPs and neuroblasts have a high proliferative capacity harboring 50 and 60% of actively cycling (non-G 1 ) cells, respectively, while in bridge and chromaffin cell populations only 25 and 20% of cells were cycling (Extended Data Fig. 2h ). To analyze the localization of medullary cell types inside the developing adrenal gland, we used single-molecule RNA FISH for the neuroblast marker ISL1 , chromaffin marker TH , bridge marker ASCL1 and SCP marker ERBB3 . Single SCPs were located inside nests of neuroblasts and in close proximity to small groups of chromaffin cells surrounding these nests, consistent with SCPs giving rise to neuroblasts and chromaffin cells (Fig. 1i,j ). ASCL1 + bridge cells were detected in adrenal glands at 8 weeks postconception but not at 14 weeks postconception, further supporting their transient nature in development (Extended Data Fig. 2i ).
Fig. 1: Cell types in the developing human adrenal gland.
The alternative text for this image may have been generated using AI.
Full size image
a , Schematic illustration of human adrenal medulla development with the time points of sample collection marked. b , UMAP embedding of 100,337 single cells derived from developing human adrenal glands. Clusters of transcriptionally similar cells are colored and labeled by major cell type. c , UMAP plot of adrenal medullary cells ( n = 10,739) with cells colored and labeled by cell population. d , UMAP visualization illustrating cells from c colored by developmental time point. e , Heatmap depicting the relative expression of marker genes for adrenal medullary cell populations as in c . Normalized expression is shown as a z -score. f , Bar plot showing the adrenal medullary cell type fractions at each individual developmental time point. g , h , Labeled UMAP representations of adrenal medullary cells from two individual adrenal glands at CS20/8 weeks postconception ( g ) and 17 weeks postconception ( h ) with the colors and labels indicating the cell populations. i , j , RNAscope FISH for the SCP marker ERBB3 , neuroblast marker ISL1 and chromaffin marker TH in human adrenal glands at CS23/8 weeks postconception ( i ) and 14 weeks postconception ( j ). The representative results for two out of four samples analyzed in independent experiments with similar results are shown. The left panels show composite overviews over the entire glands, while the boxes mark the regions of the insets shown on the right.
Source data
Differentiation dynamics during adrenal medulla development
To investigate the putative developmental relationships between adrenal medullary cell types, we applied pseudotime analysis based on diffusion distance, thus linking cell types by a branching trajectory that traces graded transcriptomic changes (Fig. 2a ). To identify the starting point of the differentiation trajectory in an unbiased way, we estimated the differentiation potential (‘stemness’) of single adrenal medullary cells based on their signaling entropy and transcriptional diversity. SCPs showed the highest stemness and therefore were placed at the root of the adrenal medullary differentiation hierarchy (Fig. 2b and Extended Data Fig. 3a–f ). SCPs gave rise to three major lineages: chromaffin cells; sympathetic neuroblasts; and late SCPs (Fig. 2c,d and Extended Data Fig. 3g,h ). The chromaffin and neuroblast trajectories shared differentiation of SCPs to connecting progenitor cells via the bridge population, which also displayed high stemness (Fig. 2b ), and subsequently bifurcated, indicating that neural crest-derived SCPs are common progenitors of chromaffin cells and sympathetic neuroblasts in the human adrenal medulla. Bifurcation of the trajectories at connecting progenitor cells into neuroblasts and chromaffin cells and differentiation of SCPs into late SCPs was further supported by RNA velocity (Fig. 2e ). We then identified genes significantly associated with these trajectories (Fig. 2f and Supplementary Table 6 ). In addition to known markers of adrenal medullary cell types (Fig. 2g ), the analysis identified transcription factors that mark cell type transitions. While PHOX2B was expressed during SCP to bridge transition, HAND2 was expressed starting in the bridge population and GATA3 late during bridge to neuroblast transition (Fig. 2f and Extended Data Fig. 3i ). Expression of the cell cycle inhibitor CDKN1C was specific to chromaffin cells, while CCND1 , which encodes a promoter of cell cycle transition, was expressed in the neuroblast lineage. The expression patterns of these regulators are consistent with the diverging cell cycle activities observed for chromaffin cells and neuroblasts. Inference of transcription factor activities in adrenal medullary cells identified transcription factors regulating adrenal medullary fate decisions (Fig. 2h and Supplementary Table 7 ). Notably, chromaffin differentiation was, among other genes, associated with activity of many members of the Jun/Fos family of transcription factors. In neuroblasts, GATA3, SOX11 and TFAP2B showed high transcription factor activities.
Fig. 2: Differentiation dynamics during adrenal medullary development.
The alternative text for this image may have been generated using AI.
Full size image
a , Diffusion map of adrenal medullary cells colored by cell population. b , Differentiation potential of adrenal medullary cell populations based on transcriptional diversity. For each box, the center line represents the median, the upper and lower boundaries represent the 75th and 25th percentile and the whiskers represent the 1.5× interquartile range (IQR). Number of cells: cycling SCPs, n = 288; SCPs, n = 817; late SCPs, n = 632; bridge cells, n = 612; chromaffin cells, n = 1,346; connecting progenitor cells, n = 1,499; neuroblasts, n = 1,388; cycling neuroblasts, n = 1,064; late chromaffin cells, n = 963; late neuroblasts, n = 2,130. c , d , Diffusion maps of adrenal medullary cells colored by chromaffin cell lineage pseudotime trajectory ( c ) and neuroblast lineage pseudotime trajectory ( d ) as determined by slingshot. e , UMAP embedding of adrenal medullary cells with the arrows showing RNA velocities. f , Normalized expression of genes that are significantly associated with pseudotime along the SCP to neuroblast or SCP to chromaffin cell lineage. Both trajectories start at the center of the heatmap (SCPs) and progress left (chromaffin cell trajectory) and right (neuroblast trajectory) with increasing pseudotime. Selected sympathoadrenal developmental genes are highlighted. g , Expression of selected pseudotime-associated and differential gene markers in UMAP embedding of adrenal medullary cells as shown in Fig. 1c . The color indicates log-normalized gene expression. h , Heatmap showing the activity of top transcription factors in adrenal medullary cell types. The colors indicate the percentage of cells where the transcription factor was active.
Neuroblastomas resemble neuroblast differentiation states
To identify progenitor cells in the developing adrenal medulla that reflect the molecular features of neuroblastoma, we compared the transcriptional profiles of adrenal medullary cell populations to neuroblastoma cells. To this end, we studied 14 neuroblastoma tumors broadly spanning clinical neuroblastoma subgroups by droplet-based snRNA-seq (Fig. 3a and Supplementary Table 8 ). We used two complementary approaches to discriminate malignant from nonmalignant cells. First, we clustered the cells and analyzed the expression of known marker genes, including PTPRC , PTPRB and COL1A1 , to identify normal infiltrating cell types like immune, endothelial and mesenchymal cells, respectively (Extended Data Fig. 4 ). Second, we inferred copy number variations (CNVs) from the expression data of single cells (Extended Data Figs. 4c and 5 ). For further analysis, only malignant cells harboring copy number alterations and lacking expression of markers for normal infiltrating cell types were kept (Supplementary Tables 9 and 10 ). Next, we determined the transcriptional similarity between single malignant neuroblastoma cells and distinct normal cell populations of the developing human adrenal medulla (Fig. 3b,c and Extended Data Fig. 6a–l ). Adrenal neuroblasts with high similarity scores were clearly the best match to neuroblastoma cells. The highest resemblance of neuroblastoma cells to adrenal neuroblasts could be confirmed when comparing to a broad set of transcriptomes of other neuronal tissues (Extended Data Fig. 6m ) 16 , 17 , 18 . Interestingly, we observed differences in assigned normal cell populations between neuroblastoma subgroups (Fig. 3d ). MYCN -amplified neuroblastoma cells were most similar to normal neuroblasts at 7 and 8 weeks postconception, with only few cells matching late neuroblasts. The proportion of cells similar to late neuroblasts was increased in MYCN -nonamplified high-risk ( TERT -rearranged and ALT) tumors and, within low-risk neuroblastoma cells, represented the majority. These data suggest that low-risk tumors arise from a later time point during development or that a higher degree of dedifferentiation is induced in high-risk and especially MYCN -amplified neuroblastomas. No malignant mesenchymal cells as defined using neuroblastoma cell lines were identified and all tumors were classified as adrenergic according to recently proposed neuroblastoma cell type categories 7 . However, the malignant cells of three high-risk tumors showed an increase in expression of the mesenchymal signature and reduced adrenergic signature expression; hence, they were termed high-risk tumors with mesenchymal features (Extended Data Fig. 4e ). High-risk neuroblastomas with mesenchymal features showed similarity to a broader set of normal cell populations including bridge, connecting progenitor and chromaffin cells in addition to neuroblasts. This was in line with results for the mesenchymal and heterogeneous neuroblastoma cell lines SK-N-AS and SK-N-SH (Extended Data Fig. 7 ) 19 . In addition, these cell lines, which showed higher mesenchymal signature expression than neuroblastomas with mesenchymal features, also showed similarity to normal SCPs. To compare normal and neuroblastoma cells at the single-cell level rather than by cell population, we projected single neuroblastoma cells onto diffusion maps of normal adrenal medullary cells (Fig. 3e–g and Extended Data Fig. 8 ). Again, neuroblastoma cells mapped to normal neuroblasts, confirming the neuroblast identity of the tumor cells. Within the neuroblast population, low-risk tumors were more comparable to more differentiated neuroblasts, while high-risk cases mapped closer to the beginning of the neuroblast differentiation trajectory. High-risk neuroblastomas with mesenchymal features mapped close to the branching point of the chromaffin and neuroblast lineages within the newly defined connecting progenitor population. Quantification of diffusion components of projected tumor cells per subtype as a surrogate for differentiation state confirmed these differences in differentiation (Fig. 3h,i ). These results indicate that characteristics of the developmental trajectory, spanning from SCPs via bridge and connecting progenitor cells to neuroblasts and late neuroblasts, are traceable in the distinct genetic and epigenetic neuroblastoma subtypes. To further probe the developmental origin of neuroblastoma, we analyzed the expression of cell identity genes whose enhancers, via neuroblastoma-specific rearrangements/translocations, have been found to activate oncogenes such as MYCN , MYC and TERT (enhancer hijacking) 2 , 20 . Remarkably, MARCH11 , NPY , EBF1 , HAND2 , ALK , CCND1 and EXOC4 , all involved in enhancer hijacking events in neuroblastoma, showed the highest expression in neuroblast trajectory cells (Extended Data Fig. 9a ), suggesting that the neuroblast lineage is specifically at risk to acquire genetic alterations promoting neuroblastoma formation.
Fig. 3: Projection of neuroblastomas onto developmental trajectories.
The alternative text for this image may have been generated using AI.
Full size image
a , Neuroblastoma cohort with molecular and clinical annotations. b , c , Heatmaps with similarity scores of neuroblastoma cells and adrenal medullary cell populations for tumors NB06 ( b ) and NB11 ( c ). d , Bar plots illustrating the proportion of neuroblastoma cells assigned to each adrenal medullary cell population by neuroblastoma subgroup. Cells are assigned to the normal population with highest similarity score. Neuroblastomas with mesenchymal features: NB02, NB13, NB14; MYCN : NB01, NB08, NB11; TERT /ALT: NB03, NB05, NB10, NB12; low-risk: NB04, NB06, NB07, NB09. e – g , Diffusion maps of adrenal medullary cells as in Fig. 2a (colored dots) with neuroblastoma cells projected onto the embedding (black dots) for tumors NB07 ( e ), NB14 ( f ) and median diffusion components for all tumors, colored by neuroblastoma subgroup ( g ). h , i , Box plots showing the diffusion components for all neuroblastoma cells by subgroup (DC1 ( h ); DC2 ( i )). For each box, the upper and lower boundaries represent the 75th and 25th percentile, respectively, the middle horizontal lines represent the median and the whiskers represent the 1.5× IQR. Statistical significance was determined by two-sided Wilcoxon rank-sum test with P < 2.22 × 10 −16 for all pairwise comparisons. Number of cells: low-risk, n = 21,086; TERT /ALT, n = 12,719; neuroblastomas with mesenchymal features, n = 8980; MYCN , n = 16,527.
To identify the molecular features that discriminate neuroblastoma cells from normal neuroblasts, we performed differential expression analysis between single neuroblastoma cells by subtype and their closest matching normal cell types, neuroblasts or late neuroblasts (Supplementary Table 11 ). Scoring of neuroblastomas for signatures of these tumor-specific genes and signatures for normal fetal adrenal medullary cell populations showed that all three groups of high-risk tumors were dominated by the tumor-specific signatures, while low-risk tumors seemed to be very similar to their normal counterparts, late neuroblasts (Fig. 4a ). This was in line with expression of developmental genes in neuroblastoma subtypes: expression of PRPH , SYN3 , GAP43 , NTRK1 and SOX4 , which defined the most differentiated normal neuroblast state, showed the highest expression in low-risk neuroblastomas (Fig. 4b and Extended Data Fig. 9b ). In contrast, markers of less differentiated neuroblasts like ALK and MEIS2 were increased in high-risk neuroblastomas; ERBB4 and VGF , which are characteristic of bridge/connecting progenitor cells, were exclusively expressed in high-risk neuroblastomas with mesenchymal features. Inference of adrenal medullary transcription factor activities in neuroblastoma subgroups showed low-risk tumors to harbor the highest TFAP2B activity, while MYCN -amplified cells were regulated by MYCN (Fig. 4c and Extended Data Fig. 9c ). Because MYCN -amplified neuroblastomas showed a pronounced oncogenic MYCN signature and a reduced normal neuroblast signature, we asked if MYCN itself can suppress differentiation in this subgroup. To address this question, we utilized inducible MYCN knockdown in MYCN -amplified neuroblastoma cells and analyzed the expression of genes specific for fetal adrenal medullary cells in single MYCN high versus MYCN lo cells. MYCN lo cells had higher expression of neuroblast- and late neuroblast-specific genes, while cell cycle-related genes were repressed, suggesting that elevated MYCN causes dedifferentiation and proliferative activation (Fig. 4d,e and Extended Data Fig. 9d–h ). Conversely, we then asked if activation of TFAP2B, a transcription factor that we found highly expressed in normal neuroblasts and whose expression is abrogated in high-risk neuroblastomas, restores differentiation signatures in neuroblastoma cells 21 . Indeed, ectopic TFAP2B expression prominently reactivated late neuroblast, neuroblast, chromaffin and bridge-related genes in MYCN -amplified cells, indicating that the preserved TFAP2B activity in low-risk neuroblastomas at least partly retains normal differentiation programs, which are downregulated on loss of TFAP2B in high-risk neuroblastomas (Fig. 4f ).
Fig. 4: Regulators in neuroblastoma differentiation.
The alternative text for this image may have been generated using AI.
Full size image
a , Heatmap showing the expression of signatures for normal neuroblasts, late neuroblasts and tumor subgroup-specific genes as determined by differential expression analysis. b , Violin plots showing the normalized expression of developmental genes in neuroblastoma subgroups. c , Activity of selected transcription factors in neuroblastoma subgroups. d , Violin plots showing the expression of signatures for neuroblasts ( P < 2.22 × 10 −16 ), late neuroblasts ( P < 2.22 × 10 −16 ) and cycling neuroblasts ( P = 1 × 10 −12 ) in MYCN -amplified (MYCN high ) neuroblastoma cells and MYCN -amplified cells on MYCN knockdown (MYCN lo ). Statistical significance was determined by two-sided Wilcoxon rank-sum test. e , Schematic representation of neuroblastoma identity. f , Boxplots showing the changes in gene expression of fetal adrenal medullary-specific genes on overexpression of TFAP2B in MYCN -amplified neuroblastoma cells. The center line represents the median, the upper and lower boundaries represent the 75th and 25th percentile and the whiskers represent the 1.5× IQR. Number of genes: late neuroblasts, n = 27; neuroblasts, n = 20; cycling neuroblasts, n = 7; late chromaffin cells, n = 20; chromaffin cells, n = 16; connecting progenitor cells, n = 15; bridge cells, n = 17; cycling SCPs, n = 51; SCPs, n = 52; late SCPs, n = 45.
Normal neuroblast features predict neuroblastoma outcome
To analyze composition and developmental programs in a larger cohort of neuroblastomas, we used the expression signatures of normal adrenal medullary cell populations to decompose the transcriptomes of bulk neuroblastoma tumors 22 . Expectedly, neuroblastomas were confirmed to transcriptionally match normal neuroblasts and also contained smaller fractions of early chromaffin cells (Fig. 5a ). Hierarchical clustering of bulk neuroblastoma transcriptomes by their relative abundances of individual cell populations indicated that the presence of a high proportion of late neuroblast-like tumor cells was associated with low- and intermediate-risk disease, while a high fraction of cycling neuroblast-like tumor cells was associated with high-risk disease (Fig. 5a ). Summarizing cell type composition over neuroblastoma subgroups confirmed the higher abundance of late neuroblast-like tumor cells in low- and intermediate-risk tumors and a higher proportion of cycling neuroblast-like tumor cells in high-risk and MYCN -amplified neuroblastomas (Fig. 5b,c ). Similar results were obtained when excluding cycling cells from the analysis (Extended Data Fig. 10a,b ). Notably, cellular heterogeneity and the proportion of undifferentiated tumor cells, resembling bridge cells, was elevated in high-risk, MYCN -amplified (on average 2.3% in MYCN -amplified versus 0.3% in low-risk neuroblastomas) and advanced stage disease (on average 1.5% in stage 4 and 0.5% in stages 1–3 neuroblastoma), indicating an increased reservoir of malignant cells with multipotency features (Fig. 5b,c ). In addition, some tumors included late SCPs, with the late SCP signature being highly correlated with a signature for normal Schwann cells ( r = 0.964, confidence interval = 0.957–0.969) and thus probably reflecting infiltrating normal Schwann cells 23 . Results were validated in a second independent cohort 24 , which showed very similar cell type abundances (Extended Data Fig. 10c ). To test whether the composition of tumors had prognostic significance, we investigated the association of different cell type proportions with survival. Presence of high proportions of more mature neuroblast-like tumor cells was significantly associated with a favorable prognosis (Fig. 5d and Extended Data Fig. 10d–g ). In contrast, patients with tumors composed of a high proportion of cycling neuroblast-like tumor cells or neuroblast-like tumor cells when excluding cycling cells, showed poor outcomes (Fig. 5e and Extended Data Fig. 10h,i ). The clinical relevance of high proportions of mature neuroblasts and low proportions of cycling neuroblasts was supported by multivariate analyses, in which both independently predicted favorable outcome together with disease stage and age at diagnosis, while MYCN status was not predictive (Fig. 5f ).
Fig. 5: Neuroblastoma cell type composition deduced from bulk transcriptomes.
The alternative text for this image may have been generated using AI.
Full size image
a , Hierarchical clustering of patient samples based on the abundance of fetal adrenal medullary cell populations determined by BSEQ-sc (SEQC cohort). b , Composition of neuroblastoma tumors by subgroup based on deconvolution of bulk RNA-seq data with fetal adrenal cell populations. c , Composition of neuroblastomas by stage based on deconvolution of the SEQC bulk RNA-seq cohort with fetal adrenal cell populations. For each box, the center line represents the median, the upper and lower boundaries represent the 75th and 25th percentile and the whiskers represent the 1.5× IQR. Statistical significance was determined by two-sided Wilcoxon rank-sum test. Number of tumors per stage: 1–3, n = 262; 4S, n = 53; 4, n = 183. d , e , Kaplan–Meier analysis of EFS in neuroblastoma patients according to the relative abundance of late ( d ) or cycling neuroblasts ( e ) as determined by the deconvolution of tumors with fetal adrenal cell populations. P values were calculated using a two-sided log-rank test. +, censoring times. f , Prognostic effect of relative cell type abundances for late and cycling neuroblasts. The forest plots show the hazard ratios and confidence intervals derived from the Cox regression survival analyses for EFS in multivariable analyses adjusted for age, stage and MYCN status.
For malignancies with a blocked differentiation program, treatments promoting cell differentiation like all- trans retinoic acid (ATRA) are interesting therapeutic approaches 25 , 26 . To examine if we could reverse arrested differentiation in neuroblastoma cells, we deconvolved the expression profiles of ATRA-treated neuroblastoma cells with the signatures of normal adrenal medullary cell populations. ATRA treatment induced outgrowth of neurites and reduced the proportion of cycling neuroblast-like tumor cells suggesting induction of differentiation and cell cycle arrest (Fig. 6a,b ). However, most cells retained the features of undifferentiated progenitor cells, indicating that treatment of neuroblastomas with ATRA cannot fully restore normal differentiation.
Fig. 6: Evaluation of neuroblastoma differentiation therapy.
The alternative text for this image may have been generated using AI.
Full size image
a , Representative images of SK-N-BE(2)C neuroblastoma cells after treatment with ATRA or solvent control. The representative images for one out of two independent experiments with similar results are shown. b , Composition of the neuroblastoma cell line SK-N-BE(2)C after treatment with ATRA or solvent control based on deconvolution of bulk RNA-seq data with fetal adrenal cell populations. The transcript profiles of two independent biological replicates were analyzed.
Discussion
Our study resolves the lineage relationships and differentiation dynamics of human adrenal medullary cell types during development. We identified neural crest-derived SCPs to give rise to adrenal chromaffin cells and neuroblasts, which is consistent with previous studies identifying a neural crest-derived common sympathoadrenal progenitor 27 . However, in mice this concept of a common progenitor was questioned recently because mouse SCPs gave rise to adrenal chromaffin cells, while neuroblasts in sympathetic ganglia were shown to arise from an earlier split of neural crest-derived progenitor cells 11 . These differences may be due to different timings of the neuroblast gene expression program along the developmental trajectory, being upregulated at earlier stages in mice than in humans; future studies are required to elucidate whether such heterochrony, or other factors, underlie differences in adrenal medulla development in mice and humans.
We further showed that neuroblastomas are transcriptionally most similar to developing adrenal neuroblasts and that the differentiation state of neuroblastomas along this normal neuroblast differentiation trajectory is associated with prognosis. Low-risk neuroblastomas closely resemble the normal committed neuroblast population and reveal the highest degree of differentiation. In contrast, MYCN -amplified and neuroblastomas with mesenchymal features are the most undifferentiated subtypes, containing tumor cells with features of early neuroblasts and bridge cells that noticeably expand the potential reservoirs of malignant cells. Thus, therapeutic resistance and relapse may be partly due to intratumoral plasticity mechanisms in a subset of high-risk neuroblastomas. However, malignant mesenchymal cells with features of SCPs, identified in few neuroblastoma cell lines, were not found in the neuroblastoma tumors analyzed in this study. Recent findings that mesenchymal features can be triggered by mutant RAS in neuroblastoma cells indicate that specific mutations can revert neuronal differentiation programs and induce stem cell features 19 . Future studies will have to show whether rare combinations of mutations may also induce malignant mesenchymal cells in neuroblastoma tumors. Cell identity genes harboring large regulatory enhancers, which are involved in neuroblastoma-specific enhancer hijacking events activating oncogenes with influence on neuroblastoma biology 2 , 20 , show selective expression in neuroblast trajectory cells. Together, this might hint to neuroblasts as cells in the adrenal gland that are most susceptible to oncogenic transformation. Our results are contrary to a recent study stating that neuroblastoma has a primarily chromaffin cell-like phenotype and that chromaffin cell differentiation state is associated with neuroblastoma prognosis 28 . This contradiction originates from differences in cell type annotation of normal adrenal medullary cells. Sympathoblasts were identified by Dong et al. 28 based on the expression of CARTPT and INSM1 , which we found expressed in chromaffin cells. Conversely, the neuronal markers NPY , PRPH , NTRK1 and ISL1 are used to annotate chromaffin cells; these were clearly expressed in neuroblasts in our analyses. Expression of many other sympathetic neuronal marker genes in our neuroblasts supports our cell type annotation, including NEFM , STMN2 , SYN3 and ALK 27 , 29 , 30 , 31 . Importantly, a subpopulation of mature chromaffin cells in our study expressed the well-established chromaffin marker PNMT , which encodes the enzyme that catalyzes the methylation of norepinephrine to form epinephrine 32 . Our identification of tumor-related transcriptional changes and molecular mechanisms underlying impaired differentiation may guide future studies on the functional evaluation of candidate genes, refined risk classification and generation of clinically relevant neuroblastoma models. Moreover, we have provided the framework to evaluate therapeutic concepts that are based on induction of differentiation.
Methods
Ethics statement and human samples
Human embryonic and fetal tissue was obtained from the Human Developmental Biology Resource, with donor informed written consent. The Human Developmental Biology Resource is licensed by the Human Tissue Authority and complies with the Human Tissue Act (Human Tissue Authority, 2004). The study was approved by the University of Heidelberg Medical Faculty ethics committee. Neuroblastoma patients were enrolled in the neuroblastoma clinical trials of the Gesellschaft für Pädiatrische Onkologie und Hämatologie (Society for Pediatric Oncology and Hematology) between 1991 and 2018, which was approved by the ethics committee of the University of Cologne. Two patients were enrolled in the INFORM registry trial between 2015 and 2018, which was approved by the ethics committee of the University of Heidelberg. Informed written consent was obtained from the patients’ parents. Clinical information including age, sex, localization and neuroblastoma subgroup are provided in Supplementary Table 8 . Tumors in the alternative lengthening of telomere subgroup were defined as tumors harboring the mutant ATRX gene.
Preparation of single-nucleus suspensions
Single-nucleus suspensions were prepared from fresh-frozen human tissue as described previously 33 . Briefly, tissue was dounce-homogenized in nucleus lysis buffer (nucleus wash buffer, 1 mM of dithiothreitol, 0.1% Triton X-100 (Sigma-Aldrich)), filtered and collected by centrifugation at 500 g for 5 min at 4 °C. The pellet was washed three times in nucleus wash buffer (0.32 M of sucrose (Sigma-Aldrich), 5 mM of CaCl 2 (Sigma-Aldrich), 3 mM of magnesium acetate (Sigma-Aldrich), 2 mM of EDTA (Invitrogen), 0.5 mM of EGTA (Alfa Aesar), 10 mM of Tris-HCl, pH 8 (Invitrogen)) and resuspended in nucleus storage buffer (0.43 M of sucrose (Sigma-Aldrich), 70 mM of KCl (Ambion), 2 mM of MgCl 2 (Invitrogen), 5 mM of EGTA, 10 mM of Tris-HCl, pH 7.2 (Sigma-Aldrich)).
snRNA-seq library preparation and preprocessing
snRNA-seq was performed with the 10x Genomics Chromium Single Cell 3′ Kit (v.2 and v.3.1) according to the standard protocol. Libraries were sequenced on an Illumina HiSeq 4000 or NovaSeq 6000 sequencing platform.
Cell Ranger v.3.1.0 (10x Genomics) was used to align the sequencing reads to the hg19 human reference genome build, distinguish cells from the background and generate count tables of unique molecular identifiers (UMIs) for each gene per cell. Intronic counts were included.
single-cell RNA-seq library preparation and preprocessing
Single-cell libraries of the cell lines were prepared with massively parallel single-cell RNA-Seq (MARS-seq) as described previously 34 . Final MARS-seq libraries were paired-end sequenced using an Illumina NextSeq 500 system.
Reads were mapped to the hg19 human genome using Bowtie 2 v.2.1.0 with the parameters -t --threads 20 and associated with gene intervals. Mapped reads were further processed and filtered as described previously 34 . Filtering of UMIs included elimination of spurious UMIs and artifacts with a minimum required false discovery rate Q value of 0.2.
Quality control of single-cell data
The R package Seurat v.3.1 was used to calculate the quality control metrics 35 . Cells were removed from the analysis if fewer than 500 distinct genes, 1,000 counts or more than 2.5% of reads mapping to mitochondrial genes were detected, for data generated with the Chromium Next GEM Single Cell 3' Kit v.3.1 (10x Genomics). For the Chromium Single Cell 3' Kit v.2 (10x Genomics) data, cells with fewer than 300 distinct genes, 1,000 counts or more than 2.5% of reads mapping to mitochondrial genes were filtered.
We further filtered cells in clusters that had hemoglobin or mitochondrial genes among their cluster-defining markers. In the adrenal gland samples, a cluster of high-quality erythrocytes was retained.
Doublets were detected and filtered using the R package DoubletFinder v.2.0.2 with default settings. Genes that were expressed in fewer than three cells were excluded.
Normalization of single-cell data
Data were normalized for sequencing depth, scaled to 10,000 UMIs per cell and log-transformed using the Seurat NormalizeData function.
Feature selection, dimensionality reduction and cluster identification
The Seurat FindVariableGenes function was used to define highly variable genes that were used as input to principal component analysis. Normalized data were scaled and elbow plots were generated to decide which principal components to include in the analysis. This corresponded to roughly the first 20 principal components. Uniform manifold approximation and projection (UMAP) embeddings were calculated using these principal components as input and cells were clustered using the FindClusters function. Stable clusters were identified as clusters insensitive to small changes in the resolution parameter. Post-clustering quality control was performed as described in ‘Quality control of single-cell data’. Clusters subjected to further in-depth analysis were extracted, re-embedded and reclustered, followed by a second post-clustering quality control phase.
Cell type annotation
Marker genes that defined clusters by differential expression were identified using the Seurat FindAllMarkers function. Clusters were annotated to cell types by comparison of marker genes for each cluster to canonical cell type markers from the literature.
Cell cycle analysis
We scored single cells based on the expression of G 2 /M and S phase markers obtained from a previously published study 36 using the Seurat CellCycleScoring function.
Pseudotime analysis
The destiny R package v.3.0.1 was used to calculate the diffusion map embeddings. Single-cell pseudotime trajectories were constructed using the slingshot R package v.1.4.0 based on clusters identified by Seurat 37 , 38 .
The monocle3 R package v.0.2.0 was used to confirm the single-cell pseudotime trajectories generated with slingshot 39 , 40 , 41 . Cells were ordered in pseudotime using the learn_graph, followed by the order_cells function. A node in cluster 16 (SCPs) was selected as the starting point for the trajectory. Genes differentially expressed along the constructed pseudotime trajectory were identified by Moran’s I using the graph_test function as implemented in the monocle3 package. We filtered for genes with P < 0.00000001 and Moran’s I > 0.15.
RNA velocity
The velocyto command line interface was used to generate spliced/unspliced expression matrices from the 10x Genomics Chromium samples 42 . RNA velocity analysis was then performed by stochastically modeling the transcriptional dynamics of splicing kinetics using scVelo v.0.2.2 (ref. 43 ).
Evaluation of differentiation potential
Signaling entropy was computed using the R package LandSCENT v.0.99.3 to order single cells by their differentiation potencies 44 . In addition, the R package CytoTRACE v.0.3.3 was used to predict the differentiation state of cells from the single-cell RNA-seq (scRNA-seq) data 45 .
Analysis of transcription factor activity in single cells
The transcription factor activity in individual cells was inferred using SCENIC 46 , using the version available via docker pull aertslab/pyscenic v.0.10.3. Only genes expressed in at least 1 and 10% of the adrenal medulla and neuroblastoma samples, respectively, were considered. For each transcription factor, its computed activity across cells was discretized into active and inactive states using k -means clustering with k = 2. Next, we computed the fraction of cells where the transcription factor state was active among the identified cell types of the developing adrenal medulla and neuroblastoma clinical subtypes. Additionally, as input, we used the curated list of human-specific transcription factors available from https://raw.githubusercontent.com/aertslab/pySCENIC/master/resources/hs_hgnc_curated_tfs.txt , an annotation file for motif to transcription factor mapping (human, v9, mc9nr) from https://resources.aertslab.org/cistarget/motif2tf/motifs-v9-nr.hgnc-m0.001-o0.0.tbl and the ranking database of regulatory features (hg38, mc9nr, +500 base pairs (bp) and −100 bp transcription start site) from https://resources.aertslab.org/cistarget/databases/homo_sapiens/hg38/refseq_r80/mc9nr/gene_based/hg38__refseq-r80__500bp_up_and_100bp_down_tss.mc9nr.feather .
Discrimination between malignant and nonmaligant cells
Two strategies were used to discriminate malignant from nonmalignant cells. First, clustering all cells in a combined analysis identified tumor-specific clusters and clusters containing cells from multiple tumors and expressing markers of immune cells, interstitial cells, endothelial cells, Schwann cells or liver cells, suggesting that they were nonmalignant cell types (Extended Data Fig. 4 ). Second, copy number alterations were inferred from high-quality single-cell transcriptomes. Inferred copy numbers were largely in line with CNVs detected by bulk sequencing of the same tumors and confirmed the grouping into malignant and nonmalignant cells (Extended Data Fig. 5 ).
Copy number analysis in single cells
CNVs at the single-cell level were called with the R package InferCNV v.1.4.0 (cutoff = 0.1, denoise = TRUE, HMM = F and k_obs_groups = 5) using normal neuroblasts as the reference cells and excluding cells with fewer than 1,000 transcripts from the analysis 47 . If this resulted in fewer than 1,000 cells, the threshold was lowered iteratively to first 500 and then 300 transcripts until either all cells or at least 1,000 cells could be evaluated. The reference gene positions were taken from GENCODE v.19.
Assignment of single cells to cell types
Single neuroblastoma cells were assigned to cell types by determining similarity to the reference cell types based on Spearman correlation with the R package SingleR v.1.0.5 (de.method = ‘wilcox’) using fetal adrenal medullary cell populations as reference 48 .
Projection of single cells onto diffusion maps
Single cells were projected onto existing diffusion map embeddings using the dm_predict function in the R package destiny.
Generation of single-cell signature scores
Scores for the expression of gene signatures in single cells were determined using the AddModuleScore function in Seurat with 100 control genes per analyzed gene. Briefly, the average expression of the gene signature was determined and subtracted by the expression of the control gene sets.
Deconvolution of bulk RNA-seq datasets
The R package bseqsc v.1.0 (BSEQ-sc) and CIBERSORT v.1.01 were used to deconvolute bulk RNA-seq datasets with scRNA-seq-derived cell populations 49 , 50 . Using an adjusted P < 0.05 and a log 2 fold change > 0.8 as identified by Seurat, we selected the top marker genes per single-cell cluster. A reference matrix with the average expression of these top markers per cell type was calculated using BSEQ-sc. This reference matrix was then used to deconvolute normalized bulk RNA-seq data with CIBERSORT. Adrenal medullary cell populations were used as references. In addition, immune cells, endothelial cells, interstitial cells and erythrocytes, summarized as microenvironment, were included as reference cells for bulk tumors but not cell lines.
Survival analysis
The Kaplan–Meier method was used to prepare curves of event-free and overall survival with a log-rank test using the R package survival v.3.1.11. Event-free survival (EFS) was determined as the time from diagnosis to tumor progression, relapse, death from disease or last follow-up if no event occurred. Overall survival was determined as the time from diagnosis to death from disease or last follow-up if the patient survived. Maximally selected rank statistics were used to identify cutoff points in the continuous predictors using the R package maxstat v.0.7.25.
Multivariable Cox regression models were used to analyze the independence of prognostic variables using the R package rms v.5.1.4. Covariates of age, stage and MYCN status were included. Backward selection was performed on the model using the function fastbw in the rms package.
Single-molecule RNA FISH
Cryosections were cut from fresh-frozen embryonic and fetal adrenal glands at a thickness of 10 µm using a Leica CM1950 cryostat (Leica Biosystems). RNA in situ hybridization was performed with the Advanced Cell Diagnostics RNAscope Fluorescent Multiplex Assay according to manufacturer’s instructions for fresh-frozen tissue. The ERBB3-C1, ASCL1-C1, ISL1-C2 and TH-C3 probes were used with the fluorophores Alexa Fluor 488, ATTO 550 and ATTO 647N. Images were acquired with an LSM 710 ConfoCor 3 confocal microscope (ZEISS) with ×20 and ×63 (oil) objectives and processed with the ZEN 2.3 v.14.0.11.201 (ZEISS) and ImageJ v.1.53c (NIH) software.
Histology and immunohistochemistry
For histology and immunohistochemistry, 4-μm sections of formalin-fixed, paraffin-embedded tissue blocks were cut. Tissue integrity was validated on hematoxylin and eosin-stained slides. For immunohistochemistry, antigen retrieval was carried out with microwave treatment using the antigen Target Retrieval Solution (Agilent Technologies). Slides were incubated for up to 60 min with the following primary antibodies in an automated immunostainer (Ventana Medical Systems): monoclonal rabbit anti-ALK (dilution, ready-to-use; catalog no. 790-4796, clone D5F3; Ventana Medical Systems); monoclonal mouse anti-chromogranin A (dilution, ready-to-use; 760-2519, clone LK2H10; Ventana Medical Systems); monoclonal rabbit anti-islet 1 (dilution, 1:250; catalog no. ab178400, clone EPR10362; Abcam); or monoclonal mouse anti-Ki-67 (dilution, 1:100; catalog no. GA62661-2, clone MIB-1; Dako). Then, slides were incubated with a secondary anti-rabbit IgG antibody (dilution, ready-to-use; ImmPRESS Reagent Kit, peroxidase-conjugated; catalog no. MP-7401; VECTOR Laboratories) or anti-mouse IgG antibody (dilution, ready-to-use; ImmPRESS Reagent Kit, peroxidase-conjugated; catalog no. MP-7402; VECTOR Laboratories) followed by target detection using ABC-kit chromogen (catalog no. K3461; Dako). Slides were counterstained with hematoxylin (Gill’s Formula; catalog no. H-3401; VECTOR laboratories). Images were acquired with an Axio Scan.Z1 (ZEISS) at ×20 magnification and processed with the ZEN 2.3 v.14.0.11.201 software.
Cell lines and culture
The neuroblastoma cell lines SK-N-AS and SK-N-BE(2)C were cultured in Roswell Park Memorial Institute 1640 medium (Thermo Fisher Scientific) supplemented with 10% FCS (Gibco) and 1% penicillin/streptomycin (AppliChem) at 37 °C and 5% CO 2 . IMR5/75-shMYCN cells were cultured as described previously 51 . Cell line authentication was done by the Multiplexion Multiplex Cell Authentication service (Heidelberg); no Mycoplasma contamination or misidentified cells were detected. SK-N-BE(2)C and SK-N-AS cells were purchased from ATCC.
Induction of cell differentiation
A total of 1 × 10 6 cells were seeded 24 h before treatment. An ATRA stock solution was prepared at a concentration of 10 mM in ethanol and diluted in fresh culture medium to obtain a final concentration of 10 µM. Cells were treated with 10 µM of ATRA or solvent control (ethanol) and collected after 144 h of treatment. Two independent biological replicates were performed.
MYCN knockdown
A total of 1 × 10 6 IMR5/75-shMYCN cells were treated with 0.1 µg ml −1 of doxycycline (MYCN lo ) or left untreated (MYCN high ) for 72 h before being collected for scRNA-seq analysis. The knockdown of MYCN was verified by western blot analysis using primary monoclonal mouse anti-Myc (dilution, 1:1,000; catalog no. sc-53993, clone B8.4.B; Santa Cruz Biotechnology) and monoclonal mouse anti-vinculin horseradish peroxidase (dilution, 1:1,000; catalog no. sc-73614, clone 7F9; Santa Cruz Biotechnology) antibodies.
Bulk gene expression profiling
Isolation of total RNA, ribosomal RNA depletion, RNA library preparation and sequencing of cell lines was performed as described previously 52 . STAR aligner v.2.5.2b was used to align FASTQ files containing reads for individual samples by two-pass alignment 53 . Reads were aligned to a STAR index generated from the phase 3 1000 Genomes Project human genome assembly (hs37d5), using GENCODE v.19 gene models. Default alignment call parameters were used except for the following modifications: --sjdbOverhang 200 --outSAMtype BAM Unsorted SortedByCoordinate --outFilterMultimapNmax 1 --outFilterMismatchNmax 5 --outFilterMismatchNoverLmax 0.3 --twopassMode Basic --twopass1readsN -1 --chimSegmentMin 15 --chimScoreMin 1 --chimScoreJunctionNonGTAG 0 --chimJunctionOverhangMin 15 --chimSegmentReadGapMax 3 --alignSJstitchMismatchNmax 5 -1 5 5 alignIntronMax 1100000 --alignMatesGapMax 1100000 --alignSJDBoverhangMin 3 --alignIntronMin 20.
Sambamba v.0.6.5 was used for the alignment file sorting, duplicate marking and BAM index generation using 12 threads 54 . Quality control analysis was performed using the sambamba flagstat command and rnaseqc v.1.1.8 with the hs37d5 assembly and GENCODE v.19 gene models 55 . Gene-specific gene counting over exon features based on GENCODE v.19 gene models was performed using featureCounts v.1.5.1 (ref. 56 ). Both reads of a paired fragment were used for counting and the quality threshold was set to 255, which indicates that STAR found a unique alignment. Strand-unspecific counting was used.
The edgeR v.3.28.1 R package was used to normalize gene counts 57 , 58 . Only genes having sum of counts per million (CPM) > 0 across all samples were kept. Compositional differences between libraries were corrected by trimmed means of M values normalization 59 ; log-transformed CPM values were used for downstream analysis 60 , 61 , 62 , 63 , 64 , 65 , 66 , 67 , 68 , 69 , 70 , 71 , 72 , 73 , 74 , 75 , 76 , 77 , 78 , 79
The processing of published bulk RNA-seq and microarray datasets was performed as described previously 21 , 22 , 24 .
Reporting Summary
Further information on research design is available in the Nature Research Reporting Summary linked to this article.
Data availability
Raw adrenal gland and neuroblastoma sequencing data have been deposited in the European Genome-phenome Archive under study accession no. EGAS00001004388 . Processed data can be downloaded and explored interactively in a Shiny App: https://adrenal.kitz-heidelberg.de/developmental_programs_NB_viz/ . Raw and processed sequencing data for the neuroblastoma cell lines have been deposited in the Gene Expression Omnibus (GEO) under accession no. GSE163431 . Bulk RNA-seq data of neuroblastomas from the SEQC cohort were obtained from the GEO (accession no. GSE49711 ). Bulk RNA-seq data of neuroblastomas from the TARGET cohort were obtained from https://portal.gdc.cancer.gov/projects/TARGET-NBL . The single-cell RNA-seq data of the neuroblastoma cell line SK-N-SH were obtained from the GEO under accession no. GSE158130 . Expression data of IMR-32 cells on inducible overexpression of TFAP2B were obtained from the GEO under accession no. GSE74350 . Whole-genome sequencing data for tumors studied by scRNA-seq were obtained from the European Genome-phenome Archive (accession nos. EGAS00001004349 and EGAS00001001308 ). Matching tumor IDs are provided in Supplementary Table 8 . Source data are provided with this paper.
References
Maris, J. M., Hogarty, M. D., Bagatell, R. & Cohn, S. L. Neuroblastoma. Lancet 369 , 2106–2120 (2007).
Article CAS PubMed Google Scholar
Peifer, M. et al. Telomerase activation by genomic rearrangements in high-risk neuroblastoma. Nature 526 , 700–704 (2015).
Article CAS PubMed PubMed Central Google Scholar
Brodeur, G. M., Seeger, R. C., Schwab, M., Varmus, H. E. & Bishop, J. M. Amplification of N-myc in untreated human neuroblastomas correlates with advanced disease stage. Science 224 , 1121–1124 (1984).
Article CAS PubMed Google Scholar
Ackermann, S. et al. A mechanistic classification of clinical phenotypes in neuroblastoma. Science 362 , 1165–1170 (2018).
Article CAS PubMed PubMed Central Google Scholar
Mossé, Y. P. et al. Identification of ALK as a major familial neuroblastoma predisposition gene. Nature 455 , 930–935 (2008).
Article PubMed PubMed Central Google Scholar
Janoueix-Lerosey, I. et al. Somatic and germline activating mutations of the ALK kinase receptor in neuroblastoma. Nature 455 , 967–970 (2008).
Article CAS PubMed Google Scholar
van Groningen, T. et al. Neuroblastoma is composed of two super-enhancer-associated differentiation states. Nat. Genet. 49 , 1261–1266 (2017).
Article CAS PubMed Google Scholar
Boeva, V. et al. Heterogeneity of neuroblastoma cell identity defined by transcriptional circuitries. Nat. Genet. 49 , 1408–1413 (2017).
Article CAS PubMed Google Scholar
Anderson, D. J., Carnahan, J. F., Michelsohn, A. & Patterson, P. H. Antibody markers identify a common progenitor to sympathetic neurons and chromaffin cells in vivo and reveal the timing of commitment to neuronal differentiation in the sympathoadrenal lineage. J. Neurosci. 11 , 3507–3519 (1991).
Article CAS PubMed PubMed Central Google Scholar
De Preter, K. et al. Human fetal neuroblast and neuroblastoma transcriptome analysis confirms neuroblast origin and highlights neuroblastoma candidate genes. Genome Biol. 7 , R84 (2006).
Article PubMed PubMed Central Google Scholar
Furlan, A. et al. Multipotent peripheral glial cells generate neuroendocrine cells of the adrenal medulla. Science 357 , eaal3753 (2017).
Article PubMed PubMed Central Google Scholar
Cooper, M. J., Hutchins, G. M. & Israel, M. A. Histogenesis of the human adrenal medulla. An evaluation of the ontogeny of chromaffin and nonchromaffin lineages. Am. J. Pathol. 137 , 605–615 (1990).
CAS PubMed PubMed Central Google Scholar
Molenaar, W. M., Lee, V. M. & Trojanowski, J. Q. Early fetal acquisition of the chromaffin and neuronal immunophenotype by human adrenal medullary cells. An immunohistological study using monoclonal antibodies to chromogranin A, synaptophysin, tyrosine hydroxylase, and neuronal cytoskeletal proteins. Exp. Neurol. 108 , 1–9 (1990).
Article CAS PubMed Google Scholar
Magro, G. & Grasso, S. Immunohistochemical identification and comparison of glial cell lineage in foetal, neonatal, adult and neoplastic human adrenal medulla. Histochem. J. 29 , 293–299 (1997).
Article CAS PubMed Google Scholar
Katsetos, C. D. et al. Class III β-tubulin isotype (β III) in the adrenal medulla: I. Localization in the developing human adrenal medulla. Anat. Rec. 250 , 335–343 (1998).
Article CAS PubMed Google Scholar
Lake, B. B. et al. Integrative single-cell analysis of transcriptional and epigenetic states in the human adult brain. Nat. Biotechnol. 36 , 70–80 (2018).
Article CAS PubMed Google Scholar
La Manno, G. et al. Molecular diversity of midbrain development in mouse, human, and stem cells. Cell 167 , 566–580.e19 (2016).
Article CAS PubMed PubMed Central Google Scholar
Zhong, S. et al. Decoding the development of the human hippocampus. Nature 577 , 531–536 (2020).
Article CAS PubMed Google Scholar
Gartlgruber, M. et al. Super enhancers define regulatory subtypes and cell identity in neuroblastoma. Nat. Cancer 2 , 114–128 (2021).
Article PubMed Google Scholar
Zimmerman, M. W. et al. MYC drives a subset of high-risk pediatric neuroblastomas and is activated through mechanisms including enhancer hijacking and focal enhancer amplification. Cancer Discov. 8 , 320–335 (2018).
Article CAS PubMed Google Scholar
Ikram, F. et al. Transcription factor activating protein 2 beta (TFAP2B) mediates noradrenergic neuronal differentiation in neuroblastoma. Mol. Oncol. 10 , 344–359 (2016).
Article CAS PubMed Google Scholar
Zhang, W. et al. Comparison of RNA-seq and microarray-based models for clinical endpoint prediction. Genome Biol. 16 , 133 (2015).
Article CAS PubMed PubMed Central Google Scholar
Ambros, I. M. et al. Role of ploidy, chromosome 1p, and Schwann cells in the maturation of neuroblastoma. N. Engl. J. Med. 334 , 1505–1511 (1996).
Article CAS PubMed Google Scholar
Wei, J. S. et al. Clinically relevant cytotoxic immune cell signatures and clonal expansion of T-cell receptors in high-risk MYCN -not-amplified human neuroblastoma. Clin. Cancer Res. 24 , 5673–5684 (2018).
Article CAS PubMed PubMed Central Google Scholar
Sidell, N. Retinoic acid-induced growth inhibition and morphologic differentiation of human neuroblastoma cells in vitro. J. Natl Cancer Inst. 68 , 589–596 (1982).
CAS PubMed Google Scholar
Matthay, K. K. et al. Long-term results for children with high-risk neuroblastoma treated on a randomized trial of myeloablative therapy followed by 13- cis -retinoic acid: a children’s oncology group study. J. Clin. Oncol. 27 , 1007–1013 (2009).
Article CAS PubMed PubMed Central Google Scholar
Huber, K. The sympathoadrenal cell lineage: specification, diversification, and new perspectives. Dev. Biol. 298 , 335–343 (2006).
Article CAS PubMed Google Scholar
Dong, R. et al. Single-cell characterization of malignant phenotypes and developmental trajectories of adrenal neuroblastoma. Cancer Cell 38 , 716–733.e6 (2020).
Article CAS PubMed Google Scholar
Huber, K. Segregation of neuronal and neuroendocrine differentiation in the sympathoadrenal lineage. Cell Tissue Res. 359 , 333–341 (2015).
Article CAS PubMed Google Scholar
Lumb, R. & Schwarz, Q. Sympathoadrenal neural crest cells: the known, unknown and forgotten? Dev. Growth Differ. 57 , 146–157 (2015).
Article PubMed Google Scholar
Janoueix-Lerosey, I., Lopez-Delisle, L., Delattre, O. & Rohrer, H. The ALK receptor in sympathetic neuron development and neuroblastoma. Cell Tissue Res. 372 , 325–337 (2018).
Article CAS PubMed Google Scholar
Unsicker, K., Huber, K., Schober, A. & Kalcheim, C. Resolved and open issues in chromaffin cell development. Mech. Dev. 130 , 324–329 (2013).
Article CAS PubMed Google Scholar
Ernst, K. J. Establishment of a simplified preparation method for single-nucleus RNA-sequencing and its application to long-term frozen tumor tissues. Preprint at bioRxiv https://doi.org/10.1101/2020.10.23.351809 (2020).
Jaitin, D. A. et al. Massively parallel single-cell RNA-seq for marker-free decomposition of tissues into cell types. Science 343 , 776–779 (2014).
Article CAS PubMed PubMed Central Google Scholar
Butler, A., Hoffman, P., Smibert, P., Papalexi, E. & Satija, R. Integrating single-cell transcriptomic data across different conditions, technologies, and species. Nat. Biotechnol. 36 , 411–420 (2018).
Article CAS PubMed PubMed Central Google Scholar
Tirosh, I. et al. Single-cell RNA-seq supports a developmental hierarchy in human oligodendroglioma. Nature 539 , 309–313 (2016).
Article PubMed PubMed Central Google Scholar
Angerer, P. et al. destiny: diffusion maps for large-scale single-cell data in R. Bioinformatics 32 , 1241–1243 (2016).
Article CAS PubMed Google Scholar
Street, K. et al. Slingshot: cell lineage and pseudotime inference for single-cell transcriptomics. BMC Genomics 19 , 477 (2018).
Article PubMed PubMed Central Google Scholar
Trapnell, C. et al. The dynamics and regulators of cell fate decisions are revealed by pseudotemporal ordering of single cells. Nat. Biotechnol. 32 , 381–386 (2014).
Article CAS PubMed PubMed Central Google Scholar
Qiu, X. et al. Reversed graph embedding resolves complex single-cell trajectories. Nat. Methods 14 , 979–982 (2017).
Article CAS PubMed PubMed Central Google Scholar
Cao, J. et al. The single-cell transcriptional landscape of mammalian organogenesis. Nature 566 , 496–502 (2019).
Article CAS PubMed PubMed Central Google Scholar
La Manno, G. et al. RNA velocity of single cells. Nature 560 , 494–498 (2018).
Article CAS PubMed PubMed Central Google Scholar
Bergen, V., Lange, M., Peidli, S., Wolf, F. A. & Theis, F. J. Generalizing RNA velocity to transient cell states through dynamical modeling. Nat. Biotechnol. 38 , 1408–1414 (2020).
Article PubMed Google Scholar
Teschendorff, A. E. & Enver, T. Single-cell entropy for accurate estimation of differentiation potency from a cell’s transcriptome. Nat. Commun. 8 , 15599 (2017).
Article CAS PubMed PubMed Central Google Scholar
Gulati, G. S. et al. Single-cell transcriptional diversity is a hallmark of developmental potential. Science 367 , 405–411 (2020).
Article CAS PubMed PubMed Central Google Scholar
Aibar, S. et al. SCENIC: single-cell regulatory network inference and clustering. Nat. Methods 14 , 1083–1086 (2017).
Article CAS PubMed PubMed Central Google Scholar
Patel, A. P. et al. Single-cell RNA-seq highlights intratumoral heterogeneity in primary glioblastoma. Science 344 , 1396–1401 (2014).
Article CAS PubMed PubMed Central Google Scholar
Aran, D. et al. Reference-based analysis of lung single-cell sequencing reveals a transitional profibrotic macrophage. Nat. Immunol. 20 , 163–172 (2019).
Article CAS PubMed PubMed Central Google Scholar
Baron, M. et al. A single-cell transcriptomic map of the human and mouse pancreas reveals inter- and intra-cell population structure. Cell Syst. 3 , 346–360.e4 (2016).
Article CAS PubMed PubMed Central Google Scholar
Newman, A. M. et al. Robust enumeration of cell subsets from tissue expression profiles. Nat. Methods 12 , 453–457 (2015).
Article CAS PubMed PubMed Central Google Scholar
Muth, D. et al. Transcriptional repression of SKP2 is impaired in MYCN -amplified neuroblastoma. Cancer Res. 70 , 3791–3802 (2010).
Article CAS PubMed Google Scholar
Henrich, K.-O. et al. Integrative genome-scale analysis identifies epigenetic mechanisms of transcriptional deregulation in unfavorable neuroblastomas. Cancer Res. 76 , 5523–5537 (2016).
Article CAS PubMed Google Scholar
Dobin, A. et al. STAR: ultrafast universal RNA-seq aligner. Bioinformatics 29 , 15–21 (2013).
Article CAS PubMed Google Scholar
Tarasov, A., Vilella, A. J., Cuppen, E., Nijman, I. J. & Prins, P. Sambamba: fast processing of NGS alignment formats. Bioinformatics 31 , 2032–2034 (2015).
Article CAS PubMed PubMed Central Google Scholar
DeLuca, D. S. et al. RNA-SeQC: RNA-seq metrics for quality control and process optimization. Bioinformatics 28 , 1530–1532 (2012).
Article CAS PubMed PubMed Central Google Scholar
Liao, Y., Smyth, G. K. & Shi, W. featureCounts: an efficient general purpose program for assigning sequence reads to genomic features. Bioinformatics 30 , 923–930 (2014).
Article CAS PubMed Google Scholar
McCarthy, D. J., Chen, Y. & Smyth, G. K. Differential expression analysis of multifactor RNA-Seq experiments with respect to biological variation. Nucleic Acids Res. 40 , 4288–4297 (2012).
Article CAS PubMed PubMed Central Google Scholar
Robinson, M. D., McCarthy, D. J. & Smyth, G. K. edgeR: a Bioconductor package for differential expression analysis of digital gene expression data. Bioinformatics 26 , 139–140 (2010).
Article CAS PubMed Google Scholar
Robinson, M. D. & Oshlack, A. A scaling normalization method for differential expression analysis of RNA-seq data. Genome Biol. 11 , R25 (2010).
Article PubMed PubMed Central Google Scholar
Pihlajoki, M., Dörner, J., Cochran, R. S., Heikinheimo, M. & Wilson, D. B. Adrenocortical zonation, renewal, and remodeling. Front. Endocrinol. (Lausanne) 6 , 27 (2015).
Article Google Scholar
Goncharov, N. V., Nadeev, A. D., Jenkins, R. O. & Avdonin, P. V. Markers and biomarkers of endothelium: when something is rotten in the state. Oxid. Med. Cell. Longev. 2017 , 9759735 (2017).
Article PubMed PubMed Central Google Scholar
Xie, T. et al. Single-cell deconvolution of fibroblast heterogeneity in mouse pulmonary fibrosis. Cell Rep. 22 , 3625–3640 (2018).
Article CAS PubMed PubMed Central Google Scholar
Foote, A. G., Wang, Z., Kendziorski, C. & Thibeault, S. L. Tissue specific human fibroblast differential expression based on RNAsequencing analysis. BMC Genomics 20 , 308 (2019).
Article PubMed PubMed Central Google Scholar
Donovan, J. A. & Koretzky, G. A. CD45 and the immune response. J. Am. Soc. Nephrol. 4 , 976–985 (1993).
Article CAS PubMed Google Scholar
Irving, B. A., Chan, A. C. & Weiss, A. Functional characterization of a signal transducing motif present in the T cell antigen receptor zeta chain. J. Exp. Med. 177 , 1093–1103 (1993).
Article CAS PubMed Google Scholar
Kadowaki, T. et al. Reconsideration of macrophage and dendritic cell classification. Anticancer Res. 32 , 2257–2261 (2012).
CAS PubMed Google Scholar
Affer, M. et al. Gene expression differences between enriched normal and chronic myelogenous leukemia quiescent stem/progenitor cells and correlations with biological abnormalities. J. Oncol. 2011 , 798592 (2011).
Article CAS PubMed PubMed Central Google Scholar
Castiglioni, I. et al. The Trithorax protein Ash1L promotes myoblast fusion by activating Cdon expression. Nat. Commun. 9 , 5026 (2018).
Article PubMed PubMed Central Google Scholar
Chal, J. & Pourquié, O. Making muscle: skeletal myogenesis in vivo and in vitro. Development 144 , 2104–2122 (2017).
Article CAS PubMed Google Scholar
Robin, Y.-M. et al. Transgelin is a novel marker of smooth muscle differentiation that improves diagnostic accuracy of leiomyosarcomas: a comparative immunohistochemical reappraisal of myogenic markers in 900 soft tissue tumors. Mod. Pathol. 26 , 502–510 (2013).
Article CAS PubMed Google Scholar
Hinz, B. et al. The myofibroblast: one function, multiple origins. Am. J. Pathol. 170 , 1807–1816 (2007).
Article CAS PubMed PubMed Central Google Scholar
Hsia, L.-T. et al. Myofibroblasts are distinguished from activated skin fibroblasts by the expression of AOC3 and other associated markers. Proc. Natl Acad. Sci. USA 113 , E2162–E2171 (2016).
Article CAS PubMed PubMed Central Google Scholar
Peters, D. T. et al. Asialoglycoprotein receptor 1 is a specific cell-surface marker for isolating hepatocytes derived from human pluripotent stem cells. Development 143 , 1475–1481 (2016).
Article CAS PubMed PubMed Central Google Scholar
Aizarani, N. et al. A human liver cell atlas reveals heterogeneity and epithelial progenitors. Nature 572 , 199–204 (2019).
Article CAS PubMed PubMed Central Google Scholar
Kim, H.-S. et al. Schwann cell precursors from human pluripotent stem cells as a potential therapeutic target for myelin repair. Stem Cell Rep. 8 , 1714–1726 (2017).
Article CAS Google Scholar
Liu, Z. et al. Specific marker expression and cell state of Schwann cells during culture in vitro. PLoS ONE 10 , e0123278 (2015).
Article PubMed PubMed Central Google Scholar
Chan, W. H., Anderson, C. R. & Gonsalvez, D. G. From proliferation to target innervation: signaling molecules that direct sympathetic nervous system development. Cell Tissue Res. 372 , 171–193 (2018).
Article CAS PubMed Google Scholar
Rohrer, H. Transcriptional control of differentiation and neurogenesis in autonomic ganglia. Eur. J. Neurosci. 34 , 1563–1573 (2011).
Article PubMed Google Scholar
Chan, W. H. et al. RNA-seq of isolated chromaffin cells highlights the role of sex-linked and imprinted genes in adrenal medulla development. Sci. Rep. 9 , 3929 (2019).
Article PubMed PubMed Central Google Scholar
Download references
Acknowledgements
We thank the patients and their parents for making available the tumor specimens analyzed in this study. We also thank the German Neuroblastoma Biobank for providing these samples. The human embryonic and fetal materials were provided by the joint MRC/Wellcome Trust (grant no. MR/R006237/1) Human Developmental Biology Resource ( www.hdbr.org ). The institutional review board approved the collection and use of all specimens in this study. We thank J.-P. Mallm and the Single-cell Open Lab, Genomics and Proteomics Core Facility and Light Microscopy Facility at the German Cancer Research Center. The results published in this article are in part based on data generated by the Therapeutically Applicable Research to Generate Effective Treatments ( https://ocg.cancer.gov/programs/target ) initiative (phs000218). The data used for this analysis are available at https://portal.gdc.cancer.gov/projects . This work was supported by the Fördergesellschaft Kinderkrebs-Neuroblastom-Forschung e.V. (F.W. and S.J.), German-Israeli Helmholtz Research School in Cancer Biology (S.J.), German Ministry of Science and Education (e:Med initiative, grant no. 01ZX1307 to F.W.; grant no. 031L0238 to F.W. and T.H.), EU as part of the EraCoSysMed initiative (Optimize-NB and Infer-NB to F.W. and T. H.), German Cancer Research Center intramural program for interaction projects (Single-cell Open Lab) and DKFZ-Heidelberg Center for Personalized Oncology (HIPO) and National Center for Tumor Disease (NCT 3.0—ENHANCE to F.W.). The laboratory of T.G.P.G. is supported by the Barbara & Wilfried Mohr Foundation.
Author information
Authors and Affiliations
Hopp Children’s Cancer Center Heidelberg (KiTZ), Heidelberg, Germany
Selina Jansky, Umut H. Toprak, Elisa M. Wecht, Moritz Gartlgruber, Thomas G. P. Grünewald, Kai-Oliver Henrich & Frank Westermann
Division of Neuroblastoma Genomics, German Cancer Research Center (DKFZ), Heidelberg, Germany
Selina Jansky, Umut H. Toprak, Elisa M. Wecht, Moritz Gartlgruber, Kai-Oliver Henrich & Frank Westermann
Faculty of Biosciences, Heidelberg University, Heidelberg, Germany
Selina Jansky, Andrés Quintero & Alessandro Greco
Health Data Science Unit, Medical Faculty University Heidelberg and BioQuant, Heidelberg, Germany
Ashwini Kumar Sharma, Andrés Quintero & Carl Herrmann
Division of Theoretical Systems Biology, German Cancer Research Center (DKFZ), Heidelberg, Germany
Verena Körber, Alessandro Greco & Thomas Höfer
Department of Computer Science and Applied Mathematics and Department of Biological Regulation, Weizmann Institute of Science, Rehovot, Israel
Elad Chomsky & Amos Tanay
Division of Translational Pediatric Sarcoma Research, German Cancer Research Center (DKFZ), Heidelberg, Germany
Thomas G. P. Grünewald
Institute of Pathology, Heidelberg University Hospital, Heidelberg, Germany
Thomas G. P. Grünewald
Authors
Selina Jansky
View author publications
Search author on: PubMed Google Scholar
Ashwini Kumar Sharma
View author publications
Search author on: PubMed Google Scholar
Verena Körber
View author publications
Search author on: PubMed Google Scholar
Andrés Quintero
View author publications
Search author on: PubMed Google Scholar
Umut H. Toprak
View author publications
Search author on: PubMed Google Scholar
Elisa M. Wecht
View author publications
Search author on: PubMed Google Scholar
Moritz Gartlgruber
View author publications
Search author on: PubMed Google Scholar
Alessandro Greco
View author publications
Search author on: PubMed Google Scholar
Elad Chomsky
View author publications
Search author on: PubMed Google Scholar
Thomas G. P. Grünewald
View author publications
Search author on: PubMed Google Scholar
Kai-Oliver Henrich
View author publications
Search author on: PubMed Google Scholar
Amos Tanay
View author publications
Search author on: PubMed Google Scholar
Carl Herrmann
View author publications
Search author on: PubMed Google Scholar
Thomas Höfer
View author publications
Search author on: PubMed Google Scholar
Frank Westermann
View author publications
Search author on: PubMed Google Scholar
Contributions
S.J. and F.W. designed and coordinated the experiments and data analyses. S.J. performed most of the experiments and data analyses. A.K.S. analyzed the transcription factor activity in the snRNA-seq data. V.K. analyzed the copy number variation in the snRNA-seq data. U.H.T. contributed to the preprocessing of the snRNA-seq and bulk RNA-seq data. E.M.W. performed the RNAscope and western blot experiments. A.G., A.Q., E.C., C.H., A.T. and T.H. contributed to the single-cell data analysis. M.G. performed the ATRA treatment. T.G.P.G. coordinated the immunohistochemical staining. S.J. and F.W. wrote the manuscript with input from K.-O.H. and T.H. F.W. supervised the project.
Corresponding author
Correspondence to Frank Westermann .
Ethics declarations
Competing interests
The authors declare no competing interests.
Additional information
Peer review information Nature Genetics thanks Guoji Guo and the other, anonymous, reviewer(s) for their contribution to the peer review of this work.
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.
Extended data
Extended Data Fig. 1 Adrenal gland histology and cell types.
a , b , H&E and immunohistochemical staining of adrenal gland serial sections for CHGA, ALK, ISL1 and KI67. Left panels show overviews over entire glands. Boxes mark regions of insets on the right. Scale bars: left: 1000/500 µm, inset: 200 µm. Sections are derived from 17 pcw (AG07) ( a ) and 14 pcw (AG08) ( b ) adrenal glands. Shown are representative results for two out of four samples analyzed in independent experiments.
Extended Data Fig. 2 Adrenal gland cluster, age and sample contribution.
a , Uniform Manifold Approximation and Projection (UMAP) embedding of single cells derived from developing human adrenal glands colored by 45 unique clusters of transcriptionally similar cells. Inset shows the cells colored by cell types as in Fig. 1b . b, c , UMAP embedding from ( a ) colored by time point of sample collection ( b ) and individual samples ( c ). d , Heat map depicting relative expression of marker genes for adrenal gland cell populations as in Fig. 1b . Normalized expression is shown as z-score. e, f , UMAP plot of adrenal medullary cells colored by 16 clusters of transcriptionally similar cells ( d ) and individual samples ( e ). Inset shows the cells colored by cell types as in Fig. 1c . g , UMAP visualizations showing adrenal medullary cells from each individual time point integrated using harmony. h , Barplot with fractions of cells in each cell cycle phase in adrenal medullary cell types. i , RNAscope fluorescent RNA in situ hybridization for bridge marker ASCL1 , neuroblast marker ISL1 and chromaffin marker TH in human adrenal glands at 8 pcw and 14 pcw. Left panels show composite overviews over entire glands, boxes mark the regions of insets shown on the right. Scale bars: left: 800 µm, inset: 20 µm. Shown are representative results for two out of four samples analyzed in independent experiments.
Extended Data Fig. 3 Adrenal medulla potency and pseudotime.
a , Diffusion map of adrenal medullary cells as shown in Fig. 2a , colored by 19 clusters of transcriptionally similar cells. Start of the pseudotime trajectory is marked with an arrow (cluster 16). b , c , UMAP embedding of adrenal medullary cells without cycling populations colored by 19 clusters of transcriptionally similar cells ( b ) or cell types ( c ). Start of the pseudotime trajectory is marked with an arrow (cluster 16). d , f , UMAP plot showing adrenal medullary cells without cycling populations colored by differentiation potential as determined by CytoTRACE ( d ) and differentiation potency as determined by LandSCENT ( f ). e , Boxplot with differentiation potencies for adrenal medullary cell populations as determined by LandSCENT. Here, the center line represents the median, upper and lower boundaries the 75 th and 25 th percentile and whiskers the 1.5x interquartile range. Number of cells: late SCPs: n = 632, SCPs: n = 817, cycling SCPs: n = 288, Bridge: n = 612, con. Prog: n = 1499, Chrom: n = 1346, late Chrom: n = 963, cycling Nbs: n = 1064, Nbs: n = 1388, late Nbs: n = 2130. g , Diffusion map of adrenal medullary cells colored by SCP-to-late SCP pseudotime trajectory as determined by slingshot. h , UMAP visualization illustrating adrenal medullary cells without cycling populations colored by pseudotime as determined by monocle3. Start of the pseudotime trajectory is marked with an arrow. i , Gene expression of selected genes over pseudotime in chromaffin cell and neuroblast trajectories.
Extended Data Fig. 4 Neuroblastoma cluster, sample and cell type contribution.
a , UMAP visualization illustrating 64.769 single neuroblastoma cells integrated using harmony and colored by cell types. b , Heat map showing expression of canonical cell type markers in cells derived from neuroblastoma tumors. Color indicates relative expression as z-score. c , UMAP embedding showing single neuroblastoma cells integrated using harmony and colored by inferred copy number status. d , Barplot with annotated cell type fractions for each neuroblastoma tumor. e , Boxplots showing expression of published adrenergic and mesenchymal neuroblastoma signatures in single neuroblastoma cells grouped by subgroup. Here, the center line represents the median, upper and lower boundaries the 75 th and 25 th percentile and whiskers the 1.5x interquartile range. Number of cells: LR: n = 21,086, ALT/TERT: n = 12,719, MES: n = 8980, MYCN: n = 16,527. f , g , UMAP plot showing neuroblastoma cells integrated using harmony and colored by clusters of transcriptionally similar cells ( f ) and sample ( g ).
Extended Data Fig. 5 Neuroblastoma copy number variations.
a–n Inferred copy number profiles of neuroblastoma cells using InferCNV with normal neuroblasts as reference. Below: Copy number profiles of the same tumors derived from whole genome sequencing data.
Extended Data Fig. 6 Similarity of single neuroblastoma cells to normal developing adrenal medullary cell populations.
a–l , Heat maps with similarity scores of single neuroblastoma cells and fetal adrenal medullary cell populations for neuroblastoma tumors not shown in Fig. 3 . m , Bar plots illustrating proportion of neuroblastoma cells assigned to adrenal medullary cells or cells from published fetal and adult brain data sets by neuroblastoma subgroup. Cells are assigned to the normal population with highest similarity score.
Extended Data Fig. 7 Similarity of single cells from neuroblastoma cell lines to normal developing adrenal medullary cell populations.
a–c , UMAP visualization of single SK-N-SH cells colored by adrenergic, mesenchymal and intermediate population ( a ), published mesenchymal neuroblastoma signature expression ( b ) or adrenergic neuroblastoma signature expression ( c ). d , Heat map with similarity scores of single SK-N-SH cells to fetal adrenal medullary cell populations. Top bar indicates SK-N-SH subpopulation identity. e , Bar plots illustrating proportion of SK-N-SH cells assigned to each normal adrenal medullary cell population. Cells are assigned to the normal population with highest similarity score. f-h , UMAP embedding of single SK-N-AS cells colored by clusters of transcriptionally similary cells ( f ), published mesenchymal neuroblastoma signature expression ( g ) or adrenergic neuroblastoma signature expression ( h ). i , Heat map with similarity scores of single SK-N-AS cells to fetal adrenal medullary cell populations. j , Bar plots illustrating proportion of SK-N-AS cells assigned to each normal adrenal medullary cell population. Cells are assigned to the normal population with highest similarity score.
Extended Data Fig. 8 Projection of single neuroblastoma cells onto adrenal medullary cell populations.
a–l , Diffusion maps of adrenal medullary cells as shown in Fig. 2a with single neuroblastoma cells projected onto the embedding for tumors not shown in Fig. 3 .
Extended Data Fig. 9 Regulation of neuroblastoma by markers of normal adrenal medullary development.
a , Dot plot showing expression of genes with strong enhancers described to engage in enhancer hijacking events in neuroblastoma, in adrenal medullary cell populations. b , Violin plots with normalized expression of adrenal medullary developmental genes in neuroblastoma subgroups. c , Heat map illustrating activity of adrenal medullary transcription factors in neuroblastoma shown as fraction of cells in which the regulon was found active by subgroup. d , UMAP embedding showing single MYCN -amplified IMR5/75 neuroblastoma cells with tetracyclin-inducible shRNAs targeting MYCN and generating MYCN high (-Tet) and MYCN low (+Tet) cells. Cells are colored by levels of regulatable MYCN. e , UMAP visualization of MYCN low and MYCN high cells colored by cell cycle phase. f , Barplot with fractions of cells in each cell cycle phase in MYCN high and MYCN low cells. g , MYCN protein levels in MYCN high and MYCN low IMR5/75 neuroblastoma cells. Detection by western blot using vinculin as loading control. Analysis was performed once on cells from the same experiment as used for single-cell sequencing. h , Violin plots show expression of signatures for Bridge (p < 2.22 × 10 −16 ), con. Progenitor cells (p < 2.22 × 10 −16 ), Chromaffin cells (p = 0.034), late Chromaffin cells (p < 2.22 × 10 −16 ), SCPs (p < 2.22 × 10 −16 ) and late SCPs (p < 2.22 × 10 −16 ) in MYCN -amplified (MYCN high) neuroblastoma cells and MYCN -amplified cells upon MYCN knockdown (MYCN low). Statistical significance was determined by two-sided Wilcoxon rank-sum test.
Extended Data Fig. 10 Association of neuroblastoma cell type composition with clinical parameters.
a , Hierarchical clustering of patient samples based on abundance of fetal adrenal medullary cell populations without cycling populations determined by deconvolution with BSEQ-sc (SEQC cohort). b , Composition of neuroblastoma tumors by subgroup based on deconvolution of bulk RNA-seq data with fetal adrenal cell populations without cycling populations using BSEQ-sc (SEQC cohort). c , Hierarchical clustering of patient samples based on abundance of fetal adrenal medullary cell populations determined by BSEQ-sc (TARGET cohort). d-i , Kaplan-Meier analysis of event-free ( d , f , h ) or overall ( e , g , i ) survival in neuroblastoma patients according to the relative abundance of late neuroblasts ( d–g ), neuroblasts ( h ) or cycling neuroblasts ( i ) determined by deconvolution of tumors with fetal adrenal cell populations. Panels f and g show deconvolution results for the TARGET cohort, panels e and i show deconvolution results for the SEQC cohort and panels d and h show deconvolution results for the SEQC cohort when excluding cycling cells from the analysis. P -values were calculated using the two-sided log-rank test.
Supplementary information
Reporting Summary (download PDF )
Supplementary Tables (download XLSX )
Supplementary Tables 1–11.
Source data
Source Data Fig. 1 (download PDF )
Unprocessed western blots.
Rights and permissions
Reprints and permissions
About this article
Cite this article
Jansky, S., Sharma, A.K., Körber, V. et al. Single-cell transcriptomic analyses provide insights into the developmental origins of neuroblastoma. Nat Genet 53 , 683–693 (2021). https://doi.org/10.1038/s41588-021-00806-1
Download citation
Received : 04 May 2020
Accepted : 29 January 2021
Published : 25 March 2021
Version of record : 25 March 2021
Issue date : May 2021
DOI : https://doi.org/10.1038/s41588-021-00806-1
Share this article
Anyone you share the following link with will be able to read this content:
Get shareable link
Sorry, a shareable link is not currently available for this article.
Copy shareable link to clipboard
Provided by the Springer Nature SharedIt content-sharing initiative
You have full access to this article via California Institute of Technology .
Associated content
Linking human sympathoadrenal development and neuroblastoma
Hermann Rohrer
Nature Genetics News & Views 08 Apr 2021
Advertisement
Explore content
Research articles
Reviews & Analysis
News & Comment
Current issue
Collections
Follow us on Facebook
Follow us on X
Sign up for alerts
RSS feed
About the journal
Aims & Scope
Journal Information
Journal Metrics
Our publishing models
Editorial Values Statement
Editorial Policies
Content Types
About the Editors
Research Cross-Journal Editorial Team
Reviews Cross-Journal Editorial Team
Web Feeds
Posters
Contact
Publish with us
Submission Guidelines
For Reviewers
Language editing services
Open access funding
Submit manuscript
Search
Search articles by subject, keyword or author
Show results from All journals This journal
Search
Advanced search
Quick links
Explore articles by subject
Find a job
Guide to authors
Editorial policies
Nature Genetics ( Nat Genet )
ISSN 1546-1718 (online)
ISSN 1061-4036 (print)
nature.com footer links
About Nature Portfolio
About us
Press releases
Press office
Contact us
Discover content
Journals A-Z
Articles by subject
protocols.io
Nature Index
Publishing policies
Nature portfolio policies
Author & Researcher services
Reprints & permissions
Research data
Language editing
Scientific editing
Nature Masterclasses
Research Solutions
Libraries & institutions
Librarian service & tools
Librarian portal
Open research
Recommend to library
Advertising & partnerships
Advertising
Partnerships & Services
Media kits
Branded content
Professional development
Nature Awards
Nature Careers
Nature Conferences
Regional websites
Nature Africa
Nature China
Nature India
Nature Japan
Nature Middle East
Privacy Policy
Use of cookies
Your privacy choices/Manage cookies
Legal notice
Accessibility statement
Terms & Conditions
Your US state privacy rights
© 2026 Springer Nature Limited
Close
Sign up for the Nature Briefing: Cancer newsletter — what matters in cancer research, free to your inbox weekly.
Email address
Sign up
I agree my information will be processed in accordance with the Nature and Springer Nature Limited Privacy Policy .
Close
Get what matters in cancer research, free to your inbox weekly. Sign up for Nature Briefing: Cancer
