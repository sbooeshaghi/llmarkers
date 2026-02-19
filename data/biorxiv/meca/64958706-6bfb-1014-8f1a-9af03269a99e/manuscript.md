# Estimation of genomic prediction accuracy from reference populations with varying degrees of relationship

## Authors

- S. Hong Lee †
- Sam Clark
- Julius H.J. van der Werf †

### Affiliations

1. School of Environmental and Rural Science, University of New England NSW 2351 Australia

† Corresponding author

## Abstract

ABSTRACT
We present a theoretical framework for genomic prediction accuracy when the reference data consists of information sources with varying degrees of relationship to the target individuals. A reference set can contain both close and distant relatives as well as ‘unrelated’ individuals from the wider population, assuming they all come from the same homogeneous population. The various sources of information were modeled as different populations with different effective population sizes (Ne). With a similar amount of data available for each source, we show that close relatives can have a substantially larger effect on genomic prediction accuracy than lesser related individuals. However, the number of individuals from the wider population can be far greater than that of close relatives. We validate our theory with analysis of real data, and illustrate that the variation in genomic relationships with the target, rather than the variation in genomic relationship as a deviation for the expected relationship, is a predictor of the information content of the reference set and information from pedigree relationships is then naturally included in the prediction framework. Both the effective number of chromosome segments (Me) and Ne are considered to be a function of the data used for prediction rather than being population parameters. We illustrate that when prediction also relies on closer relatives, there is less improvement in prediction accuracy with an increase in training data or marker panel density. We release software that can estimate the expected prediction accuracy and power when combining different reference sources with various degrees of relationship to the target, which is useful when planning genomic prediction (i.e. before collecting data) in animal, plant and human genetics.

## INTRODUCTION

Genomic prediction of (additive) genetic effects and phenotypes is emerging in a wide range of fields including animal and plant breeding, risk prediction in human medicine and forensics1–4. Genomic prediction requires modeling of the association between genome-wide single nucleotide polymorphisms (SNPs) and phenotypes. The success of genomic prediction is measured by its accuracy, i.e. how reliable a future phenotype of target individuals can be predicted.

Genomic prediction requires a reference population of individuals having information on both genotype and phenotype. The accuracy of genomic prediction depends on various parameters, including sample size of the reference and its genetic structure. An important parameter in relation to the latter is the effective size of the population. The effective population size is a predictor of the effective number of chromosome segments that are represented in the population5–7. Theoretical predictions have usually considered a homogeneous population of individuals that are essentially unrelated. However, in most practical applications, the reference population used for genomic predictions possibly consists of many sub-groups with individuals having a variety of relatedness to the target individual, e.g. direct relatives, more distant relatives, and individuals that are considered unrelated, but still part of the same population as the target individual. It is relevant to assess the contribution of these various sources to prediction accuracy before actually conducting an experiment.

A number of studies have shown that genomic predictions are more accurate if the genomic relationship between the proband and the reference population is higher, both in humans8–11 and in other species12–14. Habier et al (2013)15 distinguished between three types of information in genomic prediction; linkage disequilibrium, additive-genetic relationships and co-segregation of QTL predicted from markers genotypes with a pedigree. They argued that it would be useful to understand how these sources contribute to the accuracy of genomic predictions, especially when designing reference populations for breeding programs. They show these contributions via simulated examples but did not provide methods that allow simple predictions for their contribution to accuracy. Pszczola et al. (2012)16 showed that the relationship between the reference population and the proband should be maximized to achieve an optimal design using a simulation study. However, they also did not attempt to derive the expected prediction accuracy from an optimal design in advance. Hayes et al. (2009)17 considered the influence of direct relatives on genomic prediction. They followed the same approach as the general theory, i.e. by considering the number of independently segregating chromosome segments within families. They showed the accuracy of genomic prediction from varying sizes of the first and second degree of relatives, but did not consider the information from combined sources18. It should also be noted that those studies that derived genomic prediction accuracy from theory using effective number of chromosome segments (Me)5,6,19–21, did not consider the correlation between relatedness at different chromosomes, therefore overestimating Me and underestimating whole-genome prediction accuracy7.

