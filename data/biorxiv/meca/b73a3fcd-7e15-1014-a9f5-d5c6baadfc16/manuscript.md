# Are Different Populations Fairly Represented in Single-Cell Omic Atlases?

## Authors

- Catrina Yang<sup>1</sup>
- Kavitharini Saravanan<sup>2</sup>
- Aryan Saharan<sup>3</sup>
- Kuan-lin Huang<sup>4</sup> †

### Affiliations

1. University of Oxford, Green Templeton College, Medical Sciences Division Oxford, OX2 6HG UK
2. University of North Carolina at Charlotte Charlotte, NC USA
3. Saint Louis University St. Louis, MO USA
4. Department of Genetics and Genomic Sciences, Department of Artificial Intelligence and Human Health, Center for Transformative Disease Modeling, Tisch Cancer Institute, Icahn Genomics Institute, Icahn School of Medicine at Mount Sinai New York, NY 10029 USA

† Corresponding author

## Abstract

ABSTRACT
Single-cell Omic atlases are transforming biology and medicine, yet their demographic representativeness has not been systematically evaluated. We conducted a secondary analysis of >13,500 samples from the Human Cell Atlas (HCA), Human Tumor Atlas Network (HTAN), and PsychAD Consortium. Benchmarking against global and US general and disease-prevalence data, we found a striking, pervasive European over-representation and underrepresentation of Asian and Latino individuals. Nearly 70% of HCA samples lacked ancestry annotation, HTAN tumors were 69% European, and PsychAD showed more balanced non-European representation but markedly few Asians. Sex distributions in these atlases also skewed compared to published disease prevalence. These disparities highlight that current single-cell resources risk embedding inequities into AI foundational models, biomarker discovery, and therapeutic development.

## MAIN

Single-cell omics technologies have revolutionized our understanding of cellular heterogeneity, enabling the discovery of rare cell types, transitional states, and microenvironmental dynamics that bulk approaches obscure. Large-scale initiatives such as the Human Cell Atlas (HCA)1-3, the Human Tumor Atlas Network (HTAN)4,5, and the PsychAD consortium4,6 have generated expansive datasets spanning healthy tissues, tumor microenvironments, and neuropsychiatric or neurodegenerative conditions. These resources are invaluable to biomedical discovery, but systematic evaluation of their demographic composition has been limited, raising concerns about their representativeness and generalizability.

The challenge of representation has long plagued human genomics. Genome-wide association studies (GWAS) have been overwhelmingly conducted in individuals of European ancestry, leading to biased polygenic risk scores (PRS) that transfer poorly to other populations7,8. PRS derived from European cohorts often lose their predictive accuracy when applied to non-European groups9,10. Beyond causing technical issues for research, the lack of diversity in genomics risks reinforcing health disparities when biomedically-actionable findings are disproportionately relevant to majority populations11.

Single-cell consortia, where significant resources are unified to survey cellular profiles in thousands of individuals, risk reproducing these inequities. The outputs of these large-scale studies are often marketed as universal reference maps of human biology and used to train foundation models2,12-14. However, recent studies have suggested that the profiled cellular omic signatures could indeed be ancestry- and sex-specific15,16, calling for the need to establish single cell genomics datasets based on different populations. Here, we systematically evaluate ethnicity/race and sex representation of sampled individuals in three major single cell consortia resources (Table 1), providing a diversity audit to inform future study designs.

**Table 1.**
 Overall ancestry and sex composition of individuals from the Human Cell Atlas (HCA), Human Tumor Atlas Network (HTAN), and the PsychAD consortia evaluated in this study


### Human Cell Atlas (HCA) vs. Global Population Demographics

