# Stratified Test Accurately Identifies Differentially Expressed Genes Under Batch Effects in Single-Cell Data

## Authors

- Shaoheng Liang<sup>1</sup> †
- Qingnan Liang<sup>3</sup>
- Rui Chen<sup>3</sup>
- Ken Chen<sup>2</sup>

### Affiliations

1. Department Computer Science, Rice University Houston, TX, 77005. E-mail: sliang3@mdanderson.org
2. Department of Bioinformatics and Computational Biology, the University of Texas MD Anderson Cancer Center Houston, TX, 77030
3. Department of Molecular and Human Genetics, Baylor College of Medicine Houston, TX, 77030

† Corresponding author

## Abstract

Abstract
Analyzing single-cell sequencing data from large cohorts is challenging. Discrepancies across experiments and differences among participants often lead to omissions and false discoveries in differentially expressed genes. We find that the Van Elteren test, a stratified version of the widely used Wilcoxon rank-sum test, elegantly mitigates the problem. We also modified the common language effect size to supplement this test, further improving its utility. On both simulated and real patient data we show the ability of Van Elteren test to control for false positives and false negatives. A comprehensive assessment using receiver operating characteristic (ROC) curve shows that Van Elteren test achieves higher sensitivity and specificity on simulated datasets, compared with nine state-of-the-art differential expression analysis methods. The effect size also estimates the differences between cell types more accurately.

## Introduction

Large-scale studies such as the Human Cell Atlas [1] involve hundreds of laboratories, thousands of patients, and millions of cells, bringing about both opportunities and challenges in analyses. When comparing cell types or groups, discrepancies across experiments and differences among participants lead to omissions and false discoveries in differentially expressed genes. Even the trend (upregulated or downregulated) can be reversed in a phenomenon called Simpson’s paradox [2]. These phenomena are termed “batch effects”. For differential expression analysis, batch effects can be handled before performing statistical testing, or factored into the test. Although multiple methods have been proposed to tackle the batch effects, no such option for the widely used Wilcoxon rank-sum test [3], [4] has been applied to single-cell studies, to the best of our knowledge. Here, we show that the stratified rank-sum test (known as Van Elteren test [5]) and our modified common language effect size may fill this gap and benefit single-cell studies.

We briefly review and conceptually compare related works on correcting batch effect in section 1.1. Then, in section 2, we revisit Wilcoxon rank-sum test, and introduce the Van Elteren test supplemented by our direct extension of the common language effect size [6], [7]. In section 3, we use a few examples to illustrate the scenarios where a stratified test is necessary. A comprehensive assessment on simulated datasets shows that Van Elteren test identifies differentially expressed genes with higher sensitivity and specificity, compared with nine state-of-the-art differential expression analysis methods. We also show an application to retinal data. The results show that controlling for batch effects in the Wilcoxon test and its corresponding effect size leads to more accurate biological discoveries, which is the major contribution of this article. More discussions and explanations are shown in section 4.

### Related Works

Mainstream methods to mitigate batch effect fall into two categories, batch correction methods and batch-aware statistical tests. The former includes methods reducing batch effect in the data to facilitate downstream analysis, while the latter includes analyses that control for the batch effect.

#### Batch Correction Methods

Batch correction methods eliminate the discrepancy among batches to create an integrated dataset. The most conspicuous manifestation of batch effect is splitting one cell type into multiple clusters. To solve this problem, many methods match and combine clusters across samples based on similarities. A commonly adopted one, Mutual nearest neighbor (MNN) [8], uses similar cells across datasets as anchors, and based on them correct the gene expression of other cells. Scanorama [9] and the integration utility in Seurat [10] are both based on the MNN methodology. Another method, Harmony [11], iteratively corrects the data by clustering the cells and moving neighboring clusters toward each other. These methods typically produce a unified data matrix, which can be conveniently used in visualization and downstream analysis. However, these empirical corrections usually lack negative control and raise uncertainty in the discovery [12]. Thus, while the corrected data help in visualization and trajectory inference, raw data is recommended for statistical testings [13]. Normalized (and log-transformed) data may also be used if necessary, but any more correction is discouraged.

#### Batch-Aware Statistical Tests

