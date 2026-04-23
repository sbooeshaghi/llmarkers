Single-cell analysis of endometriosis reveals a coordinated transcriptional programme driving immunotolerance and angiogenesis across eutopic and ectopic tissues | Nature Cell Biology
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
Single-cell analysis of endometriosis reveals a coordinated transcriptional programme driving immunotolerance and angiogenesis across eutopic and ectopic tissues
Resource
Published: 21 July 2022
Single-cell analysis of endometriosis reveals a coordinated transcriptional programme driving immunotolerance and angiogenesis across eutopic and ectopic tissues
Yuliana Tan ORCID: orcid.org/0000-0002-5923-2215 1 , 2 ,
William F. Flynn ORCID: orcid.org/0000-0001-6533-0340 1 ,
Santhosh Sivajothi 1 ,
Diane Luo 1 ,
Suleyman B. Bozal 1 ,
Monica Davé ORCID: orcid.org/0000-0002-6277-1535 1 , 2 ,
Anthony A. Luciano 3 ,
Paul Robson ORCID: orcid.org/0000-0002-0191-3958 1 , 2 , 4 ,
Danielle E. Luciano ORCID: orcid.org/0000-0003-2484-5123 3 &
…
Elise T. Courtois ORCID: orcid.org/0000-0002-8749-2719 1
Nature Cell Biology volume 24 , pages 1306–1318 ( 2022 ) Cite this article
24k Accesses
167 Citations
58 Altmetric
Subjects
Inflammatory diseases
Multihormonal system disorders
Transcriptomics
An Author Correction to this article was published on 29 September 2022
This article has been updated
Abstract
Endometriosis is characterized by the growth of endometrial-like tissue outside the uterus. It affects many women during their reproductive age, causing years of pelvic pain and potential infertility. Its pathophysiology remains largely unknown, which limits early diagnosis and treatment. We characterized peritoneal and ovarian lesions at single-cell transcriptome resolution and compared them to matched eutopic endometrium, unaffected endometrium and organoids derived from these tissues, generating data on over 122,000 cells across 14 individuals. We spatially localized many of the cell types using imaging mass cytometry. We identify a perivascular mural cell specific to the peritoneal lesions, with dual roles in angiogenesis promotion and immune cell trafficking. We define an immunotolerant peritoneal niche, fundamental differences in eutopic endometrium and between lesion microenvironments and an unreported progenitor-like epithelial cell subpopulation. Altogether, this study provides a holistic view of the endometriosis microenvironment that represents a comprehensive cell atlas of the disease in individuals undergoing hormonal treatment, providing essential information for future therapeutics and diagnostics.
You have full access to this article via California Institute of Technology .
Similar content being viewed by others
Single-cell transcriptomic analysis of endometriosis
Article 09 January 2023
Mapping the temporal and spatial dynamics of the human endometrium in vivo and in vitro
Article Open access 02 December 2021
Single-cell transcriptomic analysis highlights origin and pathological process of human endometrioid endometrial carcinoma
Article Open access 22 October 2022
Main
Endometriosis is an inflammatory gynaecological condition that affects 10% of women of reproductive age worldwide 1 , 2 , with symptoms including pelvic pain and infertility. It is characterized by the presence of endometrium-like tissue outside the uterine cavity (termed lesions), commonly found within the peritoneal cavity, as superficial peritoneal or ovarian lesions. Despite the first description of endometriosis occurring almost a century ago, the exact aetiology and molecular drivers of the disease remain largely unknown. Limited non-invasive diagnostic tools impede early detection, resulting in delays of up to 7 years from onset of symptoms to definitive diagnosis, which currently requires invasive surgical biopsies of lesions. Treatment of endometriosis remains similarly challenging, relying on hormonal therapy often in conjunction with surgery. Oral contraceptives aim to reduce symptoms but do not necessarily promote lesion clearance. Even after excision, lesions often recur and repeated surgery is frequent 3 .
Challenges in diagnoses and treatment are, at least in part, due to a poor understanding of the pathophysiology of—and heterogeneity within—endometriosis. The tissue microenvironment, including immune cells, has been highlighted as a critical factor for normal endometrium development and endometriosis progression 4 , 5 , 6 , 7 , 8 . Advancements in single-cell RNA sequencing (scRNA-seq) and organoid culture systems enable interrogation of the dynamic interactions within the endometrial microenvironment and the cellular complexity and heterogeneity present in endometriosis. Recent studies have demonstrated the power of such cutting-edge technologies to characterize the dynamic changes of the human endometrium through the menstrual cycle and pregnancy 5 , 6 , 7 , 8 .
Here, we profile the transcriptomes of endometrium and endometriotic lesions using scRNA-seq and hyperplexed antibody imaging. Our study included individuals receiving oral contraceptive treatment, the most common medical therapy for endometriosis. Consequently, we sought to understand changes within the endometrium and in endometriotic lesions during treatment. The profiling of eutopic endometrium, peritoneal and ovarian lesions, and human-derived organoids uncovered distinct cellular changes in endometriosis endometrium as well as specific subsets of immunomodulatory macrophages, immunotolerant dendritic cells (DCs) and vascular changes specific to endometriosis. Our data highlight an unreported endometriosis-specific perivascular population, the presence of tertiary lymphoid structures in some lesions and a progenitor-like epithelial cell population that may be crucial for a deeper understanding of this disease.
Results
scRNA-seq and imaging mass cytometry tissue analysis
scRNA-seq was performed on biopsies from 14 individuals. Healthy eutopic endometrium (Ctrl) represented samples from individuals without endometriosis. Eutopic endometrium (EuE), ectopic peritoneal lesions (EcP) and the adjacent regions to these (EcPA), and ectopic ovarian lesions (EcO) were collected from individuals with revised American Society for Reproductive Medicine stage II–IV endometriosis. The majority of participants were receiving similar hormonal treatment (Fig. 1a , Extended Data Fig. 1a and Supplementary Tables 1 and 2 ). EcPA was included to study the environment where lesions establish and evolve.
Fig. 1: scRNA-seq from Ctrl and endometriosis samples.
The alternative text for this image may have been generated using AI.
Full size image
a , Schematic (top) and photographic (bottom) representation of collected tissue biopsy samples. Ctrl specimens were obtained from eutopic endometrium of individuals without endometriosis. EuE, EcP, EcPA and EcO samples were obtained from individuals with endometriosis. Peritoneal lesions were collected with a surrounding margin of up to 1 cm 2 . The margin (EcPA) was separated following macroscopic tissue assessment from the lesion (EcP) when possible and before single-cell dissociation, as depicted in the representative image for one of the biopsy samples. b , Diagram showing scRNA-seq metrics per person (left) and tissue type (right) after quality control. These metrics indicate unique molecular identifier (UMIs) and total genes per cells across participants and tissue types. The cord diagram (centre) represents each individual (C, Ctrl; E, endometriosis) in each tissue type. c , Violin plot of the marker gene expression for each major cell type identified in the scRNA-seq dataset. d , Uniform manifold approximation and projection (UMAP) plot showing the 108,497 single cells from Ctrl and endometriosis tissues. Five major cell types are identified (centre UMAP plot) and subsequently subclustered into 58 subpopulations (radial UMAP plots). Each subpopulation was identified using marker genes curated form the literature. The presence of basophils and neutrophils (arrow) indicate that the cell recovery workflow was well suited to capture delicate cell types known to be easily lost during tissue dissociation. e , Diagram showing the number of major cell types (bar plot) and the cell-type proportion in each tissue type (heatmap). Cell proportions are indicated within each square. Unique combinations of cell markers from each major cell cluster were used to design an IMC panel. f , g , Assigned colours from e represent each major cell type identified in EcP ( f ) and EcO ( g ). White arrowheads indicate endometriotic-like epithelial glands. Scale bar, 100 µm.
In total, 108,497 cellular transcriptomes were generated from tissues, with a median 9,186 unique transcripts and 2,823 genes per cell (Fig. 1b ). Cells were assigned to five overarching cell types: epithelial, stromal, endothelial, lymphocyte and myeloid (Fig. 1c,d and Extended Data Fig. 1b ). Subsequent subclustering identified 58 subpopulations (Fig. 1d and Supplementary Table 3 ), which highlights the cellular complexity of both the endometrium and ectopic lesions. We compared bulk transcriptomes from undissociated tissue to pseudo-bulk single-cell transcriptomes to interrogate potential biases (Extended Data Fig. 1a ). These showed a strong correspondence within each tissue type (Extended Data Fig. 1c,d ). However, differential expression analysis indicated a few expected cell types that are under-represented in our single-cell dataset (Extended Data Fig. 1e and Supplementary Table 4 ). Nevertheless, the similarities between the bulk and single-cell transcriptomes indicate that our single-cell dataset reflects much of the original tissue composition and cellular complexity.
The heterogeneity among the profiled tissues is evident in cell-type composition changes (Fig. 1e and Extended Data Fig. 2a ). To understand the spatial organization and potential cell signalling pathways responsible for the changes in cell-type proportions, we designed an antibody panel to spatially resolve cell types of interest with imaging mass cytometry (IMC) (Extended Data Fig. 2b ).
First, we observed that the endometrium composition in EuE differs dramatically relative to Ctrl, with much of the epithelial component replaced by stroma and lymphocytes in EuE (Fig. 1e ). Consistent with this, we observed a smaller epithelial proportion in EuE compared to Ctrl (Fig. 2a,b and Supplementary Table 2 ), together with an increased expression of cell-cycle-related genes and proliferation of endometrial fibroblasts in EuE (Fig. 2c–e ). On a per-person basis, analysis of the scRNA-seq data revealed that EuE biopsies stratify into two groups distinguished by immune cell or fibroblast abundance, both distinct from the Ctrl samples. This result highlights the heterogeneity in EuE across individuals that exists independent of their treatment with hormones (Fig. 2f and Extended Data Fig. 2a ). Furthermore, osteoglycin ( OGN ) expression was higher in EuE fibroblasts than Ctrl (Fig. 2g,h and Supplementary Table 5 ), which indicates that EuE is transcriptomically and compositionally distinct from Ctrl.
Fig. 2: Cellular composition of Ctrl and endometriosis eutopic endometrium.
The alternative text for this image may have been generated using AI.
Full size image
a , Representative haematoxylin and eosin (H&E) images of eutopic tissues from Ctrl ( n = 5) and EuE ( n = 8) before and after classification. b , Box plot showing the proportion of epithelial cells in endometrial tissue. Ctrl ( n = 5) tissues show significantly higher epithelial cell proportion compared to EuE ( n = 8). Welch’s T -test, two-sided, P = 0.013. Each dot represents a tissue section (see also Source Data Fig. 2 ). Box represents the interquartile range, whiskers represent minimum and maximum values, and the box centre line represents the median. c , UMAP representation of the expression of TOP2A in Ctrl and EuE in global clustering (top). Circles denote the stromal cell population. Representation of TOP2A (proliferating cells) and MME (endometrial fibroblasts) expressing cells in Ctrl and EuE stromal subclusters (bottom). Arrowheads depict all endometrial fibroblasts (eFs) expressing TOP2A in EuE. d , The proportion of cells in G1, G2M or S cell cycle phases within all eF and in eF2 subpopulations. e , Representative IMC images of Ctrl ( n = 4) and EuE ( n = 5) showing the presence of proliferating cells labelled with Ki-67 (green), epithelial cells marked with pan-CK, EpCAM and E-cadherin (magenta), stromal cells marked with COL1A1 and CD10 (orange), and nuclei marked with DNA (blue). f , Matrix plot representing the overall similarity of endometrium biopsy samples from healthy participants and individuals with endometriosis (Pearson correlation based on gene expression from each individual). EuE clustered into two groups, each showing an enrichment of fibroblasts or immune cells. g , Violin plot showing significantly upregulated genes ( OGN and NES ) in EuE relative to Ctrl in decidualized stroma (dS2) subpopulation. h , Representative IMC image confirming an increase in OGN (cyan) secretion within stroma (orange) in EuE ( n = 5) relative to Ctrl ( n = 4). For a , e and h , representative images of both Ctrl and EuE were taken from individuals receiving the same hormone treatment regimen. Scale bar, 100 μm ( a , e , h ).
Source data
Second, EcP and EcPA were highly similar, particularly among epithelial cells, which suggests that lesions may extend beyond their macroscopic core and into the surrounding peritoneum (Fig. 1e,f ). Third, the two lesion types displayed markedly different cellular compositions, confirmed by IMC, in which we observed scarce epithelial glands and a predominance of stromal cells within EcO compared to EcP (Fig. 1e–g ).
Active vascular remodelling and immune cell trafficking in EcP
Endothelial cells (ECs) were markedly increased in EcP, which hinted that angiogenesis occurs in this tissue. We identified cellular components of vasculature—four mural cell and seven EC subpopulations—by careful analysis of previously described marker genes 5 , 6 , 9 , 10 , 11 (Fig. 3a–c ). Mural cells, which include vascular smooth muscle cells and perivascular cells, are specialized cells that directly interact with ECs to support and promote vasculature stabilization. Mural cells accounted for roughly 40% of stromal cells in EcPA (Extended Data Fig. 3a ) and, together with an increased proportion of ECs, suggest a highly vascularized microenvironment (Fig. 1e ). Perivascular STEAP4 and MYH11 (Prv-STEAP4 and Prv-MYH11, respectively) have previously been identified in the endometrium 6 , and we observed an unreported perivascular CCL19 (Prv-CCL19) subpopulation expressing both STEAP4 and MYH11 (Fig. 3b ). This subpopulation accounted for the majority of perivascular cells in EcP and EcPA (Extended Data Fig. 3b ) and exhibited tissue-specific gene expression (Extended Data Fig. 3c,d ). Notably, SUSD2 , a marker for endometrial mesenchymal stem cells identified in endometriosis 12 , was specifically co-expressed in EcP and EcPA CCL19 + perivascular cells (Extended Data Fig. 3d ). Prv-CCL19 cells were more abundant in and around peritoneal lesions together with an upregulation of CCL19 and other known angiogenesis regulators such as synuclein-y ( SNCG) 13 and angiopoietins ( ANGPT1 , ANGPTL1 and ANGPT2 ) 14 . Similarly, Prv-CCL19 upregulated the expression of ligands implicated in T cell recruitment 15 ( CCL21 and FGF7 ) (Fig. 3d,e and Extended Data Fig. 3e ). Together, these data indicate the presence of an endometriosis-specific perivascular subpopulation that probably promotes angiogenesis and immune chemotaxis in peritoneal lesions (Fig. 2f ).
Fig. 3: Role of stromal cell diversity in angiogenesis and immune trafficking in endometriosis lesions.
The alternative text for this image may have been generated using AI.
Full size image
a , UMAP plot of the 12 identified stromal subpopulations and classified into three general cell subtypes: endometrial fibroblast (eF), C7 fibroblast (Fib C7) and mural cell ( n = 42,713 cells). VSMC, vascular smooth muscle cell. b , Violin plot showing markers of mural cell subpopulations. c , UMAP plot of ECs represented across seven subclusters: lymphatic EC (LEC), high endothelial venule (EC-HEV), capillary (EC-capillary), post-capillary venous (EC-PCV), activated PCV (EC-aPCV) and arterial (EC-artery). d , Top: proportion of Prv-CCL19 within stromal cells. A large increase in Prv-CCL19 is observed in EcPA. Bars represent the mean value. Bottom: swarm plot showing CCL19 expression in individual cells from each lesion. e , Dot plot showing significantly upregulated genes involved in angiogenesis and immune cell trafficking (edgeR, false discovery rate (FDR) < 0.05) in Prv-CCL19. f , Schematic of mural and EC localization. Larger arteries and veins are unsheathed by VSMCs, whereas smaller vessels (for example, capillaries) are unsheathed by perivascular cells. Perivascular cells in lesions increase the expression of pro-angiogenic genes compared to Ctrl tissue. g , Dot plot showing significant representative differentially expressed genes (DEGs) involved in new vessel formation in EC tip cells (edgeR, FDR < 0.05). h , Dot plot showing significant DEGs involved in cell adhesion and permeability in a-PCV (edgeR, FDR < 0.05). i , Representative IMC image from a peritoneal lesion ( n = 7). CD3 + T cells (cyan) and CD68 + myeloid cells (magenta) localize within and surrounding blood EC vasculature marked by CD31 and AQP1 (yellow). Nuclei were counterstained by DNA labelling (blue). Scale bar, 100 µm.
To further elucidate the interactions between ECs and Prv-CCL19, we performed ligand–receptor analysis to identify specific interactions involving Prv-CCL19 cells ( Methods and Extended Data Fig. 4a ). Our data indicated that EC-tip cells probably respond to ANGPT1 produced by perivascular cells, an interaction that induces tube formation and branching 16 (Supplementary Table 6 ). In endometriosis, TEK expression was upregulated whereas expression of TIE1 , the anti-angiogenic receptor for angiopoietins 14 , 17 , was downregulated (Fig. 3g ). Previous studies have shown that TEK pathway activation leads to EC proliferation and activation of a feedback loop through DLL4–NOTCH signalling to induce EC tip cell maturation 18 , 19 , 20 . We found significantly increased expression of cell cycle gene CCND1 and decreased expression of DLL4 in EuE, EcP and EcPA relative to Ctrl (Fig. 3g , Extended Data Fig. 4b and Supplementary Table 5 ), which suggests that EC-tip cells have higher proliferative capacity and sprouting. By contrast, the cell cycle arrest gene BTG2 was upregulated and DLL4 – NOTCH signalling was maintained in EcO, which suggests that there is inhibition of sprouting EC-tip cells in the ovarian microenvironment.
Immune cell trafficking involves the extravasation of immune cells from the bloodstream, crossing the EC barrier into interstitial tissue. Extravasation mainly occurs at the capillary and post-capillary venous (PCV) level 21 . We observed that proportions of two PCV subpopulations 10 , 11 , activated PCV (EC-aPCV) and EC-PCV cells, were markedly increased in EcP and its adjacent tissue (Extended Data Fig. 4c,d ). Genes that regulate immune cell attachment and monocyte trafficking 21 — PECAM1 , JAM2 , VCAM1 , ICAM1 and CD99 —and genes associated with EC permeability 22 — PLVAP , AQP1 and CXCL12 —were among the significantly upregulated genes in endometriosis EC-aPCV. By contrast, ICAM2 , which encodes a tight junction protein responsible for endothelial-to-endothelial cell contact 21 , was downregulated (Fig. 3h and Supplementary Table 5 ). Expression of AQP1 , which is associated with angiogenesis and migration of ECs 23 , was substantially increased in endometriosis EC-PCV and EC-aPCV cells (Extended Data Fig. 4e,f ). Myeloid and lymphocyte cells were abundant both within and surrounding blood vessels in EcP, which indicated that there was immune trafficking activity at this site (Fig. 3i ). Together, these data suggest peritoneal lesions possess a leaky PCV vasculature.
Our data describe an endometriosis-specific perivascular cell subtype and emphasize a dynamic orchestration of Prv-CCL19 and PCV endothelial subpopulations, which probably promote angiogenesis and immune cell trafficking in peritoneal endometriosis lesions. This analysis also highlights substantial differences between ovarian and peritoneal lesion microenvironments.
Contribution of macrophages to lesion microenvironments
scRNA-seq uncovered 15 myeloid cell subpopulations (Fig. 4a and Extended Data Fig. 5a ) and 14 lymphocyte subpopulations (Fig. 1d ). Myeloid cells, particularly macrophages, have been characterized as central components of the endometriosis ecosystem, playing a key role in the establishment of endometriosis 2 . This, together with our observations indicating an increased abundance of myeloid cells in peritoneal lesions (Fig. 1e ), prompted us to investigate macrophage heterogeneity. We identified five macrophages subpopulations (MΦ1–MΦ5), of which MΦ1-LYVE1 and MΦ3-APOE were previously identified by single-cell analysis in other systems 9 , 24 , 25 . Tissue-resident macrophage subpopulations (MΦ1-LYVE1, MΦ2-peritoneal and MΦ3-APOE) were distinguished by the expression of FOLR2— a gene associated with embryonic-derived tissue-resident macrophages 22 , 26 . MΦ2-peritoneal cells were exclusive to peritoneal tissue and expressed ICAM2 , a known marker for peritoneal macrophages 27 . MΦ4-infiltrated cells were present in all tissues, expressed CLEC5A , CCR2 and VEGFA , all markers for blood-infiltrated macrophages 28 , 29 , and similar to monocytes (Fig. 4b,c and Extended Data Fig. 5b ). RNA velocity trajectory analyses suggested that MΦ3-APOE are more similar to tissue-resident MΦ1-LYVE1 and MΦ2-peritoneal subpopulations (Fig. 4d and Extended Data Fig. 5b ). Notably, MΦ5-activated cells appeared to arise from both infiltrated and tissue-resident macrophages (Fig. 4b–d ). Together, these data illustrate the presence of distinct tissue-resident and blood-infiltrated macrophage populations in endometrial and lesion tissues.
Fig. 4: Macrophage heterogeneity in Ctrl and endometriosis samples.
The alternative text for this image may have been generated using AI.
Full size image
a , UMAP plot of myeloid cells clustered into 15 different subtypes ( n = 12,262 cells). Mature dendritic cells (mDC); plasmacytoid dendritic cells (pDC). b , Dot plot showing expressed marker genes for tissue-resident (TRM), blood-infiltrated and activated macrophages across identified macrophage subpopulations and tissues. c , Density plot showing the macrophage distribution for each tissue type. d , UMAP plot showing RNA velocity streamlines for monocytes and macrophages in Ctrl samples. Streamlines represent the predicted transition path of cells across subpopulations. e , Bar plot showing the proportion of LYVE1- expressing cells to all macrophages within each tissue type. Each dot represents the percentage of LYVE1 + cells in a tissue biopsy (Ctrl n = 3, EuE n = 9, EcP n = 8, EcPA n = 6, EcO n = 4). The box represents the interquartile range with median and minimum and maximum represented by the box centre line and whiskers, respectively. f , Dot plot showing DEGs involved in immunotolerance in the MΦ1-LYVE1 population. g , IMC image from a fixed-formalin paraffin-embedded tissue section of a peritoneal lesion. Images depict LYVE1 + macrophages (LYVE1, CD68) localization near ECs (CD31, AQP1) (white arrowheads). Scale bar, 100 µm. h , Matrix plot showing the expression of pro-inflammatory and pro-tolerogenic related genes in the Mϕ4 subpopulation in Ctrl and endometriosis samples.
The relative abundance of macrophage subpopulations differed dramatically between Ctrl and endometriosis samples. For example, MΦ1-LYVE1 and MΦ5-activated were enriched in endometriosis EuE and ectopic tissues, respectively, and most macrophages present in EcO were MΦ1-LYVE1 (Fig. 4c and Extended Data Fig. 5c ). Across participants, LYVE1 + macrophages were enriched in both eutopic and ectopic tissues compared to Ctrl (Fig. 4e ). Tissue-resident LYVE1 + macrophages have been previously associated with angiogenesis 22 , 24 , arterial stiffness 30 and anti-inflammatory phenotypes 26 . In agreement, we found that endometriosis MΦ1-LYVE1 upregulated tolerogenic genes ( VSIG4 , RGS1 , IL10 , EGFL7 and LYVE1 ) and angiogenesis-related genes ( THBS1 , HBEGF , PDGFB , PDGFC and IGF1 ) (Fig. 4f ). Furthermore, inflammation and antigen-presenting pathways of MΦ1-LYVE1 were downregulated in endometriosis tissues, whereas angiogenesis pathways were enriched in EcPA (Supplementary Table 7 ). MΦ1-LYVE1 localization along the vasculature — but not within — confirms the likely link between angiogenesis and this specific cell population (Fig. 4g ). In addition, two genes ( IGF1 and EMB ) previously shown to promote neurogenesis sprouting in endometriosis 31 and neuromuscular junctions 32 were among the top upregulated genes in MΦ1-LYVE1 in eutopic and ectopic tissues, implicating them in pain-related mechanisms (Fig. 4f ). MΦ4-infiltrated cells, almost completely absent in EcO, presented pro-tolerogenic features in endometrial tissue, which is in stark contrast to its pro-inflammatory presentation in Ctrl endometrium (Fig. 4h ). Altogether, we identified endometriosis-associated changes in multiple macrophage subpopulations that promote tolerogenic, pro-angiogenic and pro-neurogenic microenvironments. Moreover, the altered macrophage landscape is shared in endometriosis lesions and eutopic endometrium, affecting both tissue-resident and blood-infiltrated macrophages.
EcPA DCs adopt an immunomodulatory phenotype
Among the DCs, we classified three CD1C + populations as pre-cDC2, cDC2 and DC3 according to previously reported markers 25 , 33 , 34 (Fig. 5a ). DC proportions varied greatly across individuals (Extended Data Fig. 6a ). However, CD1C + DCs consistently accounted for the majority of the DCs in all tissues (Fig. 5b,c ).
Fig. 5: Immunomodulatory role of DCs in peritoneal endometriosis.
The alternative text for this image may have been generated using AI.
Full size image
a , Violin plot showing markers of DC subpopulations. CD1C expression was prevalent in three DC subpopulations: pre-cDC2, cDC2 and DC3. b , CD1C + cells represent the majority of the DC population, accounting for more than 80% of DCs in all tissues. c , Density plot showing the increased cDC2 populations in peritoneal lesions compared to EuE. d , Expression levels of the cDC2 markers CD207 and CD1A and the proliferation marker TOP2A . e , The proportion of CD207 -expressing cells across all cDC2 populations. CD207 + cells were consistently observed in eutopic endometrium, but variable in peritoneal lesions and not observed in ovarian lesions. Each dot represents the percentage of CD207 + cells for each tissue biopsy (Ctrl n = 3, EuE n = 9, EcP n = 8, EcPA n = 6, EcO n = 4). The box represents the interquartile range, with the median and minimum and maximum represented by the box centre line and whiskers, respectively. f , Track plot representing the expression of DEGs upregulated in cDC2-CD1A in EcPA (Wilcoxon, FDR < 0.05). Each bar represents a cell. Differential expression for the represented genes was detected in EcPA cells (black box). g , Left: density plot of cDC2 from EcP and EcPA showing the distribution of cDC2 on a UMAP representing different cell states. Right: scatter plot showing CD207 + MSR1 – ( n = 237), CD207 – MSR1 + ( n = 121), CD207 + MSR1 + ( n = 82) and CD207 – MSR1 – ( n = 141) cells. h , Top 12 DEGs between CD207 + MSR1 – and CD207 – MSR1 + populations from cDC2 subpopulations in EcP and EcPA (Wilcoxon, FDR < 0.05, log(fold change) > 1).
Despite studies reporting altered DC proportions in endometriosis 35 , 36 , the field is still lacking a comprehensive characterization of DC heterogeneity. Previous studies have suggested that DCs maintain themselves within tissue by proliferating under normal conditions but can be bolstered by an influx of blood-derived DCs during times of heightened immune activity 37 . Our analysis suggested that cDC2s derive from pre-DCs, consistent with the substantial number of proliferative pre-cDC2 cells observed (Extended Data Fig. 6b,c ). The relationship between cDC2s and DC3s appeared tissue-specific, as both populations seemed to derive from an intermediate population in Ctrl (red arrows, Extended Data Fig. 6b ) expressing FLT3 , SIGLEC6 and AXL (DC progenitor-derived and blood-derived DC markers 38 ). Meanwhile, cDC2 and DC3 subpopulations appeared to derive from pre-cDC2s in EcP (Extended Data Fig. 6d ).
As a possible reservoir for tissue-resident DCs, we further interrogated cDC2 diversity. A cDC2 subset in eutopic endometrium and peritoneal lesions, but not EcO, specifically expressed CD207 , a gene expressed by Langerhans cells and immature DCs 39 (Fig. 5d–f ). Further analysis revealed two cell states in EcP and EcPA cDC2 populations characterized by mutually exclusive expression of CD207 and MSR1 (Fig. 5f,g ). Differential gene analysis highlighted CD207 + cDC2 cells expressing genes related to immunogenic DC maturation ( IL18 , GNLY , RUNX3 and LTB ) 40 , 41 , 42 , whereas MSR1 + cDC2s expressed immunomodulatory genes ( MRC1 , VSIG4 , SGK1 and PECAM1 ) 43 , 44 , 45 (Fig. 5f,h). Gene set enrichment analysis of cDC2s across tissues indicated phagocytosis and cytokine-mediated signalling pathways were upregulated in endometriosis tissues (Extended Data Fig. 6e ). These data indicate the presence of disease-specific DC heterogeneity and highlights a potential immunomodulatory role for MSR1 + cDC2s in the peritoneum.
Lymphocyte organization and cell–cell communication
Next, we interrogated lymphocyte diversity and their interactions with other immune subpopulations (Fig. 6a and Extended Data Fig. 7a,b ). Based on ligand–receptor analysis, we observed numerous unique interactions, spatially supported by IMC, between T cells and various immune subpopulations (Extended Data Fig. 7c ). In particular, interactions between CD86 (expressed in MΦ1-LYVE1) and CTLA4 (expressed in regulatory T (T Reg ) cells) was upregulated in endometriosis (Fig. 6b , Extended Data Fig. 7d and Supplementary Table 6 ). This interaction is important for T Reg cell suppression and homeostasis 46 , and suggests that the cooperation of macrophages with T reg cells may be an additional mechanism through which an immunomodulatory microenvironment is promoted in endometriosis. Furthermore, we found that genes associated with T Reg cell regulatory function were altered between Ctrl and endometriosis samples (Fig. 6c ). Ctrl T Reg cells expressed HAVCR2 , LAG3, ENTPD1, ICOS, TNFRSF4 and CTLA4 , whereas TIGIT , PRDM1 and CD96 expression was prevalent specifically in endometriosis tissues and EcO specifically. Also noteworthy, ENTPD1— which encodes an important regulator in uterine natural killer (NK) cells that promote immune tolerance and angiogenesis during pregnancy 47 — was upregulated in lesion NK1 cells (Fig. 6d ). Collectively, these changes in gene expression indicate modulation of interactions between various immune subpopulations in ectopic lesions, although the exact mechanism remains unclear.
Fig. 6: TLS presence in peritoneal endometriosis.
The alternative text for this image may have been generated using AI.
Full size image
a , UMAP plot of lymphocyte subpopulations. Represented clustering highlights 14 different subpopulations ( n = 22,225) based on known markers. Cytotoxic T cells (CTL); innate lymphoid cells (ILC); peripheral natural killer cells (pNK); naive/central memory T cells (T N /T CM ); effector memory T cells (T EM ); resident memory CD8 + T cells (CD8-T RM ); mucosal associated invariant T cells (MAIT). b , Top: schematic showing CD86–CTLA4 ligand–receptor interaction between Mϕ1 macrophages and T Reg cells. Bottom: the dot plot shows gene expression levels for this interacting pair in each tissue type. c , Dot plot showing DEGs associated with T Reg cell self-tolerance maintenance (edgeR, FDR < 0.05) a Non-significant DEGs. d , Violin plot representing ENTPD1 gene expression in tissue-resident NK1 cells across sample types. e , H&E staining of a fomalin-fixed paraffin-embedded tissue section of a peritoneal lesion. This sample presented TLS-like formation highlighted in the white frame. TLS-like structures were detected in n = 2 out of 7 EcP samples. f , IMC image from the same lesion showing endometrial fibroblasts (CD10, red), B cells (CD20, yellow), epithelial cells (pan-KRT, green), stroma (COL1A1, cyan) and antigen-presenting cells (HLA-DR, magenta). TLS are primarily located through an accumulation of CD20 + cells forming GC-like structures in the periphery of the lesion (white frame, arrowhead). HLA-DR overlapping with CD20 indicates an antigen-presenting capacity within the GC. g , Magnified image showing GC structures with accumulation of B cells (CD20, yellow) in the centre surrounded by T cells (CD3, cyan). Ki-67 labels proliferative B cells within the GC (green, middle). CD31 and AQP1 label blood ECs (green, right). PDPN marks follicular DCs (magenta in middle or cyan in right image). h, i , H&E (left) and corresponding IMC (right) representative images from endometriotic lesions without TLS in EcP ( n = 5, 7) ( h ) and EcO ( n = 6, 6) ( i ) for identical antibodies in f . Scale bar, 100 µm ( e – i ).
We interrogated immune cell spatial localization among ectopic lesions using IMC. Notably, we observed a large cluster of immune cells in 2 out of 7 peritoneal lesions that fit the description of tertiary lymphoid structures (TLSs) (Fig. 6e–g ). TLSs consist of a germinal centre (GC) microarchitecture comprising a central B cell (CD20 + ) population surrounded by T cells (CD3 + ) and the additional presence of follicular DCs (PDPN + ) and antigen-presenting cells (HLA-DRA + ), although composition and organization of TLS vary depending on their degree of maturity. TLSs are present in autoimmune disease, chronic inflammatory disease and tumours but have not, to our knowledge, been described in endometriosis 48 , 49 . We did not observe similar structures in EcO or across all EcP samples (Fig. 6h,i ), which suggests that TLS formation may not be a driver of lesions but a consequence of a sustained inflammatory response. Gene expression analysis of B cells showed subtle transcriptomic differences among genes related to GC B cells ( BCL6 , SEMA4A and CXCR5 ) 49 , 50 (Extended Data Fig. 7e ), which suggests that this phenomenon is variable among peritoneal lesions and among individuals. Altogether, these data emphasize the diversity among immune cells co-existing within endometriosis lesions.
Characterization of endometrial MUC5B + epithelial cells
We identified ten epithelial populations constituting the endometrial glands and mesothelium (Fig. 7a–c ). Some of these have previously been observed in healthy endometrium 5 , 6 , whereas other populations differed substantially or have not been previously observed. Namely, we observed previously unreported mesothelial cells found in ectopic tissue and MUC5B + epithelial cells (Fig. 7a and Extended Data Fig. 8a ). Epithelial cell composition in peritoneal lesions reflected that found in the endometrium, whereas EcO epithelial populations were smaller and less diverse (Fig. 7b ). This suggests that endometrial-like epithelial cells in ovarian and peritoneal lesions may differ in their ability to respond to hormonal or differentiation signals.
Fig. 7: Characterization of epithelial cell subpopulations in Ctrl and endometriosis samples.
The alternative text for this image may have been generated using AI.
Full size image
a , Unsupervised clustering of epithelial cells led to 10 subpopulations ( n = 19,200) represented in the UMAP. b , Density plot showing the distribution of epithelial subtypes across tissues. c , Markers for each epithelial subtype and menstrual phase across each epithelial subtype. d , Left: immunohistochemistry staining confirmed the presence of MUC5B + cells in EuE n = 1). Right: immunofluorescence showed the co-localization of endometrial epithelial (E-cadherin + , green) and MUC5B + cells (magenta). Nuclei were counterstained with DAPI (cyan) in EuE ( n = 4). Scale bar, 100 µm. e , FPR2 expression is specific to myeloid cells (left) and more precisely to monocytes and Mϕ4-infiltrated cells (right). f , Representative image of EEO cultures derived from dissociated single cell of endometrium and endometriotic lesions. Scale bar, 100 µm g , UMAP plot representing the merge dataset for in vivo (tissue derived) and in vitro (EEO) epithelial cells. Classification follows previously described subpopulations in vivo.
The MUC5B + population was present in both eutopic (4–10% of epithelial cells) and ectopic tissues (<1%) and specifically expressed RUNX3 , TFF3 and SAA1 (Fig. 7b and Extended Data Fig. 8a ). We confirmed their presence in eutopic endometrium through immunohistochemistry and IMC (Fig. 7d and Extended Data Fig. 8b ). Both trefoil factor 3 (encoded by TFF3 ) and serum amyloid A (SAA) (encoded by SAA1 and SAA2 ) have been reported to be involved in epithelial restitution, a process initiating mucosal epithelial repair and immune cell recruitment, although details of this mechanism are still unclear 51 , 52 , 53 . SAA is a major modulator of inflammation 54 and a promotor of phagocyte chemotaxis through interactions with its receptor FPR2 (ref. 55 ). TFF3 upregulation has been linked to endometriosis and inflammation 56 . This prompted us to use ligand–receptor analysis to look for potential interactions involving MUC5B + cells. FPR2 was specifically expressed by myeloid cells, particularly monocytes and MΦ4-infiltrated cells (Fig. 7e and Supplementary Table 6 ), which suggests a potential interaction between MUC5B + cells and blood-derived myeloid cells. Additionally, we noted the co-expression of PROM1 and SIX1 , which are progenitor cell markers 57 , 58 , in in vivo MUC5B + cells (Fig. 7b ).
To investigate the presence of MUC5B + cells in in vitro cultures, we established endometrial epithelial organoids (EEOs) from primary tissue, starting with unselected single-cell suspensions (Fig. 7f ). EEOs were maintained in proliferative conditions and subsequently profiled by scRNA-seq, producing data on 13,326 cells (Extended Data Fig. 8d ). We combined the EEO dataset with the epithelial single-cell transcriptomes from primary tissue and analysed them together (Fig. 7g ). Of the populations identified in the primary tissue, EEO cells distributed along ciliated (14%) and glandular proliferative epithelial cells (11%), with few differences related to their tissue of origin (Extended Data Fig. 8e ). The largest population of EEO cells (70%) clustered closely between glandular proliferative and MUC5B + cells from primary tissue (Fig. 7g , arrow) and expressed markers similar to MUC5B + cells in vivo, such as RUNX3 , TFF3 and SAA1 (Extended Data Fig. 8f ).
The increased proportion of MUC5B + cells in organoid culture led us to further interrogate the role of MUC5B + cells. Thus, we isolated MUC5B + and MUC5B – epithelial cell populations from primary tissue and performed live imaging during organoid derivation (Extended Data Fig. 9a ). Organoids derived from MUC5B + cells grew significantly larger and in higher numbers than those of MUC5B – cells (Extended Data Fig. 9b,c ). Notably, MUC5B expression was confirmed in organoids derived from both populations (Extended Data Fig. 9d ). Altogether, these data suggest that MUC5B + epithelial cells may represent a progenitor-like population.
Discussion
We provided a comprehensive description of peritoneal and ovarian endometriosis lesions at single-cell resolution and compared this data to healthy endometrium, endometrium from individuals with endometriosis and organoids derived from these tissues. Our approach was holistic, capturing all cell types (or at least those that survived dissociation) that comprise lesions and their adjacent surroundings. This provided a view of the cellular composition and communication within the niche where lesions establish and evolve. We utilized histopathological imaging and hyperplex antibody-based imaging, with selection of antibodies guided by scRNA-seq, to provide spatial context.
Our data were generated from individuals undergoing lesion excision for endometriosis symptom relief and receiving hormonal treatment, thereby representative of the vast majority of individuals with endometriosis, as hormone therapy is the most frequent management strategy for the condition. This continuous low-dose oestrogen and/or progestin hormonal treatment comprised the bulk of our participants without endometriosis. Hormonal treatment induces systemic histological and molecular changes that vary from person to person and differ substantially from the cyclic changes observed during the normal menstrual cycle. Our study was specifically designed to interrogate transcriptional and compositional differences between healthy endometrium and endometriosis, irrespective of hormone treatment. Indeed, despite the inherent inter-individual variability in treatment and clinical history common to human studies, we confirmed robust differences between the two tissues, such as OGN upregulation and increased stromal cell presence.
As lesions are described as a piece of endometrial tissue resembling the eutopic endometrium, it was not surprising that we identified extensive similarities in cell-type composition between the eutopic endometrium and peritoneal lesions. We also detected profound dysregulation of the innate immune and vascular systems in peritoneal lesions. Ovarian lesions, however, displayed extensive and distinct compositional and gene expression differences relative to peritoneal lesions. Our study provides important clues on the interconnected cellular networks where myeloid, endothelial, epithelial and perivascular subpopulations influence the formation of an endometriosis-favouring microenvironment (Extended Data Fig. 10 ).
Among the myeloid cell subpopulations, macrophages and DCs have been described as key players in endometriosis pathology 1 , 2 , 4 , with reports showing endometriosis-related alterations of macrophages 29 , 59 and DCs 35 , 36 . However, a comprehensive description of myeloid subtypes was previously lacking. Here, we presented a precise characterization of immunomodulatory macrophage and DC populations in peritoneal endometriosis that adopt a coordinated immunotolerant phenotype in the endometriosis microenvironment. For example, DCs express MRC1 and VSIG4 , potentially promoting immunosurveillance escape and therefore benefiting lesion establishment 60 , 61 . Such a phenotype was reported in decidual macrophages and associated with fetal tolerance during pregnancy 62 , 63 . Thus, the current dataset constitutes an ideal starting point to understand how endometriosis may hijack a naturally occurring immunotolerant process to sustain lesion formation and evolution. A deeper understanding of this myeloid compartment in endometriosis is important, as therapeutics targeting the immune system have been proposed as treatment strategies 2 , 64 , 65 . The spatial analysis provided by IMC provides valuable information to understand the full dynamic of cellular interactions. One such example is the discovery of TLSs in peritoneal lesions. Their role in endometriosis remains to be determined. A functional understanding of each myeloid and lymphoid subpopulation will determine whether TLSs constitute key drivers of the disease, and therefore key therapeutic targets, or are simply a by-product of the continuous inflammation induced by the lesion.
The accumulation of myeloid cells in lesions, together with the presence of LYVE1 -expressing macrophages near the vasculature, is probably linked with increased vascularization, a distinctive trait of peritoneal lesions, and accentuated in the adjacent tissue surrounding these lesions. CCL19 + (and CCL21 + ) perivascular cells may have a role in this as such cells in primary and secondary lymphoid organs have been shown to play a part in immune cell chemoattraction 66 , 67 . This population has not been previously described in endometriosis. Supporting our findings, inhibition of SNCG , a marker specifically expressed by perivascular CCL19 + cells, prevents endometriosis vascularization and growth 68 , 69 . The peritoneal angiogenic setting is in contrast to the ovarian lesion microenvironment where CCL19 + perivascular cells are absent. Thus, while ovarian and peritoneal lesions are currently placed under a common disease name and treatment, we uncovered fundamental differences in lesion type that may assist in tailoring lesion-specific therapeutic strategy design, such as vascular targeting 70 , 71 , for peritoneal lesions.
Endometrial epithelial glands form integral components for both eutopic endometrium and endometriotic lesions. The characterization of endometrial epithelial stem cells has been challenging due to the dynamic nature of the regenerative endometrium. Recent single-cell-driven descriptions of endometrial epithelial cells from healthy endometrium provide important insights into epithelial subpopulations and the associated hormone responses across the menstrual cycle 5 , 6 , 72 . The field, however, is still lacking a precise characterization of stem or progenitor EC populations that could explain epithelial gland establishment and initial lesion formation in ectopic tissues. We described a previously uncharacterized EC population expressing MUC5B , among other specific markers, present in both eutopic and, to a lesser extent, in ectopic tissues. Our success in capturing these cells may be a combination of an optimized tissue dissociation protocol, the analyses of samples from individuals receiving hormone treatment and/or the speed at which we processed these samples from surgery. However, it remains unclear how this cell subset contributes to endometrial regeneration or the genesis of lesions. Further functional studies will be key to define the precise role of these MUC5B + cells.
Although recent studies have begun to describe endometriosis at single-cell resolution 73 , 74 , here we generated a comprehensive dataset, inclusive of spatial organization, describing the eutopic endometrium and ectopic peritoneal and ovarian endometriosis lesions. This atlas represents an important tool to understand the key players and the dynamic interplay that constitutes the endometriosis niche in individuals receiving hormonal treatment. We consider that this dataset will be instrumental for in the design of effective therapeutic strategies or diagnostic biomarkers to provide relief to the large group of underserved individuals with endometriosis.
Methods
Human endometrium and endometriosis tissue collection
This study was approved by the Ethics Committee of the Institutional Review Board at the University of Connecticut Health Center (UCHC), The Jackson Laboratory, and the Human Research Protection Office of the US Department of Defense and conducted according to all relevant ethical regulations regarding human participants. Written informed consent was obtained from all participants. All participants consented to share recoded information in public, unrestricted databases. Tissue samples were obtained from the UCHC. Pre-menopausal female participants (18–49 years old) pre-operatively diagnosed with stage II–IV endometriosis and scheduled for laparoscopic surgery were invited to take part in this study. Endometriosis staging was confirmed at the time of laparoscopy according to the revised American Society for Reproductive Medicine guidelines. The majority of the individuals (in both control and endometriosis groups) were treated with similar hormone treatments at the time of sample collection (detailed in Supplementary Table 1 ). To obtain comparable control samples, we chose participant receiving similar progestin/oestrogen therapies and fulfilled the strict selection criteria we established: no history of any inflammatory condition or cancer; presence of hormonal treatment; age-matched to the endometriosis group; and visual inspection of absence of endometriosis (by laparoscopy with expert surgical evaluation of endometriosis absence). Matched eutopic endometrium and endometriosis tissues were collected from individuals with endometriosis (Fig. 1a and Supplementary Fig. 1a,b ). Eutopic endometrium was obtained by performing an endometrial biopsy during hysteroscopy. Ectopic peritoneal endometriosis was obtained by resecting the entire endometriosis lesion and adjacent peritoneum, ensuring the entire visible lesion was excised. For the control group, non-endometriosis eutopic endometrium biopsies were obtained from individuals scheduled for surgery who were not suspected to have endometriosis. Complete demographic information for participants is provided in Supplementary Table 1 . Histological analyses of endometrium samples were performed on haematoxylin and eosin (H&E)-stained tissue sections by UCHC pathologists. Following resection, fresh tissue was immediately stored in MACS tissue storage solution (Miltenyi, 130-100-008) and kept on ice until processing.
Tissue dissociation for scRNA-seq
Fresh tissues were immediately processed for scRNA-seq. Ectopic endometriosis lesions from the peritoneum were divided into ectopic lesion (EcP) and ectopic adjacent (EcPA) (Supplementary Fig. 1a ). Viable single cells were obtained by mechanical and enzymatic digestion using cold active protease (CAP), following a modified version of a previously described protocol 75 . In brief, minced tissue was transferred to GentleMACS C tubes (Miltenyi, 130-096-334) containing protease solution (10 mg ml –1 ﻿ Bacillus licheniformis protease (CAP) (Sigma, P5380) in DPBS supplemented with 5 mM CaCl 2 and 125 U ml –1 DNaseI (Stemcell, 07900)) and incubated in a cold water bath (6 °C) for 7–10 min, performing trituration steps every 2 min. After incubation, samples were mechanically dissociated on a Miltenyi GentleMACS Dissociator for 1 min, twice. Undigested tissue was allowed to settle by gravity for 1 min. Single cells within the supernatant were transferred into a collection tube containing wash buffer PBS supplemented with 10% FBS (Gibco, 10082147), 2 mM EDTA and 2% BSA (Miltenyi 130-091-376). Remaining undissociated tissue was incubated with fresh CAP for a total of 20–40 min, proceeding with a trituration step every 5 min and a Miltenyi gentleMACS dissociator step every 15 min. After recovery of single cells, residual undissociated tissue was incubated with PBS supplemented with 1 mg ml –1 dispase on the Miltenyi gentleMACS Dissociator at 37 °C for 15 min until complete tissue dissociation. Single cells were then pelleted, washed and filtered through a 70-µm MACS Smartstrainer (Miltenyi, 130-098-462). Before FACS, single-cell suspensions were stained with propidium iodide (PI; BD Biosciences, 556364) and calcein violet (Invitrogen, C34858) in FACS buffer (PBS, 2 mM EDTA and 2% BSA) according to manufacturers’ protocols. Viable cells (PI-negative and calcein-violet-positive) were sorted using a BD FACS Aria Fusion cell sorter, gated using FACS Diva (9.0.1) and recovered in Advanced DMEM/F12 (Gibco, 12634010) supplemented with 2 mM GlutaMAX (Gibco, 35050061), 10 mM HEPES (Gibco, 15630080), 20% FBS and 1% BSA. Sorted viable cells were then washed and resuspended with 0.04% BSA in PBS and assessed for viability using trypan blue staining for subsequent scRNA-seq experiments. A detailed protocol is available at protocols.io 76 .
Endometrial epithelial organoid cultures and cell-hashing for scRNA-seq
Following tissue dissociation and single-cell recovery, and after 10X chromium chip loading, remaining single cells were pelleted and resuspended in cold Matrigel (Corning, 356231). Droplets of 50 µl were plated into 24-well plate (Greiner Bio-one, 662102) to generate EEOs. After Matrigel dome solidification, organoid medium was added to cover each dome as previously described 77 . Organoid passaging was performed every 7–10 days and according to a previously established protocol 78 . For scRNA-seq experiments, organoid cultures between passage 3 and 5 and at day 7–11 after plating were collected, washed twice with wash medium (Advanced DMEM/F12, 2 mM GlutaMAX, 10 mM HEPES and 0.1% BSA), and dissociated into single cells using TrypLE Express (Gibco, 12605010) for 3–5 min at 37 °C. Cell suspensions were filtered with a 40-µm mesh filter to remove debris and cell aggregates. Last, cells were washed and resuspended with cell staining buffer (BioLegend, 420201) for hashing with TotalSeq-A anti-human Hashtag reagents (Supplementary Table 8 , BioLegend) for 30 min at 4 °C and using a previously published protocol 79 . After staining, cells were washed to remove excess antibody and resuspended in PBS and 0.04% BSA for subsequent counting. Hashed cells were assessed for viability and sorted for viable cells as described below.
Single-cell capture, library preparation and sequencing
Single-cell suspensions were analysed for viability and counted on a Countess II automated cell counter (Thermo Fisher). A total of 12,000 cells were loaded onto a channel of a 10x Chromium microfluidic chip for a targeted cell recovery of 6,000 cells per lane. Single-cell capture, barcoding and library preparation were performed using 10x Chromium v3 chemistry according to the manufacturer’s protocol (10x Genomics, CG000183). Sample complementary DNA and library quality controls were performed using an Agilent 4200 TapeStation instrument and quantified by qPCR (Kapa Biosystems/Roche). Libraries were sequenced on a NovaSeq 6000 (Illumina) with a S2 100 cycle kit targeting 100,000 reads per cell for tissues or 50,000 reads per cell for organoids.
Single-cell data pre-processing and clustering
Illumina base call files for all libraries were demultiplexed and converted to FASTQ files using bcl2fastq v.2.20.0.422 (Illumina). The CellRanger pipeline (10x Genomics, v.3.1.0) was used to align reads to the human reference GRCh38.p13 (GRCh38 10x Genomics reference 3.0.0), deduplicate reads, call cells and generate cell-by-gene digital counts matrices for each library. The resultant count matrices were further processed with Scanpy package (v.1.7.1) 80 to exclude genes that were detected in fewer than 3 cells and to exclude cells with the following parameters: (1) fewer than 500 genes, (2) fewer than 1,000 unique molecular identifiers (UMIs), (3) maximum of 100,000 UMIs and (4) maximum mitochondrial content of 25%. Doublet identification were performed using Scrublet 81 . Filtered matrices were then combined and normalized such that the number of UMIs in each cell was equal to the median UMI across the dataset and log-transformed. Scanpy was used to identify the top 2,000 highly variable genes from the log-transformed combined matrix. The mitochondrial genes, haemoglobin genes, ribosomal genes, cell cycle genes 82 and stress-response genes were excluded from the highly variable gene set 83 . Principal component analysis and neighbourhood graph generation were performed on the basis of the highly variable genes set. Harmony (v.1.0) batch correction was performed to reduce variabilities introduced by inherent inter-individual differences, tissue types and endometriosis staging to enhance clustering by major cell type 84 . For subsequent clustering of each major cell type, batch correction was performed to account only for inherent inter-individual differences and/or endometriosis staging to preserved tissue-type-specific expression 85 . Batched-corrected principal components were used for dimensionality reduction using uniform manifold approximation and projection (UMAP). Clustering was then performed with Leiden community detection algorithm 86 , 87 . Further doublet identification was calculated based on the median distance of a cell to the centre of its respective cluster centroid in UMAP space and the co-expression of marker genes of two or more cell types. All suspected doublets were removed from the analysis.
Cell types and cell-state identification
Marker genes of each cluster were identified using Wilcoxon rank-sum test in a one-versus-rest fashion, with minimum 0.5–2 fold-change between groups, expressed by at least 0.7 fraction of cells in the group and expressed by a maximum of 0.3 fraction of cells outside the group. Cell types were determined by matching the biomarkers with previously described cell types and cell states and from biomarkers curated from the literature (Supplementary Table 3 ).
Comparative analysis with bulk RNA-seq
To assess possible biases in cellular diversity or transcript capture in the droplet-based scRNA-seq, we performed bulk RNA-seq on tissue-type-matched aliquots of six participants from the scRNA-seq cohort as well as nine additional individuals. In total, we collected 12 eutopic, 6 ovarian lesions, and 6 peritoneal lesions for bulk RNA-seq samples (Supplementary Table 2 ). A Qiagen RNeasy Mini kit was used to extract total RNA from endometrium and endometriotic lesions obtained from snap-frozen tissue or tissue stabilized with RNAlater (Invitrogen, AM7020) according to the manufacturer’s instructions. Library preparation was performed using a KAPA mRNA Hyperprep kit (Roche) according to the manufacturer’s instructions. Bulk RNA-seq libraries were sequenced on a NovaSeq 6000 (Illumina) with a SP 100 cycles single-end reads kit, resulting in an average of 38.9 million reads per sample. Reads were aligned to the GRCh38.p13 reference genome (GRCh38 10x Genomics reference 3.0.0), filtered and quantified with nf-core/rnaseq (v.1.4.2) 88 utilizing the STAR aligner. Read counts were normalized to counts per millions (CPM) reads. scRNA-seq was compared to bulk RNA-seq by using pseudo-bulk transform (summing UMI counts for all cells in each sample and CPM normalization). For each tissue type, we compared these bulk transcriptomes with pseudo-bulk scRNA-seq profiles of the same type (Extended Data Fig. 1 ). In brief, we computed the Spearman correlation for each pairwise combination ( n = 144 eutopic, n = 24 ovarian, n = 90 peritoneal) of the bulk RNA-seq transcriptome and the pseudo-bulk transcriptome (Extended Data Fig. 1a ). Spearman correlation helps minimize unwanted biases derived from differences in total mRNA abundance and differences in normalization strategies between pseudo-bulk and bulk expression profiles. Then we computed the Spearman correlation between the mean bulk and single-cell pseudo-bulk expression profiles across samples sharing the same sample type (Extended Data Fig. 1b ). Differential gene expression between scRNA-seq and bulk RNA-seq data was analysed with edgeR exactTest 89 . Differentially expressed genes (DEGs) were generated sequentially for eutopic endometrium (Ctrl and EuE), ectopic peritoneal endometriosis (EcP and EcPA) and ectopic ovarian endometriosis (EcO) (Supplementary Table 4 ).
Identification of DEGs and GSEA analysis between tissue types
DEG analysis between tissue types within a population was performed on clusters with more than 500 cells. We utilized the glmQLFTest function in edgeR to compare each tissue types to Ctrl samples. Significant DEGs were considered at false discovery rate (FDR) values of <0.01 (Supplementary Table 5 ). Gene set enrichment analysis (GSEA) to Gene Ontology (GO) biological process (2018) was performed on significant DEGs (FDR < 0.00001) with gseapy (0.10.4) prerank function for each cell subtype 90 , 91 . The resulting enriched GO list was filtered at FDR < 0.10 (Supplementary Table 7 ).
Correlation matrix, dendrogram, cell cycle phase and cell-density estimation
Analyses were executed with functions implemented in Scanpy (1.7.1). Similarities between eutopic endometrium (Ctrl and EuE) tissues were based on hierarchical clustering calculated from Pearson correlation using the Ward linkage algorithm. Cell cycle phase (G1, S or G2M) estimation was calculated following a previously described protocol 92 and based on markers retrieved from ref. 93 . The cell density was estimated with Gaussian kernel density estimation on major cell subtypes within each tissue type.
Trajectory inference
Read counts of spliced and unspliced RNA was computed with velocyto (0.17.17) 94 on all 10x libraries obtained from tissue biopsies. We utilized the run10x function, which takes output from the CellRanger pipeline. Reads were aligned to GRCh38 (10x Genomics reference 3.0.0) and GRCh38 repeat mask downloaded from UCSC Genome Browser as recommended. Projected stream and PAGA trajectory was calculated with scVelo (0.2.3) following the recommended workflow as previously described 95 , 96 . First, clusters of interest were isolated based on cell barcodes (for example, myeloid cells in Ctrl). Second, spliced and unspliced counts were log-normalized and used for nearest-neighbours estimation. Then, RNA velocity was computed using the dynamical model of scVelo, which infers the splicing trajectory for each gene and allows for differential kinetics across distinct lineages and functional states that may be present in the dataset. To summarize the mRNA velocity computations, we performed PAGA 96 (specifically regarding DC populations). The number of cells per cell type population vary, especially when a subset is within a single sample type. With the aim of increasing the robustness of the resulting PAGA graphs, we utilized the following bootstrapping procedure to generate the edges for all PAGA networks presented in this manuscript: starting with the cells derived from one sample type, we generated 100 randomly subsampled datasets such that each cell type population contained 50 cells; populations with fewer than 13 cells were discarded and those with between 13 and 50 cells were supersampled to include 50 cells. We then recomputed the velocyto neighbour graph, moments distributions and kinetics, as well as the resulting velocity and PAGA graphs for each randomized dataset 95 . The PAGA connectivities and transitions graphs were used to construct a distribution of linkages between each pairwise combinations of cells. The mean transition probability across these 100 bootstrap samples for each linkage is what was used to plot the PAGA graph, and this process was repeated independently for all sample types comprising a given group of cell types.
Ligand–receptor analysis
Ligand–receptor analysis was performed using CellPhoneDB (2.1.4) 97 on all 58 subclusters. We modified the protocol by running CellPhoneDB on each 10x library separately to reflect the interactions only within individual tissue sample. As such, we included additional parameters to obtain a list of interactions that have P values of <0.01, were detected in at least 50% fraction of each tissue type, are not self-interactions and are unique cell-to-cell interactions (number of cell type pair is fewer than 150 counts; Supplementary Fig. 5 ). The database of ligand–receptor unique interactions obtained from this analysis is supplied in Supplementary Table 6 . A full list of interactions is available at https://github.com/TheJacksonLaboratory/endometriosis-scrnaseq .
Histology and immunofluorescence
Formalin-fixed paraffin-embedded (FFPE) tissues were cut into 5-μm sections, mounted on slides and stained for H&E. The slides were then scanned with a Hamamatsu Nanozoomer slide scanner at ×40 magnification for histopathological examination by a pathologist. Cell counting and cell-type classification was performed with QuPath (0.3.0) using a random forest classifier 98 . Welch’s T -test was performed to obtain P values. Immunofluorescence staining was performed on FFPE tissue sections. Slides were incubated for 10 min at 55 °C in a dry oven, deparaffinized in fresh Histoclear (National Diagnostics, HS-200) and rehydrated through a series of graded alcohol solutions. Antigen retrieval was performed in a decloaking chamber (BioSB TintoRetriever) for 15 min at 95 °C in neutral citrate buffer, pH 6.00 (Abcam, ab93678). Tissue was blocked and permeabilized with 10% donkey serum/0.1% Triton X-100 in PBS for 30 min at room temperature, then incubated with primary antibodies against MUC5B (1:1,000; Novus Biologicals, NBP1-92151) and E-cadherin (5 µg ml –1 ; R&D Systems, AF648) overnight. Tissue sections were subsequently incubated with secondary antibody donkey anti-rabbit Alexa Fluor 647 (Invitrogen, A-31573) and donkey anti-goat Alexa Fluor 488 (Invitrogen, A-11055) for 1 h at room temperature. 4,6-Diamidino-2-phenylindole (DAPI) (1 µg ml –1 ; Sigma, MBD0015) was used to counterstain the nuclei, then the slides were mounted with ProLong Diamond (Thermo Fisher, P36970). Images were taken using a Leica SP8 Confocal microscope at ×40 magnification using Leica Application Suite X (LAS X) and processed with Fiji 99 .
IMC
FFPE tissues were cut into 5-μm sections and mounted onto slides. Slides were incubated for 15 min at 55 °C in a dry oven, deparaffinized in fresh histoclear and rehydrated through a series of graded alcohol solutions. Antigen retrieval was performed in a decloaking chamber (BioSB TintoRetriever) for 15 min at 95 °C in citrate buffer, pH 6.0. After blocking in buffer containing 3% BSA, slides were incubated overnight at 4 °C with a cocktail of metal-conjugated IMC-validated primary antibodies (described in Supplementary Table 9 ). The following day, slides were washed twice in DPBS and counterstained with iridium intercalator (0.25 μmol per litre) for 5 min at room temperature to visualize DNA. After a final wash in ddH 2 O, the slides were air-dried for 20 min. The slides were then loaded on a Fluidigm Hyperion imaging mass cytometer. Regions of interest were selected using Fluidigm CyTOF software (v.7.0) and ablated by the Hyperion. The resulting images were exported as 16-bit .tiff files using the Fluidigm MCDViewer software and analysed using napari-imc (0.6.4) 100 or the open source Histocat++ (3.0.0) toolbox/ Histocat web 101 .
Isolation and characterization of MUC5B + epithelial population
FACS was performed to isolate MUC5B + and MUC5B – epithelial cells from endometrium-dissociated tissue (Extended Data Fig. 9a ). In brief, Ctrl eutopic tissue was dissociated as described above. Cells were then stained with PI and with antibodies marking immune cells (CD45 + ), ECs (CD31 + ), epithelial cells (EpCAM + ) and MUC5B (Supplementary Table 10 ). We sorted both MUC5B + and MUC5B – epithelial cells (BD Bioscience Symphony S6), gated using FACS Diva (9.0.1), and plated 2,000 cells of each population in Matrigel domes (Corning, 356231). Growth of organoids was monitored every 4 h using an Incuycte S5 (Sartorius) live microscope on brightfield imaging for 10 days. Organoid area and counts were analysed directly in the onboard Incucyte software (Extended Data Fig. 9c ), and paired t -test was performed with GraphPad Prism8 for each timepoint.
Statistics and reproducibility
All hypothesis tests were conducted with the Wilcoxon rank-sum test unless otherwise stated, and Benjamini–Hochberg correction was used to correct for multiple simultaneous hypotheses tests where applicable.
Reporting summary
Further information on research design is available in the Nature Research Reporting Summary linked to this article.
Data availability
The RNA-seq data that support the findings of this study have been deposited in the Gene Expression Omnibus (GEO) under accession code GSE179640 . To further safeguard the genomic identities of participants, single-nucleotide variants (SNVs) relative to the reference genome are masked in all bam files (BAMboozle v.0.5.0) 102 . Moreover, we have made the final single-cell datasets available for download and interactive exploration at https://singlecell.jax.org/datasets/endometriosis-2022 . For mapping of scRNA-seq and bulk RNA-seq data, GRCh38.p13 (Ensembl Release 93, https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.27 ) was used. Source data are provided with this paper. All other data supporting the findings of this study are available from the corresponding author on reasonable request.
Code availability
All code developed for and utilized in this study are available at https://github.com/TheJacksonLaboratory/endometriosis-scrnaseq , including modified CellPhoneDB scripts developed to optimize data interpretation for this study.
Change history
29 September 2022
A Correction to this paper has been published: https://doi.org/10.1038/s41556-022-01023-6
References
Zondervan, K. T. et al. Endometriosis. Nat. Rev. Dis. Prim. 4 , 9 (2018).
Article PubMed Google Scholar
Saunders, P. T. K. & Horne, A. W. Endometriosis: etiology, pathobiology, and therapeutic prospects. Cell 184 , 2807–2824 (2021).
Article CAS PubMed Google Scholar
Nirgianakis, K., Ma, L., McKinnon, B. & Mueller, M. D. Recurrence patterns after surgery in patients with different endometriosis subtypes: a long-term hospital-based cohort study. J. Clin. Med. 9 , 496 (2020).
Article PubMed Central Google Scholar
Symons, L. K. et al. The immunopathophysiology of endometriosis. Trends Mol. Med. 24 , 748–762 (2018).
Article CAS PubMed Google Scholar
Wang, W. et al. Single-cell transcriptomic atlas of the human endometrium during the menstrual cycle. Nat. Med. 26 , 1644–1653 (2020).
Article CAS PubMed Google Scholar
Garcia-Alonso, L. et al. Mapping the temporal and spatial dynamics of the human endometrium in vivo and in vitro. Nat. Genet. 53 , 1698–1711 (2021).
Article CAS PubMed PubMed Central Google Scholar
Vento-Tormo, R. et al. Single-cell reconstruction of the early maternal–fetal interface in humans. Nature 563 , 347–353 (2018).
Article CAS PubMed PubMed Central Google Scholar
Lv, H. et al. Deciphering the endometrial niche of human thin endometrium at single-cell resolution. Proc. Natl Acad. Sci. USA 119 , e2115912119 (2022).
Article CAS PubMed PubMed Central Google Scholar
He, S. et al. Single-cell transcriptome profiling of an adult human cell atlas of 15 major organs. Genome Biol. 21 , 294 (2020).
Article CAS PubMed PubMed Central Google Scholar
Voigt, A. P. et al. Bulk and single-cell gene expression analyses reveal aging human choriocapillaris has pro-inflammatory phenotype. Microvasc. Res. 131 , 104031 (2020).
Article CAS PubMed PubMed Central Google Scholar
Goveia, J. et al. An integrated gene expression landscape profiling approach to identify lung tumor endothelial cell heterogeneity and angiogenic candidates. Cancer Cell 37 , 21–36.e13 (2020).
Article CAS PubMed Google Scholar
Masuda, H., Anwar, S. S., Bühring, H. J., Rao, J. R. & Gargett, C. E. A novel marker of human endometrial mesenchymal stem-like cells. Cell Transplant. 21 , 2201–2214 (2012).
Article PubMed Google Scholar
Edwards, A. K., Ramesh, S., Singh, V. & Tayade, C. A peptide inhibitor of synuclein-γ reduces neovascularization of human endometriotic lesions. Mol. Hum. Reprod. 20 , 1002–1008 (2014).
Article CAS PubMed PubMed Central Google Scholar
Huang, H., Bhat, A., Woodnutt, G. & Lappe, R. Targeting the ANGPT–TIE2 pathway in malignancy. Nat. Rev. Cancer 10 , 575–585 (2010).
Article CAS PubMed Google Scholar
Alpdogan, Ö. et al. Keratinocyte growth factor (KGF) is required for postnatal thymic regeneration. Blood 107 , 2453–2460 (2006).
Article CAS PubMed PubMed Central Google Scholar
Teichert, M. et al. Pericyte-expressed Tie2 controls angiogenesis and vessel maturation. Nat. Commun. 8 , 16106 (2017).
Article CAS PubMed PubMed Central Google Scholar
Carbone, C. et al. Angiopoietin-like proteins in angiogenesis, inflammation and cancer. Int. J. Mol. Sci. 19 , 431 (2018).
Article PubMed Central Google Scholar
Roca, C. & Adams, R. H. Regulation of vascular morphogenesis by Notch signaling. Genes Dev. 21 , 2511–2524 (2007).
Article CAS PubMed Google Scholar
Pitulescu, M. E. et al. Dll4 and Notch signalling couples sprouting angiogenesis and artery formation. Nat. Cell Biol. 19 , 915–927 (2017).
Article CAS PubMed Google Scholar
Mühleder, S., Fernández-Chacón, M., Garcia-Gonzalez, I. & Benedito, R. Endothelial sprouting, proliferation, or senescence: tipping the balance from physiology to pathology. Cell. Mol. Life Sci. 78 , 1329–1354 (2020).
Article PubMed PubMed Central Google Scholar
Wettschureck, N., Strilic, B. & Offermanns, S. Passing the vascular barrier: endothelial signaling processes controlling extravasation. Physiol. Rev. 99 , 1467–1525 (2019).
Article CAS PubMed Google Scholar
Sharma, A. et al. Onco-fetal reprogramming of endothelial cells drives immunosuppressive macrophages in hepatocellular carcinoma. Cell 183 , 377–394.e21 (2020).
Article CAS PubMed Google Scholar
Monzani, E., Bazzotti, R., Perego, C. & La Porta, C. A. M. AQP1 is not only a water channel: it contributes to cell migration through Lin7/β-catenin. PLoS ONE 4 , e6167 (2009).
Article PubMed PubMed Central Google Scholar
Chakarov, S. et al. Two distinct interstitial macrophage populations coexist across tissues in specific subtissular niches. Science 363 , eaau0964 (2019).
Article CAS PubMed Google Scholar
Cheng, S. et al. A pan-cancer single-cell transcriptional atlas of tumor infiltrating myeloid cells. Cell 184 , 792–809.e23 (2021).
Article CAS PubMed Google Scholar
Samaniego, R. et al. Folate receptor β (FRβ) expression in tissue-resident and tumor-associated macrophages associates with and depends on the expression of PU.1. Cells 9 , 1445 (2020).
Article CAS PubMed Central Google Scholar
Kim, K.-W. et al. MHC II + resident peritoneal and pleural macrophages rely on IRF4 for development from circulating monocytes. J. Exp. Med. 213 , 1951–1959 (2016).
Article CAS PubMed PubMed Central Google Scholar
Gonzalez-Dominguez, E. et al. CD163L1 and CLEC5A discriminate subsets of human resident and inflammatory macrophages in vivo. J. Leukoc. Biol. 98 , 453–466 (2015).
Article CAS PubMed Google Scholar
Hogg, C. et al. Macrophages inhibit and enhance endometriosis depending on their origin. Proc. Natl Acad. Sci. USA 118 , e2013776118 (2021).
Article CAS PubMed PubMed Central Google Scholar
Lim, H. Y. et al. Hyaluronan receptor LYVE-1-expressing macrophages maintain arterial tone through hyaluronan-mediated regulation of smooth muscle cell collagen. Immunity 49 , 326–341.e7 (2018).
Article CAS PubMed Google Scholar
Forster, R. et al. Macrophage‐derived insulin‐like growth factor‐1 is a key neurotrophic and nerve‐sensitizing factor in pain associated with endometriosis. FASEB J. 33 , 11210–11222 (2019).
Article CAS PubMed PubMed Central Google Scholar
Lain, E. et al. A novel role for embigin to promote sprouting of motor nerve terminals at the neuromuscular junction. J. Biol. Chem. 284 , 8930–8939 (2009).
Article CAS PubMed PubMed Central Google Scholar
Villar, J. & Segura, E. Decoding the heterogeneity of human dendritic cell subsets. Trends Immunol. 41 , 1062–1071 (2020).
Article CAS PubMed Google Scholar
Maier, B. et al. A conserved dendritic-cell regulatory program limits antitumour immunity. Nature 580 , 257–262 (2020).
Article CAS PubMed PubMed Central Google Scholar
Schulke, L. et al. Dendritic cell populations in the eutopic and ectopic endometrium of women with endometriosis. Hum. Reprod. 24 , 1695–1703 (2009).
Article CAS PubMed Google Scholar
Hey-Cunningham, A. J. et al. Comprehensive analysis utilizing flow cytometry and immunohistochemistry reveals inflammatory changes in local endometrial and systemic dendritic cell populations in endometriosis. Hum. Reprod. 36 , 415–428 (2021).
Article CAS PubMed Google Scholar
Cabeza-Cabrerizo, M. et al. Tissue clonality of dendritic cell subsets and emergency DCpoiesis revealed by multicolor fate mapping of DC progenitors. Sci. Immunol. 4 , eaaw1941 (2019).
Article PubMed PubMed Central Google Scholar
Karsunky, H., Merad, M., Cozzio, A., Weissman, I. L. & Manz, M. G. Flt3 ligand regulates dendritic cell development from Flt3 + lymphoid and myeloid-committed progenitors to Flt3 + dendritic cells in vivo. J. Exp. Med. 198 , 305–313 (2003).
Article CAS PubMed PubMed Central Google Scholar
Merad, M., Ginhoux, F. & Collin, M. Origin, homeostasis and function of Langerhans cells and other langerin-expressing dendritic cells. Nat. Rev. Immunol. 8 , 935–947 (2008).
Article CAS PubMed Google Scholar
Tewary, P. et al. Granulysin activates antigen-presenting cells through TLR4 and acts as an immune alarmin. Blood 116 , 3465–3474 (2010).
Article CAS PubMed PubMed Central Google Scholar
Brown, C. C. et al. Transcriptional basis of mouse and human dendritic cell heterogeneity. Cell 179 , 846–863.e24 (2019).
Article CAS PubMed PubMed Central Google Scholar
Durand, M. et al. Human lymphoid organ cDC2 and macrophages play complementary roles in T follicular helper responses. J. Exp. Med. 216 , 1561–1581 (2019).
Article CAS PubMed PubMed Central Google Scholar
Yi, H. et al. Targeting the immunoregulator SRA/CD204 potentiates specific dendritic cell vaccine-induced T-cell response and antitumor immunity. Cancer Res. 71 , 6611–6620 (2011).
Article CAS PubMed PubMed Central Google Scholar
Munawara, U. et al. Human dendritic cells express the complement receptor immunoglobulin which regulates T cell responses. Front. Immunol. 10 , 2892 (2019).
Article CAS PubMed PubMed Central Google Scholar
Schmid, E. et al. Serum- and glucocorticoid-inducible kinase 1 sensitive NF-κB signaling in dendritic cells. Cell. Physiol. Biochem. 34 , 943–954 (2014).
Article CAS PubMed Google Scholar
Halliday, N. et al. CD86 is a selective CD28 ligand supporting FoxP3 + regulatory T cell homeostasis in the presence of high levels of CTLA-4. Front. Immunol. 11 , 3155 (2020).
Article Google Scholar
Strunz, B. et al. Continuous human uterine NK cell differentiation in response to endometrial regeneration and pregnancy. Sci. Immunol. 6 , eabb7800 (2021).
Article CAS PubMed Google Scholar
Aloisi, F. & Pujol-Borrell, R. Lymphoid neogenesis in chronic inflammatory diseases. Nat. Rev. Immunol. 6 , 205–217 (2006).
Article CAS PubMed Google Scholar
Cabrita, R. et al. Tertiary lymphoid structures improve immunotherapy and survival in melanoma. Nature 577 , 561–565 (2020).
Article CAS PubMed Google Scholar
Ruffin, A. T. et al. B cell signatures and tertiary lymphoid structures contribute to outcome in head and neck squamous cell carcinoma. Nat. Commun. 12 , 3349 (2021).
Article CAS PubMed PubMed Central Google Scholar
Hinrichs, B. H. et al. Serum amyloid A1 is an epithelial prorestitutive factor. Am. J. Pathol. 188 , 937–949 (2018).
Article CAS PubMed PubMed Central Google Scholar
Taupin, D. & Podolsky, D. K. Trefoil factors: initiators of mucosal healing. Nat. Rev. Mol. Cell Biol. 4 , 721–732 (2003).
Article CAS PubMed Google Scholar
Paulsen, F. P. et al. Intestinal Trefoil factor/TFF3 promotes re-epithelialization of corneal wounds. J. Biol. Chem. 283 , 13418–13427 (2008).
Article CAS PubMed PubMed Central Google Scholar
Cocco, E. et al. Serum amyloid A (SAA): a novel biomarker for uterine serous papillary cancer. Br. J. Cancer 101 , 335–341 (2009).
Article CAS PubMed PubMed Central Google Scholar
Badolato, R. et al. Serum amyloid a is a chemoattractant: induction migration, adhesion, and tissue infiltration of monocytes and polymorphonuclear leukocytes. J. Exp. Med. 180 , 203–209 (1994).
Article CAS PubMed Google Scholar
Henze, D. et al. Endometriosis leads to an increased trefoil factor 3 concentration in the peritoneal cavity but does not alter systemic levels. Reprod. Sci. 24 , 258–267 (2017).
Article CAS PubMed Google Scholar
Cindrova-Davies, T. et al. Menstrual flow as a non-invasive source of endometrial organoids. Commun. Biol. 4 , 651 (2021).
Article CAS PubMed PubMed Central Google Scholar
Terakawa, J. et al. SIX1 cooperates with RUNX1 and SMAD4 in cell fate commitment of Müllerian duct epithelium. Cell Death Differ. 27 , 3307–3320 (2020).
Article CAS PubMed PubMed Central Google Scholar
Maddern, J., Grundy, L., Castro, J. & Brierley, S. M. Pain in endometriosis. Front. Cell Neurosci. 14 , 590823 (2020).
Article CAS PubMed PubMed Central Google Scholar
Izumi, G. et al. Mannose receptor is highly expressed by peritoneal dendritic cells in endometriosis. Fertil. Steril. 107 , 167–173.e2 (2017).
Article CAS PubMed Google Scholar
Brech, D. et al. A mosaic renal myeloid subtype with T-cell inhibitory and protumoral features is linked to immune escape and survival in clear cell renal cell cancer. Preprint at bioRxiv https://doi.org/10.1101/2020.01.20.912865 (2020).
Gustafsson, C. et al. Gene expression profiling of human decidual macrophages: evidence for immunosuppressive phenotype. PLoS ONE 3 , e2078 (2008).
Article PubMed PubMed Central Google Scholar
Svensson, J. et al. Macrophages at the fetal–maternal interface express markers of alternative activation and are induced by M-CSF and IL-10. J. Immunol. 187 , 3671–3682 (2011).
Article CAS PubMed Google Scholar
Ścieżyńska, Komorowski, Soszyńska & Malejczyk NK cells as potential targets for immunotherapy in endometriosis. J. Clin. Med. 8 , 1468 (2019).
Article PubMed Central Google Scholar
Nothnick, W. B. Treating endometriosis as an autoimmune disease. Fertil. Steril. 76 , 223–231 (2001).
Article CAS PubMed Google Scholar
Malhotra, D. et al. Transcriptional profiling of stroma from inflamed and resting lymph nodes defines immunological hallmarks. Nat. Immunol. 13 , 499–510 (2012).
Article CAS PubMed PubMed Central Google Scholar
Rodda, L. B. et al. Single-cell RNA sequencing of lymph node stromal cells reveals niche-associated heterogeneity. Immunity 48 , 1014–1028.e6 (2018).
Article CAS PubMed PubMed Central Google Scholar
Csibi, N. et al. Gamma-synuclein levels are elevated in peritoneal fluid of patients with endometriosis. Med. Sci. Monit. 26 , e922137 (2020).
Article CAS PubMed PubMed Central Google Scholar
Kang, T.-Y. et al. Pericytes enable effective angiogenesis in the presence of proinflammatory signals. Proc. Natl Acad. Sci. USA 116 , 23551–23561 (2019).
Article CAS PubMed PubMed Central Google Scholar
Egorova, A. et al. Anti-angiogenic treatment of endometriosis via anti-VEGFA siRNA delivery by means of peptide-based carrier in a rat subcutaneous model. Gene Ther. 25 , 548–555 (2018).
Article CAS PubMed Google Scholar
Becker, C. M. & D’Amato, R. J. Angiogenesis and antiangiogenic therapy in endometriosis. Microvasc. Res. 74 , 121–130 (2007).
Article CAS PubMed Google Scholar
Liu, Z. et al. Single-cell transcriptomic analysis of eutopic endometrium and ectopic lesions of adenomyosis. Cell Biosci. 11 , 51 (2021).
Article PubMed PubMed Central Google Scholar
Ma, J. et al. Single-cell transcriptomic analysis of endometriosis provides insights into fibroblast fates and immune cell heterogeneity. Cell Biosci. 11 , 125 (2021).
Article CAS PubMed PubMed Central Google Scholar
Zou, G. et al. Cell subtypes and immune dysfunction in peritoneal fluid of endometriosis revealed by single-cell RNA-sequencing. Cell Biosci. 11 , 98 (2021).
Article CAS PubMed PubMed Central Google Scholar
Adam, M., Potter, A. S. & Potter, S. S. Psychrophilic proteases dramatically reduce single-cell RNA-seq artifacts: a molecular atlas of kidney development. Development 144 , 3625–3632 (2017).
CAS PubMed PubMed Central Google Scholar
Tan, Y., Luo, D., Bozal, S., Robson, P. & Courtois, E. Human endometrium and endometriosis tissue dissociation for single-cell RNA sequencing. protocols.io https://doi.org/10.17504/protocols.io.bvy8n7zw (2022).
Boretto, M. et al. Patient-derived organoids from endometrial disease capture clinical heterogeneity and are amenable to drug screening. Nat. Cell Biol. 21 , 1041–1051 (2019).
Article CAS PubMed Google Scholar
Turco, M. Y. et al. Long-term, hormone-responsive organoid cultures of human endometrium in a chemically defined medium. Nat. Cell Biol. 19 , 568–577 (2017).
Article CAS PubMed PubMed Central Google Scholar
Stoeckius, M. et al. Simultaneous epitope and transcriptome measurement in single cells. Nat. Methods 14 , 865–868 (2017).
Article CAS PubMed PubMed Central Google Scholar
Wolf, F. A., Angerer, P. & Theis, F. J. SCANPY: large-scale single-cell gene expression data analysis. Genome Biol. 19 , 15 (2018).
Article PubMed PubMed Central Google Scholar
Wolock, S. L., Lopez, R. & Klein, A. M. Scrublet: computational identification of cell doublets in single-cell transcriptomic data. Cell Syst. 8 , 281–291.e9 (2019).
Article CAS PubMed PubMed Central Google Scholar
Giotti, B. et al. Assembly of a parts list of the human mitotic cell cycle machinery. J. Mol. Cell. Biol. 11 , 703–718 (2019).
Article CAS PubMed Google Scholar
O’Flanagan, C. H. et al. Dissociation of solid tumor tissues with cold active protease for single-cell RNA-seq minimizes conserved collagenase-associated stress responses. Genome Biol. 20 , 210 (2019).
Article PubMed PubMed Central Google Scholar
Korsunsky, I. et al. Fast, sensitive and accurate integration of single-cell data with Harmony. Nat. Methods 16 , 1289–1296 (2019).
Article CAS PubMed PubMed Central Google Scholar
Lavin, Y. et al. Tissue-resident macrophage enhancer landscapes are shaped by the local microenvironment. Cell 159 , 1312–1326 (2014).
Article CAS PubMed PubMed Central Google Scholar
Becht, E. et al. Dimensionality reduction for visualizing single-cell data using UMAP. Nat. Biotechnol. 37 , 38–44 (2019).
Article CAS Google Scholar
Traag, V. A., Waltman, L. & van Eck, N. J. From Louvain to Leiden: guaranteeing well-connected communities. Sci. Rep. 9 , 5233 (2019).
Article CAS PubMed PubMed Central Google Scholar
Ewels, P. A. et al. The nf-core framework for community-curated bioinformatics pipelines. Nat. Biotechnol. 38 , 276–278 (2020).
Article CAS PubMed Google Scholar
Lun, A. T. L., Chen, Y. & Smyth, G. K. in Statistical Genomics. Methods in Molecular Biology Vol. 1418 (eds Mathé, E. & Davis, S.) 391–416 (Humana Press, 2016).
Mootha, V. K. et al. PGC-1α-responsive genes involved in oxidative phosphorylation are coordinately downregulated in human diabetes. Nat. Genet. 34 , 267–273 (2003).
Article CAS PubMed Google Scholar
Subramanian, A. et al. Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. Proc. Natl Acad. Sci. USA 102 , 15545–15550 (2005).
Article CAS PubMed PubMed Central Google Scholar
Satija, R., Farrell, J. A., Gennert, D., Schier, A. F. & Regev, A. Spatial reconstruction of single-cell gene expression data. Nat. Biotechnol. 33 , 495–502 (2015).
Article CAS PubMed PubMed Central Google Scholar
Tirosh, I. et al. Dissecting the multicellular ecosystem of metastatic melanoma by single-cell RNA-seq. Science 352 , 189–196 (2016).
Article CAS PubMed PubMed Central Google Scholar
La Manno, G. et al. RNA velocity of single cells. Nature 560 , 494–498 (2018).
Article PubMed PubMed Central Google Scholar
Bergen, V., Lange, M., Peidli, S., Wolf, F. A. & Theis, F. J. Generalizing RNA velocity to transient cell states through dynamical modeling. Nat. Biotechnol. 38 , 1408–1414 (2020).
Article CAS PubMed Google Scholar
Wolf, F. A. et al. PAGA: graph abstraction reconciles clustering with trajectory inference through a topology preserving map of single cells. Genome Biol. 20 , 59 (2019).
Article PubMed PubMed Central Google Scholar
Efremova, M., Vento-Tormo, M., Teichmann, S. A. & Vento-Tormo, R. CellPhoneDB: inferring cell–cell communication from combined expression of multi-subunit ligand–receptor complexes. Nat. Protoc. 15 , 1484–1506 (2020).
Article CAS PubMed Google Scholar
Bankhead, P. QuPath: Open source software for digital pathology image analysis. Sci. Rep. 7 , 16878 (2017).
Article PubMed PubMed Central Google Scholar
Schindelin, J. et al. Fiji: an open-source platform for biological-image analysis. Nat. Methods 9 , 676–682 (2012).
Article CAS PubMed Google Scholar
Windhager, J., Bodenmiller, B. & Eling, N. An end-to-end workflow for multiplexed image processing and analysis. Preprint at bioRxiv https://doi.org/10.1101/2021.11.12.468357 (2021).
Schapiro, D. et al. HistoCAT: analysis of cell phenotypes and interactions in multiplex image cytometry data. Nat. Methods 14 , 873–876 (2017).
Article CAS PubMed PubMed Central Google Scholar
Ziegenhain, C. & Sandberg, R. BAMboozle removes genetic variation from human sequence data for open data sharing. Nat. Commun. 12 , 6216 (2021).
Article CAS PubMed PubMed Central Google Scholar
Download references
Acknowledgements
The authors would like to thank all participants for their tissue donations and valuable participation in this study. We thank the following Jackson Laboratory (JAX) Scientific Services cores, partially supported through the JAX Cancer Center Support Grant (CCSG) P30CA034196-30, for expert technical assistance: Single Cell Biology, Flow Cytometry and A. Carcio and T. Prosio, Genome Technologies and R. Maurya, Histology, and Microscopy. We also thank the JAX Cyberinfrastructure team for computational resources, L. Perpetua and the UConn Health Research Biorepository, and the UConn Health Surgery Center Personnel for assistance in collection of biopsy samples; the UCHC Pathology and Laboratory Medicine and M. Yu for assistance with histological examination of biopsies; the Clinical and Translational Research Support group, the Sponsored Research Administration service, and the Research Program Development service and A. L. Lucido for administrative assistance. All schematic panels were created using Biorender.com. This study was supported by the Assistance Secretary of Defense for Health Affairs endorsed by the Department of Defense, through the Peer Reviewed Medical Research Program under Award No. W81XWH-19-1-0130 (to E.T.C.), JAX Institutional startup funds (to P.R.) and UCHC/JAX Training Program in Genomic Science T32HG010463 (to M.D.). Opinions, interpretations, conclusions and recommendations are those of the authors and are not necessarily endorsed by the Department of Defense. The funders had no role in study design, data collection and analysis, decision to publish or preparation of the manuscript.
Author information
Authors and Affiliations
The Jackson Laboratory for Genomic Medicine, Farmington, CT, USA
Yuliana Tan, William F. Flynn, Santhosh Sivajothi, Diane Luo, Suleyman B. Bozal, Monica Davé, Paul Robson & Elise T. Courtois
Department of Genetics and Genome Sciences, University of Connecticut School of Medicine, Farmington, CT, USA
Yuliana Tan, Monica Davé & Paul Robson
Department of Obstetrics and Gynecology, University of Connecticut School of Medicine, Farmington, CT, USA
Anthony A. Luciano & Danielle E. Luciano
Institute for Systems Genomics, University of Connecticut, Farmington, CT, USA
Paul Robson
Authors
Yuliana Tan
View author publications
Search author on: PubMed Google Scholar
William F. Flynn
View author publications
Search author on: PubMed Google Scholar
Santhosh Sivajothi
View author publications
Search author on: PubMed Google Scholar
Diane Luo
View author publications
Search author on: PubMed Google Scholar
Suleyman B. Bozal
View author publications
Search author on: PubMed Google Scholar
Monica Davé
View author publications
Search author on: PubMed Google Scholar
Anthony A. Luciano
View author publications
Search author on: PubMed Google Scholar
Paul Robson
View author publications
Search author on: PubMed Google Scholar
Danielle E. Luciano
View author publications
Search author on: PubMed Google Scholar
Elise T. Courtois
View author publications
Search author on: PubMed Google Scholar
Contributions
E.T.C., P.R. and D.E.L. conceived and designed the study. Y.T. and E.T.C. performed and supervised the experiments. Y.T. and E.T.C. optimized the tissue-dissociation protocol. Y.T., D.L., S.B.B. and E.T.C. performed tissue dissociation, FACS and single-cell experiments. D.E.L. and A.A.L. collected consent from participants and clinical samples. S.S. performed IMC experiments. M.D performed organoid immunostaining. Y.T., W.F.F. and E.T.C. performed data analyses. Y.T., W.F.F. and E.T.C. wrote the manuscript and generated figures and schematics. Y.T., W.F.F., A.A.L., P.R., D.E.L. and E.T.C. contributed crucial data interpretation. All authors read or provided comments on the manuscript.
Corresponding authors
Correspondence to Paul Robson , Danielle E. Luciano or Elise T. Courtois .
Ethics declarations
Competing interests
The authors declare no competing interests.
Peer review
Peer review information
Nature Cell Biology thanks Junyue Cao, Chandrakant Tayade and the other, anonymous, reviewer(s) for their contribution to the peer review of this work.
Additional information
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.
Extended data
Extended Data Fig. 1 Overview of experiment design and comparison of bulk RNA-seq and scRNA-seq transcriptomic profiles from Ctrl and endometriosis tissues.
a , Experimental workflow. b , UMAP showing distribution of cell based on tissue types, PID, and endometriosis stage, before and after batch correction with Harmony. c , Box plot showing Spearman’s correlation rank (ρ) between bulkRNA-seq and pseudobulk from scRNA-seq in Eutopic (Ctrl & EuE, n = 144), Peritoneal (EcP & EcPA, n = 90), or Ovary (EcO, n = 24). Each dot represents a sample pair. The box represents the interquartile range with median and minimum/maximum represented by box centerline and whiskers, respectively. d , Scatterplot showing distribution of average gene expression between bulk RNA-seq and scRNA-seq (Spearman ρ). Each dot represents a gene. e , Volcano plots representing DEGs between scRNA-seq pseudo bulk (red) and bulk RNA-seq from undissociated tissue (blue) (edgeR, FDR < 0.001, LogFC > 3). The genes highlighted are exclusively expressed in bulk RNA-seq and associated with erythrocytes (orange), neuronal projections (green), adipocytes (brown), and muscle cells (purple). Related to Fig. 1 .
Extended Data Fig. 2 Proportion of major cell types in each replicate and IMC panel for spatial profiling of Ctrl and endometriosis tissues.
a , Major cell types were determined based on UMAP. The mean distribution for all 5 major cell populations is represented for each tissue type Ctrl, EuE, EcP, EcPA, and EcO (left of the line). Each pie chart represents major cell type proportions for each replicate (right of the line). b , Each antibody was selected according to the cell types identified by the scRNA-seq data analysis. Representative images show single channels for each metal-conjugated antibody in a EuE biopsy. A total of 26 antibodies was used to identify cellular heterogeneity within stromal, endothelial, epithelial, lymphocyte, and myeloid major cell types. Additional antibodies (in ‘Others’) were used to identify cell proliferation (Ki67), active metabolism (pS6), extracellular matrix (Collagen1), and nuclei (DNA). A complete list of cell subpopulations identified through this panel of markers is listed on Supplementary Table 8b . Related to Fig. 1 .
Extended Data Fig. 3 Stromal cell analysis across sample types.
a , Bar plot representing the proportion of stromal cell types in control endometrium and endometriosis lesions. Endometrial fibroblasts were found in all lesions. Fibroblast C7 is the predominant fibroblast type in EcO. b , Density plot showing distribution of mural cells for each tissue. Arrows points to Prv-CCL19. c , Heatmap of markers genes for mural cell subtypes. d , Track plot representing gene expression pattern for selected DEG in Prv-CCL19 subpopulations. GGT5 and ABCC9 are pan-markers for this cell subtype. e , Box plot showing the proportion of CCL19- expressing cells in Prv-CCL19 subpopulation within each tissue type. Each dot represents the percentage of CCL19 + cells in a tissue biopsy (Ctrl n = 3, EuE n = 9, EcP n = 8, EcPA n = 6, EcO n = 4). The box represents the interquartile range with median and minimum/maximum represented by box centerline and whiskers, respectively. Related to Fig. 2 .
Extended Data Fig. 4 Characterization of endothelial cells (EC) across sample types.
a , Unique cell-to-cell interaction counts obtained from a modified CellPhoneDB procedure. To recover meaningful interactions, we analyzed ligand-receptor interaction in each sample independently. Unique interactions in each tissue type are counted as follows; each ligand-receptor pair observed in a specific cell type pair is counted as one interaction; this is tabulated for all possible pairwise cell type combinations (up to 58 subpopulations in this study) within a sample (n). The total count (Σ, n_celltype_pairs) represents the commonality of the ligand-receptor interaction of interest. The more common interactions (observed in multiple cell type pairs and in all individual samples) will have higher counts while restricted interactions (observed in specific cell type pairs) will have lower counts. We arbitrarily restricted our analysis to interactions observed fewer than 150 times to narrow the scope of analysis and focus on potentially uncovering unique cell-to-cell interactions. b , Box plot showing the proportion of DLL4- expressing cells in EC-tip subpopulation within each tissue type. c , Density plot showing distribution of endothelial cells for each tissue. d , EC proportions by sample type. e , AQP1 + cell abundance is substantially increased in peritoneal lesions (EcP and EcPA). f , (top) Proportion of aPCV among ECs across tissue types. (bottom) Swarm plot showing AQP1 expression per cell. Horizontal lines represent the median value. For box plots, each dot represents percentage of DLL4+ cells in EC-tip cluster (b) or AQP1+ cells in EC-aPCV cluster (e), in a tissue biopsy (Ctrl n = 3, EuE n = 9, EcP n = 8, EcPA n = 6, EcO n = 4). The box represents the interquartile range with median and minimum/maximum represented by box centerline and whiskers, respectively. Related to Fig. 3 .
Extended Data Fig. 5 Myeloid cell diversity in control and endometriosis.
a , Heatmap representing marker genes for each myeloid subpopulation. b , Dendrogram showing the hierarchical clustering (Pearson correlation) for the myeloid cell clusters. c , Bar plot showing the representation of each myeloid subtype across tissue types. Related to Fig. 4 .
Extended Data Fig. 6 DC subpopulations.
a , Bar plot represents the proportion of DCs among all myeloid cells for each patient (Ctrl n = 3, EuE n = 9, EcP n = 8, EcPA n = 6, EcO n = 4). Patient-to-patient variability was observed in DC proportions within the myeloid population and across different tissue types. The box represents the interquartile range with median and minimum/maximum represented by box centerline and whiskers, respectively. b , PAGA and RNA velocity trajectory analyses suggest that pre-cDC2 differentiate towards cDC2 and DC3 in Ctrl and EuE. Red arrows indicate that some cDC2 and DC3 cells derive from a smaller intermediate cell population. c , Cell cycle analysis for pre-cDC2, cDC2 and DC3 populations. d , Expression of DC progenitor markers FLT3 , AXL , and SIGLEC6 . e , Phagocytosis pathway is enriched in cDC2 subpopulations of peritoneal lesions. Bar plot shows the Normalized Enrichment Score (NES) for the top 10- GSEA pathways in cDC2 cells of EuE and EcPA (FDR < 0.1). Related to Fig. 5 .
Extended Data Fig. 7 Lymphocyte subpopulations in control and endometriosis tissues.
a , Density plot showing distribution of lymphocyte cells for each tissue. b , Dot plot representing marker genes for each lymphocyte subpopulation, including four natural killer cell (NK) clusters, innate lymphoid cells (ILCs), effector memory T-cells (T EM ), cytotoxic T-lymphocytes (CTL), naïve/central memory T-cells (T N /T CM ), T regulatory cells (T Reg ), CD4- and CD8- tissue resident T cell (CD4-T RM and CD8-T RM , respectively), CD8 ﻿mucosal-associated invariant T cells (CD8-MAIT), plasma cells, and B cells. c , Representative IMC images showing the presence and proximity of myeloid cells labelled with CD68 (yellow) with T cells labelled with CD3 (cyan), and T Reg labelled with FOXP3 (magenta) in EcO (n = 5); nuclei are marked with DNA intercalation (blue). Scale bar = 100 μm. d , Proportion bar plot of CTLA4 expressing cells from the total T Reg subpopulation. e , Proportion box plot of BCL6 , SEMA4A , CXCR5 expressing cells from the total B cells within each sample type. For box plots, each dot represents a unique patient (Ctrl n = 3, EuE n = 9, EcP n = 8, EcPA n = 6, EcO n = 4). The box represents the interquartile range with median and minimum/maximum represented by box centerline and whiskers, respectively. Related to Fig. 6 .
Extended Data Fig. 8 Characterization of in vivo epithelial and in vitro endometrial epithelial organoid (EEO) cells.
a , Proportions of epithelial subpopulations per sample type. b , Representative IMC images of MUC5B+ epithelial cells in eutopic endometrium (Ctrl: C07, EuE: E12, E06) from multiple tissues. Epithelial cells are marked with PanCK, EpCAM, E-cadherin (green); MUC5B (magenta); nuclei (white). Scale bar = 100 μm. c , Proportion box plot of SAA1 expressing cells from the total MUC5B+ cells within each sample type. Each dot represents a unique patient (Ctrl n = 3, EuE n = 9, EcP n = 8, EcPA n = 6, EcO n = 4). The box represents the interquartile range with median and minimum/maximum represented by box centerline and whiskers, respectively. d , Sequencing metrics from EEO scRNA-seq; UMIs and unique genes counts are shown for Control (C) and endometriosis (E) patients and across tissue type. Undetermined (UD) group represents single cells which could not be assigned due to the lack of multiplexing hashtag but otherwise passed QC. e , Density plot showing distribution of EEO cells derived from Ctrl, EuE, EcP, and EcPA (UD cells were not included). f , UMAP showing the co-expression of MUC5B, SAA1, TFF3 , and RUNX3 in the MUC5B+ population comprising in vivo epithelial cells and EEO. Related to Fig. 7 .
Extended Data Fig. 9 MUC5B+ cells display a progenitor-like capacity in in vitro organoid culture.
a , Schematic and FACS sorting gating strategy to isolate MUC5B+ and MUC5B − epithelial cells from eutopic tissue for organoid generation. b , Representative brightfield images showing the progression of organoid generation from sorted single cells at day 2, 6 and 10. MUC5B+ cells formed EEO faster than MUC5B − cells. Each panel shows a whole Matrigel dome and magnified organoids are shown in the inset. Inset scale bar = 100 μm. c , Line graph showing area (top) and number (bottom) of EEO generated from MUC5B+ (dark blue, n = 1) and MUC5B − (sky blue, n = 1) cells over time. Area and Count of EEO is significantly higher in MUC5B+ compared to MUC5B − (paired t-test, two-tailed p < 0.0001). d , IF staining of EEO generated from MUC5B+(n = 1) and MUC5B- (n = 1) sorted cells showing the co-localization of endometrial epithelial (E-Cadherin, in green) and MUC5B+ (magenta) staining. Nuclei were counterstained with DAPI (gray). Scale bar = 100 µm. Related to Fig. 7 .
Source data
Extended Data Fig. 10 Schematic illustrating the proposed microenvironment alterations for ectopic peritoneal and ovary lesions.
In peritoneal lesion (left), the proportion of myeloid and endothelial is increased, and endometrial-like epithelial population is reduced. CCL19-expressing perivascular cells mediate immune cell recruitment, such as macrophages and T cells, which contributes to the immunomodulatory microenvironment. We observe the presence of MSR1-expressing dendritic cells contributing to immunomodulation. TLS is also observed in some lesions. In addition, Mø1-LYVE1 and perivascular cells contribute to angiogenesis by regulating endothelial tip proliferation. In contrast, ovarian ectopic lesions (right) show a striking increase in the proportion of stromal cell and a reduced endometrial-like-epithelial cell presence. The immunomodulatory microenvironment is mainly driven by Mø1-LYVE1 expressing IL10. In ovary lesions, the regulation of angiogenesis is marked by endothelial cell arrest, resulting in mature vasculature. Created with Biorender.com.
Supplementary information
Reporting Summary (download PDF )
Supplementary Tables (download XLSX )
Supplementary Table 1: Demographic and endometrium histology of participants. Related to Figs. 1 and 6, Extended Data Figs 1 and 2, and Supplementary Fig. 1. Supplementary Table 2: Experiment performed on each tissue. Oral contraceptive status is decoded as treated (Y) and non-treated (N). Supplementary Table 3: Marker genes expressed by 5 major cell types and 57 subpopulations found in this study. Significance was determined by two-sided Wilcoxon rank-sum test, P values were adjusting using Benjamini–Hochberg correction. The ‘in_group_fraction’ denotes the fraction of cells expressing the marker gene within the intended cluster, and ‘out_group_fraction’ denotes the fraction of cells expressing the marker gene outside the intended cluster. Related to Fig. 1d. Supplementary Table 4: DEGs between transcriptome obtained from scRNA-seq and bulk RNA-seq. Significance was determined with edgeR exact test (two-sided) and P values were adjusted using Benjamini–Hochberg correction (FDR < 0.001). Related to Extended Data Fig. 1e. Supplementary Table 5: Top 1,000 DEGs between tissue type within each subpopulation, in order from left to right: dS2, Prv-CCL19, EC tip, EC-aPCV, EC-PCV, Mɸ1-LYVE1, Mɸ4-infiltrated, cDC2, T Reg , B cell. Significance was determined with edgeR quasi-likelihood F -test (two-sided), and P values were adjusted using Benjamini–Hochberg correction. Related to Figs. 2–5 and Extended Data Fig. 2. Correction (FDR < 0.01). A comprehensive list of the 46 cell subpopulation that this analysis was performed on is available upon request. Related to Figs. 2–6. Supplementary Table 6: List of 802 unique ligand–receptor interactions in each tissue type. A comprehensive list of ligand-–receptor interactions (including common interactions) is available on GitHub (Methods). Related to Fig. 3, Figs. 6 and 7, and Extended Data 4a. Supplementary Table 7: Enriched gene ontology in each biopsy type in comparison to control endometrium, in Mɸ1-LYVE1 (top) and cDC2 (bottom). Significance was determined with GSEA Fisher’s exact test (one-sided), and P values were adjusted using Benjamini–Hochberg correction (FDR < 0.1). ES: enrichment score; NES: normalized enrichment score. A comprehensive list of the 46 cell subpopulation that this analysis was performed on is available upon request. Related to Fig. 5 and Extended Data Fig. 6e. Supplementary Table 8: Additional information about cell hashtaging reagents used in this study. Related to Fig. 7 and Extended Data Fig. 8. Supplementary Table 9: Detailed information about antibodies used for IMC in this study. Related to Figs. 1–4, Figs. 6 and 7, and Extended Data Figs. 2, 7 and 8. Supplementary Table 10: Additional information about antibodies used for FACS in this study. Related to Extended Data Fig. 9.
Source data
Source Data Fig. 2 (download XLSX )
Statistical source data.
Source Data Extended Data Fig. 9 (download XLSX )
Statistical source data.
Rights and permissions
Springer Nature or its licensor holds exclusive rights to this article under a publishing agreement with the author(s) or other rightsholder(s); author self-archiving of the accepted manuscript version of this article is solely governed by the terms of such publishing agreement and applicable law.
Reprints and permissions
About this article
Cite this article
Tan, Y., Flynn, W.F., Sivajothi, S. et al. Single-cell analysis of endometriosis reveals a coordinated transcriptional programme driving immunotolerance and angiogenesis across eutopic and ectopic tissues. Nat Cell Biol 24 , 1306–1318 (2022). https://doi.org/10.1038/s41556-022-00961-5
Download citation
Received : 29 July 2021
Accepted : 09 June 2022
Published : 21 July 2022
Version of record : 21 July 2022
Issue date : August 2022
DOI : https://doi.org/10.1038/s41556-022-00961-5
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
Sign up for the Nature Briefing newsletter — what matters in science, free to your inbox daily.
Email address
Sign up
I agree my information will be processed in accordance with the Nature and Springer Nature Limited Privacy Policy .
Close
Get the most important science stories of the day, free in your inbox. Sign up for Nature Briefing
