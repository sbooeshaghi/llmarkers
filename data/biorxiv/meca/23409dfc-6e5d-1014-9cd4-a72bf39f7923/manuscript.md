# Extended taxonomic profiling of diverse environments with mOTUs 2.6

## Authors

- Hans-Joachim Ruscheweyh<sup>1</sup>
- Alessio Milanese<sup>1</sup>
- Lucas Paoli<sup>1</sup>
- Quentin Clayssen<sup>1</sup>
- Daniel Mende<sup>3</sup>
- Georg Zeller<sup>2</sup> †
- Shinichi Sunagawa<sup>1</sup> †

### Affiliations

1. Department of Biology, Institute of Microbiology and Swiss Institute of Bioinformatics ETH Zürich, Zürich 8093 Switzerland
2. Structural and Computational Biology Unit, European Molecular Biology Laboratory 69117 Heidelberg Germany
3. Department of Medical Microbiology, Amsterdam UMC, University of Amsterdam Amsterdam the Netherlands

† Corresponding author

## Abstract

Abstract

Summary
Identifying species and estimating their relative abundance in metagenomic samples is a crucial task in microbiome research. However, for many environments, variable fractions of microbial species are not represented in reference genome databases, and thus, remain often unaccounted for in taxonomic composition analyses. Here, we present an updated version of the metagenomic profiling tool mOTUs. We extended its database of taxonomic marker genes by including information from ~600,000 prokaryotic draft genomes, >96% of which are metagenome assembled genomes from 23 environments. This extension enables researchers to profile a previously underrepresented diversity of microbes not only in some of the most intensively studied environments such as the human, soil and ocean microbiomes, but also in freshwater systems, the air, and the gastrointestinal tract of mice, cattle and other animals. This update doubles the number of detectable prokaryotic species to 33,570 and includes the release of 11,164 taxonomic profiles as a community resource.


Availability and implementation
mOTUs 2.6 is implemented in Python and licensed under GPLv3. Source code, profiles and documentation are available at: https://motu-tool.org/.


Supplementary information
Supplementary information is available online.

## Introduction

Metagenomic sequencing has transformed the field of microbiology by enabling researchers to study the genomic composition of microbial communities in the environment (microbiomes) in a cultivation-independent manner. This advance has driven the development of computational methods to profile microbiome samples, i.e. to identify species and to quantify their relative abundance (Sczyrba et al., 2017). Such methods often rely on the availability of reference genomes (Wood and Salzberg, 2014; Shah et al., 2021), the generation of which usually requires successful cultivation. However, for many environments, the majority of microbial species is still uncultivated (Lloyd et al., 2018; Konstantinidis et al., 2015). As a result, a significant proportion of microbial communities, especially at high taxonomic resolution, may be missed during profiling. Adding to this limitation, microbial community composition is typically measured as the relative abundance of its members, and hence, missing taxa can cause biased estimation of the abundance of the others (Milanese et al., 2019).

To address these issues, we developed the taxonomic profiling tool, mOTUs, which leverages universal, protein coding, single-copy phylogenetic marker genes (MGs) that can not only be identified in reference genomes, but also retrieved from metagenomes (Milanese et al., 2019; Sunagawa et al., 2013). These MGs are clustered into species-level MG-based taxonomic units, referred to as ‘ref-mOTUs’ and ‘meta-mOTUs’ if they are represented by MGs from at least one reference genome or only from metagenomes, respectively. Recent algorithmic advances (e.g. Kang et al., 2019) have made it possible to reconstruct metagenome-assembled genomes (MAGs) in studies of diverse host-associated and environmental microbiomes (Stewart et al., 2019; Anantharaman et al., 2016; Delmont et al., 2018). As for reference genomes, MGs can be extracted from MAGs and be readily used to extend the database of the mOTUs tool (Milanese et al., 2019). This feature enables the mOTUs profiler to provide a more complete view of the microbial diversity across different environments and at the same time, to reduce bias in relative abundance estimation.

Here we present an updated version, mOTUs 2.6, with a database largely extended by de novo-generated MAGs, which, combined with the addition of publicly available draft genomes, cover the most intensely studied microbiomes to date. This greatly increases the scope of metagenomic profiling to environments that are of broad interest, but currently lack cultivation-based reference genome collections.

