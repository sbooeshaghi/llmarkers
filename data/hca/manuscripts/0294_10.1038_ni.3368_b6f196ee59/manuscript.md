The heterogeneity of human CD127+ innate lymphoid cells revealed by single-cell RNA sequencing | Nature Immunology
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
nature immunology
resources
The heterogeneity of human CD127 + innate lymphoid cells revealed by single-cell RNA sequencing
Resource
Published: 15 February 2016
The heterogeneity of human CD127 + innate lymphoid cells revealed by single-cell RNA sequencing
Åsa K Björklund ORCID: orcid.org/0000-0003-2224-7090 1 , 2 , 3 na1 ,
Marianne Forkel 4 na1 ,
Simone Picelli 1 ,
Viktoria Konya 4 ,
Jakob Theorell 4 ,
Danielle Friberg 5 ,
Rickard Sandberg ORCID: orcid.org/0000-0001-6473-1740 1 , 2 &
…
Jenny Mjösberg 4
Nature Immunology volume 17 , pages 451–460 ( 2016 ) Cite this article
34k Accesses
479 Citations
106 Altmetric
Subjects
Immunological disorders
Innate lymphoid cells
RNA sequencing
A Corrigendum to this article was published on 19 May 2016
This article has been updated
Abstract
Innate lymphoid cells (ILCs) are increasingly appreciated as important participants in homeostasis and inflammation. Substantial plasticity and heterogeneity among ILC populations have been reported. Here we have delineated the heterogeneity of human ILCs through single-cell RNA sequencing of several hundreds of individual tonsil CD127 + ILCs and natural killer (NK) cells. Unbiased transcriptional clustering revealed four distinct populations, corresponding to ILC1 cells, ILC2 cells, ILC3 cells and NK cells, with their respective transcriptomes recapitulating known as well as unknown transcriptional profiles. The single-cell resolution additionally divulged three transcriptionally and functionally diverse subpopulations of ILC3 cells. Our systematic comparison of single-cell transcriptional variation within and between ILC populations provides new insight into ILC biology during homeostasis, with additional implications for dysregulation of the immune system.
You have full access to this article via California Institute of Technology .
Similar content being viewed by others
Innate lymphoid cells and cancer
Article 28 February 2022
Heterogeneity of type 2 innate lymphoid cells
Article 30 March 2022
Transcriptomic diversity of innate lymphoid cells in human lymph nodes compared to BM and spleen
Article Open access 25 June 2024
Main
The family of innate lymphoid cells (ILCs) includes natural killer (NK) cells and several populations of non-cytotoxic ILCs, which are developmentally and functionally distinct from NK cells and express the α-chain of the interleukin 7 (IL-7) receptor (CD127). The first CD127 + ILCs to be identified were lymphoid tissue–inducer cells, which promote the organization of lymph nodes in fetal mice 1 , 2 . However, it rapidly became apparent that these cells exist also after birth and have immunoregulatory properties 3 . CD127 + ILCs have been characterized in various human mucosal and non-mucosal tissues, in which they influence both homeostasis and inflammation 4 .
Human CD127 + ILCs are commonly phenotypically identified as CD45 + cells that lack markers that define progenitor cells (CD34), B cells (CD19), T cells (CD3, TCRαβ and TCRγδ), NK cells (CD94/NKG2A), dendritic cells–macrophages (CD14, CD123, BDCA2, CD1a) and mast cells (FcɛR1α) and are thus lineage marker negative (Lin − ) 5 , 6 , 7 . In addition, the majority of human CD127 + ILCs express CD161 (refs. 5 , 7 ). Three main populations of CD127 + ILCs have been identified, and following the rationale used for naming the helper T cell family, the CD127 + ILC populations (ILC1, ILC2 and ILC3) have been named according to their profiles of transcription factors and cytokines 8 . ILC3 cells express the transcription factor RORγt and produce IL-17 and/or IL-22; ILC2 cells express the transcription factor GATA-3 and produce IL-4, IL-5 and IL-13; and ILC1 cells express the transcription factor T-bet and produce interferon-γ (IFN-γ) 4 . However, this classification is complicated by several observations. First, there is substantial plasticity among populations, with ILC3 cells and ILC1 cells interconverting depending on environmental cues 5 , 9 . Second, ILC1 cells and NK cells have overlapping phenotypes and functions but rely on separate developmental pathways 5 , 10 , 11 . Furthermore, there is probably heterogeneity within the different cell populations, exemplified by the production of IL-22, IL-17 and IFN-γ alone or in various combinations in ILC3 cell clones 6 . Hence, better understanding of ILC heterogeneity is needed to determine the role of these cells in tissue homeostasis and inflammation.
Transcriptional profiling of sorted human ILC populations 12 , 13 has identified specific population markers. However, these studies were unable to investigate the heterogeneity of gene expression, as they were performed with predefined cell populations sorted in bulk. The feasibility of high-throughput analysis of transcriptomes in single cells can circumventing such limitations 14 , 15 . Single-cell RNA sequencing (scRNA-seq) has been successfully used to newly define cell types within tissues such as the brain 16 and to investigate developmental stages 17 , 18 and tumor heterogeneity 19 . scRNA-seq has also been used to study the heterogeneity of immune responses, such as those in mouse dendritic cells 20 and T cells 21 . Exploring human ILCs at single-cell resolution could reveal important variation between and within distinct cell populations.
Here we have delineated the heterogeneity of human ILCs through scRNA-seq of several hundreds of individual CD127 + ILCs and NK cells isolated from tonsils. Unbiased clustering of cellular transcriptomes grouped cells into four distinct clusters, corresponding to ILC1 cells, ILC2 cells, ILC3 cells and NK cells, and transcriptional profiles for each ILC population were identified. The single-cell resolution revealed three transcriptionally and functionally diverse subpopulations of ILC3 cells.
Results
Unbiased single-cell transcriptome analysis of ILCs
To investigate ILC heterogeneity at the transcriptional level, we performed scRNA-seq on Lin − CD127 + ILCs and NK cells from uninfected, uninflamed tonsil tissue from three adult patients with obstructive sleep apnea syndrome ( Fig. 1a ). Tonsils contain all populations of human ILCs described so far 5 . NK cells were sorted as CD45 + Lin − CD127 − NKG2A + CD56 + CD16 − , as this represents the main NK cell population in the tonsil. We used two different flow cytometry sorting approaches to obtain Lin − CD127 + ILCs. First, we sorted individual Lin − CD127 + ILCs at random from all donors (non–pre-gated sorting). The Lin − CD127 + ILC population was clearly dominated by ILC3 cells, with low frequencies of ILC1 cells and ILC2 cells ( Fig. 1a ). To obtain sufficient cell numbers of those last two populations, we also sorted ILC1 cells and ILC2 cells (from donors b and c) as defined by flow cytometry gating (pre-gated sorting) ( Fig. 1a ). Additionally, we recorded the expression of cell-surface proteins during sorting for each individually sorted cell ( Fig. 1b ). We prepared and sequenced scRNA-seq libraries using a modified Smart-seq2 protocol 14 , with exogenous RNA controls from the External RNA Controls Consortium 'spiked' into cell lysates. After undertaking quality control ( Supplementary Fig. 1 ), we assessed the transcriptomes of a total of 648 individual cells ( Fig. 1c and Supplementary Table 1 ). We performed all transcriptional analyses on the compiled data from the two sorting strategies (pre-gated and non–pre-gated) in an unbiased manner, without taking cell-surface identity into consideration.
Figure 1: Sorting of ILCs from tonsils.
The alternative text for this image may have been generated using AI.
Full size image
( a ) Gating strategy for sorting by flow cytometry (before sorting), with ILCs defined as lineage negative (Lin − ) (CD14 − CD19 − FcɛRIα − CD3 − CD34 − CD123 − CD1a − BDCA2 − TCRα/β − TCRγ/δ − ) CD45 + NKG2A − CD127 + CD16 − ; ILC1 cells defined as CD117 − CRTH2 − ; ILC2 cells defined as CRTH2 + ; and NK cells sorted as Lin − CD45 + CD127 − NKG2A + CD16 − CRTH2 − . SSC, side scatter; FSC, forward scatter. ( b ) Surface phenotype of sorted ILC populations (after sorting; indexed data). ( c ) Quantification of sorted and analyzed cells, presented as number of cells per plate and donor (a–c); colors indicate ILC classification by flow cytometry phenotype, as determined in pre-gated sorting (*) or non–pre-gated sorting with indexed data analysis. Numbers adjacent to outlined areas ( a , b ) indicate percent cells in each. Data are representative of ( a ) or pooled from ( b , c ) three independent experiments with one donor each.
First, we identified transcripts with variation above 'technical noise' 22 ( Supplementary Fig. 2a–d ). We detected, on average, transcripts from 3,000 genes in each individual cell ( Supplementary Fig. 2d ). ILC1 cells expressed the largest number of genes, in line with these cells' being larger than those of the other ILC populations ( Supplementary Fig. 2b ). Principal-component analysis (PCA) of the expression of the 847 genes with most biological variation resulted in three main clusters ( Supplementary Fig. 2e ). However, the cells grouped more distinctly, into four clusters ( Fig. 2a ), when projected onto two-dimensions by t -distributed stochastic neighbor embedding ( t -SNE) 23 , and the clusters were robust to bootstrapping ( Fig. 2b ). In the plotting, each cell was assigned a color according to its surface phenotype, inferred from the abundance of surface proteins during indexed sorting; this showed that ILC phenotype was in good agreement with the unbiased single-cell transcriptome clustering ( Fig. 2a ). ILC1 cells had the greatest frequency of mismatch between surface phenotype and transcriptional profile, with 24 of 132 (18%) of ILC1 cells (by phenotype) clustering with ILC3 cells, ILC2 cells or NK cells (by transcriptional profile) ( Fig. 2a ); this probably reflected the fact that ILC1 cells were sorted on the basis of a lack of cell-surface markers. Of note, some ILC1 cells (by phenotype) that did not cluster with ILC1 cells showed low expression of the 50 transcripts that most strongly defined the individual clusters ( Supplementary Fig. 3a ). These observations could not be explained by the sorting of multiple cells in the same well, since the preparation of cDNA libraries from two cells would have, on average, doubled the RNA content ( Supplementary Fig. 3b ). Instead, these cells might have been immature or in transition between two cell types. For subsequent analyses we relied on transcriptional clustering, as this was transcriptome wide, in contrast to the abundance measured for only 15 surface proteins by flow cytometry.
Figure 2: t -SNE and clustering of ILC and NK cell populations.
The alternative text for this image may have been generated using AI.
Full size image
( a ) t -SNE analysis of cells ( n = 648) from donors a–c; colors indicate marker phenotype, and symbols indicate donor origin (key). Each symbol represents an individual cell. ( b ) Clustering of cells on the basis of 20 iterations of t -SNE with bootstrap values from the R software package pvclust: dendrogram height indicates dissimilarity between clusters; numbers in plot indicate approximately unbiased P value (red) and bootstrap probability value (green); bar at bottom indicate cell phenotype (colors match key in a ). ( c ) Expression (log 2 RPKM (reads per kilobase of exon model per million mapped read) values) of known cell type–specific genes (right margin, d ); left margin, cell phenotype (key in a ). ( d ) Expression distribution (violin plots) in each cell population (log 2 RPKM values); colors indicate mean expression. Data are from three independent experiments with one donor each.
Next we explored the four clusters of cells and confirmed their cellular identity by their elevated expression of known cell population–specific transcripts (e.g., GATA3 in ILC2 cells, RORC in ILC3 cells, GZMA in NK cells, and CXCR3 in ILC1 cells) ( Fig. 2c,d ). These analyses showed that individual cells in a population displayed highly variable transcriptomes ( Fig. 2c,d ), a finding that could not have been revealed by traditional transcriptome analysis of bulk cell populations. The scRNA-seq profiles were rich in variability, as observed before 20 , with detection of marker transcripts in only a fraction of cells per cell population. For several of the marker transcripts, including CCL3 and IL22 , this should have represented true biological variation and not 'technical noise' (as determined by the variation in expression of exogenous 'spiked-in' RNA; Supplementary Fig. 2a ), as these transcripts had high expression in few cells ( Fig. 2c,d ). However, for marker transcripts with low or medium expression, this could have been mainly a consequence of incomplete sampling of RNA molecules. In summary, unbiased transcriptional clustering revealed four distinct populations, corresponding to ILC1 cells, ILC2 cells, ILC3 cells and NK cells, with highly variable transcriptomes.
Single-cell protein and mRNA abundance in ILCs
The recording of protein abundance on single cells during flow cytometry sorting enabled us to explore patterns of protein and RNA expression in single ILCs. Single-cell level analyses have shown protein abundance and RNA abundance to be uncorrelated in prokaryotes 24 . NKp44 protein (a cytotoxicity receptor) and its transcript ( NCR2 ) were co-expressed in many cells ( Fig. 3a ). In other cells, we observed NKp44 protein but a lack of (or low levels of) NCR2 RNA ( Fig. 3a ), which probably reflected the longer half-life of the protein relative to that of the RNA transcripts 25 . While protein-versus-RNA correlation was good for NKp44- NCR2 (Spearman correlation coefficient ( r ) = 0.63), correlations for other proteins and transcripts ranged from 0.19 to 0.62 ( Supplementary Fig. 4 ). Correlating the expression of all seven of the expressed proteins used for sorting and their corresponding RNA within individual cells revealed moderate correlations (average r value, 0.66). We observed a strong correlation ( r = 0.93) when we compared mean protein expression and RNA expression across all cells ( Fig. 3b ), in agreement with the general correlation between protein abundance and RNA abundance in bulk-cell population analyses. We next sought to identify the lowest number of cells needed to reach a correlation between protein abundance and RNA abundance. Random sub-sampling of an increasing number of cells revealed that as few as 10 cells provided a good correlation, whereas correlation coefficients plateaued at approximately 100 cells ( Fig. 3c ). Thus, although single-cell protein abundance and RNA abundance were only weakly correlated, only a few cells were needed for clear correlations to appear.
Figure 3: Protein-versus-RNA correlations.
The alternative text for this image may have been generated using AI.
Full size image
( a ) NKp44 mean fluorescence intensity (MFI) versus NCR2 mRNA expression for all cells (as in Fig. 1 ; n = 648); results normalized with greatest value set as 1. Spearman correlation: r = 0.63. ( b ) Protein intensity versus mRNA expression, presented as mean in all cells for each gene ( n = 7; protein designations in plot)). Spearman correlation: r = 0.93. ( c ) Correlation between protein expression and mRNA expression for a subsampling of cells (1,000 iterations). Data are from three independent experiments with one donor each (error bars ( c ), s.d.).
Differential RNA expression of CD127 + ILCs and NK cells
Having identified four clusters of cells corresponding to ILC1 cells, ILC2 cells, ILC3 cells and NK cells, we next set out to investigate the shared and distinct transcriptional signatures of each cell population (complete list of differentially regulated genes, Supplementary Data Set 1 ) according to analysis with the SCDE ('single-cell differential expression') software package. We identified genes with significantly higher expression in CD127 + ILCs than in NK cells that did not have differential expression in the different CD127 + ILC populations. We performed this analysis separately for all genes (13 transcripts; Fig. 4a and Supplementary Fig. 5a ) and for genes encoding transcription factors (14 transcripts; Fig. 4b and Supplementary Fig. 5b ). Among transcripts shared by all CD127 + ILCs were RARG , which encodes a receptor (RARγ) for retinoic acid (RA), and RORA , which encodes the 'orphan' receptor RORα ( Fig. 4b and Supplementary Fig. 5b ); the latter is reported to be expressed by all ILC populations in small intestinal lamina propria in mice 26 . These data suggested that CD127 + ILCs were commonly regulated by retinoic acid, as shown for mouse ILC3 cells 27 , as well as by cholesterol and its derivatives acting on RORα. Notably, expression of ZBTB16 , which encodes the transcription factor PLZF, was not restricted to the CD127 + ILC common program, as it was detected in all ILCs, including NK cells ( Fig. 4b ). In confirmation of that finding, analysis of intracellular PLZF protein by flow cytometry revealed that PLZF was expressed in all ILC subsets ( Fig. 4c,d ). In mice, mature ILC subsets do not express PLZF 11 , which indicates that PLZF expression is regulated differently in mice and humans.
Figure 4: Genes commonly expressed by all CD127 + ILC populations.
The alternative text for this image may have been generated using AI.
Full size image
( a , b ) Expression distribution (violin plots) in each population (horizontal axes), for known and previously unknown CD127 + ILC genes ( a ) or transcription factor–encoding genes of CD127 + ILCs ( b ) (differential expression according to SCDE analysis); colors indicate mean expression (key). P < 0.05 ( b ) and P < 0.001 ( a ) (multiple-testing corrected). NS, not significant differential expression (according to SCDE). ( c , d ) Flow cytometry of intracellular PLZF in adult tonsil ILCs ( c ) and mean fluorescence intensity of PLZF in those cells ( d ). CD3 + PLZF + cells (far right, d ) serve as a positive control. Each symbol ( d ) represents an individual donor; small horizontal lines indicate the mean (± s.d.). FMO, fluorescence-minus-one control. Data are from three independent experiments with one donor in each.
NK cells showed significantly higher expression of 59 transcripts than that of CD127 + ILCs ( Supplementary Fig. 5c and Supplementary Data Set 1 ). Of those, 39 genes were immediately linked to NK cell activity or have been reported to be expressed by mouse or human NK cells 28 , 29 ( Supplementary Fig. 5c ) . As expected, the majority (28 of 39) of these transcripts encoded proteins involved in cytotoxic function ( Supplementary Fig. 5c ). The remaining 20 transcripts were, to our knowledge, not previously known to be expressed by human NK cells, including HOPX and PLEK , which are expressed by NK cells in mice 28 ( Supplementary Fig. 5d ). In summary, the unique transcriptomes of CD127 + ILCs and NK cells might provide clues about the origin and function of these two major populations of human ILCs.
Differential RNA expression of human ILC1 cells
To identify molecules and pathways unique to the three CD127 + ILC populations, we compared the differential expression profile of genes upregulated in each CD127 + ILC population with that of the combined expression profile of genes upregulated in the other two CD127 + ILC populations pooled together. We excluded NK cells from differential expression analysis, as they express several transcription factors and cytokines that are characteristic of ILC1 cells. ILC1 cells showed significantly elevated expression of 79 genes, including CXCR3 and IFNG , which are signature transcripts for human ILC1 cells 5 ( Fig. 5 and Supplementary Data Set 1 ). Additional genes that serve as markers for human ILC1 cells, such as IL12RB , LTA and TBX21, were not expressed differentially in ILC1 cells. Of note, TBX21 was expressed by only 4 of 114 ILC1 cells, which prevented us from performing meaningful correlation studies of TBX21 and potential target genes of T-bet (the transcription factor encoded by TBX21 ). The low frequency of TBX21 expression in ILC1 cells paralleled published reports of low expression of T-bet protein in freshly isolated tonsil bulk ILC1 cells 5 . Notably, ILC1 cells had significantly higher expression of IKZF3 , which encodes the transcription factor Aiolos that has been suggested to function as a negative regulator of mouse NK cell function 30 and might serve as a functional target and useful marker for ILC1 cells.
Figure 5: ILC1-specific genes.
The alternative text for this image may have been generated using AI.
Full size image
Expression distribution (violin plots) in each cell population for ILC1-specific genes, grouped into functional categories (left margin) according to the function of their products (differential expression determined by SCDE). P < 0.001 (multiple-testing corrected). Data are from three independent experiments with one donor in each.
Furthermore, ILC1 cells expressed IFNG-AS1 and IL18BP ( Fig. 5 ); these encode IFN-γ antisense RNA and IL-18-binding protein, respectively, which might restrict ILC1 function in homeostatic conditions. ILC1 cells also expressed IL6R and IL6ST , which encode the two functional subunits of the IL-6 receptor (the α-subunit (CD126) and β-subunit (CD130), respectively). They also expressed SOCS3 , which encodes a signaling molecule downstream of IL-6, known to inhibit signaling via the kinase JAK and STAT transcription factors. Collectively, these pathways might represent mechanisms used by ILC1 cells to control their own activity.
Unexpectedly, ILC1 cells showed differential expression (higher than that of the other ILCs, according to SCDE analysis) of 11 transcripts encoding variable regions of the T cell antigen receptor (TCR) ( Fig. 5 , Supplementary Fig. 6a and Supplementary Data Set 1 ). This finding was notable, given the observation that mouse ILCs express germline-encoded transcripts for TCRγ 26 . Among other differentially expressed transcripts with higher expression in ILC1 cells were those from other genes typically expressed by T cells, including CD4 , CD5 , CD6 , CD28 , CD27 and CCR7 ( Fig. 5 ). Furthermore, ILC1 cells expressed several transcripts encoding members of the tumor-necrosis factor (TNF) receptor and TNF superfamilies, including TNFRSF1B (which encodes TNF receptor 2), TNFRSF10A (which encodes the receptor for the apoptosis-inducing cytokine TRAIL) and TNFSF8 (which encodes the cytokine CD30L) ( Fig. 5 ). In conclusion, ILC1 cells displayed a heterogeneous expression pattern and expressed transcripts previously not known to be expressed by ILC1 cells, such as those encoding various molecules involved in regulating IFN-γ production.
Differential RNA expression of human ILC2 cells
Similar analyses of ILC2 cells identified 58 genes with significantly elevated expression, including genes encoding several previously reported ILC2 markers, such as PTGDR2 (which encodes the prostaglandin D 2 receptor CRTH2), IL1RL1 (which encodes the IL-33 receptor), IL17RB (which encodes the IL-25 receptor), KLRG1 (which encodes the activation marker KLRG1) and GATA3 (which encodes the transcription factor GATA-3) ( Fig. 6a and Supplementary Data Set 1 ). In addition to identifying GATA3 , we identified a set of transcription factor–encoding genes whose expression was significantly elevated in ILC2 cells, including the gene encoding MAF, which is involved in IL-4 production, and the gene encoding KLF7, which is involved in hematopoiesis. However, IL13 transcripts were detected in only 6 of 143 ILC2 cells, whereas IL5 , IL4 and IL9 transcripts were not detectable at all, which suggested that ILC2 cells needed to be activated to express these transcripts.
Figure 6: ILC2-specific genes.
The alternative text for this image may have been generated using AI.
Full size image
( a ) Expression distribution (violin plots) in each cell population for ILC2-specific genes (presented as in Fig. 5 ). P < 0.001 (multiple-testing corrected). ( b , c ) Flow cytometry of intracellular TCF-1 in adult tonsil ILCs ( b ) and mean fluorescence intensity of TCF-1 in those cells ( c ). CD3 + TCF-1 + cells (far right, c ) serve as a positive control. Each symbol ( c ) represents an individual donor; small horizontal lines indicate the mean (± s.d.). Data are from three independent experiments with one donor in each.
ILC2 cells are regulated by the lipid mediators prostaglandin D 2 (refs. 31 , 32 ) and LXA 4 (ref. 31 ). It was therefore notable that ILC2 cells showed differential expression (higher than that of the other ILCs, according to SCDE analysis) of several transcripts encoding proteins involved in the synthesis and breakdown of prostaglandins and the response to prostaglandins ( Supplementary Data Set 1 ). These included transcripts encoding hematopoietic prostaglandin D synthase ( HPGDS ), hydroxyprostaglandin dehydrogenase 15-(NAD) ( HPGD ), the transcription factor PPARγ ( PPARG ) and the prostaglandin E 2 receptor EP2 ( PTGER2 ) ( Fig. 6a ). In the ILC2 population, GATA3 expression was correlated with that of PTGER2 , as well as that of several other transcripts uniquely expressed by ILC2 cells, including MAF , IL17RB , HPGDS and FCRL3 ( Supplementary Data Set 2 ); this identified these genes as potential targets of GATA-3 in ILC2 cells.
It has been shown that the in vitro differentiation of human ILC2 cells is driven by Notch signaling 33 . Notch signaling induces TCF-1 (encoded by TCF7 ), a transcription factor that promotes the development of mouse ILC2 cells 34 , 35 . We found TCF7 expression in fewer human ILC2 cells (72 of 143 ILC2 cells) than cells in the other ILC populations (426 of a total of 505 ILC1, ILC3 and NK cells) ( Fig. 6a ), a result confirmed by intracellular staining of TCF-1 protein ( Fig. 6b,c ). ILC2 cells also expressed TLE4 ( Fig. 6a ), which encodes a member of the Groucho family of co-repressors that is part of the Notch signaling pathway 36 and has been shown to repress IFN-γ expression through epigenetic changes of IFNG regulatory elements 37 . These data supported the proposal of a role for Notch signaling, potentially via induction of TLE4 and regulation of IFN-γ production, in human ILC2 cells during homeostasis. In addition, ILC2 cells showed upregulation of the expression of various transcripts encoding molecules involved in environmental sensing, such as CD150 ( SLAMF1 ), the purinergic receptor P2Y ( P2RY1 ), CD137 ( TNFRSF9 ), CD11b ( ITGAM ) and CD95L ( FASLG ) ( Fig. 6a ), which might have important functions in ILC2 biology. Collectively, our analyses revealed a transcriptional signature suggestive of important roles for prostaglandins, the Notch system and environment-sensing receptors in ILC2 function.
Differential RNA expression of human ILC3 cells
Analysis of ILC3 cells revealed 371 genes that were significantly upregulated ( Supplementary Data Set 1 ). This greater number of genes with significantly higher expression (371 genes for ILC3 cells, versus 79 genes for ILC1 cells and 58 genes for ILC2 cells) was not due to a greater number of cells in this population ( Supplementary Fig. 6b ). We focused our attention on the 85 genes annotated as 'immune genes' by gene ontology; these included genes encoding previously described transcription factors and cytokine receptors. Among such transcripts were ID2 , RORC , AHR , TOX , TOX2 and IKZF2, and IL2RB , LTBR , IL1R1 and IL23R 3 , 6 , 38 ( Fig. 7 ). RORC expression correlated with that of various notable transcripts, including, as expected, IL23R (which encodes the receptor for IL-23) ( Supplementary Data Set 2 ). Of note, transcripts encoding the archetypical cytokines produced by ILC3 cells (IL-17 and IL-22) were expressed by few ILC3 cells (for IL17 , 0 of 320 ILC3 cells (data not shown), and for IL22 , 19 of 320 ILC3 cells ( Fig. 7a )), indicative of strict homeostatic control of these cytokine transcripts.
Figure 7: ILC3-specific genes.
The alternative text for this image may have been generated using AI.
Full size image
Expression distribution (violin plots) in each cell population for ILC3-specific genes (presented as in Fig. 5 ). P < 0.001 (multiple-testing corrected). Data are from three independent experiments with one donor in each.
ILC3 cells showed differential expression (higher than that of the other ILCs, according to SCDE analysis) of transcripts encoding products involved in three key signaling pathways regulated by ligands of the receptors c-Kit, Notch and NKp44 ( Fig. 7 ). In addition to expressing KIT (which encodes c-Kit), ILC3 cells expressed several genes encoding products associated with c-Kit signaling, including PTPN6 , FES and LYN . Furthermore, ILC3 cells showed upregulation of many genes encoding molecules of the Notch pathway, including the ligands DLL1 and JAG2, the proteinase ADAM10, the intracellular signaling molecule RBPJ and the transcription factor TCF-1, which emphasized the possibility of a central role for the Notch pathway in human ILC3 cells, as has been demonstrated for mouse ILC3 cells 34 , 39 , 40 .
ILC3 cells showed differential expression (higher than that of the other ILCs, according to SCDE analysis) of NCR2 (which encodes NKp44) and a set of transcripts encoding products associated with signaling via NKp44 and immunoreceptor tyrosine-based activation motifs, which has shown to induce an inflammatory program in ILC3 cells 12 ( Supplementary Data Set 1 ). Differentially upregulated transcripts encoding products in the NKp44 signaling motif included TYROBP (which encodes DAP12), FGR and LYN (which encode kinases of the Src family) and SYK , PLCG2 , VAV3 , LAT2 and CLNK (which encode signaling molecules downstream of NKp44) ( Fig. 7 ). Furthermore, ILC3 cells expressed NRP1 (which encodes neuropilin-1), PECAM1 (which encodes the immunoreceptor tyrosine-based inhibitory motif–containing molecule CD31), AMICA1 (which encodes a γδ T cell–associated molecule), EREG (which encodes a growth factor) and KLRF2 (which encodes the C-type lectin–like receptor NKp65); the roles of these gene products are uncharacterized in ILC3 cells. Overall, ILC3 cells expressed transcripts encoding molecules involved in signaling via c-Kit, NKp44 and Notch, as well as various transcripts encoding products of unknown function in ILC3 cells.
Three subpopulations of transcriptionally distinct ILC3 cells
To address the issue of ILC3 heterogeneity in an unbiased manner and to potentially identify previously unknown ILC3 populations, we performed PCA and t -SNE analyses of 1,958 genes annotated as 'immune genes' ( Fig. 8a,b and Supplementary Fig. 7a ). The analyses separated the cells into three clusters ( Fig. 8b,c ). One cluster (cluster A) showed enrichment for cells expressing the gene encoding NKp44 ( NCR2 ) and the gene encoding its downstream signaling molecule DAP12 ( TYROBP ) ( Fig. 8a,d and Supplementary Fig. 7a,b ). Cluster A also showed enrichment for transcripts encoding products associated with cytoskeletal functions, including ARPC5 and CORO1A , and intracellular protein processing, including PSMB10 , CTSD , CANX , DDOST , ARF1 and SEC61B ( Supplementary Fig. 7a ). Hence, cluster A seemed to represent a set of activated ILC3 cells that corresponded to the published tonsil NKp44 + ILC3 population 5 , 12 , 41 .
Figure 8: ILC3 subpopulations determined by RNA expression, surface protein expression and intracellular cytokine expression.
The alternative text for this image may have been generated using AI.
Full size image
( a ) PCA of all ILC3 cells (circles); crosses and adjacent; labels in plot indicate 'loadings' (contribution to each principal component (PC1 or PC2)) for selected genes. ( b – f ) t -SNE analysis of RNA expression in ILC3 cells: colors indicate cluster definition ( b ); donor origin ( c ); expression of NCR2 , KIT , CD3E mRNA and fluorescence intensity of NKp44 protein ( d ); number of genes detected, forward scatter (FSC) by flow cytometry, and expression of SELL mRNA ( e ); and expression of HLA-DRA , HLA-DRB1 , HLA-DP1 and IL1R1 mRNA ( f ) (same scale for all color intensity for RNA expression). ( g , h ) t -SNE analysis ( g ) and overlap ( h ) of protein expression (assessed by flow cytometry) in adult and pediatric tonsils, with ILC3 cells sequentially gated on NKp44, CD62L (NKp44 − ) and HLA-DR (NKp44 − CD62L − ) ( g ), and overlap in protein expression presented frequency (%) of ILC3 cells ( h ). ( i ) Mean frequency of NKp44 + , CD62L + or HLA-DR + cells (above plots) positive for various combinations of GM-CSF, TNF, IL-2, IL-17F or IL-22 (key) after stimulation for 6 h with PMA plus ionomycin (PMA + iono) (top row) or stimulation for 12 h with IL-23 plus IL-1β followed by stimulation for 6 h with PMA plus ionomycin (bottom row); 'slice' size indicates frequency of cytokine-expressing cells; shades of gray indicate different combinations of cytokine expression; 'arcs' along periphery indicate mean frequency of cells expressing each cytokine (colors match key). Data are from three independent experiments with one donor in each and n = 320 total ILC3 cells ( a – f ), nine independent experiments with one or two donor(s) in each and n = 20,543 total ILC3 cells ( g , h ) or six independent experiments with one adult or pediatric donor in each ( i ).
Cells in cluster B were smaller than the rest of the ILC3 cells and also expressed fewer transcripts than the rest of the ILC3 cells did ( Fig. 8e ). This cluster showed enrichment for cells expressing SELL (which encodes L-selectin (CD62L)) ( Fig. 8a,e and Supplementary Fig. 7a ). Hence, this cluster potentially represented a naive ILC3 subpopulation.
A third cluster (cluster C) showed enrichment for cells expressing HLA-encoding transcripts, including HLA-DRA , HLA-DRB1 , HLA-DRB5 , HLA-DPA1 and HLA-DPB1 ( Fig. 8a,f and Supplementary Fig. 7a,b ), and might have been the human equivalents of the MHCII + ILC3 cells that regulate gut commensal–specific CD4 + T cells in mice 42 , 43 . This cluster also showed expression of transcripts encoding the IL-1β receptor ( IL1R1 ), the apoptosis-inducing cytokine TRAIL ( TNFSF10 ) and the intracellular signaling molecule PRAM1 (the retinoic acid–induced gene PRAM1 ) ( Fig. 8a,f and Supplementary Fig. 7a,b ). Our data also indicated that among these human tonsil ILC3 cells there might have been a subpopulation of ILC3 cells with the ability to present antigen. Indeed, expression of CD74 (which encodes the invariant chain) and CTSS (which encodes cathepsin S, responsible for cleavage of the invariant chain) ( Supplementary Fig. 7b ) indicated that such a function might be plausible. The lack of expression of genes encoding the costimulatory molecules CD80 and CD86 in all ILC populations (data not shown) suggested that, as reported for mice 42 , 43 , human ILC3 cells would be unable to provide classic co-stimulatory signals.
Three subpopulations of functionally diverse ILC3 cells
In confirmation of the transcriptional findings, t -SNE analysis of flow cytometry data revealed that the expression of CD62L and that of NKp44 were largely mutually exclusive, which identified two distinct ILC3 subpopulations ( Fig. 8g,h and Supplementary Fig. 8a ). Strengthening our idea that CD62L + ILC3 cells represented naive ILC3 cells, this subpopulation expressed CD45RA, a marker of naive cells ( Supplementary Fig. 8a ). HLA-DR showed a less restrictive expression pattern, as it was expressed by both NKp44 − ILC3 cells and NKp44 + ILC3 cells ( Supplementary Fig. 8a ).
To address the functionality of NKp44 + ILC3 cells, CD62L + ILC3 cells and HLA-DR + ILC3 cells, we sorted these subpopulations and performed simultaneous intracellular detection of six different cytokines (IL-2, IL-17F, IL-22, GM-CSF, TNF and IFN-γ) after stimulation of cells with the phorbol ester PMA plus ionomycin with or without IL-23 plus IL-1β. The majority of the cells in all subpopulations produced GM-CSF ( Fig. 8i ), whereas very few cells produced IFN-γ (data not shown), and there were no differences among the subpopulations in terms of their production of these two cytokines ( Fig. 8i and data not shown). Analysis of multi-functionality by Boolean gating and SPICE software 44 revealed that, as expected, the NKp44 + ILC3 cells showed the most diverse functionality, with more cells producing IL-2 and IL-22 in this population than in the other two subpopulations ( Fig. 8i and Supplementary Fig. 8b,c ). Fewer CD62L + ILC3 cells than NKp44 + ILC3 cells produced IL-22 and IL-2 ( Fig. 8i and Supplementary Fig. 8b,c ). In contrast to both HLA-DR + ILC3 cells and NKp44 + ILC3 cells, CD62L + ILC3 cells did not respond to stimulation with IL-23 plus IL-1β ( Fig. 8i and Supplementary Fig. 8b,c ), despite their expression of both IL23R ( Supplementary Fig. 7b ) and IL1R1 ( Fig. 8f ). These data supported the idea that CD62L + ILC3 cells might represent a subpopulation of transcriptionally less active, possibly naive cells. Notably, more HLA-DR + ILC3 cells than NKp44 + or CD62L + ILC3 cells produced IL-17F ( Fig. 8i and Supplementary Fig. 8b,c ).
In summary, through single-cell analyses of transcriptional expression, we identified three transcriptionally distinct subpopulations of ILC3 cells, defined by the expression of transcripts encoding NKp44, CD62L, and HLA-DR and HLA-DP chains, respectively. Sorted subpopulations of HLA-DR + and NKp44 + ILC3 cells were responsive to IL-23 plus IL-1β and, as expected, the majority of NKp44 + ILC3 cells produced GM-CSF, TN)F, IL-2 and IL-22. HLA-DR + ILC3 cells produced mainly GM-CSF, IL-2 and, to a lesser extent, TNF and IL-22. The frequency of IL-17 + cells, albeit generally low, was greatest in the HLA-DR + subpopulation. CD62L + ILC3 cells were unresponsive to IL-23 plus IL-1β and produced only GM-CSF, TNF and IL-2 at a low frequency. These data suggested previously unrecognized transcriptional and functional diversification of ILC3 cells in humans.
Discussion
Here we have delineated the heterogeneity of human ILCs through scRNA-seq of several hundreds of individual CD127 + ILCs from tonsils. Unbiased clustering of cellular transcriptomes grouped cells into four distinct clusters that resembled ILC1 cells, ILC2 cells, ILC3 cells and NK cells. Hierarchical clustering revealed that human ILC3 cells and NK cells, as well as ILC1 cells and ILC2 cells, clustered in separate branches of the dendrogram. In mice, hierarchical clustering based on transcriptome data of ILCs sorted in bulk has shown that intestinal and splenic CD127 + ILC1 cells cluster with NK cells and cytotoxic intraepithelial ILC1 cells 26 . This might reflect species or organ differences or the different technologies used (scRNA-seq versus microarray). Although we cannot completely rule out the possibility of the existence of additional transcriptionally distinct ILC populations, such ILC populations would have to be rare, as it is possible that a few rare cells could be artificially 'dragged' into larger cell populations during t -SNE analysis.
We identified several molecules that, to the best of our knowledge, have not previously been reported as being expressed by the various ILC populations; future experiments are warranted to provide functional insight into these. Furthermore, the single-cell profiling allowed us to transcriptionally delineate heterogeneity within ILC populations. We explored the transcriptional profile of ILC1 cells, which in humans might be a mixture of ILC1 cells derived from ILC3 cells ('ex-ILC3 cells') 5 and true ILC1 cells 10 ; the latter are yet to be identified in humans. Initially, we analyzed CD161 + and CD161 − ILC1 subpopulations separately but found no global differences in transcriptional profiles and therefore did not distinguish these cell subpopulations in subsequent analyses. The ILC1 population showed enrichment for cells expressing genes encoding TCR variable regions, as well as transcripts encoding the invariant signaling protein CD3. Expression of these genes was scattered throughout the ILC1 population and was not clustered in one subset of cells, which indicated that T cell contamination was unlikely explanation for this. Mouse ILCs have been shown to express transcripts encoding the TCRγ chain but lack TCRγ protein itself 26 . Furthermore, Notch signaling can induce intracellular expression of CD3ɛ in NK cells 45 . Hence, expression of the loci encoding the TCR α-chain variable region, β-chain variable region and CD3 in ILC1 cells might reflect the relatively similar developmental programs of ILC1 cells, NK cells and T cells.
Two subpopulations of ILC2 cells have been characterized in mice 46 . In addition to the 'natural' ILC2 cells present during homeostasis, an inflammatory, plastic ILC2 subpopulation is induced upon administration of IL-25 or helminthic infection. The natural ILC2 cells are characterized as IL-33R + IL-25 + KLRG1 int or IL-33R + IL-25 − KLRG1 int , whereas the inflammatory, plastic IILC2 cells are IL-33R − IL-25 + KLRG1 hi . In our study, assessing the overall expression profile or narrowing it down to expression of IL1RL1 , IL17RB and KLRG1 did not reveal any distinct subpopulations of ILC2 cells. Few cells fell into the definition of natural ILC2 cells or inflammatory, plastic ILC2 cells. In fact, most ILC2 cells lacked expression of both IL1RL1 and IL17RB . Assessing ILC2 heterogeneity in a type 2–inflamed tissue such as asthmatic lungs might be more relevant.
While exploring the heterogeneity of ILC3 cells, we identified a cell cluster that showed enrichment for cells expressing NCR2 transcripts and NKp44 protein, as well as KIT , that most probably corresponded to the reported human NKp44 + ILC3 subpopulation 41 , as it clearly responded to IL-23 plus IL-1β by producing IL-22. Another cluster of ILC3 cells was characterized by expression of SELL (which encodes CD62L), known to be expressed by naive and central memory T cells. This subpopulation showed enrichment for small cells that expressed very few transcripts. Hence, this cluster might represent a set of transcriptionally less active, naive ILC3 cells. By flow cytometry we verified the existence of a subpopulation of ILC3 cells that expressed CD62L protein. CD62L + ILC3 cells were unresponsive to stimulation with IL-23 plus IL-1β, and even in the presence of PMA plus ionomycin, they produced IL-2 relatively infrequently and produced neither IL-22 nor IL-17F. These cells also expressed CD45RA, which further suggested they were naive. Notably, CD45RA was more widely expressed than was CD62L, a result possibly explained by cleavage of surface CD62L. It is possible that CD45RA, which is generated via post-translational modifications of CD45 and therefore cannot be analyzed at the transcriptional level, is an alternative surface marker for this naive subpopulation of ILC3 cells. Exploring the differentiation potential of naive ILC3 cells is a topic for future investigation.
A third subpopulation of ILC3 cells was characterized by the expression of several transcripts encoding HLA-DR and HLA-DP chains. This subpopulation might have been the human equivalent of the mouse ILC3 cells that express major histocompatibility complex class II and exert homeostatic control of T cells in the intestine 42 , 43 . Paralleling our finding of IL1R1 expression in this subpopulation, mouse ILC3 cells that express major histocompatibility complex class II are mostly NKp44 − and produce IL-22, which would indicate that this subset might be enriched for cells that express the IL-1β receptor, known to regulate IL-22 production. Indeed, our investigation showed that HLA-DR + ILC3 cells responded to stimulation with IL-23 plus IL-1β by producing IL-22, albeit at a lower frequency than did NKp44 + ILC3. Notably, HLA-DR + ILC3 cells showed more IL-17F production following stimulation with IL-23 plus IL-1β than did NKp44 + or CD62L + ILC3 cells, a finding with implications for several mucosal inflammatory conditions. Future studies should aim at exploring the antigen-presentation ability of this subset in humans, as has been shown in mice 42 , 43 .
Collectively, our assessment of ILC3 heterogeneity revealed three transcriptionally and functionally diverse subpopulations of ILC3 cells. Of these, CD62L + ILC3 cells and HLA-DR + ILC3 cells have not been described at the transcriptional or functional level in humans, to our knowledge. Further understanding of the functionality of these subpopulations, and the plasticity among them, in different inflammatory settings should follow. In conclusion, our scRNA-seq analysis of the human CD127 + ILC compartment has revealed many molecular pathways and components with elevated expression in particular ILCs and has identified three transcriptionally and functionally diverse subpopulations of ILC3 cells. These molecular findings will add to the understanding of ILC biology in homeostasis, with implications for tissue inflammation.
Methods
Cell isolation from tonsils.
Tonsils were received fresh from adult patients (age 20–65 years) or pediatric patients (age 2–7 years) given tonsillectomy due to obstructive sleep apnea syndrome. For transcriptional analysis, donor A was 56 years of age, donor B was 44 years of age, and donor C was 23 years of age . All surgeries were performed at Karolinska University Hospital, Huddinge. Permission to collect these unidentified tissues was obtained from the regional ethical board at Karolinska Institutet. All patients, or their parents if they were younger than 18 years, gave informed consent. Whole tonsils were cut into small pieces and ground through a 100-μm cell strainer using a plunger of a plastic syringe. The obtained cell suspension was filtered through a 40-μm cell strainer, resuspended in 20 ml PBS and added on top of 20 ml lymphoprep (Axis Shield). After centrifugation for 20 min at 400 g , the mononuclear cell layer was recovered and washed once in 50 ml PBS, and a maximum of 1 × 10 9 cells used for depletion of CD3 + cells, CD19 + cells and CD14 + cells (only for subsequent sorting of ILC3 subsets) via magnetic-activated cell sorting. For depletion, 5 × 10 8 mononuclear cells were resuspended in 1 ml MACS buffer (PBS, supplemented with 2 mM EDTA and 0.5% FCS), stained with 62.5 μl fluorescein isothiocyanate (FITC)-conjugated anti-CD3 (SK7; BioLegend) and anti-CD19 (4G7; BD Biosciences) and anti-CD14 (TüK4; Invitrogen) and incubated for 30 min at 4 °C. Cells were then washed in 50 ml MACS buffer by centrifugation at 400 g for 5 min and resuspended in 1 ml MACS buffer. Cells were incubated with 250 μl anti-FITC microbeads (Miltenyi Biotech) for 30 min at 4 °C, washed as described above, resuspended in 1 ml MACS buffer and added to a LD separation column (Miltenyi Biotech) Flow-through was collected.
Flow cytometry analysis and sorting.
For flow cytometry analysis, mononuclear cells from tonsils were incubated with antibodies (identified below) for 30 min at 4 °C, washed in flow cytometry buffer (FC buffer, PBS, supplemented with 2 mM EDTA and 2% FCS), fixated in 2% paraformaldehyde in PBS for 10 min, washed and resuspended in FC buffer. The following FITC-conjugated antibodies were used for defining lineage marker–positive cells: anti-CD14 (TÜK4; Invitrogen); anti-FcɛRIα (AER-37 (CRA-1)), anti-CD34 (581), anti-CD123 (6H6), anti-CD1a (HI149), anti-TCRαβ (IP26), CD94 (DX22) and anti-TCRγδ (B1) (all from BioLegend); anti-BDCA2 (AC144; Miltenyi Biotech) and anti-CD19 (4G7; BD Biosciences). Additional surface staining was performed using the following antibodies: Brilliant Violet 605–conjugated anti-CD161 (HP-3G10); Brilliant Violet 711–conjugated anti-CD56 (HCD56) and Alexa Fluor 700–conjugated anti-CD45 (HI30), Brilliant Violet 785–conjugated anti-CD3 (OKT3) and allophycocyanin (APC)–indotricarbocyanine (Cy7)–conjugated anti-CD45RA (HI100) (all from BioLegend); BD Horizon V450–conjugated anti-CRTH2 (BM16; BD Biosciences); phycoerythrin (PE)–indodicarbocyanine (Cy5)–conjugated anti-NKp44 (Z231), PE-Cy5–conjugated anti-CD117 (104D2D1), PE–indotricarbocyanine (Cy7)–conjugated anti-CD127 (R34.34), PE–Texas Red–conjugated anti-CD62L (DREG56) (all from Beckman Coulter); and PE-conjugated anti-HLA-DR (LN3; eBioscience). In addition, cells were stained with the LIVE/DEAD Fixable Green Dead Cell Stain Kit (Life Technologies). Gating was performed as described below ( t -SNE analysis of single-cell protein expression data).
To analyze the protein expression of the transcription factors PLZF and TCF-1, mononuclear tonsil cells were surface stained for 20 min at 22 °C in FC buffer with the same combination of antibodies listed above but with biotin-labeled antibodies targeting lineage markers as follows: anti-CD14 (HCD14), anti-CD19 (HIB19), anti-CD94 (DX22), anti-CD34 (581), anti-CD123 (6H6), anti-CD1a (HI149), anti-TCRαβ (IP26) and anti-TCRγδ (B1) (all from BioLegend); anti-FcɛRIα (AER-37 (CRA-1); Affymetrix) and anti-BDCA2 (AC144; Miltenyi Biotech). Thereafter, cells were incubated with Brilliant Violet 510–conjugated streptavidin (Biolegend) and a LIVE/DEAD Fixable Aqua Dead Cell Stain Kit (Life Technologies) for 20 min at 22 °C. Cells were then fixed with 2% formaldehyde (Polysciences) for 20 min at 22 °C, washed and permeabilized in 0.05% Triton X-100 (Sigma) for 10 min at 22 °C.
Intracellular staining was performed with Alexa Fluor 488–conjugated anti-PLZF (Mags.21F7; eBioscience), unconjugated rabbit anti-TCF-1 (C63D9; Cell Signaling Technology) and rabbit IgG control (ISO-1774; EPITOMICS) for 2 h in FC buffer supplemented with 2% BSA (Sigma). Thereafter, cells were incubated with an Alexa Fluor 647–conjugated F(ab′) 2 goat anti–rabbit IgG secondary antibody (A21246; Life Technologies) for 20 min at 22 °C, washed and immediately acquired on a LSR Fortessa flow cytometer (BD Biosciences).
For flow cytometry sorting for scRNA-seq, samples depleted of CD3 + CD14 + CD19 + cells were incubated with antibodies (listed below) for 30 min at 4 °C, washed in PBS and resuspended in Yssel's medium (in-house prepared) containing 1% NHS (NHS; Invitrogen). Surface staining was performed as described for flow cytometry analysis with the following exceptions: FITC-conjugated anti-CD94, Alexa Fluor 700–conjugated anti-CD45, PE–Texas Red–conjugated anti-CD62L, PE-conjugated anti-HLA-DR, Brilliant Violet 785–conjugated anti-CD3, APC-Cy7-conjugated anti-CD45RA were omitted; and Alexa Fluor 700–conjugated anti-CD16 (3G8; Biolegend), FITC-conjugated anti-CD3 (SK7; Biolegend), BD Horizon V500–conjugated anti-CD45 (HI30; BD Biosciences) and PE-conjugated anti-NKG2A (Z199; Beckman Coulter) were included.
Sorting of single cells was performed by gating mononuclear cells from tonsils as CD45 + lymphocytes lacking lineage markers for T cells (CD3, TCRαβ, TCRγδ), B cells (CD19), monocytes/macrophages (CD14), dendritic cells (BDCA2, CD123, CD1a), mast cells (FcɛRIα) and progenitors (CD34). Among those CD45 + Lin − cells, total ILCs were identified as CD127 + NKG2A − CD16 − cells. ILC1 cells were sorted as Lin − CD127 + NKG2A − CD16 − CD117 − CRTH2 − cells and ILC2 cells were sorted as Lin − CD127 + NKG2A − CD16 − CRTH2 + . As a reference cell population, we also sorted CD45 + Lin − CD127 − CD56 + NKG2A + NK cells, representing the major NK cell subset in the tonsil. Cells were sorted into 96-well Piko PCR plates (Finnzymes) containing 4.01 μl of lysis buffer per well. Lysis buffer (per well) consisted of 1 μl SMART dT 30 VN (10 μM; Biomers.net) 1 μl dNTP mix (10 mM; Invitrogen), 0.01 μl 'spike-ins' from the External RNA Controls Consortium (1:40 000 dilution; Ambion), 1.9 μl 0.4% Triton X-100 (Sigma), 0.1 μl RNase Inhibitor (10 U/μl; Applied Biosystems). Single cells were sorted on a FACSAria III with FACSDiva version 7, enabling indexed data analysis.
Sorting and in vitro stimulation of ILC3 subsets.
The ILC3 subpopulations were sort-purified on the basis of exclusive expression of NKp44, CD62L and HLA-DR. Preparation of the cells was done as described for single-cell sorting. For defining lineage marker–positive cells the following FITC-conjugated antibodies were used: anti-CD3 (SK7; BioLegend), anti-CD14 (TÜK4; Invitrogen), anti-CD19 (4G7; BD Biosciences), anti-FcɛRIα (AER-37 (CRA-1)), anti-CD34 (581), anti-CD123 (6H6), anti-CD1a (HI149), anti-CD94 (DX22), anti-TCRαβ (IP26) and anti-TCRγδ (B1) (all from BioLegend); anti-BDCA2 (AC144; Miltenyi Biotech). Additional surface staining was performed using the following antibodies: APC-Cy7–conjugated anti-CD62L (DREG56; BioLegend), BD Horizon V450–conjugated anti-CRTH2 (BM16; BD Biosciences), BD Horizon V500–conjugated anti-CD45 (HI30; BD Biosciences), Brilliant Violet 605–conjugated anti-CD161 (HP-3G10; BioLegend), Brilliant Violet 711–conjugated anti-CD56 (HCD56; BioLegend), PE-Cy5–conjugated anti-NKp44 (Z231; Beckman Coulter), PE–cyanine 5.5–conjugated anti-CD117 (104D2D1; Beckman Coulter), PE-Cy7–conjugated anti-CD127 (R34.34; Beckman Coulter) and PE- or eVolve 605–conjugated anti-HLA-DR (LN3; eBioscience). The use of PE or eVolve 605–labeled HLA-DR antibodies resulted in a comparable frequency of HLA-DR + ILC3 cells. Additionally, cells were stained with the LIVE/DEAD Fixable Green Dead Cell Stain Kit (Life Technologies).
All ILC3 populations were gated as Lin − CD45 + CD127 + CD161 + CD117 + CRTH2 − . NKp44 + ILC3 cells were sorted as NKp44 + CD62L − HLA-DR − ILC3 cells. CD62L + ILC3 cells were sorted as CD62L + NKp44 − HLA-DR − ILC3 cells. HLA-DR + ILC3 cells were sorted as HLA-DR + CD62L − NKp44 − ILC3 cells.
Sorted cells were seeded at densities of 2 × 10 3 to 10 × 10 3 cells in round-bottomed 96-well plate in Yssel's supplemented (in-house prepared) IMDM containing 1% normal human serum. Cells were incubated with IL-2 (10 U/ml) or IL-2, IL-23 plus IL-1β (50 ng/ml each) for 12 h followed by stimulation with PMA (20 ng/ml) plus ionomycin (0.5 μM) for 6 h with the last 5 h including Golgi Plug (1:10, BD Biosciences) and Golgi Stop (1:15, BD Biosciences). ILC3 subpopulations were analyzed for intracellular cytokines GM-CSF, IFN-γ, IL-2, IL-17F, IL-22 and TNF. To that end, cells were incubated with LIVE/DEAD Fixable Green Dead Cell marker followed by Cytofix/Cytoperm buffer (BD Biosciences) for 20 min. Fixed cells were then incubated with antibodies to cytokines (listed below) for 30 min. The following anti-cytokine antibodies were used: PE-cyanine–based fluorescent dye 594–conjugated anti-GM-CSF (BVD2-21C11; BD Biosciences), Alexa Fluor 700–conjugated anti-IFN-γ (B27; BD Biosciences), Brilliant Violet 421– or Brilliant Violet 711–conjugated anti-IL-2 (5344.111; BD Biosciences), Brilliant Violet 650–conjugated anti-IL-17F (O33-782; BD Biosciences), PE- or eFluor 450–conjugated anti-IL-22 (22URTI; eBioscience) and APC-conjugated anti-TNF (MAb11; eBioscience). Using Brilliant Violet 421– or Brilliant Violet 711–conjugated anti-IL-2 or PE- or eFluor 450–conjugated anti-IL-22 resulted in comparable signal intensities. Cells were immediately acquired on a LSR Fortessa flow cytometer (BD Biosciences). Data were analyzed by using FlowJo 9.7.6 software (Tree Star) and Prism 6.0 (GraphPad). Boolean gating of five parameters (GM-CSF, IL-2, IL-17F, IL-22 and TNF) was performed using FlowJo followed by further multiparametric analysis using SPICE 5.3 software 44 .
Preparation of cDNA libraries and sequencing.
Sorted cells were processed using the Smart-seq2 protocol 14 with minor changes. Pre-amplification was carried out adding 0.15 μl ISPCR primers (10 μM) and using 21 PCR cycles. Purification of the resulting cDNA was performed using Sera-Mag Magnetic SpeedBeads Carboxylate-Modified (GE Healthcare) prepared according a modified version of a published protocol 47 . The bead stock solution (50 mg/ml beads) were resuspended in buffer containing 19.5% PEG-8000 (Sigma-Aldrich), 1 M NaCl (Ambion), 10 mM Tris-HCl pH 8.0 (Ambion), 0.1% Igepal CA-630 (Sigma-Aldrich) and a 1:1 ratio of cDNA/bead buffer was used for cDNA precipitation. Purified cDNA was eluted in 15 μl of 1 mM Tris-HCl, pH 7.5 (Sigma-Aldrich), or nuclease-free water (Gibco). Given the large number of samples involved, we randomly checked only 5% of them on a High-Sensitivity DNA chip (Agilent Bioanalyzer). A successful library had an average size of 1.7–2.0 kb with a cDNA yield of about 2–5 ng after 21 pre-amplification cycles. However, a considerable amount of primer dimers with size <150 bp was sometimes observed. Such short fragments will also be 'tagmented' (fragmented and tagged for sequencing) 48 and thus decrease the number of usable reads. The amount of primer dimers was highly variable and apparently correlated with sample handling and/or processing.
Final libraries were prepared according to the low-input cDNA (<1 ng) protocol 48 . For the tagmentation reaction, 500 pg of pre-amplified cDNA and 10 cycles of enrichment PCR were used. Indexing of the samples was performed with the Nextera XT DNA Sample Preparation Index Kit (24 index primers, Illumina) after dilution of each adaptor 1:5 with water or 1 mM Tris-HCl, pH 8.0, and using 5 μl for the enrichment PCR. Purification was done using a 0.8:1 ratio of beads/DNA using a buffer containing 24% PEG-8000, 1 M NaCl, 10 mM Tris-HCl, pH 8.0, 0.1% Igepal CA-630. Samples were eluted in 20 μl of 1 mM Tris-HCl, pH 7.5. 5% of the samples were randomly checked on a High-Sensitivity DNA chip (Agilent Bioanalyzer) to assess whether the library preparation was successful. 96 samples (the entire plate, including negative controls) were pooled in a single 1.5-ml tube, the concentration of the pool was measured with the Qubit High-Sensitivity DNA kit (Invitrogen) and the average size was established using a High-Sensitivity DNA chip (Agilent Bioanalyzer). Each pool was then diluted to a final concentration of 2 nM, and 10 pmol were loaded on an Illumina HiSeq 2000 instrument for the final sequencing. Sequencing was done to the average depth of 2.3 × 10 6 reads per cell with 43 bp reads after 'demultiplexing'.
Read alignments and gene-expression estimation.
The reads were aligned to the human genome (hg19) merged with 'spike-in' sequences (from the External RNA Controls Consortium) using STAR v2.3.0 (ref. 49 ) with default settings and were filtered for uniquely mapping reads. Gene expression values were calculated as reads per kilobase gene model and million mappable reads (RPKMs) for each transcript in Ensembl release 69 using rpkmforgenes 50 .
Quality control.
To filter low quality sequences and possible empty wells, fraction exon mapping reads, gene coverage, mapping rate, mismatch/indel rate and total number of mRNA mapping reads were evaluated for each cell. Gene body coverage and read distribution was calculated using RSeQC-2.3.4 software 51 . Cutoffs were set at the tail of the distributions for each of these metrics ( Supplementary Fig. 1 ), and for number of mRNA mapping reads, we used a cutoff of 1 × 10 5 reads. In total, 142 cells of a total 796 did not pass these stringent filtering criteria and were excluded from further analysis. To minimize the risk of T cell contamination during flow cytometry sorting, clustering using TCR-encoding genes was performed and an additional 6 cells that grouped together with CD8 + T cells from peripheral blood (data not shown) were discarded. 648 cells were left for further analyses.
Data filtering and normalization.
Biologically variable genes were defined as those with higher variation than the spike-in RNAs 22 ( Supplementary Fig. 2a ). This gave 847 variable genes that were used for further clustering by PCA. In the initial PCA, there was a clear batch effect with cells from the same donor grouped together ( Supplementary Fig. 2e ). This could have reflected biological variation between the individuals as well as technical variations, since cell sorting and libraries were prepared at different occasions. SVA ComBat function 52 was used to remove this batch effect and after batch normalization, the cells from the same cell population grouped together better and no clear patient effect was seen ( Supplementary Fig. 2e ).
Cell population definition.
Dimensionality reduction was performed with t -stochastic neighbor embedding ( t -SNE) with 10 first principal components, a perplexity of 30 and theta = 0.001 using the R software package 23 . Due to the randomness in t -SNE output, 20 runs with Rtsne were used for hierarchical clustering and bootstrapping with the pvclust R package 53 (software package available at http://CRAN.R-project.org/package=pvclust ), which clearly separated out four groups with 100% bootstrap values. Separation of ILC3 subpopulations was defined based on clustering on t -SNE and using 1,958 genes expressed by ILC3 cells and annotated as 'immune genes'.
We used the SCDE software package ('single cell differential expression') 54 to define cluster-specific genes. Differentially expressed genes for each ILC population are in Supplementary Data Set 1 . For ILC3 subpopulations, very few differentially expressed genes were detected with SCDE due to low cell numbers and highly similar cells. Hence the genes' PCA contributions were used to define subpopulation signatures ( Fig. 8 and Supplementary Fig. 7 ).
Protein and RNA comparison.
To have comparable values for the fluorescence intensities of the different proteins, as measured by flow cytometry, the intensity values for each of the eight proteins were normalized to a scale from 0 to 1. Similarly, their log 2 RPKM values were normalized to the same scale. Subsampling of cells ( Fig. 3c ) was performed for 1,000 iterations with random selection of 'X' number of cells for each data point. Pearson and Spearman correlation analysis was performed for all comparisons.
t -SNE analysis of single-cell protein-expression data.
For the analysis shown in Figure 8g,h , t -SNE of flow cytometry data was performed. First, the raw flow cytometry files from the individual tonsil donors all acquired on different days, but using application settings, were imported into FlowJo (v9.8.5; TreeStar). Files from each day were compensated separately using standard automatic compensation algorithms and subsequently visually adjusted. Bi-exponential transformation was applied individually for each parameter and acquisition day. Lymphocytes were identified using forward- and side-scatter characteristics, and doublets were excluded using forward-scatter characteristics. Events negative for CD45 were excluded. After this, events positive for CD1a, CD3, CD14, CD19, CD34, CD94, BDCA2, CD123, TCRαβ, TCRγδ and FcɛR1α were excluded. This was followed by identification of events positive for CD127 and CD161 and, finally, CRTH2 − events were identified as ILC3 cells. In this population, NKp44 + events were identified. In the NKp44 − compartment, CD62L + events were identified. In the NKp44 − CD62L − compartment, HLA-DR + events were identified. From each donor, the fluorescence information for all events in these three populations, as well as that for the remaining HLA-DR − CD62L − NKp44 − events, was exported in a bi-exponentially transformed format ('channel numbers'). The total number of exported events per file were between 3,519 and 575. In the downstream analysis, files from adults and children were combined, as we found no clear age-related differences. The files were concatenated and preprocessed using R (version 3.2.0, 64 bit; R Foundation) and the package 'plyr' 55 .
After concatenation, the parameters CD45RA, CD62L, HLA-DR and NKp44 were selected and normalized using the formula 100 × ((x − (min col(x) )) / (max col(x) ) − (min col(x) )), where 'x' is any fluorescence value and 'max/min col(x) ' represents the maximal and the minimal values in the parameter where x is present. After that, t- SNE was performed using the R package Rtsne 23 . Before making graphs of individual parameter distributions, the 0.01% most positive and negative data for each parameter were reduced to their less extreme border, to facilitate color-coding of individual parameters over the t -SNE field. Plots show all events for the specified analysis and are based on the t -SNE field parameters V1 and V2. The data on distribution of the sub-clusters identified by manual gating and the distribution of single parameters was added as the third dimension using color.
Data analysis and code availability.
All statistical analysis and plotting of scRNA-seq and cell surface protein data was performed using R software. Graphics were made using the R core package and packages gplots, ggplot2, and RColorBrewer 56 , 57 , 58 . SPICE software 44 and Prism 6.0 software (GraphPad) were used for analysis of intracellular cytokine data. For all flow cytometry data, FlowJo 9.7.6 software (Tree Star) was used. SCDE package 54 was used to define differentially expressed genes. All custom scripts can be found online ( https://github.com/asabjorklund/ILC_scRNAseq ).
Accession codes.
GEO: sequence data, GSE70580 ; Sequence Read Archive: SRP060416 .
Accession codes
Primary accessions
Gene Expression Omnibus
GSE70580
Sequence Read Archive
SRP060416
Change history
17 March 2016
In the version of this article initially published, two labels along the horizontal axis of Figure 1c were switched, so the data for donor a were presented for donor c (and vice versa). The error has been corrected in the HTML and PDF versions of the article.
References
Eberl, G. et al. An essential function for the nuclear receptor RORγ(t) in the generation of fetal lymphoid tissue inducer cells. Nat. Immunol. 5 , 64–73 (2004).
CAS PubMed Google Scholar
Mebius, R.E., Rennert, P. & Weissman, I.L. Developing lymph nodes collect CD4 + CD3 − LTβ + cells that can differentiate to APC, NK cells, and follicular cells but not T or B cells. Immunity 7 , 493–504 (1997).
CAS PubMed Google Scholar
Cupedo, T. et al. Human fetal lymphoid tissue-inducer cells are interleukin 17-producing precursors to RORC + CD127 + natural killer-like cells. Nat. Immunol. 10 , 66–74 (2009).
CAS PubMed Google Scholar
Artis, D. & Spits, H. The biology of innate lymphoid cells. Nature 517 , 293–301 (2015).
CAS PubMed Google Scholar
Bernink, J.H. et al. Human type 1 innate lymphoid cells accumulate in inflamed mucosal tissues. Nat. Immunol. 14 , 221–229 (2013).
CAS PubMed Google Scholar
Crellin, N.K., Trifari, S., Kaplan, C.D., Cupedo, T. & Spits, H. Human NKp44 + IL-22 + cells and LTi-like cells constitute a stable RORC + lineage distinct from conventional natural killer cells. J. Exp. Med. 207 , 281–290 (2010).
CAS PubMed PubMed Central Google Scholar
Mjösberg, J.M. et al. Human IL-25- and IL-33-responsive type 2 innate lymphoid cells are defined by expression of CRTH2 and CD161. Nat. Immunol. 12 , 1055–1062 (2011).
PubMed Google Scholar
Spits, H. et al. Innate lymphoid cells–a proposal for uniform nomenclature. Nat. Rev. Immunol. 13 , 145–149 (2013).
CAS PubMed Google Scholar
Bernink, J.H. et al. Interleukin-12 and -23 control plasticity of cd127 + group 1 and group 3 innate lymphoid cells in the intestinal lamina propria. Immunity 43 , 146–160 (2015).
CAS PubMed Google Scholar
Klose, C.S. et al. Differentiation of type 1 ILCs from a common progenitor to all helper-like innate lymphoid cell lineages. Cell 157 , 340–356 (2014).
CAS PubMed Google Scholar
Constantinides, M.G., McDonald, B.D., Verhoef, P.A. & Bendelac, A. A committed precursor to innate lymphoid cells. Nature 508 , 397–401 (2014).
CAS PubMed PubMed Central Google Scholar
Glatzer, T. et al. RORγt + innate lymphoid cells acquire a proinflammatory program upon engagement of the activating receptor NKp44. Immunity 38 , 1223–1235 (2013).
CAS PubMed Google Scholar
Boyd, A., Ribeiro, J.M. & Nutman, T.B. Human CD117 (cKit) + innate lymphoid cells have a discrete transcriptional profile at homeostasis and are expanded during filarial infection. PLoS ONE 9 , e108649 (2014).
PubMed PubMed Central Google Scholar
Picelli, S. et al. Smart-seq2 for sensitive full-length transcriptome profiling in single cells. Nat. Methods 10 , 1096–1098 (2013).
CAS PubMed Google Scholar
Picelli, S. et al. Full-length RNA-seq from single cells using Smart-seq2. Nat. Protoc. 9 , 171–181 (2014).
CAS PubMed Google Scholar
Zeisel, A. et al. Brain structure. Cell types in the mouse cortex and hippocampus revealed by single-cell RNA-seq. Science 347 , 1138–1142 (2015).
CAS PubMed Google Scholar
Deng, Q., Ramskold, D., Reinius, B. & Sandberg, R. Single-cell RNA-seq reveals dynamic, random monoallelic gene expression in mammalian cells. Science 343 , 193–196 (2014).
CAS PubMed Google Scholar
Treutlein, B. et al. Reconstructing lineage hierarchies of the distal lung epithelium using single-cell RNA-seq. Nature 509 , 371–375 (2014).
Article CAS PubMed PubMed Central Google Scholar
Patel, A.P. et al. Single-cell RNA-seq highlights intratumoral heterogeneity in primary glioblastoma. Science 344 , 1396–1401 (2014).
CAS PubMed PubMed Central Google Scholar
Shalek, A.K. et al. Single-cell transcriptomics reveals bimodality in expression and splicing in immune cells. Nature 498 , 236–240 (2013).
CAS PubMed PubMed Central Google Scholar
Mahata, B. et al. Single-cell RNA sequencing reveals T helper cells synthesizing steroids de novo to contribute to immune homeostasis. Cell Rep. 7 , 1130–1142 (2014).
CAS PubMed PubMed Central Google Scholar
Brennecke, P. et al. Accounting for technical noise in single-cell RNA-seq experiments. Nat. Methods 10 , 1093–1095 (2013).
CAS PubMed Google Scholar
Krijthe, J. Rtsne: T-distributed stochastic neighbor embedding using Barnes-Hut implementation. R package version 0.9 ( http://CRAN.R-project.org/package=Rtsne ).
Taniguchi, Y. et al. Quantifying E. coli proteome and transcriptome with single-molecule sensitivity in single cells. Science 329 , 533–538 (2010).
CAS PubMed PubMed Central Google Scholar
Schwanhäusser, B. et al. Global quantification of mammalian gene expression control. Nature 473 , 337–342 (2011).
PubMed Google Scholar
Robinette, M.L. et al. Transcriptional programs define molecular characteristics of innate lymphoid cell classes and subsets. Nat. Immunol. 16 , 306–317 (2015).
CAS PubMed PubMed Central Google Scholar
van de Pavert, S.A. et al. Maternal retinoids control type 3 innate lymphoid cells and set the offspring immunity. Nature 508 , 123–127 (2014).
CAS PubMed PubMed Central Google Scholar
Bezman, N.A. et al. Molecular definition of the identity and activation of natural killer cells. Nat. Immunol. 13 , 1000–1009 (2012).
CAS PubMed PubMed Central Google Scholar
Wang, F., Tian, Z. & Wei, H. Genomic expression profiling of NK cells in health and disease. Eur. J. Immunol. 45 , 661–678 (2015).
CAS PubMed Google Scholar
Holmes, M.L. et al. Peripheral natural killer cell maturation depends on the transcription factor Aiolos. EMBO J. 33 , 2721–2734 (2014).
CAS PubMed PubMed Central Google Scholar
Barnig, C. et al. Lipoxin A4 regulates natural killer cell and type 2 innate lymphoid cell activation in asthma. Sci. Transl. Med. 5 , 174ra126 (2013).
Google Scholar
Xue, L. et al. Prostaglandin D2 activates group 2 innate lymphoid cells through chemoattractant receptor-homologous molecule expressed on TH2 cells. J. Allergy Clin. Immunol. 133 , 1184–1194 (2014).
CAS PubMed PubMed Central Google Scholar
Gentek, R. et al. Modulation of signal strength switches Notch from an inducer of T Cells to an inducer of ILC2. Front. Immunol. 4 , 334 (2013).
PubMed PubMed Central Google Scholar
Mielke, L.A. et al. TCF-1 controls ILC2 and NKp46 + RORγt + innate lymphocyte differentiation and protection in intestinal inflammation. J. Immunol. 191 , 4383–4391 (2013).
CAS PubMed Google Scholar
Yang, Q. et al. T cell factor 1 is required for group 2 innate lymphoid cell generation. Immunity 38 , 694–704 (2013).
CAS PubMed PubMed Central Google Scholar
Larabee, J.L., Shakir, S.M., Barua, S. & Ballard, J.D. Increased cAMP in monocytes augments Notch signaling mechanisms by elevating RBP-J and transducin-like enhancer of Split (TLE). J. Biol. Chem. 288 , 21526–21536 (2013).
CAS PubMed PubMed Central Google Scholar
Bandyopadhyay, S., Valdor, R. & Macian, F. Tle4 regulates epigenetic silencing of gamma interferon expression during effector T helper cell tolerance. Mol. Cell. Biol. 34 , 233–245 (2014).
PubMed PubMed Central Google Scholar
Fuchs, A. et al. Intraepithelial type 1 innate lymphoid cells are a unique subset of IL-12- and IL-15-responsive IFN-γ-producing cells. Immunity 38 , 769–781 (2013).
CAS PubMed PubMed Central Google Scholar
Possot, C. et al. Notch signaling is necessary for adult, but not fetal, development of RORγt + innate lymphoid cells. Nat. Immunol. 12 , 949–958 (2011).
CAS PubMed Google Scholar
Lee, J.S. et al. AHR drives the development of gut ILC22 cells and postnatal lymphoid tissues via pathways dependent on and independent of Notch. Nat. Immunol. 13 , 144–151 (2012).
CAS Google Scholar
Hoorweg, K. et al. Functional differences between human NKp44 − and NKp44 + RORC + innate lymphoid cells. Front. Immunol. 3 , 72 (2012).
PubMed PubMed Central Google Scholar
Hepworth, M.R. et al. Group 3 innate lymphoid cells mediate intestinal selection of commensal bacteria-specific CD4 + T cells. Science 348 , 1031–1035 (2015).
CAS PubMed PubMed Central Google Scholar
Hepworth, M.R. et al. Innate lymphoid cells regulate CD4 + T-cell responses to intestinal commensal bacteria. Nature 498 , 113–117 (2013).
CAS PubMed PubMed Central Google Scholar
Roederer, M., Nozzi, J.L. & Nason, M.C. SPICE: exploration and analysis of post-cytometric complex multivariate datasets. Cytometry 79 , 167–174 (2011).
PubMed PubMed Central Google Scholar
De Smedt, M. et al. Notch signaling induces cytoplasmic CD3ɛ expression in human differentiating NK cells. Blood 110 , 2696–2703 (2007).
CAS PubMed Google Scholar
Huang, Y. et al. IL-25-responsive, lineage-negative KLRG1 hi cells are multipotential 'inflammatory' type 2 innate lymphoid cells. Nat. Immunol. 16 , 161–169 (2015).
CAS PubMed Google Scholar
Rohland, N. & Reich, D. Cost-effective, high-throughput DNA sequencing libraries for multiplexed target capture. Genome Res. 22 , 939–946 (2012).
CAS PubMed PubMed Central Google Scholar
Picelli, S. et al. Tn5 transposase and tagmentation procedures for massively scaled sequencing projects. Genome Res. 24 , 2033–2040 (2014).
CAS PubMed PubMed Central Google Scholar
Dobin, A. et al. STAR: ultrafast universal RNA-seq aligner. Bioinformatics 29 , 15–21 (2013).
CAS PubMed Google Scholar
Ramsköld, D., Wang, E.T., Burge, C.B. & Sandberg, R. An abundance of ubiquitously expressed genes revealed by tissue transcriptome sequence data. PLoS Comput. Biol. 5 , e1000598 (2009).
PubMed PubMed Central Google Scholar
Wang, L., Wang, S. & Li, W. RSeQC: quality control of RNA-seq experiments. Bioinformatics 28 , 2184–2185 (2012).
CAS PubMed Google Scholar
Leek, J.T., Johnson, W.E., Parker, H.S., Jaffe, A.E. & Storey, J.D. The sva package for removing batch effects and other unwanted variation in high-throughput experiments. Bioinformatics 28 , 882–883 (2012).
CAS PubMed PubMed Central Google Scholar
Suzuki, R. & Shimodaira, H. Pvclust: an R package for assessing the uncertainty in hierarchical clustering. Bioinformatics 22 , 1540–1542 (2006).
CAS PubMed Google Scholar
Kharchenko, P.V., Silberstein, L. & Scadden, D.T. Bayesian approach to single-cell differential expression analysis. Nat. Methods 11 , 740–742 (2014).
CAS PubMed PubMed Central Google Scholar
Wickham, H. The split-apply-combine strategy for data analysis. J. Stat. Softw. 40 , 1–29 (2011).
Google Scholar
Wickham, H. Ggplot2: Elegant Graphics for Data Analysis (Springer New York, 2009).
Neuwirth, E. RColorBrewer: ColorBrewer palettes. R package version 1.0–5. http://CRAN.R-project.org/package=RColorBrewer (2011).
Warnes, G.R. et al. gplots: Various R programming tools for plotting data. R package version 2.14.2. http://CRAN.R-project.org/package=gplots (2014).
Download references
Acknowledgements
We thank I. Douagi and R. Månsson for support with FACSAria sorting; J. Michaelsson, M. Karlsson and Y. Bryceson for discussions and critical reading of the manuscript; and M. Holm (Uppsala University) for Python scripts and input on coding. Supported by the Karolinska Institutet (J.M., M.F. and J.T.), the Swedish Research Council (J.M., M.F. and R.S.), the Swedish Cancer Society (J.M. and M.F.), the Swedish Society for Medical Research (J.M. and M.F.), the Swedish Foundation for Strategic Research (J.M., M.F. and R.S.), Torsten Söderberg's Foundation (J.M. and M.F.), the Jonas Söderquist Foundation (J.M. and M.F.), the European Union's Horizon 2020 research and innovation program (Marie Sklodowska-Curie 655677 for V.K.) and the Stockholm County Government (J.T.).
Author information
Author notes
Åsa K Björklund and Marianne Forkel: These authors contributed equally to this work.
Authors and Affiliations
Ludwig Institute for Cancer Research, Stockholm, Sweden
Åsa K Björklund, Simone Picelli & Rickard Sandberg
Department of Cell and Molecular Biology, Karolinska Institutet, Stockholm, Sweden
Åsa K Björklund & Rickard Sandberg
Department of Cell and Molecular Biology, Science for Life Laboratory, Uppsala University, Uppsala, Sweden
Åsa K Björklund
Department of Medicine Huddinge, Center for Infectious Medicine, Karolinska Institutet, Sweden
Marianne Forkel, Viktoria Konya, Jakob Theorell & Jenny Mjösberg
Department of Oto-Rhino-Laryngology, Karolinska University Hospital and CLINTEC, Karolinska Institutet, Stockholm, Sweden
Danielle Friberg
Authors
Åsa K Björklund
View author publications
Search author on: PubMed Google Scholar
Marianne Forkel
View author publications
Search author on: PubMed Google Scholar
Simone Picelli
View author publications
Search author on: PubMed Google Scholar
Viktoria Konya
View author publications
Search author on: PubMed Google Scholar
Jakob Theorell
View author publications
Search author on: PubMed Google Scholar
Danielle Friberg
View author publications
Search author on: PubMed Google Scholar
Rickard Sandberg
View author publications
Search author on: PubMed Google Scholar
Jenny Mjösberg
View author publications
Search author on: PubMed Google Scholar
Contributions
Å.K.B. contributed to study design, performed the computational analyses of transcriptome data, analyzed and interpreted data and co-wrote the manuscript; M.F. designed the study, performed experiments, analyzed and interpreted data and co-wrote the manuscript; S.P. contributed to study design, generated all scRNA-seq libraries, interpreted data and contributed to manuscript writing; V.K. performed experiments, analyzed and interpreted data and contributed to manuscript writing; J.T. analyzed and interpreted data and contributed to manuscript writing; D.F. provided clinical samples, interpreted clinical data and contributed to manuscript writing; R.S. contributed to study design, supervised the computational analyses, interpreted data and co-wrote the manuscript; and J.M. designed the study, performed experiments, interpreted data and co-wrote the manuscript.
Corresponding authors
Correspondence to Rickard Sandberg or Jenny Mjösberg .
Ethics declarations
Competing interests
The authors declare no competing financial interests.
Integrated supplementary information
Supplementary Figure 1 Overview of quality control (QC) filtering.
Histograms showing number of reads (a), percent uniquely mapping reads (b), fraction mismatches (c), fraction exon mapping reads (d), fraction of reads mapping to a region at the 10% most 3prime end of each transcript (e) and number of mRNA reads (f). Blue bars represents empty well controls and red bars represent wells containing one cell. Black bold lines indicates filtering cutoffs where cells above/below the black line have been removed. Data were generated in three independent experiments with one tonsil donor each (n=798).
Supplementary Figure 2 Overview of scRNA-seq data filtering and normalization.
a) Detection of biologically variable transcripts over technical noise with ERCC spike-in RNAs highlighted in black, human transcripts in blue (variable) or red (non-variable). Violin plots showing distributions of: b) Forward scattering (FSC), c) ratio of cell RNA to ERCC spike-in RNA (ERCC-ratio) and d) number of detected transcripts. e) PCA based on 847 variable transcripts, before (upper panel) and after (lower panel) batch normalization, cells colored either by surface phenotype (left panel) or donor (left panel) origin. Data were generated in three independent experiments with one tonsil donor each (total number of cells per cell population: ILC1, n=112; ILC2, n=143; ILC3, n=320; NK cells, n=73).
Supplementary Figure 3 Pairwise comparisons of scRNA-seq profiles.
a) Pairwise comparison of the mean expression of the top 50 differentially expressed transcripts for the two cell populations in question. Cells are colored according to cluster definition described in main Fig. 2 . Cells where cluster definition and surface phenotype were in agreement are shown with a star (*). Cells that deviated in the clustering are either highlighted as cross (x) if they were defined as the other phenotype in the comparison, and as a circle (o) if the cell had another phenotype than the 2 cell populations in question. b) ERCC-ratio plots for each plot shown in a demonstrating the ratio of cellular RNA to ERCC spike-in RNA for each cell. Data were generated in three independent experiments with one tonsil donor each. Total number of cells per cell population: ILC1, n=112; ILC2, n=143; ILC3, n=320; NK cells, n=73.
Supplementary Figure 4 Comparison of protein expression versus RNA expression.
Each plot shows the surface protein expression intensity (y-axis) vs. log2(RPKM) RNA expression (x-axis) as measured by flow cytometry (indexed flow cytometric sorting data collection) and scRNA-seq, respectively. Both quantities were normalized on a scale from 0-1. Correlation values, both Spearman and Pearson are shown in the titles. Data were generated in three independent experiments with one tonsil donor each (n=648).
Supplementary Figure 5 Transcripts commonly expressed by CD127 + ILCs and NK cells.
Violin plots with expression distribution in each cell population on log2(rpkm) scale for ILC and NK specific transcripts. Coloring according to mean expression. a) Other transcripts commonly expressed by ILCs (according to SCDE; multiple-testing corrected p-value < 0.001). b) Transcription factors commonly expressed by ILCs (according to SCDE; multiple-testing corrected p-value < 0.05). c) Transcripts known to be expressed by NK cells d) Other transcripts expressed by NK cells (according to SCDE; multipletesting corrected p-value < 0.001 for both c and d). Data were generated in three independent experiments with one tonsil donor each (total number of cells per cell population: ILC1, n=112; ILC2, n=143; ILC3, n=320; NK cells, n=73).
Supplementary Figure 6 T cell–related transcripts and detection of differentially expressed genes.
a) Heatmap of T-cell related transcripts, expression in ILC1s (blue), ILC2s (cyan), NK cells (green) and ILC3s (red). Each vertical line in the heatmap represents the expression intensity in an individual cell. Color intensities according to log2(rpkm) values. b) Number of significantly differentially expressed genes (p-value < 0.001) in ILC1s (blue), ILC2s (cyan) and ILC3s (red) with random subsampling of 25,50,75 or 100 cells from each population. Error bars represents standard deviation from 10 iterations. Data were generated in three independent experiments with one tonsil donor each (total number of cells per cell population: ILC1, n=112; ILC2, n=143; ILC3, n=320; NK cells, n=73).
Supplementary Figure 7 Transcripts expressed in ILC3 subpopulations.
a) Top 20 transcript loadings for principal components 1 (PC1) and 2 (PC2) in PCA with ILC3s ( Fig. 8a ). b) t-SNE plots with the ILC3s colored according to expression intensity of some selected transcripts. Data were generated in three independent experiments with one tonsil donor each (n=320).
Supplementary Figure 8 Flow cytometry of ILC3 subpopulations.
a) t-SNE plots based on surface marker intensities for 5 adult donors and 7 pediatric donors (n=20543) with intensities of the 4 markers used for t-SNE (NKp44, HLA-DR, CD62L and CD45RA) followed by donor distribution (red to yellow shades for pediatric, blue to green shades for adults). b) Bar charts show percentage of IL-2+, IL-22+, IL-17F+ and TNF+ cells from the indicated ILC3 subpopulations after IL-23 plus IL-1β (50 ng/ml each, for 12+6 hours) and/or PMA plus ionomycin (20 ng/ml plus 0.5 μM, for the last 6 hours). Bars show mean and SEM from 4-6 donors. **** p<0.0001, *** p<0.005, ** p<0.01 and * p<0.05 as calculated using oneway ANOVA and Tukey’s multi-comparisons test. c) Representative dot plots show intracellular IL-2 and IL-22 production by the different ILC3 subpopulations after the indicated stimulations.
Supplementary information
Supplementary Text and Figures (download PDF )
Supplementary Figures 1–8 and Supplementary Table 1 (PDF 4224 kb)
Supplementary Data Set 1 (download XLSX )
Differentially regulated genes per ILC population (XLSX 10975 kb)
Supplementary Data Set 2 (download XLSX )
List of genes correlated to RORC and GATA3 (XLSX 53 kb)
Rights and permissions
Reprints and permissions
About this article
Cite this article
Björklund, Å., Forkel, M., Picelli, S. et al. The heterogeneity of human CD127 + innate lymphoid cells revealed by single-cell RNA sequencing. Nat Immunol 17 , 451–460 (2016). https://doi.org/10.1038/ni.3368
Download citation
Received : 04 June 2015
Accepted : 07 December 2015
Published : 15 February 2016
Issue date : April 2016
DOI : https://doi.org/10.1038/ni.3368
Share this article
Anyone you share the following link with will be able to read this content:
Get shareable link
Sorry, a shareable link is not currently available for this article.
Copy shareable link to clipboard
Provided by the Springer Nature SharedIt content-sharing initiative
You have full access to this article via California Institute of Technology .
Associated content
Transcriptionally defining ILC heterogeneity in humans
Gregory F Sonnenberg
Nature Immunology News & Views 22 Mar 2016
Advertisement
Explore content
Research articles
Reviews & Analysis
News & Comment
Videos
Current issue
Collections
Follow us on X
Sign up for alerts
RSS feed
About the journal
Aims & Scope
Journal Information
Journal Metrics
About the Editors
Research Cross-Journal Editorial Team
Reviews Cross-Journal Editorial Team
Our publishing models
Editorial Values Statement
Editorial Policies
Content Types
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
Nature Immunology ( Nat Immunol )
ISSN 1529-2916 (online)
ISSN 1529-2908 (print)
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
Sign up for the Nature Briefing newsletter — what matters in science, free to your inbox daily.
Email address
Sign up
I agree my information will be processed in accordance with the Nature and Springer Nature Limited Privacy Policy .
Close
Get the most important science stories of the day, free in your inbox. Sign up for Nature Briefing