Wientjes et al (2016)22 proposed a simple selection index approach to combine information from different populations. They considered a genetic correlation between genetic effects expressed in different populations. We propose to use the same approach to combine different sources of information from within a population, where the different cohorts have a different degree of relationship with the target individual. To predict the accuracy, we derive the number of effective chromosome segments from a hypothetical Ne associated with each subset, and we show that that combining such subsets using selection index theory gives the same result as using a prediction from an Me derived from the variation in genomic relationships between the reference data and the target. Prediction accuracy is derived from variation in genomic relationship rather than the variation in genomic relationship as a deviation for the expected relationship among members of the reference set, as was proposed by Goddard et al (2011) and also applied by Wientjes et al (2016). This approach leads to a theoretical concept useful for assessing the accuracy of genomic predictions in advance, and we illustrate this with examples based on real data.

## MATERIALS AND METHODS

### Predicting genomic selection accuracy

The accuracy of genomic breeding values (GBV) or (genomic profile score in the context of human risk prediction23) based on genome-wide SNP genotypes can be predicted from theory5–7, 24, assuming that prediction is based on a reference population with phenotypes and genotypes for the same genome-wide SNPs that are linked to quantitative trait loci (QTL). The accuracy depends on i) the proportion of genetic variance at QTL captured by markers and ii) the accuracy of estimating marker effects. The proportion of genetic variance at QTL captured by markers (b) depends on linkage disequilibrium (LD) between markers and QTL, which in turn depends on the number of markers (M) and the number of ‘effective chromosome segments’ (Me)5, that is

Various forms of prediction of Me have been presented5,6,21 that were however inconsistent to each other, and without considering the correlation between chromosomes. Recently, we presented a prediction formula with the form7

where Ne = effective population size; L = average chromosome length; Nchr = number of chromosomes. This formula accounts for mutation, and that without considering mutation should be referred to equation (10) in Lee et al. (2017)7 The accuracy of the genomic prediction of a phenotype can be written as5

where ry,ĝ is the correlation coefficient between the true phenotypes (y) and estimated GBV, h2 is the heritability of the trait, and N is the number of phenotypic observations. Other measures for genomic prediction accuracy, particularly for human risk prediction, such as the area under the receiver operating characteristic curve or odds ratio of case-control status contrasting the higher or lower risk group are described elsewhere7.

### Me and genomic relationship

After collecting genotypic information of the reference data and the target individual, it is possible to obtain an empirical Me from a genomic relationship matrix (GRM). In this derivation, the elements in the GRM are  where xTm and xjm are the standardised genotype coefficients (mean 0 and variance 1) for the target individual (T) and jth individual in the reference data at the mth locus. It is possible to construct a GRM for each locus, and the elements in the GRM at the mth locus are GTj(m) = GT*(m) = xTmxjm where * denotes the set of all reference individuals. Then, the variance of the mean of GT*(m) across all M, SNPs in a single chromosome is

where cov(x*(l), x*(m)) = xT(l) ⋅ xT(m) = rm,l, which is a correlation between the mth and lth SNP-genotype, because of var(x) = 1 and mean(x) = 0, i.e. the genotype coefficients are standardized in the population, Mi is the number of SNPs in the ith chromosome and Μe(i) is the effective number of chromosome segments for the ith chromosome, which is the inverse of the expectation of the squared correlation between SNPs6,7. When considering multiple chromosomes, the covariance of the pairwise relationship between two chromosomes is not negligible7. Assuming equal length and number of SNPs for Nchr chromosomes, Me for the whole genome can be written as

where Nchr is the number of chromosomes.

In Goddard et al. (2011)5, their theoretical derivation had to assume a homogeneous population of individuals that are essentially unrelated. However, here we show that the assumption about unrelated individuals can be relaxed so that any random samples from the population can be used for Eq. (4), irrespective of they are related or not.

### Effective population size in a reference data set

