# Prediction of Alzheimer’s Disease from Single Cell Transcriptomics Using Deep Learning

## Authors

- Aman Srivastava<sup>1</sup>
- Anjali Dhall<sup>1</sup>
- Sumeet Patiyal<sup>1</sup>
- Akanksha Arora<sup>1</sup>
- Akanksha Jarwal<sup>1</sup>
- Gajendra P. S. Raghava<sup>1</sup> ([ORCID: 0000-0002-8902-2876](https://orcid.org/0000-0002-8902-2876)) †

### Affiliations

1. Department of Computational Biology, Indraprastha Institute of Information Technology Okhla Phase 3, New Delhi-110020 India

† Corresponding author

## Abstract

Abstract
Alzheimer’s disease (AD) is a progressive neurological disorder characterized by brain cell death, brain atrophy, and cognitive decline. Early diagnosis of AD remains a significant challenge in effectively managing this debilitating disease. In this study, we aimed to harness the potential of single-cell transcriptomics data from 12 Alzheimer’s patients and 9 normal controls (NC) to develop a predictive model for identifying AD patients. The dataset comprised gene expression profiles of 33,538 genes across 169,469 cells, with 90,713 cells belonging to AD patients and 78,783 cells belonging to NC individuals. Employing machine learning and deep learning techniques, we developed prediction models. Initially, we performed data processing to identify genes expressed in most cells. These genes were then ranked based on their ability to classify AD and NC groups. Subsequently, two sets of genes, consisting of 35 and 100 genes, respectively, were used to develop machine learning-based models. Although these models demonstrated high performance on the training dataset, their performance on the validation/independent dataset was notably poor, indicating potential overoptimization. To address this challenge, we developed a deep learning method utilizing dropout regularization technique. Our deep learning approach achieved an AUC of 0.75 and 0.84 on the validation dataset using the sets of 35 and 100 genes, respectively. Furthermore, we conducted gene ontology enrichment analysis on the selected genes to elucidate their biological roles and gain insights into the underlying mechanisms of Alzheimer’s disease. While this study presents a prototype method for predicting AD using single-cell genomics data, it is important to note that the limited size of the dataset represents a major limitation. To facilitate the scientific community, we have created a website to provide with code and service. It is freely available at https://webs.iiitd.edu.in/raghava/alzscpred.
Key Points

Predictive Model for Alzheimer’s Disease Using Single Cell Transcriptomics Data
Overoptimization of models trained on single-cell genomics data.
Application of dropout regularization technique of ANN for reducing overoptimization
Ranking of genes based on their ability to predict patients’ Alzheimer’s Disease
Standalone software package for predicting Alzheimer’s Disease


Author’s Biography

Aman Srivastava is pursuing M. Tech. in Computational Biology from Department of Computational Biology, Indraprastha Institute of Information Technology, New Delhi, India.
Anjali Dhall is currently working as Ph.D. in Computational Biology from Department of Computational Biology, Indraprastha Institute of Information Technology, New Delhi, India.
Sumeet Patiyal is currently working as Ph.D. in Computational Biology from Department of Computational Biology, Indraprastha Institute of Information Technology, New Delhi, India.
Akanksha Arora is currently working as Ph.D. in Computational Biology from Department of Computational Biology, Indraprastha Institute of Information Technology, New Delhi, India.
Akanksha Jarwal is pursuing M. Tech. in Computational Biology from Department of Computational Biology, Indraprastha Institute of Information Technology, New Delhi, India.
Gajendra P. S. Raghava is currently working as Professor and Head of Department of Computational Biology, Indraprastha Institute of Information Technology, New Delhi, India.

## Introduction

Alzheimer’s disease (AD) poses a significant challenge to the medical industry and is a leading cause of dementia [1]. Globally, approximately 6.2 million individuals suffer from AD-induced dementia, and this number is projected to double every 20 years if a cure is not found [2,3]. AD is a progressive neurological disorder characterized by a decline in social, behavioral, and cognitive abilities, ultimately impairing independent functioning [4]. The presence of neuroinflammation, amyloid-beta peptide deposition, and tau neurofibrillary tangles are recognized as pathological biomarkers in AD [5]. However, it is important to note that their presence does not necessarily indicate the occurrence of AD-specific dementia, and the precise relationship to neurodegeneration remains unknown [6,7]. It is worth noting that although AD typically manifests in later stages of life, the pathogenesis often initiates much earlier than the onset of symptoms. Despite numerous studies and clinical trials focused on understanding and treating these pathological changes, no effective cure for AD currently exists [6]. Present treatment strategies primarily aim to alleviate symptoms and delay disease progression [8].

One of the reasons for the absence of the successful treatment methods for AD is the lack of knowledge of molecular underpinnings of cell-type specific responses for the pathogenesis of atrophy and neurodegeneration [9]. The bulk-tissue-level analysis may obscure the complexity of modifications between and within cells, particularly for rare cell types [10]. It is one of the significant challenges to understanding the complex human brain, which comprises a huge variety of cells that include billions of neurons of different subtypes [11]. Single-cell RNA sequencing provides an approach to analyze thousands of individual cells and study the compositional as well as functional changes within the cells to gain a clear insight into the mechanism of AD [12]. Recently, several studies have been conducted to identify the diagnostic and prognostic biomarkers of AD. For instance, Xiong et al., reported that KIR3DL2, PPP2R2B, and QPCT are upregulated in peripheral B cells while FRAT2, WWC3, and SPG20 are downregulated, and this gene panel of biomarkers can be used to diagnose and predict AD [13]. In addition, Yu et al. conducted a bioinformatics analysis and identified serum-based biomarkers (NEBL, EPB41L2, FGD4, and MARCKS) for AD [14].

In our study, we utilized single-cell RNA sequencing data from the GEO dataset, which included 169,496 nuclei from the prefrontal cortex of normal human subjects and AD patients (GSE157827) [15]. Through various machine learning and data mining approaches, we aimed to identify crucial gene-based biomarkers capable of stratifying AD and normal samples. Furthermore, to facilitate the scientific community, we have provided an end-to-end Python package. The complete workflow of our study is depicted in Figure 1.

![Figure 1:](content/548171v1_fig1.tif)

**Figure 1::** Workflow shows major steps involved in this study like data extraction, data processing, feature selection, and model development.

## Materials and methods

### Data Collection and Pre-processing

We accessed the single-cell gene expression profiles from the NCBI GEO repository, specifically the dataset with the GEO accession number GSE157827 [15]. The dataset comprises 21 samples, including 12 from individuals with Alzheimer’s disease (AD) and 9 from normal controls (NC). The gene expression profiles were generated using the Illumina NovaSeq 6000 sequencing platform, focusing on the prefrontal cortex of both AD and NC samples. The dataset consists of a total of 169,496 nuclei and encompasses 33,538 genes. We utilized the 10x single-cell sequencing data format, which included raw counts, barcodes, and gene files for each AD and NC sample. As the data obtained from the Cell Ranger pipeline was in sparse format, containing only non-zero entries to minimize file size, we transformed it into feature-barcode matrices using single-nucleus RNA sequencing (snRNA-seq). Subsequently, we removed outliers, including irrelevant genes and cells, using the scanty preprocessing library [16].

After the preprocessing steps, we identified 5,401 expressed genes, representing the number of genes with mapped reads in both AD and NC samples. Normalization was performed using the scanty.pp.normalize_total Python library. Additionally, we filtered out cells and genes containing NaN or zero values for each cell type to ensure data integrity. Finally, we divided the dataset into two parts: an 80% training dataset and a 20% validation dataset, enabling us to assess the performance of our models.

### Feature Selection Algorithm

In this study, we have used a feature selection approach in order to reduce the dimensions of the data matrix and to obtain an important set of genes that can accurately stratify the AD and NC samples. Here, we have used the information-theory-based feature-selection (IFA) method of minimum Redundancy and Maximum Relevance (mRMR), which has been previously implemented in similar types of studies analysis [17–19]. mRMR algorithm selects those genes/features which have a high correlation with the class (i.e., output) and a low correlation between themselves. The mRMR method not only takes into account the associations among the genes and samples but also reduces the redundancy within genes. For example, it selects only the most representative gene out of similar types of genes. Here, we have selected the top 100 most relevant genes and then applied an incremental feature selection algorithm to find out the optimal set of genes as biomarkers [20].

### Model Development

Various machine learning and deep learning techniques have been implemented in this study to develop the models for the classification of NC and AD samples. The machine learning algorithms include decision tree (DT), random forest (RF), logistic regression (LR), XGBoost (XGB), and extra tree classifiers (ET) [21–24]. The non-parametric supervised learning models serve as the foundation for the DT algorithm. The goal was to create a model by learning the decision rules from the data features that may predict the response variable. RF is an ensemble-based approach for classification that predicts the response variable using each individual tree while fitting a variety of DTs during training. Averaging DTs increases model control over overfitting and prediction accuracy. The logistic or logit model, which offers a class or event probability, can be obtained using the LR approach. To develop a model that can predict a class or response variable, the logistic function is used. This approach resembles multiple linear regression. However, the dependent variable, in this case, is binomial instead. Scalable tree boosting classification algorithm XGB makes a final prediction after several iterations. It makes use of the ensemble method, which combines a number of models to make the final forecast. We created models that can forecast the response variable or class of the sample by using parameters tuned on the training dataset.

ML models were observed to be performing well on the training dataset. However, the performance was not comparable when checked on an independent validation set. In order to overcome this problem, we have used deep learning-based models to stratify the samples, which use a customized artificial neural network (ANN). An ANN is composed of a network of interconnected systems or nodes known as artificial neurons, which are generally designed like neurons in the human brain [25]. Our neural network architecture consists of 1 input layer, 3 hidden layers, and 1 output layer with a dropout of 0.3 at each step to reduce the overfitting of the deep learning model. The final output is the predicted label which tells whether the sample is diseased or not. Scikit-Learn, TensorFlow, and Keras Python libraries were used to implement the machine learning and deep learning algorithms [26,27].

### Cross-validation technique

To ensure the robustness and reliability of our prediction models, we employed the 5-fold cross-validation technique in combination with external validation. This approach allows us to evaluate the models using both internal and external datasets. The 80% training dataset was utilized for internal validation, where the data was split into five equal sets or folds, ensuring an equal representation of positive and negative samples in each fold. Subsequently, the models were trained using four-folds, while the fifth fold served as the test set. This process was repeated five times, with each fold acting as the test set once, and the performance metrics were calculated for each iteration. Finally, the performance results from all five sets were averaged to obtain the final performance assessment. In addition to the internal validation, we performed external validation using the remaining 20% of the data. This independent dataset served as an external benchmark to assess the generalizability of our models. By evaluating the performance on both internal and external datasets, we obtained a comprehensive understanding of the predictive capabilities and reliability of our models. This technique has been previously used in many studies [28,29].

### Performance measures

We employed established evaluation metrics to assess the effectiveness of various prediction models. We employed both threshold-dependent and independent parameters in this study. We have used the following equations to quantify threshold-dependent parameters such as sensitivity (Sens), specificity (Spec), precision, F1-Score, and accuracy (Acc). In order to evaluate the effectiveness of the models, we additionally employed the typical threshold-independent parameter Area Under the Receiver Operating Characteristic (AUROC) curve.

Where Ptr is truly positive, Ntr is truly negative, Pfa is false positive, and Nfa is false negative.

## Results

### Feature Selection

In this work, we have used snRNA-seq expression profiles of 12 AD and 9 NC samples incorporating 5401 genes and 128706 cells. We used the mRMR technique to shortlist a set of 100 genes that were highly relevant in regard to the detection of Alzheimer’s disease. The selected top 100 genes are provided in the supplementary table S1. To make our prediction model even more accurate, we wanted to obtain a smaller set of genes that play an important role in the detection of Alzheimer’s disease. To achieve the same, we employed the incremental feature selection (IFS) technique, where we plot an IFS curve for all the combinations of genes (features) on the x-axis and the accuracy value obtained from all sets on the y-axis as shown in Figure 2. The optimum accuracy was obtained when the model was trained with 35 biomarkers, as after that, there was no significant improvement in the accuracy of the model. A list of the set of 35 selected genes is given in supplementary table S2.

![Figure 2:](content/548171v1_fig2.tif)

**Figure 2::** Accuracy of models developed using a set of features selected using the incremental feature selection (IFS) technique.

![Figure 2:](content/548171v1_fig2a.tif)

**Figure 2::** Plot for patient-wise analysis using single-cell RNA profile

### Performance of classification models

Initially, we applied various machine learning algorithms like DT, ET, RF, LR, and XGB, and we found that most of the models performed well on the training dataset, but the performance was not comparable on validation data (See Table 1). In order to improve the prediction performance, we have applied deep learning. It was observed that deep learning-based models outperform all the machine learning models on the validation dataset. As shown in Table 1, we were able to achieve a maximum AUROC of 0.84 and an accuracy of 82.00% on an independent validation dataset for a set of 100 genes selected using the mRMR feature selection technique. For a set of 35 genes that were shortlisted using the IFS technique, we obtained the maximum AUROC of 0.75 and an accuracy of 74.00% on the independent validation set. The results for the top 35 selected genes are given in Table 1.

**Table 1:**
 Performance of various machine learning and deep learning models using top 100 features (mRMR) and top 35 features selected using IFS.


### Patient wise analysis

To test our final model based on deep learning, we fed the data containing a full single-cell sequence profile for each patient and saw how accurately it predicted the disease in each subject. The results for the patient-wise analysis for the top 100 genes and the top 35 genes are given in Table 2 and Figure 3.

**Table 2:**
 Patient-wise analysis using single-cell RNA sequence profile


### Biological functions of selected genes

After feature selection using mRMR and IFS, about 35 genes were extracted, which could serve as potential diagnostic biomarkers of Alzheimer’s. We then performed Gene Ontology (GO) Enrichment Analysis on these extracted 35 genes to map the biological functions of the selected genes. The Go enrichment analysis results are shown in Table 3. Most of the Genes are involved in the Binding Activity and catalytic activity of various metabolic processes. Other activities associated with reported genes are ATP-dependent activity, molecular function regulator, transcription regulator activity, molecular transducer activity, and transporter activity.

**Table 3:**
 Gene Ontology (GO) enrichment analysis for the selected 35 genes


## Discussions

Alzheimer’s has now been recognized in the category of world health concerns. It accounts for nearly 60-70% of cases of dementia [30]. There are several criteria that have been proposed for the screening and diagnosis of AD, including physical symptoms, bodily fluids, and imaging studies. Despite this, there is currently no cure for AD, and the only effective therapy involves the management of symptoms. Various drugs such as galantamine, donepezil, and rivastigmine are prescribed to increase memory power and brain alertness, but they cannot control the disease progression [31]. Numerous studies have demonstrated that altering lifestyle practices, including food and exercise, can improve brain health and lessen AD without needing medical attention [32]. Hence, it is recommended as a first-line prevention strategy for all AD patients. Significant neuronal loss and neuropathological abnormalities can harm several brain regions by the time the disease is identified [33]. To prevent this, the study aims to identify some specific biomarkers which could aid in early screening and diagnosis of Alzheimer’s disease from the Single Cell genome.

In this study, we have used various machine learning models and a deep learning model to classify NC cells and AD cells from their single-cell RNA-seq profile. Also, patient-wise analysis to classify the samples is also done in this study on a total of 21 samples. We compared the deep learning model with other traditional machine learning models to find out that the deep learning model performed well very against all the traditional machine learning models. Initially, the dataset was quite large, with a very high number of features (>30000). The data were then pre-processed, and the feature count was reduced to a significantly lower number (=5000). Since many features were correlated and redundant, so a feature selection method known as mRMR was applied to get a minimal set of features, which could be helpful in classifying the samples. Out of these 5000 features, mRMR was applied to extract the top 100 features with minimal redundancy and maximal relevance, which achieved an AUROC of 0.84 on an independent validation set using deep learning. The IFS method was then applied to select an even smaller gene set and obtain an optimal number of biomarkers. We found about 35 genes (features) to be optimal, and they were able to distinguish the AD patients from NC individuals with an accuracy of 74% and AUROC of 0.75 on the independent validation set. In addition, we performed Gene Ontology (GO) enrichment analysis in our study to gain insight into the mechanism and role of selected genes in the development of Alzheimer’s disease. Silencing of lncRNA X-inactive specific transcript (XIST) was found to be directly connected to an increase in Alzheimer’s symptoms. The XIST gene was found to be upregulated in AD models in both in vitro and in vivo studies [34]. Gene “TSC22D4” in a study with Japanese Alzheimer’s patients showed to be significantly differentially regulated as compared to normal controls [35]. “FGF17”, i.e., Fibroblast growth factor dysregulation, has been reported in various brain-related (neurological and psychiatric) disorders. It has been shown to be altered in epileptogenesis [36]. Transcriptional regulatory changes are prominent features of brain diseases, transcriptional changes in the gene “FOXN2” highlights the convergence of genetic risk with psychiatric and neurodegenerative disorders [37].

Genes such as “CDK18” have uncharacterized mechanisms by which they may promote AD neurodegeneration, and this increases the probability that their inhibition may cause protection against AD development pathology [38]. There are also genes such as ‘BCOR,’ ‘AC090517.4’, ‘LGI4’, ‘SLC25A13’, and ‘ZBED5’, which have not yet been reported in any connection with Alzheimer’s disease progression and development. Thus, further deep studies are required to evaluate these biomarkers, and these could act as novel findings. Genes ‘SCD’ and ‘UBE2Z’ have been reported in various studies related to cognitive impairment and diagnosis or treatment of Alzheimer’s disease [39,40]. About 21 genes out of the 35 genes reported in this study have been observed to have a connection to Alzheimer’s disease and a relation with neurodegeneration. Other findings need further study and research.

The limitation of this study is that we have only evaluated a total of 21 samples from both normal and Alzheimers affected patients. The data was obtained from the prefrontal cortex of the brain. More data from areas like the hippocampus and amygdala can be obtained to add to this dataset for identifying further promising biomarkers. In addition, more studies on the identified genes in clinical setups are required for in-depth analysis and their role in how they affect and cause Alzheimer’s disease progression.

## Supporting information