The HCA dataset comprised 10,125 samples across 15 tissue categories1,2, the largest included immune (n = 3,704, 36.6%), gut (n = 883, 8.7%), skin (n = 906, 8.9%), lung (n = 743, 7.3%), and kidney (n = 601, 5.9%)(Supplementary Figure 1, Supplementary Table S1). Overall, 69.9% of samples lacked ancestry annotation after we thoroughly cataloged data from the HCA website or Supplementary Information reported by the linked publications (Methods). Among the 3,043 samples with reported ancestry, Europeans comprised 56.5%, followed by Asians (21.1%), Africans (10.4%), Latinos (6.2%), and Other (5.8%)(Figure 1A). Compared to global expectations (Europe 9.4%, Asia 59.4%, Africa 17.6%, Latino 13.6%), Europeans were overrepresented sixfold, while Asians, Africans, and Latinos were consistently underrepresented (0.36×, 0.59×, and 0.45×, respectively; p < 2e-16).

![Figure 1.](content/677375v1_fig1.tif)

**Figure 1.:** (A) Comparison of ancestry proportions in HCA (excluding samples with unknown ancestries, in red bars), with proportions of European, African, Asian, Latino, Other ancestry to the global reference data (in blue bars).
(B) Stacked barplots of ancestry distributions across 15 HCA tissue categories (excluding samples with unknown ancestries), with proportions of European, African, Asian, Latino, Other, and Unknown ancestry shown for each tissue.
(C) Comparison of sex proportions in HCA (excluding samples with unknown sexes, in red bars) to global population reference distributions (in blue bars).
(D) Stacked barplots of sex distributions across 15 HCA tissue categories (excluding samples with unknown ancestries), with proportions of female and male shown for each tissue

Tissue-level analyses revealed pronounced but heterogeneous skews—all tests compare observed ancestry mix within tissue to the global reference mix (see Methods) showed FDR <0.01, except for musculoskeletal where 205/226 were of unknown ancestry (Figure 1B). Among ancestry-labeled samples most biased for European samples, skin was 82.9% European, lung 79.3%, eye 77.8%, musculoskeletal 76.2%, and heart 65.5% European. By contrast, immune and gut showed comparatively higher Asian representation (41.7% and 41.6%, respectively), with lower European fractions (immune 46.5%, gut 39.2%). African ancestry individuals were better represented in development (45.2%), kidney (25.3%), and breast (23.9%) atlases, whereas latino individuals showed higher representation in liver (27.4%), adipose (21.4%), and reproduction (18.9%) atlases (Figure 1B). We note that high ancestry-missingness in HCA (69.9%) likely obscure the true ancestry compositions and should be addressed in future releases.

Sex ratios in HCA were 34.0% female, 36.6% male, and 29.4% unreported (Supplementary Figure 1)(Figure 1C). Among samples with sex information, expected skews were observed in breast (89.0% female) and reproductive tissues (66.2% female). Several tissues were modestly male-enriched, including immune (54.3% male), eye (68.1% male), lung (56.1% male), and musculoskeletal. No significant sex biases were observed for adipose, development, gut, kidney, and liver (P>0.17), suggesting more balanced sampling in these tissue atlases (Figure 1D). These sex patterns are sometimes directionally consistent with physiological expectations in sex-specific disease tissues, but also suggest potential ascertainment or study-design bias elsewhere.

### The Human Tumor Atlas Network (HTAN) vs. the US Cancer Population Incidence

The HTAN dataset comprised 1,959 tumor samples across 22 cancer types 4,5. Breast cancer was the largest contributor (n = 993, 50.7%), followed by lung (n = 245, 12.5%), colorectal/colon (n = 151, 7.7%), skin (n = 79, 4.0%), neuroblastoma (n = 74, 3.8%), pancreas (n = 47, 2.4%), ovary (n = 26, 1.3%), and several smaller categories (<20 cases each)(Supplementary Figure 2, Supplementary Table S2). Overall, 12.3% of samples lacked ancestry annotation. Among the 1,719 samples with reported ancestry, Europeans comprised 78.3%, Africans 17.3%, Asians 2.0%, Latinos 2.0%, and Other 0.3%.