One of critical parameters to determine the accuracy of genomic prediction is the effective population size (Ne). It is not very common to represent a reference population by a single value of Ne when it consists of several cohorts of individuals with different relationships to the target individual. The only study using a single value for Me representing a reference set consisting of two population is by Wientjes et al. (2016)22. Here, we introduce a novel concept based on the relationship between Ne, Me and var(GT*), which can assign a value of Ne for a reference population consisting of several cohorts. For any subset of the reference data set, there are realized relationships with the target sample. From Eq. (4), a value of Me, which is the inverse of the variance of the genomic relationships between the proband and the reference sample, can be assigned to the reference data. Then, a single value of Ne, which is a function of Me from Eq. (1), can be obtained for the reference data. The effective population size of the reference set is therefore a parameter specific to the data used. It can be smaller, but also larger than the actual effective size that is often contributed to the population from which the data is derived, depending on whether closer or more distant individuals are chosen for the reference set.

Based on this concept of Ne, reflecting information content of the reference sample in relation to the target sample, we consider three information sources consisting of 1) close relatives of the proband, e.g. Ne = 10, 2) distant relatives or individuals from the local area of the proband, e.g. Ne = 100 and 3) a wider population sample of individuals that are not related to the proband, e.g. Ne = 1,000.

The GBV can be estimated based on each of these information sources, and the accuracy of the estimation can be calculated as above, e.g. rg,ĝ(i) from Eq. (1) where i represents the ith information source. It is also possible to estimate GBV based on combined data of all three information sources. Assuming a random sample from the same population for each source, the accuracy of the GBV based on the combined data set can then be calculated using standard selection index theory as

where g is the vector with covariances between each of the GBV and the true breeding value, and P is the variance-covariance matrix of the set of GBV. The accuracy of the GBV based on the combined data set can also be estimated based on the weighted Me from the three information sources. Assuming a random sample from the same population for each source, the weighted Me can be obtained as

where pk is the proportion of the sample size over the total sample for each information source. The accuracy of the GBV based on the weighted Me is identical with that using standard selection index theory above (Eq. (5)). Following Wientjes et al. (2016)22 we can further generalize for a case where genetic correlations among multiple reference populations and those between reference populations and the target are not one. Equation (5) can be generalized as

where rGk,T is the genetic correlation between the kth reference population and the target set, and similarly, rGi,j is the genetic correlation between the ith and jth reference population (i = j = 1 ~ k).

### Simulation

In a simulation, a stochastic gene-dropping method 25,26 was used to simulate 4,000 SNPs for each of 30 chromosomes, each of length L=1 Morgan with Ne = 50, 500 and 1000 for 50, 500 and 1000 generations, respectively. Recombination and mutations were modelled according to the genetic distance between SNPs and the mutation rate of 1e-08 per site per generation27. In the final generation, we constructed a genomic relationship matrix for a random set of 3000 individuals. Among the 3000 individuals, we randomly selected 1000 individuals as target data and 2000 individual as reference data, and estimated variance of the genomic relationships between the target and reference data to validate Eq. (3).

### Evaluation of the formulas

For each of the three information sources contributing to genomic prediction we varied values for Ne, sample size in reference data and marker density. We compared the expected accuracy of GBV from the sample of Ne =1000 with predictions that additionally included information from the sample of Ne =100 and Ne =10. The total number in the reference population was kept equal between the comparisons.

### Real data analysis

We used publicly available data from the Framingham heart study (phs000007.v26.p10.c1)28. There were 6950 individuals genotyped for 500,568 SNPs. Stringent quality control for genotype data and phenotype adjustment for confounders were applied to the data (the details can be found in Lee et al. (2016)7). The quality control included SNP call rate > 0.95, individual call rate > 0.95, HWE p-value > 0.0001, MAF > 0.01 and individual population outliers < 6 SD from the first and second principal components (PC). After QC, 6920 individuals and 389,265 SNPs remained. Among them, 4243 individuals were phenotyped for height and body mass index (BMI).

We made three different information sources to form the reference data that were tested in 100 replicated analyses (Table 1). Initially, we randomly selected 800 individuals out of 4243 phenotyped individuals as a target data set. For reference data set #1, we selected 50% of individuals that were highly related (> relatedness of 0.3) to the 800 target individuals (N1 = 617 ± 19). For reference data set #2, we selected 80% of moderately related individuals (> relatedness of 0.1) of the 800 target individuals (N2 = 1254 ± 30). For reference data set #3, we took the rest of the individuals that were not selected for reference data set #1 and #2 (N3 = 1572 ± 33). There was no overlap sample between target data set and reference data sets #1, #2 and #3.

