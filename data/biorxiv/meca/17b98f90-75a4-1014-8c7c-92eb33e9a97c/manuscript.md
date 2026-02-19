# Sample-level modeling of single-cell data at scale with tinydenseR

## Authors

- Pedro Milanez-Almeida<sup>1</sup> ([ORCID: 0000-0001-8285-957X](https://orcid.org/0000-0001-8285-957X)) †
- Daniela Schildknecht<sup>2</sup>
- Markus Linder<sup>2</sup>
- Saskia M. Brachmann<sup>2</sup>
- Andreas Weiss<sup>2</sup>
- Flavia Adler<sup>2</sup>
- Sofia Cardoni Lenticchia<sup>2</sup>
- Morgane Meistertzheim<sup>2</sup>
- Sophia Wild<sup>2</sup>
- Rachel Cuttat<sup>2</sup>
- Pushpa Jayaraman<sup>1</sup>
- Lang Ho Lee<sup>1</sup>
- Tanya Mulvey<sup>1</sup>
- Nadia Hassounah<sup>1</sup>
- Gina Crafts<sup>1</sup>
- David S. Quinn<sup>1</sup>
- Elena J. Orlando<sup>1</sup>

### Affiliations

1. Novartis Biomedical Research Cambridge, MA 02139 USA
2. Novartis Biomedical Research 4056 Basel Switzerland

† Corresponding author

## Abstract

AbstractSingle-cell studies now routinely encompass hundreds of samples and millions of cells, offering unprecedented opportunities to link sample-level phenotypes with cellular and molecular states. However, current workflows often depend on cell-level inference and rigid clustering, which can distort significance and obscure subtle, continuous variation, in particular for complex experimental designs. Here, we present tinydenseR, a clustering-independent framework that enables robust, scalable, and statistically sensitive detection of differential cell states, outperforming existing workflows in speed, memory usage, and biological resolution. Technology-agnostic at its core, tinydenseR works seamlessly on scRNA-seq, flow, mass and spectral cytometry. Across synthetic benchmarks, a preclinical xenograft model, two immuno-oncology trials and a multi-study atlas, tinydenseR uncovers disease and treatment history-associated effects, including subtle within-cluster heterogeneity. Designed to accelerate discovery in clinical, preclinical, and translational research, the open-source package is available at GitHub.com/Novartis/tinydenseR.

## Introduction

The growing volume of single-cell data offers unprecedented opportunities to link sample-level phenotypes with cellular and molecular states. Studies now routinely profile hundreds of samples and millions of cells, enabling deeper insights into disease mechanisms and treatment responses [1–5]. However, this scale introduces significant computational challenges. Traditional workflows and data structures often fail to scale efficiently, creating bottlenecks in memory usage, processing time, and reproducibility when datasets reach atlas size [6–8].

Most current analysis strategies rely on clustering and cell-level inference as foundational steps for differential abundance and expression testing [9–11]. While clustering provides a convenient way to structure cellular diversity, it imposes rigid boundaries on inherently continuous biological processes. This simplification, combined with cell-level inference, can obscure subtle state changes and distort statistical significance, particularly within heterogeneous populations or complex experimental designs [12, 13]. Despite these drawbacks, clustering remains deeply embedded in single-cell workflows [14–17].

To improve efficiency and depth of analysis, many workflows employ landmark-based strategies, selecting representative cells to summarize large datasets [17–22]. Landmark approaches reduce computational burden but often remain tied to clustering or technology-specific assumptions, which can restrict flexibility and interpretability. More continuous methods, such as graph-based or embedding-driven analyses, aim to preserve biological resolution without rigid groupings. However, these approaches frequently depend on low-dimensional embeddings, which introduce uncertainty, or cannot generalize across technologies [19, 23–25].

In contrast, tinydenseR introduces a probabilistic, technology-agnostic framework for sample-level modeling that avoids rigid clustering while preserving biological resolution (schematics in Fig. 1). By leveraging efficient data structures, tinydenseR scales to atlas-sized datasets and enables robust detection of differential abundance and expression across diverse technologies. We demonstrate its utility across synthetic benchmarks, a preclinical xenograft model, two immuno-oncology trials, and a multi-study atlas, uncovering treatment-associated effects, including subtle within-cluster heterogeneity, while outperforming popular current workflows.

![Figure 1](content/690752v1_fig1.tif)

**Figure 1:** Method schematics showing synthetic scRNA-seq dataset simulating differential trajectory patterns across two conditions (A and B), each with 3 samples, 500 cells, and 500 genes. Ground truth distribution along PC1/PC2. Please refer to Material and Methods for details on landmark selection, probability derivations and modeling strategies.

## Results

### Detection of Differential Cell States in Synthetic Benchmarks

To start evaluating the statistical behavior and robustness of tinydenseR, we applied it to three synthetic datasets designed to simulate key single-cell analysis tasks across different technologies. The first dataset, distributed with the miloR package, simulated differential continuous trajectory patterns in single-cell RNA sequencing (scRNA-seq) data across two conditions, including batch effects (3 samples per condition; 500 cells and 500 genes total). tinydenseR correctly recovered trajectory-associated abundance and expression changes, demonstrating its ability to model continuous variation in cell states (Fig. 1 and Fig. S1).

The second and third datasets mimicked flow cytometry experiments: one focused on differential abundance (DA) and the other on differential expression (DE), each comprising 12 samples, 50,000 cells per sample, and 5 markers, all affected by batch effects. Scripts to reproduce these datasets are available on tinydenseR’s GitHub repository (please see Code Availability). The DA dataset simulated a two-fold depletion of a large (50%), small (5%), or very small (0.5%) cell population. tinydenseR accurately detected all three shifts in population frequencies, with strong agreement between estimated and ground truth values (Fig. S2).

The DE dataset simulated activation-dependent upregulation of a marker in a small cell population (5% of total), with decreasing effect sizes (log-mean expression change from 0 to 2, 1, or 0.5; log-SD = 1.5). tinydenseR successfully identified all three expression shifts (Fig. S3), including subtle within-cluster changes. Of note, except for the largest expression change, cluster percentages remained largely unaltered between Activation and Baseline, whereas tinydenseR was able to detect cell state changes within the affected subpopulation across all three conditions.

Analysis of the cytometry datasets with diffcyt also detected the expected differences associated with depletion and activation in both simulations (Fig. S4). However, tinydenseR was able to identify which marker was differentially expressed with activation in an unsupervised manner, whereas diffcyt requires, by design, manual distinction of lineage and functional markers for clustering and differential expression analysis, respectively. This reliance on prior knowledge can restrict the discovery of unexpected treatment effects. Across all three synthetic datasets, tinydenseR maintained high sensitivity and low estimated false discovery rate (Fig. S5), validating its capacity to handle diverse single-cell analysis tasks while also enabling unsupervised and unexpected discoveries.

### Application to Preclinical and Clinical Real-World Datasets

Next, we investigated treatment-induced transcriptional changes in a preclinical setting with tinydenseR. For this, we analyzed a xenograft model dataset generated by scRNA-seq. KRAS(G12D) mutant SW1990 pancreatic cancer cells, either wild-type (WT) for HRAS and NRAS (H/NRAS) or engineered with a H/NRAS double knockout (KO), were implanted into mice that were subsequently treated for seven days with either a vehicle or the KRAS(G12D) inhibitor MRTX1133 (Fig. S6a; see Methods for experimental details). This design enabled comparison of treatment effects in both genetic backgrounds.

tinydenseR revealed distinct shifts in the abundance of transcriptionally defined cell states, with notable differences between WT and H/NRAS KO tumors. For example, KO cells from mice treated with KRAS(G12D) inhibitor or vehicle separated into two distinct clusters (clusters 5 and 6), indicating a strong treatment effect on KO cells (Fig. S6b-f). In contrast, WT cells from mice treated with KRAS(G12D) inhibitor or vehicle were distributed across two clusters (clusters 1 and 2) that contained a mixture of cells from both conditions, suggesting a more heterogeneous or attenuated response on WT cells (Fig. S6b-f). Quantitative analysis of gene signature scores revealed more consistent treatment-induced downregulation of cell cycle, mTORC1, and PI3K signaling pathways, as well as KRAS signaling modulation, in KO and cluster 2 WT cells compared to cluster 1 WT cells (Fig. S6g). These results highlight the utility of tinydenseR in dissecting complex treatment responses in preclinical models by resolving both compositional and functional heterogeneity.

We then applied tinydenseR to a single-cell dataset from a phase 1 immuno-oncology clinical trial evaluating NIZ985, a recombinant heterodimer of IL-15 and IL-15 receptor α, in combination with PDR001, an anti-PD-1 monoclonal antibody, in adults with metastatic cancers. The dataset included longitudinal 12-marker flow cytometry profiles from peripheral blood mononuclear cells (PBMC) from nine patients, with samples collected at baseline (Cycle 1 Day 1, C1D1) and at multiple post-treatment timepoints (C1D3, C1D4, C1D8, C1D15 and C1D17; Fig. S7a). tinydenseR identified treatment-associated shifts in the abundance and activation states of CD8 T cell subsets, including most prominently a transient expansion of Ki67⁺HLADR⁺ proliferating cells peaking at C1D4 (Fig. S7b-e). Within this subset, the method further resolved a Ki67⁺HLADR⁺CD45RA⁺ subpopulation that increased in abundance in response to treatment more strongly than its CD45RA⁻ counterpart (Fig. S7f–g). These results highlight tinydenseR’s ability to support analysis across multiple levels of resolution, from broad lineage-level classifications (e.g., CD3⁺ T cells) to fine-grained activation states within subsets.

To further evaluate tinydenseR in a clinical trial context, we analyzed scRNA-seq data from a phase 1 trial of PHE885, a rapidly manufactured BCMA-targeting CAR T cell therapy, in 25 patients with newly diagnosed multiple myeloma (NDMM) and 42 patients with relapsed or refractory multiple myeloma (RRMM). The dataset included 321 samples and 1.76 million cells post-quality control (median 4,725 cells/sample) from leukapheresis, final product, and longitudinal PBMC and bone marrow mononuclear cells (BMMC; day 28, month 3, month 6; Fig. S8).

tinydenseR enabled multi-level modeling of abundance shifts across timepoints and compartments, revealing changes associated with treatment and disease history in cellular composition and transcriptional states. For example, the method captured enrichment of T cells with proliferative potential from leukapheresis to final product (Fig. S9), a shift that reflects the manufacturing process and is consistent with enhanced therapeutic potency [26]. tinydenseR also identified increased memory CD8 T cell and monocyte subpopulations at baseline in PBMC from RRMM patients compared to NDMM (Fig. S10), supporting disease and treatment-related immune remodeling [27].

Furthermore, CAR T cell expansion and plasma cell depletion were detected peaking at day 28 in the bone marrow (Fig. 2), both of which are indicative of treatment response. Of note, BMMC cluster 18 was significantly more abundant at screening compared to day 28 (Fig. 2c and e). That is counter-intuitive given that cells in cluster 18 expressed the CAR construct (Fig. 2d) and abundance of CAR T cells in patients before treatment is zero. tinydenseR helped resolve this apparent contradiction by revealing intra-cluster heterogeneity, showing that CAR T cells were in fact more abundant post-infusion compared to screening (Fig. 2g-h). Together, these findings illustrate the utility of tinydenseR in uncovering subtle, clinically relevant cell states by modeling sample-level variation in complex, heterogeneous datasets in a clustering independent manner.

![Figure 2](content/690752v1_fig2.tif)

**Figure 2:** (a-b) Landmark UMAP projection of bone marrow mononuclear cells (BMMC) colored by (a) cluster identity or (b) log2 fold change (log2FC) in cluster abundance at day 28 versus screening; red indicates increased abundance at day 28, blue indicates decreased.(c) Bar plots showing the percentage of cells in each BMMC cluster across individual samples.(d) Box plots showing the frequency of CAR-positive cells per cluster in each BMMC sample.(e) Violin plots of log2 fold change (log2FC) in cluster abundance at indicated time points versus screening while controlling for subject ID.(f) Heatmap showing reference-based cell type mapping across clusters.(g–h) Scatter plot showing the log2FC in abundance of cells in cluster 18 at day 28 versus screening (g) and all landmarks at day 28, month 3 and month 6 (h) compared to CAR construct transcript levels, highlighting that CAR-positive cells are not more abundant at baseline.

### Computational Performance and Biological Resolution

Finally, we directly compared the computational performance of tinydenseR in comparison with two widely used workflows, Seurat and miloR, in a Posit Workbench session with 128GB of memory and 32 CPUs linked with OpenBLAS. We used the 1.5 million cell COVID PBMC atlas [28–30] described in Seurat’s tutorial. Analysis workflows started from raw counts and ended with quantifiable per-sample measurements – that is, for Seurat, percent of cells annotated as each cell type; for miloR, neighborhood counts; and for tinydenseR, percent cells annotated as each cell type, percent cells in each cluster as well as the fuzzy density matrix. We generated random splits of samples to achieve a range of total number of cells and repeated each workflow three times on each split, applying method-appropriate on-disk data management [31–33]. tinydenseR outperformed Seurat and miloR in processing time and Seurat in memory usage (Fig. 3a–b), underscoring tinydenseR’s efficiency in handling atlas-scale single-cell datasets. Of note, long processing times with miloR precluded memory usage assessment for larger numbers of cells.

![Figure 3](content/690752v1_fig3.tif)

**Figure 3:** (a) Processing time vs. dataset size. Wall-clock time (minutes) for three workflows, tinydenseR, Seurat (BPCells backend) and miloR (DelayedMatrix backend), across subsets of increasing number of cells from the COVID-19 PBMC atlas (up to ∼1.5 M cells). Each point represents a single run (n = 3 per method per size); lines show the median across runs. miloR was evaluated only for splits with fewer than ∼250k cells due to unreasonably long run times.(b) Peak memory vs. dataset size. Peak memory consumption (GB) measured during the same runs using a profvis-based peak-tracking routine. Points denote individual runs; lines show the median per method.(c–d) Percent change estimates across major immune cell subsets in COVID-19 vs. normal PBMC using Seurat (c) and tinydenseR (d) using the entire dataset (∼1.5M cells). Points represent individual samples.(e) Scatter plots comparing cell type abundance estimates between tinydenseR and Seurat for individual COVID PBMC samples. Red dashed line shows one-to-one correspondence between methods.(f) Violin plots of abundance log2FC for cell clusters comparing COVID-19 versus normal PBMC while controlling for sex and publication of origin.(g) Heatmap showing reference-based cell type mapping across clusters. Color scale represents the percentage of cells in each cluster that mapped as each cell type.

On the full dataset, similar trends were observed with tinydenseR and Seurat at the level of reference cell type annotation when comparing immune populations in healthy vs COVID PBMC (Fig. 3c–d), with some subsets showing higher correlation (e.g., cDC2, pDC, HSPC, plasmablasts, CD14 and CD16 monocytes) than others (e.g., ASDC, doublets, erythrocytes and DN T and ψ8 T cells) in head-to-head comparison between the methods (Fig. 3e). In part, observed differences could be due to the two workflows having different reference mapping algorithms (symphony [34], in tinydenseR, vs Seurat’s FindTransferAnchors and MapQuery [35]). In addition, subpopulations within CD4 and CD8 T cells are notoriously tricky to annotate at the transcriptional level, requiring protein expression profiling by CITE-seq for reliable separation[36], which could also contribute to discrepancies in cell type annotations with tinydenseR and Seurat. Of note, despite greater computational efficiency, the tinydenseR workflow yielded three different sample-level outputs compared to a single output in each of the other two workflows. Among tinydenseR’s output is the landmark-level fuzzy density matrices that can be used to shed light on heterogeneity within clusters and/or annotated cell types (Fig. 3f–g). Thus, tinydenseR scales to >1.5M cells, outperforms Seurat and miloR in speed and memory, and provides richer sample-level outputs for heterogeneity analysis.

## Discussion

tinydenseR introduces a shift in single-cell analysis by prioritizing sample-level modeling over cell-level inference and rigid clustering. This design addresses three persistent challenges in large-scale studies: scalability, sensitivity, and robustness. By leveraging probabilistic landmark representations, tinydenseR avoids hard cluster boundaries and preserves continuous biological variation, enabling detection of subtle within-cluster heterogeneity that traditional workflows often miss.

Our results demonstrate that this approach is not only conceptually distinct but also practically impactful. Across synthetic benchmarks, tinydenseR accurately detected differential abundance and expression shifts, including subtle within-cluster changes that traditional clustering methods missed. In preclinical xenograft models, tinydenseR resolved distinct transcriptional states and treatment effects between KO and WT tumors, revealing both compositional and functional heterogeneity in response to KRAS(G12D) inhibition. In clinical trial datasets, tinydenseR uncovered, for example, immune remodeling linked to disease history in multiple myeloma patients. Notably, tinydenseR outperformed widely used workflows such as Seurat and miloR in both speed and memory efficiency, scaling to atlas-sized datasets with over 1.5 million cells while providing richer sample-level outputs – such as fuzzy density matrices and nuanced abundance estimates – that support reproducible and detailed biological analysis.

While tinydenseR is agnostic to technology and biological context, its power depends on well-controlled experimental design and sufficient replicates. As with any computational method, discoveries require orthogonal validation [12]. Future work will focus on extending landmark selection strategies, supporting multi-modal and spatial assays, and improving interoperability with popular data structures and visualization tools [24].

In summary, tinydenseR offers a clustering-independent, sample-centric framework that enables deeper insights into complex biological systems. By modeling samples as the primary unit of inference, tinydenseR provides a scalable and robust foundation for single-cell analysis in clinical, preclinical, and translational research.

## Material and Methods

### tinydenseR AlgorithmStep 1: Data Preprocessing

tinydenseR operates on quality-controlled input data. For scRNA-seq experiments, it accepts sparse raw count matrices with genes as rows and cells as columns. For cytometry experiments, it accepts normalized expression matrices (e.g., arcsine-transformed), with cells as rows and proteins as columns. Each matrix is provided as an element in a list of on-disk RDS file locations, one matrix for each sample.

### Step 2: Landmark Selection

The full cell-by-gene matrix for the entire dataset is never loaded into memory. Instead, tinydenseR processes samples individually, selecting a subset of landmark cells per sample and retaining only landmark-level data. By default, the per-sample contribution is capped at 10% of cells (configurable at object initialization) and the total number of landmarks across the dataset is capped at 5,000. Landmarks are selected with probability proportional to leverage score, where per-cell leverage score is the row-wise sum of squared left singular vectors after single value decomposition (SVD) on the (preprocessed) expression matrix[37]. A fixed random seed (default = 123) ensures reproducibility in sampling.

For scRNA-seq, we first apply library size normalization per cell and log-transform counts as



where y denotes raw counts and s is the cell-specific size factor defined as the total counts per cell divided by the mean total counts across cells. We then select highly variable genes (HVG; default = 5,000), excluding by default TCR/Ig, mitochondrial, and ribosomal protein genes; a user-specified force-in list can be optionally included in the HVG set. We compute a truncated SVD (default k = 30) via irlba [38] on the per-sample centered and scaled HVG matrix, and sample landmarks are selected with probability proportional to the sum of squared entries of the corresponding rows of the left singular vectors.

For cytometry data, we use protein markers (defaults to all markers, but the list of markers used can be defined by the user) and apply per-marker centering and scaling (z-scoring) prior to SVD. We then compute a full-rank SVD (no truncation) and pick landmarks with probability proportional to the row-wise sum of squared left singular vectors. No HVG selection is performed for cytometry.

After per-sample landmarking, we pool the provisional landmarks and fit a dataset-wide PCA (RNA: truncated SVD on z-scored HVGs; cytometry: SVD on z-scored markers). We then compute dataset-wide leverage for every cell by streaming over samples, so the full cell-by-gene matrix is never materialized. For RNA, each sample is library-size normalized and log-transformed, with an additional scalar adjustment that matches the sample’s mean library size to the landmark mean to avoid scale drift, and restricted to the learned HVG set. The sample-specific leverage score derived from the dataset-wide SVD for cell i is , where yi is the centered and scaled expression of cell i, and V,D are the dataset-wide right singular vectors and singular values, respectively.

When batch covariates are provided, we first run harmony [39] on the provisional landmark embedding and build a symphony reference. During the second landmarking pass, we project each cell with symphony into the harmony-corrected space and obtain approximate loadings by taking the SVD of the cross-covariance between the centered corrected embedding and the standardized expression. The sample-specific leverage score derived from the dataset-wide SVD after batch correction for cell i is then computed as above using these approximated loadings.

Using these dataset-wide leverage scores, we perform a second (final) within-sample resampling with probabilities proportional to leverage under the same per-sample and global caps, and recompute the PCA on the updated landmark set (RNA: truncated SVD with HVG re-selection; cytometry: SVD on z-scored markers). After this final PCA, if batch covariates are provided, we again run harmony to replace the embedding with the harmony-corrected one and rebuild the symphony reference. We then derive rotations aligned to the corrected space by linearly residualizing landmark expression against the batch design matrix and performing an SVD of the cross-covariance between the corrected embedding and the residualized, standardized expression (with sign alignment). Since harmony applies a nonlinear correction that alters the geometry of the original PCA space, these approximate rotations should not be interpreted as true loadings. Instead, they are intended only for exploratory analysis and visualization, not for inference on gene–PC relationships. Furthermore, while the landmark selection method described here is heuristic and performs well empirically, it does not guarantee mathematical optimality. Such guarantees would require computing exact leverage scores over the entire expression matrix, which in principle is possible but would entail prohibitive memory and I/O costs.

### Step 3: Landmark Graph Building

Landmark expression data (after PCA/harmony for scRNA-seq as described in the previous step; internally z-scored by uwot::umap for cytometry data using scale = TRUE) is used to construct an approximate k-nearest neighbor (k-NN) graph (default k = 20) on Euclidean distance via the annoy algorithm and to train a UMAP model, both using the uwot package [40].

From this k-NN graph, we derive a Jaccard index-based Shared Nearest Neighbor (SNN) graph based for clustering. Let N(i) and N(j) denote the respective sets of k-nearest neighbors of two landmarks i and j. The Jaccard similarity is:



This measure captures the overlap in neighborhoods rather than raw distance, making the graph more robust to local density variations. The resulting SNN matrix is sparse and symmetric, with entries pruned below a threshold (default τ = 1/15) to reduce noise.

We cluster landmarks using the Leiden algorithm [41, 42] on the SNN graph, optimizing the Constant Potts Model (CPM) objective for modularity and connectivity. Initialization uses k-means (k = 25) on the Laplacian Eigenmaps (LE) embedding (described below). Clusters smaller than 0.5% of landmarks are considered stragglers and merged into the cluster with the highest mean connectivity to the stragglers.

Optionally, the user can manually provide a list mapping one or more clusters to cell types. This is particularly useful in cytometry experiments, where there typically is a larger number of cells and lineage marker-based hierarchical analysis is common.

For LE graph construction, let G = (V, E) be the k-NN landmark graph described above with ∣ V ∣= n landmarks. From the directed, kNN-derived adjacency matrix A, we form a symmetric, unweighted adjacency



and degree matrix D = diag(d1, …, dn) with di = ∑jWij.

We use the symmetric normalized Laplacian:



For LE embedding, we compute the smallest n − 1 eigenpairs of Lsym (or as many as numerically feasible), sort eigenvalues ascending 0 = λ0 ≤ λ1 ≤ ⋯, and discard near-zero eigenvalues λℓ ≤ ω (with ω = 10-6) in our implementation) to remove trivial/degenerate modes.

Let the retained non-trivial eigenpairs be , where each uℓ ∈ ℝn. We select the embedding dimension k via a smooth “elbow” criterion (second derivative) on {λ1, …, λr}, bounded by a target dimension k+ (the number of available PCs) and by r, and floored at 2:



The LE coordinates are the first k non-trivial eigenvectors, rescaled by D$/! and column-normalized:

### Step 4: Probability Computation and Density Matrix Construction

tinydenseR estimates the probability of each cell to be in the neighborhood of a landmark using the first part of the UMAP algorithm before dimensionality reduction. Briefly, landmarks are used as reference to query the nearest landmarks for each cell. UMAP computes a high dimensional graph with fuzzy edge weights between cells, which can be interpreted as connection strengths or probabilities [40].

For each cell c and landmark ℓ, let zc, zℓ ∈ ℝp be the coordinates used by uwot::umap_transform:

Cytometry case: marker intensities are passed to UMAP, which internally z-scores features using center and scale from the training set (scale = TRUE) before constructing the fuzzy graph. No PCA embedding or HVG selection is applied.
RNA case (no Harmony/Symphony): counts are library-normalized to the landmark mean library size and log-transformed, then projected by the landmark PCA:

, where  (cell’s library size),  is the mean landmark library size, and (μ, σ, R) are the PCA center, scale, and rotation from the landmarks. The scalar  ensures per-cell normalization and aligns sample scale to the landmark mean library size.

Harmony/Symphony case (if provided):

Distances used for neighbor search are Euclidean:



Let Nk(c) ⊆ L be the k nearest landmarks of cell c. Define the local connectivity ρ1 = minℓ∈Nkd(c, ℓ). Choose σ1 > 0 so that the total membership mass to the k neighbors equals a target τ (UMAP/uwot default τ = log!k) :



Then the directed fuzzy membership (cell → landmark) is



Let μℓ→c be defined analogously (landmark → cell). The undirected cell–landmark fuzzy edge weight used by tinydenseR is the UMAP fuzzy union:



The per-cell memberships ∑ℓ∈:-(1)μc → ℓ equal τ by construction.

In tinydenseR, we sum the connection probabilities for all cells in a sample to each landmark to yield a measure of sample-level abundance near each landmark. We normalize these abundances by size factors, which are the number of cells in each sample divided by the mean number of cells across samples, preserving the scale of the original data and facilitating log transformation for linear modeling.

Thus, for each landmark, the sum of probabilities across all cells in a sample is used as an estimate of the abundance of cells from that sample around that landmark. If w1ℓ is the UMAP-derived fuzzy connection probability between cell c and landmark ℓ after fuzzy set union symmetrization, the unnormalized abundance around landmark ℓ in sample s is:



, where Cs is the set of cells belonging to sample s.To account for differences in number of cells per sample, the computed probabilities are size normalized using:

, where µc is the across-sample mean of |Cs|, S is the set of samples s, sfs is the sample-specific size factor and  is the size-normalized abundance. This density matrix represents the fuzzy distribution of cells across landmarks (rows) for each sample (columns).

The Leiden clustering labels from Step 3 are transferred to cells from their nearest landmarks (k = 1), automatically deriving clustering results for each cell in each sample. For scRNA-seq, a reference map can also be provided in this step for cell typing, in which case landmarks and cells are mapped against the reference using the symphony package and the nearest neighbor (k = 1) cell annotation from the reference is used as cell type annotation for each landmark and each cell in the dataset. For the current manuscript, a commercial PBMC reference map from Genevestigator was used to annotate leukapheresis, final product and PBMC data, and a symphony object was created from the SeuratData bmcite CITE-seq dataset [43] for annotation of BMMC data.

### Step 5: Differential Abundance and Expression Analysis

We test for differential abundance at the landmark level using the fuzzy density matrix described above. Let  denote the size-normalized abundance for landmark ℓ in sample s. We fit linear models with limma [44, 45] on log-transformed abundances,



, where the pseudocount 0.5 stabilizes variance at low counts. The design matrix encodes the phenotype(s) of interest and any covariates. When repeated-measures (or other blocking) are present, we estimate a consensus intra-block correlation with duplicateCorrelation and fit blocked models with empirical Bayes moderation (eBayes, robust mode [45]).

To increase power while preserving false discovery rate (FDR) control, we implement FDR regression using swfdr [46, 47] with principal component (PC) scores as covariates. Specifically, let X PCA ∈ ℝ&k- be the top k PCs computed from the expression data as in step 2. To ensure independence from the tested covariates, we first residualize these PCs against the same design used to generate the p-values, respecting block structure when blocking is present. We then estimate the covariate-specific null proportion

, where x i ∈ ℝk, with k selected via a smooth “elbow” criterion (second derivative) on the PC standard deviations. The resulting  is used to rescale the q-values:

where  is the BH backbone q-value for the rank of test i:

with p (j) the j-th ordered p-value (ascending) and r(i) the rank of p i in that ordering. Since monotonicity is not enforced after scaling, these q-values are plug-in estimates of per-feature FDR, not a formal rejection set with guaranteed global FDR control. That means, for example, that if we reject a hypothesis with q = 0.1, the estimated false discovery rate for that decision is about 10% (emphasis on “about”). Unlike BH, these q-values do not guarantee that the set of all hypotheses with q ≤ α has FDR less or equal to alpha; they provide covariate-adjusted estimates for individual hypotheses.

In practice, for n < 100 tests (that is, fewer than 100 landmarks) we fall back to BH; for 100 ≤ n < 1000, we use standard Storey q-values to avoid overfitting ; for n ≥ 1000, we apply swfdr on the residualized PCs as described above. To guard against anti-conservative behavior in regimes with large π1(for example, strong signal, correlated tests, small n, etc.), we stabilize the global π0 by taking a robust median across a grid of λ thresholds, (that is, ranging from 0.1 to 0.8 in steps of 0.05), and if this global estimate falls below 0.6, we floor πõ’ at 0.6 before computing PCA-weighted q-values.

Although not used in this manuscript, tinydenseR also returns density-weighted BH-corrected p-values that down-weight landmarks in dense neighborhoods, analogous to cydar and miloR. Let  denote the total fuzzy density mass at landmark l. We define weights



, normalize them to ∑lwl = 1, and apply the weighted BH procedure (equivalently, ordering by p i/wi with the appropriate weighted step-up).

Furthermore, a “traditional” differential abundance analysis is run based on the results from clustering (and cell typing, if provided). Here, cluster/cell type percentages are log2(+0.5)-transformed prior to fitting the same limma workflow models as above. This can be helpful for the analyst to get a quick overview of the results.

For differential expression analysis, tinydenseR uses the map of mutual nearest neighbors between cells and landmarks to generate pseudo-bulk samples for cell subsets of interest (which can be defined flexibly as a single or multiple clusters, single or multiple cell types, or just as landmark indices; here, the nearest neighbor landmark (k = 1) to a cell defines the cell’s subset membership), followed by limma modeling of expression as a function of sample variables in a design matrix. Pseudo-bulks are sums of counts, in the case of scRNA-seq, followed by edgeR voom normalization [48], or medians, in the case of cytometry experiments. Optionally, gene sets can be provided for GSVA-based scoring [49] of pseudo-bulks from scRNA-seq data, which are additionally used in differential gene set score analysis with limma. Gene sets used here were collected from MSigDB using msigdbr [50] (species = “Homo sapiens”; retrieved gene sets: EGFR_UP.V1_UP [51], MEK_UP.V1_UP [51]; KEGG [52]: CELL_CYCLE, and hallmark [52]: G2M_CHECKPOINT, APOPTOSIS, KRAS_SIGNALING_DN, KRAS_SIGNALING_UP, PI3K_AKT_MTOR_SIGNALING, MTORC1_SIGNALING).

### Synthetic Data

Reproducible scripts to generate the three synthetic datasets are provided in the package vignettes (link in Code Availability).

### Benchmarking using COVID PBMC atlas

PBMC datasets in h5ad format were downloaded from three cellxgene collections:

https://cellxgene.cziscience.com/collections/8f126edf-5405-4731-8374-b5ce11f53e82
https://cellxgene.cziscience.com/collections/b9fc3d70-5a72-4479-a046-c2cc1ab19efc
https://cellxgene.cziscience.com/collections/03f821b4-87be-4ff4-b65a-b5fc00061da7

Preprocessing and the Seurat workflow followed the vignette (https://github.com/satijalab/seurat/blob/30f82df52159ac5f0feb80b149698abbd876b779/vignettes/COVID_SCTMapping.Rmd), with one additional QC step: exclusion of samples with fewer than 1,000 cells (94% of samples retained; final dataset: ∼1.48 M cells).

Scripts to reproduce the benchmarking are provided on the tinydenseR GitHub (see Code Availability). In brief:

tinydenseR workflow

Non-default options:

symphony object built from the same reference used in Seurat (not part of benchmarking)
harmony correction by publication of origin
2,000 HVGs (default = 5,000)
Clustering resolution parameter set to 2 (default = 0.8)


All other steps used defaults: raw count normalization, transformation, dimensionality reduction, graph building, and reference mapping.


Seurat workflow

Followed the SCT mapping vignette with BPCells on-disk representation for large-scale efficiency.


miloR workflow

Non-default option: d = 30 in miloR buildGraph
Otherwise followed the miloR and SingleCellExperiment standard with DelayedMatrix representation:

Normalization and log-transformation
HVG selection via DelayedMatrixStats rowVars (top 2,000)
PCA using BiocSingular runPCA with IrlbaParam(deferred = TRUE)
Graph construction and neighborhood counting

Benchmark design:

Subsets of increasing size (16 K to ∼1.5 M cells)
Three replicates per method per size
Metrics: wall-clock time (minutes) and peak memory (GB), measured via a profvis-based peak-tracking routine [53].

### Xenograft model: SW1990 H/NRAS KO cell line engineering

Human cancer cell line SW1990 originated from the CCLE, and was authenticated by single-nucleotide polymorphism analysis and tested for Mycoplasma infection using a PCR-based detection technology (https://www.idexxbioanalytics.com/) when CCLE was established in 2012. SW1990 cells were cultured in RPMI-Glutamax Medium (Thermo Fisher Scientific) supplemented with 10% HyClone FetalClone II serum (Cytiva). Knockout clones were generated by CRISPR technology using ribonucleoproteins (RNP). CRISPR RNA (crRNA) targeting NRAS and HRAS (crRNA NRAS: AGACTCGGATGATGTACCTA, crRNA HRAS: TTGGACATCCTGGATACCGC (IDT)) were annealed with a universal tracrRNA (IDT) to form guide RNAs (gRNAs). RNPs were then formed by combining the gRNAs and Cas9 nuclease (produced in house). Cells were electroporated with the RNPs. NRAS knockout was confirmed by Western Blot. The H/NRAS double knockout was sequentially generated and verified by Western Blot but was only partial, so individual clones were isolated by plating the cells at low density in 96 well plates and selecting the wells where a single cell had formed a colony. NRAS and HRAS knockout in the single clones were further confirmed by Western blot and Amplicon-EZ sequencing (SNP/INDEL detection, Azenta) of PCR-amplified target regions.

### Xenograft model: In vivo Study and Single-Cell Dissociation

Xenograft studies were performed at Novartis in alignment with the protocols and regulations established by the Novartis Institutes for BioMedical Research Animal Care and Use Committee. The studies were approved by the Cantonal Veterinary Office of Basel Stadt, Switzerland, ensuring strict adherence to the Swiss Federal Animal Welfare Act and Ordinance. Mice used in the studies were housed under optimal hygienic conditions in individually ventilated cages, maintained on a 12-hour light/12-hour dark cycle, and provided with sterilized food and water ad libitum. Tumors were generated by subcutaneously injecting 6×106 SW1990 (WT or H/NRAS KO) cells in HBSS mixed with 50% Matrigel (BD Bioscience) into the flanks of female athymic Crl:NU(NCr)-Foxn1nu-homozygous nude mice (Charles River Germany). Tumors were measured twice a week, and tumor volume was calculated using the formula (length × width²) × π/6. The treatment was initiated once the average tumor size reached approximately 500 - 700 mm3. Mice were treated with the KRAS(G12D) inhibitor MRTX1133 at 30 mg/kg i.p. BID, formulated in 20% SBE-β-CD in 50mM citric acid. Tumors were harvested after seven days of treatment, 3h post last dose. A total of 650 mg of tumor material was cut into small pieces and processed according to the manufacturer’s protocol using the Tumor Dissociation Kit (Miltenyi Biotec), followed by mouse cell depletion (Miltenyi Biotec). Single-cell RNA sequencing libraries were prepared using the Chromium Single Cell 3’ Reagent Kit v3.1 (10x Genomics) following the manufacturer’s protocol without modifications. Briefly, single-cell suspensions were resuspended in PBS containing 0.04% BSA and quantified using the Nexcelom K2 cell counter with acridine orange/propidium iodide (AO/PI) staining to assess cell viability and concentration. Minimum cell viability was 80%. Each sample was diluted and subsequently loaded onto a Next GEM v3.1 chip (10x Genomics) to achieve a target recovery of 10,000 cells. Library quality was assessed using an Agilent 2100 Bioanalyzer. Sequencing libraries were analyzed on a NovaSeq6000 system with a depth of 50,000 reads per cell. Mapping was performed using CellRanger version 7.1.0 against the GRCh38-2020-A reference genome.

### Clinical data use statement

Data from a de-identified subset of biospecimens from the NCT04261439 (NIZ985) and NCT04318327 (PHE885) clinical trials were used solely to demonstrate computational workflows without clinical outcome analysis. No clinical endpoints, response evaluations, dose recommendations, or safety analyses were performed here. They were and/or will be described in one or more dedicated clinical manuscripts elsewhere. Sample handling and sequencing followed the study standard operating procedures as summarized below.

### NIZ985 clinical trial flow cytometry data

PBMCs were isolated from whole blood and cryopreserved until analysis. Immunophenotyping was performed starting with approximately 2×107 total white blood cells (WBCs). Cells were thawed, washed and counted. Fc receptor blocking was performed, followed by viability dye staining (eFluor®506, Thermo Fisher, Cat. No. 65-0866-14). PBMCs were then stained for various surface markers, fixed, permabilized, and stained for Ki67 (clone B56, BD, Cat. No. 558615). The stained samples were analyzed on a BD LSRFortessa X-20 flow cytometer. For flow cytometry data analysis, debris was excluded based on FSC/SSC, then singlets were gated on the basis of pulse geometry, viable WBC on the basis of CD45 and viability dye, and lymphocytes were identified as SSC low. T cells were gated as CD3+TCRvd2- in FlowJo (v10). FlowJo workspaces, including gating tree and data transformation were imported into R using flowWorkspace [54].

### PHE885 clinical trial scRNA-seq data

Leukapheresis and final cell product samples were frozen in 1 mL Nunc vials in CS10 by the processing facility. PBMC and BMMC were isolated from 10 mL of whole blood or bone marrow aspirates respectively and cryopreserved until analysis. For scRNA-seq analyses, a 10× Genomics Chromium instrument was used to isolate single cells from thawed samples of cryopreserved cells. Between 10,000 and 20,000 cells per sample were input into the Chromium instrument, targeting data generation between 5000 and 10,000 cells. A 10× Genomics single-cell 5′ library was constructed. The final amplified libraries were pooled, each having a unique adapter index sequence, and applied to a sequencing flow cell. The flow cell underwent cluster amplification and massively parallel sequencing by synthesis using standard approaches (Illumina Inc). Library pooling and flow cell loading were coordinated to target a median coverage of 50,000 reads per cell. The raw sequencing data were processed through 10× Genomics CellRanger, mkfastq, count, and aggr for the 5′ gene expression assay. The human reference genome is based on GRCh38. After CellRanger was run, additional quality control criteria removed droplets that met any of the three conditions: percentage of mitochondrial unique molecular identifiers >15%, number of genes detected <200, and number of unique molecular identifiers <800. For quality control, SoupX (1.4.5) [55] was used to estimate ambient RNA for each sample, and Seurat (5.1.0) was used for data normalization with SCTransform (0.4.1) [56].