Cancer-specific ancestry distributions revealed additional skew in several cancer types compared to their expected US incidences (Figure 2A-B). Within samples with annotated ancestry data, all the cancer tissue sites showed over 72% European. For example, skin cancer showed 96.1% European, pancreas 93.6% European, ovary 92.3% European, liver 88.9% European, and lung 87.1% European. Substantial African representations were found in blood tumors (27.3%), breast (25.3%), cervix (21.1%), and neuroblastoma (17.8%). Asian and latino participants were severely under-represented in all cancer tissue sites; the highest count of Asian was in lung (N=15) that comprised 7.8% of the cohort, whereas the highest count of Latino was found in colorectal cancer (N=15)(Figure 2A-B).

![Figure 2.](content/677375v1_fig2.tif)

**Figure 2.:** (A-B) Stacked barplots comparing ancestry distributions across 11 major cancer categories in
(A) HTAN (excluding samples with unknown ancestry) vs. the reference SEER cancer incidence data of the respective cancer type, as shown in proportions of European, African, Asian, Latino, Other, and Unknown ancestry.
(B) Stacked barplots of sex distributions across the same cancer types, showing female, male, and missing annotations.
(C-D) Stacked barplots comparing sex proportions in (C) HTAN (excluding samples with unknown sex) to (D) the reference SEER cancer incidence data of the respective cancer type.

The overall sex distribution was heavily female (74.3% female, 21.1% male, 4.6% unreported)(Supplementary Figure 2), driven by the predominance of breast cancer that comprised over half the cohort and minorly by other sites, i.e., ovary, cervix, that were female specific. Considering only cases with reported sex, multiple cancer type showed a female skew in HTAN, such as liver (68.4% female), lung (49%), blood (58.3%), and skin (47.4%) tumors, compared to the SEER female/male incidence of those respective cancers (Figure 2C-D).

### The PsychAD Consortium vs. US Demographics in Neurological Diseases

The PsychAD dataset comprised 1,494 samples drawn from three contributing cohorts: HBCC (n = 300), MSBB (n = 1,042), and RADC (n = 152)4,6. Across the cohort, diagnostic categories included Alzheimer’s disease (AD_combined, n = 373, 25.0%), schizophrenia (SCZ, n = 120, 8.0%), dementia with Lewy bodies (DLBD, n = 112, 7.5%), vascular dementia (n = 85, 5.7%), bipolar disorder (BD, n = 55, 3.7%), tauopathies (n = 47, 3.1%), Parkinson’s disease (PD, n = 40, 2.7%), frontotemporal dementia (FTD, n = 15, 1.0%), and dementia not otherwise specified (n = 439, 29.4%); in PsychAD, some individuals may have multiple diagnosis and 597 individuals who do not have any of these diagnoses (Supplementary Figure 3, Supplementary Table S3).

Among all 1,494 Psych samples, Europeans accounted for 65.9%, Africans 22.6%, Latinos 9.0%, Asians 1.8%, and Unknown 0.6%. Compared to ADRD reference demographics in the United States (Europeans 59.1%, Africans 12.2%, Latinos 9.2%, Asians 6.6%)(Methods) (Figure 3A-B), AD cases in PsychAD were characterized by overrepresentation of Europeans (71.6%), slightly higher representation of Africans (17.2%) and near parity Latino (9.4%), but marked underrepresentation of Asians (1.4%). For other diseases, Europeans are heavily represented in FTD (86.7%), BD (81.8%), and DLBD (77.7%). African individuals comprised a significant fraction of Vascular dementia (31.8%) and SCZ cases (26.7%). The highest percentage of Latino individuals were found within Tau (19.2%) and FTD (13.3%) cases. The highest fraction of Asian was found in PD and BD with mere 7.5% and 5.5%, respectively (Figure 3A-B).

![Figure 3.](content/677375v1_fig3.tif)

**Figure 3.:** (A) Stacked barplots of ancestry distributions across 9 diagnostic categories, including Alzheimer’s disease, schizophrenia, dementia with Lewy bodies, vascular dementia, bipolar disorder, tauopathies, Parkinson’s disease, frontotemporal dementia, and dementia not otherwise specified.
(B) Comparison of ancestry proportions in PyschAD Alzheimer’s disease cases (excluding samples with unknown ancestries, in red bars), with proportions of European, African, Asian, Latino, Other ancestry to the reference data of Alzheimer’s disease and related dementia cases (in blue bars).
(C-D) Stacked barplots comparing sex proportions in (C) PyschAD (excluding samples with unknown ancestries) to (D) the reference data from literature for each dementia type.