## Results & Discussion

To increase the phylogenetic coverage of the mOTUs database for microbial species without any genome-sequenced representative available, we generated 150,880 MAGs from 4,531 publicly available metagenomes originating from 23 environments (Supplementary Table 1). These MAGs were complemented with 454,773 draft genomes (~96% MAGs; ~4% isolate and single cell genomes) gathered from previous work (Supplementary Table 1). After extracting MGs from these draft genomes, we extended the previous database (2.5.1) using existing functionality described at https://motu-tool.org/. A total of 79,833 of these genomes were not represented by any mOTU (neither meta-mOTU nor ref-mOTU) in version 2.5.1 and were thus used to extend the database of MGs by 19,358 new mOTUs (‘ext-mOTUs’, Figure 1a). Among these, more than half (10,401) were assigned to unknown families (Supplementary Table 4) based on taxonomic annotations using the STAG classifier (v0.7, https://github.com/zellerlab/stag). MGs from assembled metagenomes, which were neither part of a MAG nor previously represented by a mOTU, were added to an unbinned group (shown as ‘unassigned’ in mOTUs abundance profiles). As a unique feature of mOTUs, quantifying the abundance of this group allows for estimating the relative abundance of unknown species, and thus improves the accuracy of relative taxonomic abundance estimates for all detected organisms (Milanese et al. 2019).

![Figure 1.](content/440600v1_fig1.tif)

**Figure 1.:** (a) The mOTUs 2.6 database was constructed based on version 2.5.1 of the database by adding phylogenetic marker genes from 605,653 MAGs (as well as a small fraction of isolate and single amplified genomes), of which 454,773 originated from external resources and 150,880 were reconstructed de novo from 4,531 metagenomes. This addition resulted in the generation of more than 19,358 new ext-mOTUs. Genomes already represented by ref- and meta-mOTUs were discarded (grey lines). (b) Breakdown of the relative abundance covered by the three types of mOTUs using the mOTUs 2.6 database. The numbers underneath the ring charts represent the total number of mOTUs that can be profiled per environment (left) considering only species with a prevalence of 0.1%, as well as the median number of mOTUs per sample that were detected after downsampling to 5,000 inserts (right).

The updated database, version 2.6, increases the number of mOTUs by a factor of 2.3 (from 14,212 to 33,570). Notably, the proportion of newly represented species varies widely across different environments (Figure 1b). For example, in the well-studied mouse gut microbiome, less than 25% of the 5,345 MAGs were found to correspond to ref-mOTUs. The remaining 75% of the MAGs resulted in 587 ext-mOTUs (Supplementary Figure 2). Even for the human microbiome, 2,750 ext-mOTUs were generated, although 97% of the ~400,000 newly added MAGs had already been represented by ref- or meta-mOTUs. This finding illustrates that while the vast majority of human-associated microbial species are repeatedly sampled, novel species are still being recovered, possibly by the inclusion of underrepresented populations, dietary habits and/or disease states (Pasolli et al., 2019; Wirbel et al., 2019). The remaining 16,021 ext-mOTUs cover a large range of other animal-associated (e.g., cattle, fish, chicken, pig, bee, dog, cat) and environmental (e.g., soil, freshwater, wastewater, ocean, air) microbiomes for which reference genomes are generally still scarce (Figure 1b). The total number of species represented in the mOTUs 2.6 database varies across different environments from hundreds to several thousands of which 5 to 40% (Figure 1b) are typically detected in a single profiled metagenome. To facilitate comparative research, we profiled a total of 11,164 metagenomes and metatranscriptomes from 23 environments using the mOTUs 2.6 database. These profiles are released alongside the updated mOTUs database as a basis for comparisons with newly generated ones.

## Conclusions

By including assembled metagenomes from previously underrepresented environments, the updated mOTUs tool (version 2.6) enables a greatly extended profiling of the microbial diversity on earth, a large fraction of which is missed if their detection and quantification relies exclusively on sequenced reference genomes.

## Supporting information
