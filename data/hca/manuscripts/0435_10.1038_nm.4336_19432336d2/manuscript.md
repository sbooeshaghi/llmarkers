Single-cell transcriptomics uncovers distinct molecular signatures of stem cells in chronic myeloid leukemia | Nature Medicine
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
nature medicine
articles
Single-cell transcriptomics uncovers distinct molecular signatures of stem cells in chronic myeloid leukemia
Published: 15 May 2017
Single-cell transcriptomics uncovers distinct molecular signatures of stem cells in chronic myeloid leukemia
Alice Giustacchini ORCID: orcid.org/0000-0002-8733-8594 1 , 2 na1 ,
Supat Thongjuea 1 , 2 na1 ,
Nikolaos Barkas 1 , 2 ,
Petter S Woll 2 ,
Benjamin J Povinelli 1 , 2 ,
Christopher A G Booth 1 , 2 ,
Paul Sopp 1 ,
Ruggiero Norfo 1 , 2 ,
Alba Rodriguez-Meira 1 , 2 ,
Neil Ashley 1 , 2 ,
Lauren Jamieson 1 , 2 ,
Paresh Vyas ORCID: orcid.org/0000-0003-3931-0914 1 ,
Kristina Anderson 3 ,
Åsa Segerstolpe 4 , 5 ,
Hong Qian ORCID: orcid.org/0000-0002-2512-9199 6 ,
Ulla Olsson-Strömberg 7 ,
Satu Mustjoki 8 ,
Rickard Sandberg ORCID: orcid.org/0000-0001-6473-1740 4 , 9 ,
Sten Eirik W Jacobsen 1 , 2 , 4 , 6 , 10 na2 &
…
Adam J Mead ORCID: orcid.org/0000-0001-8522-1002 1 , 2 , 11 na2
Nature Medicine volume 23 , pages 692–702 ( 2017 ) Cite this article
35k Accesses
397 Citations
83 Altmetric
Subjects
Cancer stem cells
Chronic lymphocytic leukaemia
Transcriptomics
Abstract
Recent advances in single-cell transcriptomics are ideally placed to unravel intratumoral heterogeneity and selective resistance of cancer stem cell (SC) subpopulations to molecularly targeted cancer therapies. However, current single-cell RNA-sequencing approaches lack the sensitivity required to reliably detect somatic mutations. We developed a method that combines high-sensitivity mutation detection with whole-transcriptome analysis of the same single cell. We applied this technique to analyze more than 2,000 SCs from patients with chronic myeloid leukemia (CML) throughout the disease course, revealing heterogeneity of CML-SCs, including the identification of a subgroup of CML-SCs with a distinct molecular signature that selectively persisted during prolonged therapy. Analysis of nonleukemic SCs from patients with CML also provided new insights into cell-extrinsic disruption of hematopoiesis in CML associated with clinical outcome. Furthermore, we used this single-cell approach to identify a blast-crisis-specific SC population, which was also present in a subclone of CML-SCs during the chronic phase in a patient who subsequently developed blast crisis. This approach, which might be broadly applied to any malignancy, illustrates how single-cell analysis can identify subpopulations of therapy-resistant SCs that are not apparent through cell-population analysis.
You have full access to this article via California Institute of Technology .
Similar content being viewed by others
Potential value of high-throughput single-cell DNA sequencing of Juvenile myelomonocytic leukemia: report of two cases
Article Open access 09 September 2023
Management and outcome of patients with chronic myeloid leukemia in blast phase in the tyrosine kinase inhibitor era – analysis of the European LeukemiaNet Blast Phase Registry
Article Open access 28 March 2024
Single-cell multi-omics identifies chronic inflammation as a driver of TP53 -mutant leukemic evolution
Article Open access 04 September 2023
Main
Molecularly targeted therapies for cancer frequently induce impressive remissions; however, complete disease elimination remains rare, and patients remain at risk of disease relapse. At a cellular level, this is likely to reflect intratumoral heterogeneity, with differential response to treatment in distinct tumor subpopulations 1 . This phenomenon relates to the proposed hierarchical organization of some tumors, in which only rare cancer stem cells (CSCs) are capable of tumor propagation 2 , 3 , 4 . There is now ample evidence for the existence of such rare CSCs in some tumors, subsets of which are resistant to therapy and persist during remission 2 , 3 , 4 . However, studies characterizing CSCs during remission are lacking, which reflects in part the fact that these residual CSCs are typically rare and outnumbered by their normal tissue counterparts, from which they cannot easily be separated 5 , 6 .
Advances in single-cell gene-expression techniques offer great potential for studying the CSC heterogeneity that might underlie therapy resistance 1 , 7 , 8 , 9 . Thus far, however, the application of single-cell RNA sequencing in cancer has been relatively limited in patients who achieve remission after therapy 1 , 7 , 8 , 9 , 10 , 11 , 12 , partly because the detection of somatic mutations is grossly underappreciated using current techniques 11 . This primarily relates to poor coverage in the RNA-sequencing reads from single cells across the specific mutated region of a gene, owing to both technical dropouts and stochastic gene expression in individual cells 8 . Thus, it is difficult to simultaneously apply single-cell transcriptome analysis with highly sensitive detection of specific mutations; the latter is essential for reliably distinguishing normal cells from somatically mutated cells that form part of the malignant clone. This is of particular importance when analyzing CSC during remission, at which point malignant cells are rare and may largely share transcriptomic features with normal tissue counterparts.
CML is a paradigm for molecularly targeted therapy and an ideal disease in which to explore the cellular basis of selective resistance to targeted therapy 13 , 14 . CML is less genetically complex than most cancers and is defined by the presence of the BCR - ABL fusion gene, the product of which is the target of tyrosine kinase inhibitor (TKI) treatments, which have improved outcomes dramatically for this disease 15 . However, chronic-phase CML (CP-CML) is propagated by rare CML-SCs that are selectively resistant to TKI therapy and incompletely eradicated in most patients 16 , 17 , which leads to frequent relapse following treatment discontinuation 18 . CML-SCs reside in the same phenotypic compartment as their normal hematopoietic stem cell (HSC) counterparts, and both express a CD34 + CD38 – surface phenotype 5 , 6 . Techniques for selectively analyzing BCR-ABL + SCs throughout the disease course are not currently available. It therefore remains to be established whether therapy-resistant CML-SCs following TKI therapy represent the stochastic persistence of heterogeneous CML-SCs; a selective persistence of a pre-existing distinct, therapy-resistant CML-SC subset; or a resistant CML-SC with novel properties that evolved as a result of the therapeutic selection process.
In addition, there is ample evidence in hematological malignancies that dysregulated hematopoiesis occurs as much through extrinsic disruption of the normal-HSC compartment as through intrinsic expansion of the leukemic clones 19 , 20 , 21 . For example, recent evidence from mouse models supports the involvement of nonclonal BCR-ABL − SCs in the CML disease phenotype 22 , 23 . However, in the absence of single-cell analysis enabling the separation of BCR-ABL − and BCR-ABL + SCs within individual patients, it remains unclear to what degree the disruption of BCR-ABL − SCs occurs in patients with CML, and how disruption of the nonclonal SC compartment might correlate with response to treatment.
Herein, we developed a new protocol that integrates fluorescence-activated cell sorting (FACS), high-sensitivity single-cell mutation detection and single-cell RNA sequencing. We apply this method to characterize distinct molecular signatures of SC subpopulations in human CML samples from diagnosis through remission and disease progression.
Results
Combined single-cell mutation detection and transcriptomics
Presence of the BCR-ABL fusion gene remains the only unequivocal marker of CML-SCs, and we therefore first sought to determine the sensitivity of BCR-ABL detection using Smart-seq2, a commonly used single-cell RNA-sequencing approach 8 , 24 , 25 , by analyzing the BCR-ABL + K562 human erythroleukemic cell line derived from a patient in blast crisis of CML 26 . BCR-ABL transcripts were not detected in as many as 18 of 24 cells (75%; Fig. 1a ), despite the generation of satisfactory complementary DNA (cDNA) libraries, as determined through bioanalyser analysis of the size and concentration of amplified cDNA libraries ( Supplementary Fig. 1a ). We obtained a similar result using a commercial nanofluidic platform 27 ( Supplementary Fig. 1b ) and across a range of other myeloid leukemia mutation hot spots ( Supplementary Fig. 1c ), which enabled us to validate that current single-cell RNA-sequencing techniques do not enable sensitive mutation detection 10 .
Figure 1: High-sensitivity single-cell detection of BCR-ABL with parallel unbiased whole-transcriptome analysis.
The alternative text for this image may have been generated using AI.
Full size image
( a , b ) Detection of BCR-ABL and GAPDH by qPCR in libraries from single K562 cells processed by Smart-seq2 ( a ) or BCR-ABL tSS2 ( b ). Values shown are the gene expression levels relative to the limit of detection (LOD), as indicated by the dashed horizontal line. Box plot shows median and quartile values and whiskers show outlier values within 1.5 times the interquartile range of the quartiles. Numbers below each plot show the frequency of cells showing expression above the LOD. ( c ) Correlation of expression data for 14,240 RefSeq genes generated from K562 single cells using Smart-seq2 ( n = 38) or BCR-ABL tSS2 ( n = 38). ( d ) RNA-sequencing results from single K562 cells processed with Smart-seq2 (blue, n = 38) or by BCR-ABL tSS2 (red, n = 38) shown by tSNE using 3,368 highly variable genes (see Online Methods ). ( e ) Dot plot illustrating sufficient sensitivity to detect specific copy numbers of BCR-ABL spiked-in before BCR-ABL tSS2 amplification of single BM cells from a healthy donor. Y axis indicates the gene expression level of BCR-ABL relative to the LOD. X axis indicates the absolute number of copies of BCR-ABL expected to be present in each reaction, calculated using a commercial standard. Table at top shows the numbers of wells that would be expected to contain at least one copy of BCR-ABL by Poisson distribution and the actual frequency of amplification following BCR-ABL tSS2.
Source data
To improve the sensitivity of BCR-ABL detection, we developed a BCR-ABL-targeted Smart-seq2 protocol ( BCR-ABL tSS2). By multiplexing BCR-ABL -specific primers at the reverse transcription and amplification steps, BCR-ABL detection was improved to 100% of K562 cells in plate-based ( Fig. 1b ) or microfluidic-based platforms ( Supplementary Figs. 1d and 2a–d ). Importantly, there was no evidence of bias caused by BCR-ABL tSS2 in relation to library quality ( Supplementary Fig. 2d ), and good correlation existed between the level of expression of 14,240 RefSeq genes ( Fig. 1c ) generated by Smart-seq2 or BCR-ABL tSS2; these samples also did not show separate clustering ( Fig. 1d and Supplementary Fig. 3 ). BCR-ABL plasmid 'spike-in' experiments demonstrated detection sensitivity to single molecules of BCR-ABL , with expected Poisson distribution. Importantly, no BCR-ABL amplification was observed from any negative control cells in this case ( Fig. 1e ) or in any subsequent experiment ( n = 232 cells). This BCR-ABL tSS2 method therefore allows for highly specific, sensitive and quantitative BCR-ABL detection with parallel unbiased whole-transcriptome analysis from the same single cell.
Single-cell RNA sequencing and BCR-ABL detection in CML stem cells
Because human HSCs are small and highly quiescent as compared to K562 cells, we first analyzed 232 Lin – CD34 + CD38 – BM cells from five healthy human donors (normal HSCs) using BCR-ABL tSS2. Satisfactory cDNA libraries were generated ( Supplementary Fig. 4a ), with a plateau in the numbers of genes detected above 1 × 10 6 mapped reads/cell ( Fig. 2a ). With an average sequencing depth of 3.4 × 10 6 mapped reads, a mean of 3,445 genes was detected in each cell ( Supplementary Fig. 4b ). 12,018 genes were detected (RPKM ≥1) in single-cell ensembles (sequencing data from all 232 cells were pooled in silico ), which correlated well with cell-population data ( Supplementary Fig. 4c ) providing sufficient sensitivity to detect low-level expressed transcripts ( Supplementary Fig. 4d ), in line with previous reports 28 . Human HSCs clustered separately and were more heterogeneous than K562 cells ( Fig. 2b and Supplementary Fig. 4e ). Importantly, independently processed cells from five different donors clustered together, illustrating stability of the data across independent experiments ( Fig. 2b ).
Figure 2: Single-cell whole-transcriptome analysis and BCR-ABL detection in single CML stem cells.
The alternative text for this image may have been generated using AI.
Full size image
( a ) Box plot illustrating the number of genes detected (RPKM ≥1) in relation to depth of sequencing in normal-HSC samples (shown as million reads/cell). ( b ) RNA-sequencing results from single K562 cells processed by BCR-ABL tSS2 (purple, n = 38) and normal HSCs ( n = 232), as shown by tSNE using 7,428 highly variable genes. ( c ) Correlation between merged data from 40 single cells from patient OX1407 with CML ('ensemble') and the bulk (100 cells sorted together) RNA-sequencing measurement of gene expression from the same patient. The ensemble was created by computationally pooling all reads obtained from the 40 single Lin – CD34 + CD38 − cells from patient OX1407. Some of the genes in f are highlighted to indicate selected differentially expressed genes. ( d ) Correlation between the levels of gene expression of BCR-ABL + ensemble and BCR-ABL − ensemble data. Some of the genes in f are highlighted. ( e ) Heat map illustrating the hierarchical clustering of BCR-ABL + SCs (red, n = 17) or BCR-ABL − SCs (blue, n = 23) showing the top 75 differentially expressed genes. ( f ) Correlation of log 2 (FC) by RNA sequencing ( y axis) and by qPCR ( x axis) between BCR-ABL + and BCR-ABL − SCs for selected genes. Differentially expressed genes (red dots) were selected by setting a fold change cutoff of >8 and choosing 12 genes of potential biologic interest. Nondifferentially expressed genes (gray dots, n = 12) were selected as housekeeping genes or relevant genes for the cell type analyzed. ( g , h ) Beeswarm plots for 6/12 selected differentially expressed genes between BCR-ABL + and BCR-ABL − SCs showing RNA sequencing ( g ) and qPCR ( h ) data. Numbers of cells analyzed and numbers showing amplification for the selected gene are shown below the plot. Nonparametric Wilcoxon test P values are shown on top of each bar graph. Fisher's exact test P values are shown below the graph. Average gene expression levels are indicated by red squares, and the median and quartiles of gene expression levels are represented by the boxes. Dashed lines represent the LOD.
Source data
We next analyzed 40 Lin – CD34 + CD38 – SCs from a patient with CML who was in hematologic remission following 3 months of TKI therapy (OX1407; Supplementary Table 1 ). BCR-ABL was detected in 17/40 cells (43%) by BCR-ABL tSS2 and in 7/20 cells (35%; P = 0.8) by single-cell fluorescence in situ hybridization. We detected 12,499 genes in data ensembles, which correlated well with bulk-analysis data ( Fig. 2c ). Comparison of BCR-ABL + and BCR-ABL − SCs identified genes showing differential expression ( Fig. 2d,e ). The level of expression correlated well between single-cell RNA sequencing and qPCR data ( Fig. 2f–h ; Supplementary Fig. 5a–c ). Taken together, these data provide proof of principle that BCR-ABL tSS2 can be applied to detect distinct gene expression in BCR-ABL + as compared to BCR-ABL − SCs from the same patient during TKI treatment.
Single-cell RNA sequencing of CML-SCs at diagnosis
We next used BCR-ABL tSS2 to process 2,070 Lin – CD34 + CD38 – BM SCs from diagnosis samples from 20 patients with CP-CML ( Supplementary Table 1 ). Two patients with CP-CML developed early progression to blast crisis (BC), and these cells were removed from the current analysis and analyzed in later experiments. As previously reported 29 , although the progenitor compartment was disrupted in patients with CML, the HSC-containing Lin – CD34 + CD38 – compartment was relatively intact phenotypically ( Supplementary Fig. 6 ). As expected 5 , 6 , 30 , the frequency of BCR-ABL + SCs was variable (median: 69%, 9–94%; Supplementary Table 1 ).
We selected 854 CP-CML-SCs (477 BCR-ABL + and 377 BCR-ABL − ) for sequencing and detected a mean of 3,591 genes/cell ( Supplementary Fig. 7a ). Read depth and mapped reads/cell were not different between normal HSCs ( n = 232), BCR-ABL − SCs and BCR-ABL + SCs ( Supplementary Fig. 7b,c ). The expression of housekeeping genes, for example, B2M , was also comparable in the three groups ( Supplementary Fig. 7d ). By contrast, whereas the mean number of genes detected was comparable between normal HSCs ( n = 3,445) and BCR-ABL − SCs ( n = 3,409), a significantly higher number of genes was detected in BCR-ABL + SCs ( n = 3,735, P = 1.67 × 10 −6 , Supplementary Fig. 7e ). This correlated with BCR-ABL-driven proliferation; markedly increased proliferation gene expression ( Fig. 3a ) and reduced quiescence-associated gene expression ( Fig. 3b ) were observed in BCR-ABL + SCs in comparison with normal HSCs. By contrast, BCR-ABL − SCs showed similar proliferation ( Supplementary Fig. 7f ) and quiescence-associated gene expression ( Supplementary Fig. 7g ) as normal HSCs. Consequently, coexpression of G2M-associated genes was selectively increased in BCR-ABL + SCs ( Supplementary Fig. 7h ).
Figure 3: Single-cell RNA-sequencing reveals distinct molecular signatures of BCR-ABL + CML-SCs at diagnosis.
The alternative text for this image may have been generated using AI.
Full size image
( a , b ) GSEA on 477 BCR-ABL + single-cells from 18 patients with chronic-phase CML at diagnosis, as compared to 232 normal HSCs from five normal donors. Gene sets shown are cell proliferation ( a ) and quiescence-associated genes ( b ). ( c ) tSNE visualization of single normal HSCs (gray circles; n = 232), BCR-ABL − SCs (blue diamonds; n = 377) and BCR-ABL + SCs (red triangles; n = 477) using 8,589 highly variable genes. ( d ) Hierarchical clustering analysis of the same 1,086 cells. The heat map is built using Pearson correlation generated using the top 245 differentially expressed genes. The horizontal color bar on top of the heat map indicates the sample from which each single SC was purified (upper bar, individual color for each patient) and the cell ID (lower bar): normal HSCs (black), BCR-ABL − SCs (blue) and BCR-ABL + SCs (red). ( e ) GSEA of unbiased HALLMARK gene sets for (i) normal HSCs ( n = 6) versus BCR-ABL + SCs ( n = 18) as an in silico bulk analysis; (ii) single-cell analysis of normal HSCs ( n = 232) versus BCR-ABL − SCs ( n = 377); (iii) single-cell analysis of normal HSCs ( n = 232) versus BCR-ABL + SCs ( n = 477); (iv) single-cell analysis of BCR-ABL − SCs ( n = 377) versus BCR-ABL + SCs ( n = 477). A false-discovery rate (FDR) cutoff of >0.25 was used.
Source data
t-distributed stochastic neighbor embedding (tSNE) analysis using 8,589 highly variable genes revealed distinct clustering of normal HSCs, BCR-ABL + and BCR-ABL − SCs ( Fig. 3c ). Differentially expressed genes between normal HSCs and BCR-ABL + and BCR-ABL − SCs included many that had previously been implicated in CML pathogenesis ( Supplementary Fig. 8a and Supplementary Table 2 ), but also a number of novel candidate genes of interest, such as RXFP1 , receptor for the hormone relaxin; the small GTPase RAB31 ; the spliceosome gene SRSF2 ; and the beta-galactoside-binding protein LGALS1 ( Supplementary Fig. 8b and Supplementary Table 2 ). In silico generation of cell-ensemble data demonstrated that few of these differentially expressed genes would have been revealed without single-cell analysis ( Supplementary Fig. 8c ). Using the top 245 differentially expressed genes, BCR-ABL + cells clustered separately from BCR-ABL − SCs, importantly, without evidence of major patient-specific clustering ( Fig. 3d ), which shows consistency of aberrant gene expression in BCR-ABL + SCs across different patients ( Supplementary Fig. 9a,b ).
Our comparison of BCR-ABL + SCs with normal HSCs and/or BCR-ABL − SCs showed expected enrichment in BCR-ABL + SCs for the large majority of established CML stem and progenitor gene sets ( Supplementary Tables 3 and 4 and Supplementary Fig. 10 ). Analysis using unbiased gene sets ( Supplementary Table 5 and Fig. 3e ) uncovered multiple gene sets selectively enriched in BCR-ABL + SCs (for example, overexpression of MTOR , E2F targets, G2M checkpoint, oxidative phosphorylation and glycolysis-associated gene expression; Supplementary Table 5 and Fig. 3e ), none of which showed enrichment through in silico bulk analysis of the same data set.
Importantly, our single-cell approach also uniquely allowed for analysis of BCR-ABL − SCs within the same patients—of relevance for recent evidence suggesting that the microenvironment is disrupted in mouse models of CML 22 , 23 . Interleukin (IL)-6-associated gene expression and downstream mediators such as STAT5 were indeed significantly enriched in BCR-ABL − SCs in comparison with normal HSCs ( Fig. 3e , Supplementary Fig. 10 and Supplementary Tables 4 and 5 ). Furthermore, other inflammation-associated gene expression, including those involved in the transforming growth factor (TGF)-β and tumor-necrosis factor (TNF)-α pathways, were also markedly enriched in BCR-ABL − SCs in comparison with normal HSCs ( Fig. 3e ). Inflammation is an important suppressor of HSC function 31 , 32 , including TGF-β and TNF-α, both of which are notably cell-extrinsic suppressors of HSCs 33 , 34 .
Single-cell RNA sequencing of CML-SCs predicts TKI response
Next, to establish the potential clinical utility of CML-SC single-cell gene expression signatures, in line with current guidelines 35 , we stratified patients with sufficient response data available as good ( n = 11) or poor ( n = 5) responders on the basis of subsequent achievement of a major molecular response (MMR) to TKI, defined as a BCR-ABL transcript level of <0.1% ( Supplementary Table 1 ). There was no significant difference in the frequency of BCR-ABL + SCs between good (61%) and poor (58%) responders ( P = 0.7). Although BCR-ABL + SCs at diagnosis did not clearly cluster according to response category ( Fig. 4a ), BCR-ABL − SCs from poor-responder patients showed highly distinct clustering according to analysis of 5,611 highly variable genes ( Fig. 4b ). Notably, in all five patients with CML who failed to achieve MMR, the frequency of BCR-ABL − SCs contained within the poor-responder cluster was higher than for all 11 patients who achieved MMR, in four cases with virtually all BCR-ABL − SCs falling within the poor-responder cluster ( Fig. 4c ). The five patients with >10% of BCR-ABL − SCs falling within the poor-responder cluster had a markedly inferior likelihood of achieving MMR ( Fig. 4d ; P < 0.01).
Figure 4: Single-cell RNA sequencing of SCs at diagnosis of patients with CML predicts molecular response to TKI.
The alternative text for this image may have been generated using AI.
Full size image
( a ) tSNE visualization of single BCR-ABL + SCs (from 16 patients with CP-CML with molecular follow-up data available; n = 436) using 5,011 highly variable genes. Color indicates whether cells were isolated from good responders ( n = 11 patients achieving MMR, blue) or poor responders ( n = 5 patients not achieving MMR, red). ( b ) tSNE visualization of single BCR-ABL − SCs from 16 patients with molecular follow-up data available ( n = 356) using 5,611 highly variable genes. Color indicates whether cells were isolated from good responders (11 patients achieving MMR, blue) or poor responders (five patients not achieving MMR, red). ( c ) The dot plot shows the proportion (%) of BCR-ABL − SCs falling in the poor-responders cluster for individual patients ( n = 16; red, patients with >10% of cells in poor-responder cluster; blue, patients with <10% of cells in poor responder cluster; squares represent patients failing to achieve MMR, and circles, patients who achieved MMR). ( d ) Kaplan–Meier curves showing time for MMR achievement for patients with >10% (red, n = 5) or <10% (blue, n = 11;) of BCR-ABL − SCs falling in the poor-responder cluster. P value represents the log–rank test. ( e ) GSEA of unbiased HALLMARK gene sets comparing BCR-ABL − SCs ( n = 356) and BCR-ABL + SCs ( n = 436) from good ( n = 11) and poor ( n = 5) TKI responders.
Source data
Gene-set enrichment analysis (GSEA) also showed enrichment at diagnosis of gene expression associated with signaling pathways, inflammation, TGF-β and TNF-α in BCR-ABL − SCs from poor as compared to good responders ( Fig. 4e and Supplementary Table 6 ). By contrast, both BCR-ABL − and BCR-ABL + SCs from good responders showed enrichment of MYC, E2F and G2M-checkpoint gene expression, all of which are associated with increased proliferation ( Fig. 4e and Supplementary Table 6 ). These data demonstrate that BCR-ABL + , as well as BCR-ABL − SCs, in poor-responding patients are already at diagnosis expressing more quiescence-associated genes than in patients who will later achieve MMR; given that this was observed for both BCR-ABL + and BCR-ABL − SCs, this may reflect differences in cell-extrinsic, microenvironmental factors in good as compared to poor responders.
Given that poor responders showed upregulation of TGF-β- and TNF-α-pathway-associated gene expression, combined with a highly quiescent CML-SC signature, we reasoned that TGF-β and TNF-α might promote quiescence in the CML-SC compartment and thereby confer TKI resistance. We therefore cultured single normal HSCs and CML-SCs in vitro , with or without TGF-β or TNF-α, and tracked the time it took for the SCs to divide. TNF-α promoted quiescence of both CML-SCs and normal HSCs ( Supplementary Fig. 11 ). Notably, TGF-β more strongly influenced the rate of cell division of CML-SCs than that of normal HSCs ( Supplementary Fig. 11 ). Taken together, these data highlight the power of single-cell (unlike bulk) RNA sequencing of CML-SCs at diagnosis to reveal gene-expression patterns in leukemic as well as nonleukemic SCs within the same patient.
Characterization of quiescent CML-SCs persisting during TKI therapy
We next analyzed 19 patients who had already commenced TKI therapy and had achieved at least hematological remission (normalization of blood counts), and most of whom showed additional cytogenetic response ( Supplementary Table 1 ). In 11 of these patients, paired diagnosis and follow-up BM samples were available following either 3 or 6 months of TKI ( Supplementary Table 1 ). In follow-up samples, the percentage of BCR-ABL + SCs (median: 9%, 0–82%) was lower than in diagnosis samples from the same patient ( P = 0.0001; Supplementary Table 1 ). From a total of 3,306 cells processed, we selected 245 BCR-ABL + SCs and 420 BCR-ABL − SCs for single-cell sequencing. Notably, unlike in diagnosis samples, the average number of genes detected in each cell was similar between BCR-ABL + ( n = 3,284) and BCR-ABL − SCs ( n = 3,196) in follow-up samples.
Using the top 500 genes (as indicated by random forests analysis) informative for distinguishing normal HSCs from BCR-ABL + SCs at diagnosis and during remission ( Supplementary Table 7 ), tSNE analysis revealed two distinct clusters of remission BCR-ABL + SCs (group A and group B; Fig. 5a ). Group-A remission BCR-ABL + SCs were enriched for quiescence and HSC-associated gene expression, whereas group B showed enrichment of MYC, E2F and proliferation-associated gene sets ( Fig. 5b and Supplementary Table 8 ). Group-A cells were progressively enriched with more prolonged TKI treatment, accounting for 43% of BCR-ABL + SCs at 3 months and 84% at ≥1 year ( P < 0.01; Fig. 5c ). This enrichment for group-A cells was even more striking when we included only patients who subsequently achieved MMR, with 65% and 91% of BCR-ABL + SCs falling in group A at 3 months and 1 year following the initiation of TKI treatment, respectively ( P < 0.01; Fig. 5d ; Supplementary Fig. 12a ). The only exceptions were one patient who temporarily interrupted TKI therapy and one patient who failed to achieve therapeutic imatinib levels, both of whom showed predominantly group-B SCs at 3 months ( Supplementary Fig. 12b ). This supports the concept that an excess of group-B cells during TKI therapy identifies patients with inadequate BCR-ABL inhibition. We also noted that in 15 of 18 (83%) diagnosis samples, a minority of BCR-ABL + SCs clustered in group A (26% of all diagnosis BCR-ABL + SCs; Fig. 5a,c,d and Supplementary Fig. 12 ), although the frequency of group-A cells at diagnosis did not correlate with response to TKI in this small cohort of patients. Taken together, these data suggest that prolonged TKI treatment results in the selective persistence of a distinct and highly quiescent BCR-ABL + CML-SC subset (group A) already present at diagnosis, rather than a stochastic persistence of heterogeneous CML-SCs or a resistant CML-SC with novel properties. To better understand the selective persistence of quiescent CML-SCs during long-term TKI treatment, we therefore focused subsequent analysis on remission group-A cells.
Figure 5: Single-cell analysis reveals distinct molecular signatures of quiescent CML-SCs persisting during TKI therapy.
The alternative text for this image may have been generated using AI.
Full size image
( a ) tSNE visualization of single normal HSCs (black circles; n = 232; five donors), BCR-ABL + SCs from patients at diagnosis (gray circles; n = 477; 18 donors) and BCR-ABL + SCs from patients at remission (light-blue diamonds and dark-blue triangles; n = 245; 16 donors). Remission BCR-ABL + SCs clustering closer to normal HSCs (light-blue diamonds; n = 122) are defined as group-A BCR-ABL + SCs, whereas those cells clustering with most diagnostic BCR-ABL + SCs are defined as group B (dark-blue triangles; n = 123). ( b ) GSEA of group-A versus group-B BCR-ABL + SCs at remission ( n = 122 and n = 123, respectively). Gene sets shown are cell proliferation, quiescence and HSC-associated genes. ( c ) Bar graph showing the proportion (%) of group-A BCR-ABL + SCs and group-B BCR-ABL + SCs for all patients analyzed at diagnosis ( n = 18), at 3 months ( n = 11) and more than 1 year ( n = 4) after TKI initiation. χ-squared and Fisher's exact test P < 0.01 for comparison of diagnosis versus 1-year samples. ( d ) The bar graph shows same results as in c , but only for patients eventually achieving MMR, samples taken at diagnosis ( n = 11), at 3 months ( n = 6) and more than 1 year ( n = 2) after TKI initiation. χ-squared and Fisher's exact test P < 0.01 for comparison of diagnosis versus 1-year samples. ( e ) GSEA of TNF-α, TGF-β and IL-6–JAK–STAT pathways comparing group-A BCR-ABL + SCs at remission ( n = 122) versus normal HSCs ( n = 232). ( f ) GSEA of TNF-α and TGF-β pathways performed on normal HSCs ( n = 232) versus group-A BCR-ABL + SCs at 3 months ( n = 72), 6 months ( n = 24) and more than 1 year after TKI initiation ( n = 27). ( g ) Beeswarm plots for ten selected differentially expressed genes between normal HSCs (black; n = 232; five donors), BCR-ABL + SCs from patients at diagnosis (red; n = 477; 18 donors) and group-A BCR-ABL + SCs from patients at remission (light blue; n = 122; 16 donors). Numbers of cells analyzed and numbers showing amplification for the selected genes are shown below the plot. The average gene expression levels are indicated by red squares, and the boxes represent the median and quartiles of gene expression levels. Nonparametric Wilcoxon test P values are shown on top of each bar graph. Fisher's exact test P values are shown below the graph.
Source data
Most group-A BCR-ABL + SCs clustered separately from normal HSCs ( Fig. 5a ); we detected 1,086 differentially expressed genes in group-A remission BCR-ABL + SCs in comparison with normal HSCs ( Supplementary Table 9 ). We also detected 1,681 and 1,348 differentially expressed genes in group-A remission BCR-ABL + SCs in comparison with group-B remission BCR-ABL + SCs and BCR-ABL + SCs at diagnosis, respectively ( Supplementary Table 9 ). In comparison with normal HSCs, group-A BCR-ABL + SCs showed enrichment of TGF-β-, TNF-α- (via nuclear factor (NF)-κB) and IL-6–JAK–STAT-associated gene expression, whereas E2F-, G2M-checkpoint- and MYC-associated gene expression were enriched in normal HSCs ( Fig. 5e , Supplementary Fig. 13 and Supplementary Table 10 ). Similar findings were obtained by comparing group-A remission cells with BCR-ABL − SCs during TKI treatment ( Supplementary Fig. 13 ). These findings support the concept that group-A remission CML-SCs, characterized by marked quiescence-associated gene expression, selectively evade eradication by TKI. These cells show more quiescence-associated gene expression than normal HSCs or BCR-ABL − SCs during remission, likely because the latter are intrinsically much less sensitive to TKIs owing to an absence of BCR-ABL expression. TGF-β- and TNF-α (via NF-κB)-associated gene expression was progressively more enriched within remission group-A BCR-ABL + SCs during the course of TKI treatment ( Fig. 5f ), which supports that these pathways may be important to sustain of this resistant and quiescent CML-SC population during TKI treatment. Remission group-A BCR-ABL + SCs, also showed overexpression of Wnt/β-catenin-pathway-associated genes ( GAS2 and CTNNB1 ), the TGF-β-pathway gene SKIL , regulators of NF-κB ( NFKB1A and SQSTM (also known as p62 )), the hypoxia factors HIF1A and the Wilms tumor protein (WT1) partner WTAP , as well as downregulation of the chemokine receptor CXCR4 and the transcription factor FOS , in comparison with normal HSCs ( Fig. 5g and Supplementary Table 9 ). This single-cell analysis provides insight into pathways that may be involved in promoting the selective persistence of distinct BCR-ABL + SCs following TKI treatment.
Analysis of CML-SC heterogeneity during blast crisis
We next analyzed three patients with lymphoid ( n = 2) or myeloid ( n = 1) BC transformation of CML ( Supplementary Table 1 ), to explore the possibility that single-cell sequencing of BCR-ABL + CML – SCs could already in CP predict a subsequent BC transformation. At the time of BC, tSNE analysis of CML-SCs revealed a separate cluster of BCR-ABL + SCs, clearly distinct from both normal HSCs, BCR-ABL + SCs from 18 patients with CP-CML at diagnosis and K562 cells ( Fig. 6a ). Notably, myeloid and lymphoid BC BCR-ABL + SCs clustered together. Comparison of gene expression of the BC and CP BCR-ABL + SC clusters revealed 1,166 differentially expressed genes ( Fig. 6b and Supplementary Table 11 ), including overexpression of HGF 36 and reduced expression of the Wnt pathway negative-regulator EAF2 (ref. 37 ).
Figure 6: Single-cell RNA sequencing reveals heterogeneity of CML stem cells associated with disease progression in CML.
The alternative text for this image may have been generated using AI.
Full size image
( a ) tSNE visualization of single normal HSCs from five donors (gray circles; n = 232), BCR-ABL + SCs from 18 patients with CP-CML (red triangles; n = 477) BCR-ABL + SCs from three patients at the time of BC (CML1931, light blue squares, n = 85; CML1266, purple squares, n = 63; CML1203, pink squares, n = 7 and K562 cells (brown circles, n = 53). The tSNE has been generated using 207 differentially expressed genes, as described in Online Methods. ( b ) Heat map shows the top 40 genes differentially expressed between BCR-ABL + SCs falling in the CP-CML cluster ( n = 477) and BCR-ABL + SCs falling in the BC cluster ( n = 155). Bar above the heat map indicates CP-CML cluster in red, BC-CML cluster in purple. ( c ) tSNE visualization as shown in a , but with BC (light-blue squares, n = 85) and pre-BC (orange diamonds, n = 132) cells from patient 1931 highlighted. Arrow indicates eight pre-BC cells clustering separately from remaining pre-BC cells and together with BCR-ABL + CP-SCs. ( d ) Heat map of log 2 (RPKM) of selected lymphoid- and myeloid-associated genes in BCR-ABL + CML-SCs at BC ( n = 155; three donors), pre-BC ( n = 185; two donors with SCs from patient OX1931 annotated according to those falling within the CP-CML cluster in yellow or BC-CML cluster in orange) and CP-CML SCs at diagnosis ( n = 477; 18 donors) and normal-HSCs ( n = 232; five donors), showing aberrant coexpression of lymphoid and myeloid genes in SCs falling within the BC cluster. ( e ) Dot plot showing index sort results corresponding to individual BCR-ABL + SCs from pre-BCs OX1931. The color and shape of the dots indicate whether the SC clustered with CP-CML BCR-ABL + SCs (blue triangles) or with BC-CML BCR-ABL + SCs (red circles) according to the RNA-seq results presented in the tSNE analysis in a . The value is expressed as fluorescence intensity for CD90 and CD45Ra antigens ( y and x axis, respectively). ( f ) Histogram (left) shows the frequency of differentially expressed genes between pre-BC OX1931 BCR-ABL + SCs clustering with CP-CML or BC-CML BCR-ABL + SCs ( y axis) with respect to the distance (Kb) of RUNX1 binding sites from the respective transcription start site (TSS; x axis). The box plot (right) shows the fraction of RUNX1 binding sites/window found in the genes that are differentially expressed between the CP-CML and the BC-CML SC clusters (red box) versus those found in background genes (gray box). P = 0.0018 by Wilcoxon test.
Source data
Two of the patients who developed BC following TKI initiation also had samples available from diagnosis, when the patients presented in CP (pre-BC) 12 months and 3 months before transformation to myeloid and lymphoid BC, respectively ( Supplementary Table 1 ). All pre-BC cells from the patient transforming to myeloid BC 12 months later clustered with other CP-CML SCs (CP-CML cluster, Supplementary Fig. 14a ). However, the pre-BC SCs from the patient who, 3 months later, developed lymphoid BC fell into two distinct groups, one clustering close to the BC-SCs (BC cluster, n = 124), but notably with a minority ( n = 8) clustering separately from the BC cluster within the CP-CML cluster ( Fig. 6c ). This provides direct evidence of evolution from CP to BC within the SC compartment of this patient, before any clinical or morphological evidence of development of BC. In further support of this, the pre-BC single BCR-ABL + SCs cells falling within the BC cluster showed aberrant coexpression of myeloid and lymphoid genes in comparison with normal HSCs or CP-CML – SCs, as did cells within the BC cluster from all three of the investigated BC patients, whereas none of the pre-BC BCR-ABL + SCs cells clustering with the CP CML – SCs showed this aberrant coexpression pattern ( Fig. 6d ), with validation of a number of aberrantly expressed genes by single-cell qPCR ( Supplementary Fig. 14b ). Moreover, index-sorting analysis (allowing specific FACS data of individual cells to be linked with gene expression data from the same cell) of the rare pre-BC cells in the CP-SC cluster showed that they all resided within the normal Lin – CD34 + CD38 – CD90 + CD45RA – HSC compartment, whereas 62 of 68 of the pre-BC SCs falling in the BC-SC cluster had a distinct Lin – CD34 + CD38 – CD90 – CD45RA + phenotype ( Fig. 6e ). Indeed, in contrast to patients with CP-CML ( Supplementary Fig. 6 ), all patients with BC analyzed showed a marked expansion of Lin – CD34 + CD38 – CD90 – CD45RA + lymphoid-primed multipotent progenitor (LMPP)-like cells ( Supplementary Fig. 15 ), a population previously implicated in the propagation of acute leukemia 38 .
Finally, to explore a possible genetic basis for clonal evolution within the pre-BC SCs, we carried out exome sequencing of the patient with early lymphoid BC, which revealed a somatic RUNX1 mutation (c.G521A, Supplementary Fig. 16a ). To track acquisition of the RUNX1 mutation within the BCR-ABL + SC compartment, we carried out parallel targeted amplification of both BCR-ABL and the RUNX1 mutation. All four pre-BC cells falling in the CP-SC cluster were RUNX1 wild-type. By contrast, all RUNX1 mutated pre-BC SCs ( n = 43) were found within the BC-SC cluster ( P < 0.01). This distinct distribution of the RUNX1 mutation was confirmed by single-cell qPCR ( Supplementary Fig. 16b,c ). Furthermore, differentially expressed genes between the pre-BC CP-SC and BC-SC clusters were typically RUNX1 target genes ( Fig. 6f ). These findings are consistent with the acquisition of a RUNX1 mutation as a key genomic event occurring during pre-BC, which drives subsequent BC transformation—at least in this one patient—with an expansion of lympho-myeloid transcriptionally primed LMPP-like SCs preceding the clinical BC. This is also consistent with our observed expansion of this distinct SC population in both patients with myeloid and lymphoid BC ( Supplementary Fig. 15 ). These data illustrate how integrated single-cell gene expression, mutational profiling and index sorting can be used to unravel CSC heterogeneity and reveal insights that may help to predict and understand subsequent disease progression.
Discussion
Single-cell gene-expression approaches offer great promise to explore the cellular heterogeneity that might underlie therapy resistance and disease progression in cancer 1 , 2 , 3 , 8 , 10 , 11 , 16 , 17 , none the least in rare CSC populations. This is of crucial importance, given that therapeutic elimination of all CSCs is not only required but might also be sufficient to cure cancers 3 . However, a lack of coverage in the RNA-sequencing data has precluded parallel mutation analysis 10 , 11 , representing a major limitation with current techniques.
We used CML as the disease model for single-cell CSC analysis because the identity of the CSC compartment is well established 39 , and the persistence of rare CML-SCs during therapy remains a key challenge 16 . Although certain cell-surface markers have been proposed to allow for selective enrichment of CML-SCs 40 , 41 , 42 , they are not reproducible across all patients, nor do they allow for effective purification of BCR-ABL + CML-SCs during remission. In reality, the presence of BCR-ABL remains the only unequivocal marker of CML-SC. Therefore, we herein established a method for single-cell RNA sequencing with markedly improved sensitivity for BCR-ABL detection as compared to standard techniques. This new technique uniquely allowed us to selectively analyze aberrant gene expression in BCR-ABL − SCs at diagnosis, which is of relevance in view of recent findings that cell-extrinsic factors disrupt normal stem/progenitor cells in CML mouse models and other hematological malignancies 21 , 22 , 23 . Our analysis revealed marked dysregulation of the TGF-β and TNF-α pathways in BCR-ABL − (as well as BCR-ABL + ) SCs, associated with increased SC quiescence. Moreover, we uncovered heterogeneity of BCR-ABL − SCs in patients with CML, with a distinct cluster of BCR-ABL − SCs already dominant at diagnosis in patients who later failed to achieve MMR on TKI treatment. Indeed, elevated serum levels of TNF-α and TGF-α also correlate with poor treatment response in CML 43 . Further validation studies in larger patient cohorts will be required to determine whether gene expression signatures of BCR-ABL − SCs might have utility as a clinically predictive biomarker. Targeting inflammatory pathways such as TGF-β and TNF-α might also be of therapeutic value, by reducing microenvironment-induced quiescence of CML-SCs, although further preclinical evidence of the feasibility of such an approach is needed before this could be taken forward into a clinical trial setting.
Our single-cell method also provided a unique opportunity to assess rare BCR-ABL + SCs persisting during TKI-induced remission 16 , 17 . It was not possible to analyze resistant CML-SCs in patients who had already achieved deep molecular remissions owing to the very low frequency of BCR-ABL + SCs in these patients. However, analysis of samples from patients established on TKI, including serial samples and patients on long-term TKI (>1 year), identified a distinct subpopulation of highly quiescent BCR-ABL + SCs, already present at diagnosis, that is markedly selected for during otherwise clinically effective TKI treatment. Quiescence is a hallmark of many normal SCs, including HSCs, that confers selective resistance to therapeutic targeting 44 , 45 . Crucially, our data, acquired using a whole-transcriptome approach, support that TKI-resistant CML-SCs are transcriptionally distinct from quiescent normal HSCs, with dysregulation of specific genes and pathways (TGF-β, TNF-α, JAK–STAT, CTNNB1 and NFKB1A ) that might be selectively targeted in CML-SCs. Another recent study applied a single-cell targeted gene expression analysis of BCR-ABL + CML-SCs 46 , rather than unbiased single-cell global RNA sequencing. Although the much more restricted gene expression analysis focused on the heterogeneity of lineage programs in BCR-ABL + stem cells and improved strategies for prospective purification of CML-SCs, the findings in those studies also supported a TKI-induced enrichment of quiescent BCR-ABL + stem cells, albeit investigated following short-term TKI treatment only.
CML is an ideal tractable disease model to which to apply this single-cell technique because of its relative genomic simplicity 15 . However, a number of our findings might also be more generally applicable to other malignant disease. For example, although limited by the relatively small numbers of BC patient samples available, our analysis of patients with BC-CML supports the idea that a single-cell approach may prove powerful for predicting imminent disease progression in CSC populations. Specifically, our ability to detect RUNX1 mutations in distinct BC CML-SCs subclones shows how a single-cell approach can help to unravel the mechanisms underlying clonal progression associated with certain mutations at the CSC level. However, further work is required to determine the feasibility of applying this new method to the detection of a range of other mutations and a number of possible limitations in the approach need to be considered. Some tumors are characterized by exceedingly complex clonal heterogeneity. It is likely that there will be a limitation in relation to the number of mutations that could be detected simultaneously by targeted amplification in individual cells before this affects the complexity of the RNA-seq library generated, although this remains to be determined. Our technique also relies on the transcriptional expression of the mutation of interest, and given the increasing level of interest in mutations in the noncoding space 47 , further modifications to this approach will be required, for example, to enable parallel genomic DNA analysis. Furthermore, to obtain a high level of sensitivity for BCR-ABL detection, the amplicon size used in this study was short and did not encompass the kinase domain of ABL. Longer BCR-ABL amplicons were less efficient at BCR-ABL detection (data not shown). We were therefore unable to detect the presence of kinase-domain mutations in individual cells, which are of relevance for TKI resistance 48 . Further modification to our technique will be required to detect multiple, distantly located mutations occurring within the same allele.
In summary, we present a novel method that allows for simultaneous single-cell RNA sequencing and high-sensitivity, targeted mutation detection. We demonstrate how this technique can be applied to unravel heterogeneity in clonal CSCs, as well as in coexisting and frequently suppressed normal SCs, to provide insights into cellular and molecular mechanisms of therapy resistance and clonal evolution. In principle, this approach could be applied across a broad range of clonal disorders. Although considerable technical challenges remain in relation to the standardization of single-cell genomics techniques, we anticipate that the next few years will see major inroads toward clinical application of this powerful new technology.
Methods
Cell lines.
Authenticated K562 and mycoplasma-negative (chronic myeloid leukemia, human cell line) cells were obtained from the American Type Culture Collection (ATCC) and grown in Iscove's modified Dulbecco's media (IMDM), 10% fetal bovine serum (FBS).
Samples and bone marrow mononuclear cells processing.
Patients with CML included in the study, and their clinical details, are listed in Supplementary Table 1 . Patients provided written informed consent in accordance with the Declaration of Helsinki for sample collection and use in research under Oxford University ethics committee approval (MREC 06/Q1606/110). Bone marrow (BM) mononuclear cells (MNCs) were isolated using Ficoll density gradient. Cryopreserved BM mononuclear cells (MNCs) were thawed and processed for flow cytometry analysis, as previously described 4 .
FACS staining and single-cell sorting.
All FACS experiments included single-color-stained CompBeads (BD Biosciences) and fluorescence-minus-one (FMO) controls. Live cells were selected on the basis of their nonpermeability and subsequent lack of fluorescence associated with 7AAD or DAPI. The combination of monoclonal antibodies used to identify hematopoietic stem and progenitor cell populations was previously described 4 and is shown in Supplementary Table 12 . The cocktail of lineage markers used (Lin) was: CD2, CD3, CD4, CD7, CD8a, CD10, CD11b, CD14, CD19, CD20, CD56 and CD235ab. Single cells were isolated from BM samples of healthy controls or patients with CML. Single cells were FACS-sorted as Lin – CD34 + CD38 − . For some experiments, index-sort data of the mean fluorescence intensities (MFI) of CD90, CD45Ra and CD123 were also recorded for each individual cell isolated.
Single-cell sorting was performed on FACS ARIA II, FACS ARIA III or FACS ARIA Fusion (Becton Dickinson) directly into 96-well plates (PCR microplate Thermo-Fast 96 well, semi-skirted). To check the correct alignment of the sorter, BD FACS Accudrop Beads (BD Biosciences) were deposited initially onto the lid or film cover of a setup plate. After this sort, 50 beads were sorted into several wells of a clean PCR plate where it was checked that the beads formed a discrete drop in the center of the bottom of the well. If any splashing was noticed on the sides of the well, the alignment was adjusted. Single 488-Flow-Check Fluorospheres (Beckman Coulter) were then deposited into each well of a flat-bottomed, 96-well tissue-culture plate, and single-cell mode sorting was verified by checking the presence of 1 fluorosphere/well using a conventional fluorescence microscope. The investigators were not blinded when performing this and following steps of the experiments. Experiments were not randomized.
Short-term culture from single cells for first division measurement.
Single Lin – CD34 + CD38 − cells from normal BM donors or from patients with CML were sorted using FACSAriaIII into 60-well Terasaki plates containing 25 μl of Stemspan SFEM (Stemcell Technologies) medium supplemented with 10% BIT 9500 serum substitute (Stemcell Technologies), 2-mM L -glutamine (P A A Laboratories), 10-4 M 2-mercaptoethanol (Sigma-Aldrich), 100 U/ml penicillin/streptomycin (PAA), 100 ng/ml rhSCF (Amgen), 100 ng/ml rhFLT3-ligand (FL; Immunex), 50 ng/ml rhTPO (Peprotech), 10 ng/ml rhIL-3 (Peprotech), 10 ng/ml rhG-CSF (Amgen), 10 ng/ml rhIL-6 (Peprotech). rhTNF-α (Miltenyi Biotec) or rhTGF-β (Miltenyi Biotec) were added to the culture at 20 ng/ml, as indicated. Single cells were scored microscopically for number of cells that had reached time of first division after 96 h of culture.
Fluorescence in situ hybridization (FISH).
For interphase FISH, Lin – CD34 + CD38 − cells were cytocentrifuged onto slides and hybridized with the LSI BCR/ABL Dual Color, Dual Fusion Translocation Probe (Abbot Molecular) spanning the ABL1 and BCR respective breakpoints involved in the t(9:22) translocation (ABL1: 9q34, BCR: 22q11.2). Fluorescence images were obtained with the use of fluorescence microscopy. In nuclei from normal cells lacking the t(9:22) translocation, the probe hybridizing to the ABL1 region appears as two orange signals, whereas the probe hybridizing to the BCR region appears as two green signals. Nuclei containing a balanced t(9;22) will display one orange and one green signal from the normal chromosomes 9 and 22 and two orange/green (yellow) fusion signals, one each from the derivative chromosomes 9 and 22.
Generation of single-cell cDNA libraries using Smart-seq2 protocol.
Single K562 or Lin – CD34 + CD38 − cells were FACS-sorted into 96-well plates (Thermo) containing 4 μl of a lysis mix, including oligo dT (Biomers), RNAse inhibitor (Takara) and dNTPs mix (Fermentas), at concentrations described in the original Smart-seq2 protocol and listed in Supplementary Table 13 24 . ERCC spikes (AMbion) were pre-diluted to 1:400,000 from stock concentration and added to the lysis mix at a final dilution of 1:40,000,000. ERCC spikes were not included in the analysis of patient samples, given that a number of samples were analyzed before ERCC spikes were routinely included in the reaction. Retrotranscription and PCR amplification steps were performed following the Smart-seq2 protocol using reagent concentrations optimized for small cells ( Supplementary Table 13 ). The thermal conditions for RT and PCR reactions were according to the original Smart-seq2 protocol. The number of cycles used for PCR amplification was 22. After PCR amplification, cDNA libraries from single cells were purified using Ampure XP magnetic beads according to the manufacturer's instructions, in a ratio of 0.8 to 1 with cDNA. After purification, the libraries were resuspended in 17.5 μl of buffer EB (Qiagen) and stored at –20 °C. Quality and concentration of the cDNA libraries generated was assessed using High-Sensitivity Bioanalyzer (Agilent).
Generation of single-cell cDNA libraries using BCR-ABL tSS2 protocol.
BCR-ABL targeted amplification Smart-seq2 protocol (tSS2) was implemented during both RT and PCR steps of Smart-seq2, as described in Supplementary Figure 2 . During RT and PCR amplification, a pair of primers recognizing the BCR and the ABL portion of the fusion transcripts (sequences indicated in Supplementary Fig. 2b ) were added to the RT and PCR mixes, respectively, at the concentrations indicated in Supplementary Figure 2c in condition 6. The primers pair was designed to give rise to a PCR amplicon of 505 bp for BCR-ABL e14a2 transcript and 430 for BCR-ABL e13a2 transcript ( Supplementary Table 13 ).
Generation of single-cell cDNA libraries using BCR-ABL targeted amplification protocol with C1 microfluidic platform.
K562 cells were captured on a large-sized (17- to 25-μm cell diameter) C 1 Single-Cell Auto Prep IFC for mRNA sequencing (Fluidigm) using the Fluidigm C1 system. Cells were loaded onto the chip at a concentration of ∼ 250k cells/ml and imaged by phase-contrast microscopy to check single-cell per capture site. Cells were lysed and cDNA prepared on the C1 Fluidigm chip, according to the manufacturer's protocol, using SMARTer Ultra Low RNA kit for Illumina (Clontech). BCR-ABL targeted amplification in the C1 setting was performed using the modified C1 PCR MIX protocol described in Supplementary Table 14 . BCR-ABL Taqman assay (20X) was included in the C1 PCR MIX at a final dilution of 1:495. Any other step in the C1 protocol was performed following manufacturer's indications.
Illumina library preparation and sequencing.
1.25 μl of cDNA was used for tagmentation reaction carried out with Nextera XT DNA Sample Preparation kit (Illumina) according to the manufacturer's instructions, but using one-fourth of the volumes. Purification of the product was done with a 1:1 ratio of AMPure XP beads, with a final elution in 17.5 μl in resuspension buffer provided from the Nextera kit. Samples were loaded on a High-Sensitivity DNA chip (Agilent Technologies) to check the size and quality of the indexed library, and the concentration was measured with Qubit High-Sensitivity DNA kit (Invitrogen). BCR-ABL + or BCR-ABL − SCs eligible for sequencing were selected on the basis of the quality of their indexed cDNA libraries (size 400–900 bp; concentration >4 ng/ml). The number of BCR-ABL + or BCR-ABL − SCs to be sequenced per patient was determined by availability of SCs from each sample and space available per flow cell to ensure sufficient depth of sequencing. Libraries were pooled to a final concentration ranging between 3 nM and 10 nM and were sequenced with Illumina HiSeq 2000 and Illumina Hiseq 4000 (51 bp single-end read) at the Wellcome Trust Centre for Human Genetics in Oxford.
BCR-ABL genotyping of single-cell cDNA libraries.
BCR-ABL genotyping of cDNA libraries from single cells was performed using a qPCR reaction in a 384-well plate (Roche, Lightcycler). qPCR was performed in duplicate using 1.5 μl of the cDNA library for each reaction. The expression levels of BCR-ABL and GAPDH were measured using the following Taqman FAM-MGB assays BCR-ABL : Hs03024541_ft and GAPDH : Hs02758991_g1 (Life Technologies). The reactions were performed using a minimum of 60 cycles of amplification. We used qPCR and not raw sequencing reads to genotype cells for presence of BCR-ABL owing to the low coverage of BCR-ABL in the sequencing data.
Exome sequencing.
Genomic DNA was extracted from unfractionated BM MNCs from patient OX1931 at both pre-BC and BC stages using QIAamp DNA Blood Mini Kit (Qiagen) according to the manufacturer's instructions. Exome capture was performed from GATC Biotech, using INVIEW Human Exome Library preparation Enrichment with SureSelectXT Human All Exon Kit for Illumina Paired-End Sequencing (Read length: 2 × 125 bp). The number of PCR cycles performed for the amplification of the adaptor-ligated library was five. The number of cycles used for the posthybridization captured library amplification step was 12. The enriched exome fragments were pooled and paired-end sequenced on a HiSeq 2000 platform (Illumina). From this, we obtained >60× on target coverage for the majority of positions for each of the samples.
Assessment of BCR-ABL tSS2 sensitivity using plasmid spike-in.
BCR-ABL breakpoint region (e14a2) was PCR-amplified from cDNA of K562 cells using specific BCR-ABL primer set #1 described in Supplementary Figure 2b . The resulting PCR amplicon was Sanger sequenced before being cloned into the pcr- Blunt II-TOPO vector using Zero Blunt TOPO PCR Cloning Kit (Thermo Fisher). Correct size of the BCR-ABL insert was verified by PCR. Concentration of the resulting BCR-ABL plasmid was measured using Qubit (Invitrogen), and the absolute number of plasmid copies/μl was calculated. Several plasmid pre-dilutions were produced to be able to spike in the retro-transcription reaction of single BCR-ABL − SCs (HSCs from a normal donor), the desired amount of plasmid copies (1, 2, 5,10, 20, 50, 100 and 1,000) always at a volume of 1 μl. The PCR step was performed according to the standard BCR-ABL tSS2 protocol. Quantification of the absolute number of BCR-ABL amplified copies after BCR-ABL tSS2 reaction was carried out by qPCR (Roche, Lightcycler) using a commercial BCR-ABL standard curve as a reference (Ipsogen BCR-ABL 1 Mbcr, Qiagen).
RUNX1 c.G521A detection with single-cell qPCR.
RUNX1 c.G521A mutation (NM_001001890 or NM_001122607 c.521G>A or NM_001754 c.602G>A; GRCh38 21:34859485C>T) detected in patient OX1931 by exome sequencing was PCR amplified and validated by Sanger sequencing. (Fw:GGCTGGCAATGATGAAAACT and Rev:CAATGGATCCCAGGTATTGG). A SNP genotyping Taqman assay specific for RUNX1 c.G521A was designed using the Custom Assay Design tool (ThermoFisher) and validated on positive (OX1931) and negative controls ( Supplementary Table 15 ).
Single-cell gene expression analysis.
For single-cell gene expression analysis, single cells isolated by FACS were collected in each well of a 96-well plate containing 5 μl of Cells Direct One-Step qRT–PCR (Invitrogen) mix and pre-amplified as previously described 49 . Pre-amplified samples were diluted 1:5 with TE before the analysis of gene expression on either a Fluidigm 96.96 or 192.24 Dynamic array using gene-specific Taqman assays (Life technologies). No template and no reverse transcriptase were included as negative controls.
Analysis of quantitative PCR single-cell gene expression data.
We calculated ΔCt values, which are relative to the mean expression level of two housekeeping genes ( B2M and GAPDH ). As previously described 25 , 50 , Ct values were subtracted from the limit of detection (CT = 30) followed by subtraction of the mean Ct value of housekeeping genes for each cell. Ct = 40 was used for the comparative analysis of the detection of BCR-ABL and GAPDH in K562 cells between Smart-seq2 and BCR-ABL tSS2 protocols. Cells not expressing at the 15th percentile of all genes, or of two housekeeping genes, were removed from the analysis. Analysis of differential gene expression between BCR-ABL + and BCR-ABL − SCs was performed using the Wilcoxon test and Fisher's exact test to compare expression level and expression frequency, respectively.
Analysis of single-cell RNA sequencing.
Short reads (51 bp) were aligned to the human genome (GRCh37 assembly (hg19)) using Tophat 51 with a supplied set of known RefSeq transcripts as the input. The mapping parameters '-g 1' was used to allow one alignment to the reference for a given read. Expression values were quantified as read per kilobase of transcript length per million mapped reads (RPKM) on the basis of the RefSeq gene model using the rpkmforgenes 52 . As previously demonstrated, single-cell analyses reliably identified distinct subpopulations of cells at a sequencing depth of 50,000 reads per cell 53 , 54 , we used cells with higher than 50,000 mapping reads and 1,000 detected genes (RPKM ≥1) for the downstream analysis. We used the genes that were highly expressed in more than 50% of each population of cells to identify the candidate outliers on the basis of gene expression level, similar to the method previously described in Singular from Fluidigm, using the standard method for the outlier detection 55 . The modified Z -scores were calculated using the formula 0.6745(xi - ×)/MAD; MAD denoting the median absolute deviation and x denoting the median. Cells with an absolute modified Z -score of greater than 3 were considered to be candidate outliers (28 out of 2,287 cells), and these cells were monitored during the analysis. We found that excluding or including them in our analysis did not have any notable impact on the results.
Analysis of the effective sequencing depth.
To examine the effective sequencing depth, we selected 12 normal HSCs with a sequencing depth larger than 6 million mapped reads. We randomly sampled reads in the range of 0.1 million to 6 million mapped reads and calculated a number of detected genes with RPKM ≥1 in each category. We observed that the detected number of genes plateaued at a sequencing depth of beyond 1 million mapped reads per cell ( Fig. 2a ).
T-distributed stochastic neighbor embedding (tSNE) analysis.
As previously described, the advantage of using tSNE over a traditional principal-component analysis is to visualize the projection of high-dimensional single-cell gene expression data into a low-dimensional space 25 , 56 , 57 . We selected genes expressed in ≥10 cells with a coefficient of variation score (CV), “standard deviation/mean,” ≥1 and the sum of expression values per gene of all analyzed cells in log 2 scale ≥1 for the tSNE analysis. We normalized the RPKM values into log 2 (RPKM) scale and set up the limit of detection at 1 RPKM. Log 2 scale of genes expressed at <1 RPKM was set to 0. Possible batches from processing samples in different dates were removed from expression values using the function “removeBatchEffect” in Limma package 58 . We then downloaded the tSNE software from https://lvdmaaten.github.io/tsne/ to perform the analysis, using the Matlab implementation with “initial dims=20” and “perplexity=20” parameters.
To identify highly variable genes, similarly to a previously described approach 56 , we fitted a simple noise model using the lowess model of mean expression level and the coefficient of variation (CV) to estimate the variable genes from each type of cells. The lowess model predicted 3,368, 5,611, and 5,011 and 5,522 genes from K562, BCR-ABL − and BCR-ABL + SCs (from diagnosis), and normal HSCs, respectively, that show high variation as compared to the whole genes set with mean of expression log 2 (RPKM) higher than 0. We next used these genes for the tSNE analysis, and compared the tSNE results to the previous tSNE results of different gene sets. We found the same pattern of clustering, suggesting reproducibility of our results. We then selected 3,368, 7,428 (combined variable genes from K562 and normal HSCs) and 8,589 (combined variable genes from BCR-ABL − SCs, BCR-ABL + SCs and normal HSCs) genes to generate Figures 1d , 2b and 3c , respectively. 5,011 and 5,611 variable genes in BCR-ABL + and BCR-ABL − SCs were used to generate Figure 4a,b for the good- and poor-responder classifications.
For tSNE analysis of samples following TKI therapy, we performed the random-forests analysis of normal HSCs, BCR-ABL + SCs (diagnosis) and BCR-ABL + SCs (remission) cells using the “randomForest” package in R (ntree parameter = 2,000). We obtained the top-500 important genes, as measured by the Gini index ( Supplementary Table 7 ). These genes were used to distinguish normal HSCs from BCR-ABL + SCs at diagnosis and during remission. We next used this gene set for tSNE analysis of the remission cells ( Fig. 5a ). We applied K -means clustering ( k = 3) on the basis of tSNE analysis results (from dimensions 1 and 2) to assign remission cells to group A and group B ( Fig. 5a ).
For tSNE analysis of normal HSCs and K562 and BCR-ABL + SCs from diagnosis, pre-BC and BC samples, we obtained combined differentially expressed genes from the multiple-ways comparison. 207 genes shown to be differentially expressed between BCR-ABL + SCs from 18 patients with chronic-phase CML ( n = 477), BCR-ABL + SCs at BC ( n = 148), BCR-ABL + SCs at pre-BC ( n = 185) and normal HSCs ( n = 232). We next used this gene set for the tSNE to generate Figure 6a,c and Supplementary Figure 14a . We note that pre-BC cells were involved in the tSNE analysis but were not shown in Figure 6a .
Cell-to-cell variation analysis.
To analyze the variation within K562 and normal HSCs, the Pearson correlation was calculated on the basis of log 2 (RPKM) expression values among the cells of each group by using the same set of genes from the tSNE analysis. A Kolmogorov–Smirnov test was used to test the difference of correlation score distribution ( Supplementary Fig. 4e ).
Differentially expressed gene analysis.
Differentially expressed gene analysis was performed using the nonparametric Wilcoxon test on log 2 (RPKM) expression values for the comparison of expression level and Fisher′s exact test for the comparison of expressing cell frequency. P values generated from both tests were then combined using Fisher's method and were adjusted using Benjamini–Hochberg (BH). Differentially expressed genes were selected on the basis of the absolute log 2 fold change of ≥1 and the adjusted P value of <0.05. Selected genes were subjected to the hierarchical clustering analysis using Pearson correlation as a distance, with the complete clustering method performed in R with the “pheatmap” function. Beeswarm plots from selected genes were generated using the “beeswarm” package in R. We determined the top 100 differentially expressed genes ranked by adjusted P values from normal HSCs against BCR-ABL − and BCR-ABL + SCs, and BCR-ABL − against BCR-ABL + SCs at diagnosis. We then used the 245 unique genes from this analysis to make the heat map of Figure 3d .
Gene-set enrichment analysis.
GSEA 59 was performed using GSEA software ( http://www.broadinstitute.org/gsea ) with permutation on the phenotype, 1,000 permutations, and default values for other parameters. Gene sets used in this study were selected from the CML-, proliferation-, quiescence- and HSC-related pathways shown in Supplementary Table 3 and the MSigDB hallmark gene sets ( Supplementary Table 5 and http://www.broadinstitute.org/gsea/msigdb/collections.jsp ).
Comparison of bulk and single-cell analysis.
To compare differentially expressed genes identified between analysis performed at the bulk level and at the single-cell level, in silico bulk data were generated by generating a data 'ensemble,' by combining mapped reads per gene for all HSCs from five normal donors (the ensemble of single cells from five donors, plus one set of normal HSCs from a sixth donor that were isolated as a bulk population of 100 cells rather than as single cells). 18 replicates were generated from the ensemble of single cells from each patient with CML. DESeq2 (ref. 60 ) was then performed from the raw read count of the ensemble to get differentially expressed genes. We then performed differentially expressed genes analysis for the single-cell analysis, as described above, using 232 single normal-HSCs against 477 BCR-ABL + SCs and 377 BCR-ABL − SCs. To make a comparison of differentially expressed genes, we applied the same cutoff (adjusted P value of <0.05 and the absolute log 2 fold change ≥0.5) to get the number of differentially expressed genes from both bulk and single-cell analyses.
Coexpression analysis of G2M, lymphoid- and myeloid-associated genes.
We selected a gene set from gene ontology “G2M transition of mitotic cell cycle (GO:0000086)” from “ amigo2.berkeleybop.org/amigo/term/GO:0000086 ” to analyze coexpression. Gene would be called “present” when the quantile-normalized RPKM value was ≥1 and “absent” when RPKM values were <1. We counted the frequency of genes that were expressed in the same cells ( Supplementary Fig. 7h ). We calculated the coexpression frequency of random gene sets, excluding cell-cycle-related genes as the background. A Kolmogorov–Smirnov test was used to test the difference of correlation-score distribution. For the analysis of coexpression of lymphoid- and myeloid-associated genes, we selected known lymphoid- and myeloid-associated genes to show the coexpression analysis in the CP-CML, BC-CML and normal-HSC clusters. The heat map was generated using the log 2 (RPKM) with the pheatmap function in R ( Fig. 6d ).
Chromatin immunoprecipitation (ChIP)-seq analysis.
RUNX1 and IgG control ChIP-seq data (CD34 + HSPCs) 61 were downloaded from the Gene Expression Omnibus (GEO) database ( GSE45144 ). Raw reads were mapped to the human genome (GRCh37 assembly (hg19)) using bowtie2 (ref. 62 ) with default parameters. The peak calling was performed by MACS2 (ref. 63 ), using default parameters, with IgG ChIP-seq data as a control. 8,706 RUNX1 binding sites were identified with 5% FDR. We next calculated the distribution of distances between RUNX1 binding sites and transcription start sites (TSS) of differentially expressed genes that are between the CP-CML and the BC-CML clusters. We further analyzed the fraction of RUNX1 binding sites/window (ranging from ± 0.5-kb to ± 10-kb windows around a TSS of a gene) found in the differentially expressed genes in comparison to 2,000 randomly selected background genes ( Fig. 6f ).
Code availability.
R and MATLAB scripts used for data analyses are available on request.
Statistical analysis.
All statistical analyses were performed in R and GraphPad Prism 6 (GraphPad Software, San Diego, CA). For single-cell expression levels, a nonparametric Wilcoxon test was used, and Fisher′s exact test was used to compare expression frequencies at the single-cell level between defined populations. No statistical method was used to predetermine sample size, and experiments were not randomized. The investigators were not blinded to allocation during experiments or outcome assessment.
Data-availability statement.
Single-cell RNA sequencing data are available at the NCBI's GEO data repository with the accession code GSE76312 . Source data are available for Figures 1 , 2 , 3 , 4 , 5 , 6 .
Accession codes
Primary accessions
Gene Expression Omnibus
GSE76312
Referenced accessions
Gene Expression Omnibus
GSE45144
References
McGranahan, N. & Swanton, C. Biological and therapeutic impact of intratumor heterogeneity in cancer evolution. Cancer Cell 27 , 15–26 (2015).
Article CAS PubMed Google Scholar
Tehranchi, R. et al. Persistent malignant stem cells in del(5q) myelodysplasia in remission. N. Engl. J. Med. 363 , 1025–1037 (2010).
Article CAS PubMed Google Scholar
Magee, J.A., Piskounova, E. & Morrison, S.J. Cancer stem cells: impact, heterogeneity, and uncertainty. Cancer Cell 21 , 283–296 (2012).
Article CAS PubMed PubMed Central Google Scholar
Woll, P.S. et al. Myelodysplastic syndromes are propagated by rare and distinct human cancer stem cells in vivo. Cancer Cell 25 , 794–808 (2014).
Article CAS PubMed Google Scholar
Sloma, I. et al. Genotypic and functional diversity of phenotypically defined primitive hematopoietic cells in patients with chronic myeloid leukemia. Exp. Hematol. 41 , 837–847 (2013).
Article CAS PubMed Google Scholar
Mustjoki, S. et al. Impact of malignant stem cell burden on therapy outcome in newly diagnosed chronic myeloid leukemia patients. Leukemia 27 , 1520–1526 (2013).
Article CAS PubMed Google Scholar
Alizadeh, A.A. et al. Toward understanding and exploiting tumor heterogeneity. Nat. Med. 21 , 846–853 (2015).
Article CAS PubMed PubMed Central Google Scholar
Wills, Q.F. & Mead, A.J. Application of single-cell genomics in cancer: promise and challenges. Hum. Mol. Genet. 24 , R74–R84 (2015).
Article CAS PubMed PubMed Central Google Scholar
Wang, Y. & Navin, N.E. Advances and applications of single-cell sequencing technologies. Mol. Cell 58 , 598–609 (2015).
Article CAS PubMed PubMed Central Google Scholar
Patel, A.P. et al. Single-cell RNA-seq highlights intratumoral heterogeneity in primary glioblastoma. Science 344 , 1396–1401 (2014).
Article CAS PubMed PubMed Central Google Scholar
Miyamoto, D.T. et al. RNA-seq of single prostate CTCs implicates noncanonical Wnt signaling in antiandrogen resistance. Science 349 , 1351–1356 (2015).
Article CAS PubMed PubMed Central Google Scholar
Tirosh, I. et al. Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq. Science 352 , 189–196 (2016).
Article CAS PubMed PubMed Central Google Scholar
Druker, B.J. et al. Effects of a selective inhibitor of the Abl tyrosine kinase on the growth of Bcr-Abl positive cells. Nat. Med. 2 , 561–566 (1996).
Article CAS PubMed Google Scholar
Goldman, J.M. & Melo, J.V. Targeting the BCR-ABL tyrosine kinase in chronic myeloid leukemia. N. Engl. J. Med. 344 , 1084–1086 (2001).
Article CAS PubMed Google Scholar
Longo, D.L. Imatinib changed everything. N. Engl. J. Med. 376 , 982–983 (2017).
Article PubMed Google Scholar
Gallipoli, P., Abraham, S.A. & Holyoake, T.L. Hurdles toward a cure for CML: the CML stem cell. Hematol./oncol. Clinics North Am. 25 , 951–966 (2011).
Article Google Scholar
Chu, S. et al. Persistence of leukemia stem cells in chronic myelogenous leukemia patients in prolonged remission with imatinib treatment. Blood 118 , 5565–5572 (2011).
Article CAS PubMed PubMed Central Google Scholar
Mahon, F.X. et al. Discontinuation of imatinib in patients with chronic myeloid leukaemia who have maintained complete molecular remission for at least 2 years: the prospective, ulticenter Stop Imatinib (STIM) trial. Lancet Oncol. 11 , 1029–1035 (2010).
Article CAS PubMed Google Scholar
Schepers, K. et al. Myeloproliferative neoplasia remodels the endosteal bone marrow niche into a self-reinforcing leukemic niche. Cell Stem Cell 13 , 285–299 (2013).
Article CAS PubMed PubMed Central Google Scholar
Colmone, A. et al. Leukemic cells create bone marrow niches that disrupt the behavior of normal hematopoietic progenitor cells. Science 322 , 1861–1865 (2008).
Article CAS PubMed Google Scholar
Schepers, K., Campbell, T.B. & Passegué, E. Normal and leukemic stem cell niches: insights and therapeutic opportunities. Cell Stem Cell 16 , 254–267 (2015).
Article CAS PubMed PubMed Central Google Scholar
Welner, R.S. et al. Treatment of chronic myelogenous leukemia by blocking cytokine alterations found in normal stem and progenitor cells. Cancer Cell 27 , 671–681 (2015).
Article CAS PubMed PubMed Central Google Scholar
Reynaud, D. et al. IL-6 controls leukemic multipotent progenitor cell fate and contributes to chronic myelogenous leukemia development. Cancer Cell 20 , 661–673 (2011).
Article CAS PubMed PubMed Central Google Scholar
Picelli, S. et al. Full-length RNA-seq from single cells using Smart-seq2. Nat. Protoc. 9 , 171–181 (2014).
Article CAS PubMed Google Scholar
Wilson, N.K. et al. Combined single-cell functional and gene expression analysis resolves heterogeneity within stem cell populations. Cell Stem Cell 16 , 712–724 (2015).
Article CAS PubMed PubMed Central Google Scholar
Wu, S.Q. et al. Extensive amplification of bcr/abl fusion genes clustered on three marker chromosomes in human leukemic cell line K-562. Leukemia 9 , 858–862 (1995).
CAS PubMed Google Scholar
Wu, A.R. et al. Quantitative assessment of single-cell RNA-sequencing methods. Nat. Methods 11 , 41–46 (2014).
Article CAS PubMed Google Scholar
Islam, S. et al. Highly multiplexed and strand-specific single-cell RNA 5′ end sequencing. Nat. Protoc. 7 , 813–828 (2012).
Article CAS PubMed Google Scholar
Bruns, I. et al. The hematopoietic stem cell in chronic phase CML is characterized by a transcriptional profile resembling normal myeloid progenitor cells and reflecting loss of quiescence. Leukemia 23 , 892–899 (2009).
Article CAS PubMed Google Scholar
Miyawaki, K. et al. The expansion of CML clones initiates at the CMP stage, and is associated with the down-regulation of IRF8 and GFI1. Blood 122 , 1477 (2013).
Article Google Scholar
Schuettpelz, L.G. & Link, D.C. Regulation of hematopoietic stem cell activity by inflammation. Front. Immunol. 4 , 204 (2013).
Article CAS PubMed PubMed Central Google Scholar
King, K.Y. & Goodell, M.A. Inflammatory modulation of HSCs: viewing the HSC as a foundation for the immune response. Nat. Rev. Immunol. 11 , 685–692 (2011).
Article CAS PubMed PubMed Central Google Scholar
Pronk, C.J., Veiby, O.P., Bryder, D. & Jacobsen, S.E. Tumor necrosis factor restricts hematopoietic stem cell activity in mice: involvement of two distinct receptors. J. Exp. Med. 208 , 1563–1570 (2011).
Article CAS PubMed PubMed Central Google Scholar
Cashman, J.D., Eaves, A.C., Raines, E.W., Ross, R. & Eaves, C.J. Mechanisms that regulate the cell cycle status of very primitive hematopoietic cells in long-term human marrow cultures. I. Stimulatory role of a variety of mesenchymal cell activators and inhibitory role of TGF-beta. Blood 75 , 96–101 (1990).
Article CAS PubMed Google Scholar
Baccarani, M. et al. European LeukemiaNet recommendations for the management of chronic myeloid leukemia: 2013. Blood 122 , 872–884 (2013).
Article CAS PubMed PubMed Central Google Scholar
Kentsis, A. et al. Autocrine activation of the MET receptor tyrosine kinase in acute myeloid leukemia. Nat. Med. 18 , 1118–1122 (2012).
Article CAS PubMed PubMed Central Google Scholar
Liu, J.X. et al. Eaf1 and Eaf2 negatively regulate canonical Wnt/β-catenin signaling. Development 140 , 1067–1078 (2013).
Article CAS PubMed Google Scholar
Goardon, N. et al. Coexistence of LMPP-like and GMP-like leukemia stem cells in acute myeloid leukemia. Cancer Cell 19 , 138–152 (2011).
Article CAS PubMed Google Scholar
Jamieson, C.H. Chronic myeloid leukemia stem cells. Hematology Am. Soc. Hematol. Educ. Program. 2008 , 436–442 (2008).
Article Google Scholar
Zhao, K. et al. IL1RAP as a surface marker for leukemia stem cells is related to clinical phase of chronic myeloid leukemia patients. Int. J. Clin. Exp. Med. 7 , 4787–4798 (2014).
PubMed PubMed Central Google Scholar
Herrmann, H. et al. Dipeptidylpeptidase IV (CD26) defines leukemic stem cells (LSC) in chronic myeloid leukemia. Blood 123 , 3951–3962 (2014).
Article CAS PubMed Google Scholar
Gerber, J.M. et al. Genome-wide comparison of the transcriptomes of highly enriched normal and chronic myeloid leukemia stem and progenitor cell populations. Oncotarget 4 , 715–728 (2013).
Article PubMed PubMed Central Google Scholar
Nievergall, E. et al. TGF-α and IL-6 plasma levels selectively identify CML patients who fail to achieve an early molecular response or progress in the first year of therapy. Leukemia 30 , 1263–1272 (2016).
Article CAS PubMed Google Scholar
Trumpp, A., Essers, M. & Wilson, A. Awakening dormant haematopoietic stem cells. Nat. Rev. Immunol. 10 , 201–209 (2010).
Article CAS PubMed Google Scholar
Clevers, H. The cancer stem cell: premises, promises and challenges. Nat. Med. 17 , 313–319 (2011).
Article CAS PubMed Google Scholar
Warfvinge, R. et al. Single-cell molecular analysis defines therapy response and immunophenotype of stem cell subpopulations in CML. Blood http://dx.doi.org/10.1182/blood-2016-07-728873 (2017).
Mansour, M.R. et al. Oncogene regulation. An oncogenic super-enhancer formed through somatic mutation of a noncoding intergenic element. Science 346 , 1373–1377 (2014).
Article CAS PubMed PubMed Central Google Scholar
Soverini, S., De Benedittis, C., Mancini, M. & Martinelli, G. Present and future of molecular monitoring in chronic myeloid leukaemia. Br. J. Haematol. 173 , 337–349 (2016).
Article PubMed Google Scholar
Sanjuan-Pla, A. et al. Platelet-biased stem cells reside at the apex of the haematopoietic stem-cell hierarchy. Nature 502 , 232–236 (2013).
Article CAS PubMed Google Scholar
Guo, G. et al. Resolution of cell fate decisions revealed by single-cell gene expression analysis from zygote to blastocyst. Dev. Cell 18 , 675–685 (2010).
Article CAS PubMed Google Scholar
Kim, D. et al. TopHat2: accurate alignment of transcriptomes in the presence of insertions, deletions and gene fusions. Genome Biol. 14 , R36 (2013).
Article CAS PubMed PubMed Central Google Scholar
Ramsköld, D., Wang, E.T., Burge, C.B. & Sandberg, R. An abundance of ubiquitously expressed genes revealed by tissue transcriptome sequence data. PLoS Comput. Biol. 5 , e1000598 (2009).
Article CAS PubMed PubMed Central Google Scholar
Pollen, A.A. et al. Low-coverage single-cell mRNA sequencing reveals cellular heterogeneity and activated signaling pathways in developing cerebral cortex. Nat. Biotechnol. 32 , 1053–1058 (2014).
Article CAS PubMed PubMed Central Google Scholar
Streets, A.M. & Huang, Y. How deep is enough in single-cell RNA-seq? Nat. Biotechnol. 32 , 1005–1006 (2014).
Article CAS PubMed Google Scholar
Iglewicz, B. & Hoaglin, D.C. How to detect and handle outliers (ASQC Quality Press, Milwaukee, Wis., 1993).
Zeisel, A. et al. Brain structure. Cell types in the mouse cortex and hippocampus revealed by single-cell RNA-seq. Science 347 , 1138–1142 (2015).
Article CAS PubMed Google Scholar
Saadatpour, A., Guo, G., Orkin, S.H. & Yuan, G.C. Characterizing heterogeneity in leukemic cells using single-cell gene expression analysis. Genome Biol. 15 , 525 (2014).
Article PubMed PubMed Central Google Scholar
Ritchie, M.E. et al. limma powers differential expression analyses for RNA-sequencing and microarray studies. Nucleic Acids Res. 43 , e47 (2015).
Article CAS PubMed PubMed Central Google Scholar
Subramanian, A. et al. Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. Proc. Natl. Acad. Sci. USA 102 , 15545–15550 (2005).
Article CAS PubMed PubMed Central Google Scholar
Love, M.I., Huber, W. & Anders, S. Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. Genome Biol. 15 , 550 (2014).
Article CAS PubMed PubMed Central Google Scholar
Beck, D. et al. Genome-wide analysis of transcriptional regulators in human HSPCs reveals a densely interconnected network of coding and noncoding genes. Blood 122 , e12–e22 (2013).
Article CAS PubMed Google Scholar
Langmead, B. & Salzberg, S.L. Fast gapped-read alignment with Bowtie 2. Nat. Methods 9 , 357–359 (2012).
Article CAS PubMed PubMed Central Google Scholar
Zhang, Y. et al. Model-based analysis of ChIP-Seq (MACS). Genome Biol. 9 , R137 (2008).
Article CAS PubMed PubMed Central Google Scholar
Download references
Acknowledgements
This work was funded by a Medical Research Council Senior Clinical Fellowship (MR/L006340/1), MRC Confidence in Concept award (MC_PC_13073) and Rosetrees Trust award (A712: Rosetrees Trust Award (A712)) to A.J.M., the MRC Molecular Haematology Unit core award (A.J.M. and S.E.W.J.; MC_UU_12009/5), a MRC programme grant to S.E.W.J. (G0801073), an international-recruitment award from the Swedish Research Council (S.E.W.J.), and grants from the Tobias Foundation (S.E.W.J.) and the Center for Innovative Medicine (CIMED) at the Karolinska Institute (S.E.W.J.). This work was also supported by the MRC-funded Oxford Consortium for Single-cell Biology (MR/M00919X/1) and the Oxford NIHR Biomedical Centre based at Oxford University Hospitals NHS Trust and University of Oxford. The views expressed are those of the author(s) and not necessarily those of the NHS, the NIHR, the Department of Health or the NIH. The work was also supported by an educational grant from Novartis. The authors acknowledge the contributions of the WIMM Flow Cytometry Facility, supported by the MRC HIU; MRC MHU (MC_UU_12009); NIHR Oxford BRC and John Fell Fund (131/030 and 101/517), the EPA fund (CF182 and CF170) and by the WIMM Strategic Alliance awards G0902418 and MC_UU_12025. N.A. was supported by the Oxford–Wellcome Trust Institutional Strategic Support Fund. S.M. is supported by the Finnish Cancer Institute and the Finnish Cancer Organizations.
Author information
Author notes
Alice Giustacchini and Supat Thongjuea: These authors contributed equally to this work.
Sten Eirik W Jacobsen and Adam J Mead: These authors jointly directed this work.
Authors and Affiliations
MRC Molecular Hematology Unit, Weatherall Institute of Molecular Medicine, University of Oxford, Oxford, UK
Alice Giustacchini, Supat Thongjuea, Nikolaos Barkas, Benjamin J Povinelli, Christopher A G Booth, Paul Sopp, Ruggiero Norfo, Alba Rodriguez-Meira, Neil Ashley, Lauren Jamieson, Paresh Vyas, Sten Eirik W Jacobsen & Adam J Mead
Haemopoietic Stem Cell Biology Laboratory, Weatherall Institute of Molecular Medicine, University of Oxford, Oxford, UK
Alice Giustacchini, Supat Thongjuea, Nikolaos Barkas, Petter S Woll, Benjamin J Povinelli, Christopher A G Booth, Ruggiero Norfo, Alba Rodriguez-Meira, Neil Ashley, Lauren Jamieson, Sten Eirik W Jacobsen & Adam J Mead
Department of Cellular Therapy, Norwegian Radium Hospital, Oslo University Hospital, Oslo, Norway
Kristina Anderson
Department of Cell and Molecular Biology, Karolinska Institutet, Stockholm, Sweden
Åsa Segerstolpe, Rickard Sandberg & Sten Eirik W Jacobsen
Integrated Cardio Metabolic Center (ICMC), Karolinska Institutet, Huddinge, Sweden
Åsa Segerstolpe
Department of Medicine, Center for Hematology and Regenerative Medicine, Karolinska Institutet, Stockholm, Sweden
Hong Qian & Sten Eirik W Jacobsen
Department of Medical Science and Division of Hematology, University Hospital, Uppsala, Sweden
Ulla Olsson-Strömberg
Department of Clinical Chemistry and Hematology, Hematology Research Unit Helsinki, University of Helsinki and Helsinki University Hospital Comprehensive Cancer Center, Helsinki, Finland
Satu Mustjoki
Ludwig Institute for Cancer Research, Stockholm, Sweden
Rickard Sandberg
Karolinska University Hospital, Stockholm, Sweden
Sten Eirik W Jacobsen
NIHR Biomedical Research Centre, Churchill Hospital, Oxford, UK
Adam J Mead
Authors
Alice Giustacchini
View author publications
Search author on: PubMed Google Scholar
Supat Thongjuea
View author publications
Search author on: PubMed Google Scholar
Nikolaos Barkas
View author publications
Search author on: PubMed Google Scholar
Petter S Woll
View author publications
Search author on: PubMed Google Scholar
Benjamin J Povinelli
View author publications
Search author on: PubMed Google Scholar
Christopher A G Booth
View author publications
Search author on: PubMed Google Scholar
Paul Sopp
View author publications
Search author on: PubMed Google Scholar
Ruggiero Norfo
View author publications
Search author on: PubMed Google Scholar
Alba Rodriguez-Meira
View author publications
Search author on: PubMed Google Scholar
Neil Ashley
View author publications
Search author on: PubMed Google Scholar
Lauren Jamieson
View author publications
Search author on: PubMed Google Scholar
Paresh Vyas
View author publications
Search author on: PubMed Google Scholar
Kristina Anderson
View author publications
Search author on: PubMed Google Scholar
Åsa Segerstolpe
View author publications
Search author on: PubMed Google Scholar
Hong Qian
View author publications
Search author on: PubMed Google Scholar
Ulla Olsson-Strömberg
View author publications
Search author on: PubMed Google Scholar
Satu Mustjoki
View author publications
Search author on: PubMed Google Scholar
Rickard Sandberg
View author publications
Search author on: PubMed Google Scholar
Sten Eirik W Jacobsen
View author publications
Search author on: PubMed Google Scholar
Adam J Mead
View author publications
Search author on: PubMed Google Scholar
Contributions
A.G. designed, performed and analyzed experiments and contributed to writing the manuscript. S.T. designed and performed bioinformatic analyses and contributed to writing the manuscript. N.B. and B.J.P. performed analyses of RNA sequencing and qPCR results. P.S.W. and P.S. were involved in FACS analysis and sorting. R.N., A.R.-M., C.A.G.B. and L.J. performed experiments. N.A. maintained single-cell facility infrastructure. P.V., S.M. and H.Q. provided infrastructure for sample banking and provided input on experimental design and analysis. K.A. performed FISH experiments. Å.S. was involved in RNA-sequencing experiments. U.O.-S. collected clinical information. R.S. provided input on RNA-sequencing experiments. A.J.M. and S.E.W.J. conceived and supervised the project, designed and analyzed experiments and wrote the manuscript.
Corresponding authors
Correspondence to Sten Eirik W Jacobsen or Adam J Mead .
Ethics declarations
Competing interests
A.J.M. has received honoraria and research funding from Novartis.
Supplementary information
Supplementary Text and Figures (download PDF )
Supplementary Figures 1–16 and Table 12–15. (PDF 3114 kb)
Supplementary Table 1 (download XLSX )
Patient demographics and characteristics. (XLSX 46 kb)
Supplementary Table 2 (download XLSX )
Differentially expressed genes between normal HSCs, BCRABL+ and BCR-ABL- SCs from CP-CML patients at diagnosis. (XLSX 186 kb)
Supplementary Table 3 (download XLSX )
Gene-sets from previous studies on CML stem and progenitor cells. (XLSX 113 kb)
Supplementary Table 4 (download XLSX )
Results from GSEA comparing normal HSCs to BCRABL+ SCs and BCR-ABL- SCs from CP-CML patients at diagnosis and using gene-sets from previous studies on CML stem and progenitor cells. (XLSX 24 kb)
Supplementary Table 5 (download XLSX )
Results from GSEA comparing normal HSCs to BCRABL+ SCs and BCR-ABL- SCs from CP-CML patients at diagnosis and using HALLMARK gene sets (XLSX 79 kb)
Supplementary Table 6 (download XLSX )
Results from GSEA comparing diagnostic samples from good and poor responder CML patients. (XLSX 28 kb)
Supplementary Table 7 (download XLSX )
Top 500 informative genes for distinguishing normal-HSCs from BCR-ABL+ SCs at diagnosis and during remission. (XLSX 72 kb)
Supplementary Table 8 (download XLSX )
Results from GSEA on HALLMARK gene-sets comparing remission group-A BCR-ABL+ SCs to remission group-B BCRABL+ SCs. (XLSX 12 kb)
Supplementary Table 9 (download XLSX )
Differentially expressed genes between normal HSCs, BCRABL+ SCs from diagnosis, remission group-A and remission group-B. (XLSX 704 kb)
Supplementary Table 10 (download XLSX )
Results from GSEA comparing remission group-A BCRABL+ SCs to normal HSCs and remission BCR-ABL- SCs. (XLSX 27 kb)
Supplementary Table 11 (download XLSX )
Differentially expressed genes between single BCRABL+ SCs falling in CP-CML cluster and BCR-ABL+ SCs falling in BC-CML cluster. (XLSX 193 kb)
Source data
Source data to Fig. 1 (download XLSX )
Source data to Fig. 2 (download XLSX )
Source data to Fig. 3 (download XLSX )
Source data to Fig. 4 (download XLSX )
Source data to Fig. 5 (download XLSX )
Source data to Fig. 6 (download XLSX )
Rights and permissions
Reprints and permissions
About this article
Cite this article
Giustacchini, A., Thongjuea, S., Barkas, N. et al. Single-cell transcriptomics uncovers distinct molecular signatures of stem cells in chronic myeloid leukemia. Nat Med 23 , 692–702 (2017). https://doi.org/10.1038/nm.4336
Download citation
Received : 14 January 2017
Accepted : 10 April 2017
Published : 15 May 2017
Issue date : June 2017
DOI : https://doi.org/10.1038/nm.4336
Share this article
Anyone you share the following link with will be able to read this content:
Get shareable link
Sorry, a shareable link is not currently available for this article.
Copy shareable link to clipboard
Provided by the Springer Nature SharedIt content-sharing initiative
You have full access to this article via California Institute of Technology .
Associated content
Collection
Stem cells from development to the clinic
Understanding cancer from the stem cells up
Christopher A Eide
Brian J Druker
Nature Medicine News & Views 06 Jun 2017
Advertisement
Explore content
Research articles
Reviews & Analysis
News & Comment
Podcasts
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
About the Editors
Research Cross-Journal Editorial Team
Reviews Cross-Journal Editorial Team
Statistical Advisory Panel
Our publishing models
Editorial Values Statement
Editorial Policies
Content Types
Web Feeds
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
Nature Medicine ( Nat Med )
ISSN 1546-170X (online)
ISSN 1078-8956 (print)
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