**Table 1.**
 The sample size (N) and empirically observed Me in each of three different reference data sets and combined data set in the Framingham data analysis.


Using the real genotype data, the genomic relationships between the reference and target sample were constructed. Empirical Me was estimated from equation (3) for reference #1, 2 and 3, and that for combined data. We took a median rather than mean because the distribution of variance of the genomic relationship between target and reference sample was skewed. The correlation between the true phenotypes (that were not used in the analyses) and estimated GBV in the target data set was estimated for the combined data set, which was used as the genomic prediction accuracy (ry,ĝ). Phenotypes were adjusted for birth year, sex, and the first 10 PCs were used to control non-genetic confounding effects, e.g. population stratification.

## RESULTS

In the simulation study, as shown in Figure 1A, 1B and 1C, the expected (from Eq. (1)) and empirically observed Me from the simulated genotyped data (using Eq. (4)) are in good agreement, however, they are considerably lower than the expectation from the previous formulas5,6,21, which confirms the result from Lee et al. (2016)7. It is noted that Eq. (4) is still valid in the subset with a smaller Ne = 50 that has a significant proportion of high related individuals, indicating that the assumption about unrelated individuals (made in Godard et al. (2011)5) can be relaxed.

![Figure 1.](content\119164_fig1.tif)

**Figure 1.:** Expected effective number of chromosome segments (Me) from previous studies in 20096, 20115 and 201321 and from Eq. (1) in this study, compared to empirically observed from Me simulation when varying the number of chromosomes each with 1 Morgan long. Effective population size was used as Ne =50 (A), 500 (B) and 1000 (C). This confirms the result from Lee et al. (2016)7.

