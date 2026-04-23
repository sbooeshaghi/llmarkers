Single-cell transcriptomic atlas of the human endometrium during the menstrual cycle | Nature Medicine
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
Single-cell transcriptomic atlas of the human endometrium during the menstrual cycle
Published: 14 September 2020
Single-cell transcriptomic atlas of the human endometrium during the menstrual cycle
Wanxin Wang ORCID: orcid.org/0000-0001-8919-9332 1 na1 ,
Felipe Vilella 2 , 3 na1 ,
Pilar Alama ORCID: orcid.org/0000-0003-0204-0826 4 ,
Inmaculada Moreno 2 , 3 ,
Marco Mignardi 5 ,
Alina Isakova 1 ,
Wenying Pan 1 ,
Carlos Simon 2 , 3 , 6 &
…
Stephen R. Quake ORCID: orcid.org/0000-0002-1613-0809 1 , 5 , 7
Nature Medicine volume 26 , pages 1644–1653 ( 2020 ) Cite this article
46k Accesses
558 Citations
106 Altmetric
Subjects
Reproductive biology
RNA sequencing
Transcriptomics
Abstract
In a human menstrual cycle the endometrium undergoes remodeling, shedding and regeneration, all of which are driven by substantial gene expression changes in the underlying cellular hierarchy. Despite its importance in human fertility and regenerative biology, our understanding of this unique type of tissue homeostasis remains rudimentary. We characterized the transcriptomic transformation of human endometrium at single-cell resolution across the menstrual cycle, resolving cellular heterogeneity in multiple dimensions. We profiled the behavior of seven endometrial cell types, including a previously uncharacterized ciliated cell type, during four major phases of endometrial transformation, and found characteristic signatures for each cell type and phase. We discovered that the human window of implantation opens with an abrupt and discontinuous transcriptomic activation in the epithelia, accompanied with a widespread decidualization feature in the stromal fibroblasts. Our study provides a high-resolution molecular and cellular characterization of human endometrial transformation across the menstrual cycle, providing insights into this essential physiological process.
You have full access to this article via California Institute of Technology .
Similar content being viewed by others
An integrated single-cell reference atlas of the human endometrium
Article Open access 28 August 2024
Time-series single-cell transcriptomic profiling of luteal-phase endometrium uncovers dynamic characteristics and its dysregulation in recurrent implantation failures
Article Open access 02 January 2025
SFRP4 + stromal cell subpopulation with IGF1 signaling in human endometrial regeneration
Article Open access 27 September 2022
Main
The human menstrual cycle—with its monthly remodeling, shedding and regeneration of the endometrium—is not shared with many other species. Similar cycles have been consistently observed only in humans, apes, Old World monkeys 1 , 2 , molossid bats 3 and spiny mice ( Acomys cahirinus ) 4 , and not in any of the commonly used model organisms that undergo sexual reproduction such as the mouse, zebrafish or fly. A cycle can be primarily divided into two major phases by the event of ovulation: the proliferative (preovulatory) and the secretory (postovulatory) 5 . During the secretory phase, the endometrium enters a narrow window of receptive state that is both structurally and biochemically ideal for embryo implantation 6 , 7 —that is the window of implantation (WOI) or mid-secretory phase. Given its relevance to human fertility and regenerative biology, a systematic characterization of endometrial transformation across the menstrual cycle has long been pursued.
The endometrium is unlike any other tissue, consisting of multiple cell types that vary dramatically in state through a monthly cycle as they enter and exit the cell cycle, remodel and undergo various forms of differentiation at relatively rapid rates. Histology has established morphological definitions of menstrual, proliferative, early-, mid-, and late-secretory phases 5 . Whole-tissue transcriptomic profiling advanced the definition to a molecular and quantitative level 8 , 9 , and has been translated into clinics to determine the timing of the WOI for in vitro fertilization and embryo transfer 10 . Here, we sought to decouple and define endometrial cell types and states with minimum bias, leveraging the high resolution of single-cell RNA-sequencing (RNA-seq). By studying both the static and dynamic aspects of the tissue, we discovered molecular characterizations of hallmark events such as the WOI, and provide a systematic single-cell transcriptomic delineation of endometrial transformation at the levels of cell type, state, proliferation and differentiation across the human menstrual cycle.
Results
To characterize endometrial transformation across the natural human menstrual cycle we collected endometrial biopsies from 19 healthy ovum donors, 4–27 days after the onset of their menstrual bleeding (see Methods and Extended Data Fig. 1a–c ). All women had regular menstrual cycles when the biopsies were taken, with no influence from exogenous hormones or gynecologic pathology. Single cells were captured and complementary DNA was generated using Fluidigm C1 medium chips. To validate results from the C1 dataset, we collected additional data from ten healthy ovum donors using the 10x Chromium system (see Methods and Extended Data Fig. 1b ).
Dimensional reduction via t -distributed stochastic neighbor embedding ( t -SNE) 11 on the top overdispersed genes revealed clear segregation of cells into distinct groups (Fig. 1a ). We defined cell types as segregations that were not time associated—that is, groups encompassing cells sampled across the menstrual cycle. Six cell types were thus identified; canonical markers and highly differentially expressed genes enabled straightforward identification of four of these: stromal fibroblast, endothelium, macrophage and lymphocyte (Fig. 1b ). The two remaining cell types both express epithelium-associated markers, one of which is characterized by an extensive list of uniquely expressed genes. Functional analysis 12 , 13 revealed that 56% (Supplementary Fig. 1 ) of genes in this list are annotated with a cilium-associated cellular component or biological process (Fig. 1c ), thereby identifying this cell type as ‘ciliated epithelium’, specifically with motile cilia 14 . We defined the other epithelial cell type as ‘unciliated epithelium’. Lastly, we used the 10x dataset to test whether additional cell types would be captured with a substantially larger sample size and found that the only cell type consistently captured by 10x but not by the C1 dataset is smooth muscle cell (Fig. 1d and Extended Data Fig. 2a–e ). Given that this cell type has an abundance comparable to that of macrophages (Extended Data Fig. 2c,d ), it is likely that it escaped the C1 capture sites due to its shape and size. Expression of PDGFRB , MCAM and SUSD2 (Extended Data Fig. 2f–h ) suggests that this smooth muscle cell type contains previously identified endometrial cells with mesenchymal stem cell characteristics 15 , 16 .
Fig. 1: Human endometrium consists of seven cell types across the menstrual cycle.
The alternative text for this image may have been generated using AI.
Full size image
a , Dimension reduction ( t -SNE) on 2,148 single cells from 19 healthy human endometria across the menstrual cycle using the top 1,000 overdispersed genes across all cells. Top right inset: t- SNE on immune cells using the top 1,000 overdispersed genes across immune cells only. Boundaries of cell types were defined by density-based spatial clustering of applications with noise on the two-dimensional t -SNEs (2d- t- SNEs). b , Top discriminatory genes for each identified cell type. Shown are differentially expressed genes (–log 10 ( P adj of Wilcoxon’s rank-sum test) > 30, log 2 (FC) > 2) expressed in >85% of cells of the given cell type. For each cell type, genes were ordered from top to bottom by the ratio (percentage of cells within the cell type expressing a gene)/(percentage of cells from other cell types expressing the same gene). In the column at the far right, genes colored purple are canonical markers for a cell type. The color bar at the top denotes cell types shown in a . c , Cellular components and biological processes enriched in top discriminatory genes for ciliated epithelium. d , Dimension reduction (uniform manifold approximation and projection (UMAP) on top PCs) on 71,032 single cells from ten healthy human endometria revealed an additional smooth muscle cell type. See also Extended Data Figs. 1 and 2 .
Using RNA and protein costaining (see Methods ), we validated previously unannotated discriminatory markers and epithelial lineage identity for endometrial ciliated cells and visualized the spatial distribution of these cells in situ. Four genes were selected for RNA staining, as these were highly discriminatory for the cell type (Fig. 1b ) but either had no previous functional annotation ( C11orf88 , C20orf85 , FAM183A ) or were annotated with noncilia-associated functionality ( CDHR3 ) (Supplementary Table 1 ). We found consistent coexpression of all four genes with FOXJ1 protein (canonical master regulator for motile cilia with epithelial lineage identity) in both glandular (Fig. 2a,c ) and luminal (Fig. 2b,d ) epithelia on day 17 (Fig. 2a,b ) and day 25 (Fig. 2c,d ) of the menstrual cycle. The results validated these ciliated cells as an epithelial cell type embedded in both luminal and glandular epithelia in healthy human endometrium across the menstrual cycle, and also demonstrated the consistent discriminatory power of the new markers we identified (Fig. 2e and Supplementary Dataset 1 ) across the cycle.
Fig. 2: Marker validation and spatial visualization of endometrial ciliated cells.
The alternative text for this image may have been generated using AI.
Full size image
a – d , Representative images of human endometrial epithelial glands ( a , c ) and lumen ( b , d ) on day 17 ( a , b ) and day 25 ( c , d ) of the menstrual cycle—that is, the number of days after the onset of last menstrual bleeding. Single CDHR3 and C11orf88 RNA molecules appear as dots colored cyan and magenta, respectively. FOXJ1 antibody staining is colored green and nuclei gray. Close-up panels (right) contain triple-expressing cells seen in the white dashed box in the main panel to the left. e , Integrated intensity of FOXJ1 antibody from all images on day 17 (left) and day 25 (right) for double RNA-positive (++) and -negative (– –) cells of marker combination CDHR3 , C11orf88 (black) and C20orf85 , FAM183A (gray). ++: cells expressing at least four RNA molecules of both markers; horizontal line: median. Two-sided testing was used to derive P values. For day 17, eight and nine representative fields of view ( n ) were captured as z-stacked images for marker combinations CDHR3 , C11orf88 (set1) and C20orf85 , FAM183A (set2), respectively. For day 25, eight and ten representative fields of view were captured as z-stacked images for set1 and set2, respectively. No images were excluded in analyses to derive the results shown in Fig. 2e , and data from all images are available in Supplementary Dataset 1 .
Human endometrial transformation consists of four major phases across the menstrual cycle
Samples were taken throughout the menstrual cycle and annotated by the day of menstrual cycle (number of days after the onset of last menstrual bleeding). While the time variable serves as an informative proxy for assignment of endometrial states, it is susceptible to bias due to variances in menstrual cycle length between and within women 17 , and limited in resolution due to variance of cells within an individual. To study transcriptomes of endometrial transformation in an unbiased manner, we performed within-cell type t -SNE using whole-transcriptome data from unciliated epithelia and stromal fibroblasts, respectively, representing the two major contributing cell types to endometrial transformation. The results revealed four major phases for both cell types, which we refer to as phases 1–4 (Extended Data Fig. 3a ). Although the four phases were clearly time associated, examples where the orders were reversed for two women between their phase assignments and their day of menstrual cycle, and cases where women on the same day of cycle were assigned into different phases (Extended Data Fig. 1b ), demonstrate variations in menstrual cycle length as well as the bias and imitated resolution if we were to use the day of menstrual cycle directly for characterizations.
The WOI opens with an abrupt and discontinuous transcriptomic activation in unciliated epithelia
We used a mutual information (MI) 18 -based approach (see Methods and Extended Data Fig. 3b ) to build a model that not only retains phase-wise characteristics but also allows the assignment of each cell to a pseudotime along the time trajectory of a menstrual cycle (Fig. 3a and Extended Data Fig. 3c ). We observed high correlations between time and pseudotime (Fig. 3b ), and between pseudotimes of unciliated epithelia and stromal fibroblasts from the same woman (Fig. 3c ), supporting the validity of the trajectory. Notably, we observed a notable discontinuity in the time trajectory of unciliated epithelia between phase 4 and the preceding phases (Fig. 3a , left). This discontinuity was consistently observed regardless of the method we used for dimension reduction (Supplementary Fig. 2a,b ) or feature enrichment (Supplementary Fig. 2c ). This is unlikely to be an artifact of sampling density, given that the involved biopsies were taken with a maximum interval of 1 day (Extended Data Fig. 1b,c ) and that a similar discontinuity was not observed in the stromal fibroblast counterpart (Fig. 3a , right).
Fig. 3: Construction of single-cell resolution trajectory of endometrial transformation across the human menstrual cycle.
The alternative text for this image may have been generated using AI.
Full size image
a , Pseudotime assignment of unciliated epithelia (epi) and stromal fibroblasts (str) across the trajectory of a menstrual cycle. For both cell types, the trajectory was constructed as a principal curve on the 2d- t -SNE obtained using time-associated genes ( Methods ). 1–4: the four major phases consistently identified using either the whole transcriptome (Extended Data Fig. 3a ) or time-associated genes (Extended Data Fig. 3c ). Start: pseudotime 0, assigned based on the clinical definition of the start of a cycle. b , Correlation of pseudotime and time (day) for epi and str from each woman. c , Correlation of pseudotimes of epi and str from the same woman. b , c , Dots and error bars are the median and median absolute deviation, respectively, of all epi or str from a woman; see source data for n values—that is, the numbers of epi or str, respectively, from each woman that were used to derive her sets of median and mad. See Statistics and reproducibility for detailed description of the source data . Day: the day of menstrual cycle. See also Extended Data Fig. 3 .
Source data
To understand the nature of this discontinuity, we identified genes that were dynamically changing along the single-cell trajectories of endometrial transformation via MI calculation (see Methods and Extended Data Fig. 4a ). Ordering these genes based on the pseudotime at which their global maximum was estimated to occur (pseudotime max ; Methods ) revealed the global features of transcriptomic dynamics across the menstrual cycle (Extended Data Fig. 4b ). In unciliated epithelia, the dynamics demonstrated an overall continuous feature across phases 1–3 until an abrupt and uniform activation of a gene module marked the entrance into phase 4. Genes in this module included PAEP , GPX3 and CXCL14 (Fig. 4a ), which have consistently been reported in whole-tissue transcriptomic datasets as overexpressed in the WOI despite notable discrepancies between whole-tissue profiling results 9 , 10 , 19 . Thus, entrance into phase 4 can be identified with the opening of the WOI or the mid-secretory phase.
Fig. 4: Temporal transcriptome dynamics of endometrial transformation across the human menstrual cycle.
The alternative text for this image may have been generated using AI.
Full size image
a – c , Exemplary phase- and subphase-defining genes, and the relationship between single-cell transcriptomically defined and histologically defined endometrial phases for unciliated epithelia (epi) ( a ) and stromal fibroblasts (str) ( b ) across a human menstrual cycle ( c ). Shown are genes that were differentially expressed (–log 10 ( P adj of Wilcoxon’s rank-sum test) > 10, log 2 (FC) > 1) in a phase or subphase. Genes were further filtered for their potential to be deconvolutated between epi and str in whole-tissue data to obtain either (1) those that are temporally in synchrony between the two cell types or (2) those with negligible expression in one cell type across the cycle but major phase-specific dynamics in another. Cells (columns) are ordered by pseudotime. Dashed lines: within-phase transition; solid lines: boundaries between the four phases assigned in Fig. 3a ; pro: proliferative; sec: secretory. The complete phase-defining gene lists can be found in Supplementary Table 4 ; see also Extended Data Figs. 4 – 7 and 9 .
The WOI is characterized by widespread decidualization features in stromal fibroblasts
Unlike their epithelial counterparts, transcriptomic dynamics in stromal fibroblasts demonstrate discrete stages where genes are upregulated in a modular form (Fig. 4b and Extended Data Fig. 4b , right). In phase 4 stromal fibroblasts the upregulated gene module includes DKK1 and CRYAB , among a few others that were recapitulated by consensus among whole-tissue analysis, and further confirms the identity of the WOI 9 , 10 , 19 although the transition was not as abrupt as in their epithelial counterparts. In the same module we noticed the decidualization-initiating transcriptional factor FOXO1 (ref. 20 ) and decidualization stromal marker IL15 (ref. 21 ). Importantly, while their upregulation in phase 4 was obvious, their expression was already noticeable in phase 3 in a lower percentage of cells and at a lower expression level.
Decidualization is the transformation of stromal fibroblasts where they change from elongated, fibroblast-like cells into enlarged round cells (Fig. 4c ) with specific cytoskeleton modifications, playing essential roles in embryo invasion and pregnancy development 22 . Our data suggest that this process is initiated before the opening of the WOI in a small percentage of stromal fibroblasts, and that at the receptive state of tissue decidualization features are widespread in stromal fibroblasts, in agreement with histologic observations 5 . Our analysis therefore shows that the transition into the receptive phase of the endometrium occurs with an abrupt transcriptomic activation in the unciliated epithelia to reach a state where WOI-associated genes are uniformly and highly upregulated, in contrast to a more gradual transition in stromal fibroblasts.
Using dimensional reduction and the two ‘anchor biopsies’ that were shared between the C1 and 10x datasets (see Methods ), we were also able to assign biopsies in the 10x dataset to their respective phases (Extended Data Fig. 5a–c ). To further increase our resolution in characterizing opening of the WOI, we looked into the 10x dataset where six of the ten biopsies were between days 19 and 23 (Extended Data Fig. 1b ) of the menstrual cycle, when WOI opening is likely to occur. Using the two anchor biopsies (see Methods ) as points of reference, seven of the ten biopsies were ordered between early- and mid-secretory phase (Extended Data Fig. 5c ). Examining WOI-associated genes across these biopsies confirmed the more abrupt WOI gene activation in unciliated epithelia than in stromal fibroblasts (Extended Data Fig. 5d,e ). Moreover, with increased resolution in time and stratification between two epithelial subtypes (which we show to be glandular and luminal epithelia), we observed finer dynamics of WOI gene activation in unciliated epithelia in both their differential timing and spatial pattern (Extended Data Fig. 5d ). For example, MAOA and NUPR1 activation preceded DPP4 although this occurred at a comparable level in both subtypes of unciliated epithelium. Activation of CXCL14 , GPX3 and PAEP in luminal epithelia lagged behind that in their glandular counterparts. Nonetheless, it was not until all WOI genes were highly and uniformly upregulated in both subtypes that temporal progression reached the anchor-biopsy-defined WOI state, exactly as observed in the C1 dataset.
The WOI closes with continuous transcriptomic transitions
While the WOI opens with an abrupt transcriptomic transition in unciliated epithelia, it closes with more gradual transition dynamics (Fig. 4a and Extended Data Fig. 4b , left). Genes expressed in phase 4 unciliated epithelia were featured by three major groups with distinct dynamic characteristics. Group 1 genes (for example, PAEP , GPX3 ) had sustained expression throughout phase 4 and their expression remained noticeable in phase 1 of a new cycle. Towards later phase 4, group 2 genes (for example, CXCL14 , MAOA , DPP4 and metallothioneins) notably declined whereas group 3 genes (for example, THBS1 , MMP7 ) were upregulated and sustained in phase 1 of a new cycle. Group 2 and 3 genes thus help to identify the transition from mid- to late-secretory phase 9 , 19 and hence closure of the WOI, while all three gene groups—their expression and lack thereof—can be used to differentiate the WOI from the remaining endometrial phases. Similarly the parallel transition in stromal fibroblasts was featured by three characteristic gene groups with continuous dynamics (Fig. 4b and Extended Data Fig. 4b , right) and represented the progression of decidualization in a natural human menstrual cycle, which, differing from that during pregnancy, ultimately leads to shedding of the endometrium.
WOI-associated transcriptional regulators are featured with characteristic regulatory roles at opening and closure of the WOI
Global transcriptional regulator (TF) dynamics (see Methods and Supplementary Table 2 ) in unciliated epithelia demonstrated a single major discontinuity (Extended Data Fig. 6a ), whereas in stromal fibroblasts no comparable discontinuity was observed (Extended Data Fig. 6b ). We found that TFs that peaked during the WOI (group 1) were enriched with notably different functional roles than those that peaked at the end of the cycle (group 2) (Extended Data Fig. 6c,d ). In unciliated epithelia, group 1 TFs were enriched with early developmental regulators, especially in differentiation ( IRX3, PAX8, MITF, ZBTB20 ) whereas group 2 included those associated with endoplasmic reticulum stress ( DDIT3 ) and immediate early genes ( FOS, FOSB, JUN ). In stromal fibroblasts, group 1 contained regulators of cAMP pathway-mediated chondrocyte differentiation ( BHLHE40, ATF3 )—probable drivers for decidualization—whereas group 2 included those associated with endoplsasmic reticulum stress ( YBX3, ZBTB16 ), inflammation ( CEBPD ) and apoptosis ( STAT3 ). Of note, the concurrent upregulation of MTF1 , encoding an activator of the metallothionein I promoter (Extended Data Fig. 6c ), with metallothionein I genes ( MT1F , 1X , 1E , 1G ; Fig. 4a ) in unciliated epithelia, suggests that these heavy-metal-binding proteins may be a key regulatory module associated with the WOI.
Nuclear receptors for steroid hormones are a special group of TFs mediating communication between endometrium and other female reproductive organs. The decline in messenger RNA (mRNA) level of estrogen receptor ( ESR1 ) and progesterone receptor ( PGR ) from proliferative (phases 1 and 2) to secretory phases (phases 3 and 4) in both cell types agrees with previous proteomic 23 and histological 24 , 25 analyses, although the decrease in PGR in stromal fibroblasts quantified at the histological level was more moderate and lagged behind compared to that at the mRNA level (Extended Data Fig. 6e ).
Similar analyses were performed on genes encoding secretory proteins (Extended Data Fig. 7a–d and Supplementary Table 3 ). IGFBP1 and PRL are two secretory proteins canonically used to identify endometrial decidualization during early pregnancy 22 . In the absence of pregnancy, patchy expression of IGFBP1 during mid-secretory phase endometrium in both epithelia and stromal fibroblasts was reported by in situ mRNA staining 26 . We observed higher abundance of IGFBP1 -expressing cells in unciliated epithelia than in their stromal counterparts during mid-secretory phase, supported by both our C1 (Extended Data Fig. 7e,f ) and 10x datasets (Extended Data Fig. 8a ); PRL , however, showed low expression in both cell types across the cycle.
Two single-cell studies 27 , 28 on early-pregnant human endometrium reported three subtypes of stromal fibroblasts, including one distinct subtype that co-upregulates IGFBP1 and PRL . We did not, however, observe notable subtype segregation in stromal fibroblasts (Fig. 3 ) and observed limited numbers of cells co-expressing IGFBP1 and PRL in mid- to late secretory phase (Extended Data Fig. 7e,f ), suggesting a less heterogeneous cellular hierarchy than that in early-pregnant endometrial stromal fibroblasts. Examination of our 10x dataset (Extended Data Fig. 8a,b ), where sampling was higher by over an order of magnitude, indicates that this relative homogeneity was not due to undersampling but, rather, to a lack of PRL expression. More specifically, although IGFBP1 -expressing stromal fibroblasts ( IGFBP1 + , blue in Extended Data Fig. 8a ) increased notably from mid- to late-secretory phase (Extended Data Fig. 8a , top), PRL -expressing cells ( PRL + , yellow in Extended Data Fig. 8a ) remained low and hence were cells expressing both genes ( IGFBP1 + PRL + , red in Extended Data Fig. 8a ). In addition, aforementioned early pregnancy studies 27 , 28 reported further division of stromal fibroblasts that do not co-upregulate IGFBP1 and PRL into two subtypes. Expression profiles of genes reported to define the two subtypes (Extended Data Fig. 8c,d )—for example, ACTA2 and IGFBP1 —revealed that decidualizing stromal fibroblasts in nonpregnant and naturally cycling endometrium, although less heterogeneous, demonstrate the potential to differentiate into the hierarchy in early pregnancy.
Relationship between endometrial phases identified at the single-cell transcriptome level and those defined canonically
Since its formalization in the 1950s 5 , a histological definition of endometrial phases—that is, the proliferative, early-, mid- and late-secretory phases—has been used as the gold standard in determining endometrial state. We therefore explored the relationship between histological phases with phases we identified at the single-cell level. Cell mitosis is one of the most distinct features of the proliferative phase endometrium. Thus, to identify the boundary between proliferative and secretory phases, we explored cell cycle activities across the menstrual cycle (see Methods and Extended Data Fig. 9a,b ). For both unciliated epithelia and stromal fibroblasts, cell cycling was elevated in phases 1 and 2 and ceased in later phases (Extended Data Fig. 9c,d ), indicating that the transition from proliferative to secretory phase occurred between phases 2 and 3. Characteristic signatures (Supplementary Table 4 ), enriched biological processes (Supplementary Table 5 ) and association with whole-tissue-level results for phases 1–4 further confirmed this assignment (see Methods ). With this boundary identified and the anchor provided by the WOI, phase 3 can thus be associated with early secretory phase and phases 1 and 2 can be identified as early and late proliferative phase, respectively. Histology suggests that transformation in the proliferative endometrium has gradual morphological changes that do not permit the recognition of distinct subphases 5 . We discovered, however, that at the transcriptomic level, proliferative endometrium can be divided into two distinct phases in both unciliated epithelia and stromal fibroblasts that can be quantitatively identified by transcriptomic signatures (Extended Data Fig. 9e,f ). We did not identify a distinct mid-proliferative phase.
Transcriptome signatures in deviating glandular and luminal epithelium
In unciliated epithelia, we noticed further segregation of cells in the direction perpendicular to the overall trajectory of the menstrual cycle in both our C1 (Fig. 5a and Supplementary Fig. 3a–c ) and 10x (Extended Data Figs. 2a and 10a ) datasets. Among genes that consistently differentiated the subpopulations across multiple phases (Fig. 5b–d and Extended Data Fig. 10b ), we found those that were associated with luminal and glandular epithelia. For example, WNT7A was overexpressed in one subpopulation in all proliferative phases (Fig. 5c ), and its exclusive expression in the luminal epithelia of human 29 , primate 30 and mouse 31 endometrium has been demonstrated in situ. Similarly, we observed differential expression of LGR5 , ITGA1 and FOXA2 in one of the two subpopulations across multiple phases (Fig. 5c,d ), and previous in situ studies have reported their differential expression between luminal and glandular epithelia in both humans ( LGR5 (ref. 32 ), ITGA1 (ref. 33 ), FOXA2 (ref. 34 )) and mice ( FOXA2 (refs. 35 , 36 )). The same expression pattern was recapitulated in our 10x dataset (Extended Data Fig. 10b ). Therefore, the deviating subpopulations can be identified as glandular and luminal epithelia. Differentially expressed genes also included those associated with endometrial remodeling and embryo implantation, such as LIF (Supplementary Fig. 3d ), MMP26 and MT1E (Fig. 5c ).
Fig. 5: Deviating subpopulations of unciliated epithelia across the human menstrual cycle.
The alternative text for this image may have been generated using AI.
Full size image
a , Subpopulations of unciliated epithelia. The color-coded classification is based on dimension reduction independently performed for each phase or subphase shown in Supplementary Fig. 3a (gray: cells that are transcriptomically between the two subpopulations). Labels 1–4 and the major curve: the four phases and the principal curve, respectively, as identified in Fig. 3a , left; small arrow pairs pointing to opposite directions: direction of segregation between the unciliated epithelial subpopulations. b – d , Dynamics of genes differentially expressed ( P adj of Wilcoxon’s rank-sum test < 0.05, log 2 (FC) > 1) between the two subpopulations across multiple phases ( b ), genes that were previously reported to be implicated in endometrial remodeling or embryo implantation ( c ) and genes that exemplified those that reached maximum differential expression in proliferative phases in this dataset ( d ). Colored orange are markers previously reported as differentially expressing in situ between glandular and luminal epithelia in adult human endometria. Cells were ordered by pseudotime. Solid lines: boundaries between the four phases. e , GO enrichment (FDR < 0.05) in genes overexpressed in luminal epithelia during proliferative phases (see Extended Data Fig. 10c for the complete gene list). For each hierarchy, shown are the terms with the highest specificity (top in the hierarchy, indented) and with the highest significance value (FDR, unindented). See also Extended Data Fig. 10 .
Functional enrichment analysis (Fig. 5e ) of genes overexpressed in proliferative phase luminal epithelia (Extended Data Fig. 10c ) revealed extensive enrichment in morphogenesis and tubulogenesis that leads to development of anatomic structures, as well as cellular morphogenesis that leads to differentiation. The Wnt signaling pathway, associated with gland formation during human fetal uterine development (adenogenesis), was also enriched in this gene group. On the other hand, the most pronounced functional feature of glandular epithelia in proliferative phases was a consistently higher fraction of cycling cells (Extended Data Fig. 9c ).
Decidualization in the natural human menstrual cycle is characterized by direct interplay between lymphocytes and stromal fibroblasts
Infiltrating lymphocytes play essential roles during pregnancy, in decidual angiogenesis and regulation of trophoblastic invasion 37 . Their functions in decidualization during the natural human menstrual cycle, however, remain to be defined. Given the notable rise in lymphocyte abundance in the early secretory phase (Supplementary Fig. 4a ), we characterized their transcriptomic dynamics to explore their roles and interactions with other endometrial cell types during decidualization.
Compared to their counterparts in nondecidualized endometrium, lymphocytes in decidualizing endometrium (phase 4) had increased expression of markers characteristic of uterine natural killer (NK) cells during pregnancy ( CD69 , ITGA1 , CD56 ) (Supplementary Fig. 4b,c ) and expressed a more diverse repertoire of both activating and inhibitory NK receptors (NKR) responsible for recognizing major histocompatibility complex (MHC) class I molecules (Fig. 6a ). We observed lymphocytes expressing both NK and T-cell markers and those expressing only NK markers (Supplementary Fig. 4b ), and therefore classified these as CD3 + and CD3 – cells based on their expression of markers characteristic of T cells (Fig. 6b ).
Fig. 6: Endometrial lymphocytes across the human menstrual cycle and their interactions with stromal fibroblasts during decidualization.
The alternative text for this image may have been generated using AI.
Full size image
a , Expression of inhibitory and activating NKR in endometrial lymphocytes. Cells (columns) were sorted from left to right based on percentage of listed NKR expressed. b , Dynamics of genes related to lymphocyte functionality (shown are the medians). CD3 + and CD3 – lymphocytes were classified based on the expression of markers characteristic of T lymphocytes, as shown in Supplementary Fig. 4b . c , Functional annotation (left) and expression (right) of genes overexpressed in decidualizing stromal fibroblasts (phase 4) and implicated in immune responses. d – g , Spatial distribution of immune cells expressing CD3 ( d , f , open arrows) or CD56 ( g , solid arrows) protein and stromal fibroblasts (arrowheads) before ( d , e , day 17) and during ( f , g , day 24) decidualization. VIM, vimentin.
We next identified genes that were changing dynamically in lymphocytes across the menstrual cycle, and characterized those associated with immune functionality (Fig. 6b ). In CD3 – cells we observed a marked rise in cytotoxic granule genes in decidualizing endometrium (phase 4), with the exception of GNLY . In CD3 + cells, this rise in cytotoxic potential was manifested by an increase in CD8 while the elevation in cytotoxic granule genes was only moderate. For both cell subsets, the increased expression of genes encoding IL2 receptors is noticeable in decidualizing endometrium. Equally notable are genes involved in IL2-elicited cell activation. In regard to the cytokine/chemokine repertoire, CD3 – cells in decidualizing endometrium express a high level of chemokines. Their CD3 + counterparts, although expressing a more diverse cytokine repertoire, demonstrate much lower chemokine expression. Lastly, in decidualizing endometrium we noted ligand–receptor pairs that were upregulated respectively in stromal fibroblasts and lymphocytes—for example, IL15 and IL2RB, IL2RG , MHC class I genes and NKR (Fig. 6a–c ), suggesting direct interplay between the two cell types. Using immunofluorescence, we compared spatial proximity between the identified immune subsets and stromal fibroblasts before (Fig. 6d,e ) and during (Fig. 6f,g ) decidualization, and observed a notable increase in the number of immune subsets expressing either CD3 (Fig. 6d,f ) or CD56 (Fig. 6e,g ) protein in close proximity to stromal fibroblasts during decidualization, supporting a direct interplay between the two cell types.
Discussion
In this study, we systematically characterized the human endometrium across the menstrual cycle from both a static and a dynamic perspective. Other recent studies 38 , 39 , 40 on the human endometrium were limited to a single cell type 38 , a single patient with a gynecological condition 39 or focused on an in vitro system 40 . In our study, each of the reported biological phenotypes was supported by multiple healthy biological replicates and data were collected on multiple platforms to control for technical artifacts.
We show that the ciliated epithelium is a transcriptomically distinct endometrial cell type; these cells are consistently present in the healthy endometrium but dynamically changing in abundance across the menstrual cycle (Supplementary Fig. 4a ). Although the existence of ciliated cells in the human endometrium has been speculated upon based on microscope studies since the 1890s 41 , 42 , information on this cell type has been lacking. We provide a cross-cycle molecular characterization of the cell type, which can inform future studies.
Our data suggest that the WOI opens with an abrupt and strong transcriptomic activation in unciliated epithelia, accompanied by a more continuous transition in stromal fibroblasts. The abruptness of the transition also suggests that it should be possible to diagnose the opening of the WOI with higher precision for in vitro fertilization and embryo transfer. Given that WOI opening is also accompanied with striking histological changes, future work can correlate transcriptomic and histological features of WOI for a more comprehensive understanding of this important event.
This dataset also enabled comparison of decidualizing stromal fibroblasts in naturally cycling human endometrium with their counterparts in early pregnancy. It is unclear how decidualization in naturally cycling, nonpregnant endometrium compares to that in early pregnancy, especially considering the substantial endometrial remodeling that occurs after implantation. Our data revealed a different cellular hierarchy of decidualizing stromal fibroblasts in natural cycles that is less heterogeneous and lacks the transcriptomically distinct subtype that co-upregulates the classical decidualization markers IGFBP1 and PRL . These findings support a paradigm where an implanting embryo further drives decidualization of stromal fibroblasts into subtypes, rather than stromal fibroblasts being fully decidualized without implantation.
This dataset can be used as a healthy human baseline for endometrial diseases and for evaluation of model systems. The dating system will be useful for studies in clinical fertility and endometrial biology focused on one or more major phases of the cycle, such as those studying the spatial molecular and cell type gradient across different layers of the uterus or interactions between ligand–receptor pairs. The relationship between the new dating system and other, easily measurable, physiological metrics can also be studied to determine the impact of menstrual cycle variation on molecular and behavior measurements in females.
Methods
Subject details
All procedures involving human endometrium were conducted in accordance with the Institutional Review Board (IRB) guidelines for Stanford University under IRB code no. IRB-35448 and IVI Valencia, Spain under IRB code no. 1603-IGX-016-CS. Collection of endometrial biopsies was approved under IRB code no. 1603-IGX-016-CS. There were no medical reasons for obtaining endometrial biopsies. Healthy ovum donors were recruited in the context of the research project approved by the IRB. Informed written consent was obtained from each donor in her natural menstrual cycle (no hormone stimulation) before an endometrial biopsy was performed. De-identified human endometrium was obtained from women aged 18–34 years with regular menstrual cycling (3–4 d every 28–30 d), body mass index 19–29 kg m –2 (inclusive), normal karyotype and negative serological tests for human immunodeficiency virus, hepatitis B virus, hepatitis C virus and syphilis. Women with the following conditions were excluded from tissue collection: recent contraception (intrauterine device usage in past 3 months; hormonal contraceptives in past 2 months), uterine pathology (endometriosis, leiomyoma or adenomyosis; bacterial, fungal or viral infection) or polycystic ovary syndrome.
Method details
Endometrium tissue dissociation and population enrichment
A two-stage dissociation protocol was used to dissociate endometrium tissue and separate it into stromal fibroblast- and epithelium-enriched single-cell suspensions. Before dissociation, the tissue was rinsed with DMEM (Sigma) on a Petri dish to remove blood and mucus. Excess DMEM was removed after rinsing. The tissue was then minced into pieces as small as possible and dissociated in collagenase A1 (Sigma) overnight at 4 °C in a 50-ml Falcon tube in the horizontal position. This primary enzymatic step dissociates stromal fibroblasts into single cells while leaving epithelial glands and lumen mostly undigested. The resulting tissue suspension was then briefly homogenized and left unagitated for 10 min in a 50-ml Falcon tube in the vertical position, during which epithelial glands and lumen sedimented as a pellet and stromal fibroblasts remained suspended in the supernatant. The supernatant was therefore collected as the stromal fibroblast-enriched suspension. The pellet was washed twice in 50 ml of DMEM to further remove residual stromal fibroblasts. The washed pellet was then dissociated in 400 μl of TrypLE Select (Life technology) for 20 min at 37 °C, during which homogenization was performed via intermittent pipetting. DNaseI (100 μl) was then added to the solution to digest extracellular genomic DNA. The digestion was quenched with 1.5 ml of DMEM after 5 min of incubation. The resulting cell suspension was then pipetted, filtered through a 50-μm cell strainer and centrifuged at 1,000 r.p.m. for 5 min. The pellet was resuspended as the epithelium-enriched suspension.
Fluidigm C1 single-cell capture, imaging and cDNA generation
For cell suspension of both portions, live cells were enriched using the MACS dead cell removal kit (Miltenyi Biotec) following the manufacturer’s protocol. The resulting cell suspension was diluted in DMEM to a final concentration of 300–400 cells μl –1 before loading onto a medium C1 chip for mRNA-sequencing (mRNA-seq) (Fluidigm). Live dead cell stain (Life Technology) was added directly to the cell suspension. Single-cell capture, mRNA reverse transcription and cDNA amplification were performed on the Fluidigm C1 system using default scripts for mRNA-seq. All capture site images were recorded using an inhouse-built microscopic system at ×20 magnification through phase, GFP and Y3 channels. Prediluted spike-in controls developed by the External RNA Controls Consortium (ERCC) (1 μl, Ambion) was added to the lysis mix, resulting in a final dilution factor of 1:80,000.
Fluidigm C1 single-cell RNA-seq library generation
Single-cell cDNA concentration and size distribution were analyzed on a capillary electrophoresis-based automated fragment analyzer (Advanced Analytical). Tagmented and barcoded cDNA libraries were prepared only for cells imaged as singlet or empty at the capture site and with >0.06 ng ul –1 cDNA generated. Library preparation was performed using a Nextera XT DNA Sample Preparation kit (Illumina) on a Mosquito HTS liquid handler (TTP Labtech), following Fluidigm’s single-cell library preparation protocol with a fourfold scaledown of all reagents. Dual-indexed, single-cell libraries were pooled and sequenced in paired-end reads on Nextseq (Illumina) to a depth of 1–2 × 10 6 reads per cell. bcl2fastq (v.2.17.1.14) was used to separate out the data for each single cell using unique barcode combinations from the Nextera XT preparation, and to generate *.fastq files.
Chromium 10x single-cell RNA-seq library generation
Biopsies in the 10x dataset were obtained and dissociated following the protocol used for the C1 dataset. Importantly, we collected both C1 and 10x data for two biopsies, one each from the mid- and early-secretory phases (Extended Data Fig. 1b ). These served as anchors for a direct comparison between the two datasets, and are referred to as anchor biopsies in this manuscript. Following live cell enrichment via MACS (see description for the Fluidigm C1 dataset), live cells were washed twice with PBS to remove ambient RNA. The resulting epithelial and stromal portions were combined in a 1:1 concentration ratio and loaded onto the Chromium Next GEM Chip G (10x Genomics) for each donor. GEM generation and barcoding, reverse transcription, cDNA generation and library construction were performed following the manufacturer’s protocol (Single cell 3′ reagent kit v.3.1, 10x Genomics). Dual-indexed, single-cell libraries were pooled and sequenced in paired-end reads on Novaseq (Illumina).
Tissue preparation for in situ hybridization
Endometrial tissues were fixed for 24–48 h in 4% paraformaldehyde at room temperature, trimmed, embedded in paraffin, sectioned into 3-µm units and applied to 3-aminopropyltriethoxysilane-coated slides.
Immunofluorescence
Tissue sections were baked at 60 °C for 1 h, deparaffined with Histoclear and rehydrated with ethanol series. Antigen retrieval was performed by boiling tissue sections in 10 mM sodium citrate buffer (pH 6.0) for 20 min, followed by immediate cooling in cold water for 10 min. Tissue permeabilization was performed with 0.25% Triton X-100 in PBS for 5 min, followed by washing twice in 0.05% Triton X-100 in PBS for 5 min. Nonspecific binding was blocked with 5% BSA/0.05% Triton X-100/4% goat serum in PBS for 1 h at room temperature. Tissue sections were then incubated with primary antibodies overnight at 4 °C and secondary antibodies for 1 h at room temperature. Primary antibodies used and dilution ratios were as follows: vimentin (2 µg ml –1 ; no. ab8978, Abcam), CD3 (1:100; no. ab5690, Abcam) and CD56 (1:50; no. ab133345, Abcam). Secondary antibodies used and dilution ratios were as follows: goat antimouse IgG (H + L) Superclonal Alexa Fluor 488 (1:200; no. A27034, Thermo Fisher Scientific) and goat antirabbit IgG (H + L) Superclonal Alexa Fluor 555 (1:200; no. A27039, Thermo Fisher Scientific). All sections were counterstained with DAPI (Thermo Fisher Scientific) and mounted with Aquatex (Merck-Millipore). Images were captured using a confocal microscope (FV1000, Olympus) at ×20 and ×60 magnification with oil immersion lens, and analyzed using Imaris (v.9.2, Bitplane).
RNAscope for ciliated cells
Combined RNA and antibody in situ hybridization was performed according to the manufacturer’s technical note, ‘RNAscope Multiplex Fluorescent v.2 Assay combined with Immunofluorescence’ for formalin-fixed, paraffin-embedded samples (Advanced Cell Diagnostics). Incubation times of 15 and 30 min were used for target retrieval and Protease Plus treatment, respectively. RNA probes (Advanced Cell Diagnostics) with the following channel assignment (C), fluorophore and dilution in TSA buffer were used: CDHR3 (C1, cyanine 3, 1:1,500), C11orf88 (C2, cyanine 5, 1:750); C20orf85 (C1, cyanine 3, 1:1,500) and FAM183A (C2, cyanine 5, 1:1,500). Tissue sections were blocked with SuperBlock (PBS) blocking buffer (Fisher Scientific) for 30 min at room temperature, incubated in antihuman FOXJ1 (1:500; no. 14-9965-80, clone no. 2A5, eBioscience) overnight at 4 °C and goat antimouse IgG secondary antibody (1:500; no. F2761, Life Technologies) for 2 h at room temperature. All sections were mounted with Prolong Diamond Antifade Mountant (Thermo Fisher Scientific). Imaging was carried out on an Axio-plan epifluorescence microscope equipped with an Axiocam 506 mono camera (Zeiss) using a ×20/0.8 numerical aperture Plan-Apochromat objective (Zeiss). For each sample, eight to ten fields of view were captured with 10–15 z-stacks.
Quantification and statistical analysis
Single-cell RNA-seq data analysis
Fluidigm C1 dataset
Raw reads in the *.fastq files were trimmed to 75 base pairs using fastqx (v.0.11.7), aligned to Ensembl human reference genome GRCh38.87 (dna.primary_assembly) using STAR (v.2.5) 43 with default parameters, and duplicates removed using picard (2.9) MarkDuplicates. Aligned reads were converted to counts using HTSeq (v.0.7.0) 44 and Ensembl GTF for GRCh38.87 under the setting -m intersection-strict \-s no. Downstream data analysis was performed in R and Java. For each cell, raw counts (ct) were normalized to log-transformed reads per million (log 2 (rpm + 1)) by the equation \({{\log_2\left( {\mathrm{rpm} + 1} \right)}} = {{\log_2(1 + \frac{{10^6 \times \mathrm{ct}_{ij}}}{{{\sum} {\mathrm{ct}_i} }})}}\) where i denotes cell i and j denotes gene j .
Quality filtering
For quality filtering, the fraction of reads mapped to ERCC ( f ERCC ) was used as the quality metric and empirical cumulative distribution of f ERCC in empty capture sites recorded on the C1 chip was calculated (R function ecdf() in stats v.3.5.1) and used as the null model (ecdf n ull ). Single cells retained for downstream analysis were those with (ecdf ull ( f ERCC ))<0.05. A total of 2,148 cells were retained for downstream analysis.
Cell heterogeneity analysis
Overdispersion of genes was calculated as \(\frac{{\mathrm{CV}_{{i}}^2}}{{\mathrm{CV}_{\mathrm{e}}^2}}\) , where \(\mathrm{CV}_{{i}}^2\) is the squared variation of coefficient of gene i across cells of interest and \(\mathrm{CV}_{\mathrm{e}}^2\) is the expected squared variation of the coefficient-given mean, fitted using non-ERCC counts. All pairwise distances between cells were calculated as 1 – Pearson’s correlation. Dimensional reduction was performed using the R implementation of t -SNE (Rtsne v.0.13).
Differential expression analysis
To obtain differentially expressed genes for a cell type or state, for each gene, Wilcoxon’s rank-sum test 45 (R implementation wilcox.test v.3.5.1) was performed and fold change (FC, dummy variable = 1 × 10 –2 ) was calculated between cells within a cell type/state and cells from other cell types/states. P values obtained from Wilcoxon’s rank-sum test were adjusted for multiple comparison by the Benjamini–Hochberg’s procedure 46 (R function BH() in sgof 2.3) to obtain P adj . To evaluate the ‘sensitivity’ and ‘specificity’ of a gene in identifying a cell type/state, we also calculated the percentage of cells within the cell type/state of interest expressing the gene (pct in ) and percentage of cells from other cell types/states expressing the gene (pct out ), as well as the ratio between pct in and pct out .
Gene ontology (GO) functional enrichment
Functional enrichment analysis was performed using GO enrichment analysis ( http://www.geneontology.org ), and each enriched ontology hierarchy (false discovery rate (FDR) < 0.05) was reported with two terms in the hierarchy: (1) the term with the highest significance value and (2) the term with the highest specificity.
Constructing single-cell-resolution trajectories of the menstrual cycle using a MI-based approach
Endometrial transformation over the menstrual cycle is, at least in part, a continuous process. A model that not only retains phase-wise characteristics but also allows delineation of continuous features between and within phases will enable higher precision characterization. To build such a model, we used a MI-based aproach 18 such that we exploited the information provided by the time annotation, minimized its limitation noted in the previous section and accounted for potential continuity between and within phases. Briefly, we enriched for genes that were changing across the menstrual cycle based on MI between gene expression and time annotation, regardless of the underlying model of dynamics (see next section for details). In total we obtained 3,198 and 1,156 ‘time-associated’ genes for unciliated epithelia and stromal fibroblasts, respectively (FDR < 0.05; Extended Data Fig. 3b ). For both cell types, dimensional reduction ( t -SNE) using time-associated genes revealed the same four major phases as obtained using an unsupervised approach (Extended Data Fig. 3a,c ), demonstrating that the MI-based approach reduced the bias of time annotation to the same extent as the unsupervised approach. Meanwhile, the MI-based approach enabled identification of a clear trajectory that connected the phases and was time associated within phases. We defined trajectories using the principal curve 47 (R implementation princurve v.2.1.1; Fig. 3a ) and assigned each cell an order along the trajectory based on its projection on the curve 48 , 49 , 50 , 51 , which we refer to as pseudotime (Fig. 3a ).
Enrichment of time-associated genes via the MI-based approach
The time-associatedness of a gene was calculated as the MI between its expression and time (or pseudotime) using the Java implementation of ARACNe-AP 52 . For each gene, MI i = MI(( e 1 i , e 2 i ,…, e ni ),( t 1 , t 2 , …, t n )), where i denotes gene i , e ni denotes the expression of gene i in cell n and t n is the time (or pseudotime) annotation of cell n . The statistical significance of MI i was evaluated using the null model where the time (or pseudotime) annotation was permutated 1,000 times with respect to cells, based on which an empirical cumulative distribution function (ecdf null, i ) between the expression of gene i and the permutated time (or pseudotime) was constructed using the R function ecdf() (in stats v.3.5.1). The P value for MI i was calculated as (1 – ecdf null, i (MI i )). P values were then adjusted for multiple comparison by the Benjamini–Hochberg procedure 46 to obtain the FDR value for each gene.
In Extended Data Fig. 4a , by calculating the MI between gene expression and pseudotime, we obtained 1,382 and 527 genes for unciliated epithelia and stromal fibroblasts, respectively (FDR < 1 × 10 –5 ) (Supplementary Table 4 ).
Smoothing of time-associated genes and assignment into characteristic phases
To estimate the pseudotime at which a gene reached maximum expression (pseudotime max ), smoothing of gene expression was performed with respect to pseudotime using the R function smooth.spline() (spar=1, in stats v.3.5.1), and the pseudotime(s) at which a smoothed curve reached global or local maximum was estimated using the R function peaks() and inflection point was estimated using a custom R script.
Characteristic signatures for phases 1–4 (Supplementary Table 4 ) were identified by assigning each pseudotime-associated gene we identified (Extended Data Fig. 4a,b ) to the phase where its peak expression occurred (that is, pseudotime max ).
Characterization of dynamics of TF and genes encoding secretory proteins (sec genes) across the menstrual cycle
We define a dynamic TF/sec gene (Extended Data Figs. 6 and 7 ) as a time-associated gene (Extended Data Fig. 3b ) that is annotated as a transcriptional regulator/encoding a secretory protein by the Human Protein Atlas 53 . Dynamic TFs/sec genes were first categorized into major groups using hierarchical clustering on smoothed and [0,1] normalized curves. For both unciliated epithelia and stromal fibroblasts, these TFs/sec genes can primarily be assigned to two main categories (Extended Data Figs. 6 and 7a,b and Supplementary Tables 2 and 3 )—that is, with one or two peak(s) of expression detected within one menstrual cycle. In each group, TFs/sec genes were ordered by the pseudotime where a peak or a major peak (for curves with two peaks) occurred, and ties were broken by the pseudotime where the inflection point occurred.
For WOI-associated TFs with a peak expression detected after opening of the WOI (Extended Data Fig. 6c,d )—that is, the boundary between phases 3 and 4—we further divided them into those that peaked during and at the end of phase 4, with the hypothesis that the former are more probably related to opening of the WOI and the latter to its closure.
Cell cycle analysis
We took a two-step approach in identifying cycling cells and defining endometrium-specific cell cycle signatures (Extended Data Fig. 9a,b ). We first used a published gene set encompassing 43 G1/S and 55 G2/M genes 54 , representing the intersection of four previous gene sets 55 , 56 , 57 , and calculated a G1/S and a G2/M score for all single cells in unciliated epithelia and stromal fibroblasts, respectively, following the scoring scheme in ref. 54 . Briefly, cells with at least twofold average expression of either G1/S or G2/M genes compared to the average of all cells in the respective cell type were assigned as putative cycling cells. We next performed Wilcoxon’s rank-sum test 45 between putative cycling cells and the remaining cells in the cell type, to enrich for cell-cycle-associated transcriptome signatures specific to endometrium (Extended Data Fig. 9a,b ). To assign cells into the G1/S or G2/M phase, we performed dimension reduction on putative cycling cells using the identified signature, which revealed two major populations enriched with known G1/S or G2/M signatures. We assigned genes as either G1/S or G2/M associated, by estimating the population at which peak expression of the gene occurred. We then recalculated the G1/S and G2/M scores for each cell using the signature customized for endometrium and finalized the assignment of G1/S and G2/M cells with at least twofold average G1/S or G2/M expression with respect to all cells in that cell type.
Validation of boundary assignment between proliferative and secretory phases
To further validate the assignment based on cell cycle activity, we defined characteristic signatures for phases 1–4 (see Supplementary Table 4 and Methods ) and identified major hierarchies of biological processes that were enriched by the signatures (see Supplementary Table 5 and Methods ). While phase 1 was characterized by processes such as tissue regeneration—for example, Wnt signaling pathways (unciliated epithelia, epi), tissue morphogenesis (epi), wound healing (stromal fibroblasts, str) and angiogenesis (str)—and phase 2 by cell proliferation (epi), phase 3 was dominated by negative regulation of growth (epi) and response to ions (epi) and phase 4 by secretion (epi) and implantation (epi). The transition from positive to negative regulation in growth from phase 2 to 3 further confirmed a pre-to-postovulatory transition 19 .
Lastly, we used previous whole-tissue analyses to help differentiate the pre- and postovulatory phases. We reasoned that, although whole-tissue data would be confounded by varying proportions of the major cell types (stromal fibroblasts and unciliated epithelia), whole-tissue and single-cell data taken together should have a high level of consensus on genes that are either in synchrony between the two cell types or have negligible expression in one cell type but major phase-specific dynamics in another. We therefore identified genes with these characteristics using our single-cell data (Fig. 4 ). As expected, among these genes that we identified are those that have been consistently reported in whole-tissue studies as being characteristic of canonical endometrial phases, confirming the validity of using these to identify the WOI. Particularly, upregulation of the metallothioneins ( MT1F, X, E, G ) from phases 2 and 3 is characteristic of proliferative to early secretory transition based on whole-tissue-level reports 9 , 19 . Therefore, considering both cell cycling activity and all of the evidence above, phases 1 and 2 can be identified as preovulatory (proliferative), and phases 3 and 4 as postovulatory (secretory).
Chromium 10x dataset
Raw reads in the *.fastq files were aligned to reference (GRCh38-3.0.0) and quantified using Cell Ranger (v.3.1.0) with -expect-cells=10,000. Downstream data analysis was performed using the Seurat package (v.3.1.2) 58 and scripts in R. Raw counts (ct) were normalized to log-transformed transcripts per million (log(TPM + 1)) by the equation \({\mathrm{log}}\left( {{\mathrm{TPM}} + 1} \right) = {\mathrm{log}}\left(1 + \frac{{10^6 \times {{\mathrm{ct}}_{ij}}}}{{{\sum} {{{\mathrm{ct}}_i}} }}\right)\) where i denotes cell i and j denotes gene j , using the NormalizeData() function in Seurat.
Quality filtering
Dimension reduction was first performed on all barcodes that were output as cells by Cell Ranger (v.3.1.0). In the reduced dimensional space, each identified cell cluster was evaluated by quality matrices including the following: unique molecular identifier count, number of genes detected and percentage mitochondrial reads. In addition, differential gene expression was performed between each cluster and the remaining cells to identify uniquely expressed genes. Clusters with no uniquely expressed genes identified above threshold and poor-quality metric readouts were removed as low-quality clusters. Clusters with combined expression of two distinct cell lineages were removed as doublet clusters. Homotypic doublets—that is, those formed from transcriptionally similar cell states—were removed using DoubletFinder (v.2.0.2) 59 . Lastly, for clusters containing unciliated epithelia and stromal fibroblasts, respectively, a Gaussian mixture model was fit on the distribution of the number of genes detected (R package mixtools (v.1.1.0)). For each cell type, the Gaussian distribution N ( μ , σ 2 ) with the lowest mean was identified and a threshold (th) was calculated as th = μ + 2 σ for N . Only cells (71,032 in total) with a number of genes detected equal to or higher than th were retained for downstream analysis.
Assignment of unciliated epithelia subtypes
To deconvolute temporal change from subtype difference, unciliated epithelia were integrated across donors using the Seurat functions FindIntegrationAnchors() and IntegrateData() with default parameters. To deconvolute cell cycling from subtype difference, cell cycle scores were regressed out during the scaling (ScaleData()) of integrated data. Two unciliated epithelia subtypes were then assigned using the Seurat functions FindNeighbors() and FindClusters() on top principal components.
RNAscope image analysis
Z-stacks were projected (maximum intensity projection, MIP) using ImageJ (v.1.5.1w). The resulting MIP images were analyzed using CellProfiler (v.3.0.0) as follows: (1) correct background by subtracting the lower quartile of the intensity measured from the whole image; (2) detect cell nuclei using the DAPI channel and cell boundaries using Voronoi distance (25 pixels) from the nuclei; (3) enhance RNA signals using a Top-hat filter (five pixels) and detect signals by intensity threshold (0.004 and 0.002 for Cy3 and Cy5, respectively); and (4) measure antibody intensity for each detected cell. All images were analyzed in the same way, with no image excluded.
Statistics and reproducibility
See Fig. 3b,c : each set of dots (median) and error bars (median absolute deviation) represents statistics derived from all unciliated epithelia (epi) or stromal fibroblasts (str), respectively, from a single woman. The exact number of cells ( n ) used to derive each set of median and mad is included in the column headed ‘ n ’ in the source data linked to Fig. 3 , which also includes, for each woman, the exact values of median and mad of pseudotimes for epi and str, respectively, and the day of menstrual cycle.
Reporting Summary
Further information on study design is available in the Nature Research Reporting Summary linked to this article.
Data availability
All raw and analyzed sequencing data associated with Figs. 1 , 3 – 5 and 6a–c , all Extended Data figures and all supplementary figures in this study can be found at NCBI’s Gene Expression Omnibus (series accession code GSE111976 ) and Sequence Read Archive (accession code SRP135922 ). Data associated with Fig. 2 , extracted from all representative fields of view, can be found in Supplementary Dataset 1 . Source data are provided with this paper.
Code availability
Custom codes developed in this study for gene dispersion calculation, MI calculation and transcriptional regulator and secretory protein analyses are available at https://github.com/wanxinw/endometrium/ . Specific codes are accessible, with no restrictions, upon request to W.W. (wanxinw@stanford.edu).
References
Martin, R. D. The evolution of human reproduction: a primatological perspective. Yearb. Phys. Anthropol. 50 , 59–84 (2007).
Article Google Scholar
Emera, D., Romero, R. & Wagner, G. The evolution of menstruation: a new model for genetic assimilation: explaining molecular origins of maternal responses to fetal invasiveness. BioEssays 34 , 26–35 (2012).
Article CAS Google Scholar
Crichton, E. & Krutzsch, P. Reproductive Biology of Bats (Elsevier, 2000).
Bellofiore, N. et al. First evidence of a menstruating rodent: the spiny mouse ( Acomys cahirinus ). Am. J. Obstet. Gynecol 216 , 40E.1–40E.11 (2017).
Noyes, R. W., Hertig, A. T. & Rock, J. Dating the endometrial biopsy. Fertil. Steril. 1 , 3–25 (1950).
Article Google Scholar
Croxatto, H. B. et al. Studies on the duration of egg transport by the human oviduct. II. Ovum location at various intervals following luteinizing hormone peak. Am. J. Obstet. Gynecol. 132 , 629–634 (1978).
Article CAS Google Scholar
Wilcox, A. J., Baird, D. D. & Weinberg, C. R. Time of implantation of the conceptus and loss of pregnancy. N. Engl. J. Med. 340 , 1796–1799 (1999).
Article CAS Google Scholar
Riesewijk, A. et al. Gene expression profiling of human endometrial receptivity on days LH+2 versus LH+7 by microarray technology. Mol. Hum. Reprod. 9 , 253–264 (2003).
Article CAS Google Scholar
Ruiz-Alonso, M., Blesa, D. & Simón, C. The genomics of the human endometrium. Biochim. Biophys. Acta Mol. Basis Dis. 1822 , 1931–1942 (2012).
Article CAS Google Scholar
Díaz-Gimeno, P. et al. A genomic diagnostic tool for human endometrial receptivity based on the transcriptomic signature. Fertil. Steril. 95 , 50–60 (2011).
Article Google Scholar
Van Der Maaten, L. & Hinton, G. Visualizing data using t-SNE. J. Mach. Learn. Res. 620 , 267–284 (2008).
Google Scholar
Ashburner, M. et al. Gene ontology: tool for the unification of biology. Nat. Genet. 25 , 25–29 (2000).
Article CAS Google Scholar
The Gene Ontology Consortium. Expansion of the Gene Ontology knowledgebase and resources. Nucleic Acids Res. 45 , D331–D338 (2017).
Article Google Scholar
Zhou, F. & Roy, S. SnapShot: motile cilia. Cell 162 , 224–224 (2015).
Article CAS Google Scholar
Schwab, K. E. & Gargett, C. E. Co-expression of two perivascular cell markers isolates mesenchymal stem-like cells from human endometrium. Hum. Reprod . 22 , 2903–2911 (2007).
Masuda, H., Anwar, S. S., Bühring, H. J., Rao, J. R. & Gargett, C. E. A novel marker of human endometrial mesenchymal stem-like cells. Cell Transplant. https://doi.org/10.3727/096368911X637362 (2012).
Guo, Y., Manatunga, A. K., Chen, S. & Marcus, M. Modeling menstrual cycle length using a mixture distribution. Biostatistics 7 , 100–114 (2006).
Article Google Scholar
Tkačik, G. & Walczak, A. M. Information transmission in genetic regulatory networks: a review. J. Phys. Condens. Matter 23 , 153102 (2011).
Article Google Scholar
Talbi, S. M. et al. Molecular phenotyping of human endometrium distinguishes menstrual cycle phases and underlying biological processes in normo-ovulatory women. Endocrinology 147 , 1097–1121 (2006).
Park, Y., Nnamani, M. C., Maziarz, J. & Wagner, G. P. Cis-regulatory evolution of forkhead box O1 (FOXO1), a terminal selector gene for decidual stromal cell identity. Mol. Biol. Evol. 33 , 3161–3169 (2016).
Article CAS Google Scholar
Okada, H. et al. Regulation of decidualization and angiogenesis in the human endometrium: mini review. J. Obstet. Gynaecol. Res. 40 , 1180–1187 (2014).
Article CAS Google Scholar
Ramathal, C. Y., Bagchi, I. C., Taylor, R. N. & Bagchi, M. K. Endometrial decidualization: of mice and men. Semin. Reprod. Med. 28 , 17–26 (2010).
Article CAS Google Scholar
Hood, B. L. et al. Proteomics of the human endometrial glandular epithelium and stroma from the proliferative and secretory phases of the menstrual cycle. Biol. Reprod . 92 , 106 (2015).
Lessey, B. A., Metzger, D. A., Haney, A. F. & McCarty, K. S. Immunohistochemical analysis of estrogen and progesterone receptors in endometriosis: comparison with normal endometrium during the menstrual cycle and the effect of medical therapy. Fertil. Steril . 51 , 409–415 (1989).
Lessey, B. A. et al. Immunohistochemical analysis of human uterine estrogen and progesterone receptors throughout the menstrual cycle. J. Clin. Endocrinol. Metab . 67 , 334–340 (1988).
Zhou, J., Dsupin, B. A., Giudice, L. C. & Bondy, C. A. Insulin-like growth factor system gene expression in human endometrium during the menstrual cycle. J. Clin. Endocrinol. Metab . 79 ,1723–1734 (1994).
Vento-Tormo, R. et al. Single-cell reconstruction of the early maternal–fetal interface in humans. Nature 563 , 347–353 (2018).
Suryawanshi, H. et al. A single-cell survey of the human first-trimester placenta and decidua. Sci. Adv . 4 , eaau4788 (2018).
Tulac, S. et al. Identification, characterization, and regulation of the canonical Wnt signaling pathway in human endometrium. J. Clin. Endocrinol. Metab. 88 , 3860–3866 (2003).
Article CAS Google Scholar
Fan, X. et al. Dynamic regulation of Wnt7a expression in the primate endometrium: implications for postmenstrual regeneration and secretory transformation. Endocrinology 153 , 1063–1069 (2012).
Article CAS Google Scholar
Yin, Y. & Ma, L. Development of the mammalian female reproductive tract. J. Biochem. 137 , 677–683 (2005).
Tempest, N., Baker, A. M., Wright, N. A. & Hapangama, D. K. Does human endometrial LGR5 gene expression suggest the existence of another hormonally regulated epithelial stem cell niche? Hum. Reprod . 33 , 1052–1062 (2018).
Lessey, B. A. et al. Luminal and glandular endometrial epithelium express integrins differentially throughout the menstrual cycle: implications for implantation, contraception, and infertility. Am. J. Reprod. Immunol. 35 , 195–204 (1996).
Article CAS Google Scholar
Kelleher, A. M. et al. Integrative analysis of the forkhead box A2 (FOXA2) cistrome for the human endometrium. FASEB J . 33 , 8543–8554 (2019).
Jeong, J.-W. et al. Foxa2 is essential for mouse endometrial gland development and fertility. Biol. Reprod . 83 , 396–403 (2010).
Filant, J. & Spencer, T. E. Endometrial glands are essential for blastocyst implantation and decidualization in the mouse uterus. Biol. Reprod . 88 , https://doi.org/10.1095/biolreprod.113.107631 (2013).
Hanna, J. et al. Decidual NK cells regulate key developmental processes at the human fetal–maternal interface. Nat. Med. 12 , 1065–1074 (2006).
Article CAS Google Scholar
Krjutskov, K. et al. Single-cell transcriptome analysis of endometrial tissue. Hum. Reprod . 31 , 844–853 (2016).
Wu, B. et al. Cell atlas of human uterus. Preprint at bioRxiv https://doi.org/10.1101/267849 (2018).
Lucas, E. S. et al. Recurrent pregnancy loss is associated with a pro-senescent decidual response during the peri-implantation window. Commun. Biol . 3 , 37 (2020).
Benda, C. Klenusches Handbuch der Han und Sexualorgane (Hansebooks, 1894).
Turco, M. Y. et al. Long-term, hormone-responsive organoid cultures of human endometrium in a chemically defined medium. Nat. Cell Biol . 19 , 568–577 (2017).
Dobin, A. et al. STAR: ultrafast universal RNA-seq aligner. Bioinformatics 29 , 15–21 (2013).
Article CAS Google Scholar
Anders, S., Pyl, P. T. & Huber, W. HTSeq—a Python framework to work with high-throughput sequencing data. Bioinformatics 31 , 166–169 (2015).
Article CAS Google Scholar
Mann, H. B. & Whitney, D. R. On a test of whether one of two random variables is stochastically larger than the other. Ann. Math. Stat. 18 , 50–60 (1947).
Article Google Scholar
Benjamini, Y. & Hochberg, Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J. R. Stat. Soc. B 57 , 289–300 (1995).
Google Scholar
Hastie, T. & Stuetzle, W. Principal curves. J. Am. Stat. Assoc. 84 , 502–516 (1989).
Article Google Scholar
Petropoulos, S., Edsga, D., Reinius, B. & Linnarsson, S. Single-cell RNA-Seq reveals lineage and X chromosome dynamics in human preimplantation resource single-cell RNA-seq reveals lineage and X chromosome dynamics in human preimplantation embryos. Cell 165 , 1012–1026 (2016).
Article CAS Google Scholar
Kim, T. H. et al. Single-cell transcript profiles reveal multilineage priming in early progenitors derived from Lgr5 + intestinal stem cells. Cell Rep . 16 , P2053–P2060 (2016).
Marco, E. et al. Bifurcation analysis of single-cell gene expression data reveals epigenetic landscape. Proc. Natl Acad. Sci. USA 111 , E5643–E5650 (2014).
Ji, Z. & Ji, H. TSCAN: pseudo-time reconstruction and evaluation in single-cell RNA-seq analysis. Nucleic Acids Res . 44 , e117 (2016).
Lachmann, A., Giorgi, F. M., Lopez, G. & Califano, A. ARACNe-AP: gene network reverse engineering through adaptive partitioning inference of mutual information. Bioinformatics 32 , 2233–2235 (2016).
Article CAS Google Scholar
Uhlen, M. et al. Tissue-based map of the human proteome. Science 347 , 1260419 (2015).
Article Google Scholar
Tirosh, I. et al. Single-cell RNA-seq supports a developmental hierarchy in human oligodendroglioma. Nature 539 , 309–313 (2016).
Article Google Scholar
Macosko, E. Z. et al. Highly parallel genome-wide expression profiling of individual cells using nanoliter droplets. Cell 161 , 1202–1214 (2015).
Article CAS Google Scholar
Kowalczyk, M. S. et al. Single-cell RNA-seq reveals changes in cell cycle and differentiation programs upon aging of hematopoietic stem cells. Genome Res. 25 , 1860–1872 (2015).
Article CAS Google Scholar
Whitfield, M. L. Identification of genes periodically expressed in the human cell cycle and their expression in tumors. Mol. Biol. Cell 13 , 1977–2000 (2002).
Article CAS Google Scholar
Stuart, T. et al. Comprehensive integration of single-cell data. Cell 177 , P1888–P1902 (2019).
McGinnis, C. S., Murrow, L. M. & Gartner, Z. J. DoubletFinder: doublet detection in single-cell RNA sequencing data using artificial nearest neighbors. Cell Syst . 8 , P329–P337 (2019).
Download references
Acknowledgements
We thank H. Ding for valuable discussions and advice; N. Neff and J. Okamoto for sequencing expertise; F. B. Yu, S. Darmanis and F. Zanini for technical expertise and discussions; S. Crasta and S. Kolluru for technical assistance; and the Stanford Cell Science Imaging Facility for assistance with imaging. This study was jointly supported by the March of Dimes, Chan Zuckerberg Biohub and MINECO/FEDER (no. SAF-2015-67164-R, to C.S.) (Spanish Government). W.W. was supported by the Stanford Bio-X Graduate Bowes Fellowship and Chan Zuckerberg Biohub. F.V. was supported by the Miguel Servet Program Type II of ISCIII (no. CPII18/00020) and the FIS project (no. PI18/00957). P.A. was supported by IVI-RMA Valencia. I.M. was supported by the Igenomix Foundation. M.M. and A.I. were supported by Chan Zuckerberg Biohub. W.P. was supported by the March of Dimes.
Author information
Author notes
These authors contributed equally: Wanxin Wang, Felipe Vilella.
Authors and Affiliations
Department of Bioengineering, Stanford University, Stanford, CA, USA
Wanxin Wang, Alina Isakova, Wenying Pan & Stephen R. Quake
Department of Obstetrics & Gynecology, Stanford University, Stanford, CA, USA
Felipe Vilella, Inmaculada Moreno & Carlos Simon
Igenomix Foundation, INCLIVA Health Research Institute, Valencia, Spain
Felipe Vilella, Inmaculada Moreno & Carlos Simon
IVI Valencia, Valencia, Spain
Pilar Alama
Chan Zuckerberg Biohub, San Francisco, CA, USA
Marco Mignardi & Stephen R. Quake
Department of Obstetrics & Gynecology, University of Valencia, Valencia, Spain
Carlos Simon
Department of Applied Physics, Stanford University, Stanford, CA, USA
Stephen R. Quake
Authors
Wanxin Wang
View author publications
Search author on: PubMed Google Scholar
Felipe Vilella
View author publications
Search author on: PubMed Google Scholar
Pilar Alama
View author publications
Search author on: PubMed Google Scholar
Inmaculada Moreno
View author publications
Search author on: PubMed Google Scholar
Marco Mignardi
View author publications
Search author on: PubMed Google Scholar
Alina Isakova
View author publications
Search author on: PubMed Google Scholar
Wenying Pan
View author publications
Search author on: PubMed Google Scholar
Carlos Simon
View author publications
Search author on: PubMed Google Scholar
Stephen R. Quake
View author publications
Search author on: PubMed Google Scholar
Contributions
W.W., W.P., F.V., C.S. and S.R.Q. conceived and designed the study. W.W., F.V., I.M. and A.I. performed experiments. W.W. performed single-cell experiments, RNAscope experiments and imaging. A.I. performed single-cell experiments. F.V. optimized the tissue dissociation protocol. I.M. performed tissue dissociation and immunofluorescence experiments. P.A. collected endometrial biopsies. W.W. and S.R.Q. analyzed single-cell RNA-seq data. M.M. and W.W. analyzed RNAscope data. W.W., F.V., C.S. and S.R.Q. interpreted the results. W.W., F.V., C.S. and S.R.Q. wrote the manuscript.
Corresponding authors
Correspondence to Carlos Simon or Stephen R. Quake .
Ethics declarations
Competing interests
A patent disclosure has been filed for the study under the inventors S.R.Q., C.S., W.W. and F.V. C.S. is Founder and Head of the Scientific Advisory Board of Igenomix SL. P.A., I.M., M.M., A.I. and W.P. declare no competing interests.
Additional information
Peer review information Saheli Sadanand was the primary editor on this article and managed its editorial process and peer review in collaboration with the rest of the editorial team.
Publisher’s note Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.
Extended data
Extended Data Fig. 1 Data summary.
a , Number of single cells analyzed across the human menstrual cycle in the C1 dataset. b , C1: Relationship between the day of menstrual cycle (day) and endometrial phase/subphase assigned by single cell transcriptome data as in Fig. 4 for each woman (dot) in the C1 dataset. Arrows annotate discrepancy between day and phase/subphase where 1) orders were reversed for a pair of women between their orders in phase/subphase assignment and their cycle day (red) and 2) women on the same day of cycle were assigned into different phases or subphases (black). 10x: The day of menstrual cycle for each woman (dot) in the 10x dataset. Dots with * and # to the right are anchors shared between the two datasets ( Methods ). c , For each woman (dot: top, middle panel; bar: bottom panel) in the C1 dataset: (top) relationship between her pseudotime order (x-axis) and her cycle day, (middle) total number of single cells analyzed, (bottom) distribution of the six cell types identified by the C1 dataset. From left to right, women were ordered based on the median pseudotime of all her stromal fibroblasts and unciliated epithelia. Pseudotime and phase were as assigned in Fig. 3a . Related to Fig. 1 , 3 , 4 .
Extended Data Fig. 2 Summary of cell types and states in the 10x validation dataset.
a , Dimension reduction (UMAP on top PCs) on 71032 single cells from 10 healthy human endometria. Integration was done across donors using Seurat IntegrateData() to decouple temporal signal. b , Distribution of cycling cells. c , Relative abundance of each cell type/subtype identified. Each black dot is a woman. Dots in pink are medians. d , Total number of cells analyzed per cell type/subtype. e , Expression of top discriminatory genes identified by the C1 dataset (Fig. 1b ) and for smooth muscle cells. f , Expression of markers identifying cells with mesenchymal stem cell features in the human endometrium. g , Combinatorial expression of PDGFRB and MCAM in smooth muscle cells. In brackets: abundance of each of the four cell groups normalized by the total smooth muscle cell count. (Expression values were jittered (amount=0.1) for visualization.) h , Percent cells expressing SUSD2 in the four cell groups identified in ( g ). Related to Fig. 1 , 5 .
Extended Data Fig. 3 Constructing single cell resolution trajectories of the human menstrual cycle using mutual information (MI) based approach.
a , Dimension reduction (tSNE) using whole transcriptome data, that is all genes detected, for unciliated epithelia (epi) and stromal fibroblasts (str), respectively, led to identification of four major phases (insets). b , MI between expressions of each gene and time (red) or permutated time (black). Genes were ranked by their MI with time. c , tSNE using ‘time-associated genes’ for epi and str, respectively led to the identification of the same four major phases as in ( a ) and trajectories of endometrial transformation. In a , c main panels, cells were colored by the day of menstrual cycle (day). Related to Fig. 3 .
Extended Data Fig. 4 Global temporal transcriptome dynamics across the human menstrual cycle.
a , MI between expressions of each pseudotime-associated gene (FDR<1E-05) and pseudotime (red) or permutated pseudotime (black) for unciliated epithelia (epi) and stromal fibroblasts (str). b , Dynamics of pseudotime- associated genes across the menstrual cycle. Related to Fig. 4 .
Extended Data Fig. 5 Dynamics of WOI-associated genes in the 10x validation dataset.
a-b , Dimension reduction (UMAP on top PCs) on unciliated epithelia ( a ) and stromal fibroblasts ( b ) in the 10x dataset. Highlighted are anchors between the C1 and 10x datasets ( Methods ). Phases were assigned based on relative order between each cell group and the anchors. c , Relationship between the day of menstrual cycle and phase assignment. In blue are anchors. d-e , Dynamics of WOI-associated genes in Fig. 4 stratified by epithelial subpopulations ( d ) and stromal fibroblasts ( e ). MTIX , FGF7 , and LMCD1 peaked at non-WOI phases in the C1 dataset and were included as references. White dots: medians; Boundaries of black bars: 25% and 75% quantiles. Highlighted in blue are cell groups where the anchors grouped with. Related to Fig. 4 .
Extended Data Fig. 6 Dynamics of genes encoding transcriptional factors (TF) across the menstrual cycle.
a - b , All time-associated TFs for unciliated epithelia (epi, a ) and stromal fibroblasts (str, b ) (TFs bracketed by red bars were zoomed in c , d ). c-d , TFs that are associated with the entrance/exit of WOI (bottom panel) or phase-defining (top) in epi ( c ) and str ( d ). e , Expression of TFs that are nuclear hormone receptors for steroid hormones estrogen ( ESR1 ), progesterone ( PGR ), glucocorticoid ( NR3C1 ), and androgen ( AR ). For heatmap, TFs were ordered first by the pseudotime of the major peak and then by the pseudotime of the peak’s inflection point. Full list of pseudotime-associated TFs can be found in Supplementary Table 2 . Related to Fig. 4 .
Extended Data Fig. 7 Dynamics of genes encoding secretory proteins (sec genes) across the menstrual cycle.
a - b , All time-associated sec genes for unciliated epithelia (epi, a ) and stromal fibroblasts (str, b ) (sec genes bracketed by blue bars were zoomed in c , d ). c - d , Sec genes that are associated with the entrance/exit of WOI (bottom) in epi ( c ) and str ( d ). e-f , Expression of sec genes encoding canonical protein markers for decidualization during pregnancy in epi ( e ) and str ( f ). For heatmap, sec genes were ordered following the same strategy as in Extended Data Fig. 6 . Full list of pseudotime-associated sec genes can be found in Supplementary Table 3 . Related to Fig. 4 .
Extended Data Fig. 8 Expression of genes that define human early-pregnant endometrial stromal fibroblast subtypes.
a , Abundance of stromal fibroblasts (str) and unciliated epithelia (epi) expressing IGFBP1 , PRL , or both in non-pregnant human endometria across the menstrual cycle. Phases were assigned as in Extended Data Fig. 5 . b , Distribution of stromal fibroblasts co-expressing IGFBP1 and PRL on the reduced dimension of all late-secretory stromal fibroblasts. c , Dispersion level of all genes detected in late-secretory stromal fibroblasts. Highlighted are genes reported to differentially express in the two early-pregnant subtypes that do not co-express IGFBP1 and PRL . d , Some of the subtype genes that are highly dispersed in ( c ), for example ACTA2 , IGFBP1 , showed a subtle expression gradient (arrow) on dimension-reduced late-secretory stromal fibroblasts. In c , d , red and blue indicate genes reported to define the two early-pregnant subtypes, respectively.
Extended Data Fig. 9 Dynamics of cell cycling activity across the menstrual cycle and transcriptomic signature of proliferative phases.
a - b , Endometrial G1/S and G2/M signatures for unciliated epithelia (epi, a ) and stromal fibroblasts (str, b ) identified in the C1 dataset. c - d , Distribution (left) and abundance (right) of cycling cells across major phases of the menstrual cycle. e - f , Top discriminatory genes for the two proliferative phases identified in epi ( e ) and str ( f ). Related to Fig. 4 .
Extended Data Fig. 10 Deviating subpopulations in unciliated epithelia and their transcriptomic signatures across the menstrual cycle.
a . Dimension reduction (UMAP on top PCs) on all unciliated epithelia in the 10x validation dataset and distribution of cycling cells. Integration was done across donors using Seurat IntegrateData() to decouple temporal signal. b , Expression of markers differentially expressed between the two subpopulations that were identified in the C1 dataset. In black are genes in Fig. 5b . In orange are genes in Fig. 5c, d that were previously shown to be differentially expressed by glandular or luminal epithelia of human endometria in situ . c , Dynamics of differentially expressed genes between the two subpopulations in proliferative phases identified in the C1 dataset. Related to Fig. 5 .
Supplementary information
Supplementary Information (download PDF )
Supplementary Figs. 1–4.
Reporting Summary (download PDF )
Supplementary Tables 1–5. (download XLSX )
Supplementary Data 1 (download XLSX )
Supplementary Dataset 1. Data were extracted from all representative fields of view captured for Fig. 2a–d and were used to generate Fig. 2e.
Source data
Source Data Fig. 3. (download XLSX )
Statistical source data.
Rights and permissions
Reprints and permissions
About this article
Cite this article
Wang, W., Vilella, F., Alama, P. et al. Single-cell transcriptomic atlas of the human endometrium during the menstrual cycle. Nat Med 26 , 1644–1653 (2020). https://doi.org/10.1038/s41591-020-1040-z
Download citation
Received : 06 August 2019
Accepted : 29 July 2020
Published : 14 September 2020
Version of record : 14 September 2020
Issue date : October 2020
DOI : https://doi.org/10.1038/s41591-020-1040-z
Share this article
Anyone you share the following link with will be able to read this content:
Get shareable link
Sorry, a shareable link is not currently available for this article.
Copy shareable link to clipboard
Provided by the Springer Nature SharedIt content-sharing initiative
You have full access to this article via California Institute of Technology .
Associated content
Multidimensional transcriptomic mapping of human endometrium at single-cell resolution
Linda C. Giudice
Nature Medicine News & Views 14 Sept 2020
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
Sign up for the Nature Briefing newsletter — what matters in science, free to your inbox daily.
Email address
Sign up
I agree my information will be processed in accordance with the Nature and Springer Nature Limited Privacy Policy .
Close
Get the most important science stories of the day, free in your inbox. Sign up for Nature Briefing
