# Accurate highly variable gene selection using RECODE in scRNA-seq data analysis

## Authors

- Yusuke Imoto<sup>1</sup> ([ORCID: 0000-0003-2574-4471](https://orcid.org/0000-0003-2574-4471)) †

### Affiliations

1. Institute for the Advanced Study of Human Biology, Kyoto University Kyoto Japan

† Corresponding author

## Abstract

Abstract
Accurate selection of highly variable genes (HVGs) is essential in single-cell RNA sequencing (scRNA-seq) data analysis, as it enables the identification of functionally important genes and the characterization of cell types and states. However, HVG selection is often confounded by technical noise inherent in the scRNA-seq measurement process, leading to the misidentification of biologically relevant genes. In this study, we propose a novel HVG selection method based on the RECODE-denoised variance. RECODE is a recently developed noise reduction algorithm that models technical noise in scRNA-seq data as a random sampling process and removes it through a theoretically grounded denoising procedure. Benchmarking on 10x Genomics PBMC data revealed that our method outperformed conventional approaches in capturing known marker genes. Moreover, it demonstrated robustness to changes in normalization parameters and downsampling of cell numbers. Importantly, the same denoised data used for HVG selection can be directly reused in downstream analysis, ensuring consistency throughout the scRNA-seq data analysis pipeline.

## Introduction

Recent advances in single-cell RNA sequencing (scRNA-seq) have enabled the analysis of transcriptomic profiles at the resolution of individual cells, greatly contributing to our understanding of developmental processes, cell type classification, and disease mechanisms [13]. In such analyses, the accurate selection of highly variable genes (HVGs), which reflect cell-to-cell heterogeneity, is essential to identify functional genes and decipher gene regulatory networks [19]. However, scRNA-seq data are known to contain a large amount of technical noise arising from processes such as library preparation and sequencing [1]. As a result, observed variability statistics often fail to accurately reflect true biological variability. When technical noise is not properly corrected, cell-type-specific genes and functional genes that drive cellular differentiation may be missed, and low-variability non-functional genes may be erroneously selected.

To address this issue, existing approaches have attempted to correct bias in variability statistics, such as observed variance or dispersion (variance-to-mean ratio), which tend to depend on mean expression levels.

For example, Satija et al. [11] proposed an HVG selection method using normalized dispersion, which is modified by a z-score transformation according to bins of average expression. As its newer version, Stuart et al. [12] introduced an HVG selection method using a normalized variance estimated by non-linear regression based on a negative binomial model [4]. While both methods show practical utility, they rely on empirical normalization of observed statistics and do not accurately account for the impact of noise. Consequently, their theoretical justifications remain limited. Moreover, the normalized variability statistics produced by conventional HVG selection methods are not directly applicable to downstream analyses such as clustering or pathway enrichment. As a result, these approaches fail to provide consistent and integrated analytical outcomes throughout the scRNA-seq data analysis pipeline.

To overcome this limitation, we previously developed RECODE (resolution of the curse of dimensionality), a method for reducing technical noise across entire single-cell transcriptome datasets based on highdimensional statistics [7]. RECODE mathematically models technical noise as random sampling noise, derived from the measurement process of single-cell omics data, and applies eigenvalue modification techniques theoretically derived in high-dimensional statistics [18] to remove the noise component. More recently, the incorporation of eigenvector modification [17] has further improved the accuracy of noise reduction [5]. The application of RECODE to single-cell omics data has been shown to improve a wide range of downstream analyses, including clustering, trajectory inference, and differential expression analysis, leading to enhanced detection of functional genes and rare cell types [2, 6, 3, 8, 9, 10, 16].

In this study, we propose a simple and theoretically grounded method to select HVGs using the variance after applying RECODE. Using the widely studied PBMC dataset, we demonstrate through comparative experiments with conventional methods (Seurat, Seurat v3) that our approach achieves superior accuracy and robustness in detecting known marker genes. Our method is readily applicable to standard scRNA-seq analysis pipelines and offers HVG selection that is less affected by technical noise.

## Results

### Technical noise floor curve disturbs HVG selections

To investigate the influence of technical noise on variability statistics, we first visualized the relationship between mean expression per gene and various measures of variability across different normalizations (Figure 1a). In scRNA-seq data, we expect that a substantial number of genes, such as housekeeping or cellcycle-related genes, are expressed consistently across most cell types and exhibit near-zero biological variance. Accordingly, variability measures should, in principle, contain many values close to zero and remain largely independent of mean expression.

![Figure 1.](content/661026v1_fig1.tif)

**Figure 1.:** Overview of technical-noise structure and HVG selections. a, Scatter plots of mean expression per gene (x-axis) versus variability measures (y-axis) under different normalization schemes. Left: dispersion after total-count normalization; center: variance after total-count normalization; right: variance after log-normalization. Each black dot represents a gene. The red dashed line denotes the technical noise floor (TNF) curve, representing the lower bound of variability statistics elevated by technical noise. b, Comparison of highly variable gene (HVG) selection by two conventional methods. The y-axis shows the variability measure used by each method: normalized dispersion (Seurat) and normalized variance (Seurat v3). c, HVG selection by RECODE v1 and RECODE v2. The y-axis shows the RECODE-denoised variance after noise correction and normalization. In b–c, genes highlighted in red are those selected as HVGs with a cutoff of n_top_genes = 2,000, and genes in black are others.

However, as shown by the red dashed lines in Figure 1a, the observed distributions of dispersion and variance after total-count normalization exhibit a strong lower bound that increases monotonically with mean expression. Even after log-normalization, the lower envelope of variance remains non-negligible, peaking around mean expression levels of 1–2 on the log scale. These lower bounds are not of biological origin but rather arise from technical noise intrinsic to the scRNA-seq measurement process.

We refer to this increasing baseline as the technical noise floor (TNF) curve. Genes whose expression variability lies near the TNF curve are likely dominated by noise rather than true biological differences, and as a result, HVG selection in these regions is particularly error-prone. Therefore, reducing or equalizing the TNF curve across the range of expression levels is essential for comparing variances on an equal footing and improving the precision of HVG selection.

### Existing and RECODE-based methods for HVG selection

We summarize two widely used methods for highly variable gene (HVG) selection and introduce our proposed approach based on RECODE-denoised variance. The Seurat method [11] classifies genes according to their mean expression and then z-score normalizes the dispersion (variance-to-mean ratio) within each bin. The resulting normalized dispersion values are used to select HVGs. Seurat has been widely adopted due to its scalability and ease of use, and its practical utility has been validated in benchmark studies such as Yip et al. [19]. Seurat version 3 (Seurat v3) [12] improves upon the earlier method by using normalized variances obtained through variance-stabilizing transformation, in which the mean-variance relationship is modeled based on a negative binomial distribution [4]. These methods serve as the default HVG selection procedures in the popular Python package scanpy [15] and the R package Seurat [12], and are thus adopted as baselines in our subsequent comparisons.

Our proposed method is based on RECODE version 2 (RECODE v2) [5], which denoises scRNA-seq data by reducing technical noise arising from the random sampling process. We then apply total-count normalization and log normalization, two standard preprocessing steps in scRNA-seq analysis, to the RECODE-denoised data. Total-count normalization, also known as library size normalization or total count scaling, scales gene expression so that the total count in each cell is fixed to a constant value, known as the target sum cTS. Log normalization applies a log(x + 1) transformation to each entry. While cTS = 104 is commonly used in scRNA-seq data analysis, the proposed method adopts cTS = 105. The rationale for this choice is empirically justified in later sections, and the full implementation details are described in the Methods.

All three methods aim to mitigate the influence of technical noise on variability statistics, effectively correcting the lower bound imposed by noise (Figure 1b). Notably, both Seurat v3 and RECODE v2 achieve a flattened TNF curve, meaning that the lower bound of the variability statistic becomes nearly constant with respect to the mean expression level. This may suggest improved comparability of gene variances and greater reliability in HVG selection, as the influence of technical noise no longer distorts comparisons of variability across genes. In the next section, we quantitatively evaluate the performance of these methods using numerical benchmarks.

All methods aim to mitigate the influence of technical noise on variability statistics, effectively correcting the lower bound (TNF curve) imposed by noise (Figure 1b, c). Seurat uses z-score normalization within gene expression bins, which leads to an irregular and fragmented lower bound of the normalized dispersion across the range of mean expression values. Seurat v3 achieves a nearly horizontal lower bound by performing nonlinear regression based on a negative binomial model. However, this correction tends to elevate the lower bound in low-expression regions, indicating incomplete noise removal in that range. As a reference, RECODE v1 attenuates the TNF curve but does not fully flatten it. In contrast, RECODE v2 achieves a nearly flat TNF curve with a lower bound approaching zero across all expression levels, suggesting that technical noise has been effectively removed and that variability statistics now primarily reflect biological differences. This flattening improves comparability of gene variances and reliability in HVG selection, as technical noise no longer distorts variability comparisons across genes. In the next section, we quantitatively evaluate the performance of these methods using numerical benchmarks.

### Quantitative comparison of HVG selection methods

To evaluate the accuracy of HVG selection, we benchmarked each method on the publicly available 10x Genomics 3k Peripheral Blood Mononuclear Cells (PBMCs) scRNA-seq dataset. For validation, we considered 17 canonical marker genes associated with distinct immune cell types. These include, for example, IL7R (CD4 T cells), CD8A and CD8B (CD8 T cells), and CD14 (CD14+ monocytes).

Table 1 shows the rank of each marker gene under different HVG selection methods. Figure 2a visualizes the distribution of these marker genes with respect to each method’s variability statistic. In addition to the comparing methods Seurat, Seurat v3, and RECODE v2, we sometimes include RECODE v1 for reference.

**Table 1:**
 Gene-wise rankings of highly variable genes across different methods.


![Figure 2.](content/661026v1_fig2.tif)

**Figure 2.:** The performance of HVG selection methods evaluated with marker genes. a, Scatter plots corresponding to Figure 1b, with known marker genes highlighted in red. b, Box-plot comparison of the ranks assigned to marker genes by four methods (Seurat, Seurat v3, RECODE v1, RECODE v2); lower values indicate better detection. c, Venn diagram showing the overlap among the 2,000 HVGs selected by Seurat, Seurat v3, and RECODE v2. Numbers in parentheses indicate the count of marker genes contained in each region.

The dataset contains a total of 32,738 genes. Although Seurat ranks many marker genes higher, a large number of them still fall outside the commonly used cutoff of 2,000 genes for HVG selection, indicating insufficient sensitivity. However, Seurat v3 improves substantially over Seurat, assigning higher ranks to nearly all marker genes. Remaerkebly, RECODE shows even greater improvements in both versions v1 and v2. As shown in Figure 2b, RECODE v2 achieves the highest accuracy in marker gene ranking. For example, under a typical HVG selection cutoff of n_top_genes = 2,000, REOCDE v2 can detect all the marker genes and only RECODE v2 is able to capture key marker genes such as IL7R, CD8A, CD8B, and CD14, while Seurat and Seurat v3 fail to detect them (Figure 2c).

Importantly, these improvements are particularly notable for genes with intermediate expression levels. As seen in Table 1, RECODE v2 shows large gains in ranking over Seurat v3 for genes with mean expression between 0.20 and 0.87. Empirically, this expression range is enriched for functional marker genes [1], suggesting that RECODE v2’s improvement is both quantitatively and biologically meaningful.

### Effect of total-count parameter on HVG selection

We next examined how the total-count normalization parameter, denoted cTS (target sum), affects HVG selection. This parameter sets the total count to which each cell’s expression values are scaled during totalcount normalization. Since this scaling directly influences the input to the subsequent log-transformation, it alters the effective dynamic range of expression values. For example, as shown in Figure 3a and Table 2, when cTS = 104, highly expressed genes such as LYZ tend to rank higher. However, as cTS increases, genes with moderate expression levels such as GNLY and NKG7 become more prominent in the ranking. This indicates that increasing cTS relatively amplifies variability in the low-to-moderate expression range, thereby shifting the focus of variability to different regions.

**Table 2:**
 Marker-gene ranks of proposed method (RECODE v2) at different target sum (TS) values for total-count normalization.


![Figure 3.](content/661026v1_fig3.tif)

**Figure 3.:** Influence of the total-count normalisation parameter cTS on variability profiles and marker-gene ranking. a, Scatter plots of gene-wise mean log-normalised expression (x-axis) versus RECODE-denoised variance (y-axis) for three values of cTS = 104, 105, 106. Grey points indicate all genes; red points denote those selected as HVGs at n_top_genes = 2,000. Labeled points are established marker genes. b, Box plots of marker-gene ranks produced by each method as a function of parameter cTS. Within Seurat and RECODE (v1, v2), three boxes correspond to cTS = 104, 105, 106 (labels beneath the x-axis). Seurat v3 is independent of parameter cTS and therefore appears as a single box.

Typical cells contain many low-expression genes that are highly susceptible to technical noise (dropout) in scRNA-seq data. Therefore, smaller values such as cTS = 104 are commonly used to suppress the amplification of noise. In contrast, bulk RNA-seq pipelines often adopt count per million (CPM) normalization, which corresponds to cTS = 106, as technical noise has a much smaller impact in such datasets. In our benchmark, we observed that increasing cTS degraded the HVG selection accuracy of Seurat, likely due to insufficient noise correction (Figure 3b).

In contrast, the median ranks of marker genes under both RECODE v1 and v2 remained stable or improved slightly with increasing cTS (Figure 3b and Table 2). Notably, the rankings of low-expression genes (e.g., PPBP, FCER1A, KLRB1; mean expression ≲ 0.1) improved at higher cTS, suggesting that RECODE successfully denoised low-count features and enabled their reliable detection.

These results demonstrate that our RECODE-based method allows users to tailor HVG selection to target specific expression ranges by tuning cTS. In this study, we adopted cTS = 105 as the default setting, as it offered a favorable tradeoff between high average marker gene rank and low rank variability (Figure 3b).

### Robustness of HVG selection under cell downsampling

Finally, we investigated the robustness of HVG selection against reduced cell numbers. Using the same PBMC dataset, we randomly downsampled the number of cells to n = 2,000, 1,000, 500, and 100 and performed HVG selection for each case. For each n, this process was repeated 10 times, and the average rank of each marker gene was computed across repetitions (Table 3, Figure 4).

**Table 3:**
 Average marker-gene ranks of proposed method (RECODE v2) under random downsampling of cell number (n = 2,000, 1000, 500, 100).
Each rank is averaged over 10 repetitions.


![Figure 4.](content/661026v1_fig4.tif)

**Figure 4.:** Robustness of HVG selection under cell downsampling. a, Scatter plots showing gene-wise mean log-normalized expression (x-axis) versus normalized dispersion (y-axis) after downsampling the number of cells to n = 2,000, 1,000, and 100. Red points indicate genes selected as HVGs (n_top_genes = 2,000); labeled black points represent known marker genes. b, Box plots of marker-gene ranks produced by each method (Seurat, Seurat v3, RECODE v2) under different levels of downsampling (n = 2,000, 1,000, 500, 100). Each box represents the distribution of average HVG ranks for 17 marker genes, calculated over 10 random subsampling replicates. Effect of cell downsampling on variability profiles and HVG selection. Seurat v3 failed at 500 and 100 cells owing to numerical errors; these cases are indicated as “NA”.

Because the raw scRNA-seq data are sparse, downsampling results in a reduction in the number of expressed genes per cell. As a consequence, we observed a general decrease in gene-wise variance following downsampling (Figure 4a). Despite this, both Seurat and RECODE v2 remained computationally stable across all downsampled sizes, though a mild degradation in marker-gene ranking was observed as the cell number decreased (Figure 4b). In particular, RECODE v2 maintained reliable performance for genes with moderate to high expression levels (mean expression ≥ 0.25), with average ranks remaining below the commonly used cutoff n_top_genes = 2,000 even for n = 100. By contrast, Seurat v3 failed to produce results at n = 500 and n = 100 due to numerical instability, indicating a lack of robustness under strong downsampling conditions.

Low-expression genes were more frequently excluded from the proposed HVG selection as the number of cells decreased due to downsampling. This is likely due to increased sparsity in the count matrix, fewer cells express these genes after downsampling, thereby degrading the accuracy of noise correction. These findings suggest that sufficient cell numbers are necessary to reliably detect low-expression HVGs. On the other hand, for identifying highly variable genes with moderate to high expression levels, our proposed method (RECODE v2) remains accurate even under extreme downsampling conditions.

## Discussion

In this study, we proposed a novel method for selecting highly variable genes (HVGs) based on the variance after denoising by RECODE (RECODE-denoised variance) and evaluated its effectiveness through comparison with existing methods. RECODE mathematically models the technical noise inherent in scRNA-seq data as random sampling noise and removes it based on high-dimensional statistics theory [7]. Our method applies total-count normalization and log normalization to RECODE-denoised data, and uses the resulting variance as the HVG selection criterion.

We first examined how technical noise affects statistical measures of variability in scRNA-seq data. We observed that dispersion and variance showed a lower bound dependent on mean expression, which we termed the technical noise floor (TNF) curve (Figure 1). This TNF structure distorts HVG selection. In contrast, RECODE normalization flattens the TNF curve, demonstrating its ability to eliminate the expression-level dependency in variability metrics.

We assessed HVG selection performance using the 3k PBMC scRNA-seq dataset provided by 10x Genomics and evaluated the ranking of 17 known marker genes. Our results demonstrated that the proposed method ranked more marker genes in the top ranks compared with Seurat and Seurat v3 (Figure 2, Table 1). In particular, several marker genes for major cell types, such as CD4 T cells, CD8 T cells, and CD14+ monocytes, were selected within the top 2,000 genes only by RECODE v2. This indicates that RECODE successfully removes technical noise, enabling biologically important low-to mid-expression genes to be properly detected as HVGs.

We then investigated the sensitivity to the parameter cTS used in total-count normalization. While the selection performance of conventional methods varied considerably depending on cTS, RECODE consistently showed stable accuracy across different settings (Figure 3, Table 2). In particular, we adopted cTS = 105 in this study, as it provided high accuracy and low variability in marker gene detection. Moreover, increasing cTS led to an improvement in the ranking of low-expression genes, suggesting that RECODE allows flexible HVG selection according to the expression level of interest.

We also evaluated the robustness of each method under cell downsampling. RECODE v2 remained stable even with as few as 100 cells (Figure 4, Table 3). In contrast, Seurat v3 frequently failed when the number of cells was reduced to 500 or fewer, indicating limited robustness under low-sample conditions. For RECODE v2, mid-to high-expression genes (mean expression ≥ 0.25) retained rankings within the top 2,000 even under severe downsampling, demonstrating the method’s resilience. Although the detection of low-expression HVGs requires a sufficient number of cells, RECODE remains accurate for moderate-to-high expression HVGs even when the number of cells is extremely small.

These findings highlight the versatility of RECODE-based HVG selection. For example, adjusting the target sum cTS enables the user to focus on different expression ranges of interest. In addition, the robustness to cell number is advantageous not only in low-quality datasets but also when isolating specific rare cell types for targeted analysis.

Most importantly, because RECODE reduces the noise in the scRNA-seq data itself, the same denoised data used for computing RECODE-denoised variance can be directly reused for downstream analysis. This ensures methodological consistency between HVG selection and downstream analysis, providing a key advantage over conventional approaches that often apply distinct models to each step.

Although we did not evaluate multi-batch datasets in this study, an extended version of RECODE, called iRECODE [5], has been developed to simultaneously reduce technical and batch noises. This suggests potential for accurate HVG selection in multi-batch integration scenarios as well.

In summary, we have shown that RECODE-based HVG selection is theoretically robust to technical noise and achieves higher accuracy and stability than standard methods. This approach provides a practical and flexible tool for cell-type identification and functional gene discovery in scRNA-seq analysis. Future work will focus on evaluating its generalizability to a wider variety of datasets and integration with other preprocessing pipelines.

## Methods

### Overview of RECODE

We provide an overview of the resolution of the curse of dimensionality (RECODE) algorithm. For details, refer to the Supplementary File of Imoto–Nakamura et al. [7] and the Methods section of Imoto [5].

Let  denote the raw count matrix of scRNA-seq data, where xij represents the observed RNA (UMI) count for gene i in cell j. Here, d and n indicate the number of genes and cells, respectively. Cells with zero total count (∑i xij = 0) and genes with zero total count (∑j xij = 0) are excluded from the analysis. RECODE begins by applying a noise variance–stabilizing normalization (NVSN), defined as:



where tj = ∑i xij is the total count for cell j. This normalization equalizes the variance of random sampling noise, which originates from the scRNA-seq measurement process and is mathematically modeled as technical noise. This step is also essential to ensure compatibility with the subsequent eigenvalue and eigenvector correction procedures developed in the field of high-dimensional statistics.

Next, the covariance matrix of the normalized matrix F (X) = (F (xij)) ∈ ℝd×n is computed as S = F (X)F (X)T/(n − 1), where T denotes matrix transpose. The eigenvalue equation Sui = λiui (∥ui∥ = 1) is then solved for i = 1, …, d. Yata and Aoshima proposed a modification of eigenvalues [18] defined by:



where ℓ ≤ min {n − 1, d} is a parameter representing the essential dimensionality. This modification improves the convergence of empirical eigenvalues to their population counterparts, indicating mitigation of the curse of dimensionality caused by noise accumulation. In the RECODE algorithm, the optimal value of the essential dimensionality ℓ is automatically determined as



RECODE version 1 (RECODE v1) modifies the raw count matrix X such that the eigenvalues λi match the modified eigenvalues :



where , and.

Recently, Yata and Aoshima also proposed a correction method for eigenvectors [17]:



where σ : {1, …, d}→ {1, …, d} is a permutation such that |uiσ(1) ≥ … ≥ | uiσ(d) |, and ki is the integer uniquely determined by the following condition:



This eigenvector correction also alleviates the curse of dimensionality [17]. RECODE version 2 (RECODE v2) incorporates both the modified eigenvalues and eigenvectors:



where .

### RECODE-based HVG selection

Let  denote the scRNA-seq data denoised by RE-

CODE. We apply two standard preprocessing steps, total-count normalization and log normalization, to the RECODE-denoised data . Given a non-negative matrix , the total-count normalization f TN is defined as follows:



where cTS is a scaling parameter known as the target sum or size factor. The log normalization f LN is defined as:



In RECODE-based HVG selection, we first apply total-count normalization followed by log normalization, resulting in the matrix . We then compute the variance for each gene across cells and select the top n_top_genes genes with the highest variances as highly variable genes.

### Implementation

RECODE-based HVG selection is implemented in the screcode Python package (version 2.1 or later). Given an AnnData object [14] representing scRNA-seq data, users can perform HVG selection using the following procedure:

![Figure](content/661026v1_ufig1.tif)

By default, the top 2,000 genes with the highest variance are selected as HVGs. These genes are stored in adata.var.RECODE highly variable, and the RECODE-normalized variances used for ranking are stored in adata.var.RECODE normalized variance.

In addition, the RECODE-denoised data after applying total-count and log normalizations is stored in adata.layers[“RECODE log”]. Users can use the following commands to set this as the default data matrix and subset it to HVGs:

![Figure](content/661026v1_ufig2.tif)

This procedure allows seamless reuse of RECODE-denoised data in downstream analyses using Scanpy or other libraries.

For R users, RECODE can be used by calling Python from within R using reticulate. For detailed instructions and tutorials, please refer to the GitHub repository at https://github.com/yusuke-imoto-lab/ RECODE and the tutorial page at https://yusuke-imoto-lab.github.io/RECODE/Tutorials/index.html.

### HVG selection analysis

The peripheral blood mononuclear cell (PBMC) dataset and marker genes used in this study are consistent with those introduced in the Scanpy tutorial “Preprocessing and clustering 3k PBMCs.” Specifically, the following 17 marker genes were used: IL7R (CD4 T cells), CD8A and CD8B (CD8 T cells), CD14, LYZ, LGALS3, and S100A8 (CD14+ monocytes), MS4A1 and CD79A (B cells), GNLY, NKG7, and KLRB1 (natural killer cells), FCGR3A and MS4A7 (FCGR3A+ monocytes), FCER1A and CST3 (dendritic cells), and PPBP (megakaryocytes).

For comparative evaluation, we applied the widely used methods Seurat and Seurat v3. Both were implemented using the function scanpy.pp.highly variable genes in Python. For Seurat, total-count normalization followed by log normalization was applied before HVG selection. Except in the section “Effect of total-count parameter on HVG selection,” the total-count normalization parameter cTS was set to 104. Although Seurat provides an option to filter genes based on mean expression, we disabled this filter to enable direct comparison of the variability statistics between methods.

Seurat v3 was applied directly to the raw count matrix, as required by its negative binomial-based modeling framework. The average expression values shown in Tables 1–3 represent gene-wise means computed after applying total-count normalization with cTS = 104 and log normalization to the raw count matrix.
