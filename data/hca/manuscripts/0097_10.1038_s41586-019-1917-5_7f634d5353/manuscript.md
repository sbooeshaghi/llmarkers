Decoding the development of the human hippocampus | Nature
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
articles
Decoding the development of the human hippocampus
Published: 15 January 2020
Decoding the development of the human hippocampus
Suijuan Zhong 1 na1 ,
Wenyu Ding 2 na1 ,
Le Sun 1 , 3 , 4 na1 ,
Yufeng Lu 1 , 4 na1 ,
Hao Dong 1 , 4 ,
Xiaoying Fan 5 ,
Zeyuan Liu 1 , 4 ,
Ruiguo Chen 1 , 4 ,
Shu Zhang 5 ,
Qiang Ma 1 , 4 ,
Fuchou Tang 5 , 6 , 7 ,
Qian Wu 2 , 8 &
…
Xiaoqun Wang 1 , 3 , 4 , 9
Nature volume 577 , pages 531–536 ( 2020 ) Cite this article
50k Accesses
227 Citations
45 Altmetric
Subjects
Cell fate and cell lineage
Developmental neurogenesis
Abstract
The hippocampus is an important part of the limbic system in the human brain that has essential roles in spatial navigation and the consolidation of information from short-term memory to long-term memory 1 , 2 . Here we use single-cell RNA sequencing and assay for transposase-accessible chromatin using sequencing (ATAC–seq) analysis to illustrate the cell types, cell linage, molecular features and transcriptional regulation of the developing human hippocampus. Using the transcriptomes of 30,416 cells from the human hippocampus at gestational weeks 16–27, we identify 47 cell subtypes and their developmental trajectories. We also identify the migrating paths and cell lineages of PAX6 + and HOPX + hippocampal progenitors, and regional markers of CA1, CA3 and dentate gyrus neurons. Multiomic data have uncovered transcriptional regulatory networks of the dentate gyrus marker PROX1. We also illustrate spatially specific gene expression in the developing human prefrontal cortex and hippocampus. The molecular features of the human hippocampus at gestational weeks 16–20 are similar to those of the mouse at postnatal days 0–5 and reveal gene expression differences between the two species. Transient expression of the primate-specific gene NBPF1 leads to a marked increase in PROX1 + cells in the mouse hippocampus. These data provides a blueprint for understanding human hippocampal development and a tool for investigating related diseases.
You have full access to this article via California Institute of Technology .
Similar content being viewed by others
Mapping the spatial transcriptomic signature of the hippocampus during memory consolidation
Article Open access 29 September 2023
Single-cell transcriptomics of adult macaque hippocampus reveals neural precursor cell populations
Article 30 May 2022
Highly dynamic inflammatory and excitability transcriptional profiles in hippocampal CA1 following status epilepticus
Article Open access 14 December 2023
Main
The hippocampal formation (hippocampus) is a compound structure under the cerebral cortex in primates that forms and stores long-term memory by consolidating information from short-term memory, and also processes spatial information and navigation 1 , 2 .
Hippocampus single-cell transcriptome
To understand the molecular features of hippocampal cells during human brain development, we analysed 30,416 cells from the entire left hippocampus (including the hippocampus proper, the dentate gyrus (DG) and some of the subiculum connected to the hippocampus proper) at gestational weeks (GW) 16–27 (Supplementary Table 1 ) by droplet-based single-cell RNA sequencing (scRNA-seq). We performed t -distributed stochastic neighbour embedding ( t -SNE) analysis and identified cells as progenitors, excitatory neurons (ExN), inhibitory neurons (InN), Cajal Retzius cells, astrocytes, oligodendrocyte progenitor cells (OPCs), oligodendrocytes, microglia and endothelial cells by using classic markers and gene ontology (GO) of differentially expressed genes (DEGs) (Fig. 1a–c , Extended Data Fig. 1a–c ). The distributions of samples from two individuals at GW22 were similar on the t -SNE plot (Extended Data Fig. 1d ). We then used the DG marker PROX1 to subclassify the ExN as DG ExN or non-DG ExN. The InN were further subclassified as being derived from the medial or caudal ganglionic eminence (MGE or CGE) on the basis of LHX6 and NR2F2 expression (Fig. 1a–d ). PROX1 is an essential transcription factor for the genesis of hippocampal granule cells and formation of the DG 3 , 4 . By searching transcription factor motifs identified from ATAC-seq peaks close to the PROX1 transcription start site (TSS), we found three potential binding sites for LEF1 or TCF4, indicating that WNT signals are crucial for the production of DG granule cells (Fig. 1e, f ), which is consistent with reported studies 5 , 6 . We further segregated cells into 47 distinct hierarchical subtypes by principal component analysis (PCA), showing that different subtypes of progenitors were highly correlated with fate-determined cells (Fig. 1g , Extended Data Fig. 2a–c ).
Fig. 1: Molecular diversity of single cells from the developing human hippocampus.
The alternative text for this image may have been generated using AI.
Full size image
a – c , Visualization of eleven major classes using t -SNE in 3D ( a ) and 2D ( b ) visualization. c , Expression of known markers. HP, hippocampus; PFC, prefrontal cortex. Dots, individual cells; grey, no expression; red, relative expression (log-normalized gene expression). d , Immunostaining of MEIS2 and PROX1. Scale bar, 500 μm. e , Normalized ATAC-seq profiles of PROX1 in GW25 hippocampus show the activation of PROX1 . Amplified view (pink) shows predicted LEF1 and TCF4 binding sites. f , LEF1 and TCF4 binding motifs are identified in the ATAC-seq peaks close to the PROX1 TSS. g , Hierarchical clustering analysis of 47 subclasses. AC, astrocyte; P, progenitor; CR, Cajal–Retzius cell; M, microglia; EC, endothelial cell. n = 134, 141, 95, 275, 58, 300, 397, 159, 204, 483, 101, 74, 670, 1,019, 1,765, 2,334, 793, 1,073, 909, 3,189, 2,347, 92, 1,838, 717, 1,956, 730, 1,192, 2,573, 54, 259, 84, 84, 44, 489, 465, 246, 68, 229, 638, 540, 131, 103, 139, 257, 227, 459 and 282 cells, top to bottom. h , Abstracted graph shows the connections on the transcriptome between different cell types in the developing human hippocampus and PFC. i , Scatterplot of all genes for correlation with conserved differentiation network across PFC and hippocampus. Blue plot shows genes related to PFC; red plot shows genes related to hippocampus. j , k , Maturation scores of excitatory neurons ( j ) and inhibitory neurons ( k ) in PFC and hippocampus. l , m , Immunostaining for oligodendrocyte markers at GW16 in human hippocampus and prefrontal cortex. Scale bars, 500 μm ( l , left); 100 μm ( l , right, m ). The experiment was repeated three times independently with similar results.
To study developmental differences between the hippocampus and neocortex, we compared the transcriptome of the hippocampus (GW16–27) with that of the human prefrontal cortex (PFC) (GW8–26) 7 (Fig. 1h ) and found differences in gene expression between the PFC and hippocampus across all cell types (Fig. 1i , Supplementary Table 2 ). The HMG box domain-containing protein TOX was highly expressed in the PFC, whose progenitors are regulated by HMGA2 7 , 8 . SOX4 and SOX11, two SOXC transcription factors that are required for neuronal differentiation during neurogenesis in the adult hippocampus 9 , 10 , were relatively highly expressed in the hippocampus (Fig. 1i ). GO analysis of DEGs between ExN from the hippocampus and PFC at GW16 indicate that hippocampal ExN may undergo synapse organization and axonogenesis at GW16 (Extended Data Fig. 2d ). Comparison of the maturation trajectories of hippocampus and PFC neurons indicated that hippocampus non-DG ExN were more mature than PFC ExN, whereas maturation of DG ExN was similar to that of PFC ExN (Fig. 1j ). InN of the PFC and hippocampus generally showed a similar maturation status, whereas MGE-derived InN were more mature than CGE-derived InN in the hippocampus (Fig. 1k ). Consistent with transcriptome analysis, immunofluorescence staining for OLIG2 and MBP showed a number of MBP + cells in the subfield of the hippocampus, whereas no MBP + cells were found in the human PFC at GW16 (Fig. 1l, m , Extended Data Fig. 2e ), suggesting that oligodendrocytes may be involved the maturation of hippocampal neurons during early development.
Progenitors of the developing hippocampus
To further investigate cellular lineage relationships in the fetal human hippocampus, we reconstructed five developmental paths by monocle analysis without microglia and endothelial cells (Fig. 2a ). Three major subgroups of progenitors differentiated to excitatory neuronal, OPC and oligodendrocyte or astrocyte lineages. The MGE- and CGE-derived InN were separated in different directions, which is consistent with previous studies showing that hippocampal InN originate from different progenitors located in the ganglionic eminence 11 . To further reveal the diversity and molecular properties of human hippocampal progenitors, we used GO analysis of DEGs and marker genes to identify eight subclusters (Extended Data Fig. 3a–c ). EOMES + , MEIS2 + and NEUROD2 + progenitors were in clusters P3 and P4, indicative of ExN generation (Extended Data Fig. 3a ). AQP4 , OLIG1 / OLIG2 and PDGFRA were highly expressed in clusters P5, P6 and P7, respectively, indicative of astrocyte and oligodendrocyte cell fates. Cluster P8 contained a small number of progenitors that highly expressed DLX1 and DLX2 , indicating that these cells may differentiate as InN (Extended Data Fig. 3a–f ).
Fig. 2: Molecular signature of neural progenitor cells of the developing human hippocampus.
The alternative text for this image may have been generated using AI.
Full size image
a , Cell lineage relationships of all cells analysed except for microglia and endothelial cells in developing human hippocampus. Monocle recovered a branched single-cell trajectory beginning with progenitors and terminating at excitatory neurons, inhibitory neurons, astrocytes and oligodendrocytes. b , Cell lineage relationships of progenitors, excitatory neurons, astrocytes and oligodendrocytes in developing human hippocampus. Known gene expression is shown below. Arrows show the directions of lineages. c , Immunofluorescence images of PROX1(scale bar, 200 μm), PAX6 and SOX2 at GW11. Scale bars, 500 μm (left), 200 μm (top right), 100 μm (bottom right). I, primary matrix. d , Immunofluorescence images of HOPX and SOX2 at GW11. Scale bars, 500 μm (left), 200 μm (top right), 100 μm (bottom right). e , Immunofluorescence images of PROX1 (scale bars, 1,000 μm, inset 500 μm), PAX6, HOPX and SOX2 in GW14. Scale bar, 200 μm. II, secondary matrix. f , Immunofluorescence images of PROX1 (scale bar, 1,000 μm), PAX6, HOPX and SOX2 at GW16 (top) and GW22 (bottom). Scale bar, 500 μm. III, tertiary matrix. g , h , Immunofluorescence images of PAX6, HOPX, NEUROD1 and GFAP at GW25. Scale bars, 500 μm (left); 100 μm (right). c – h , The experiments were repeated three times independently with similar results. i , Schema depicting locations of PAX6 + or HOPX + progenitors in developing human hippocampus from GW11 to GW22. Arrows indicate direction of migration.
To understand how progenitors develop into neuronal and glial cells, we carried out trajectory analysis (Fig. 2b ) and separated three paths towards neurons, astrocytes and oligodendrocytes. Notably, PAX6 + and HOPX + progenitors, which are considered as neurogenic progenitors in the neocortex 12 , were likely to contribute to both neurogenesis and gliogenesis in the human hippocampus (Fig. 2b , Extended Data Fig. 3g, h ). We next examined the locations of cells expressing PAX6 or HOPX by immunofluorescence staining (Fig. 2c–f ). At GW11, the primordial hippocampal area, located adjacent to the cortical hem (CH), was composed of the dentate neuroepithelium (DNE) and ammonic neuroepithelium (ANE). The majority of cells in the DNE and ANE expressed SOX2, and PAX6 + SOX2 + progenitors of ANE started to migrate (Fig. 2c , Extended Data Fig. 4a ). At the same time, HOPX + SOX2 + DNE progenitors also indicated migration potential (Fig. 2d , Extended Data Fig. 4b ). As the hippocampus developed at GW14, a number of PAX6 + progenitors migrated away from the ventricular zone towards the future DG (PROX1 + region, Fig. 2e , Extended Data Fig. 4c ), forming the primary matrix (I) and secondary matrix (II). HOPX + progenitors also migrated in the same direction but closer to the pial side (Fig. 2e , Extended Data Fig. 4c ). At GW16, the migration of PAX6 + and HOPX + progenitors continued and many cells arrived at the hilus and formed an origin hub of DG cells, called the tertiary matrix (III). Notably, PAX6 + progenitors were located outside HOPX + progenitors while migrating (Fig. 2f , Extended Data Fig. 4d–f ). PAX6 + progenitors were still abundant, and some were located in the blades of the DG, but only some HOPX + progenitors were found in the hilus; the majority of HOPX + progenitors were in the cornu ammonis (CA) at GW 22 (Fig. 2f , Extended Data Fig. 4g–i ).
We next evaluated the proliferation capacity and cell fate of PAX6 + and HOPX + progenitors. Both scRNA-seq data and immunostaining indicate that a subpopulation of PAX6 + and HOPX + progenitors are active in the cell cycle even at the mid-gestational stage (Extended Data Fig. 5a–d ). In cell fate assessment, we observed PAX6 + NEUROD1 + cells in the CA and DG, but PAX6 + GFAP + cells only in the CA (Fig. 2g , Extended Data Fig. 5e–g ). Similar expression patterns were found in HOXP + cells (Fig. 2h , Extended Data Fig. 5h, i ). Next, we evaluated the maturation status of PAX6 + or HOPX + progenitors and found that NEUROD1 + cells were more mature than GFAP + cells, suggesting that they may have been born earlier (Extended Data Fig. 5j, k ). Together, our data suggest that although the origins and migrating paths of PAX6 + and HOPX + progenitors differ, they both contribute to neural and glial genesis in a spatiotemporal manner in the developing human hippocampus (Fig. 2i ).
Neurons in developing hippocampus
To further investigate the developmental characteristics of hippocampal neurons, we subclassified all the excitatory neurons into seven groups by PCA (Fig. 3a, b ). Excitatory neurons from CA1, CA3 and DG were grouped as ExN01–03 (Fig. 3b , Extended Data Fig. 6a ). SEMA5A and PID1 were selected as marker genes for DG and CA1, respectively, while SULF2 and NRIP3 were considered as CA3 markers (Fig. 3c , Extended Data Fig. 6b ). Consistent with progenitor migration paths, the maturation analysis suggests that CA1 neurons were more mature than CA3 and DG neurons (Fig. 3d ). Excitatory neurons were categorized into three groups according to their developmental stage, and GO analysis of DEGs indicates that neurogenesis is the major event at GW16–18, followed by axonogenesis (GW20–22) and function development (GW25–27) (Fig. 3e–g ). To further analyse the transcriptional regulation of DG formation, we selected the subclusters of highly variable genes and clustered them into nine modules by weighted gene coexpression network analysis (WGCNA) (Extended Data Fig. 6c, d ). The green module includes PROX1 , suggesting that the genes in this module may be correlated with DG development (Fig. 3h ). When we analysed ATAC-seq data for the hippocampus at GW25, we found PROX1 motifs in ATAC peaks close to the TSSs of several genes, including KCNJ6 , NFIA , DUSP1 and NPTX2 , which are also in the green module (Fig. 3i, j ). Among these genes, KCNJ6 (also known as GIRK2 ) encodes a member of the G-protein-activated inwardly rectifying K + channels that is widely abundant in the brain and has been implicated in learning and memory, reward, motor coordination, and other functions 13 .
Fig. 3: Dynamics of neurogenesis in the developing human hippocampus.
The alternative text for this image may have been generated using AI.
Full size image
a , Visualization of seven subtypes of excitatory neuron in the developing human hippocampus using t -SNE. Sample sizes of clusters: 2,573, 2,347, 1,838, 1,956, 1,192, 717, 92 cells. b , Heat map showing the expression level and identity of genes in the excitatory neurons subclasses. Top, distribution of each subclass by gestational week. c , In situ hybridization of region-specific genes in DG, CA1 and CA3 at GW27. Scale bar, 600 μm. The experiment was repeated three times independently with similar results. d , Maturation scores of seven subtypes of excitatory neuron show that CA1 neurons are more mature than CA3 and DG neurons. e – g , The enriched gene ontology terms show the cell properties of the hippocampus at different weeks. Sample sizes: 4,912 cells ( e ); 4,164 cells ( f ); 1,639 cells ( g ). h , The social network Cytoscape graph depicts the gene network regulation of excitatory neurons. i , j , Motifs of PROX1 ( i ) and the normalized ATAC-seq profile of downstream genes of PROX1 ( j ) in GW25 hippocampus with three independent biological replicates. k , Cell lineage relationships of progenitors and inhibitory neurons analysed in developing human hippocampus. Monocle recovered a branched single-cell trajectory beginning with progenitors and terminating at subgroups of inhibitory neurons. l , Markers were ordered by Monocle analysis in pseudo-time. Line with blue shading represents inhibitory neurons derived from CGE; pink shading represents inhibitory neurons derived from MGE.
Hippocampal inhibitory neurons arise from MGE and CGE precursors. Notably, monocle analysis suggested that the majority of MGE-derived InN ( LHX6 + ) and CGE-derived InN ( NR2F1/2 + ) were separated (Fig. 3k , Extended Data Fig. 7a–c ). The pseudo-time analysis demonstrated that InN expressing CCK , CALB2 and VIP accumulated in the CGE differentiation path, and the majority of SATB1 + and SST + neurons were in the MGE path (Fig. 3l , Extended Data Fig. 7b, c ). Additionally, we found genes that may regulate cell fate determination at the first branch point (Extended Data Fig. 7d, e ). Microglia, the immune cells in the CNS, originate from the mesoderm 14 . We classified microglia into 11 subclusters and observed that M9 contained microglia in active cell cycles from all developing stages (Extended Data Fig. 8a–d ). The immunostaining images also indicated proliferating microglia at GW25 (Extended Data Fig. 8e ).
Evolution signatures of developing hippocampus
Although the hippocampus is considered an evolutionarily conserved part of the brain, transcriptomic correlation coefficient analysis illustrated that the developmental timing of the human hippocampus from GW16 to 20 was similar to that at P0–5 in mice 15 , 16 (Fig. 4a ), suggesting that the human embryonic hippocampal development occurs earlier but lasts for longer than in mice. We also found DEGs in the human hippocampus, some of which are primate-specific, including STX10 , CHMP4A , BEX5 , NBPF1 and the long non-coding RNA CASC15 (Fig. 4b, c ). In situ images and ATAC-seq data identified the mRNA localization and transcription regulatory sites of these genes (Fig. 4c ). Genes of the neuroblastoma breakpoint family (NBPF) contain a repeated domain called DUF1220, the copy number of which is related to brain evolution and complexity 17 . Several NBPF family genes are expressed in hippocampal cells, and the expression of NBPF1 was relatively high and general in all cell types (Fig. 4c , Extended Data Fig. 9a ). NBPF1 with eight DUF1220 domains exists only in primates, and in particular in species that are evolutionally close to humans (Extended Data Fig. 9b, c ). To further investigate its role in hippocampal development, we transiently expressed NBPF1 in the mouse primordial hippocampal area at embryonic day 13.5 (E13.5) and observed that these mice had more PROX1 + cells and an enlarged PROX1 + area at E15.5 and E18.5 when compared with control mice (Fig. 4d–g , Extended Data Fig. 9d–f ). To understand how NBPF1 regulates hippocampal development, we collected single GFP + cells (Extended Data Fig. 9g ). LHX2 has been considered as an essential gene in the hippocampal primordium to regulate hippocampal neuronal development 18 . Single-cell quantitative RT–PCR results indicated that LHX2 expression was higher in NBPF1–GFP + cells (Extended Data Fig. 9h ). Further analysis of open chromatin areas close to the PROX1 TSS revealed three potential sites for LHX2 binding (Extended Data Fig. 9i ), indicating a possible molecular mechanism by which NBPF1 may regulate hippocampal development via LHX2.
Fig. 4: Specific genes expressed in the human developing hippocampus.
The alternative text for this image may have been generated using AI.
Full size image
a , Heat map showing correlation of different stages of hippocampus development in human and mouse. The developing human hippocampus is similar to the developing mouse hippocampus at P0–5. b , Heat map showing DEGs in human and mouse hippocampus. c , Expression of human-specific genes in t -SNE plots (left). Right, in situ hybridization at GW25; bottom, normalized ATAC-seq profile of human-specific genes in hippocampus in GW25 with three independent biological replicates. Scale bar, 300 μm. d , e , Overexpression of NBPF1 promotes DG formation at E13.5, observed at E15.5 ( d ) and E18.5 ( e ) in mouse. Scale bars, 500 μm ( d , left), 100 μm ( d , right), 200 μm ( e ). f , g , Percentage of PROX1 + cells among GFP + cells. f , E13.5–E15.5: ** P = 0.0049, two-sided t -test. n = 6, 5 brain slices per experiment; mean ± s.d. g , E13.5–E18.5: ** P = 0.0015. n = 6, 5 brain slices per experiment. IUE, in utero electroporation.
Source data
Discussion
We have systematically analysed scRNA-seq and ATAC-seq data to identify cell type diversities, gene expression trajectories, transcription regulation networks and signal transduction pathways in the developing human hippocampus. The hippocampus starts to form from the hippocampal primordium in response to bone morphogenetic protein (BMP) and WNT secreted by the CH 18 , 19 , 20 . An open chromatin area close to the PROX1 TSS contains the binding motif for LEF1 and TCF4, two transcription factors that are involved in the WNT signalling pathway by recruiting the coactivator beta-catenin to enhancer elements of targeting genes 5 , indicating that WNT signals not only initiate differentiation of the medial pallium to the hippocampus, but also contribute to subregional patterning of the hippocampus. The adult neural stem cells located in the subgranular zone give rise to granule cells throughout adult life in most mammals 21 . WNT signalling also helps to regulate granule cell genesis and neural activity in adult mammals 22 , 23 , indicating that the key gene regulation may be conserved in embryonic and adult neurogenesis in the hippocampal DG.
HOPX has been recently identified as a gene that is expressed by dentate precursors and contributes to embryonic and postnatal neurogenesis in mice 24 . Another unbiased single-cell RNA-seq analysis has indicated that perinatal, postnatal, and adult neurogenesis in the mouse DG are fundamentally similar 15 . Notably, clonal lineage-tracing of HOPX + cells in mice showed that these precursors generate neurons located in the DG or CA 24 . Consistently, we found that at GW11, although most HOPX + progenitors are located in the DNE, a subset of HOPX + progenitors is found in the ANE, indicating that HOPX + progenitors in different locations may have different cell fates.
The copy number of the DUF1220 protein domain in the genome is correlated with the evolutionary proximity of the species to humans as well as with brain size, cognitive capability, and severity of autism 17 , 25 , 26 , 27 . Major copies of human DUF1220 domains are encoded by the NBPF gene family. Microarray data from the Allen Brain Atlas suggest that NBPF1 expression decreases when the human brain develops ( http://www.brainspan.org ). LHX2 is expressed in the dorsal and medial pallium but not in the CH, which secretes WNT ligands and functions as an organizer that is necessary and sufficient to induce the hippocampus 18 . Notably, expression of NBPF1 upregulates LHX2 expression and increases the number of hippocampal PROX1 + granule cells in the developing mouse brain. However, the detailed molecular mechanisms of this process need further investigation.
Methods
No statistical methods were used to predetermine sample size. The experiments were not randomized and investigators were not blinded to allocation during experiments and outcome assessment.
Tissue sample collection
The de-identified human tissue collection and research protocols were approved by the Reproductive Study Ethics Committee of Beijing Anzhen Hospital and the institutional review board (ethics committee) of the Institute of Biophysics. The informed consent was designed as recommended by the ISSCR guidelines for fetal tissue donation and fetal tissue samples were collected after the donor patients signing an informed consent document that was in strict observance of the legal and institutional ethical regulations for samples from elective pregnancy terminations at Beijing Anzhen Hospital, Capital Medical University. All samples used in these studies had not been involved in any other procedures. All the protocols were in compliance with the Interim Measures for the Administration of Human Genetic Resources, administered by the Ministry of Science and Technology of China.
Animals
Timed pregnant female mice at embryonic day 13.5 were used for in utero electroporation experiments. Embryos for experiments after in utero electroporation included both male and female mice. Mouse housing and experimental protocols in this study were in compliance with the guidelines of the Institutional Animal Care and Use Committee of the Institute of Biophysics, CAS. All mice had free access to food and water and were housed in the institutional animal care facility with a 12-h light–dark schedule.
Tissue sample dissection
Gestational age was measured in weeks from the first day of the woman’s last menstrual cycle to the sample collecting date. Fetal brains were collected in ice-cold artificial cerebrospinal fluid containing 125.0 mM NaCl, 26.0 mM NaHCO 3 , 2.5 mM KCl, 2.0mM CaCl 2 , 1.0 mM MgCl 2 , 1.25 mM NaH 2 PO 4 at a pH of 7.4 when oxygenated (95% O 2 and 5% CO 2 ). The hippocampus was dissected and put in hibernate E medium (Invitrogen, Cat. A1247601). The hippocampus tissue was first digested in 2 mg/ml collagenase IV (Gibco, Cat. 17104-019) and 10 U/μl DNase I (NEB, Cat. M0303L) in hibernate E medium and then in 1 mg/ml papain (Sigma, Cat. P4762) and 10 U/μl DNase I in hibernate E medium. Samples were vortexed at 300 g and 37 °C on a thermocycler for 20 min. Further pipetting was used to fully digest the tissue into single cells. After that, the cell suspension was centrifuged at 700 g for 5 min to obtain the cell pellet. The digestion medium was carefully removed and the cell pellet was resuspended in 300 μl 0.04% BSA in PBS and kept on ice.
RNA library preparation for high-throughput sequencing
Thousands of cells were partitioned into nanolitre-scale Gel Bead-In-EMulsions (GEMs) using 10x GemCode Technology, where cDNA produced from the same cell shares a common 10x Barcode. Upon dissolution of the single cell 3′ gel bead in a GEM, primers containing an Illumina R1 sequence (read1 sequencing primer), a 16-bp 10x Barcode, a 10-bp randomer and a poly-dT primer sequence were released and mixed with cell lysate and Master Mix. After incubation of the GEMs, barcoded, full-length cDNA from poly-adenylated mRNA was generated. Then the GEMs were broken and silane magnetic beads were used to remove leftover biochemical reagents and primers. Prior to library construction, enzymatic fragmentation and size selection were used to optimize the cDNA amplicon size. P5, P7, a sample index and R2 (read 2 primer sequence) were added to each selected cDNA during end repair and adaptor ligation. P5 and P7 primers were used in Illumina bridge amplification of the cDNA ( http://10xgenomics.com ). Finally, the library was sequenced into 150-bp paired-end reads using the Illumina HiSeq4000.
Data processing of scRNA-seq from Chromium system
Cell ranger 2.0.1 ( http://10xgenomics.com ) was used to perform quality control and read counting of Ensemble genes with default parameters (v2.0.1) by mapping to the hg19 human genome. We excluded poor-quality cells after the gene-cell data matrix was generated by Cell Ranger software using the Seurat package (v2.3.4). Only cells that expressed more than 800 genes and fewer than 7,000 genes were considered, and only genes expressed in at least 30 single cells (0.1% of the raw data) were included for further analysis. Cells that expressed haemoglobin genes ( HBM , HBA1 , HBA2 , HBB , HBD , HBE1 , HBG1 , HBG2 , HBQ1 and HBZ ) were also excluded. Cells with a mitochondrial gene percentage over 15% were discarded. In total, 17,737 genes across 30,416 single cells remained for subsequent analysis. The data were normalized to a total of l × 10 4 molecules per cell for the sequencing depth using the Seurat package. The batch effect was mitigated by using the ScaleData function of Seurat (v2.3.4).
Identification of cell types and subtypes by dimensional reduction and PAGA analysis
The Seurat package (v2.3.4) was used to perform linear dimensional reduction. We selected 982 highly variable genes with average expression between 0.0125 and 8 and dispersion greater than 2 as input for PCA. Then we identified significant PCs based on the JackStrawPlot function. Strong PC1–PC10 were used for t -SNE to cluster the cells by FindClusters function with resolution 1.2. Clusters were identified by the expression of known cell-type markers and GO analysis. The markers ASCL1, NEUROD2, GAD1, OLIG2, MBP, AQP4, SPARC and PTPRC were used to hippocampal cells as progenitor cells, excitatory neurons, inhibitory neurons, OPCs, oligodendrocytes, astrocytes, endothelial cells and microglia, respectively.
Three-dimensional t -SNE was applied to cluster all cells in the human developing hippocampus (dim.embed = 5) with PC1–PC10. Visualizations were done using rgl package (v0.99.16) implemented in R. We then applied partition-based graph abstraction (PAGA) to predict a lineage tree for the hippocampal and the prefrontal cortical cells in an unbiased way. We produced a consolidated lineage tree that included all identified cell types rooted to a stem cell group.
Identification of DEGs among clusters
The DEGs of each cluster were identified using the FindAllMarkers function (thresh.use = 0.25, test.use = “wilcox”) with the Seurat R package (6). We used the Wilcoxon rank-sum test (default), and genes with average expression difference >0.5 natural log with P < 0.05 were selected as marker genes. Enriched GO terms of marker genes were identified using DAVID 6.8 28 , 29 ( https://david.ncifcrf.gov/home.jsp ) and Metascape 30 ( http://metascape.org ).
Constructing single cell trajectories in the hippocampus
The Monocle 2 R package (version 2.6.4) and Monocle 3 alpha R package (version 2.99.2) were applied to construct single cell pseudo-time trajectories to discover developmental transitions 31 , 32 , 33 . We used highly variable genes identified by Seurat to sort cells into pseudo-time order. The actual gestational time of each cell informs us which states of cells are at the beginning of pseudo-time in the first round of “orderCells”. We then call “orderCells” again, passing this state as the root_state argument. “DDRTree” and “UMAP” were applied to reduce dimensional space and the minimum spanning tree on cells was plotted using the visualization functions “plot_complex_cell_trajectory” or “plot_3d_cell_trajectory” for Monocle 2 and Monocle 3 alpha, respectively.
Cell-cycle analysis
In the cell-cycle analysis, we applied a cell-cycle related gene set with 43 genes expressed during G1/S and 54 genes expressed during G2/M 34 , 35 . We defined the G1/S and G2/M states of each cell by comparing the average expression of the two gene sets using the CellCycleScoring function using Seurat R package. These gene sets should be anticorrelated in their expression levels, and cells expressing neither are likely to be in the G1 phase (not cycling).
WGCNA analysis in categorizing genes
WGCNA analysis was performed by R package ‘‘WGCNA’’ 36 , 37 (R version 3.4.3, https://cran.r-project.org/src/contrib/Archive/WGCNA ; package version 1.6.6). The WGCNA soft power value was determined by navigating the soft-threshold-mean-connectivity curve. Modules with <0.25 similarity were merged. Modules correlated with a specific cell subtype were considered as standard modules for categorizing genes into certain cell subtypes. Seven modules were selected for neuron subtypes.
ATAC library preparation for high-throughput sequencing
ATAC-seq was performed as described previously 38 , 39 . In brief, a total of 50,000 cells were washed twice with 50 μl of cold PBS and resuspended in 50 μl lysis buffer (10 mM Tris-HCl pH 7.4, 10 mM NaCl, 3 mM MgCl2, 0.1% (v/v) Nonidet P40 Substitute). The suspension of nuclei was then centrifuged for 10 min at 500 g at 4 °C, followed by the addition of 50 μl transposition reaction mix (10 μl 5 × TTBL buffer, 4 μl TTE mix and 36 μl nuclease-free H 2 O) from the TruePrep DNA Library Prep Kit V2 for Illumina (Vazyme Biotech). Samples were then incubated at 37 °C for 30 min. DNA was isolated using a QIAquick PCR Purification Kit (QIAGEN). ATAC-seq libraries were first subjected to five cycles of preamplification. To determine the suitable number of cycles required for the second round of PCR, the library was assessed by quantitative PCR as described previously 38 and then PCR amplified for the appropriate number of cycles. Libraries were purified with a QIAquick PCR Purification Kit (QIAGEN). Library quality was checked using a High Sensitivity DNA Analysis Kit (Agilent). Finally, 2 × 150 paired-end sequencing was performed on an Illumina HiSeq X-10.
ATAC-seq data analysis
In simple terms, we removed adaptor sequences and then mapped reads to the hg19 reference genome with the parameters: -t -q -N 1 -L 25 -X 2000 using Bowtie2 (version 2.3.4.3). All unmapped reads, non-uniquely mapped reads and PCR duplicates were removed. The uniquely mapped reads were shifted by +4 or −5 bp according to the strand of the read. To visualize the ATAC-seq signal, we extended each read by 50 bp and counted the coverage for each base. All the ATAC-seq peaks were called by MACS2 v2.1.1 with the parameters –nolambda.
ATAC-seq data quality control
ATAC-seq data quality was evaluated for several parameters, including the number of raw reads, alignment rate, percentage of reads mapped to chromosome M, percentage of reads mapped to repeat regions (black list), percentage of reads that passed MAPQ score filter, percentage of total signal within known artefact regions and correlation between replications.
Connecting transcription factors to target genes
To find the potential transcription factors that bind the PROX1 regulatory sequence (TSS ± 2k), FIMO from MEME Suite (version 5.0.4) was used for motif enrichment analysis. To investigate the genes that are regulates by PROX1, the PROX1 motif profile was downloaded from the Jaspar database ( http://jaspar.genereg.net/ ), and we used FIMO from the MEME suite for enrichment analysis of our peaks.
Immunofluorescent staining
Tissue samples were fixed overnight in 4% paraformaldehyde, cryoprotected in 30% sucrose, and embedded in optimal cutting temperature (Thermo Scientific). Thin 40-μm cryosections were collected on superfrost slides (VWR) using a Leica CM3050S cryostat. For immunohistochemistry, heat-induced antigen retrieval was performed in 10 mM sodium citrate buffer, pH 6. Primary antibodies: mouse anti-CD45 (1:100, Abcam ab8216), goat anti-SOX2 (1:250, Santa Cruz sc-17320), rabbit anti-PAX6 (1:500, BioLegend 901301), rabbit anti-NEUROD2 (1:500, Abcam ab104430), mouse anti-NEUROD1 (1:100, Abcam ab60704), rabbit anti-HOPX (1:1,000, Santa Cruz sc-30216), mouse anti-Ki67 (1:100, BD 550609), mouse anti-SATB2 (1:250, Abcam ab51502), mouse anti-MEIS2 (1:200, Santa cruz sc-81986), rabbit anti-PROX1 (1:500, Abcam ab199359), rabbit anti-OLIG2 (1:500, Millipore AB9610), human anti-MBP (1:1,000, Abcam ab209328), mouse anti-GFAP (1:200, CST 3670S) diluted in blocking buffer containing 10% donkey serum, 0.5% Triton-X100 and 0.2% gelatin diluted in PBS at pH 7.4. Binding was revealed using an appropriate Alexa Fluor 488, Alexa Fluor 594, or Alexa Fluor 647 fluorophore-conjugated secondary antibody (Life Technologies). Cell nuclei were counterstained using DAPI (Life Technologies). Images were collected using an Olympus FV1000 confocal microscope.
In situ hybridization
The in situ hybridization protocol has been described previously 40 . In brief, probes complementary to target human mRNA used for RNA in situ hybridization were cloned from primary human fetal cortical cDNA samples and reverse-transcribed using PrimeScript II 1st Strand cDNA Synthesis Kit (Takara) with oligo dT primers. Total RNA was isolated from GW27 human hippocampus using SV Total RNA Isolation System (Promega). Specific genes were amplified using the following primers: SEMA5A forward AGC TCG CTT GGC TTT AGT CTT A, reverse CAA AAT AGG CTT TGA CTC CCA C; PID1 forward TGG GAT CTC TAG TGG GGT GG, reverse TAA GGC TTC TTA GGT GCC GC; SULF2 forward GTT TGA CAT CAG GGT CCC GT, reverse CTT TAA TGG GGT TGG CGG CT; NRIP3 forward AGC TGT GGT TGA TGA CAA TGA G, reverse CTG TAA TGG ATA ATG TCC CTG G; STX10 forward GGG GAA GGG ACT GAC ATG TC, reverse GGA GGG CTG GGG TCA GAG AG; CHMP4A forward GAT TGG GCA AGG CTG GTC CC, reverse TTG GGA GCT GGC CCT GCC GG; BEX5 forward TCA ACA TGG AAA ATG TCC CC, reverse AGA CTG CTT TTA AAT TGC TT; NBPF1 forward GGG TGC ACC AAG AGC AGC CT, reverse CCT CAG CAT AAA TTT TAT GA; CASC15 forward CAA GCA TGT AGC CCT GCC CG, reverse CTC TGT TTC TGT CAT CTC TC; primers specific to target genes of interest were designed using Primer3 and amplified by PCR using Q5 High-Fidelity DNA Polymerase (NEB). PCR products of predicted band size were gel extracted and ligated into the Hieff Clone Plus One Step Cloning Kit (Yeason). Ligation products were transfected into Trans5α Chemically Competent E. coli (Transgene). Cloned sequences were confirmed by sequencing. Digoxigenin-labelled RNA probes for in situ hybridization were generated by linearizing the pSPT18 Vector and in vitro transcribing the probe using T7 or SP6 RNA Polymerase (Roche) in the presence of DIG-RNA Labelling Mix (Roche). Fetal brain sections of 30µm thickness were hybridized with RNA probes at a final concentration of 500 ng/ml overnight at 64.5 °C in hybridization solution (50% formamide, 10% dextran sulfate, 0.2% tRNA (Invitrogen), 1 × Denhardt’s solution (Sigma) and 1 × salt solution (containing 0.2 M NaCl, 0.01 M Tris, 5 mM NaH 2 PO 4 , 5 mM Na 2 HPO 4 , 5 mM EDTA pH 7.5)) overnight. After the sections were washed, alkaline phosphatase-coupled anti-digoxigenin Fab fragments (Roche) were applied. For visualization of the labelled cRNAs, the sections were incubated in the dark in NBT/BCIP solution (Roche). Images were taken using a Leica SCN400 (Leica Microsystems).
Plasmids and in utero electroporation
NBPF1 genes were cloned into a pEGFP-C1 vector. Electroporation was performed as previously described 41 . In brief, timed pregnant CD-1 mice (E13.5) were deeply anaesthetized with isoflurane, and the uterine horns were exposed through a midline incision. 1 μl of plasmid DNA (1–2 μg/μl) mixed with Fast Green (Sigma) was manually microinjected into the fetal brain lateral ventricle through the uterus, using a bevelled and calibrated glass micropipette (Drummond Scientific) followed by five 50-ms pulses of 50 mV with a 1 s interval delivered across the uterus with two 9-mm electrode paddles positioned on either side of the head (BTX, ECM830).
Patch-qRT–PCR of NBPF1–GFP plasmid overexpressed cells
Coronal slices containing cells overexpressing the NBPF1–GFP plasmid were prepared using a vibratome (VT1200S, Leica, Wetzlar, Germany) in oxygenated (95% O 2 and 5% CO 2 ) ice-cold sucrose-based artificial cerebrospinal fluid (s-ACSF, 234 mM sucrose, 2.5 mM KCl, 26 mM NaHCO 3 , 1.25 mM NaH 2 PO 4 , 11 mM d -glucose, 0.5 mM CaCl 2 and 10 mM MgSO 4 ). The slices were kept in an incubating chamber filled with oxygenated ACSF (126 mM NaCl, 3 mM KCl, 1.2 mM NaH 2 PO 4 , 2.4 mM CaCl 2 , 1.3 mM MgSO 4 , 26 mM NaHCO 3 , 10 mM d -glucose) at 34 °C for 30 min. After a recovery period of at least 60 min at room temperature, an individual slice was transferred to a recording chamber and was continuously superfused with oxygenated ACSF (4 ml/min) at room temperature. We captured whole cells overexpressing the NBPF1–GFP plasmid and distributed each into a single tube, and then we used SMART-seq2 to amplify the mRNA into a cDNA library. Then, we used qRT–PCR to detect NBPF1 and LHX2 gene expression. Specific genes were amplified using the following primers: GAPDH forward GTC AAG CTC ATT TCC TGG TAT GAC, reverse TAT GGG GGT CTG GGA TGG AA; NBPF1 forward GCG AGG CTG CCC GAG CTT CT, reverse GAC TTC GCG TAA CTT CCC ATT CA; LHX2 forward GAA CGA TGC TGA ACA CCT GG, reverse AAC CAG ACC TGG AGG AC TCT C.
Statistical analysis
Comparisons between two groups were made using t -tests. The quantification graphs were analysed by using GraphPad Prism (GraphPad Software). Sample size and P values are given in the Figure legends.
Reporting summary
Further information on research design is available in the Nature Research Reporting Summary linked to this paper.
Data availability
The scRNA-seq data and ATAC-seq data used in this study have been deposited in the Gene Expression Omnibus (GEO) under accession number GSE131258 . Raw image files used in the figures that support the findings of this study are available from the corresponding authors upon reasonable request.
References
Bird, C. M. & Burgess, N. The hippocampus and memory: insights from spatial processing. Nat. Rev. Neurosci . 9 , 182–194 (2008).
PubMed CAS Google Scholar
Miller, A. M., Vedder, L. C., Law, L. M. & Smith, D. M. Cues, context, and long-term memory: the role of the retrosplenial cortex in spatial cognition. Front. Hum. Neurosci . 8 , 586 (2014).
PubMed PubMed Central Google Scholar
Lavado, A., Lagutin, O. V., Chow, L. M., Baker, S. J. & Oliver, G. Prox1 is required for granule cell maturation and intermediate progenitor maintenance during brain neurogenesis. PLoS Biol . 8 , e1000460 (2010).
PubMed PubMed Central Google Scholar
Sugiyama, T., Osumi, N. & Katsuyama, Y. The germinal matrices in the developing dentate gyrus are composed of neuronal progenitors at distinct differentiation stages. Dev. Dyn . 242 , 1442–1453 (2013).
PubMed CAS Google Scholar
Galceran, J., Miyashita-Lin, E. M., Devaney, E., Rubenstein, J. L. R. & Grosschedl, R. Hippocampus development and generation of dentate gyrus granule cells is regulated by LEF1. Development 127 , 469–482 (2000).
PubMed CAS Google Scholar
Lee, S. M. K., Tole, S., Grove, E. & McMahon, A. P. A local Wnt-3a signal is required for development of the mammalian hippocampus. Development 127 , 457–467 (2000).
PubMed CAS Google Scholar
Zhong, S. J. et al. A single-cell RNA-seq survey of the developmental landscape of the human prefrontal cortex. Nature 555 , 524–528 (2018).
ADS PubMed CAS Google Scholar
Nowakowski, T. J. et al. Spatiotemporal gene expression trajectories reveal developmental hierarchies of the human cortex. Science 358 , 1318–1323 (2017).
ADS PubMed PubMed Central CAS Google Scholar
Mu, L. et al. SoxC transcription factors are required for neuronal differentiation in adult hippocampal neurogenesis. J. Neurosci . 32 , 3067–3080 (2012).
PubMed PubMed Central CAS Google Scholar
Wang, Y., Lin, L., Lai, H., Parada, L. F. & Lei, L. Transcription factor Sox11 is essential for both embryonic and adult neurogenesis. Dev. Dyn . 242 , 638–653 (2013).
PubMed CAS Google Scholar
Bandler, R. C., Mayer, C. & Fishell, G. Cortical interneuron specification: the juncture of genes, time and geometry. Curr. Opin. Neurobiol . 42 , 17–24 (2017).
PubMed CAS Google Scholar
Pollen, A. A. et al. Molecular identity of human outer radial glia during cortical development. Cell 163 , 55–67 (2015).
PubMed PubMed Central CAS Google Scholar
Cooper, A. et al. Trisomy of the G protein-coupled K+ channel gene, Kcnj6 , affects reward mechanisms, cognitive functions, and synaptic plasticity in mice. Proc. Natl Acad. Sci. USA 109 , 2642–2647 (2012).
ADS PubMed CAS PubMed Central Google Scholar
Gomez Perdiguero, E., Schulz, C. & Geissmann, F. Development and homeostasis of “resident” myeloid cells: the case of the microglia. Glia 61 , 112–120 (2013).
PubMed Google Scholar
Hochgerner, H., Zeisel, A., Lönnerberg, P. & Linnarsson, S. Conserved properties of dentate gyrus neurogenesis across postnatal development revealed by single-cell RNA sequencing. Nat. Neurosci . 21 , 290–299 (2018).
PubMed CAS Google Scholar
La Manno, G. et al. RNA velocity of single cells. Nature 560 , 494–498 (2018).
ADS PubMed PubMed Central Google Scholar
Dumas, L. J. et al. DUF1220-domain copy number implicated in human brain-size pathology and evolution. Am. J. Hum. Genet . 91 , 444–454 (2012).
PubMed PubMed Central CAS Google Scholar
Mangale, V. S. et al. Lhx2 selector activity specifies cortical identity and suppresses hippocampal organizer fate. Science 319 , 304–309 (2008).
ADS PubMed PubMed Central CAS Google Scholar
Grove, E. A., Tole, S., Limon, J., Yip, L. & Ragsdale, C. W. The hem of the embryonic cerebral cortex is defined by the expression of multiple Wnt genes and is compromised in Gli3-deficient mice. Development 125 , 2315–2325 (1998).
PubMed CAS Google Scholar
Yoshida, M., Assimacopoulos, S., Jones, K. R. & Grove, E. A. Massive loss of Cajal-Retzius cells does not disrupt neocortical layer order. Development 133 , 537–545 (2006).
PubMed CAS Google Scholar
Kempermann, G., Song, H. & Gage, F. H. Neurogenesis in the adult hippocampus. Cold Spring Harb. Perspect. Biol . 7 , a018812 (2015).
PubMed PubMed Central Google Scholar
Ortiz-Matamoros, A., Salcedo-Tello, P., Avila-Muñoz, E., Zepeda, A. & Arias, C. Role of wnt signaling in the control of adult hippocampal functioning in health and disease: therapeutic implications. Curr. Neuropharmacol . 11 , 465–476 (2013).
PubMed PubMed Central CAS Google Scholar
Varela-Nallar, L. & Inestrosa, N. C. Wnt signaling in the regulation of adult hippocampal neurogenesis. Front. Cell. Neurosci . 7 , 100 (2013).
PubMed PubMed Central CAS Google Scholar
Berg, D. A. et al. A common embryonic origin of stem cells drives developmental and adult neurogenesis. Cell 177 , 654–668.e15 (2019).
PubMed CAS PubMed Central Google Scholar
Davis, J. M. et al. DUF1220 dosage is linearly associated with increasing severity of the three primary symptoms of autism. PLOS Genet . 10 , e1004241 (2014).
PubMed PubMed Central Google Scholar
Keeney, J. G., Dumas, L. & Sikela, J. M. The case for DUF1220 domain dosage as a primary contributor to anthropoid brain expansion. Front. Hum. Neurosci . 8 , 427 (2014).
PubMed PubMed Central Google Scholar
Popesco, M. C. et al. Human lineage-specific amplification, selection, and neuronal expression of DUF1220 domains. Science 313 , 1304–1307 (2006).
ADS PubMed CAS Google Scholar
Huang, W., Sherman, B. T. & Lempicki, R. A. Bioinformatics enrichment tools: paths toward the comprehensive functional analysis of large gene lists. Nucleic Acids Res . 37 , 1–13 (2009).
Google Scholar
Huang, W., Sherman, B. T. & Lempicki, R. A. Systematic and integrative analysis of large gene lists using DAVID bioinformatics resources. Nat. Protoc. 4 , 44–57 (2009).
CAS Google Scholar
Tripathi, S. et al. Meta- and orthogonal integration of influenza “OMICs” data defines a role for UBR4 in virus budding. Cell Host Microbe 18 , 723–735 (2015).
PubMed PubMed Central CAS Google Scholar
Qiu, X. et al. Single-cell mRNA quantification and differential analysis with Census. Nat. Methods 14 , 309–315 (2017).
PubMed PubMed Central CAS Google Scholar
Qiu, X. et al. Reversed graph embedding resolves complex single-cell trajectories. Nat. Methods 14 , 979–982 (2017).
PubMed PubMed Central CAS Google Scholar
Trapnell, C. et al. The dynamics and regulators of cell fate decisions are revealed by pseudotemporal ordering of single cells. Nat. Biotechnol . 32 , 381–386 (2014).
PubMed PubMed Central CAS Google Scholar
Macosko, E. Z. et al. Highly parallel genome-wide expression profiling of individual cells using nanoliter droplets. Cell 161 , 1202–1214 (2015).
PubMed PubMed Central CAS Google Scholar
Tirosh, I. et al. Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq. Science 352 , 189–196 (2016).
ADS PubMed PubMed Central CAS Google Scholar
Langfelder, P. & Horvath, S. WGCNA: an R package for weighted correlation network analysis. BMC Bioinformatics 9 , 559 (2008).
PubMed PubMed Central Google Scholar
Langfelder, P. & Horvath, S. Fast R functions for robust correlations and hierarchical clustering. J. Stat. Softw . 46 , i11 (2012).
PubMed PubMed Central Google Scholar
Buenrostro, J. D., Wu, B., Chang, H. Y. & Greenleaf, W. J. ATAC-seq: A method for assaying chromatin accessibility genome-wide. Curr. Protoc. Mol. Biol . 109 , 21–29 (2015).
PubMed PubMed Central Google Scholar
Buenrostro, J. D., Giresi, P. G., Zaba, L. C., Chang, H. Y. & Greenleaf, W. J. Transposition of native chromatin for fast and sensitive epigenomic profiling of open chromatin, DNA-binding proteins and nucleosome position. Nat. Methods 10 , 1213–1218 (2013).
PubMed PubMed Central CAS Google Scholar
Palop, J. J., Roberson, E. D. & Cobos, I. Step-by-step in situ hybridization method for localizing gene expression changes in the brain. Methods Mol. Biol . 670 , 207–230 (2011).
PubMed CAS Google Scholar
Wang, X., Tsai, J. W., LaMonica, B. & Kriegstein, A. R. A new subtype of progenitor cell in the mouse embryonic neocortex. Nat. Neurosci . 14 , 555–561 (2011).
PubMed PubMed Central CAS Google Scholar
Download references
Acknowledgements
This work was supported by the National Key R&D Program of China (2019YFA0110100), the Strategic Priority Research Program of the Chinese Academy of Sciences (XDA16020601, XDB32010100), the National Basic Research Program of China (2017YFA0102601, 2017YFA0103303), the National Natural Science Foundation of China (NSFC) (91732301, 31671072, 31771140, 81891001), the Grants of Shanghai Brain-Intelligence Project from STCSM (16JC1420500), the Grants of Beijing Brain Initiative of Beijing Municipal Science & Technology Commission (Z181100001518004).
Author information
Author notes
These authors contributed equally: Suijuan Zhong, Wenyu Ding, Le Sun, Yufeng Lu
Authors and Affiliations
State Key Laboratory of Brain and Cognitive Science, CAS Center for Excellence in Brain Science and Intelligence Technology, Institute of Brain-Intelligence Technology (Shanghai), Institute of Biophysics, Chinese Academy of Sciences, Beijing, China
Suijuan Zhong, Le Sun, Yufeng Lu, Hao Dong, Zeyuan Liu, Ruiguo Chen, Qiang Ma & Xiaoqun Wang
State Key Laboratory of Cognitive Neuroscience and Learning, Beijing Normal University, Beijing, China
Wenyu Ding & Qian Wu
Institute for Stem Cell and Regeneration, Chinese Academy of Sciences, Beijing, China
Le Sun & Xiaoqun Wang
University of Chinese Academy of Sciences, Beijing, China
Le Sun, Yufeng Lu, Hao Dong, Zeyuan Liu, Ruiguo Chen, Qiang Ma & Xiaoqun Wang
Beijing Advanced Innovation Center for Genomics, College of Life Sciences, Peking University, Beijing, China
Xiaoying Fan, Shu Zhang & Fuchou Tang
Biomedical Institute for Pioneering Investigation via Convergence and Center for Reproductive Medicine, Ministry of Education Key Laboratory of Cell Proliferation and Differentiation, Beijing, China
Fuchou Tang
Peking-Tsinghua Center for Life Sciences, Peking University, Beijing, China
Fuchou Tang
IDG/McGovern Institute for Brain Research, Beijing Normal University, Beijing, China
Qian Wu
Beijing Institute for Brain Disorders, Beijing, China
Xiaoqun Wang
Authors
Suijuan Zhong
View author publications
Search author on: PubMed Google Scholar
Wenyu Ding
View author publications
Search author on: PubMed Google Scholar
Le Sun
View author publications
Search author on: PubMed Google Scholar
Yufeng Lu
View author publications
Search author on: PubMed Google Scholar
Hao Dong
View author publications
Search author on: PubMed Google Scholar
Xiaoying Fan
View author publications
Search author on: PubMed Google Scholar
Zeyuan Liu
View author publications
Search author on: PubMed Google Scholar
Ruiguo Chen
View author publications
Search author on: PubMed Google Scholar
Shu Zhang
View author publications
Search author on: PubMed Google Scholar
Qiang Ma
View author publications
Search author on: PubMed Google Scholar
Fuchou Tang
View author publications
Search author on: PubMed Google Scholar
Qian Wu
View author publications
Search author on: PubMed Google Scholar
Xiaoqun Wang
View author publications
Search author on: PubMed Google Scholar
Contributions
Q.W. and X.W. conceived the project, designed the experiments and wrote the manuscript. S. Zhong and Y.L. performed the scRNA-seq experiment. W.D. performed the ATAC-seq and animal surgery. S. Zhong, Y.L., X.F., S. Zhang and F.T. analysed the RNA-seq data. S. Zhong and H.D. analysed the ATAC-seq data. L.S. and R.C. collected single cells by patch-clamping. Z.L. and S. Zhong carried out qRT–PCR. Q.M. prepared the samples. S. Zhong, Q.W. and W.D. performed immunostaining, in situ hybridization and imaging. All authors edited and proofread the manuscript.
Corresponding authors
Correspondence to Qian Wu or Xiaoqun Wang .
Ethics declarations
Competing interests
The authors declare no competing interests.
Additional information
Peer review information Nature thanks Joseph Loturco, Christopher Walsh and the other, anonymous, reviewer(s) for their contribution to the peer review of this work.
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.
Extended data figures and tables
Extended Data Fig. 1 Single-cell RNA-seq information and molecular diversity of single cells.
a , Scheme of bioinformatic analysis. b , Expression of known markers shown using the same layout as in Fig. 1b . Grey, no expression; red, relative expression. c , Heat map showing the expression level and identity of genes in all cells in the developing hippocampus. Sample sizes: astrocytes, 703; Cajal–Retzius cells, 101; endothelial cells, 540; non-DG ExN, 8,199; MGE-derived InN, 6,377; microglia, 2,660; oligodendrocytes, 209; OPCs, 1,250; progenitors, 2,486; DG ExN, 2,516; CGE-derived InN, 5,375. d , t -SNE plots of cells in the hippocampus. Two repetitions of GW22 are labelled in different shapes, and no obvious distribution differences are observed among the different batches from the same embryo stages. Each cell colour represents the gestational week. Sample size: GW16, 4,411 cells; GW18, 4,035 cells; GW20, 10,101 cells; GW22#01, 1,617 cells; GW22#02, 2,485 cells; GW25, 2,824 cells; GW27, 4,943 cells.
Extended Data Fig. 2 Molecular diversity of subgroups of cells.
a – c , Heat maps show the subclasses of inhibitory neurons ( a ), astrocytes ( b ) and oligodendrocytes ( c ). The genes are organized into clusters. The bar chart on the top shows the gestational week. Specific genes related to each subtype are highlighted on the right with enriched GO terms. Interneurons: 3,189, 2,334, 909, 670, 1,765, 1,073, 1,019, 793 cells; astrocytes: 275, 95, 141, 134, 58 cells; oligodendrocytes: 103, 227, 131, 282, 257, 459 cells. d , The enriched GO terms show the cell properties of the hippocampus in different cell types. Progenitors, 2,486 cells; excitatory neurons, 10,715 cells. e , Immunostaining for oligodendrocyte markers at GW16 showing the position ands morphology of oligodendrocytes in human prefrontal cortex. Scale bar, 500 μm. The experiment was repeated three times independently with similar results.
Extended Data Fig. 3 Molecular diversity of progenitors in the hippocampus.
a , Heat map showing the expression levels and identities of genes in the progenitor subclasses. Known gene expression in each type and GO enrichments are shown to the right. The graph above shows the distribution of each subclass by gestational week, and the graph below shows the subclusters of progenitors. Clusters 1–8: 204, 159, 483, 730, 397, 300, 139 and 74 cells. b , Dot plot for known markers of subtypes of progenitors in Fig. 2b . The size of each dot represents the percentage of cells in each cluster. Grey-to-blue gradient shows low-to-high gene expression. Progenitors: 204, 159, 483, 730, 397, 300, 139 and 74 cells. c , Dot plot for novel markers of subtypes of progenitors. The size of each dot represents the percentage of cells in each cluster. Grey-to-red gradient shows low-to-high gene expression. Progenitors: 204, 159, 483, 730, 397, 300, 139 and 74 cells. d , Abstracted graph shows the connection on the transcriptome of different subtypes in the developing human hippocampus. Each dot represents a single cell, and cell colour represents the cell type. e , Abstracted graph shows the connection on the transcriptome of all subtypes in the developing human hippocampus. Each dot represents a single cell, and cell colour represents the cell type. f , Abstracted graph shows the connection on the transcriptome of different weeks in the developing human hippocampus. Each dot represents a single cell, and cell colour represents the week. g , h , Visualization of eight subtypes of progenitors in the developing human hippocampus using t -SNE ( g ), and expression of known markers using the same layout ( h ). Grey, no expression; red, relative expression.
Extended Data Fig. 4 Immunostaining of progenitors in the developing hippocampus.
a , Immunofluorescence images of PAX6 and SOX2 at GW11. Scale bar, 2,000 μm. b , Immunofluorescence images of HOPX and SOX2 at GW11. Scale bar, 2,000 μm. c , Immunofluorescence images of PROX1, PAX6, HOPX and SOX2 at GW14. Scale bar, 1,000 μm. d – i , Immunofluorescence images of PROX1, PAX6, HOPX and SOX2 in GW16 ( d – f ) and GW22 ( g – i ). Scale bar, 500 μm. The experiment was repeated three times independently with similar results.
Extended Data Fig. 5 Immunostaining of developing hippocampus.
a , b , Immunofluorescence images of PAX6, HOPX and MKI67 at GW25. Scale bar, 500 μm. c , d , Cell cycle analysis of PAX6 + ( c ) or HOPX + ( d ) progenitors. e , Immunofluorescence images of PROX1 in GW25 to show granule cell layer. Scale bars, 500 μm (left); 100 μm (right, panels 1–3). f – i , Immunofluorescence images of PAX6, HOPX, NEUROD1 and GFAP at GW25. Scale bar, 500 μm. The experiment was repeated three times independently with similar results. j , k , The maturation scores of PAX6 + ( j ) and HOPX + ( k ) progenitors.
Extended Data Fig. 6 Molecular diversity of excitatory neurons in the hippocampus.
a , b , Expression of known markers ( a ) and new markers ( b ) shown using the same layout as in Fig. 3a . Grey, no expression; red, relative expression. c , Cluster dendrogram showing the modules selected to calculate the gene network in Fig. 3h . d , The cluster trees and heat map show the correlation of different gene modules in excitatory neurons.
Extended Data Fig. 7 Molecular diversity of inhibitory neurons in the hippocampus.
a , GO analysis of modules created by clustering the two main branches from the lineage tree. The analysis reflects cell fate commitment. In this heat map, the middle represents the start of pseudo-time. From this point, one lineage moves to the CA and the other moves to the DG. Rows are GO terms correlated into different modules. Sample size: 12,115 cells. b , c , Expression of known markers shown using the same layout as in Fig. 3k . d , Expression of novel markers of MGE-derived inhibitory neurons shown using the same layout as in Fig. 3k . Grey, no expression; red, relative expression. e , Expression of novel markers of CGE-derived inhibitory neurons shown using the same layout as in Fig. 3k .
Extended Data Fig. 8 Molecular diversity of microglia in the human hippocampus.
a , Heat map showing the expression levels and identities of genes in the microglia subclasses. The graph above shows the distribution of each subclass by gestational week. b , Visualization of ten subtypes of microglia in the developing human hippocampus using t -SNE. Each dot represents a single cell, and cells are laid out to show similarities. Each cell colour represents the cell type. Expression of known markers is shown using the same layout on the right; grey, no expression; red, relative expression. Microglia: 638, 489, 246, 259, 465, 229, 84, 84, 68, 54 and 44 cells. c , d , Distribution of G1, S, and G2/M stages of the cell cycle for microglia of different subtypes ( c ) and at different gestational weeks ( d ). e , Immunostaining images of PTPRC and MKI67 at GW25. Scale bars, 500 μm (left), 100 μm (right). The experiment was repeated three times independently with similar results.
Extended Data Fig. 9 NBPF family genes in the human hippocampus.
a , Expression of NBPF family genes shown using the same layout as in Fig. 1b . Grey, no expression; blue, relative expression. b , Domains of NBPF1. c , Evolutionary history inferred using the neighbour-joining method. The tree is drawn to scale, with branch lengths in the same units as those of the evolutionary distances used to infer the phylogenetic tree. The evolutionary distances were computed using the Poisson correction method and are in the units of the number of amino acid substitutions per site. The analysis involved six amino acid sequences. Evolutionary analyses were conducted in MEGA X. d , Overexpression of NBPF1 promotes DG formation at E13.5, and is observed at E15.5 in mouse. Scale bars, 500 μm. The experiment was repeated six times independently with similar results. e , Scheme depicting the position in the mouse brain at E18.5 of the slice in f . f , Overexpression of NBPF1 promotes DG formation at E13.5, and this is observed at E18.5 in mouse. Scale bars, 1,000 μm. The experiment was repeated six times independently with similar results. g , Flow chart of patch-qRT–PCR. h , Relative expression of specific genes of GFP + cells. ** P = 0.0020, * P = 0.0408, two-sided t -test; n = 10 GFP cells; 8 NBPF1–GFP cells. Mean ± s.e.m. i , Normalized ATAC-seq profiles of PROX1 in GW25 hippocampus with three independent biological replicates (Rep1, Rep2 and Rep3) showing the activation of PROX1 . The amplifying panel shows the predicted LHX2 binding sites.
Source data
Supplementary information
Supplementary Tables (download XLSX )
This file contains Supplementary Tables 1 and 2.
Reporting Summary (download PDF )
Source data
Source Data Fig. 4 (download XLSX )
Source Data Extended Data Fig. 9 (download XLSX )
Rights and permissions
Reprints and permissions
About this article
Cite this article
Zhong, S., Ding, W., Sun, L. et al. Decoding the development of the human hippocampus. Nature 577 , 531–536 (2020). https://doi.org/10.1038/s41586-019-1917-5
Download citation
Received : 04 April 2019
Accepted : 12 November 2019
Published : 15 January 2020
Version of record : 15 January 2020
Issue date : 23 January 2020
DOI : https://doi.org/10.1038/s41586-019-1917-5
Share this article
Anyone you share the following link with will be able to read this content:
Get shareable link
Sorry, a shareable link is not currently available for this article.
Copy shareable link to clipboard
Provided by the Springer Nature SharedIt content-sharing initiative
You have full access to this article via California Institute of Technology .
Advertisement
Explore content
Research articles
News
Opinion
Research Analysis
Careers
Books & Culture
Podcasts
Videos
Current issue
Browse issues
Collections
Subjects
Follow us on Facebook
Follow us on Bluesky
Follow us on X
Sign up for alerts
RSS feed
About the journal
Journal Staff
About the Editors
Journal Information
Journal Metrics
Our publishing models
Editorial Values Statement
Editorial policies
Journalistic Principles
History of Nature
Awards
Contact
Send a news tip
Publish with us
For Authors
For Referees
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
Nature ( Nature )
ISSN 1476-4687 (online)
ISSN 0028-0836 (print)
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