Instead of manipulating the data directly, statistical methods may handle batch effect by considering it as a covariate in the model. Both classical statistical tests and models specifically designed for single-cell data have been adopted in scRNA-seq analyses. The most popular ones are integrated into Seurat [10], a widely used scRNA-seq data analysis platform. To date, it includes Wilcoxon rank-sum test, likelihood ratio test [14], ROC (Receiver operating characteristic) Analysis, Student’s t-test, negative binomial test, Poisson test, logistic regression, MAST [15], and DESeq2 [16]. Among those methods, VanElteren, Linear Regression test, Negative Binomial test, Poisson test, and MAST are capable of accounting for covariates, which can be used to model the batch effects. A more detailed description of these methods is available in Section 2.3.

Notably, all these tests are parametric, meaning that a distribution must be given in advance. However, the debate of the true distribution of single-cell gene expression has never ceased [17], which is a reason why the nonparametric Wilcoxon rank-sum test is widely used. To allow modeling covariates in nonparametric tests, one may use a generalized version of rank-sum test, the proportional odds model [18]. However, modeling batches by using a covariate also makes unnecessary assumptions upon them. Stratification, which only combines statistics from batches, is the “as simple as possible, but no simpler” way to handle batches. The Van Elteren test we use, is the stratified version of Wilcoxon rank-sum test.

It is worth noting that methods like scVI [19] have combined statistical modeling with batch effect correction. However, the effect of batches is modeled by a black-box neural network, making it subject to the same problem of batch correction methods.

## Methods

### Wilcoxon Rank-Sum Test

We briefly revisit the Wilcoxon rank-sum test (also known as Mann–Whitney U test) [3], [4]. The test statistics U is defined as



where  and  are the two samples to be compared (e.g., two cell types in one experiment), with sample sizes n1 and n2, respectively. Function  takes value 1 when its condition holds true, and 0 otherwise. When n1 and n2 are both at least 10, which is common in single-cell studies, the distribution of U approximately follows a normal distribution  where



and



in which ti stands for ties (corresponding to the second term in Equation 1).

### Van Elteren Test

The Van Elteren test [5] is the stratified version of Wilcoxon rank-sum test. For example, if there are m patients, they maybe treated as strata. In that case, a U statistic may be obtained from each patient g ∈ {1, …, m}, denoted as . A new statistics V is constructed by



where wg is a weight for each sample to be discussed later. When m = 1, the formula degenerates to , which is consistent with the rank-sum test.

#### Weights

As discussed by Van Elteren [5], the weights wg can be assigned in different ways. It should be noted that the Ug for a batch g ranges from 0 to ng1 ng2, the product of two sample sizes in the batch. Should the weights all be equal, a patient with more cells available will dominate the test results. It is proven in [5] that weight



eliminates such effect, and a test utilizing such weight is thus named as “design-free test”. However, given that a batch with more instances available (e.g., a patient with more cells sequenced) may be more convincing, another weight



is introduced, which gives more power to larger batches. It also effectively assigns larger weights to batches whose samples are more balanced, when the batch sizes are the same. It is shown in [5] that this choice yields largest statistical power against randomized alternatives, and is thus named as “locally-best test”. The comparison of two weights are shown in Fig. 1.

![Fig. 1.](content/447617v1_fig1.tif)

**Fig. 1.:** The weight (z-axis) for each batch when using the (a) design-free test and (b) locally-best test. samples sizes for two batches are on x- and y-axis. For design-free test all the batches have equal weights, while for locally-best test higher weights are given to batches with higher and balanced sample sizes.

#### Effect Sizes

For Wilcoxon rank-sum test, a simple definition of effect size is



which is centered at 50%, meaning the probability P(a > b) when a and b are randomly drawn from sample A and sample B, respectively. An effect size greater than 50% generally means that A is higher, and vice versa. It may be easily extended for Van Elteren test by taking average using desired weights. For the design-free test, the effect size is



as all batches are treated equally regardless of the sample sizes. It may be interpreted as the probability of P(ag > bg) for ag and bg randomly drawn from Ag and Bg, after randomly choosing a batch g. For the locally-best test, the effect size becomes






which changes the probability of choosing a group g to be in proportion to , giving higher weights to batches with higher and balanced sample sizes (Fig. 1). Generally, any wg may be used to define f, as in



