# AsaruSim: a single-cell and spatial RNA-Seq Nanopore long-reads simulation workflow

## Authors

- Ali Hamraoui<sup>1</sup> ([ORCID: 0009-0008-7001-4252](https://orcid.org/0009-0008-7001-4252))
- Laurent Jourdren<sup>1</sup> ([ORCID: 0000-0003-4253-1048](https://orcid.org/0000-0003-4253-1048))
- Morgane Thomas-Chollier<sup>1</sup> ([ORCID: 0000-0003-2608-476X](https://orcid.org/0000-0003-2608-476X)) †

### Affiliations

1. GenomiqueENS, Institut de Biologie de l’ENS (IBENS), Département de biologie, École normale supérieure, CNRS, INSERM, Université PSL 75005 Paris France
2. Group Bacterial infection, response & dynamics, Institut de biologie de l’ENS (IBENS), École normale supérieure, CNRS, INSERM, Université PSL 75005 Paris France

† Corresponding author

## Abstract

Abstract

Motivation
The combination of long-read sequencing technologies like Oxford Nanopore with single-cell RNA sequencing (scRNAseq) assays enables the detailed exploration of transcriptomic complexity, including isoform detection and quantification, by capturing full-length cDNAs. However, challenges remain, including the lack of advanced simulation tools that can effectively mimic the unique complexities of scRNAseq long-read datasets. Such tools are essential for the evaluation and optimization of isoform detection methods dedicated to single-cell long read studies.


Results
We developed AsaruSim, a workflow that simulates synthetic single-cell long-read Nanopore datasets, closely mimicking real experimental data. AsaruSim employs a multi-step process that includes the creation of a synthetic UMI count matrix, generation of perfect reads, optional PCR amplification, introduction of sequencing errors, and comprehensive quality control reporting. Applied to a dataset of human peripheral blood mononuclear cells (PBMCs), AsaruSim accurately reproduced experimental read characteristics.


Availability and implementation
The source code and full documentation are available at: https://github.com/GenomiqueENS/AsaruSim.


Data availability
The 1,090 Human PBMCs count matrix and cell type annotation files are accessible on zenodo under DOI: 10.5281/zenodo.12731408.

## Introduction

Single-cell RNA sequencing technologies (scRNAseq) have revolutionized our understanding of cell biology, providing high-resolution insights on Eukaryote cellular heterogeneity. Still, studying the heterogeneity at the level of isoforms and structural variations is currently limited. Traditional short-read sequencing coupled with single-cell technologies (commonly droplet-based scRNA-seq protocols such as 10X Genomics) are not suitable for studying full-length cDNAs, because they require RNA/cDNA fragmentation, often resulting in the loss of information regarding the complete exonic structure (Arzalluz-Luque et Conesa 2018). Combining long-read sequencing, such as Oxford Nanopore or Pacbio, with single-cell technologies has enabled addressing this challenge (Arzalluz-Luque et Conesa 2018). Despite its advantages, the quality of Nanopore sequencing used to be impacted by higher error rates compared to short-read technologies, thus negatively impacting the detection of cell barcodes (CBs) and unique molecular identifiers (UMIs) (Karst et al. 2021). Yet, these elements are critical for attributing reads to their original cells, and for the accurate characterization and quantification of isoforms. That is why a hybrid approach, coupling long-read and short-read technologies, used to be necessary for a reliable assignment of CBs and UMIs (Lebrigand et al. 2020). Recently, the accuracy of Nanopore reads has been drastically improved (95-99% with the R10.3 flow cells (Dippenaar et al. 2021)), paving the way to untie long-read from short-read approaches in single-cell studies. Recently-released bioinformatics methods, including scNapBar (Wang et al. 2021), FLAMES (Tian et al. 2021), BLAZE (You et al. 2023), Sicelore 2.1 (Lebrigand et al. 2020), Sockeye (nanoporetech, 2023) and scNanoGPS (Shiau et al. 2023), have been developed to detect CBs and/or UMIs without using companion short-read data (referred to as Nanopore-only methods). These advances have the potential to reduce both the cost and the amount of work traditionally associated with hybrid sequencing computational workflows.

In the context of these developments, evaluating Nanopore-only methods for processing single-cell long-read datasets remains challenging. Most of the methods currently available are benchmarked against short-read datasets; this approach is not devoid of biases and is therefore considered to be an imperfect gold standard (Ziegenhain et al. 2022; Sun et al. 2024). One solution lies in the use of simulated datasets, which can mimic real experimental outcomes without the same biases as empirical methods. Simulated data provide a known ground truth—true cell barcodes (CBs), true unique molecular identifiers (UMIs). This ground truth can be exploited by method developers in various ways, such as tuning method parameters, validating results, benchmarking novel tools against existing methods, and highlighting their performance across a wide range of scenarios. Besides, the focus of most long read scRNA-seq and spatial methods is to identify alternative splicing events and differentially expressed isoforms (DEI) between cell types or cell states (Joglekar et al. 2023). Assessing the performance of these methods is also challenging because the ground truth is typically not known, and simulating random reads without any biological insight does not address this issue. One solution to this issue is to use instead simulated datasets, in which the ground truth (e.g., DEI, Fold change, batch effect) is known.

To date, no existing workflow has been designed with the specific purpose of simulating single cell or spatial RNAseq long-read data, especially with biological insights. Current scRNAseq counts simulation tools (such as SPARSim (Baruzzo, Patuzzi, et Di Camillo 2020) or ZINB-WaVE (Risso et al. 2018)) generate only a synthetic single cell count matrix. The bottleneck lies in the generation of simulated raw reads. It is notable that some studies on single-cell long-read methods, such as those described in Wang et al. 2021 and You et al. 2023, have employed simulated data. As part of these studies, individual tools (e.g., SLSim; https://github.com/youyupei/SLSim) have been developed to generate artificial template sequences with random cDNA, and simulators such as Badread (Wick 2019) or NanoSim (Yang et al. 2017) are employed to introduce sequencing errors based on a predefined error model. While such tools can effectively be used to benchmark the accuracy of CB assignment algorithms, it does not account for the complexities of estimating a realistic complete single-cell long-read dataset. Such complexities include PCR biases and artifacts, sparsity, variability, and heterogeneity—characteristics intrinsic to single-cell and spatial data. Comprehensive simulation would allow for broader and more precise benchmarking of the performance of single-cell long-read bioinformatics tools.

To address this gap, we have developed AsaruSim, a workflow that simulates single-cell long-read Nanopore data. This workflow aims to generate a gold standard dataset for the objective assessment and optimization of single-cell long-read methods. The development of such a simulator alleviates the bottleneck in generating diverse in silico datasets by leveraging parameters derived from real-world datasets. This capability enables the assessment of method performance across different scenarios and refines pre-processing and analysis methods for handling the unique complexities of long-read data at the single-cell level.

## Methods

AsaruSim mimics real data by first generating realistic UMI counts using SPARSSim (Baruzzo, Patuzzi, et Di Camillo 2020), and then simulating realistic Nanopore reads using Badread (Wick 2019). Five major steps are implemented (Figure 1).

![Figure 1.](content/613625v1_fig1.tif)

**Figure 1.:** It takes as input a real UMI count matrix and (1) trains the count simulator SPARSim to generate the corresponding synthetic UMI count matrix, serving as ground truth. It then (2) generates perfect reads (FASTA file) based on this synthetic UMI count matrix and a reference transcriptome. (3) It can optionally simulate bias introduced by PCR cycles. (4) It generates more realistic synthetic reads from the previous read templates (perfect or post-PCR) using Badread simulator with a pre-trained error model on real Nanopore reads. (5) It outputs an HTML report presenting quality control plots that enable the user to assess the simulated reads, before using them to evaluate tools dedicated to analyse scRNAseq long-read data.

### Synthetic UMI count matrix

AsaruSim takes as input a feature-by-cell (gene/cell or isoform/cell) UMI count matrix (.CSV), which may be derived from an existing single-cell shortor long-read preprocessed run, or from a count simulator tool. The R SPARSim library (Baruzzo, Patuzzi, and Di Camillo 2020) is used to estimate the count simulation parameters from the provided UMI count matrix and generate the corresponding synthetic count matrices, taking advantage of its ability to support various input parameters. AsaruSim also enables the user to input their own count simulation parameters, or alternatively, to select them from a predefined set of parameters stored in the SPARSim database.

### Perfect raw reads generation

This step is an original Python script. AsaruSim generates synthetic reads based on the synthetic count matrix. The retro-engineering of reads is achieved by generating a corresponding number of random UMI sequences for each feature (gene or isoform). The final construction corresponds to a 10X Genomics coupled with Nanopore sequencing library (Lebrigand et al. 2020): an adaptor sequence composed of 10X and Nanopore adaptors, a cellular barcode (CB), UMI sequences at the same frequencies as in the synthetic count matrix, a 20-bp oligo(dT), the feature-corresponding cDNA sequence from the reference transcriptome, and a template switch oligo (TSO) at the end. When a gene expression matrix is provided, a realistic read length distribution is achieved by selecting a random transcript of the corresponding gene, with a prior probability in favor of short length cDNA (Supplementary Note a). At the end, generated reads are randomly oriented, with each synthetic read having an equal probability of being oriented in the original strand or the reverse strand. These final sequences are named “perfect reads’’ as they exactly correspond to the introduced elements (CB, UMI, cDNA…) without addition of sequencing errors.

### Mimicking PCR amplification bias (optional)

The perfect reads are duplicated through artificial multiple PCR cycles by an original Python script reimplemented from Sarkar, Srivastava, and Patro 2019; Orabi et al. 2019 with several optimizations to improve speed and memory usage. This enables us to take into account the bias of amplification introduced during library constructions Bolisetty, Rajadinakaran, and Graveley 2015. At each cycle, a synthetic read has a certain probability to be successfully replicated. The efficiency rate of duplication is fixed by the user (default pdup= 0.9). Then, each nucleotide in the duplicated read has a probability to be mutated during the process. The error rate is also fixed by the user (default perror= 3.5e-05). From this resulting artificial PCR product, a random subset of reads is finally selected to mimic the experimental protocol where only a subset of the sample is used for the sequencing step.

### Introduction of sequencing errors in the reads

The perfect reads or post-PCR reads are used as template for Badread error simulation, which simulates Nanopore sequencing errors and assigns per-base quality scores based on pre-trained error models and sequence identity with the reference genome. AsaruSim allows the user to a) provide a personal pre-trained model, or b) providea real FASTQ read file to internally train a new model, or c) choose a pre-trained model within the Badread database. To approximate the observed sequence identity distribution in the experimental data, we align the real FASTQ read to the reference genome using Minimap2 (Li 2018), then calculate a gap-excluded identity for each alignment from the Minimap2 output: g = ma/(ma + mi), where ma is number matches and mi is number mismatches). A beta distribution is then fitted to the identity value to estimate the distribution parameters (Supplementary Note b).

### Report

Finally, AsaruSim generates an HTML report presenting quality control plots obtained by analyzing the final FASTQ read files with ToulligQC (GenomiqueENS, 2017). This report aims to make sure the simulated data correspond to the expectations of the user before using them with tools dedicated to analyse scRNAseq long-read data.

AsaruSim is implemented in Nextflow (Di Tommaso et al. 2017) under GPL 3 license to allow a flexible and easily customizable workflow execution, computational reproducibility, and traceability (Supplementary Note c). To ensure numerical stability and easier installation, it also uses Docker (Merkel 2014) containerization technology.

## Results

We developed AsaruSim to produce artificial Nanopore scRNAseq data that resembles a real experiment in terms of biological insights.

As a use case, we used a public dataset of human peripheral blood mononuclear cells (PBMCs) (10X, 2022) as reference data. We downloaded the count matrix and used it as input to AsaruSim. From the 5,000 cells initially present in the original matrix, we selected 3 cell types (CD8+T, CD4+T and B cells) resulting in 1,090 cells then used as a template to simulate the synthetic UMI count matrix (step1). Next, we simulated 30 million perfect reads (FASTA) (step2) with 2 PCR cycles (step 3). We downloaded a subset of one million original FASTQ raw reads to generate the error model for Badread, and then introduced errors to generate the synthetic reads (FASTQ) (step4). The quality control report is finally generated (step5, Supplementary Note d).

We compared the properties of the simulated data to the experimental data. Both datasets showed similar a) read-length distribution and transcript coverage, b) number of mismatches in reads aligned to the 10X adapter sequence using VSEARCH (T et al. 2016), and c) error patterns in reads aligned to human genome hg38 using Minimap2 (Li 2018) (Supplementary Note d).

Next, we pre-processed the simulated raw reads using the Sockeye pipeline (nanoporetech, 2023), and both experimental and simulated matrices were processed using Seurat v5 (Hao et al. 2024). The correlation of the average log fold change for cell types markers between real and simulated data shows a pearson’s correlation coefficient r=0.86 and the integration of both datasets shows a miLISI=1.58, demonstrating a good agreement in gene expression between the real and simulated datasets (Supplementary Note d).

## Conclusion

We presented a comprehensive workflow for simulating single-cell Nanopore data from the matrix to the sequence level, to create custom gold standard datasets. Potential applications include generating reads with differential gene expression (DEG) or differential expression of isoforms (DEI) between cell groups, as well as simulating known fold changes or batch effects, to assess and optimize single-cell long-read methods. AsaruSim offers a variety of configuration options to allow for flexible input and design.

Currently, AsaruSim generates data compatible with the 10X Genomics 3’ protocol. We plan to expand AsaruSim to accommodate additional single-cell techniques and protocols, and support for PacBio sequencing.
