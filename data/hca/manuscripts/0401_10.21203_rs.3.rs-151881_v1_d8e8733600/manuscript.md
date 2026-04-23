Single-cell profiling of human subventricular zone progenitors identifies SFRP1 as a target for stimulating progenitor activation | Research Square
Browse
Preprints
In Review Journals
COVID-19 Preprints
AJE Video Bytes
Research Tools
Research Promotion
AJE Professional Editing
AJE Rubriq
About
Preprint Platform
In Review
Editorial Policies
Our Team
Advisory Board
Help Center
Sign In
Submit a Preprint
Cite
Share
Single-cell profiling of human subventricular zone progenitors identifies SFRP1 as a target for stimulating progenitor activation
Vanessa Donega, Astrid van der Geest, Jacqueline Sluijs, Roland Van Dijk, and 4 more
This is a preprint; it has not been peer reviewed by a journal.
https://doi.org/ 10.21203/rs.3.rs-151881/v1
This work is licensed under a CC BY 4.0 License
Status:
Published
Journal Publication
published 24 Feb, 2022
Read the published version in Nature Communications →
Version 1
posted
You are reading this latest preprint version
Abstract
Following the decline of neurogenesis at birth, progenitors of the subventricular zone (SVZ) remain mostly in a quiescent state in the adult human brain. The mechanisms that regulate this quiescent state are still unclear. Here, we isolated CD271+ progenitors from the aged human SVZ for single-cell RNA sequencing analysis. Our transcriptome data revealed the identity of progenitors of the aged human SVZ as late oligodendrocyte progenitor cells. We identified the Wnt pathway antagonist SFRP1 as a possible signal that promotes quiescence of progenitors from the aged human SVZ. Administration of WAY-316606, a small molecule that inhibits SFRP1 function, stimulates activation of neural stem cells both in vitro and in vivo under homeostatic conditions. Our data unravel a possible mechanism through which progenitors of the adult human SVZ are maintained in a quiescent state and a potential target for stimulating progenitors to re-activate.
Cellular & Molecular Neuroscience
Stem Cell & Developmental Cell Biology
Adult SVZ
human progenitors
NSC quiescence
SFRP1
P57
progenitor activation
Figures
Figure 1
Figure 2
Figure 3
Figure 4
Figure 5
Figure 6
Figure 7
Figure 8
Introduction
In most mammals, neurogenesis in the dentate gyrus (DG) and subventricular zone (SVZ) continues during adulthood 1 . In rodents and non-human primates, new neurons generated in the SVZ migrate to the olfactory bulb. In humans, on the other hand, the addition of new neurons to the olfactory bulb is likely negligible 1 – 5 and new neurons produced in the SVZ migrate to the neighboring striatum 2 . Growing evidence suggests that the decline in neurogenesis observed during aging in mammals is due to increased quiescence of neural stem cells (NSCs) and progenitors 6 – 8 (hereafter progenitors refers to both NSCs and progenitors).
Studies in rodents have shown that adult NSCs arise from a population of quiescent radial glial cells that accumulate embryonically 9 , 10 . Rather than being a static non-proliferating pool of cells, studies in rodents have demonstrated that they are a very dynamic population of cells that transit between proliferative and quiescent states 11 – 13 . With aging progenitors become less plastic and remain mainly quiescent, which prevents depletion of the progenitor pool 7 . The mechanisms that regulate quiescence of progenitors are just beginning to be unraveled 6,7,14−24 . With age, the germinal niches become less neurogenic due to increased inflammatory signals and Wnt pathway antagonists, and decreased activity of the Wnt pathway 6,7,12,25−27 . Despite the decrease in neurogenic function of the aged SVZ, adult progenitors are permissive to pharmacological or genetic approaches that stimulate their neurogenic potential 7,28−30 . Furthermore, progenitors were shown to exit quiescence and re-enter the cell-cycle following ischemic injury in adult rodents 12 . Quiescent NSCs of the SVZ could be a potential source of stem cells for repair. However, the transcriptional programs that regulate quiescence of progenitors of the human brain are still unclear.
We have previously identified NGFR ( i.e. CD271) as a marker expressed by progenitors of the aged human SVZ 31 – 33 . We showed that these cells form neurospheres and can differentiate into immature neurons and glia cells in vitro 31 , 32 . The present study assesses the molecular identity of NGFR-positive progenitors from the SVZ of the aged human brain at single-cell level and investigates a new mechanism through which human progenitors could be maintained in a quiescent state. We identify the secreted frizzled-related protein-1 (SFRP1), an inhibitor of the Wnt signaling pathway, to be among genes whose expression changes over time. We demonstrate that inhibition of SFRP1 with a small molecule stimulates proliferation in vitro , in human iPSC-derived NSCs, and in vivo in early postnatal mice. Altogether, our work proposes a mechanism that maintains quiescence of progenitors of the human SVZ, which opens up future possibilities to stimulate NSCs of the human brain to promote repair.
Methods
Lead contact and materials availability
This study did not generate new unique reagents. Lead contact: [email protected]
Data availability
The single-cell RNA sequencing dataset generated in this study have been deposited in NCBI’s Gene Expression Omnibus (accession number: GSE164986). No new code was generated. All the analysis is described in the Methods. Source data are provided with this paper.
Experimental model and subject details
Animals
All animal experiments were performed in accordance to the international guidelines from the EU directive 2012/63/EU and approved by the Experimental Animal Committee Utrecht (University Utrecht, Utrecht, Netherlands) (CCD number: AVD1150020184944). Animal experiments were carried out on 2 days old (P2) wild-type C57BL/6 mice. The morning when a plug was observed is considered as E0.5 and the day of birth is defined as P0.
Human post-mortem brain tissue for single-cell RNAseq
Fresh human post-mortem dorsal SVZ including adjoining white matter tissue (n=3) (Figure S1A) was obtained from donors without known neurological or psychiatric disease from the Netherlands Brain Bank (NBB; https://www.brainbank.nl ). The NBB performs quick brain autopsies to ensure high tissue quality. Directly after autopsy, samples are placed in Hibernate-A medium (ThermoFisher Scientific, Landsmeer, The Netherlands) and were kept cold until isolation. Samples had a mean post-mortem delay of 6.35 hours (Supplementary Data 1). All donors have given informed consent to the NBB to perform autopsies for tissue isolation and access to medical records for research purposes. To ensure donor anonymity only an autopsy serial number, which is given by the NBB, is disclosed. This number contains the year that the autopsy was performed and the number of the autopsy. This study was performed according to the Dutch and European legal and ethical regulations.
Human post-mortem brain tissue for immunofluorescence
Adult post-mortem dorsal SVZ tissue from donors without known neurological disease was obtained from the NBB (Supplementary Data 2) (n=5). Material was fixed in formalin and embedded in paraffin. Fetal human brain tissue was obtained from abortion material without developmental structural chromosomal abnormalities (Supplementary Data 3) from the Chinese University of Hong Kong. Forebrain tissue was obtained from gestational week (GW) 9 (n=3), GW 16 (n=2) and GW 17 (n=2), fixed in 4%-paraformaldehyde (PFA) and embedded in paraffin. All parents of the donors have given informed consent to the use of the tissue for research. Identity of the donor is kept anonymous by the use of a serial number. This study was performed according to the Dutch, European, and Hong Kong institutional ethical regulations for the use of abortion material.
Single-cell RNA sequencing
Following single-cell sorting the plate was centrifuged at 1200 rpm for 1 min and kept at -20 o C until further processing. Sort-seq was run on single-cells as described in Muraro et al., 2016 34 , which is based on single-cell RNA sequencing by multiplexed linear amplification (Cel-Seq2 protocol from Hashimshony et al., 2012 35 ). Cells were lysed for 5 min at 65 o C, followed by dispersion of RT and second strand mixes with the Nanodrop II liquid handling platform (GC Biotech, Waddinxveen, NL). After in vitro transcription, the cDNA library was prepared according to the Cell-Seq2 protocol. The primers used consisted of 24 bp polyT stretch, a 6 bp random molecular barcode (UMI), a cell-specific 8 bp barcode, the 5’ Illumina TruSeq small RNA kit adaptor and a T7 promoter. TruSeq small RNA primers (Illumina, San Diego, CA, USA) were used for making the Illumina sequencing libraries. Sequencing was done on the Illumina NextSeq 500 platform by sequencing paired-end at 75 bp read length (25 bp from R1 and 50 bp from R2) with a sequencing depth of 15M reads per 384-well plate.
Statistical analysis
Data shown in figures 4, 5, 7, 8 and Supplemental figure 6 are expressed as mean ± SEM. Measurements were taken from distinct samples. The number of samples analyzed is stated in the figure legend. Significance was tested on GraphPad Prism 7 with two-tailed unpaired t-test, one-way ANOVA with Sidák multiple comparisons test or a two-way ANOVA with Sidák multiple comparisons test. A P-value of < 0.05 was considered statistically significant. Outliers were detected using the Grubbs test with α = 0.05.
Results
Characterization of the human SVZ at single-cell level
We have recently confirmed the progenitor identity of NGFR + ( i.e. CD271) cells 33 from the human SVZ by assessing their transcriptome and proteome signature. To further characterize the dorsal SVZ of the aged human brain at single-cell level, we isolated progenitors, astrocytes, and microglia by fluorescently labelling the different populations for CD271 (progenitors) 32 , GLT-1 (astrocytes), and CD11b (microglia), followed by FACS (Figure S1a-b). We also sorted the negative fraction. We obtained the profile of 1074 cells from the SVZ of the aged human brain. After QC-analysis, 728 cells remained for further analysis (Figure S1c-h). We performed unbiased cluster analysis using the Louvain algorithm and the Uniform Manifold Approximation and Projection (UMAP) 36 identifying seven clusters (Figure 1a and Figure S2a). Cell types clustered based on biological cell type, rather than donor or technical artefacts (Figure S1d-e). We identified three microglia clusters, viz. Microglia 1, Microglia 2, and Microglia 3 as they expressed canonical microglia markers ( e.g. CX3CR1 and AIF1 ) (Figure 1). These three clusters contained cells that were CD11b + . We identified two clusters as progenitor clusters ( i.e. Progenitors 1 and Progenitors 2), which expressed markers for progenitors ( e.g . SOX2 and SOX10 ), and lacked expression of markers for ependymal cells ( FOXJ1 and AQP4 ), radial glial cells ( HOPX ), or astrocytes ( VIM , GFAP and ALDH1A1 ) (Figure 1c). These two clusters contained the cells that were sorted based on CD271 expression and some cells from the negative fraction (Figure S1e-h). They expressed the marker for early progenitor/astrocyte CD9 12 , but did not express markers for activated progenitors NES and EGFR 23 , and neither PROM1 (not shown) or markers for late neuronal progenitors ( e.g. PAX6 and ASCL1 ). Both clusters also expressed markers for the oligodendrocyte lineage including the oligodendrocyte progenitor cell (OPC) markers SOX10 and RGCC 37 . The cluster Neuronal was negative for all the above markers, and instead, expressed SOX6 and neuronal markers ( e.g. MAP2, RBFOX1 , NRXN1 and CTNNA2 ) (Figure 1b-c and Figure S3). SOX6 is a transcription factor expressed in early OPCs, but has also been associated with the development of interneurons 37–39 . The final cluster that we identified only expressed LYZ and SPINT2 as cluster marker genes (Figure S3 and Supplementary Data 5). These two clusters only contained CD271 - CD11b - GLT1 - sorted cells.
To further substantiate the identity of the two Progenitor and the Neuronal clusters we performed Gene ontology (GO) analysis on all highly expressed genes (adj P-value < 0.01) (Supplementary Data 5) within the clusters: Progenitors 1, Progenitors 2, and Neuronal. Cluster Progenitors 1 and 2 showed enrichment for GO terms related to central nervous system development, axonogenesis, and glial cell development (Figure S2b). Cluster Neuronal showed enrichment for terms related to protein modification, cell adhesion, and glutamate receptor binding. These GO analyses corroborate the identities of the three clusters as progenitors and neuronal.
Progenitors isolated from the aged human SVZ are OPCs
As the gene signature of aged human SVZ progenitors suggested an OPC identity we compared our data to the dataset from Zhong, et al., 2018 40 and Jäkel, et al., 2019 41 . Zhong et al., isolated cells from the fetal human brain at different gestational stages and Jäkel et al., isolated white matter cells from healthy donors aged between 35 and 82 years (mean age 60 years). We used Seurat v3.2.2 to run an integrative analysis on the three datasets. This revealed several clusters including early progenitors, late progenitors, and migrating neurons (Figure 2a-c). Moreover, we observed substantial mixing of cells from the different datasets, arguing against clustering due to batch effects. Neuronal lineage clustered together, and include mostly fetal cells and mid-aged cells from Jäkel et al. Microglia from our dataset clustered with microglia from the two other studies. Cells from the OPC lineage from our dataset formed clusters with OPC lineage cells from Jäkel et al., and fetal OPCs (Figure 2a-b and Supplementary Data 6). We next performed clustering analysis on cells from the OPC lineage only, which revealed seven subclusters (Figure 2d-e). These subclusters corresponded to early OPCs ( PDGFRA and SOX6 ), late OPCs ( SOX10 and SOX2 ), and oligodendrocytes ( KLK6 and OPALIN ) (Figure 2f). Our analysis showed that from the 395 progenitor cells that we analyzed, 138 cells corresponded to late OPCs and the remaining cells to oligodendrocytes (Supplementary Data 6). We performed SOX10 immunofluorescence staining on post-mortem human brain tissue, which showed that only a few SOX2 progenitors in the SVZ are SOX10 positive (Figure S4).
Increased expression of cell cycle inhibitors in OPCs from the aged human SVZ
Analysis of the expression of a panel of markers for the oligodendroglial cell lineage further confirmed the OPC identity of the CD271 + progenitor cells (Figure 3a). We next identified genes that were differentially expressed over time using Monocle3 v0.2.3.0 (Supplementary Data 7). One of the genes that was differentially expressed over time was SFRP1, which increased in expression with age (Supplementary Data 7 and Figure 3c). SFRP1 is an antagonist of the Wnt pathway, thereby inhibiting cell proliferation 42,43 . This is interesting as the mechanisms that regulate quiescence of progenitors from the human SVZ are unclear. Therefore, we compared the expression of several proliferation and cell cycle markers in fetal, mid-aged, and aged OPC lineage cells. As expected, markers for proliferation and cell cycle progression were mostly absent in the mid-aged and aged OPC lineage cells (Figure 3b), while markers for quiescence and cell cycle arrest were highly expressed in mid-aged and aged OPC lineage cells, in particular CDKN1B ( i.e. P27 ), CDKN1C ( i.e. P57 ) and SFRP1 (Figure 3c).
Cell cycle inhibitors are expressed in the aged human SVZ
P57 is a known marker for stem cell quiescence in rodents 9,24 and SFRPs are a family of biphasic regulators of Wnt signaling expressed in the nucleus or cytoplasm of the cell 42–44 . SFRP1 is mainly expressed in late OPCs (Figure 4b) and is the only member of the SFRP family that is expressed in aged OPCs (Figure S5a). In contrast, P57 is expressed in both late OPCs as well as oligodendrocytes (Figure 4a). To characterize the expression pattern of both P57 and SFRP1 in the aged SVZ, we performed immunofluorescence staining on post-mortem human brain tissue (Supplementary Data 2). In the aged SVZ around 25% of SFRP1 + cells in the SVZ expressed SOX2 (Figure 4c-d). SFRP1 expression is not limited to progenitors, as it is also highly expressed in ependymal cells, cortical neurons (Figure S6a) and OLIG2 + cells in the SVZ (Figure S6b-c). While SFRP1 is expressed in the nucleus of progenitors (Figure 4c) and ependymal cells, it is also expressed in the cytoplasm of neurons (Figure S6a).
SFRP1 inhibits the Wnt pathway by binding to Wnt ligands and by directly binding to β-catenin in the nucleus 42 . To determine whether SFRP1 expression correlated with a quiescent state, we assessed the expression of P57 in SFRP1 + cells in the SVZ only. Our results showed that around 78% of the SFRP1 + cells in the SVZ expressed P57 (Figure 4e-f). The majority of P57 + cells were positive for SFRP1 (87.81 ± 10.39, not shown). This suggests that in the adult SVZ, SFRP1 is mostly expressed by quiescent/primed-quiescent stem cells. We confirmed that SFRP1 is also expressed by post-mitotic progenitors of the fetal human brain at nine gestational weeks (Figure 4g). Immunofluorescence staining of SFRP1 expression in the SVZ from aged, mid-aged, and fetal post-mortem brain shows an increase in the number of SFRP1 + cells from mid-aged (mean age of 61 years) to aged (mean age of 91 years) (Figure 4h) and from GW9 to GW16-17 (Figure 4i). We also confirmed in our bulk RNAseq dataset 32 that SFRP1 has the highest expression from the SFRP family members, in both CD271 + cells and SVZ homogenate isolated from post-mortem brain tissue from healthy donors (Figure S5b).
Inhibition of SFRP1 stimulates proliferation in iPSC-derived NSCs
A previous study showed that proliferation and differentiation increases during early corticogenesis in Sfrp1 -/- mouse embryos 43 . Therefore, we assessed the effect of inhibiting SFRP1 function on proliferation of human NSCs by using a human iPSC-derived neural stem cell line to model human NSCs in vitro . This was done with the small molecule WAY-316606, which is known to sequester SFRP1 in vitro . This molecule prevents SFRP1 from binding to Wnt ligands, thereby stimulating the Wnt pathway 45 . We first confirmed the expression of SFRP1 protein in human iPSC-derived NSCs (Figure 5a). Most cells expressed SFRP1 protein in the cytoplasm and nucleus, while in some cells cytoplasmic expression was absent. Sequestration of SFRP1, stimulated proliferation of iPSC-derived NSCs 72 hours after stimulation in vitro (Figure 5b-e). This effect is dosage-dependent (not shown). Stimulation with WAY increased the number of cells by two fold (Figure 5b). While we observed an increase in SOX2 + cells, the percentage of KI67 + iPSC-derived NSCs did not increase when compared to control condition (Figure 5d-f). Our data therefore, suggest that, this increase in cell number is mediated by a shortening of the cell cycle rather than an increase in cell activation. This can be explained by the fact that iPSC-derived NSCs do not exit the cell cycle, and instead remain actively cycling. To confirm that the observed effect is mediated by increased activity of the canonical Wnt pathway we performed a Topflash luciferase reporter assay on HEK293 cells. Our results confirmed that the small molecule WAY-316606 activates the canonical WNT pathway through inhibition of SFRP1 (Fig S7). WAY-316606 acts specifically on SFRP1 and does not activate the Wnt pathway when in presence of SFRP5, an SFRP isoform that promotes NSC quiescence in the mouse SVZ 7 .
SFRP1 is expressed in the postnatal mouse brain
To determine whether SFRP1 inhibition also stimulates proliferation of progenitors in vivo , we first assessed the expression pattern of SFRP1 over time in the embryonic and postnatal mouse brain. In situ hybridization (ISH) data from Allen Brain Atlas showed a gradual increase in SFRP1 expression from E11.5 to E18.5 (Figure 6a). During the embryonic period, SFRP1 is mainly expressed in the germinal regions. Following birth, SFRP1 expression decreases in the SVZ, while increasing in regions outside the SVZ. We confirmed the ISH data by performing immunofluorescence staining for SFRP1 on P1 and P67 mouse brains. This showed expression of SFRP1 in the SVZ, striatum, and cortex in P1 mouse brain (Figure 6b-d), and a strong decrease in SFRP1 expression in the SVZ in P67 mouse brains (Figure 6e-g). Kalamakis et al., 2019 7 showed that from all members of the SFRP family, only SFRP5 expression increased with time in the mouse SVZ, while SFRP1 expression decreased (Figure S5c). Thus, in contrast to the expression pattern of SFRP1 in the human SVZ, its expression is highest in the early postnatal mouse SVZ.
Inhibition of SFRP1 promotes proliferation and differentiation through stimulation of the Wnt and Notch pathways
Previous studies showed that SFRPs are multifunctional proteins that regulate both Wnt and Notch signalling 42,43 , through which they regulate dopamine neuron development 46 and cortical expansion 43 . We first assessed whether inhibiting SFRP1 function increased activation of the Wnt and Notch pathways in vivo . SFRP1 was prevented from binding to Wnt ligands by the administration of the small molecule WAY-316606 to two days old mouse pups. We assessed this in the early postnatal mouse brain, as SFRP1 levels are highest in the SVZ at this age (Figure 6, Figure S5c). The entire SVZ was dissected 72 hours after treatment with WAY-316606 for RT-PCR analysis, focusing on Wnt and Notch pathway related genes. Our results show a 3.5-fold increase in Cyclin d1 ( Ccnd1 ) (P = 0.0079) , which promotes cell proliferation 47 (Figure 7a). p57 ( Cdkn1c ) expression did not change (P = 0.4812). Moreover, some key genes of the Wnt signaling ( Fzd7 P = 0.0025, Ctnnb1 P = 0.0203, and Lef1 P = 0.0497) and the Notch signaling ( Hes5 P = 0.0131, and Nrarp P = 0.0041) were also increased following administration of the small molecule WAY-316606 (Figure 7a). Administration of WAY also enhanced the expression of Dcx (P = 0.0007) and CNPase (P = 0.0466) genes, suggesting increased specification towards neuronal and OPC lineages (Figure 7b).
Sequestration of SFRP1 increases activation of progenitors in the mouse SVZ
We next determined whether WAY-316606 administration would stimulate progenitor proliferation also in vivo . To determine if inhibiting the function of SFRP1 increases the number of GFP + cells and their migration away from the SVZ, we specifically labelled progenitors from the dSVZ by dorsal electroporation of a GFP plasmid at P2 and terminated the pups 72 hours after administration of WAY-316606. Our results show a 1.6-fold increase in the number of GFP + cells in the dSVZ (Figure 8a-b). We did not see a significant increase in migration towards the cortex, nor to the olfactory bulb (not shown). The increase in the number of GFP + cells in the dSVZ correlated with a 2-fold increase in proliferating cells in the dSVZ (Figure 8c-d). There was also a 1.6-fold increase in Ki67 + cells in the lSVZ (Figure 8c-d). Our results show that while the number of Sox2 + progenitors remains constant in the lSVZ, and increases with 2-fold in the dSVZ, there was a 3-fold decrease in the mSVZ after administration of WAY-316606 (Figure 8e-f). There was a significant increase in the number of Olig2 + cells in both the dorsal and lateral SVZ (Figure 8g-h).
Discussion
Although NSCs are present in the adult human SVZ, few neurons are generated after birth 2 , 4 . NSCs of the rodent SVZ become increasingly quiescent during aging. Studies in rodents suggest that NSC quiescence is regulated by both intrinsic and extrinsic factors ( e.g . inflammatory signaling in the SVZ) 7,14−24 . The molecular mechanisms that maintain progenitors of the adult human brain quiescent are still unclear. Here, we identify SFRP1, an inhibitor of the canonical Wnt pathway, as a potential target to stimulate progenitor proliferation and differentiation in the adult human SVZ. We show both in vitro , in a human iPSC-derived NSC line, and in vivo , in mice, that inhibiting SFRP1 function with the administration of WAY-316606 increases activation of progenitors, likely by stimulating the activity of both Wnt and Notch pathways. Our work identifies the Wnt antagonist SFRP1 as a potential signal that maintains quiescence of progenitors of the aged human SVZ.
Interestingly, we show that progenitors from the adult human SVZ are primed towards the oligodendroglial lineage, as genes from this lineage are highly expressed, while canonical markers of the neuronal lineage are practically absent. Integration of our data with published datasets from the fetal forebrain 40 and adult white matter 41 , revealed the CD271 + cells to be late OPCs. We cannot exclude that CD271 may label a subpopulation of progenitors in the human SVZ. It is likely that human progenitors of the SVZ are heterogeneous as in the rodent SVZ, where progenitors differ in their lineage specificity depending on their location within the SVZ 48 , 49 . A previous study suggested that CD271 is expressed specifically in OPCs following demyelinating brain injuries in both humans and rodents 50 . Therefore, we cannot conclude, based on our current results, that either early OPCs or NSCs are absent from the aged human SVZ.
The turnover rate of oligodendrocytes stabilizes around five years of age and remains low throughout the human lifespan 51 . Our results indicate that this low turnover rate is not caused by the absence of OPCs in the SVZ, but rather due to increased quiescence. Here, we identified SFRP1, a Wnt pathway antagonist, as a possible signal that maintains late OPCs in a quiescent state in the human SVZ. SFRP expression is not restricted to NSCs, but is also expressed by astrocytes 52 and microglia 53 . Two other members of the SFRP family, SFRP3 and SFRP5, were shown to regulate NSC quiescence in the mouse brain. SFRP3 maintains NSCs in a quiescent state in the dentate gyrus 54 of adult mice and its deletion increases NSC activation and maturation. SFRP5 was shown to maintain NSCs of the aged mouse SVZ quiescent and when blocked by the administration of antibodies, activation of aged NSCs was increased 7 . Neither SFRP3 nor SFRP5 are expressed in our datasets (Figure S5) 32 , suggesting species-specific differences in expression profile. Indeed, our data show that while in humans, SFRP1 expression in the SVZ increases with age, its expression decreases in young adult mice. Hence, SFRP1 could be the human homologue of SFRP5 in regulating NSC quiescence in the aged human SVZ.
The mechanisms through which SFRPs modulate the canonical Wnt pathway to maintain cells in a quiescent state are still unclear. Growing evidence suggests that members of the SFRP family function as tumor suppressor genes, as they are lowly expressed in different types of tumors, including meduloblastoma 55 – 57 . Methylation of the promoter region of SFRP , results in its decreased expression, which correlates to increased malignancy 56 . Indeed, low levels of SFRP1 have been shown to increase proliferation in different tumor cell lines 55 . A recent study proposed a Wnt-independent mechanism in which nuclear SFRP1, 2, and 5 directly bind to β-catenin, thus inhibiting its transcriptional activity and the expression of cancer stem cell related genes 41 . We show that inhibition of SFRP1, by the administration of WAY-316606, stimulates proliferation and differentiation of NSCs both in vitro and in vivo by activation of the canonical Wnt pathway. The luciferase Topflash reporter assay also shows that WAY-316606 acts specifically on SFRP1 and does not activate the canonical Wnt pathway when in the presence of SFRP5. These results are also supported by a study where bone formation was stimulated through sequestration of SFRP1 with WAY-316606 58 showing that WAY-316606 inhibits SFRP1 activity with 40%, while SFRP2 and SFRP5 activities were only decreased by 2 to 5%. All together, these data suggest that the small molecule WAY-316606 promotes the activity of the canonical Wnt pathway through inhibition of the Wnt antagonist SFRP1.
In conclusion, our work identifies SFRP1 as a potential signal that maintains progenitors of the aged human SVZ in a quiescent state, supporting the possibility to re-activate progenitors of the aged human brain to regenerate the brain following injury or neurodegenerative diseases.
Declarations
Acknowledgments
This work was supported by an Off-road grant to V.D, a TAS-ZonMw grant (40-41400-98-16020) to E.M.H, by the MAXOMOD consortium, under the frame of E-Rare-3, the ERANET for Research on Rare Diseases to R.J.P, and a Ministry of Science and Technology of China (MOST, 2016YFC1000500), a Theme-based Research Scheme (TRS, T13-602/21-N), a Health and Medical Research Fund (01120156) and CUHK Direct Grant (2019.052) to C.C.W. We are grateful to Peter Burbach for discussions and comments on the manuscript. We thank Christiaan van der Meer, Youri Adolfs, Roger Koot and Nina Chu for technical support. The single-cell RNA sequencing was performed at Single Cell Discoveries by Judith Vivié and Mauro Muraro.
Contributions
V.D. conceived and designed the study, performed and analyzed the single-cell RNAseq and mouse experiments. A.G. performed and analyzed in vitro experiments. J.A.S. performed Luciferase reporter assay. R.E.D. performed FACS. C.C.W. provided fetal brain tissue. O.B. provided the protocol for single-cell sorting and performed alignment of the sequenced data. V.D. wrote the manuscript with input from E.M.H., R.J.P, O.B. and C.C.W. All authors revised and approved the manuscript.
Conflict of interests: The authors declare no conflicts of interests.
References
Kempermann, G. et al. Human Adult Neurogenesis: Evidence and Remaining Questions. Stem Cell 23 , 1–6 (2018). doi: 10.1016/j.stem.2018.04.004
Ernst, A. et al. Neurogenesis in the Striatum of the Adult Human Brain. Cell 156 , 1072–1083 (2014).
Ernst, A. & Frisén, J. Adult Neurogenesis in Humans- Common and Unique Traits in Mammals. PLOS Biol. 13 , e1002045 (2015).
Bergmann, O. et al. The Age of Olfactory Bulb Neurons in Humans. Neuron 74 , 634–639 (2012).
Sanai, N. et al. Corridors of migrating neurons in the human brain and their decline during infancy. Nature 478 , 382–386 (2011).
Silva-Vargas, V., Maldonado-Soto, A. R., Mizrak, D., Codega, P. & Doetsch, F. Age-Dependent Niche Signals from the Choroid Plexus Regulate Adult Neural Stem Cells. Cell Stem Cell 19 , 643–652 (2016).
Kalamakis, G. et al. Quiescence Modulates Stem Cell Maintenance and Regenerative Capacity in the Aging Brain. Cell 176 , 1407–1419.e14 (2019).
Leeman, D. S. et al. Lysosome activation clears aggregates and enhances quiescent neural stem cell activation during aging. Science (80-.). 359 , 1277–1283 (2018).
Furutachi, S. et al. Slowly dividing neural progenitors are an embryonic origin of adult neural stem cells. Nat Neurosci 18 , 657–665 (2015).
Fuentealba, L. C. et al. Embryonic Origin of Postnatal Neural Stem Cells. Cell 161 , 1644–1655 (2015).
Basak, O. et al. Troy + brain stem cells cycle through quiescence and regulate their number by sensing niche occupancy. Proc. Natl. Acad. Sci. U. S. A. 115 , E610–E619 (2018).
Llorens-Bobadilla, E. et al. Single-Cell Transcriptomics Reveals a Population of Dormant Neural Stem Cells that Become Activated upon Brain Injury. Cell Stem Cell 17 , 329–340 (2015).
Obernier, K. et al. Adult Neurogenesis Is Sustained by Symmetric Self-Renewal and Differentiation. Cell Stem Cell 22 , 221–234 (2018). doi: 10.1016/j.stem.2018.01.003
Zywitza, V., Misios, A., Bunatyan, L., Willnow, T. E. & Rajewsky, N. Single-Cell Transcriptomics Characterizes Cell Types in the Subventricular Zone and Uncovers Molecular Defects Impairing Adult Neurogenesis. Cell Rep. 25 , 2457–2469 (2018).
Zelentsova, K. et al. Protein S Regulates Neural Stem Cell Quiescence and Neurogenesis. Stem Cells 35 , 679–693 (2017). doi: 10.1002/stem.2522
Borrett, M. J. et al. Single-Cell Profiling Shows Murine Forebrain Neural Stem Cells Reacquire a Developmental State when Activated for Adult Neurogenesis. Cell Rep. 32 , 108022 (2020).
Hirabayashi, Y. et al. Polycomb Limits the Neurogenic Competence of Neural Precursor Cells to Promote Astrogenic Fate Transition. Neuron 63 , 600–613 (2009).
Nieto-González, J. L. et al. Loss of postnatal quiescence of neural stem cells through mTOR activation upon genetic removal of cysteine string protein-α. Proc. Natl. Acad. Sci. U. S. A. 116 , 8000–8009 (2019).
Sueda, R., Imayoshi, I., Harima, Y. & Kageyama, R. High Hes1 expression and resultant Ascl1 suppression regulate quiescent vs. active neural stem cells in the adult mouse brain. Genes Dev. 33 , 511–523 (2019).
Leeman, D. S. et al. Lysosome activation clears aggregates and enhances quiescent neural stem cell activation during aging. Science 359 , 1277–1283 (2018).
Otsuki, L. & Brand, A. H. Dorsal-Ventral Differences in Neural Stem Cell Quiescence Are Induced by p57KIP2/Dacapo. Dev. Cell 49 , 293–300.e3 (2019).
Otsuki, L. & Brand, A. H. Cell cycle heterogeneity directs the timing of neural stem cell activation from quiescence. Science 360 , 99–102 (2018).
Codega, P. et al. Prospective Identification and Purification of Quiescent Adult Neural Stem Cells from Their In Vivo Niche. Neuron 82 , 545–559 (2014).
Furutachi, S., Matsumoto, A., Nakayama, K. I. & Gotoh, Y. P57 Controls Adult Neural Stem Cell Quiescence and Modulates the Pace of Lifelong Neurogenesis. EMBO J. 32 , 970–981 (2013).
Marchetti, B. et al. Parkinson’s disease, aging and adult neurogenesis: Wnt/β-catenin signalling as the key to unlock the mystery of endogenous brain repair. Aging Cell 19 , 1–41 (2020).
Nicaise, A. M., Willis, C. M., Crocker, S. J. & Pluchino, S. Stem Cells of the Aging Brain. Front. Aging Neurosci. 12 , 1–23 (2020).
Belenguer, G. et al. Adult Neural Stem Cells Are Alerted by Systemic Inflammation through TNF-α Receptor Signaling. Cell Stem Cell 1–15 (2020).
Azim, K. et al. Pharmacogenomic identification of small molecules for lineage specific manipulation of subventricular zone germinal activity. PLoS Biol. 15 , 1–27 (2017).
Bragado Alonso, S. et al. An increase in neural stem cells and olfactory bulb adult neurogenesis improves discrimination of highly similar odorants. EMBO J. 38 , 1–13 (2019).
Van Den Berge, S. A. et al. The proliferative capacity of the subventricular zone is maintained in the parkinsonian brain. Brain 134 , 3249–3263 (2011).
van Strien, M. E. et al. Isolation of Neural Progenitor Cells From the Human Adult Subventricular Zone Based on Expression of the Cell Surface Marker CD271. Stem Cells Transl. Med. 3 , 470–480 (2014).
Donega, V. et al. Transcriptome and proteome profiling of neural stem cells from the human subventricular zone in Parkinson’s disease. Acta Neuropathol. Commun. 7 , 84 (2019).
Muraro, M. J. et al. A Single-Cell Transcriptome Atlas of the Human Pancreas. Cell Syst. 3 , 385–394.e3 (2016).
Hashimshony, T., Wagner, F., Sher, N. & Yanai, I. CEL-Seq: Single-Cell RNA-Seq by Multiplexed Linear Amplification. Cell Rep. 2 , 666–673 (2012).
Butler, A., Hoffman, P., Smibert, P., Papalexi, E. & Satija, R. Integrating single-cell transcriptomic data across different conditions, technologies, and species. Nat. Biotechnol. 36 , 411–420 (2018).
Marques, S. et al. Oligodendrocyte heterogeneity in the mouse juvenile and adult central nervous. Science 352 , 1326 (2016).
Batista-Brito, R. et al. The Cell-Intrinsic Requirement of Sox6 for Cortical Interneuron Development. Neuron 63 , 466–481 (2009).
Azim, E., Jabaudon, D., Fame, R. M. & MacKlis, J. D. SOX6 controls dorsal progenitor identity and interneuron diversity during neocortical development. Nat. Neurosci. 12 , 1238–1247 (2009).
Panman, L. et al. Sox6 and Otx2 control the specification of substantia nigra and ventral tegmental area dopamine neurons. Cell Rep. 8 , 1018–1025 (2014).
Zhong, S. et al. A single-cell RNA-seq survey of the developmental landscape of the human prefrontal cortex. Nature 555 , 524–528 (2018).
Jäkel, S. et al. Altered human oligodendrocyte heterogeneity in multiple sclerosis. Nature 566 , 543–547 (2019).
Liang, C.-J. et al. SFRPs Are Biphasic Modulators of Wnt-Signaling-Elicited Cancer Stem Cell Properties beyond Extracellular Control. Cell Rep. 28 , 1511–1525.e5 (2019).
Esteve, P., Crespo, I., Kaimakis, P., Sandonís, A. & Bovolenta, P. Sfrp1 modulates cell-signaling events underlying telencephalic patterning, growth and differentiation. Cereb. Cortex 29 , 1059–1074 (2019).
Shimogori, T., VanSant, J., Paik, E. & Grove, E. A. Members of the Wnt, Fz, and Frp Gene Families Expressed in Postnatal Mouse Cerebral Cortex. J. Comp. Neurol. 473 , 496–510 (2004).
Hawkshaw, N. J. et al. Identifying novel strategies for treating human hair loss disorders: Cyclosporine A suppresses the Wnt inhibitor, SFRP1, in the dermal papilla of human scalp hair follicles. PLoS Biol. 16 , 1–17 (2018).
Kele, J. et al. SFRP1 and SFRP2 dose-dependently regulate midbrain dopamine neuron development in vivo and in embryonic stem cells. Stem Cells 30 , 865–875 (2012).
Lange, C., Huttner, W. B. & Calegari, F. Cdk4/CyclinD1 Overexpression in Neural Stem Cells Shortens G1, Delays Neurogenesis, and Promotes the Generation and Expansion of Basal Progenitors. Cell Stem Cell 5 , 320–331 (2009).
Mizrak, D. et al. Single-Cell Analysis of Regional Differences in Adult V-SVZ Neural Stem Cell Lineages. Cell Rep. 26 , 394–406.e5 (2019).
Merkle, F. T., Mirzadeh, Z. & Alvarez-buylla, A. Mosaic organization of neural stem cells in the adult brain. Science 317 , 381–4 (2007).
Petratos, S. et al. Expression of the low-affinity neurotrophin receptor, p75NTR, is upregulated by oligodendroglial progenitors adjacent to the subventricular zone in response to demyelination. Glia 48 , 64–75 (2004).
Yeung, M. S. Y. et al. Dynamics of oligodendrocyte generation and myelination in the human brain. Cell 159 , 766–774 (2014).
Rueda-Carrasco, J. et al. Astrocyte to microglia cross-talk in acute and chronic neuroinflammation is shaped by SFRP1. bioRxiv (2020). doi: 10.1101/2020.03.10.982579
Esteve, P. et al. Elevated levels of Secreted-Frizzled-Related-Protein 1 contribute to Alzheimer’s disease pathogenesis. Nat. Neurosci. 22 , 1258–1268 (2019).
Jang, M. H. et al. Secreted frizzled-related protein 3 regulates activity-dependent adult hippocampal neurogenesis. Cell Stem Cell 12 , 215–223 (2013).
Kongkham, P. N. et al. The SFRP family of WNT inhibitors function as novel tumor suppressor genes epigenetically silenced in medulloblastoma. Oncogene 29 , 3017–3024 (2010).
Dahl, E. et al. Frequent loss of SFRP1 expression in multiple human solid tumours: Association with aberrant promoter methylation in renal cell carcinoma. Oncogene 26 , 5680–5691 (2007).
Suzuki, H. et al. Epigenetic inactivation of SFRP genes allows constitutive WNT signaling in colorectal cancer. Nat. Genet. 36 , 417–422 (2004).
Bodine, PVN. et al. A small molecule inhibitor of the Wnt antagonist secreted frizzled-related protein-1 stimulates bone formation. Bone 44 , 1063–1068 (2009).
Additional Declarations
There is NO Competing Interest.
Supplementary Files
SupplementaryData1.xlsx
Supplementary Data 1
SupplementaryData2.xlsx
Supplementary Data 2
SupplementaryData3.xlsx
Supplementary Data 3
SupplementaryData4.xlsx
Supplementary Data 4
SupplementaryData5.xlsx
Supplementary Data 5
SupplementaryData6.xlsx
Supplementary Data 6
SupplementaryData7.xlsx
Supplementary Data 7
SupplementalFig1.tif
Supplemental Figure 1
SupplementalFig2.tif
Supplemental Figure 2
SupplementalFig3.tif
Supplemental Figure 3
SupplementalFig4.tif
Supplemental Figure 4
SupplementalFig5.tif
Supplemental Figure 5
SupplementalFig6.tif
Supplemental Figure 6
SupplementalFig7.tif
Supplemental Figure 7
RS.pdf
SourceData.xlsx
Source Data
DescriptionofadditionalSupplementaryfiles.docx
SupplementaryMethodsandFigures.doc
Supplementary Methods and Figures
Cite
Share
Status:
Published
Journal Publication
published 24 Feb, 2022
Read the published version in Nature Communications →
Version 1
posted
You are reading this latest preprint version
Research Square lets you share your work early, gain feedback from the community, and start making changes to your manuscript prior to peer review in a journal.
As a division of Research Square Company, we’re committed to making research communication faster, fairer, and more useful. We do this by developing innovative software and high quality services for the global research community. Our growing team is made up of researchers and industry professionals working together to solve the most critical problems facing scientific publishing.
Also discoverable on
Platform
About
Our Team
In Review
Editorial Policies
Advisory Board
Help Center
Resources
Author Services
Accessibility
API Access
RSS feed
Manage Cookie Preferences
© Research Square 2026 | ISSN 2693-5015 (online)
Privacy Policy Terms of Service Do Not Sell My Personal Information