Overall sex balance was near parity: 51.6% female and 48.4% male (Supplementary Figure 3). Disease-level analyses revealed stronger deviations compared to each disease’s sex reference data (Methods) (Figure 3C-D). AD and dementia not otherwise specified were 64.6/64.9% female, consistent with known female predominance. Vascular dementia also showed female enrichment in PyschAD (63.5% female). On the other hand, male skew were seen in SCZ (59.2% male, aligned with literature’s 58.7%), BD (54.6%), FTD (60%), and control (57.8%). While PD had 20 males and 20 females in PyschAD, the known disease incidence is about 60% male (Figure 3C-D).

### Significant Ancestry and Sex-Biases Exist in Large-Scale scRNA-Seq Studies

Our systematic assessment across HCA1,2, HTAN4,5, and PsychAD4,6 shows that demographic bias is pervasive in single-cell resources. HCA had nearly 70% missing ancestry annotation, and among labeled donors, European individuals dominated (56.5%), far exceeding their expected global share (9.4%). HTAN revealed even starker distortions: Europeans comprised >78% of annotated samples compared to 23% expected from SEER cancer incidence, while Asians and Latinos were underrepresented by over 90%. PsychAD presented a somewhat more balanced profile, with African ancestry represented at 22.6% (higher than expected based on ADRD prevalence), but Asians were again underrepresented (1.8% vs. 6.6%). Sex balance was dataset-dependent: near parity in PsychAD overall, modest male skewing in HCA immune tissues, and strong female skewing in HTAN across both sex-specific and non–sex-specific cancers.

These findings extend the well-documented inequities of genomics7,9,11. Just as GWAS and PRS suffer from limited transferability across ancestries8,10, single-cell resources biased toward European donors risk producing cell atlases and disease maps that fail to generalize globally. This is not a trivial concern: genetic background influences gene expression and regulatory variation17, sex differences shape immune responses and disease trajectories18, and ancestry-associated biology can alter therapeutic options and responses. Large-scale sequencing studies have revealed many pathogenic mutations and genetic alterations are unique to diverse populations19-21; what if some of the rare and pathogenic cell types are also population specific? Overrepresentation of Europeans in single-cell genomics precludes discovery of biology that exists across the wide spectrum of human diversity and risks building single-cell models that obscure the cellular mechanisms most relevant to underrepresented groups.

This study has several limitations. First, ancestry was analyzed as reported metadata rather than genetically inferred, which may introduce misclassification. Classifying ancestry groups into broad categories like “European” or “Asian” is challenging due to the complex and personal nature of ethnic identity. Some groups, such as Ashkenazi Jews, classified as “European,” have distinct cultural and genetic backgrounds that may not fit neatly into this category. Similarly, “Hispanic/Latino” encompasses individuals with mixed heritage. Second, the high degree of missing data limits resolution. Third, small sample sizes for certain groups reduced statistical power for some disease-specific comparisons. Fourth, the use of reference populations herein is limited by their surveyed populations and timepoints, for example, the global demographics continental population shares used for HCA will not match genetic ancestry estimates. Finally, our analyses focused on 3 publicly available single-cell consortium datasets, which may not reflect the demographic composition of all other single-cell omic resources. Despite these caveats, the consistency of European overrepresentation and Asian/Latino underrepresentation across these datasets underscores the robustness of our conclusions.

### How Can We Fix this Disparity?

The implications of disparity in single-cell omics are both scientific and societal. Scientifically, biased datasets constrain the interpretability of findings, hinder reproducibility, and limit the scope of discovery. Societally, they risk exacerbating health disparities by embedding inequities into the reference frameworks that guide biomarker discovery, drug development, and precision medicine. This is especially problematic when much of these advances may be driven by foundation models built on the potential biased datasets. Missing metadata compounds these problems, as incomplete annotation disproportionately affects careful study designs that account for diversity and limits the interpretability of cross-population analyses.