In the evaluation of the formulas, we first tested how the prediction accuracy was changed with varying marker density, using formula (1) and (2) and b = M / (Me + M) (Figure 2). For Ne=10,000, the accuracy gradually increased with marker density, but the slope became flat when using the number of SNPs exceeded 100,000 (Figure 2A). For Ne=1,000, the accuracy did not increase with marker density as long as the number of SNPs was higher than 50,000 (Figure 2B). For Ne=100, there was no improvement of the accuracy if the number of SNPs was more than 10,000 (Figure 2C). This would be expected because the proportion of genetic variance at QTL captured by markers (b = M/ (Me + M) approached one when the number of SNPs (M) was more than 100,000, 50,000 and 10,000 for Ne = 10,000, 1000 and 100, respectively (Figure 3), as Me was equal to 21,248, 2,313 and 254 for these three cases.

![Figure 2.](content\119164_fig2.tif)

**Figure 2.:** Accuracy of GBV when varying the number of SNPs for Ne = 10,000 (A), 1000 (B) and 100 (C). The sample size in the reference data was N=12,000, 6000 or 3000. The heritability was 0.25.

![Figure 3.](content\119164_fig3.tif)

**Figure 3.:** The proportion of genetic variance at QTL captured by markers (b =M / (Me + M) when varying the number of SNPs for Ne = 10,000, 1000 and 100.

Next, we quantified the contribution of each information source when varying sample size in the reference data using formula (1), (2) and (4) (Figure 4). It was assumed that the number of SNPs was sufficient to capture most of causal variants (e.g. > 50,000). When adding 100 individuals of Ne=100 or Ne=10 to the reference sample with Ne=1000, the accuracy was slightly or substantially improved (Figure 4A). The improvement was larger when adding more individuals (500) (Figure 4B). Results showed that an information source of a smaller Ne was more important when the samples sizes of each information source were the same. When the total number of reference data was increased, the importance of adding an information source of a smaller Ne was relatively decreased (Figure 4). When heritability was higher, overall accuracy was increased, and the relative contribution from an information source of a smaller Ne, i.e. the close relatives, was reduced (Figure 5).

![Figure 4.](content\119164_fig4.tif)

**Figure 4.:** Accuracy of GBV when adding 100 individuals (N=100) (A) or 500 individuals (N=500) (B) of Ne= 100 or Ne= 10 to the reference population of Ne= 1000, The heritability was 0.25.

![Figure 5.](content\119164_fig5.tif)

**Figure 5.:** Accuracy of GBV when adding 100 individuals (N=100) (A) or 500 individuals (N=500) (B) of Ne= 100 or Ne= 10 to the reference population of Ne= 1000, The heritability was 0.25. The heritability was 0.75.

Figure 6 confirms again that the smaller Ne, the better the prediction accuracy when using each information source separately. However, the sample sizes can be also varied across the information sources, as there are generally a lot fewer close relatives than individuals from the wider population. In Figure 6A, the accuracy at a sample size of 100 for Ne=10 was 0.73, which was lower than that of a sample size of 1,000 for Ne=100 (0.81) or that of a sample size of 20,000 for Ne=1,000 (0.83). With a higher heritability, the result is similar in that the 20,000 records in the information source of Ne=1000 gave a better accuracy than the 100 records of close relatives (Ne=10).

![Figure 6.](content\119164_fig6.tif)

**Figure 6.:** Accuracy of GBV when using Ne=1000 only, Ne= 100 only and Ne=10 only with a heritability of 0.25 (A), and with a heritability of 0.75 (B). For Ne=l0 only, the accuracy at a sample size of 100 was 0.73 (A) and 0.88 (B). For Ne=100 only, the accuracy at a sample size of 1000 was 0.81 (A) and 0.92 (B). For Ne=1000 only, the accuracy at a sample size of 20,000 was 0.83 (A) and 0.93 (B).

In real situations, the most common and desirable design may combine all of the information sources to maximize the prediction accuracy. We plotted the accuracy using a composite design consisting of Ne=1000 + Ne=100 (N=500) + Ne=10 (N=50), compared to that using Ne=1000 (Figure 7). The accuracy for a composite design was substantially increased especially when the total number of reference sample is low (Figure 7).

![Figure 7.](content\119164_fig7.tif)

**Figure 7.:** Accuracy of GBV when using a composite design, e.g. Ne=1000 + Ne=100 (N=500) + Ne= 10 (N= 50), compared to Ne=1000 only with a heritability of 0.25 (A) and with a heritability of 0.75 (B).

Figure 8 illustrates the real data analyses. The median of empirically estimated Me from the inverse of the variance of the genomic relationship (Eq. 3) over 100 replicates was 2254 (SD=50), 3989 (SD=104) and 28848 (SD=920) for reference #1, #2 and #3, respectively (Table 1). Empirically estimated Me based on the combined data was 4836 (SD=106) while expected Me was 5309 (SD=88), approximately confirming Eq. (4). The (small) difference between empirical observation and expectation was probably due to skewed distribution of the variance of the genomic relationships.

![Figure 8.](content\119164_fig8.tif)

**Figure 8.:** When using Framingham data, empirically estimated Me based on each of the reference data sets and combined data. Empirically estimated Me based on combined data is approximately agreed with that from theory (Eq. 4).

Given Me, N and h2, the expected accuracy (from Eq. (2)) agreed well with the observed accuracy when using Framingham data (Figure 9). The reported heritabilities, h2=0.8 29–31 for height and h2=0.4632,33 for BMI, were used.

![Figure 9.](content\119164_fig9.tif)

**Figure 9.:** When using Framingham data, observed prediction accuracy and expected prediction accuracy with given Me and N (from Eq. (2)) are agreed well. The reported heritability, h2=0.8 29–31 for height and h2=0.4632,33 for BMI, were used.

Finally, we quantified the importance of marker density using the real data. In agreement with Figure 2, the prediction accuracy is not much decreased even with 50,000 SNPs that were randomly selected from 389,265 SNPs (Figure 10).

![Figure 10.](content\119164_fig10.tif)

**Figure 10.:** When using Framingham data, the prediction accuracy is not much decreased even with 50,000 SNPs that were randomly selected from 389,265 SNPs.

## DISCUSSION

This work shows a simple approach for modeling genomic prediction in a reference data set that contained several subpopulations that differ in relatedness to the target set, and by modeling these subpopulations as having different effective population size. The model allows assessing the prediction accuracy before actually conducting an experiment so that designing genomic prediction can be precise and effective in animal, plant and human genetics. For example, it can address a question how much the prediction accuracy can be increased by adding 10,000 (conventionally) unrelated individuals into the current experiment consisting of 100 relatives in the reference data. The value for Ne in equation (1) can be approximated based on prior knowledge of a population, and the relatedness of the sample with the target, possibly supported by some genotype information that maybe available on cohorts, or samples thereof. Prediction in advance indeed relies on arbitrary modelling a number of cohorts, but it would be a useful exercise, as illustrated in the results when considering marker density and various sizes of the subsets of the training data. The theory is also useful for an animal breeder to predict the value of genotyped animals in an own herd versus those in a wider references population consisting of a larger number of more distantly related individuals.

The genotypic and phenotypic information of close and distant relatives of the proband can be effectively used as a part of the unified reference panel that also include a large number of individuals that are not related to the predicted subject to improve the accuracy further as illustrated in Figure 7. For a random sample from the same homogenous population, e.g. within the same breed or ethnicity, an optimal design should consist of both close and distant relatives and unrelated individuals, e.g. a composite design, to maximise the prediction accuracy (Figure 7). That is, the composite design takes advantage of effective information from smaller number of relatives while it also use information from a greater number of unrelated individual.

Using equation (1) and (4), we showed that the prediction accuracy derived for a population with unrelated individuals turns out to be higher, compared to previous quantifications that overestimated Me for a larger number of chromosomes5,6,21,34.

Using the same theory, we also showed that the information from close relatives could increase the accuracy even further, especially for smaller reference populations (Figures 3–6). It is important to note that the assumption about using unrelated individuals in estimating empirical Me from genomic relationship5 is not strictly necessary and can be relaxed (Eq. (3) and (4)). The theory and empirical observation from simulation study agreed well (Figure 1) even when using a population with a smaller effective population size (Ne=50) that consisted of a significant proportion of high relatedness.

Previous studies related to genomic prediction accuracy have suggested that Me can be derived from the variation in the differences between realized and expected relationships6,22, i.e. D = G – A where G is a genomic relationship matrix and A is a numerator relationship matrix based on pedigree. Those studies validated their results also with simulation. If the individuals used in the training set have a low expected relationship to the target individuals, then there is not much difference between the variations in D versus G. However, when some closer relatives are used, var(G) is larger than var(D) and Me is therefore smaller. Note that non-random sampling of individuals used for the training set can cause a difference between the Ne of the population that was simulated, and the Ne of the data set that was used for prediction.

We have not tested the theory for multi-breed reference populations, i.e. those that are heterogeneous in the sense of consisting of populations from different genetic background, i.e. different breeds or ethnicities, each with different minor allele frequencies, different LD structure and different effects for causal variants. Wientjes et al. (2016)22 explicitly addressed the problem of different effects for causal variants (i.e. genetic correlation less than one) when combining data from two populations. Individuals from different populations share genomic relationships that are lower than those among members within each population. Evidence in literature suggests low prediction accuracies when using information from different breeds or populations, which could be viewed as predicting from populations with very large Ne. Moreover, we have not considered historical population dynamics such as bottleneck and admixture, but assumed a constant Ne over the historical generations, which leads to simplifications that make the formulae tractable and easy to derive. Further work is required to extend the theory accounting for admixture populations and historical population dynamics.

We have shown an improved theory for the prediction of the effective number of chromosome segments, which is a key parameter in genomic prediction accuracy7. The theory accounts for the correlation between relationships at different chromosomes and as a result the effective number of chromosome segments is smaller than predicted from previous theory5,6,21. As a result, the increase of the genomic prediction accuracy appears to be less reliant on higher marker density unless Ne is very large (e.g. > 10,000) (Figure 2), compared to what have been quantified by previous theory5,6,21. The previous theory overestimates Me (mostly due to neglecting correlation between chromosomes), therefore underestimates the proportion of genetic variance at QTL captured by markers. Little improvement of prediction accuracy with increasing SNP marker density has been empirically observed in a number of studies35–37. This may also have important implication in genomic prediction as to designing marker density in animal, plant and human genetics.

The ability to quantify the accuracy in relation to various degrees of relationships (e.g. close relatives, distant relatives, local or extensive population sample) is important for predicting outcomes of genomic prediction for specific designs. This study has addressed this question, and the theory has been implemented in MTG2 software (https://sites.google.com/site/honglee0707/mtg2). Therefore, a user can know the expected prediction accuracy and the power38 before designing an experiment of genomic prediction. Our approach can be applied both before and after collecting the data.
