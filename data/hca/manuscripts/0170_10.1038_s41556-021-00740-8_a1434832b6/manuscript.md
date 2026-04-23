Human melanocyte development and melanoma dedifferentiation at single-cell resolution | Nature Cell Biology
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
nature cell biology
resources
Human melanocyte development and melanoma dedifferentiation at single-cell resolution
Resource
Published: 02 September 2021
Human melanocyte development and melanoma dedifferentiation at single-cell resolution
Rachel L. Belote ORCID: orcid.org/0000-0002-3001-0002 1 na1 ,
Daniel Le 2 na1 nAff10 ,
Ashley Maynard ORCID: orcid.org/0000-0002-3588-3080 2 nAff11 ,
Ursula E. Lang 3 , 4 ,
Adriane Sinclair 5 ,
Brian K. Lohman 6 ,
Vicente Planells-Palop ORCID: orcid.org/0000-0003-0940-1671 7 ,
Laurence Baskin 5 ,
Aaron D. Tward ORCID: orcid.org/0000-0003-4868-8732 7 ,
Spyros Darmanis ORCID: orcid.org/0000-0003-4002-8158 2 , 10 &
…
Robert L. Judson-Torres ORCID: orcid.org/0000-0002-6559-0553 1 , 8 , 9
Nature Cell Biology volume 23 , pages 1035–1047 ( 2021 ) Cite this article
21k Accesses
139 Citations
61 Altmetric
Subjects
Differentiation
Melanoma
RNA sequencing
Tumour heterogeneity
Abstract
In humans, epidermal melanocytes are responsible for skin pigmentation, defence against ultraviolet radiation and the deadliest common skin cancer, melanoma. Although there is substantial overlap in melanocyte development pathways between different model organisms, species-dependent differences are frequent and the conservation of these processes in human skin remains unresolved. Here, we used a single-cell enrichment and RNA-sequencing pipeline to study human epidermal melanocytes directly from the skin, capturing transcriptomes across different anatomical sites, developmental age, sexes and multiple skin tones. We uncovered subpopulations of melanocytes that exhibit anatomical site-specific enrichment that occurs during gestation and persists through adulthood. The transcriptional signature of the volar-enriched subpopulation is retained in acral melanomas. Furthermore, we identified human melanocyte differentiation transcriptional programs that are distinct from gene signatures generated from model systems. Finally, we used these programs to define patterns of dedifferentiation that are predictive of melanoma prognosis and response to immune checkpoint inhibitor therapy.
You have full access to this article via California Institute of Technology .
Similar content being viewed by others
The journey from melanocytes to melanoma
Article 24 April 2023
Sexual dimorphism in melanocyte stem cell behavior reveals combinational therapeutic strategies for cutaneous repigmentation
Article Open access 27 January 2024
Signal pathways of melanoma and targeted therapy
Article Open access 20 December 2021
Main
Epidermal melanocytes, the pigment-producing cells of human skin, are responsible for skin tone and orchestrate the primary defence against ultraviolet radiation. Some anatomical site-specific differences in pigmentation are due to environmental factors, such as the tanning response to ultraviolet exposure. Others, such as the hypopigmentation at volar sites (for example, palms and soles), are present at birth. In adult skin, mesenchymal–melanocyte interactions are known to influence anatomical site-specific melanocyte survival and pigment production 1 , but melanocyte intrinsic factors that contribute to site-specific specialization remain unclear.
Model organisms are powerful tools for investigating melanocyte development. In chick and mouse, a transient, multipotent neural crest cell population gives rise to committed immature melanocyte precursors called melanoblasts through two spatially and temporally distinct pathways 2 , 3 . Such studies focus primarily on melanocytes in skin appendages (hair follicles, feathers and sweat glands). However, despite constituting the predominate subtype in human skin, resident epidermal melanocytes have not been the subject of analogous investigations into developmental trajectories and anatomical specializations.
Melanocytes can give rise to melanomas that present distinct phenotypic and genomic characteristics correlated with primary tumour location 4 , 5 . Like many cancers, melanoma progression is coupled to the dedifferentiation of the cell of origin 6 . The aggressive nature of melanoma is proposed to be rooted in unique attributes of the melanocytic lineage 7 . Decoding the transcriptome of epidermal melanocytes across the human body during development and in aged skin would provide insights into the precise origins of melanoma and the developmental programs that are reacquired during progression.
Single-cell RNA sequencing (scRNA-seq) characterizes cell heterogeneity at an unprecedented resolution. Pioneering studies of human skin with scRNA-seq focused on predominant cell types (keratinocytes, fibroblasts) from few and/or uniform samples and lacked substantial representation of rare cell types, including melanocytes 8 , 9 . As a consequence, the melanocytes captured were not characterized beyond inter-cell-type comparisons 10 , 11 . Moreover, single-cell sequencing efforts for human fetal tissue have not included the melanocytic lineage 12 , 13 , 14 , 15 . We therefore sought to develop a cell atlas of human epidermal melanocytes during development and aging that captured diversity within and across anatomical locations, sex and multiple skin tones.
Results
Multisite scRNA-seq analysis of normal human melanocytes
We performed scRNA-seq on 37 healthy skin samples across multiple anatomical locations (leg, arm, foreskin, palm and sole) from 22 donors aged from 9.5 fetal weeks (f.w.) to 81 years (Fig. 1a and Supplementary Table 1 ), representing multiple skin tones and sexes. Each epidermis was enzymatically removed from the dermis and dissociated into a single-cell suspension. As melanocytes comprise a small fraction of the total epidermal cell mass, fluorescence-activated cell sorting (FACS) analysis was used to increase the capture rate of KIT + melanocytes within the basal layer 16 , 17 , 18 (Fig. 1a , Extended Data Fig. 1a,b and Methods ). Sorted cells were processed using the Smartseq2 scRNA-seq protocol 19 . After quality control (Extended Data Fig. 1c–e and Methods ) and iterative Louvain clustering ( Methods ), differential expression was used to annotate 9,719 cells into the following cell-types: melanocytes, keratinocytes, eccrine sweat gland cells and three immune cell populations (Fig. 1b,c and Extended Data Fig. 1f–i ). Gene expression within the melanocyte cluster presented agreement with differentially expressed genes (DEGs) from melanocyte clusters identified in previous fresh from human skin sequencing studies 10 , 11 (Extended Data Fig. 1j ). Individual cells were designated as cycling or non-cycling on the basis of the expression of established marker genes 20 (Extended Data Fig. 2 ). To investigate heterogeneity within melanocytes, we performed Louvain clustering on melanocytes alone ( Methods ). Low-resolution Louvain clustering yielded three major clusters (clusters A–C) that aligned with the three developmental ages collected in this study (cluster A, 97.5% adult; cluster B, 99.5% fetal; cluster C, 93.2% neonatal; Fig. 1d and Extended Data Fig. 1g–i ). We next performed high-resolution Louvain clustering. The resulting 11 high-resolution clusters (0–10; Fig. 1e ) did not correspond individually to skin tone, sex or donor (Fig. 1f–h ). Differential gene expression analysis of the high-resolution clusters indicated high similarity between clusters within each developmental age group, with the notable exception of fetal cluster 10 (Fig. 1i ). Consistent with this observation, unsupervised hierarchical clustering using principal components binned the high-resolution clusters into four groups: m1, one fetal cluster (10); m2, the remaining fetal clusters (2, 3, 6); m3, encompassing all adult clusters (0, 1, 4, 5, 7); and m4, both neonatal clusters (8, 9) (Fig. 1j ). Two of the top-five ranked genes for the m1 group had known associations with stem cell and progenitor cell function ( TC4F (ref. 21 ) and CXCL14 (ref. 22 )) (Fig. 1i ). We therefore assessed established melanocyte stem cell (MSC) signatures 23 , 24 , 25 and found high expression in the m1 group (Fig. 1k ), indicating that the melanocytes captured from our cohort encompass four developmental groups: adult, neonatal, fetal and MSC (Fig. 1l ). Furthermore, evaluation of anatomical location presented volar versus non-volar sites as another possible source of heterogeneity within the adult and fetal groups (Fig. 1m ).
Fig. 1: Melanocyte transcriptomic profiles differ based on development and anatomical location.
The alternative text for this image may have been generated using AI.
Full size image
a , The single-cell isolation, enrichment and sequencing pipeline using fresh healthy human skin samples. b , Uniform manifold approximation and projection (UMAP) visualization of the 9,719 cells (7,088 melanocytes (Mel.), 1,865 keratinocytes (Ker.), 636 eccrine cells, 76 dendritic cells, 25 mast cells and 29 T cells) that passed quality control, coloured according to cell type as identified from Louvain clustering and candidate genes (Extended Data Fig. 1 ). c , The relative expression of the top DEGs for 100 randomly selected cells from each cell-type cluster in b . d – h , UMAPs of all non-cycling melanocytes with Louvain clustering and demographic information overlays. d , Three low-resolution Louvain clusters correspond to developmental age: adult (cluster A), fetal (cluster B) and neonatal (cluster C). e – h , The 11 high-resolution Louvain clusters (0–10) do not correspond to sex ( f ), skin tone (light (L), light medium (LM), medium (M) and unknown (NA)) ( g ) or donor ( h ). i , The mean expression and fraction of cells expressing the top-five ranked genes (two-sided Wilcoxon rank-sum test) for each high-resolution Louvain cluster in e . j , Hierarchical clustering dendrogram. Using the average expression of the top-15 melanocyte-specific principal components, high-resolution Louvain clusters were binned into the following four groups: m1 (fetal cluster 10), m2 (fetal clusters 3, 2 and 6), m3 (adult clusters 4, 1, 0, 7 and 5), and m4 (neonatal (neo) clusters 9 and 8). k , Group m1, from fetal hair-baring non-volar cutaneous skin, expresses known MSC markers. l , m , UMAP analysis of all non-cycling melanocytes with developmental age and fetal MSC annotation based on hierarchical clustering of high-resolution Louvain clusters in j ( l ) and an anatomical location overlay ( m ).
Source data
Site-specific pigment-associated transcriptional programs
Hypopigmentation of palms and soles is present in neonates and continues through adulthood, indicating that site-specific pigmentation occurs during development, but the genes that regulate the variation in intraindividual pigmentation are poorly understood 1 . As anatomical location was a possible source of melanocyte heterogeneity (Fig. 1m ), we sought to identify the genes that are associated with differential pigmentation. As part of our single-cell isolation pipeline, FACS backscatter (BSC) measurements were indexed for individual cells (Fig. 1a ). BSC values are an established correlate of relative pigmentation and pigment organelle (melanosome) content 26 (Extended Data Fig. 3 ). Using BSC, we queried the relative pigmentation between donor-matched volar and non-volar melanocytes (Fig. 2a and Supplementary Table 1 (asterisks)). At 10 f.w. and 12 f.w., there were no detectable differences in BSC (Fig. 2b,c ). By contrast, we observed a striking increase in BSC within the non-volar cutaneous-derived melanocytes at 18 f.w. and adulthood (Fig. 2b,c ). Moreover, fetal skin presented an increase in Fontana–Masson staining at 18.5 f.w. in non-volar cutaneous skin with no evidence of staining in donor-matched volar skin (Fig. 2d ). These observations are consistent with previous reports 27 , 28 and indicate that the site-specific bifurcation of melanocyte pigmentation occurs between 12 f.w. and 18 f.w.
Fig. 2: Characterization of divergent pigment developmental trajectories in volar and non-volar melanocytes.
The alternative text for this image may have been generated using AI.
Full size image
a , Schematic of the cohort of donor-matched non-volar and volar skin. n = 6 donors and n = 20 total skin samples (Supplementary Table 1). b , c , Raw ( b ) and average normalized ( c ) BSC values of volar and non-volar cutaneous melanocytes before 18 f.w. (pre-bifurcation) and at/after 18 f.w. (post-bifurcation). Statistical analysis was performed using two-sided Wilcoxon rank-sum tests; Bonferroni multiple-testing-adjusted P values: ns, P = 0.25; * P = 3.6 × 10 −165 . For c , the box plots show the interquartile range (box limits) with median (centre line), s.d. (whiskers) and outliers (grey circles). d , Fontana–Masson staining for melanin/melanosomes in fetal and adult non-volar and volar skin. Representative images from n = 3 for each age. Scale bars, 50 µm. e , Increased pigment content coincides with the upregulation of the pigment transcriptional program in cutaneous melanocytes at 18 f.w. Normalized mean expression of 170 pigment-associated genes (thin lines) in volar (blue) and non-volar cutaneous (red) melanocytes. The thick lines show the average expression of all pigment associated genes. f , The mean expression of the 14 pigment genes with significant differential expression between non-volar and volar melanocytes from both adult donors; colour and size corresponds to the fold change between sites. g , The fold change in the expression of the DEGs in f for each donor-matched age. Lineage genes, melanocyte lineage-specific genes. Bifurcation-associated, genes with significant differential expression coinciding with pigment bifurcation (between 12 f.w. and 18 f.w.). Post-bifurcation, genes with significant differential expression only in donor-matched adults. Statistical analysis was performed using unpaired two-tailed t -tests; * P = 0.0278; ** P = 0.0013; *** P = 3.3 × 10 −5 . The box plot shows the full range of data values (minimum to maximum values; box limits) and the mean (Supplementary Table 2 ). h , Schematic of the identification of pigment genes associated with intraindividual pigmentation divergence between non-volar cutaneous and volar melanocytes.
Source data
To identify genes that are correlated with intraindividual pigmentation, we analysed age-dependent expression of known pigment genes 29 between donor-matched volar and non-volar cutaneous melanocytes (Supplementary Table 2 ). Although we observed an overall increase in the relative expression of pigment-associated genes in non-volar cutaneous melanocytes compared with in volar melanocytes after 12 f.w. (Fig. 2e (bold red line)), the expression patterns of individual pigment-associated genes were varied (Fig. 2e (thin red lines)). We therefore grouped pigment-associated genes on the basis of three expression patterns ( Methods )—lineage genes, melanocytic-lineage-specific genes that are highly expressed in volar and non-volar cutaneous melanocytes; bifurcation genes, genes that are upregulated in non-volar cutaneous melanocytes in concordance with pigment bifurcation at 12–18 f.w.; and post-bifurcation genes, genes that are upregulated in adult non-volar cutaneous melanocytes (Fig. 2f,g ). Lineage genes included melanocyte differentiation genes and master regulators of melanin production ( SOX10 , PAX3 , MITF , DCT , TYRP1 , TYR and PMEL ), whereas bifurcation genes and post-bifurcation genes were involved in melanosome biogenesis and function ( SLC45A2 , TPCN2 , OCA2 , RAB27A , AP3D1 , ADAM10 , TRAPPC6A , SLC24A5 and ATOX1 ) and/or pigment signalling pathways/ultraviolet response ( MC1R , GNAS and DSTYK ; Fig. 2h and Supplementary Table 2 ). Further supporting these findings, allelic variation and/or differential expression of several bifurcation and post-bifurcation genes, such as MFSD12 , are known to regulate skin pigmentation variation between individuals 30 , 31 , 32 , 33 . Here our approach pinpointed pigment genes with differential expression correlated with intraindividual pigment variation (Fig. 2h ).
Anatomical-site-enriched melanocyte subpopulations
The anatomical location of skin influences melanocyte survival and function, but it remains unclear how site-specific specialization arises during melanocyte maturation 1 . To broaden our understanding of melanocyte intrinsic differences during development between anatomical sites, we queried donor matched volar and non-volar cutaneous samples from individuals aged 10 f.w. to 77 years and different sexes and skin tones for transcriptional programs that distinguished volar versus non-volar cutaneous melanocytes across developmental ages ( n = 6 donors, n = 20 skin specimens; Fig. 2a and Supplementary Table 1 (asterisks)). Differential gene expression analysis (Mann–Whitney U -test, Benjamini–Hochberg false-discovery rate (FDR) < 5%) revealed 2,042 transcripts with site-specific expression in both fetal and adult donors (Fig. 3a and Supplementary Table 3 ). Volar melanocytes presented an increased expression of NTRK2 , ID2 and ID3 —genes previously associated with a subset of melanomas and/or silenced in non-volar cutaneous melanocytes 34 , 35 . As expected from our above analyses, non-volar melanocytes expressed genes involved in pigmentation. Using binary expression of the top-ten volar and non-volar cutaneous genes (Fig. 3b and Methods ), we classified individual cells from the full cohort ( n = 22 donors, n = 37 skin specimens) as volar-like (v-mel) and non-volar cutaneous-like (c-mel). While v-mel and c-mel cells were present in all anatomical locations for both adult and fetal skin (Fig. 3c ), v-mel cells were enriched in volar skin (mean ± s.d., 94 ± 5% volar sites, ~7 ± 5 % non-volar sites) and c-mel cells were enriched in non-volar cutaneous skin (mean ± s.d., ~89 ± 9% non-volar sites, 5 ± 5% volar sites). The presence of melanocytes with a c-mel signature in volar sites and melanocytes with the v-mel signature in cutaneous sites indicated that (1) two distinct subpopulations of epidermal melanocytes exist in human skin with anatomical site-specific enrichment, and (2) enrichment occurs during and persists after skin development. This discovery was validated using RNA fluorescence in situ hybridization and immunofluorescence analysis using the v-mel and c-mel signature genes that presented a striking level of inverse expression between volar and non-volar cutaneous melanocytes across all donor-matched skin— NTRK2 and HPGD , respectively (Fig. 3d–i and Extended Data Fig. 4 ). These observations further suggest the previously reported site-specific mesenchymal–melanocyte interactions 1 , 36 that drive the epidermal phenotype in fully developed skin provide more permissive, but non-exclusive, conditions for one melanocyte subpopulation over another.
Fig. 3: Anatomical site-specific melanocyte subpopulation enrichment arises during development and persists in adulthood.
The alternative text for this image may have been generated using AI.
Full size image
a , Volcano plot of genes enriched (two-sided Wilcoxon rank-sum test with Benjamin–Hochberg adjustment for multiple testing) in donor-matched non-volar cutaneous versus volar melanocytes (Supplementary Table 3 ). b , Top site-specific DEGs. c , The fraction of melanocytes with the v-mel or c-mel signature in each skin sample ( n = 37) from all 22 donors. The box plots show the interquartile range (box limits) and median (centre line). Statistical analysis was performed using two-sided Mann–Whitney U -tests with Bonferroni multiple-testing correction; * P = 0.12, ** P = 0.0061 (palm), ** P = 0.0058 (sole), *** P = 0.00021, **** P = 8.2 × 10 −6 . d , Expression level of the v-mel gene NTRK2 and the c-mel gene HPGD in all volar melanocytes ( n = 1,634 cells) compared to all non-volar cutaneous melanocytes ( n = 5,192 cells). Statistical analysis was performed using two-sided Mann–Whitney U- tests; *** P = 1.9 × 10 −100 , **** P = 0. The box plots show the interquartile range (box limits), median (centre line), s.d. (whiskers) and outliers (grey circles). e , Representative pseudocoloured fluorescence microscopy images of NTRK2 , HPGD and the melanocyte marker DCT (outlined in yellow) mRNA staining in adult volar and non-volar epidermis. The dashed line shows the epidermal–dermal junction. Scale bars, 20 μm (left), 10 μm (right), 5 μm (insets). f , Quantification of NTRK2 and HPGD foci in DCT + melanocytes in volar ( n = 44 cells) and non-volar cutaneous skin ( n = 22) in e . Statistical analysis was performed using two-tailed unpaired t -tests; *** P = 5.5 × 10 −6 , **** P = 4.1 × 10 −7 . The box plots show the interquartile range (box limits), median (centre line); 10% to 90% (whiskers) and outliers (grey circles). g , The percentage v-mel ( NTRK2 > HPGD ) and c-mel ( HPGD > NTRK2 ) at each site in e and f . Statistical analysis was performed using two-tailed, two-sample Z- tests for proportions; ‡ z = 6.062, P = 1.8 × 10 –11 (v-mel), and z = 7.885, P = 1.6 × 10 −15 (c-mel). h , Immunofluorescence co - staining of adult volar and non-volar skin cryo-sections with the c-mel marker HPGD (green) and melanocyte marker KIT (magenta). Arrows indicate melanocytes. The dashed line indicates the epidermal–dermal junction. Scale bars, 50 μm. i , The percentage of HPGD + melanocytes per donor volar and non-volar skin. Adult skin: A1046, n = 78 cells; A1038, n = 39 cells; A1018, n = 48 cells; A1026, n = 15 cells. Fetal skin: 9WK07, n = 41 cells; 16WK04, n = 10 cells. Statistical analysis was performed using two-tailed unpaired t -tests; ** P = 0.001. j , Illustration of the hypothesis that healthy melanocyte anatomical site-specific transcriptional programs are conserved in melanoma. k , The ratio of the average expression of the top v-mel and c-mel genes in primary melanomas. n = 15 (acral), n = 103 (non-acral cutaneous). Statistical analysis was performed using unpaired two-tailed t -tests; **** P = 1.5 × 10 −6 . The box plots show the interquartile range (box limits), median (centre line), 10% to 90% (whiskers) and outliers (grey circles).
Source data
Approximately 4% of primary cutaneous melanomas (CMs), called acral melanomas (AMs), arise from volar regions 37 . The disease-specific death rate from AM is more than twice as high as that of CM in general 38 . While AMs are, on average, diagnosed at more advanced stages and at a deeper Breslow depth, partially explaining the increased morbidity, when adjusted for Breslow depth and stage, AMs still have worse outcomes 38 , 39 , suggestive of a biologic aetiology for this discrepancy. To determine whether AM may arise from v-mel cells (Fig. 3j ), we accessed publicly available datasets to compare the expression of v-mel to c-mel signatures in 103 primary non-acral CMs and 15 primary AMs. The v-mel signature was significantly elevated in the AM cohort (Fig. 3k ; unpaired two-tailed t -test, P < 0.0001), suggesting that AMs retain v-mel transcriptional programs and are therefore possibly derived from v-mel cells.
Human-specific melanocyte differentiation programs
We next assessed the transcriptional programs that changed with non-volar cutaneous melanocyte development. Diffusion pseudotime analysis, pairwise differential gene expression and gene set enrichment analysis for Gene Ontology Biological Process (GO-bp) terms 40 , 41 identified neonatal melanocytes (NEO) as an intermediate transcriptional state between fetal (FET) and adult (ADT) (Fig. 4a , Extended Data Figs. 5 and 6 , and Supplementary Table 4 ). A comparison with previously published transcriptomes of neonatal and adult human melanocytes 10 (Supplementary Table 4 ) demonstrated significant enrichment with the NEO (normalized enrichment score (NES) = −1.81 for Cheng et al. 10 neonatal foreskin, FDR-adjusted q = 0.00) and ADT (NES = 3.15 for Cheng et al. 10 adult non-volar, FDR-adjusted q = 0.00) programs, respectively, further supporting this distinction. MSCs were enriched for terms associated with extracellular matrix assembly and morphogenesis, development and differentiation—the latter of which remained significant but trended downwards in FET and NEO (Fig. 4a and Extended Data Fig. 6 ). By contrast, genes associated with immunity, inflammation, organelle maturation and pigmentation presented increasingly significant enrichment with each consecutive developmental group. Together, these data suggest that the four main developmental groups represent distinct developmental stages along a differentiation trajectory. Our analyses did not reveal further substantial transcriptional changes associated with donor age in adult melanocytes (Extended Data Fig. 5c ).
Fig. 4: Defining transcriptomic programs specific to human melanocyte development.
The alternative text for this image may have been generated using AI.
Full size image
a , The median NESs of GO-bp terms enriched at each developmental stage (Extended Data Fig. 6 ). n.e., not enriched. b , Schematic of the DevMel logistical regression model (DevMel LOGIT) used to generate and validate unique transcription profiles for each developmental stage of normal human melanocytes. c , The relative expression (column z score) of genes in each DevMel program from b (the gene list is provided in Supplementary Table 4 ). d – g , DevMel program expression is highly expressed by cells from all skin donors within each corresponding developmental stage (prg[MSC] ( d ), prg[FET] ( e ), prg[NEO] ( f ) and prg[ADT] ( g )). Program expression for each donor (black line, average) is the ratio of the mean expression of positively correlated genes to negatively correlated genes. Statistical significance was determined using one-sided Mann–Whitney U- tests. n = 3 (MSC), n = 5 (FET), n = 2 (NEO) and n = 14 (ADT) donors. For d – g , prg[MSC]: MSC versus the rest, *** P = 0.0005 ( d ); prg[FET]: FET versus the rest, **** P = 0.0001 ( e ); prg[NEO]: FET versus the rest, ** P = 0.0072 ( f ); prg[ADT]: ADT versus the rest, **** P = 5.1 × 10 −7 ( g ).
Source data
To identify gene signatures that best distinguished each human melanocyte developmental group from each other, a regularized logistic regression model was trained using the single-cell transcriptomes from 66% of the dataset representing the four developmental stages (Fig. 4b ). The resultant developmental stage melanocyte (DevMel) model demonstrated excellent classification accuracy when tested on the holdout set, with F 1 scores ranging from 0.93–1.00 (Supplementary Table 5 ). Elastic net regularization yielded genes that collectively constituted developmental stage-specific expression programs (prg): prg[MSC], prg[FET], prg[NEO] and prg[ADT] (Fig. 4c–g and Supplementary Table 5 ). Each program is a relatively small (45–69 genes) expression program unique to the associated developmental group. Small gene sets are not amenable to reliable GO analyses, so we used an augmented artificial intelligence approach to identify biological processes that are associated with each program ( Methods ). prg[MSC] was again associated with extracellular matrix assembly, as well as neural crest cell fate specification, IGF signalling and a stem-cell-associated WNT–TCF–LEF–beta-catenin program; prg[FET] with MAPK, PI3K and NF-κB signalling and chromatin remodelling; and prg[ADT] with inflammation, skin epidermis, and cell polarity (Extended Data Fig. 7 ). prg[NEO], in particular, was least associated with unique known biological processes, potentially reflective of its intermediated status between FET and ADT.
While there is substantial overlap in melanocyte developmental pathways between different model organisms, there are known species-dependent differences, and conservation of these processes in human skin remains unresolved 2 , 3 , 42 . To benchmark human melanocyte development against known mammalian developmental systems, we assessed the expression the gene signatures previously defined during mouse melanocyte development 25 , 43 , 44 , 45 (Fig. 5a ) and in vitro differentiation of human embryonic stem (ES) cells into mature melanocytes 46 within ADT, NEO, FET and MSC non-volar cutaneous skin. Both the Sennet et al. 45 embryonic day 14.5 (E14.5) mouse melanoblast signature and the Rezza et al. 44 P4 and P5 mouse melanocyte signature were more highly expressed in the FET, NEO and ADT melanocytes compared with in MSCs ( P < 1 × 10 –12 ; Fig. 5b,d ). In these studies, melanocytic cells were isolated using LEF1 and KIT expression, and the gene signatures were derived from the comparison of melanocytic cells with other skin cells. In mice, LEF1 is a marker of differentiated (and differentiating) melanocytes and is not expressed in MSCs 47 , 48 . Thus, the resulting gene signatures represent a general melanocytic cell-type-specific program, exclusive of MSCs, at each mouse developmental time point. The observed low program expression in the human MSC group defined here is therefore consistent with the experimental design of the Sennet 45 and Rezza 44 studies (Fig. 5b,d ). By contrast, the Marie et al. 43 melanoblast signature was most highly expressed in MSCs (>1.5-fold change compared with each other group, P < 1 × 10 –7 ; Fig. 5c ). In contrast to the Sennet et al. 45 melanoblast signature, the Marie et al. 43 melanoblast signature was derived from the comparison of DCT + melanoblasts at E15.5 and E17.5 to postnatal day 1 (P1) and P7 melanocytes, and is therefore a melanoblast-specific signature. DCT is expressed in differentiated (and differentiating) melanocytes as well as MSCs. Consistent with this finding, the CD34 + mouse hair follicle MSC gene set 25 was most highly expressed in MSCs ( P = 5.4 × 10 –38 ; Fig. 5e ).
Fig. 5: Evaluation of the expression of melanocyte developmental programs from mammalian models in human non-volar cutaneous melanocyte developmental groups.
The alternative text for this image may have been generated using AI.
Full size image
a , Schematic of human 50 , 51 and corresponding mouse 49 melanocyte development. In hair-bearing skin, both humans and mice develop follicular melanocytes (purple). Mice retain a dermal melanocyte population (blue) in fully developed skin, whereas humans develop resident epidermal melanocytes (red) within the skin at all anatomical locations. The pink bar indicates human fetal ages captured in our dataset. b – f , The distribution of the indicated transcriptional program expression scores for individual cells within each developmental group. n = 3,281 (ADT), n = 735 (NEO), n = 1,176 (FET) and n = 63 (MSC). The dashed line shows the mean expression. Program scores were generated from published signatures of mouse melanoblasts (cells committed to the melanocyte fate) ( b and c ) from ref. 45 ( b ) and ref. 43 ( c ) (**** P = 1.5 × 10 −14 ( b ); ** P = 1.0 × 10 −8 , *** P = 2.3 × 10 −19 , **** P = 5.9 × 10 −28 ( c )); mouse melanocytes from ref. 44 ( d ; **** P = 2.8 × 10 −13 ); MSCs from mature hair follicles in adult mice from ref. 25 ( e ; **** P = 4.5 × 10 −38 ); and in vitro stages of differentiation of human pluripotent stem cells to melanocytes from ref. 46 ( f ; **** P = 2.8 × 10 −25 ). Statistical significance was determined using one-sided Man–Whitney U -tests; **** P < 1 × 10 −7 . The variance (reported below the corresponding group for each violin plot) of the average program expression among donors within the MSC, FET, NEO and ADT groups was low showing concordance across ages within each group. g , h , The number of unique and overlapping genes of melanoblast-related gene signatures with the positive correlated component of the DevMel profiles prg[MSC] ( g ) and prg[FET] ( h ). MB, melanoblast. i , j , The number of unique and overlapping genes of differentiated melanocyte related gene signatures with the positively correlated component of the DevMel profiles prg[NEO] ( i ) and prg[ADT] ( j ).
Source data
Mouse hair follicle morphogenesis occurs around E14 and is completed postnatally by P8 as a fully mature hair-bearing follicle in anagen phase 49 . In humans, hair follicle formation is reported to start around 10 f.w., with mature hair follicles appearing around 20 f.w. depending on the anatomical location and study 50 , 51 . The fetal skin specimens in our dataset coincide with the onset and later stages of human hair follicle development, which would encompass morphological stages that resemble mouse hair follicle development at E15.5 and E17.5 from Marie et al. 43 (Fig. 5a ). In contrast to mice, human hair-bearing skin contains both hair follicle-associated and epidermal-associated melanocytes. It is therefore reasonable that the mouse melanoblast-specific program from Marie et al. 43 is most highly expressed in a subset of the human fetal melanocytes that express known follicular-associated gene signatures (Figs. 1k and 5c,e ). Together, these data suggest that our human MSCs are melanoblasts that give rise to follicular and perhaps also epidermal melanocytes.
Of the in vitro differentiation programs, the mature differentiated melanocyte program was expressed across all developmental groups with the highest expression in FET, NEO and ADT groups compared with MSCs ( P < 1× 10 –14 ; Fig. 5f ). These observations suggest that the in vitro generation of melanocytes from pluripotent stem cells does not distinguish between differentiating, young and aged melanocytes. Differentiation protocols that better distinguish the in vivo profiles reported here, especially accounting for the effect of the aged adult developmental state, would be a valuable tool for the field.
Comparison of DevMel program genes with those identified in mouse or in human in vitro differentiation yielded sparse overlap (Fig. 5g–j ), indicating that our approach revealed previously unidentified programs that are specific to human fetal, neonatal and adult skin. We therefore sought to determine whether profiles that are unique to human in vivo development could provide insights into melanoma dedifferentiation and aggression.
Reacquisition of developmental programs during tumorigenesis
Melanoma progression often coincides with the loss of melanocyte differentiation markers and upregulation of genes associated with earlier stages of development 43 , 52 , 53 , 54 , 55 . This process is broadly described as dedifferentiation. Given the substantial cell-to-cell intratumour heterogeneity of melanoma 56 , we reasoned that single cells within a tumour might occupy various stages of dedifferentiation and that the proportion of cells in each state potentially influences overall patient outcome. To assess tumour heterogeneity, we classified published single-cell malignant melanoma samples 57 , 58 using our DevMel model. Each melanoma cell was classified according to the similarity of its transcriptome to the human development-associated programs, resulting in four groups of melanoma cells—MAL MSC , MAL FET , MAL NEO and MAL ADT (Fig. 6a ). We observed intertumour and intratumour heterogeneity in the representation of each melanoma group (Fig. 6b ), indicating that tumours are composed of a mix of dedifferentiated states.
Fig. 6: Identification of distinct patterns of developmental programs reacquired in metastasized melanomas.
The alternative text for this image may have been generated using AI.
Full size image
a , DevMel LOGIT was used to classify individual melanoma cells by normal melanocyte developmental stages. Every melanoma cell was categorized by the predominantly expressed developmental stage program. b , Individual tumours are a heterogeneous mix of malignant cells in different dedifferentiation states. The fraction of MAL ADT , MAL NEO , MAL FET and MAL MSC cells in each of the 14 tumours analysed from Tirosh et al. 58 and Jerby-Arnon et al. 57 in a . c , Top: workflow to generate the gene set (511 unique genes) used to identify patterns associated with melanoma dedifferentiation. Bottom: the percentage of genes across MAL groups that exhibit patterns consistent with dedifferentiation categories in d , e and g . d – g , Dedifferentiation can occur through several categories of cancer-associated transcriptional reprogramming: sequential dedifferentiation, a reverse stepwise unfolding of development ( d ); direct dedifferentiation, direct reacquisition of programs from early developmental stages ( e ); melanoma specific, acquisition of programs not associated with the stages of melanocyte development identified here ( f ). Normal adult developmental stage programs that are lost and earlier developmental stage programs that are not readopted in metastatic melanoma ( g ). Examples of each category are visualized as heatmaps of the relative expression (row z score). The complete gene lists are provided in Supplementary Table 6 .
Source data
Previous reports have used bulk-tumour transcriptional signatures to classify cohorts of melanomas—most notably, The Cancer Genome Atlas (TCGA) cohort 59 can be classified as immune, keratin or MITF-low; and the Cirenajwis et al. cohort 60 as immune, normal-like, pigmented or proliferative. Others have classified tumours on the basis of the profiling of in vitro differentiation of human stem cells into melanocytes, resulting in signatures for undifferentiated, neural crest like, transition and melanocytic 53 . Additionally, there are two well-established transcriptional signatures centred in the average expression level of a MITF-regulated transcriptional program (inclusive of MITF itself) defined as ‘MITF-high/proliferative’ and ‘AXL-high/invasive’ 58 , 61 . We determined how our signatures derived from human melanocyte development corresponded with published melanoma states and signatures. Similar to our analysis of model system developmental programs, the MAL MSC melanoma cells corresponded to previously identified stem cell-like transcriptional states (Extended Data Fig. 8a–e (MITF-low, slow cycling, invasive)). We also observed significant enrichment between the MAL ADT group and the Cirenajwis et al. 60 normal-like signature, consistent with these cells retaining a substantial component of the differentiated melanocyte program. Surprisingly, neither the MAL FET nor the MAL NEO group exclusively segregated with previously defined signatures. For example, the MAL FET group was significantly enriched for both the TCGA immune and MITF-low signatures, whereas the MAL NEO group was not enriched for any previously defined signatures. These observations suggest that categorization of malignant melanoma cells by the human developmental stage categories defined here represents a different classification system, with the MAL MSC and MAL ADT groups reasonably aligned with previously reported MITF-low/stem cell and normal melanocytes, respectively, and the MAL FET and MAL NEO groups representing previously unreported signatures. Thus, we reasoned that the classification of melanoma cells by human developmental programs might offer further insights into understanding dedifferentiation in melanoma.
To better define the course of dedifferentiation during melanoma progression, we identified differential gene expression patterns across each of the four MAL groups that were consistent with different forms of cellular reprogramming: (1) a retrograde unfolding of the differentiation cascade (sequential dedifferentiation) 53 , (2) direct reprogramming to a more pluripotent stage (direct dedifferentiation) or (3) the acquisition of a melanoma-specific program (Fig. 6c–g ). Of 511 total unique genes, inclusive of the DevMel model variables and the MAL group top DEGs (Supplementary Table 6 ), 45% exhibited expression patterns consistent with sequential dedifferentiation, in which the relative expression across healthy melanocyte developmental groups was conserved among MAL groups (Fig. 6c,d ). We found that 3.1% of genes exhibited a direct dedifferentiation pattern, indicating that the expression of these genes may be a prerequisite for disease progression and metastasis (Fig. 6e ). Supporting this interpretation, this small set of genes includes known markers of aggressive melanoma such as AXL and HMGA2 (refs. 58 , 62 ). Similarly, recently identified therapeutic resistance programs 63 , 64 were evident in both the MSC healthy and MAL MSC populations (Extended Data Fig. 8d,e ). We also identified genes expressed in healthy melanocyte groups that were downregulated in all of the melanoma groups (Fig. 6f ), therefore characterizing aspects of normal melanocyte expression that are either non-essential or potentially inhibitory to melanoma progression and/or metastasis. Although we found no significant enrichment for the in vitro differentiation-based gene signatures from Tsoi et al. 53 in any of the MAL groups (Extended Data Fig. 8c ), the analyses conducted here suggest that sequential dedifferentiation, which recapitulates the ordered cascade of differentiation in reverse (Fig. 6d ), is predominant in melanoma progression. This discovery mirrors the findings of Tsoi et al. 53 , which show that the development of therapeutic resistance in melanoma traverses a sequential dedifferentiation trajectory 53 .
Finally, 52 highly expressed genes in melanoma were absent from each of the healthy melanocyte developmental groups (Fig. 6g and Supplementary Table 6 ). Among the top DEGs was the melanoma-associated antigen PRAME, further supporting its use as a melanoma molecular diagnostic. Other of these melanoma-specific genes might be important for melanoma progression, such as the MTRNR2L family of transcripts, which encode short peptides with anti-apoptotic activity 65 , and were highly and exclusively expressed in all of the melanoma groups.
Developmental stage programs correlate with patient survival
To determine whether gene expression programs that are characteristic of different human developmental ages offer prognostic value, we applied CIBERSORT 66 to estimate the fraction of melanoma cells similar to ADT, NEO, FET, MSC for all skin cutaneous melanoma (SKCM) tumour samples from the TCGA 59 . Similar to the single-cell melanoma dataset (Fig. 6b ), we observed intertumour heterogeneity in the fractional representation of the four developmental groups (Fig. 7a ). Hierarchical clustering of SKCM label distributions classified tumour samples according to the observed predominant developmental group: SKCM ADT , SKCM NEO , SKCM FET , SKCM MSC (Supplementary Table 7 ). Neither genetic driver nor tumour site correlated with the developmental group classification of the tumour (Fig. 7a and Extended Data Fig. 8f ).
Fig. 7: Reacquisition of specific developmental programs in heterogeneous melanoma is prognostic.
The alternative text for this image may have been generated using AI.
Full size image
a , Hierarchical clustering of TCGA SKCM tumours on the basis of fractional composition of normal melanocyte developmental stages assigned using CIBERSORT (top) with clinicopathological features (bottom). b , Kaplan–Meier curves for each SKCM group from a . Enrichment of cells similar to ADT is associated with increased survival, whereas enrichment of NEO is associated with worse survival. Statistical analysis was performed using the two-sided log-rank test. c , Kaplan–Meier curve showing that enrichment of the NEO fraction is associated with worse survival in a second cohort (Lund University). Statistical analysis was performed using the two-sided log-rank test. d , The fraction of MAL NEO cells from the single-cell analysed tumours ( n = 7 (untreated), n = 7 (resistant)) from Fig. 6b correlates with post-ICI resistance. Statistical analysis was performed using unpaired one-sided t -tests; ** P = 0.0099. The black bar shows the mean. e , The expression of the MAL NEO signature (top-100 DEGs; Supplementary Table 8 ) is significantly higher in tumours from patients exhibiting only a partial response (PR; n = 25) or no response (PD; n = 49) to anti-PD-1 antibody treatment compared with those who responded (CR; n = 14). Statistical analysis was performed using unpaired one-sided t -tests; * P = 0.018. The box plot shows the interquartile range (box limits), median (centre line) and the minimum and maximum values (whiskers). f , g , Schematic of the decoding of melanoma dedifferentiation using human developmental programs. f , Individual melanoma tumours comprise a heterogeneous mix of malignant cells expressing defined melanocyte developmental programs. The fraction of cells expressing each program within the tumour is predictive of overall survival and correlates with signatures of immune infiltration, evasion and potential therapeutic options. g , Each melanoma cell can occupy a different degree of dedifferentiation defined by sequential dedifferentiation transcriptional programs (Fig. 6 and Supplementary Table 6 ). The MSC- and adult-like programs are associated with previously described melanoma signatures, whereas the fetal-like and neonatal-like programs do not segregate with known melanoma signatures, offering unique insights into previously uncharacterized melanoma transcriptional states (Extended Data Fig. 8 , from refs. 58 , 59 , 60 , 61 , 63 , 64 ). Melanoma-specific genes, genes common to melanoma cells but not melanocytes, such as PRAME . Direct dedifferentiation genes, MSC or FET genes that can be expressed in melanoma cells regardless of the over-all differentiation state of the cell, such as AXL , EGR1 and HMGA2 .
Source data
Using our developmentally defined subclasses of melanoma tumours, we evaluated the correlation of bulk tumour differentiation status with patient outcome. As expected, the most differentiated group (SKCM ADT ) exhibited best median overall survival (Fig. 7b ; SKCM ADT = 11.0 year versus rest = 5.3 year). Surprisingly, the most dedifferentiated groups (SKCM FET and SKCM MSC ) were not associated with worse outcomes; rather, the intermediately differentiated group (SKCM NEO ) exhibited the shortest median overall survival (SKCM NEO = 4.2 year versus the rest = 8.2 year). To validate this observation, we developmentally classified specimens from the Lund University dataset 60 and again found that tumours comprising predominantly NEO-like cells (LUND NEO ) were associated with worse outcomes (Fig. 7c ; LUND NEO = 1.21 year versus the rest = 3.43 year). To better understand this unexpected finding, we evaluated the expression of transcriptional programs associated with clinical response to therapeutics. Indeed, SKCM NEO tumours expressed higher levels of transcripts associated with immune resistance 57 ( P = 1.6 × 10 −2 , SKCM NEO versus the rest) and a dearth in immune infiltration signatures 57 ( P = 5.5 × 10 −4 , SKCM NEO versus the rest) as well as FDA-approved therapeutic targets 67 ( P = 1.6 × 10 −5 , SKCM NEO versus the rest; Extended Data Fig. 8g ). The SKCM MSC tumour group was unique in its increased expression of FDA-approved therapeutic targets ( P = 4.6 × 10 −21 , SKCM MSC versus the rest) in agreement with previous studies of stem-like melanoma cells 53 , 57 . The MAL NEO signature presented almost no enrichment for previously published prognostic signatures, with the striking exception of genes that are poorly expressed in tumours that respond to the immune checkpoint inhibitor (ICI) nivolumab (Extended Data Fig. 8h and Supplementary Table 8 ). Consistent with this finding, the fraction of MAL NEO cells within a melanoma was a strong predictor of ICI-resistant versus treatment-naive tumours (Fig. 7d ; unpaired one-sided t -test, P = 0.0099) and, importantly, the MAL NEO signature was significantly more expressed in tumours exhibiting only a partial or no response to ICI therapy compared with a full response (Fig. 7e ; unpaired one-sided t -test P = 0.018).
Taken together, classification using human epidermal melanocyte developmental stage signatures revealed that at least four states of dedifferentiation constitute individual tumours (Fig. 7f ). The proportion of melanocytes that have readopted a neonatal-like signature is associated with worse prognosis and a higher likelihood of resistance to ICI therapy, demonstrating that, although some amount of dedifferentiation is associated with a worse prognosis, overall survival, immune evasion and immune resistance are not linearly correlated with dedifferentiation (Fig. 7g ).
Discussion
We have provided a fresh-from-skin human epidermal melanocyte dataset that encompasses human development, sex and diverse race/ethnicities and includes multiple donor-matched anatomical locations. Our findings deliver a unique perspective on human melanocyte biology through the characterization of distinct transcriptional programs that are specific to development and function. Thus, the transcriptional programs identified here are valuable for understanding the diversity and malignant transformation of human melanocytes.
We identified an additional population of epidermal melanocytes that appear early during human development. It is possible that epidermal v-mel cells are hypopigmented descendants of previously defined sweat gland stem cells 68 . It is also possible that v-mel cells derive from Schwann-cell-derived melanoblasts, which undergo a distinct lineage specification pathway 2 , 69 . Having identified genes in each subtype that are conserved through fetal development to adulthood, we have provided markers that permit the examination of these hypotheses in future studies. As the predominant class of melanocytes in volar regions, we speculated that these v-mel cells could represent a distinct cell of origin of AMs and demonstrated that the v-mel signature was significantly elevated in primary AMs compared with in other primary CMs (Fig. 3j,k ). As AM is associated with poor therapeutic response and overall survival, assessing whether the v-mel origin confers therapeutic vulnerabilities that are unique to AMs could be clinically valuable 4 , 70 .
By characterizing melanoma dedifferentiation using human-specific developmental programs, our research sheds light on the relationships among developmental stages, tumour characteristics and melanoma cell transcriptional states (Figs. 6 and 7 ). For example, with 63 years as the average age of melanoma diagnosis, our in situ adult melanocyte transcriptome provides a relevant basis for investigating disease aetiology and progression 71 . Moreover, our analyses identified the transcriptional state associated with neonatal melanocytes that is correlated with the worst overall survival and predicted response to immune checkpoint inhibitors. One limitation of our cohort is that the neonatal samples are limited to a single anatomical location (foreskin). The pseudotime analysis and the frequency of observed sequential dedifferentiation in melanoma both support the hypothesis that neonatal melanocytes represent an intermediate developmental stage, but we cannot rule out the contribution of the foreskin tissue environment on the transcriptional programs. Indeed, foreskin is established as immunologically hyperactive 72 , it is therefore possible that foreskin melanocytes evolved to express more immune-evasive programs. Regardless, our discovery of the prognostic value of this expression program could prove to be clinically valuable in the a priori prediction of therapeutic response to immune checkpoint inhibition. Owing to tissue availability and ease of culture, the neonatal melanocyte transcriptome is often considered to be the baseline ‘normal differentiated program’ for comparison with melanoma transcriptomes. This technical artefact can explain why this program has previously been underappreciated. We further identified melanoma-specific genes that are directly acquired in all stages of dedifferentiation (Figs. 6g and Fig. 7g and Supplementary Table 6 ), suggesting that these genes may undergo positive selection during early metastatic dissemination. Along with the widely accepted diagnostic melanoma biomarker PRAME 73 and an established marker of invasion AXL 58 , we identified additional melanoma-associated genes. Further investigation into the mechanistic roles of these gene sets could reveal previously uncharacterized drivers of melanoma metastasis.
Methods
Human participant details
All skin was collected from surgical discards with informed consent and approval from the UCSF Institutional Review Board. The research conducted using human tissue is compliant with all relevant ethical regulations regarding human patients. All ages, races/ethnicities and sexes were included in the eligibility criteria for this study. Participants were not compensated for their participation. Adult tissue was obtained from surgical remnants of heathy skin taken for reconstructive surgery or from amputations with heathy skin. Neonatal foreskins were obtained after routine circumcision. Anonymous fetal specimens were obtained from elective terminations and fetal age (stated as fetal weeks) was estimated by heel–toe length 74 . When possible, fetal sex was determined by visual inspection using a dissecting microscope. All samples were collected in cold CO 2 Independent Media (Gibco, Thermo Fisher Scientific) or Medium 154 (Gibco) with 1× Antibiotic-Antimycotic (Gibco) at 4 °C until dissociation. Human melanoma data were obtained from previous studies: the TCGA Research Network ( https://www.cancer.gov/tcga ); Lund University ( GSE65904 ); 60 , 75 Translational Genomics Research Institute (dbGAP: phs001036.v1.p1 ); 76 Broad Institute ( GSE72056 (ref. 58 ), GSE115978 (ref. 57 ) and https://portals.broadinstitute.org/single_cell/study/melanoma-immunotherapy-resistance ).
Skin sample preparation
Tissue dissociation was started on the same day as sample acquisition. For adult and neonatal skin, the epidermis was enzymatically dissociated from the dermis using a Dispase neutral protease grade II (Roche, Sigma-Aldrich) and incubation for 14 h at 4 °C. Epidermal sheets were manually separated from the dermis, finely minced and incubated with 0.5% trypsin (Gibco) for 3 min at 37 °C. After manual trituration, trypsin was deactivated using ice-cold soybean trypsin inhibitor (Gibco), then diluted 2:3 in ice-cold Hank’s balanced salt solution, no Mg 2+ , no Ca 2+ (Gibco). The dissociated cell suspension was centrifuged at 500 g , 4 °C, for 4 min, resuspended in FACS buffer (0.1% bovine serum albumin (Sigma-Aldrich) and 25 mM HEPES (Gibco) in Dulbecco’s phosphate-buffered saline (DPBS) (Gibco)) and strained with a 70 μM filter to achieve a single-cell suspension. For fetal tissue, the developing epidermis was manually removed from the dermis after incubation for 20–30 min with 10 mM EDTA (Invitrogen), DPBS at 37 °C. The resulting epidermal layer was incubated with 0.5% trypsin (Gibco) for 1 min at 37 °C and manually triturated. Trypsin was deactivated using ice-cold soybean trypsin inhibitor (Gibco), then diluted 2:3 in ice cold Hank’s balanced salt solution (Gibco). The dissociated cell suspension was centrifuged at 500 g , 4 °C, for 4 min, resuspended in FACS buffer, and strained using a 70 μm filter to achieve a single-cell suspension.
FACS analysis and single-cell sorting
Single-cell suspensions were counted, diluted to 1 × 10 6 cells per 100 ul with ice-cold FACS buffer containing the following dye-conjugated antibodies: anti-KIT (104D2; 15 ng per 100 µl; CD11705, Thermo Fisher Scientific), anti-ITGA6 (GoH3; 15 ng per 100 µl; 12–0495–82, Thermo Fisher Scientific) and anti-CD11c (1:20 dilution; 46-0116-41; Thermo Fisher Scientific) and incubated on ice for 25 min. Cells were washed once with 10× volume of FACS buffer, centrifuged for 2 min at 500 g , resuspended in 30 ng ml −1 DAPI (D3571, Molecular Probes), FACS buffer. Resuspended cells were strained through a 35 µm nylon mesh filter and kept on ice until sorted.
Single cells were sorted into 384-well plates using the ultra-purity setting on a SH800S (Sony) sorter. For a typical sort, a tube containing 0.3–1 ml the prestained cell suspension was vortexed gently and loaded onto the FACS machine. A small number of cells were flowed at low pressure to check cell concentration and amount of debris. The pressure was then adjusted, flow was paused, and the first destination plate was unsealed and loaded. Single cells were sorted into plates by gating to exclude dead/dying cells (DAPI + ) and doublets. The majority of the plates contained melanocytes (CD11c − KIT + ) with 4 to 5 columns of basal keratinocytes (CD11c − KIT − ITGA6 + ) and other triple-negative cells such as suprabasal keratinocytes (CD11c − KIT − ITGA6 − ). Immediately after sorting, plates were sealed with a prelabelled aluminium seal, centrifuged at 4 °C and flash frozen on dry ice, before storage at −80 °C for later use.
Lysis plate preparation
Lysis plates were created by dispensing 0.4 µl lysis buffer (0.5 U Recombinant RNase Inhibitor (Takara Bio, 2313B), 0.0625% Triton X-100 (Sigma-Aldrich, 93443-100ML), 3.125 mM dNTP mix (Thermo Fisher Scientific, R0193), 3.125 µM Oligo-dT30VN (IDT, 5′-AAGCAGTGGTATCAACGCAGAGTACT30VN-3′) and 1:600,000 ERCC RNA spike-in mix (Thermo Fisher Scientific, 4456740)) into 384-well hard-shell PCR plates (BioRad, HSP3901) using a Tempest liquid handler (Formulatrix). All of the plates were then centrifuged for 1 min at 3,220 g and snap-frozen on dry ice. Plates were stored at −80 °C until used for sorting.
cDNA synthesis and library preparation
cDNA synthesis was performed using the Smart-seq2 protocol 19 . In brief, 384-well plates containing single-cell lysates were thawed on ice followed by first-strand synthesis. Reaction mix (0.6 µl of 16.7 U µl −1 SMARTScribe Reverse Transcriptase (Takara Bio, 639538), 1.67 U µl −1 Recombinant RNase Inhibitor (Takara Bio, 2313B), 1.67× First-Strand Buffer (Takara Bio, 639538), 1.67 µM TSO (Exiqon, 5′-AAGCAGTGGTATCAACGCAGACTACATrGrG+G-3′), 8.33 mM dithiothreitol (Bioworld, 40420001-1), 1.67 M Betaine (Sigma-Aldrich, B0300-5VL) and 10 mM MgCl 2 (Sigma-Aldrich, M1028-10X1ML)) were added to each well using a Tempest liquid handler or Mosquito (TTP Labtech). Reverse transcription was performed by incubating wells on a ProFlex 2 × 384 thermal-cycler (Thermo Fisher Scientific) at 42 °C for 90 min and stopped by heating at 70 °C for 5 min. Subsequently, 1.5 µl of PCR mix (1.67X KAPA HiFi HotStart ReadyMix (Kapa Biosystems, KK2602), 0.17 µM IS PCR primer (IDT, 5′-AAGCAGTGGTATCAACGCAGAGT-3′) and 0.038 U µl −1 lambda exonuclease (NEB, M0262L)) was added to each well with a Mantis liquid handler (Formulatrix) or Mosquito, and second strand synthesis was performed on the ProFlex 2 × 384 thermal-cycler using the following program: (1) 37 °C for 30 min; (2) 95 °C for 3 min; (3) 23 cycles of 98 °C for 20 s, 67 °C for 15 s and 72 °C for 4 min; and (4) 72 °C for 5 min. The amplified product was diluted at a ratio of 1 part cDNA to 10 parts 10 mM Tris-HCl (Thermo Fisher Scientific, 15568025). Diluted product (0.6 µl) was transferred to a new 384-well plate using the Viaflow 384 channel pipette (Integra). Illumina sequencing libraries were prepared as follows 75 . In brief, tagmentation was performed on double-stranded cDNA using the Nextera XT Library Sample Preparation kit (Illumina, FC-131-1096). Each well was mixed with 0.8 µl Nextera tagmentation DNA buffer (Illumina) and 0.4 µl Tn5 enzyme (Illumina), then incubated at 55 °C for 10 min. The reaction was stopped by adding 0.4 µl Neutralize Tagment Buffer (Illumina) and centrifuging at room temperature at 3,220 g for 5 min. Indexing PCR reactions were performed by adding 0.4 µl of 5 µM i5 indexing primer, 0.4 µl of 5 µM i7 indexing primer and 1.2 µl of Nextera NPM mix (Illumina). All reagents were dispensed with the Mantis or Mosquito liquid handlers. PCR amplification was performed on a ProFlex 2 × 384 thermal cycler using the following program: (1) 72 °C for 3 min; (2) 95 °C for 30 s; (3) 12 cycles of 95 °C for 10 s, 55 °C for 30 s and 72 °C for 1 min; and (4) 72 °C for 5 min. For library pooling, quality control and sequencing, after library preparation, wells of each library plate were pooled using a Mosquito liquid handler. Pooling was followed by two purifications using 0.7× AMPure beads (Thermo Fisher Scientific, A63881). Library quality was assessed using capillary electrophoresis on a Fragment Analyzer (Agilent) or Tapestation (Agilent), and libraries were quantified using quantitative PCR (Kapa Biosystems, KK4923) using the CFX96 Touch Real-Time PCR Detection System (BioRad). Plate pools were normalized to 2 nM and equal volumes from library plates were mixed together to make the sequencing sample pool.
Sequencing libraries from 384-well plates
Libraries were sequenced using the NextSeq or NovaSeq 6000 Sequencing System (Illumina) using 2 × 100 bp paired-end reads and 2 × 8 bp or 2 × 12 bp index reads. NextSeq runs used high output kits, whereas NovaSeq runs used either a 200 or 300-cycle kit (Illumina, 20012860). PhiX control library was spiked in at 1%.
Single-cell transcriptomic processing and analysis
Single-cell RNA-seq analysis was conducted in Jupyter (v.4.4.0)/Jupyter lab (v.2.1.0)/Python (v.3.7.3) using: Pandas (v.1.0.3), numpy (v.1.18.2), scanpy.api (v.1.4.4.post1), anndata (v.0.6.22rc1), plotnine (v.0.6.0), scipy (v.1.4.1), more_itertools (v.8.2.0), tqdm (v.4.45.0), sklearn (v.0.22.2.post1), lifelines (v.0.24.3) and matplotlib (v.3.0.3). Single-cell reads were mapped to the human reference hg38 containing ERCC sequences using STAR aligner 77 . HTSeq 78 was used to create gene count tables. These count tables were compiled and processed using Scanpy 79 . Low-quality cells were filtered on the basis of the following criteria: number of genes <500 or number of reads <50,000. Each gene in the transcriptome exhibited read counts in at least three cells. Cells exhibiting a greater than twofold higher number of genes than average were labelled as putative doublets and removed. Iterative Louvain clustering yielded cell-type-specific clusters, which were annotated using published marker genes based on intercluster differential expression analysis (two-sided Mann–Whitney U -test, Benjamini–Hochberg FDR <5%). In brief, Louvain clustering was performed on the k -nearest neighbour graph in principal component (PC) space of scaled highly variable genes. Cells were visualized using two-dimensional UMAP embeddings. Cell cycle status was inferred by the mean ranked expression of marker genes, referred to as the cell cycle program score 80 . Cells below the 95th percentile of the cell cycle program score were labelled non-cycling; by contrast, cells equal to or greater than the 95th percentile of the cell cycle program score were labelled cycling. To control for variance introduced by disproportionate populations of cycling cells across groups, non-cycling cells were considered for all downstream analyses. Thus, derivation of the four melanocyte developmental groups, anatomical site-specific analyses and human melanocyte differentiation programs analyses were conducted on non-cycling cells.
The resulting scRNA-seq data generated for this study available under accession number GSE151091 and code used to annotate and analyse the data are available at GitHub ( https://www.github.com/czbiohub/human_melanocytes ).
Melanocyte-specific Louvain clustering
Louvain clustering on melanocytes was performed on the melanocyte-only k -nearest neighbour graph in PC space of scaled highly variable genes. Low-resolution clustering (Fig. 1d ) was achieved using resolution = 0.1. High-resolution Louvain clustering (Fig. 1e ) was achieved independently of the low-resolution Louvain clustering using resolution = 0.9.
Identification of four melanocyte developmental stages
Differential gene expression analysis (using the Wilcoxon rank-sum test) of the high-resolution Louvain clusters indicated high similarity between clusters within each developmental age group (consistent with the low-resolution clustering), with the exception of fetal cluster 10. We therefore used unsupervised hierarchical clustering to group the high-resolution clusters according the median values of the first 15 PCs. PCs were chosen according to the elbow point in the variance explained PC plot 79 . Cells were binned according to high-resolution Louvain clustering groups (0–10). For each group of cells, the median of individual PCs was computed, resulting in a matrix consisting of 11 high-resolution Louvain clustering groups by 15 median PCs. This matrix was mean-centred and scaled to unit variance before performing hierarchical clustering using Ward’s criterion method. The four hierarchical clustering groups were established independent of the low-resolution Louvain clusters. However, as expected, they were consistent with the three low-resolution Louvain clusters while revealing a small distinct group of fetal cells enriched for MSC markers. Thus, both independent methods revealed this forth cluster (cluster 10 or m4 cluster) as a distinct group of cells ultimately defined as MSCs.
BSC analysis
Normalized FACS BSC was computed as the ratio of mean non-volar cutaneous cell BSC over mean volar cell BSC for each multisite donor-matched pair.
Fontana–Masson staining
Fontana–Masson staining was performed on fixed frozen sections, from patient-matched volar and non-volar cutaneous skin, using the Fontana-Masson Stain Kit (ab150669, Abcam) according to the manufacturer’s protocol.
Identification of pigment bifurcation and post-bifurcation genes
Pigment-associated genes identified by Baxter et al. 29 were filtered for genes associated with a human phenotype and mean ranked expression greater than the 10th percentile across each age of donor-matched melanocytes. Next, the differentially expressed pigment genes between adult donor-matched volar and non-volar melanocytes were identified (Mann–Whitney U- test). Genes that were differentially expressed in both donors were further invested for divergent expression in the fetal donor matched volar/non-volar melanocytes. Genes coinciding with pigment bifurcation were identified as differentially expressed between volar and non-volar melanocytes at 18 f.w. and/or 12 f.w. with a greater than or equal to 1.3-fold higher expression in non-volar melanocytes. The remaining genes were categorized at post-bifurcation.
Percentage of v-mel and c-mel cells
The top-ten cutaneous and top-ten volar DEGs were identified from the site-enriched genes on the basis of the highest median per-patient log-transformed fold change between cutaneous and volar samples. Individual cells were classified as v-mel if (1) four or more top-ten volar DEGs exhibited non-zero expression and (2) fewer than four top-ten cutaneous DEGs exhibited non-zero expression. By contrast, individual cells were classified as c-mel if (1) four or more top-ten cutaneous DEGs exhibited non-zero expression and (2) fewer than four top-ten volar DEGs exhibited non-zero expression. The percentage of v-mel and c-mel cells were then calculated for each skin sample of unique anatomical location from each individual patient.
To determine the percentage of HPGD + melanocytes in tissue sections, melanocytes (TYPR1 + cells) were manually counted. The fraction of cells was determined by the number of HPGD + TYRP1 + cells divided by the total number of TYRP1 + cells from each fixed frozen section. To quantify the number of NTRK2 and HPGD foci per DCT + cells from the RNAscope data, images were processed to correct for Opal 570 (HPGD) bleed-through into the Opal 620 (NTRK2) channel. After bleed-through correction, DCT and the associated DAPI signal were used to define the area of DCT + cells. Next, NTRK2 and HPGD foci within DCT + cells were counted manually. All Image analysis was performed in Fiji ( http://fiji.sc/ ), and statistical analysis was performed in OriginPro (2018b) and GraphPad Prism (v.9.0.0(121))
Immunofluorescence
Skin samples were fixed in 4% paraformaldehyde (Electron Microscopy Sciences) at 4 °C overnight, and washed with cold DPBS before paraffin or OCT embedding. Fixed frozen skin sections were incubated in blocking buffer (2.5% donkey serum, 2.5% goat serum (Jackson ImmunoResearch Laboratories), 1% bovine serum albumin (Sigma-Aldrich) and 0.1% Triton X-100 (Sigma-Aldrich)) for 1–2 h at room temperature. The following primary antibodies were used at the indicated concentration in blocking buffer overnight at 4 °C: mouse monoclonal anti-TYRP1 (1:200; TA99, ab3312, Abcam), mouse monoclonal anti-KIT (1:100; MA1-10072, Invitrogen, Thermo Fisher Scientific), rabbit polyclonal anti-HPGD (1:100; HPA005679, Sigma-Aldrich). Secondary antibodies against mouse IgG Alexa Fluor 488 (A21202, Thermo Fisher Scientific) or rabbit IgG conjugated to Dylight 594 (SA5-10040, Thermo Fisher Scientific) were used at a 1:1,000 dilution for 1–2 h at room temperature followed by addition of DAPI (1:1,000, Molecular Probes) for 1 min. Sections were mounted in VECTASHIELD Vibrance (Vector Laboratories) before imaging.
Immunofluorescence images were acquired using Nikon NIS-Elements multiplatform acquisition software (v.5.30.01) on a fully automated Nikon Ti-E inverted microscope with an Apo TIRF, ×60/1.49 NA oil-immersion objective (Nikon) and a Clara CCD camera (Andor). All Image analysis was performed in Fiji with statistical analysis performed in OriginPro and GraphPad Prism.
Multiplex RNA-FISH
We performed Muliplex RNA-FISH using the RNAscope Multiplex Fluorescent V2 assay (Bio-Techne, 323110) kit according to the manufacturer’s protocol on 10 µM formalin-fixed paraffin-embedded tissue sections. Tissues were stained using probes purchased from ACD for HPGD (Channel 1, 583651), NTRK2 (Channel 2, 402621-C2) and DCT (Channel 3, 494361-C3), and TSA Opal 570 (Channel 1, Akoya Biosciences, FP1488001KT), TSA Opal 620 (Channel 2, Akoya Biosciences, FP1488001KT) and TSA Opal 690 (Channel 3, Akoya Biosciences, FP1497001KT). TSA was used at a 1:1,500 dilution. Cells were counterstained with DAPI and mounted with Prolong Gold Antifade Mountant (Thermo Fisher Scientific, P36930). Tissues were imaged using the Leica DMi8 microscope.
Melanoma v-mel:c-mel score
Average log 2 -normalized expression of the top-100 volar enriched and top-100 cutaneous enriched genes was calculated for each primary tumour from SKCM TCGA and dbGAP ( phs001036.v1.p1 ). A v-mel:c-mel ratio was then calculated for each tumour by dividing the v-mel score (average expression) by the c-mel score. Tumours were then grouped according to their reported anatomical subtype: acral ( n = 13; dbGAP: phs001036.v1.p1 ; n = 2 SKCM) and non-acral cutaneous ( n = 103 SKCM).
Diffusion pseudotime
Diffusion pseudotime analysis of all non-cycling melanocyte cells was performed using the scanpy.tl.dpt function. The pseudotime reference root cell was chosen from the youngest sample (9.5 f.w.). The diffusion map was computed from an n = 30 neighbourhood graph with a Gaussian kernel.
Developmental group GSEA analyses
Gene set enrichment analyses for GO-bp 40 , 41 and previously identified neonatal foreskin and adult non-volar melanocyte cell-type DEG lists 10 were conducted using the top DEGs (Mann–Whitney U -test, Benjamini–Hochberg FDR < 5%) between developmental group in GSEA v.4.1.0 (refs. 81 , 82 ) using the GSEAPreranked tool with the weighted enrichment statistic, maximum size of 500 and minimum size of 10. Significantly enriched biological processes between temporally adjacent developmental groups (FET versus MSC; NEO versus FET; and NEO versus ADT) were determined by grouping the top-50 GO-bp terms (top-50 terms with FDR-adjusted q < 0.250) for each developmental group in each pairwise comparison based on common biological themes (Extended Data Fig. 6 ). The above identified biological processes were then assessed for enrichment across all the human developmental stages using the DEGs for (1) each developmental group compared to ADT and (2) each developmental group compared to MSC and then calculating the median NES (for all GO-bp terms with an FDR-adjusted q < 0.250) for each common biological theme (Fig. 4a ).
DevMel program biological pathway analysis
PercayAI (v.4.0, build 21) was used to identify relevant biological processes and pathways represented by the positive correlated genes within each DevMel program. The PercayAI software extracts all abstracts from PubMed that reference entities (genes) of interest (or their synonyms) using contextual language processing and a biological language dictionary that is not restricted to fixed pathway and ontology knowledge bases. Conditional probability analysis is used to compute the statistical enrichment of biological concepts (processes/pathways) over those that occur by random sampling. Related concepts built from the list of differentially expressed entities are further clustered into higher-level themes (for example, biological pathways/processes, cell types and structures). Within the PercayAI software platform, scoring of gene, concept and overall theme enrichment is accomplished using a multicomponent function referred to as the NES. The first component uses an empirical P value derived from several thousand random entity lists of comparable size to the users input entity list to define the rarity of a given entity-concept event. The second component, which effectively represents the fold enrichment, is based on the ratio of the concept enrichment score to the mean of that concept’s enrichment score across the set of randomized entity data. The top themes (chosen using the following settings: scale factor = 5, visible theme threshold = 7, connector threshold = 70) were manually reviewed for quality control to ensure that concepts within themes were based on key words linked to biological processes and pathways.
Single-cell DevMel logistic regression model
Input data were composed of single-cell transcriptomes from the following four non-volar cutaneous groups: MSC, FET, NEO and ADT. The input examples were randomly sampled and the number of examples was balanced among all labels. The combination of normal and melanoma transcriptomes was used to scale and centre the data. The input data were split into testing and training partitions at a ratio 33:67. We implemented elasticnet regularization with an l1 ratio = 0.8. Single-cell transcriptomes were evaluated by the model to yield a developmental stage label.
The code for the logistical regression model is available at GitHub ( https://github.com/danledinh/human_melanocytes ) 83
Model systems melanocyte program scores
For each individual cell, the program score is the mean normalized expression for all genes in the indicated published gene signature.
Classification of genes in melanoma dedifferentiation categories
Genes involved in melanoma dedifferentiation were identified from the normal melanocyte developmental programs (logistic regression variables: [MSC]prg, [FET]prg, [NEO]prg, and [ADT]prg) and the top-100 DEGs for each DevMel melanoma cell population (MAL [MSC] versus the rest, and so on). To identify transcriptional programs associated with patterns of dedifferentiation, the mean ranked expression pattern of each gene was compared (1) across four normal melanocyte DevMel groups (MSC, FET, NEO and ADT) and/or (2) across the four melanoma DevMel-based groups (MAL [MSC] , MAL [FET] , MAL [NEO] , MAL [ADT] ) and (3) between the normal melanocyte groups and the melanoma groups. Genes were then grouped into the following dedifferentiation pathways on the basis of the following expressing patterns:
Direct dedifferentiation genes
Direct dedifferentiation genes met both of the following two criteria: (1) the mean expression for MAL [MSC] , MAL [FET] , MAL [NEO] and MAL [ADT] was greater than or equal to fourfold of the mean expression of MSC, FET and NEO and (2) the mean expression of ADT was less than the mean expression of MSC, FET and NEO.
Sequential dedifferentiation genes
Sequential dedifferentiation genes met the following criterion: the DevMel stage with the highest mean expression in the normal melanocyte group was also the DevMel stage with the highest mean expression of the MAL [DevMel] melanoma groups. Ex: the MSC group has the highest expression of WNT5A compared all the normal melanocyte DevMel groups and MAL [MSC] also has the highest expression of WNT5A compared with the other MAL [DevMel] melanoma groups.
Normal-specific genes
Normal-specific genes met all of the following criteria: (1) the mean expression in each MAL [DevMel] melanoma group was less than the corresponding normal melanocyte DevMel group, and (2) the mean expression was in the bottom 10th percentile for all MAL [DevMel] melanoma groups, and (3) the mean expression was in the top 15th percentile for all normal melanocyte DevMel groups. Genes were then further classified into the following two groups:
Downregulated genes
Downregulated genes met all of the following criteria: (1) mean expression in each MAL [DevMel] melanoma group was less than or equal to the mean expression of MSC, FET and NEO normal melanocyte groups, and (2) mean expression of the ADT normal melanocyte group was greater than 1.5-fold mean expression of MSC, FET and NEO normal melanocyte groups.
Not-readopted genes
Not-readopted genes met all of the following criteria: (1) the mean expression in each MAL [DevMel] was less than or equal to the mean expression of the ADT normal melanocyte group, and (2) the mean expression in the MSC, FET and NEO normal melanocyte groups was greater than 1.5-fold the mean expression of the ADT normal melanocyte group.
Melanoma-specific genes
Melanoma-specific genes (identified from full transcriptomes of normal and malignant cells) met all of the following criteria: (1) the mean expression for each MAL [DevMel] melanoma group was greater than the corresponding normal melanocyte DevMel group, (2) the mean expression was in the top 40th percentile for each MAL [DevMel] melanoma group, and (3) the mean expression was in the bottom 10th percentile for all normal melanocyte DevMel groups.
Bulk tumour deconvolution
Bulk mRNA-seq analysis was conducted in Python (v.3.7.3) using Pandas (v.1.0.3), numpy (v.1.18.2), scanpy.api (v.1.4.4.post1), anndata (v.0.6.22rc1), plotnine (v.0.6.0), scipy (v.1.4.1), more_itertools (v.8.2.0), tqdm (v.4.45.0), sklearn (v.0.22.2.post1), lifelines (v.0.24.3), matplotlib (v.3.0.3) and CIBERSORT (v.1.06). CIBERSORT 66 was used to deconvolve bulk RNA-seq from the SKCM-TCGA ( https://www.cancer.gov/tcga ) as well as the LUND dataset ( GSE65904 ) 60 , 75 cohorts. As input, CIBERSORT requires cell-type-labelled transcriptomes to estimate the proportion of each cell type in a bulk RNA-seq sample. Here, we trimmed both single-cell and bulk RNA-seq transcriptomes to include only genes that are shared in both datasets. Adopting a k -fold cross-validation approach, we prepared ten sets of single-cell input transcriptomes from normal melanocytes across four developmental stages: MSC, FET, NEO and ADT (balanced cell counts across all labels). Each input transcriptome set was used to devolve the SKCM–TCGA or LUND bulk RNA-seq samples, yielding ten estimates of cell proportion. For each individual sample in the SKCM–TCGA or LUND dataset, the label means were used as the final estimate of label proportion. Hierarchical clustering was used to group SKCM–TCGA samples based on similar label proportions. One-sided Fisher’s exact tests were used to determine significant enrichment between two gene lists. The lifelines python package ( https://doi.org/10.5281/zenodo.3833188 ) was used to create Kaplan–Meier survival plots and perform log-rank tests using curated SKCM–TCGA metadata 84 .
Reporting Summary
Further information on research design is available in the Nature Research Reporting Summary linked to this article.
Data availability
All healthy human skin scRNA-seq data generated for this study has been deposited in the Gene Expression Omnibus (GEO) database repository and are available under accession number GSE151091 . Human melanoma datasets were obtained from publicly accessible repositories: GSE65904 , GSE72056 , GSE115978 , dbGAP phs001036.v1.p1 , TCGA Research Network ( https://www.cancer.gov/tcga ), and the Single Cell portal ( https://portals.broadinstitute.org/single_cell/study/melanoma-immunotherapy-resistance ). All other data supporting the findings of this study are available from the corresponding authors on reasonable request; lead contact: R.L.J.-T. Source data are provided with this paper.
Code availability
Jupyter notebooks with detailed analysis scripts are available at GitHub ( https://github.com/danledinh/human_melanocytes ) 83 .
References
Yamaguchi, Y. et al. Mesenchymal-epithelial interactions in the skin: Increased expression of dickkopf1 by palmoplantar fibroblasts inhibits melanocyte growth and differentiation. J. Cell Biol. 165 , 275–285 (2004).
Article CAS PubMed PubMed Central Google Scholar
Adameyko, I. et al. Schwann cell precursors from nerve innervation are a cellular origin of melanocytes in skin. Cell 139 , 366–379 (2009).
Article CAS PubMed Google Scholar
Mort, R. L., Jackson, I. J. & Elizabeth Patton, E. The melanocyte lineage in development and disease. Development 142 , 620–632 (2015).
Article CAS PubMed PubMed Central Google Scholar
Hayward, N. K. et al. Whole-genome landscapes of major melanoma subtypes. Nature 545 , 175–180 (2017).
Article CAS PubMed Google Scholar
Rabbie, R., Ferguson, P., Molina-Aguilar, C., Adams, D. J. & Robles-Espinoza, C. D. Melanoma subtypes: genomic profiles, prognostic molecular markers and therapeutic possibilities. J. Pathol. 247 , 539–551 (2019).
Article PubMed PubMed Central Google Scholar
Malta, T. M. et al. Machine learning identifies stemness features associated with oncogenic dedifferentiation. Cell 173 , 338–354 (2018).
Article CAS PubMed PubMed Central Google Scholar
Gupta, P. B. et al. The melanocyte differentiation program predisposes to metastasis after neoplastic transformation. Nat. Genet. 37 , 1047–1054 (2005).
Article CAS PubMed PubMed Central Google Scholar
Vorstandlechner, V. et al. Deciphering the functional heterogeneity of skin fibroblasts using single-cell RNA sequencing. FASEB J. 34 , 3677–3692 (2020).
Article CAS PubMed Google Scholar
Solé-Boldo, L. et al. Single-cell transcriptomes of the human skin reveal age-related loss of fibroblast priming. Commun. Biol. 3 , 188 (2020).
Article PubMed PubMed Central CAS Google Scholar
Cheng, J. B. et al. Transcriptional programming of normal and inflamed human epidermis at single-cell resolution. Cell Rep. 25 , 871–883 (2018).
Article CAS PubMed PubMed Central Google Scholar
Takahashi, R. et al. Defining transcriptional signatures of human hair follicle cell states. J. Invest. Dermatol. 140 , 764–773 (2020).
Article CAS PubMed Google Scholar
Popescu, D. M. et al. Decoding human fetal liver haematopoiesis. Nature 574 , 365–371 (2019).
Article CAS PubMed PubMed Central Google Scholar
Gao, S. et al. Tracing the temporal-spatial transcriptome landscapes of the human fetal digestive tract using single-cell RNA-sequencing. Nat. Cell Biol. 20 , 721–734 (2018).
Article CAS PubMed Google Scholar
Cao, J. et al. A human cell atlas of fetal gene expression. Science 370, eaba7721 (2020).
Sridhar, A. et al. Single-cell transcriptomic comparison of human fetal retina, hPSC-derived retinal organoids, and long-term retinal cultures. Cell Rep. 30 , 1644–1659 (2020).
Article CAS PubMed PubMed Central Google Scholar
Belote, R. L. & Simon, S. M. Ca 2+ transients in melanocyte dendrites and dendritic spine-like structures evoked by cell-to-cell signaling. J. Cell Biol. 219 , e201902014 (2020).
Article PubMed CAS Google Scholar
Norris, A., Todd, C., Graham, A., Quinn, A. G. & Thody, A. J. The expression of the c-kit receptor by epidermal melanocytes may be reduced in vitiligo. Br. J. Dermatol. 134 , 299–306 (1996).
Article CAS PubMed Google Scholar
Randall, V. A., Jenner, T. J., Hibberts, N. A., De Oliveira, I. O. & Vafaee, T. Stem cell factor/c-Kit signalling in normal and androgenetic alopecia hair follicles. J. Endocrinol. 197 , 11–23 (2008).
Article CAS PubMed Google Scholar
Picelli, S. et al. Smart-seq2 for sensitive full-length transcriptome profiling in single cells. Nat. Methods 10 , 1096–1100 (2013).
Article CAS PubMed Google Scholar
Hsiao, C. J. et al. Characterizing and inferring quantitative cell cycle phase in single-cell RNA-seq data analysis. Genome Res. 30 , 611–621 (2020).
Article CAS PubMed PubMed Central Google Scholar
Lu, R. et al. Transcription factor TCF4 maintains the properties of human corneal epithelial stem cells. Stem Cells 30 , 753–761 (2012).
Article CAS PubMed PubMed Central Google Scholar
Li, Z., Li, Y. & Jiao, J. Neural progenitor cells mediated by H2A.Z.2 regulate microglial development via Cxcl14 in the embryonic brain. Proc. Natl Acad. Sci. USA 116 , 24122–24132 (2019).
Article CAS PubMed PubMed Central Google Scholar
Denecker, G. et al. Identification of a ZEB2-MITF-ZEB1 transcriptional network that controls melanogenesis and melanoma progression. Cell Death Differ. 21 , 1250–1261 (2014).
Article CAS PubMed PubMed Central Google Scholar
Nishikawa, S.-I. & Osawa, M. Generating quiescent stem cells. Pigment Cell Res. 20 , 263–270 (2007).
Article PubMed Google Scholar
Joshi, S. S. et al. CD34 defines melanocyte stem cell subpopulations with distinct regenerative properties. PLOS Genet. 15 , e1008034 (2019).
Article CAS PubMed PubMed Central Google Scholar
Choi, H. R., Park, S. H., Choi, J. W., Kim, D. S. & Park, K. C. A simple assay method for melanosome transfer. Ann. Dermatol. 24 , 90–93 (2012).
Article CAS PubMed PubMed Central Google Scholar
Nakamura, M. et al. Site-specific migration of human fetal melanocytes in volar skin. J. Dermatol. Sci. 78 , 143–148 (2015).
Article CAS PubMed Google Scholar
Cramer, S. F. & Fesyuk, A. On the development of neurocutaneous units—Implications for the histogenesis of congenital, acquired, and dysplastic nevi. Am. J. Dermatopathol. 34 , 60–81 (2012).
Article PubMed Google Scholar
Baxter, L. L., Watkins-Chow, D. E., Pavan, W. J. & Loftus, S. K. A curated gene list for expanding the horizons of pigmentation biology. Pigment Cell Melanoma Res. 32 , 348–358 (2019).
Article PubMed Google Scholar
Adhikari, K. et al. A GWAS in Latin Americans highlights the convergent evolution of lighter skin pigmentation in Eurasia. Nat. Commun. 10 , 358 (2019).
Article PubMed PubMed Central CAS Google Scholar
Crawford, N. G. et al. Loci associated with skin pigmentation identified in African populations. Science 358 , eaan8433 (2017).
Article PubMed PubMed Central CAS Google Scholar
Han, J. et al. A genome-wide association study identifies novel alleles associated with hair color and skin pigmentation. PLoS Genet. 4 , e1000074 (2008).
Article PubMed PubMed Central CAS Google Scholar
Sturm, R. A. A golden age of human pigmentation genetics. Trends Genet. 22 , 464–468 (2006).
Article CAS PubMed Google Scholar
Antunes, L. C. M. et al. Tropomyosin-related kinase receptor and neurotrophin expression in cutaneous melanoma is associated with a poor prognosis and decreased survival. Oncology 97 , 26–37 (2019).
Article CAS PubMed Google Scholar
DiVito, K. A., Simbulan-Rosenthal, C. M., Chen, Y. S., Trabosh, V. A. & Rosenthal, D. S. Id2, Id3 and Id4 overcome a Smad7-mediated block in tumorigenesis, generating TGF-β-independent melanoma. Carcinogenesis 35 , 951–958 (2014).
Article CAS PubMed Google Scholar
Yamaguchi, Y. et al. Epithelial-mesenchymal interactions in wounds: treatment of palmoplantar wounds by nonpalmoplantar pure epidermal sheet grafts. Arch. Dermatol. 137 , 621–628 (2001).
CAS PubMed Google Scholar
Bolognia, J., Schaffer, J. & Cerroni, L. Dermatology 4th edn (Elsevier, 2018).
Bradford, P. T., Goldstein, A. M., McMaster, M. L. & Tucker, M. A. Acral lentiginous melanoma: Incidence and survival patterns in the United States, 1986-2005. Arch. Dermatol. 145 , 427–434 (2009).
Article PubMed PubMed Central Google Scholar
Mahendraraj, K. et al. Malignant melanoma in African-Americans. Medicine 96 , e6258 (2017).
Article PubMed PubMed Central Google Scholar
Ashburner, M. et al. Gene ontology: tool for the unification of biology. Nat. Genet. 25 , 25–29 (2000).
Article CAS PubMed PubMed Central Google Scholar
Carbon, S. et al. The Gene Ontology resource: enriching a GOld mine. Nucleic Acids Res. 49 , D325–D334 (2021).
Article CAS Google Scholar
Hou, L., Arnheiter, H. & Pavan, W. J. Interspecies difference in the regulation of melanocyte development by SOX10 and MITF. Proc. Natl Acad. Sci. USA 103 , 9081–9085 (2006).
Article CAS PubMed PubMed Central Google Scholar
Marie, K. L. et al. Melanoblast transcriptome analysis reveals pathways promoting melanoma metastasis. Nat. Commun. 11 , 333 (2020).
Article CAS PubMed PubMed Central Google Scholar
Rezza, A. et al. Signaling networks among stem cell precursors, transit-amplifying progenitors, and their niche in developing hair follicles. Cell Rep. 14 , 3001–3018 (2016).
Article CAS PubMed PubMed Central Google Scholar
Sennett, R. et al. An integrated transcriptome atlas of embryonic hair follicle progenitors, their niche, and the developing skin. Dev. Cell 34 , 577–591 (2015).
Article CAS PubMed PubMed Central Google Scholar
Mica, Y., Lee, G., Chambers, S. M., Tomishima, M. J. & Studer, L. Modeling neural crest induction, melanocyte specification, and disease-related pigmentation defects in hESCs and patient-specific iPSCs. Cell Rep. 3 , 1140–1152 (2013).
Article CAS PubMed PubMed Central Google Scholar
Osawa, M. et al. Molecular characterization of melanocyte stem cells in their niche. Development 132 , 5589–5599 (2005).
Article CAS PubMed Google Scholar
Lu, Z. et al. Hair follicle stem cells regulate retinoid metabolism to maintain the self-renewal niche for melanocyte stem cells. eLife 9 , e52712 (2020).
Article CAS PubMed PubMed Central Google Scholar
Saxena, N., Mok, K. W. & Rendl, M. An updated classification of hair follicle morphogenesis. Exp. Dermatol. 28 , 332–344 (2019).
Article PubMed PubMed Central Google Scholar
Gleason, B. C., Crum, C. P. & Murphy, G. F. Expression patterns of MITF during human cutaneous embryogenesis: evidence for bulge epithelial expression and persistence of dermal melanoblasts. J. Cutan. Pathol. 35 , 615–622 (2008).
Article PubMed PubMed Central Google Scholar
Holbrook, K. A., Underwood, R. A., Vogel, A. M., Gown, A. M. & Kimball, H. The appearance, density and distribution of melanocytes in human embryonic and fetal skin revealed by the anti-melanoma monoclonal antibody, HMB-45. Anat. Embryol. 180 , 443–455 (1989).
Article CAS Google Scholar
Hoek, K. S. et al. In vivo switching of human melanoma cells between proliferative and invasive states. Cancer Res. 68 , 650–656 (2008).
Article CAS PubMed Google Scholar
Tsoi, J. et al. Multi-stage differentiation defines melanoma subtypes with differential vulnerability to drug-induced iron-dependent oxidative stress. Cancer Cell 33 , 890–904 (2018).
Article CAS PubMed PubMed Central Google Scholar
Richard, G. et al. ZEB 1-mediated melanoma cell plasticity enhances resistance to MAPK inhibitors. EMBO Mol. Med. 8 , 1143–1161 (2016).
Article CAS PubMed PubMed Central Google Scholar
Landsberg, J. et al. Melanomas resist T-cell therapy through inflammation-induced reversible dedifferentiation. Nature 490 , 412–416 (2012).
Article CAS PubMed Google Scholar
Grzywa, T. M., Paskal, W. & Włodarski, P. K. Intratumor and intertumor heterogeneity in melanoma. Transl. Oncol. 10 , 956–975 (2017).
Article PubMed PubMed Central Google Scholar
Jerby-Arnon, L. et al. A cancer cell program promotes T cell exclusion and resistance to checkpoint blockade. Cell 175 , 984–997 (2018).
Article CAS PubMed PubMed Central Google Scholar
Tirosh, I. et al. Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq. Science 352 , 189–196 (2016).
Article CAS PubMed PubMed Central Google Scholar
Akbani, R. et al. Genomic classification of cutaneous melanoma. Cell 161 , 1681–1696 (2015).
Article CAS Google Scholar
Cirenajwis, H. et al. Molecular stratification of metastatic melanoma using gene expression profiling—prediction of survival outcome and benefit from molecular targeted therapy. Oncotarget 6 , 12297–12309 (2015).
Article PubMed PubMed Central Google Scholar
Widmer, D. S. et al. Systematic classification of melanoma cells by phenotype-specific gene expression mapping. Pigment Cell Melanoma Res. 25 , 343–353 (2012).
Article CAS PubMed Google Scholar
Raskin, L. et al. Transcriptome profiling identifies HMGA2 as a biomarker of melanoma progression and prognosis. J. Invest. Dermatol. 133 , 2585–2592 (2013).
Article CAS PubMed PubMed Central Google Scholar
Webster, M. R. et al. Wnt5A promotes an adaptive, senescent-like stress response, while continuing to drive invasion in melanoma cells. Pigment Cell Melanoma Res. 28 , 184–195 (2015).
Article CAS PubMed Google Scholar
Rambow, F. et al. Toward minimal residual disease-directed therapy in melanoma. Cell 174 , 843–855 (2018).
Article CAS PubMed Google Scholar
Guo, B. et al. Humanin peptide suppresses apoptosis by interfering with Bax activation. Nature 423 , 456–461 (2003).
Article CAS PubMed Google Scholar
Newman, A. M. et al. Robust enumeration of cell subsets from tissue expression profiles. Nat. Methods 12 , 453–457 (2015).
Article CAS PubMed PubMed Central Google Scholar
Wishart, D. S. et al. DrugBank 5.0: a major update to the DrugBank database for 2018. Nucleic Acids Res. 46 , D1074–D1082 (2018).
Article CAS PubMed Google Scholar
Okamoto, N. et al. A melanocyte-melanoma precursor niche in sweat glands of volar skin. Pigment Cell Melanoma Res. 27 , 1039–1050 (2014).
Article CAS PubMed Google Scholar
Nitzan, E., Pfaltzgraff, E. R., Labosky, P. A. & Kalcheim, C. Neural crest and Schwann cell progenitor-derived melanocytes are two spatially segregated populations similarly regulated by Foxd3. Proc. Natl Acad. Sci. USA 110 , 12709–12714 (2013).
Goydos, J. S. & Shoen, S. L. in Cancer Treatment and Research Vol. 167 321–329 (Kluwer Academic Publishers, 2016).
Siegel, R. L., Miller, K. D. & Jemal, A. Cancer statistics, 2020. CA Cancer J. Clinicians 70 , 7–30 (2020).
Article Google Scholar
Sennepin, A. et al. The human penis is a genuine immunological effector site. Front. Immunol. 8 , 1732 (2017).
Article PubMed PubMed Central CAS Google Scholar
Lezcano, C., Jungbluth, A. A., Nehal, K. S., Hollmann, T. J. & Busam, K. J. PRAME expression in melanocytic tumors. Am. J. Surgical Pathol. 42 , 1456–1465 (2018).
Article Google Scholar
Drey, E. A., Kang, M. S., McFarland, W. & Darney, P. D. Improving the accuracy of fetal foot length to confirm gestational duration. Obstet. Gynecol. 105 , 773–778 (2005).
Article PubMed Google Scholar
Darmanis, S. et al. A survey of human brain transcriptome diversity at the single cell level. Proc. Natl Acad. Sci. USA 112 , 7285–7290 (2015).
Article CAS PubMed PubMed Central Google Scholar
Liang, W. S. et al. Integrated genomic analyses reveal frequent TERT aberrations in acral melanoma. Genome Res. 27 , 524–532 (2017).
Article CAS PubMed PubMed Central Google Scholar
Dobin, A. et al. STAR: ultrafast universal RNA-seq aligner. Bioinformatics 29 , 15–21 (2013).
Article CAS PubMed Google Scholar
Anders, S., Pyl, P. T. & Huber, W. HTSeq-A Python framework to work with high-throughput sequencing data. Bioinformatics 31 , 166–169 (2015).
Article CAS PubMed Google Scholar
Wolf, F. A., Angerer, P. & Theis, F. J. SCANPY: large-scale single-cell gene expression data analysis. Genome Biol. 19 , 15 (2018).
Article PubMed PubMed Central Google Scholar
Hsiao, C. J. et al. Characterizing and inferring quantitative cell cycle phase in single-cell RNA-seq data analysis. Genome Res. 30 , 611–621 (2020).
Article CAS PubMed PubMed Central Google Scholar
Mootha, V. K. et al. PGC-1α-responsive genes involved in oxidative phosphorylation are coordinately downregulated in human diabetes. Nat. Genet. 34 , 267–273 (2003).
Article CAS PubMed Google Scholar
Subramanian, A. et al. Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. Proc. Natl Acad. Sci. USA 102 , 15545–15550 (2005).
Article CAS PubMed PubMed Central Google Scholar
Jupyter note books: danledinh/human_melanocytes. Zenodo https://doi.org/10.5281/zenodo.5076159 (2021).
Liu, J. et al. An integrated TCGA pan-cancer clinical data resource to drive high-quality survival outcome analytics. Cell 173 , 400–416 (2018).
Article CAS PubMed PubMed Central Google Scholar
Download references
Acknowledgements
We thank the staff at the University of California, San Francisco Program for Breakthrough Biomedical Research Sandler Fellows Program for funding (to R.L.J.-T.); the staff at the University of California, San Francisco Biospecimen Resource Program for support with tissue acquisition; N. Neff and M. Tan for assistance with library quality control and sequencing; the staff at the Huntsman Cancer Institute Bioinformatic Analysis Shared Resource and University of Utah Center for High Performance Computing for supporting analyses of acral tumour samples at the Huntsman Cancer Institute; and the staff at Life Science Editors for critical editing of the manuscript. Funders had no role in study design, data collection and analysis, decision to publish or preparation of the manuscript.
Author information
Author notes
Daniel Le
Present address: Department of Microchemistry, Proteomics, Lipidomics and Next Generation Sequencing, Genentech Inc, South San Francisco, CA, USA
Ashley Maynard
Present address: Department of Biosystems Science and Engineering, ETH Zürich, Basel, Switzerland
These authors contributed equally: Rachel L. Belote, Daniel Le.
Authors and Affiliations
Huntsman Cancer Institute, University of Utah, Salt Lake City, UT, USA
Rachel L. Belote & Robert L. Judson-Torres
Chan Zuckerberg Biohub, San Francisco, CA, USA
Daniel Le, Ashley Maynard & Spyros Darmanis
Department of Dermatology, University of California, San Francisco, CA, USA
Ursula E. Lang
Department of Pathology, University of California, San Francisco, CA, USA
Ursula E. Lang
Department of Urology and Division of Pediatric Urology, University of California, San Francisco, CA, USA
Adriane Sinclair & Laurence Baskin
Bioinformatics Shared Resource, Huntsman Cancer Institute, University of Utah, Salt Lake City, UT, USA
Brian K. Lohman
Department of Otolaryngology–Head and Neck Surgery, University of California, San Francisco, CA, USA
Vicente Planells-Palop & Aaron D. Tward
Department of Dermatology, University of Utah, Salt Lake City, UT, USA
Robert L. Judson-Torres
Department of Oncological Sciences, University of Utah, Salt Lake City, UT, USA
Robert L. Judson-Torres
Department of Microchemistry, Proteomics, Lipidomics and Next Generation Sequencing, Genentech Inc, South San Francisco, CA, USA
Spyros Darmanis
Authors
Rachel L. Belote
View author publications
Search author on: PubMed Google Scholar
Daniel Le
View author publications
Search author on: PubMed Google Scholar
Ashley Maynard
View author publications
Search author on: PubMed Google Scholar
Ursula E. Lang
View author publications
Search author on: PubMed Google Scholar
Adriane Sinclair
View author publications
Search author on: PubMed Google Scholar
Brian K. Lohman
View author publications
Search author on: PubMed Google Scholar
Vicente Planells-Palop
View author publications
Search author on: PubMed Google Scholar
Laurence Baskin
View author publications
Search author on: PubMed Google Scholar
Aaron D. Tward
View author publications
Search author on: PubMed Google Scholar
Spyros Darmanis
View author publications
Search author on: PubMed Google Scholar
Robert L. Judson-Torres
View author publications
Search author on: PubMed Google Scholar
Contributions
Conceptualization: R.L.B., D.L., A.D.T, S.D. and R.L.J.-T. Methodology: R.L.B. and A.M. Validation: R.L.B. and D.L. Formal analysis: R.L.B. and D.L. Investigation: R.L.B., D.L. and A.M. Resources: U.E.L., A.S., B.K.L., V.P.-P., L.B. and A.D.T. Data curation: D.L., A.M. and B.K.L. Writing—original draft: R.L.B. and R.L.J.-T. Writing—review and editing: D.L., A.M., U.E.L. and S.D. Visualization: R.L.B. and D.L. Supervision: S.D. and R.L.J.-T. Funding acquisition: S.D. and R.L.J.-T.
Corresponding authors
Correspondence to Spyros Darmanis or Robert L. Judson-Torres .
Ethics declarations
Competing interests
The authors declare no competing interests.
Additional information
Peer review information Nature Cell Biology thanks the anonymous reviewers for their contribution to the peer review of this work. Peer reviewer reports are available.
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.
Extended data
Extended Data Fig. 1 Single cell RNA sequencing quality control, cell-type specific markers, and donor age.
a) FACS gate protocol for representative sort. Melanocytes (blue circles in live, scatter, and singlets) were isolated as KIT+ cells from the CD11c- gate. b) Fraction of cells from each indexed FACS gate assignment. c) Number of reads and d) number of genes per cell for all 14,370 sequenced cells. Dashed line: quality control threshold, cells with < 50,000 reads and < 500 genes were excluded from further analysis. e) Genes expressed in more than 3 cells (dashed line) were included for subsequent analysis. f) Cell-type specific gene expression overlay on UMAPs. Genes indicated in upper left corner of each plot. g-i) UMAPs with donor age overlay for g) adult, h) neonatal, and i) fetal cells. j) Heatmap of expression values (row z-score) for all cell types in our dataset of differentially expressed genes (DEG)s from melanocyte clusters identified in previous fresh from human skin sequencing studies 10 , 11 .
Source data
Extended Data Fig. 2 Characterization of cell cycle state.
a) UMAPs of cycling cell program score used to determine which cells were designated as b) cycling (blue, in G2 & M phase) vs non-cycling (red). c) Fraction of cycling and non-cycling cells for each cell type identified in Fig. 1b .
Source data
Extended Data Fig. 3 FACS BSC is a correlate of relative melanocyte pigmentation.
a) Representative FACS plots of BSC and FSC for melanocytes from three non-volar cutaneous skin donors of varying skin pigmentation levels: light (L), light-medium (LM), and medium (M). b) Increase in BSC corresponds to increase in pigmentation. Mean raw BSC value with corresponding histogram for melanocytes isolated from non-volar cutaneous skin donors.
Source data
Extended Data Fig. 4 NTRK2 and HPGD expression (summarized in Fig. 3d ) by anatomic site and donor age.
Expression level of v-mel gene, NTRK2 , and c-mel gene, HPGD , in volar melanocytes compared to non-volar cutaneous melanocytes at each age (n=22 donors). Interquartile range with median, standard deviation, and outliers (grey circles).
Source data
Extended Data Fig. 5 Pseudotime and pairwise differential expression analysis of developmental ages and groups.
Pseudotime and pairwise differential expression analysis of developmental ages and groups. a) Melanocytes cluster by developmental age in diffusion component space DC1 and DC2. b) Pseudotime overlay onto DC space. c) Progression from fetal to adult through an intermediate neonatal transcriptional state. Diffusion pseudotime from b) is plotted for each cell, binned by donor age. d) Volcano plot highlighting the top ten DEGs between MSC (yellow) and FET (teal) non-volar cutaneous melanocyte populations. e) Volcano plot showing the top ten DEGs between FET (teal) and ADT (magenta) non-volar cutaneous melanocytes. (d-e) DEGs determined by Two-sided Wilcoxon Rank Sum Test and adjusted p-value computed using Benjamini-Hochberg multiple testing procedure. f) Heatmap visualization of the relative expression (column z score) of DEGs from (d) and (e) for all four non-volar cutaneous developmental groups. Both MSC and FET were enriched for known developmental genes ( SOX11, LYPD1 ) and genes involved in extracellular matrix establishment/remodeling ( COL1A2, PXDN ). The ADT group expressed genes involved in innate immunity, inflammation and regulating apoptosis/cell stress in other cell types and tissues ( HLAs, APOD, CLU, LGALS3 ). The NEO group exhibited high expression of a subset of genes from both the FET and ADT stages, consistent with neonatal melanocytes being an intermediate developmental state. See Supplementary Table 4 for the full list.
Source data
Extended Data Fig. 6 Identification of enriched biological processes in MSC, FET, NEO and ADT melanocytes.
Significantly enriched biological processes between temporally adjacent developmental groups a) FET vs MSC; b) NEO vs FET; and c) ADT vs NEO. Each dot represents an individual GO-bp term, plotted according to their associated NES. Dot color correspond to the FDR q-value for each GO-bp term and size corresponds to number of enriched genes from each GO-bp term.
Source data
Extended Data Fig. 7 Biological processes associated with DevMel transcriptional programs.
PercayAI, an augmented artificial intelligence software platform, identified biological concepts (processes/pathways) associated with the positively correlated genes in each DevMel transcriptional program. Two dimensional representation of biological themes (circles) comprised of genes related by associated biological concepts arrange in three dimensional space based on relatedness of each themes for a) prg[MSC]; b) prg[FET]; c) prg[NEO]; and d) prg[ADT]. Highly related themes are connected by grey lines.
Extended Data Fig. 8 Characterization of melanoma cells and tumors classified by in situ human melanocyte developmental programs.
a-b) Density plots showing the expression of a) the Widmer et al . from ref. 61 invasive and proliferative programs and b) the Tirosh et al . from ref. 58 AXL and MITF programs for individual cells in MAL ADT , MAL NEO , MAL FET and MAL MSC groups. c) Pairwise Fisher (one-sided) exact test showing negative log10 adjusted (Bonferroni multiple testing) p-values for the gene set enrichment analysis conducted using TCGA et al ., 2015, Cirenajwis et al ., 2015 and Tsoi et al ., 2018 gene signatures. Significant enrichment determined as adjusted p-value < 0.05. d) Heatmap showing the relative expression levels (row z score) of WNT5A high, TP53 high slow cycling cell associated genes in each normal melanocyte and MAL developmental group. e) Heatmap showing the relative expression levels (row z score) of the four minimal residual disease states identified by Rambow et al ., 2018 in each normal melanocyte and MAL developmental group. f) Pairwise Fisher (one-sided) exact test showing negative log10 adjusted (Bonferroni multiple testing) p-values for clinicopathological feature and transcriptional categorization within each SKCM group (SKCM ADT , SKCM NEO , SKCM FET , SKCM MSC ). There is little to no difference in the enrichment of pigment level, mutation category, or tissue origin between SKCM groups in Fig. 7 . g) Heatmap showing the relative expression levels (row z-score) of immune infiltration program, immune evasion program and FDA-approved therapeutic targets in SKCM groups. h) The MAL NEO signature is enriched for genes down regulated in tumors that respond to Nivolumab treatment (green text). Pairwise Fisher (one-sided) exact test showing negative log10 adjusted (Bonferroni multiple testing) p-values for the gene set enrichment analysis conducted using previously identified prognostic signatures (Supplementary Table 8 ).
Source data
Supplementary information
Reporting Summary (download PDF )
Supplementary Table 1–8 (download XLSX )
Supplementary Tables 1–8 in a single Excel file.
Peer Review Information (download PDF )
Source data
Source Data Fig. 1 (download XLSX )
Numerical and statistical source data.
Source Data Fig. 2 (download XLSX )
Numerical and statistical source data.
Source Data Fig. 3 (download XLSX )
Numerical and statistical source data.
Source Data Fig. 4 (download XLSX )
Numerical and statistical source data.
Source Data Fig. 5 (download XLSX )
Numerical and statistical source data.
Source Data Fig. 6 (download XLSX )
Numerical and statistical source data.
Source Data Fig. 7 (download XLSX )
Numerical and statistical source data.
Source Data Extended Data Fig. 1 (download XLSX )
Numerical and statistical source data.
Source Data Extended Data Fig. 2 (download XLSX )
Numerical and statistical source data.
Source Data Extended Data Fig. 3 (download XLSX )
Numerical and statistical source data.
Source Data Extended Data Fig. 4 (download XLSX )
Numerical and statistical source data.
Source Data Extended Data Fig. 5 (download XLSX )
Numerical and statistical source data.
Source Data Extended Data Fig. 6 (download XLSX )
Numerical and statistical source data.
Source Data Extended Data Fig. 8 (download XLSX )
Numerical and statistical source data.
Rights and permissions
Reprints and permissions
About this article
Cite this article
Belote, R.L., Le, D., Maynard, A. et al. Human melanocyte development and melanoma dedifferentiation at single-cell resolution. Nat Cell Biol 23 , 1035–1047 (2021). https://doi.org/10.1038/s41556-021-00740-8
Download citation
Received : 03 December 2020
Accepted : 18 July 2021
Published : 02 September 2021
Version of record : 02 September 2021
Issue date : September 2021
DOI : https://doi.org/10.1038/s41556-021-00740-8
Share this article
Anyone you share the following link with will be able to read this content:
Get shareable link
Sorry, a shareable link is not currently available for this article.
Copy shareable link to clipboard
Provided by the Springer Nature SharedIt content-sharing initiative
You have full access to this article via California Institute of Technology .
Associated content
Focus
Mapping the cells of the body
Dissecting melanocytes to predict melanoma
Alicia M. McConnell
Leonard I. Zon
Nature Cell Biology News & Views 02 Sept 2021
Advertisement
Explore content
Research articles
Reviews & Analysis
News & Comment
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
Nature Cell Biology ( Nat Cell Biol )
ISSN 1476-4679 (online)
ISSN 1465-7392 (print)
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