Moving forward, several structural reforms are needed. First, intentional recruitment strategies should align donor sampling with disease incidence and population demographics22, as proposed in recent roadmaps for equity in genomics9. Second, metadata completeness and standardization should be mandated in single cell repositories, with ancestry, sex, and clinical variables treated as required fields. This can be achieved by working groups that provide harmonized toolsets and checklists like the HCA Ethnics Working Group23. Indeed, dataset such as PsychAD has much more complete metadata and non-European representation, suggesting this could be achieved with careful study and workflow design. Finally, equity metrics should be adopted as benchmarks for evaluating single-cell datasets, complementing measures of resolution and scale with measures of demographic diversity.

To translate these findings into actionable steps, we developed a practical checklist (Table 2) that research teams can apply during study design. The table frames 12 critical questions— such as whether planned cohorts reflect disease incidence, whether sex balance and subgroup sample sizes are adequate, and whether under-represented community sites are included in recruitment—and pairs them with concrete solutions, including targeted sampling, stratified quotas, standardized biobanking protocols, and mandatory metadata fields. This structured approach provides a guide for anticipating and addressing demographic imbalances before they are embedded in single-cell datasets and address bias proactively.

**Table 2.**
 Key design considerations for ensuring fair representation in single-cell studies


In summary, our findings show that single cell omics is at risk of repeating the inequities long criticized in genomics. Unless deliberate corrective actions are taken, the benefits of cell atlases will be unevenly distributed, disproportionately serving populations that are already well represented. Embedding diversity, equity, and completeness at the foundation of single-cell omic research will be essential to realizing its promise as a universal reference for human biology.

## METHODS

### Study Design and Data Sources

We conducted a systematic evaluation of sex- and ancestry-related representation across three large-scale single-cell resources: the Human Cell Atlas (HCA), the Human Tumor Atlas Network (HTAN), and the PsychAD consortium. These datasets were chosen because they represent flagship community efforts to generate, harmonize, and disseminate high-resolution cellular and disease-relevant data. For contextual benchmarking, we compared observed representation in each dataset against appropriate reference distributions: (1) global ancestry proportions from United Nations population statistics for HCA; (2) SEER cancer incidence rates stratified by ancestry and sex for HTAN; and (3) Alzheimer’s disease and related dementias (ADRD) prevalence estimates for PsychAD. Each of these data sources were described in detail in the later sections of the Methods.

In brief, metadata files from HCA, HTAN, and PsychAD were harmonized into canonical categories. Ancestry was standardized into African, Asian, European, Latino, Other, and Unknown. For HTAN, Hispanic/Latino identifiers were mapped to “Latino” regardless of race; for PsychAD, genetic ancestry labels (e.g., EUR, AFR, AMR, EAS, SAS) were collapsed into the canonical categories. Biological sex was standardized to female, male, or missing. For disease and tissue annotations, HCA samples were grouped by tissue of origin (15 categories), HTAN samples by cancer type (22 categories), and PsychAD samples by diagnosis (9 categories).

### Statistical Analyses

We computed descriptive statistics for ancestry and sex distributions overall and within tissues or disease categories. Representation was quantified both as raw counts and as proportions among non-missing annotations. Chi-square tests compared observed vs. expected representation, using equal-distribution and population-level baselines (global ancestry, SEER, or ADRD). To measure magnitude of imbalances, we calculated representation ratios (observed ÷ expected), equity indices (symmetrized measures of under- vs. overrepresentation), and diversity metrics (Simpson’s and Shannon’s indices). Intersectional analyses assessed ancestry × sex strata at dataset and disease levels.

For HCA, analyses were stratified by tissue type; for HTAN, by cancer type; and for PsychAD, by diagnosis. Within each stratum, we assessed ancestry composition, sex distribution, and statistical significance relative to reference populations. We flagged highly skewed categories (defined as >70% representation from a single ancestry or >65% representation by one sex where not biologically expected).