the two previous options being its special cases.

### Other Statistical Tests

We briefly introduce likelihood ratio test [14], ROC (Receiver operating characteristic) Analysis, Student’s t-test, negative binomial test, Poisson test, logistic regression, MAST [15], and DESeq2 [16], which we compared Van Elteren test with in Section 3.2.

#### Likelihood Ratio Test

The likelihood ratio test introduced by McDavid et al. [14] checks if the probabilities (π1 and π2) of cells expressed a gene and the mean expressions (μ1 and μ2) of the cells that express the gene have changed between the two groups. For each group k ∈ 0, 1 the likelihood is defined as



where yk is the expression profile for a specific gene,  is the number of cells expressed the gene, Sk is a set of the cells expressing the gene, and σ2 is the second parameter for the log normal distribution. The likelihood is maximized for the condition H0: π0 = (π1 and μ0 = μ1 and its opposite. The likelihood ratio Λ is then used as the criteria to identify the differentially expressed genes. A p-value can be derived using the fact that –2logΛ asymptotically converges to a χ2 distribution.

#### ROC Analysis

A classifier is built on each gene alone to classify two groups of cells. The area under the curve (AUC) of the ROC for the classifier is used as the metric. An AUC close to 0 or 1 suggests a perfect separation, while a value of 0.5 implies a perfect mixture. The predicted “power” is defined as 2|AUC – 0.5| ∈ [0, 1], where higher is better. A p-value is not available for this method.

#### Student’s t-Test

The distribution of the expression of a gene in both groups are assumed to follow normal distributions with unknown variances. Differentially expressed genes and their p-values are identified by Student’s t-test.

#### Negative Binomial Test and Poisson Test

A negative binomial or Poisson generalized linear model (GLM) is used to identify the differentially expressed genes. Covariates may be added to account for the batches. The distribution of the coefficient accounting for two groups asymptotically converges to a t-distribution and a p-value can be derived.

#### Logistic Regression

Similar to ROC analysis, a logistic regression classifier is built on each gene. A likelihood ratio test is used to calculate the p-values.

#### MAST

MAST [15] is a method specifically designed for scRNA-seq data. It models the log-transformed expression. Similar to the likelihood ratio test, MAST models the number of expressed cells and the expression in the expressed cells separately. A logistic regression model and a Gaussian linear model are used, respectively. The cell detection ratio (CDR), i.e., the proportion of genes expressed in a cell, is added as a covariates to account for nuisance effects in single-cell data. Other covariates may also be manually added.

#### DESeq2

DESeq2 is based on a negative binomial GLM, with more detailed modeling to address large dynamic range, outliers, etc. The p-value is derived using the Wald test.

#### SigEMD

SigEMD [20] combines a data imputation approach, a logistic regression model, and a nonparametric method based on the Earth Mover’s Distance. It can also use gene interaction network information to reduce false positives.

#### DEsingle

To model single-cell data, DEsingle [21] uses a zero-inflated negative binomial distribution to find genes with a significant change in the proportion of drop outs, expression levels, or both. Batch effect is not modeled.

#### Accounting for Batch Effects

Poisson test, negative binomial test, MAST, and DESeq2 can account for batch effects using covariates. For MAST, we one-hot encode the categorical batches as multiple realvalued covariates, each corresponding to a batch (i.e., a patient or an experiment).

## Results

We implemented the Van Elteren test with the effect size in R, available at our GitHub repository (https://github.com/KChen-lab/stratified-tests-for-seurat), based on Seurat 3.0 by utilizing its differential expression analysis part (but irrelevant to the data integration) [10]. When there are two groups of cells, A and B, denoted as type, and patient identity, denoted as batch, the Van Elteren Test can be called as follows.

The genre may be set to either locally-best or design-free, as introduced in section 2, based on which p-values and effect sizes are calculated. Typical results are shown in Table 2 and 3. An effect size of larger than 0.5 indicates a higher expression in cell type A, and vice versa. The avg_logFC, average logarithmic fold changes, are calculated automatically by Seurat, where a positive value indicates a higher expression. It may show different trends compared with the effect sizes. Generally, the effect sizes are more indicative after controlling for the batch effect.

### Illustrations

To show the utilities of Van Elteren test, we simulated a illustrative dataset. The parameters are specified in Table 1. Poisson distribution is used to model sequencing depth. Visualization is available in Fig. 2 for illustration. We assume that the library size of each sample is equalized by other genes beyond the simulated ones. For illustrative purpose only, we applied Van Elteren test and Wilcoxon rank-sum test for an intuitive comparison, as the former is a stratified version of the latter. A more comprehensive comparison of all the state-of-the-art methods on a more realistic dataset is available in Section 3.2. The results are shown in Table 2 and 3. Trend (A over B) are indicated by arrows. For Van Elteren test, the locally-best version and the design-free version return very similar results.

![Fig. 2.](content/447617v1_fig2.tif)

**Fig. 2.:** The illustrative dataset. Two shades correspond to two cell types (dark: cell type A; light: cell type B). For each gene, the left panel is stratified by patients and the right panel shows aggregated distribution.

**TABLE 1**
 Rates for Poisson Distribution in Illustrative datasets


**TABLE 2**
 P-values on the Illustrative Dataset


**TABLE 3**
 Effect Sizes on the Illustrative Dataset


#### Suppressing False Negatives

Batch effect may introduce false negatives, where a significantly differentially expressed gene is overshadowed. For gene 1, on which cell type B always have higher expression on both patients, the Wilcoxon rank-sum test did not pass the threshold of 0.05 to reject the null hypothesis, while Van Elteren test yields a significant p-value. The effect size, smaller than 0.5, also correctly suggests that the expression of gene 1 in cell type B is higher than that in cell type A, compared with the average logarithmic fold change, which wrongfully indicates otherwise.

#### Suppressing Reversed Conclusions

Batch effect may also lead to reversed conclusion (i.e., which cell type has higher expression). For gene 2, on which cell type A always have higher expression value, both tests reject the null hypothesis. However, the effect size of Van Elteren test, larger than 0.5, correctly identifies that the expression of gene 2 in cell type A is higher than that in cell type B, while the average logarithmic fold change wrongfully indicates otherwise.

#### Suppressing False Positives

False discoveries are also possible outcome of batch effect. As is shown in gene 3, the distribution of both cell types are exactly the same in each patient. Nevertheless, Wilcoxon test yields a very significant p-value. The average logarithmic fold change also has a large magnitude. Van Elteren test returns a p-value of 0.7831, together with a effect size close to 0.5, suggesting that the difference is neither significant nor large.

#### Consistency

As a negative control, when the three issues above are not present, p-value from Van Eleteren test is consistent with Wilcoxon rank-sum test, as is shown by gene 4. The effect size and the log fold change also both show that the cell type B has higher expression in gene 4.

### Simulation Study

To evaluate the performance of differential analysis methods, we simulated scRNA-seq datasets using Splatter [22]. The expression of each gene in each cell follows a Poisson–gamma mixture (i.e., negative binomial distribution), whose parameters follow a hierarchical model which characterizes the library size for each cell using a log-normal distribution, and the expression level of a gene using another gamma distribution. In addition, outlier genes are chosen by a Bernoulli distribution and scaled by a log-normal distribution, and a mean-variance trend in the expression is enforced by simulated Biological Coefficient of Variation. Using the R package of Splatter, 1,000 genes were simulated for six samples, each containing 100, 200, 300, 400, 500, and 600 cells. The split of two cell types is 3:7. Genes are randomly (p = 0.1) designated as differentially expressed and multiplied by a factor following a log-normal distribution (σ = 0.4, μ as specified below). For other parameters, we used default values except for batch.facLoc=2.0, batch.facScale = 0.8, and bcv.common = 0.5. The genes that are expected to be differentially expressed was identified using the simulated parameters and served as the ground truth for our assessment.

We compared Van Elteren test with all state-of-the-art differential expression analysis methods that interface with Seurat, i.e., Wilcoxon Rank Sum test, log likelihood test, ROC Analysis, Student’s t-test, Negative Binomial test, Poisson Test, Logistic Regression, MAST, and DESeq2. We used raw data whenever possible, as suggested by Luecken and Theis [13], except for MAST, which runs only on log-transformed normalized data. Batch information were input for Van Elteren test, Linear Regression test, Negative Binomial test, Poisson test, and MAST, which have the ability to account for batch effects.

We used the receiver operating curve (ROC) for each test to compare the methods intuitively. Formally, the ROC is the trace of false positive rate (FPR) and true positive rate (TPR) for selecting different numbers of top genes ordered by their p-values (or power for ROC Analysis). The area under curve (AUC) of the ROC was used as a quantitative metric. A good statistical test would achieve a high true positive ratio at a low false positive ratio, and thus have a greater AUC.

One example (μ of the log-normal distribution for DEG was set to 0.1) is shown in Fig. 3. Van Elteren test is clearly better than all methods not accounting for the batch effect (dashed lines). By a smaller margin, Van Elteren test also achieves greater AUC (0.860) than MAST (0.841), negative binomial (0.839), logistic regression test (0.833), and Poisson test (0.763), where the batch effects are accounted for as covariates. It is notable that tests uses covariates or stratification generally performs better than those that do not, showing the importance of accounting for such factors when analyzing dataset with batch effects. An exception is Poisson test, because the dataset largely deviates from the Poisson distribution. Nevertheless, Poisson test with covariates still performs better than its counterpart without covariates.

![Fig. 3.](content/447617v1_fig3.tif)

**Fig. 3.:** ROC curve of tested methods. Solid lines are for stratified tests or test with covariates (labeled by “+” symbol in the legends), while dashed lines are for the others. Methods are split into two panels for visual clarity.

To confirm the observation, we used μ = 0.1, 0.3, and 0.5 to repeat the experiment. Results summarized in Fig. 4 consolidate that tests uses covariates or stratification generally performs better. With the batch effects addressed, the accuracy of Van Elteren test, linear regression test, negative binomial test, and MAST are largely comparable. Van Elteren test performs slightly better in terms of median/mean AUC with a smaller variance. The performances of all methods improve when the effect size (which corresponds to μ) is larger, while the contrasts of the methods remain unchanged. It should be noted that gamma–Poisson mixture is a major part of Splatter, which naturally favors negative binomial test and MAST. In reality, patterns of gene expression are highly variable. The performance of parametric methods will decrease significantly, like the Poisson test, when the model does not fit. The nonparametric Van Elteren test is more versatile to different distributions.

![Fig. 4.](content/447617v1_fig4.tif)

**Fig. 4.:** AUC of tested methods in n = 10 randomly simulated datasets. The median (center lines), interquartile range (hinges), 1.5 interquartile range (whiskers), and corresponding data points (dots) are shown. “μ” is the location parameter of the log-normal distribution for DEG.

### Retina Data

We have tested the Van Elteren test on real retina singlecell RNA sequencing data gathered from three patients [23]. Two regions, macula (i.e., the center area) and peripheral, are labeled in the data of 5,873 cells × 10,713 genes. Cell types was annotated using unbiased clustering and marker genes in the original publication. We question which genes differentially express for the same cell type between two regions. We ran Wilcoxon rank-sum test and Van Elteren test on 2,295 rod cells and 203 cone cells. Original counts (accessed by GEO series number GSE133707) were used for both methods. We compare the results in Fig. 5, where genes with large differences in p-values between two tests are labeled with gene names.

![Fig. 5.](content/447617v1_fig5.tif)

**Fig. 5.:** Comparison of p-values returned from Wilcoxon rank-sum test and Van Eletern test on (a) rod cells and (b) cone cells. Each dot is a gene, whose p-value from Wilcoxon rank-sum test and Van Elteren test are shown by its x-coordinate and y-coordinate, respectively. Genes with largely changed p-values (102 for rod cells and 101 for cone cells) are labeled with gene names.

#### Rod Cells

The results of two tests are largely comparable, showing a diagonal pattern. Meanwhile, some exceptions are present (see Table 4 for the p-values and effect sizes), among which we observed that p-values for gene GNGT1 and SYNE2 change the most.

**TABLE 4**
 Gene with large p-value chagne in rod cells


For GNGT1, the reversed conclusion effect is also observed, as the Van Elteren f effect size suggests that the peripheral region has a higher expression, while the log fold change indicates otherwise. We further inspected the distributions to validate and interpret the differences. In Fig. 6A, the left panel does show generally higher expression of GNGT1 in each individual patient, while the aggregated distribution on the right shows a reversed effect, which is an instance of the aforementioned Simpson’s paradox. For SYNE2 (Fig. 6B), conspicuous discrepancy among batches is also shown, which leads to a less precise rank-sum test result. Indeed, these two genes were found playing roles in macular degeneration diseases [24], [25].

![Fig. 6.](content/447617v1_fig6.tif)

**Fig. 6.:** Distribution of counts of (a)(b) GNGT1 and (c)(d) SYNE2 in rod cells. Left panels are stratified by patients and right panels show aggregated distributions.

#### Cone Cells

For cone cells, the results are similar. Some genes show changes while most genes are consistent across the tests. The p-values and effect sizes are shown in Table 5.

**TABLE 5**
 Gene with large p-value change in cone cells


For gene PCBP4, Van Elteren test shows more significant p-value, and an effect size indicating smaller expression in macula, which is different from the log fold change. Decrease in PCBP4 has also been linked with age-related macular degeneration [26]. Fig. 7 shows that batch effect in distribution of PCBP4 may have misled the rank-sum test and the logarithmic fold change.

![Fig. 7.](content/447617v1_fig7.tif)

**Fig. 7.:** Distribution of counts of PCBP4 in rod cells. The left panel is stratified by patients and the right panel shows aggregated distributions.

## Discussion

The results have clearly shown that Van Elteren test benefits biological studies in precisely identifying differentially expressed genes. Although the results we show do not include multiple comparison correction, Seurat 3.0 will automatically give corrected p-value based on the raw p-value using Bonferroni correction. Generally, any correction based on p-values will also apply.

Our simulation study shows that Van Elteren test is one of the best performing methods among the most widely used state-of-the-art methods. It should be noted that due to no free lunch theorem, the performance of a method depends on the degree of match of the data and the model. Being a nonparametric test, Van Elteren test does not assume a specific distribution and thus suits the exploratory analysis of a dataset, where the distribution of the gene expression varies. This is especially valuable for scRNA-seq data analyses as it is cumbersome to check the distribution pattern of thousands of genes.

The result also indicates that stratified test is a neat way to handle batch effect. Although covariate has the ability to control for explanatory variables, it is generally more suitable for continuous variables. It also casts more assumptions when modeling covariate. Stratified test, on the other hand, does not infer the influence of the discrete batches. Rather, it directly aggregates the statistical power of multiple samples.

We also show that the weighted common language effect size, a byproduct of Van Elteren test, reflects the difference of gene expression more faithfully. It can be used with Van Elteren test or other tests, to support a more comprehensive understanding of the data.

Admittedly, for the rod cells in the retinal data, although changes in p-values are observed, the significance threshold was well passed by both. However, it should be noted that the retina data are collected from relatively healthy tissues and are considered clean, while Van Elteren test is expected to make a more meaningful difference on noisy pathological and tumor data. In addition, rod cell is the most populous cell in retina. For rare cell types that take smaller proportions, like the cone cells, the difference Van Elteren test makes can be crucial.

Overall, Van Elteren test and our modified common language effect size are direct extensions of the Wilcoxon ranksum test and common language effect size. As nonparametric methods, they perform well in various scenarios, with or without obvious batch effect. A caveat of the stratified test is that for it to work the strata shall not overlap with the variable of interest. For instance, it may not find the difference, meanwhile also control for the batch effect, between two patients. Nonetheless, neither is covariate applicable to such cases. As the batch effect and biological effect are convoluted, more prior knowledge is generally needed to distinguish them. Another limitation is that it does not detect interaction effects between variables, which may need more complex nonparametric tests such as Aligned Rank Transform [27]. Besides, when the distribution can be reasonably assumed, such as a normal distribution where the central limit theorem apply, a corresponding parametric test may offer a higher power.

## Summary

We have adopted Van Elteren test, an underappreciated statistical test, and our weighted common language effect size to single-cell sequencing data. When batch effect is severe, the test control for false positives and false negatives. Otherwise, it is consistent with Wilcoxon rank-sum test. Simulation study show that Van Elteren test achieves the state of the art. The modified common language effect size also faithfully depicts the trends. This work may increase the precision of differential expression analysis to help identify genes of interests.
