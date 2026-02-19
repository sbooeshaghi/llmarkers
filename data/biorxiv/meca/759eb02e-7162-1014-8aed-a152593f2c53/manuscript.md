# Bringing PanglaoDB to 5-star Linked Open Data using Wikidata

## Authors

- Tiago Lubiana<sup>1</sup> ([ORCID: 0000-0003-2473-2313](https://orcid.org/0000-0003-2473-2313)) †
- João Vitor F. Cavalcante<sup>2</sup> ([ORCID: 0000-0001-7513-7376](https://orcid.org/0000-0001-7513-7376))

### Affiliations

1. Graduate Program in Bioinformatics, University of São Paulo São Paulo Brazil
2. Bioinformatics Multidisciplinary Environment, Federal University of Rio Grande do Norte Rio Grande do Norte Brazil

† Corresponding author

## Abstract

Abstract
PanglaoDB is a database of cell-type markers widely used for single-cell RNA sequencing data analysis. However, cell types and genes in the database are encoded by free text, lacking proper identifiers. Wikidata, is a freely editable knowledge graph database useful for integrating biomedical knowledge. We thus reasoned that porting PanglaoDB’s markers to the platform could improve their reusability and overall technical quality (FAIRness).We mapped 188 cell types from PanglaoDB to species-neutral terms on Wikidata and created 376 species-specific terms for cell types in Homo sapiens and Mus musculus. These terms were enriched with marker information via the has marker (P8872) property, totaling over 15.000 cell type X marker associations (w.wiki/9iw6). We explored this new subset of the graph via SPARQL queries, illustrating the discovery potential of structured, integrated knowledge. For example, we found a previously unexplored link between rosehip neurons, clozapine, and schizophrenia via the HRH1 marker. Besides the graph-based insights, we took time to describe the details of the reconciliation process, hoping to stimulate more resources for a move to a 5-star linked open data format.

## Introduction

PanglaoDB (Franzén et al., 2019) is a publicly available database that hosts metadata and results of hundreds of single-cell RNA sequencing experiments. It also provides a rich dataset of cell type markers, containing thousands of cell type to marker associations. It also displays a rich web user interface for easy data acquisition, including database dumps for bulk downloads.

As of 30 December 2020, when the first draft of this article was completed, the PanglaoDB had already been cited 88 times. As of 27 March 2024, when we were finalizing the preprint for bioRxiv, PanglaoDB had been cited even more impressively, amassing over 880 citations. Despite that, PanglaoDB’s data is still at a 3-star level of quality for Linked Open Data (Berners-Lee, 2008) as it does not use the open semantic standards from W3C (RDF and links to the web, Figure 1). Moving data format toward W3C’s gold standards is a valuable step in making biological knowledge FAIR (Findable, Accessible, Interoperable, and Reusable) (Wilkinson et al., 2016). Among other qualities, 5-star linked open data uses unique resolvable identifiers, removing ambiguity, and is parseable by computers, making it easier to integrate it into smart algorithms.

![Figure 1:](content/589259v1_fig1.tif)

**Figure 1::** The 5-star linked open data schematics, designed by Sir Tim Berners-Lee, available at 5stardata.info/en. Cell marker data in PanglaoDB is at 3 stars, with openly available CSV dumps. Wikidata provides two extra layers of quality: RDF support and links to the wider web of data.

Wikidata is an open, freely editable, knowledge graph database within the semantic web that stores knowledge across a multitude of domains and uses an item-property-value model (Figure 2). It is easy to use and edit by both humans and machines, with a rich web user interface and wrapper packages available in R and Python. All pieces of information within Wikidata are automatically available on the web and released in the public domain for unrestricted reuse.

![Figure 2:](content/589259v1_fig2.tif)

**Figure 2::** Wikidata item example, showing item hepatocyte (Q827450), the labels change according to the user’s language, but each item has a universal identifier, called the QID1 and formatted as a Q followed by numbers. Items are assigned numbers in chronological order, as they are created.

Several advances for biological data in Wikidata have been made before, showcasing its potential for bioinformatics. The platform has been proposed as a unified base to gather and distribute biomedical knowledge and includes concepts for a myriad of genes, organs, diseases, biological processes, and other biological and biomedical concepts (Mitraka et al., 2015; Turki et al., 2019, 2022; Waagmeester et al., 2020).

Wikidata already covers a wide range of concepts in the life sciences, but as it is collaborative, quality depends on the attention given to a particular domain. In particular, Wikidata had very little information about cell types when we started, with less than 300 items classified as cell types, while other projects described over 2,000. (Diehl et al., 2016; Stachelscheid et al., 2013).

We, thus, had 2 main motivations for the work described here. The first was integrating PanglaoDB into the semantic web, in light of the needs of the Human Cell Atlas community (Regev et al., 2017). And second, increasing the scientific usefulness of Wikidata while describing the steps taken as references for similar projects.

## Methods

In Figure 3 we show an outline of the relatively simple steps taken on this work. In summary, we got permission to do the migration from Oscar Franzén from PanglaoDB, then selected the bits of information needed (cell types and genes). We then figured out a semantic schema for markers on Wikidata. Some curation followed, with manual mappings of the controlled vocabulary of PanglaoDB to Wikida identifiers. We then used the mappings as the basis for some Python scripts that used WikidataIntegrator to batch-add the markers to Wikidata.

![Figure 3.](content/589259v1_fig3.tif)

**Figure 3.:** An overview of the basic pipeline for reconciling a resource to Wikidata.

### Getting the data

Gene data from Wikidata was acquired using the Wikidata Query Service for Homo sapiens genes and Mus musculus genes. The markers dataset was downloaded manually from PanglaoDB’s website (panglaodb.se/markers/PanglaoDB_markers_27_Mar_2020.tsv.gz). It contained 15 columns and 8256 rows. Only the columns species, official gene symbol, and cell type were used for the reconciliation. All data was handled using the pandas Python library.

### Creating classes on Wikidata

Classes corresponding to species-neutral concepts were retrieved from Wikidata manually using Wikidata’s graphical user interface and biocurated to matching terms in PanglaoDB. Cell types not represented on Wikidata were added via its web interface and logged into the mapping table. Although PanglaoDB is not a semantic resource, we used the Simple Standard for Sharing Ontology Mappings (SSSOM) based format (Matentzoglu et al., 2022) for sharing openly the mappings on Zenodo (https://doi.org/10.5281/zenodo.10936294).

Mappings were not purely based on lexical matches, but carefully curated to reflect meaning. For example, the description of “Basal cells” on PanglaoDB states that “Basal cells are keratinocytes found in the basal layer of the skin”, so the concept was matched to basal cell of the skin (Q101062513) instead of the more general basal cell (Q809772). The concept of basal cell may be used to describe cells in many organs, but that is seemingly not what was intended by PanglaoDB curators. The lack of unique identifiers on PanglaoDB (and its subsequent 3-star rating) makes the platform ambiguous, and the matching process opinionated, time-consuming, and somewhat delicate.

After the mapping, species-specific cell types for human and mouse cell types were created for every entry in the reference table and connected to the species-neutral concept via a subclass of (P279) property (e.g., human neutrophil is a subclass of neutrophil). Our approach to species-specificity was analogous to the one taken by the CELDA ontology, which used rdfs:subClassOf to denote it (Seltmann et al., 2013).

Each item was labeled “human” + the label for the neutral cell type, described as “cell type found in Homo sapiens” and tagged with the statement found in taxon Homo sapiens. An analogous framework was used for mouse cell types, assuming that “mouse” in PanglaoDB meant Mus musculus. Batch creations were added to Wikidata via the Quickstatements tool.2

All genes in PanglaoDB either had a 1:1 mapping to Wikidata, in which case they were mapped via the HUGO Gene Nomenclature Committee (HGNC) ID (P354) property, or resolved to multiple entities, in which case they were excluded from the reconciliation. Mouse markers on PanglaoDB are curiously also identified with HGCN symbols. They were assumed to be valid only when the upper case transformation of their Mouse Genome Informatics (MGI) Gene Symbol (P2394) was a 1:1 match to HGNC.

### Crafting the “has marker” property on Wikidata

We needed a way to represent marker information on Wikidata. New properties need to be supported by the community in a public forum before creation. Thus, we proposed a property called has marker for peer review, so we would have the technical infrastructure for the project. We posted a message on 17 November 2020 presenting the property, domain, range constraints, and additional comments. The following motivation statement accompanied the proposal:

“Even though the concept of a marker gene/protein is not clear cut, it is very important, and widely used in databases and scientific articles. This property will help us to represent that a gene/protein has been reported as a marker by a credible source, and should always contain a reference. Some markers are reported as proteins and some as genes. Some genes don’t encode proteins, and some protein markers are actually protein complexes. The property would be inclusive to these slightly different markers. Some cell types are marked by the absence of expression of genes/proteins/protein expression. As these seem to be less common than positive markers (no organized databases, for example) they are left outside the value range for this property”

The proposal had specifications of the property such as:

The property was approved on 27 November 2020. For those curious about it, more details can be found on the Wikidata property proposal page, available online (wikidata.org/wiki/Wikidata:Property_proposal/has_positive_marker).

### Integration to Wikidata

The reconciled dataset was uploaded to Wikidata via the WikidataIntegrator python package3, a wrapper for the Wikidata Application Programming Interface. The integration details can be seen in the Jupyter notebooks on the GitHub page jvfe/wikidata_panglaodb. Authorization to do the migration and release the data in the CC0 license on Wikidata was provided by e-mail by Oscar Franzén, lead developer of PanglaoDB.

### Access to reconciled data

The PanglaoDB markers are now part of the main Wikidata content and are available via two formats: database dumps and a SPARQL endpoint. The bulk formats include RDF dumps at wikidata.org/wiki/Wikidata:Database_download and it is possible to also download partial dumps of the database with reduced size (ex: wdumps.toolforge.org/dump/987 for all cell types with the has marker property).

Besides the Wikidata Dumps, Wikidata provides an SPARQL endpoint with a Graphical User Interface (query.wikidata.org/). Updated data was instantly accessible via the endpoint, enabling integrative queries.

Of note, as Wikidata is an open system, marker information from different resources was added in the years that followed. Thus, to get only information from PanglaoDB, one needs to filter the markers by the provenance, with SPARQL queries as the one shown in Code snippet 1.

### Code and data availability

All source code used for the study and data created during the study are available in a GitHub repository, github.com/jvfe/wikidata_panglaodb, as well as archived (as of April 2024) at doi.org/10.5281/zenodo.4438614.

![Code snippet 1.](589259v1_ufig1.tif)

**Code snippet 1.:** SPARQL query to get only PanglaoDB (Q99936939) cell type markers (P8872) on Wikidata. 15772 edges as of 8 April 2024. Available at w.wiki/9hgV,

## Results

### Cell types on Wikidata

As of August 2020, Wikidata had 264 items being categorized as instances of cell type, considerably less than in specialized cell catalogs at the type, which counted over two thousand cell types. Strikingly, there were also 23 items categorized as instances of cell (Q7868). This classification was imprecise, as an instance of cell would be an individual named cell from a single named individual, which should not generally be on Wikidata.

Wikidata editors often mix first-order with second-order classes. First-order classes point to real-world individuals, like the zygote that gave rise to Dolly, the sheep (a real-world cell), and the brain of Albert Einstein (a real-world organ). Second-order classes point to classes, like zygote (a conceptual cell type) and brain (a conceptual organ type) (Brasileiro et al., 2016). For that reason, alongside the PanglaoDB integration, we improved the modeling of cell types on Wikidata. As of February 2021, the Wikidata database contained 1828 instances of cell type (w.wiki/b2t) and no instances of “cell” (w.wiki/b2q), reducing conceptual disarray.

As a note, by April 2024, the number of instances of “cell type” on Wikidata is much higher (5624), due to subsequent curation efforts, and we were able to clean it to keep it with no instances of “cell.” Of note, the data shown here was generated back in 2020/2021 and represents the state of the platform then.

### Cell markers on Wikidata

Adding marker information on Wikidata was not possible before this study and became possible after community approval of the property has marker (P8872) (see Methods). In Figure 4 we illustrate two of the current markers of “human cholinergic neuron”, CHAT and ACHE, as they are seen on Wikidata. The PanglaoDB is referenced via a URL to the website (panglaodb.se/markers.html) and a pointer to the PanglaoDB item on Wikidata (Q99936939).

![Figure 4.](content/589259v1_fig4.tif)

**Figure 4.:** Two of the current markers of “human cholinergic neuron” (Q101405051) in the Widata interface for web navigation.

Since Wikidata is an open system, user contributions now complement the PanglaoDB information about markers. Until February 2021, however, no other project had systematically integrated cell-type markers into Wikidata, and thus, most of the information shown here comes from PanglaoDB. Tables 1 and 2 show the marker count for the five cell types of humans and mice with the most markers on Wikidata, for both species around two hundred marker genes.

**Table 1:**
 Top 5 Homo sapiens cell types with the most markers on Wikidata (15/02/2021, full query on w.wiki/zoQ).


**Table 2:**
 Top 5 Mus musculus cell types with the most markers on Wikidata (15/02/2021, full query on /w.wiki/zoN).


### Wikidata SPARQL queries enabled by the integration

One of the benefits of our pipeline is the ability to query the data using SPARQL and potentially running federated queries (Martens et al., 2021; Sima et al., 2019). After finishing adding the markers we explored some of these questions, outlined in Figure 5.

![Figure 5:](content/589259v1_fig5.tif)

**Figure 5::** Wikidata SPARQL queries bring to light hidden biomedical knowledge. Blue nodes represent Items on Wikidata and green nodes represent variables in the SPARQL queries. A-C) Graphical representation of feasible SPARQL queries and a sample of their results as of 07/02/2021 (w.wiki/yQ6, /w.wiki/yQD and w.wiki/3Hj).

### Which cell types are related to neurogenesis via cell markers?

To test this first question, we leverage the mapping of Wikidata genes to Gene Ontology terms done by others in the past to get cell types related to the biological process “neurogenesis” (Ashburner et al., 2000; The Gene Ontology Consortium et al., 2023). The query results showed over 55 cell types linked by genes (Fig. 5A) which is illustrated in Figure 6. The results, exemplified in Table 3, show a series of neuron types, such as human Purkinje neuron and human Cajal-Retzius cell. It also retrieved non-neural cell types such as the human loop of Henle cell, a type of kidney cell, and human osteoclast, a type of bone cell.

**Table 3:**
 Sample of 10 cell types related to neurogenesis via markers (07/02/2021, current version on w.wiki/yQ6)


![Figure 6.](content/589259v1_fig6.tif)

**Figure 6.:** Overview of the graph linking cell types (red) and their markers (white) to neurogenesis (blue) as of 08/04/2024. See the current version on w.wiki/9hj2.

These seemingly unrelated cell types markedly express genes involved in neurogenesis, but that of course does not mean that they are involved in this process. As genes play different roles in the body, just because a set of genes plays a role in two biological systems does not mean we can make a direct, mechanistic connection. These results reinforce the need for carefulness when interpreting data based on curated pathways.

### Which cell types express markers associated with Parkinson’s disease?

Besides Gene Ontology, Wikidata has been integrated with sources about diseases, such as the Disease Ontology (Schriml et al., 2021; Waagmeester et al., 2020). This makes Wikidata a spot to quickly investigate links of cell types to particular diseases. The genes linked to diseases (via the genetic association property, P2293) are often compiled from Genome-Wide Association Studies, which look for sequence variation at the overall genomic level. These studies are blind to cell types, and bridging the gap from GWAS to cell types is a topic of research in itself. In Table 4, we can see some cell types marked by genes genetically associated with Parkinson’s disease (PD).

**Table 4:**
 Sample of 5 cell types related to Parkinson’s disease via markers (07/02/2021, current version of query on w.wiki/yQD).


Once more, we have a mix of confirming and surprising results. The relation with human neurons is obviously expected, but we see hits of cells from the immune system and the pancreas. Reassuringly, the immune axis connections to Parkinson’s disease via BST1 are indeed studied in the literature (Yokoyama, 2023).

The SH3GL2 gene. related to Parkinson’s, has not been yet connected to via their role on pancreatic cells to the disease. The gene apparently plays a more direct role, acting on brain synapses (Decet & Soukup, 2023). SH3GL2 is reportedly expressed in pancreatic endocrine cells, but we could not find much information about its role in the organ, as most papers seem to focus on its role in the central nervous system.4 This can signal that this particular link has little biological significance or there is a biological connection to be investigated.

### Which diseases are associated with the markers of pancreatic beta cells?

With the flexibility of SPARQL queries, we can investigate the cell-type-to-disease relation in both ways. One may be interested in particular cell types and which diseases are related to their cell type of interest.

For that, we looked for the diseases linked to human pancreatic beta cells, which play an important role in controlling blood sugar levels (Table 5). Reassuringly, the top hits associated with markers included obesity and type-2 diabetes. Other diseases, such as Parkinson’s, asthma and aniridia - a disturb of the iris of the eye - do not bear a clear link with classic pancreatic functions. Once more, the links may either be spurious or hint at unknown connections, providing seeds for future research.

**Table 5:**
 Top 5 diseases (by number of links) related to human pancreatic beta cells via markers (07/02/2020, full query on https://w.wiki/yQD).


### Disease-drug-gene-cell networks associate rosehip neurons with schizophrenia

For this section, we took inspiration from the work by Lüscher Dias and colleagues on networks containing drugs, diseases, and genes using the now-discontinued Watson Drug Discovery (Dias et al., 2020). We decided to query for similar multi-hop connections on Wikidata now enriched with PanglaoDB, linking cell types and diseases in more elaborate ways.

Complex conditions, like schizophrenia, are not caused by a single gene mutation, and disease progression may be influenced by several cell types. Reasoning that drugs might perturb the cell types expressing their targets, we explored cell types that express markers (1) genetically associated with schizophrenia and, at the same time, markers (2) targeted by drugs used for the disease.

Figure 6A showcases some of the cell types related to schizophrenia via markers and drugs. Purkinje neurons, for example, connect via the marker GRIA3 to the disease, and via the marker GABRA1 to clonazepam, an anti-epileptic drug sometimes used for schizophrenia. Some relations are probably spurious, such as the link between hepatic stellate cells—RELN—and schizophrenia. RELN is expressed independently in the brain and the liver, and it is reasonable to assume that its association with schizophrenia occurs at the brain level (Alexander et al., 2023).

A particular cell type caught our eye: the human-specific, recently discovered rosehip neuron, highlighted in Figure 6B (Boldog et al., 2018). Boldog et al. when describing the cell type highlighted that “several highly selective markers for RCs have been implicated as risk factors for neuropsychiatric disease, including netrin G1 (NTNG1) for Rett syndrome and neurotrypsin (PRSS12) for mental retardation” and even mentioned HRH1 as a marker, but did not make the link to schizophrenia.

![Figure 6.](content/589259v1_fig6a.tif)

**Figure 6.:** A disease-drug-gene-cell network on Wikidata reveals hidden connections of schizophrenia genes (08/04/2024). A. The network relates schizophrenia (orange) to drugs (green) and cell types (blue) via genes (white). A live version is available at this long link. B. A Subset of the graph includes the connection of rosehip neurons to schizophrenia.

A later study comparing transcriptomic markers to genetic markers in schizophrenia pointed to a link between the cell type and the disease (Yu et al., 2021) and a third study used single-cell RNA-seq to look at various populations in the brain, including rosehip neurons, but did not investigate the matter in detail (Ruzicka et al., 2020). Neither, however, seemed to have dedicated much time to investigating the association of rosehip neurons with schizophrenia in detail. Given that rosehip neurons are marked by HRH1 and the histamine H1 receptor is a target of many anti-psychotic drugs, like clozapine (Fell et al., 2012), there is a hint of a role for these cells in the natural history of the disease, or at least in the response to treatment.

The PanglaoDB-enriched Wikidata graph allows us to traverse many types of edges through the biomedical knowledge landscape. The disease-drug-gene-cell graphs showcase the strength of 5-star Linked Open Data for cross-domain integration. We added similar plots in the Supplementary Disease-Drug-Gene-Cell Network Collection, each generated for a different disease by changing a single line of the SPARQL query in Figure 6. As with the other pieces of knowledge here, all edges are backed by references on Wikidata, and thus reliable to some extent. As usual, interpretation should be done carefully.

## Discussion

We hope that the results section has provided the reader with a flavor of what 5-star Linked Open Data and SPARQL queries - particularly on Wikidata - can bring research insights. The contribution detailed here is small, and the actual processing of data and connections took only a couple of months of part-time work. If one is familiar with the Wikidata data model and some basic Python programming, reconciling small datasets is quite straightforward.

As we care about cell types, the Human Cell Atlas, and the rise of the single-cell transcriptomics field, we focused on the PanglaoDB information. While we don’t necessarily expect bioinformaticians to use Wikidata directly - though it is definitely possible - the community curation model provides a way of crowdsourcing cell-type markers for later reuse. The PanglaoDB data is, then, but a seed to grow the structured representation of cell type-gene associations on Wikidata.

We considered writing some R or Python package to connect the PanglaoDB markers on Wikidata to single-cell RNA-seq workflows but eventually gave up on the idea. There are already too many single-cell RNA-seq tools, some even using PanglaoDB (Osorio et al., 2022). If Wikidata indeed becomes a hub for marker genes, then it will find its way into the single-cell RNA-seq workflows. All gene-to-cell-type annotations can be retrieved and reused, and while the technical details werie not discussed in this paper, we demonstrated analogous procedures in the past (Lubiana et al., 2022).

It is important to note that not all data on PanglaoDB was added to Wikidata. Some fine-grained details did not fit a general-purpose knowledge base like Wikidata (e.g., the scores for sensitivity and specificity attached to each marker-cell type pair). If one really wanted to get the additional bits in 5-star Linked Open Data, these parts could be also transformed to RDF format and connected to independent SPARQL endpoints. For reference, similar processes have been done for other datasets by the Bio2RDF effort (Callahan et al., 2013).

One other option for turning PanglaoDB into 5-star linked open data would be using the infrastructure of the OBO Foundry community of ontologies, including the major source for cell type IDs, the Cell Ontology. (Diehl et al., 2016; Jackson et al., 2021) However, the way markers are defined on PanglaoDB is semantically ambiguous, and not very amenable to rigorous ontologization. Also, as the project was a branch of T.L.’s Ph.D. work, done with J.V.F.C., an undergraduate student at the time, we chose the simpler Wikidata to have a straightforward, technically lighter framework. Wikidata makes it extremely easy to mint new identifiers for a scientific concept, by just clicking a few buttons on a web interface, without authorization systems or gatekeeping (Shafee et al., 2023).

As described in the methods session, we added species-specific terms to Wikidata for cell types of Homo sapiens and Mus musculus described in the PanglaoDB database. The use of species-specific cell types is necessary because genes in Wikidata are also species-specific. In the biomedical literature, however, genes and cell types are sometimes referred to broadly, in a multi-species or species-neutral way. These fuzzy ways of human language are not always compatible with formalized data models. Thus, this mapping task is not merely one of picking the right match on Wikidata, but largely of consistent and coherent interpretations of data.

Also, though usage of Wikidata on bioinformatics is limited, its impact on the web is decently sized. Data on Wikidata is commonly reused on Wikipedia, a major source of information for scientists and laypeople alike (Good et al., 2012; Thompson & Hanley, 2017). Moreover, Google, Apple, and several other organizations leverage Wikidata’s graph directly. They value Wikidata’s public domain licensing, reusing data in many automated ways. Thus, though it may be hard to track, adding knowledge to Wikidata certainly influences the information landscape on the web (Pellissier Tanon et al., 2016; Vrandečić et al., 2023).

Of course, Wikidata has its limitations. Concerns with the reliability of Wikipedia are as old as the encyclopedia itself5 and Wikidata shares many of such concerns. The ontological modeling of Wikidata is often far from perfect, and inconsistencies and logical mistakes abound (Brasileiro et al., 2016). While a comprehensive analysis of the pros and cons of scientific Wikidata is not available, we extend Don Fallis’ view on Wikipedia and argue that Wikidata also has a number of “epistemic virtues (e.g., power, speed, and fecundity) that arguably outweigh any deficiency in terms of reliability” (Fallis, 2008).

In summary, this work provides the biomedical community with a semantically accessible, 5-star Linked Open Data dataset of cell markers, adding knowledge from PanglaoDB to Wikidata. The work also provides a blueprint for other databases of cell-type markers, such as CellMarker, labome, CellFinder, and SHOGoiN/CELLPEDIA (Hatano et al., 2011; Stachelscheid et al., 2013; Yakimchuk, 2013; Zhang et al., 2018) in case they want to increase FAIRness even more and integrate their datasets as a 5-star Linked Open Data on Wikidata.