We also quantified missingness for demographic and clinical covariates. In HCA, we measured missingness for ancestry, sex, and study identifiers. In HTAN, missingness was assessed for tumor grade and stage. In PsychAD, we quantified missingness for neuropathological measures (Braak, CERAD), APOE genotype, and dementia status. Missing data were stratified by ancestry and sex to identify whether gaps disproportionately affected underrepresented groups.

All analyses were performed in R using packages including dplyr, tidyr, ggplot2, car, and scipy. Scripts were version-controlled, and all transformations were logged for reproducibility.

### Global reference population

To approximate global “ancestry” composition in a way that is transparent and reproducible, we used share of the world population by major world region (continent). Specifically, we used the widely-cited 2021 distribution: Asia 59.4%, Africa 17.6%, Europe 9.4%, North America 7.5%, South America 5.5%, Oceania 0.6%. These values correspond to UN-based tallies compiled in the “World population by continent, 2021” table24. We combined North America + Oceania into a single bucket when needed. Although “ancestry” is not directly measurable at a global scale, continental population shares provide a neutral, geography-based reference that is stable year-to-year and can be transparently mapped.

Global sex composition was derived from the United Nations World Population Prospects (WPP) 2022 summary, which reports that the world had 50.3% males and 49.7% females in 202225.

### U.S. Cancer reference population

We used SEER*Explorer (National Cancer Institute) to obtain age-adjusted incidence rates (per 100,000) for 2018–2022 by cancer site, race/ethnicity, and sex. SEER*Explorer methods specify that rates are age-adjusted to the 2000 U.S. standard population and are reported per 100,000 persons; incidence estimates incorporate SEER delay-adjustment methodology26.

For ancestry/ethnicity, we used the five mutually exclusive SEER race/ethnicity categories:

These are standard, mutually exclusive SEER groupings (Hispanic supersedes race). Sex was coded as Male and Female.

SEER provides rates rather than percentage shares. To construct reference distributions (for ancestry and for sex) within each cancer site:

Because rates are age-adjusted, the share is a proxy for the composition of incident cases, not general population composition.

### ADRD reference population

#### U.S. ancestry/ethnicity composition (ADRD)

For Alzheimer’s disease and related dementias (ADRD), we used the analysis by Matthews et al. (2019), which reported age-standardized prevalence estimates by race/ethnicity in adults aged ≥65 years27. Specifically, they reported the 2014 number of Medicare Fee-for-Service (FFS) beneficiaries with ADRD in each of the NH white, black, Asian and Pacific Islander (annotated as Asian for our analysis), Hispanic (annotated as Latino for our analysis), and American Indian and Alaska Native as well as Other (grouped into Others for our analysis). For the other diseases, we could not find consistent race-specific incidence data and thus were not modelled.

#### Sex composition

To standardize sex differences in incidence and prevalence across neuropsychiatric and neurodegenerative diseases in the United States, we relied on the best available population-based studies and large systematic reviews, converting reported sex-specific rates or ratios into fractions that sum to one. For Alzheimer’s disease and related dementias (AD/ADRD), we adopted the Global Burden of Disease 2019 estimate showing that globally in 2019, there were substantially more women than men living with dementia, with a female-to-male ratio of 1.69 (95% UI 1.64–1.73)28. For bipolar disorder, U.S. National Comorbidity Survey data indicate nearly equal prevalence—2.8% in women versus 2.9% in men—resulting in fractions of 0.491 and 0.509, respectively29. Dementia with Lewy bodies is markedly male-predominant: in Olmsted County, Minnesota, incidence was 4.8 per 100,000 person-years in men compared to 2.2 in women, yielding fractions of 0.314 and 0.68630. Frontotemporal dementia overall shows little sex bias, with pooled case series reporting near parity (373 males vs. 338 females), translating to fractions of 0.525 and 0.47531. Parkinson’s disease consistently demonstrates male predominance in North America, with men approximately 1.5 times more likely than women to develop the disease, corresponding to fractions of 0.600 and 0.40032. Schizophrenia also occurs more frequently in men, with meta-analyses estimating a male-to-female incidence rate ratio of ∼1.42:1, equivalent to 0.587 male and 0.413 female fractions33. Tauopathies as an aggregate entity are epidemiologically heterogeneous: progressive supranuclear palsy often shows modest male predominance, while corticobasal degeneration is closer to balanced; given the inconsistency, we reported a neutral 0.5/0.5 split as an aggregate reference34. Finally, vascular dementia appears more common in men in high-income cohorts, with estimates such as 5.6 vs. 3.2 cases per 1,000 person-years, corresponding to 0.636 male and 0.364 female fractions35.

### Curation of Demographic Data in Single-Cell Consortia Studies

#### Human Cell Atlas (HCA)

##### Data Source

We used publicly available datasets from the Human Cell Atlas (HCA) Bionetwork1-3 to assess ethnic disparities in single-cell genomics research. The analysis covered datasets from 14 HCA networks, including: adipose, breast, development, eye, gut, heart, immune, kidney, liver, musculoskeletal, nervous system, oral and craniofacial, pancreas, reproduction, and skin. Two networks, genetic diversity and organoid, did not have available datasets, while the lung and nervous system networks included fully developed cell atlases and were excluded from this analysis.

##### Dataset Selection and Metadata Extraction

For each network, we accessed all available datasets to review the associated metadata files, typically provided in Excel spreadsheet format. These metadata files were examined to identify clinical and demographic information about the donors, specifically focusing on age, gender, ethnicity, and disease status. If demographic metadata was present, we extracted and compiled the relevant information into a single comprehensive spreadsheet for each network.

In cases where ethnicity data was absent from the metadata, we manually reviewed the publications associated with the dataset. These publications were linked within each dataset’s page and often contained supplementary information. Ethnicity data was most frequently found in the Materials and Methods sections or the supplementary materials of these publications. We documented the presence or absence of metadata for each dataset and categorized the ethnicity reporting as follows:

If ethnicity was provided in the metadata, the column asking about ethnicity data in publications was marked as “N/A.” In cases where the ethnicity data in the publication were incomplete or unclear (e.g., presented as proportions or graphs without clear detail), we flagged this limitation with an asterisk.

### Standardization of Ethnicity Categories

Given the variability in how ethnicity data were reported across projects (e.g., “Asian,” “East Asian,” or “Korean”), we standardized the ethnicity categories to allow for consistent comparisons across datasets. The following broad categories were used:

Donors from other species (e.g., Mus musculus) and cell lines, including human-induced pluripotent stem cells (iPSCs), were excluded from the dataset.

### HTAN (Human Tumor Atlas Network)

We analyzed HTAN (Human Tumor Atlas Network)4,5 data by filtering for datasets with single cell RNA sequencing data (scRNA-seq). For each HTAN dataset, we accessed the associated metadata files and reviewed sample-level attributes including primary tissue of origin, tumor type, anatomical location, and contributing research center. To ensure consistency across datasets, we created a standardized labeling system for tissue origin and tumor site, modeled after the category structure used on the HTAN homepage. Where metadata fields were ambiguous or inconsistent, we manually reconciled them using information from the associated publications and supplementary materials. Each sample was then re-annotated using this uniform classification framework, allowing for improved comparison across atlases. The curated metadata was compiled into a master file that enables streamlined analysis of tissue-specific patterns and site-based tumor characteristics. When available, publication links were included to reference original annotations and methods.

To classify ancestry groups, metadata for scRNA-seq from HTAN were extracted and analyzed for racial/ethnic differences to be processed. Racial labels were standardized and all empty rows were removed. For the purpose of this study, individuals reported as Hispanic/Latino were considered as Latino, individuals reported White but non-Latino or missing ethnicity were considered as European, individuals reported as African or African American were considered as African, individuals reported to be East Asian, South Asian, or EAS_SAS were considered Asian, individuals reported to be other values were considered as Other, and Unknown or missing data were considered as Unknown.

### PsychAD Consortium

We downloaded the metadata from the Supplementary Table 1 of PsychAD’s latest data release and landmark manuscript6 as of May 2025.

## Supporting information
