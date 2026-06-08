# Poster Review Cards

Use this as a quick self-review sheet. Each card has the point, what the analysis did, and the answer to give if someone asks why the claim is justified.

## Core Story

### One-Sentence Summary

LLMs can extract marker-gene claims from papers, link them to source evidence, and turn scattered marker reports into a cross-study map that helps reveal when cell type labels behave like stable cell types versus context-dependent cell states.

### Central Problem

Cell type labels are compressed biological claims. A label such as "TREG" or "macrophage" often implies marker genes, assay context, tissue context, and prior knowledge, but the label itself rarely states those assumptions.

**If asked:** The issue is not that labels are bad. They are useful because they are practical, communicable, and testable. The issue is that labels are underspecified when we compare across papers.

### Why Marker Genes Matter

A marker gene is a measured feature that helps identify or distinguish a population of cells. Marker genes give cell type labels experimental meaning.

**Example answer:** A "T cell" label usually implies CD3 and T cell receptor expression. A "regulatory T cell" label usually implies additional markers such as FOXP3 and IL2RA. The label and marker evidence are connected.

### Why Binary Marker Reporting Persists

Binary marker lists are easy to report, remember, test, and reuse. That is why databases and papers use them.

**But:** The same binary format compresses away the comparison, assay, sample, and prior knowledge that made the gene informative.

## Figure 1: Conceptual Problem

### What Figure 1 Shows

Figure 1 is a toy but real-data-motivated representation of the problem. Each node is a reported marker profile from a paper. One graph compares cell type labels. The other compares marker genes. The joint distribution asks whether labels and marker genes agree.

### What Is a Marker Profile?

A marker profile is one paper, one reported cell type label, and a binary set of marker genes.

**Short version:** `(paper, cell type label, marker gene set)`.

### Label Relation

Labels are compared by string relationship.

- Exact: same normalized label.
- Partial: labels share informative tokens.
- Different: labels do not match by this simple rule.

**If asked:** This is intentionally simple. It is not an ontology. It is a first-pass way to expose where names agree or disagree.

### Marker-Gene Relation

Marker genes are compared by Jaccard similarity:

`J = |genes A intersect genes B| / |genes A union genes B|`.

- Exact: `J = 1`.
- Partial: `0 < J < 1`.
- None: `J = 0`.

### Why the Joint Distribution Matters

The table shows the cases atlas builders care about.

- Exact label, exact genes: likely reproducible marker profile.
- Different labels, exact genes: alias, naming drift, granularity difference, or shared state.
- Exact label, partial genes: same name may hide context-specific marker programs.
- Different labels, partial genes: the hardest and often most interesting cases.

**Careful wording:** Marker overlap nominates a relationship. It does not prove two labels are the same cell type.

### What Figure 1 Sets Up

The question is whether we can extract enough marker evidence from papers to study label-marker discordance at scale.

## LLMarkers Dataset

### What LLMarkers Is

LLMarkers is a human-curated benchmark of reported marker genes from seven single-cell RNA-seq papers across six tissues.

Key numbers:

- 2,528 reported marker records.
- 168 cell types.
- 641 Ensembl-mapped genes.
- 1,560 unique cell type-gene pairs.
- 7 papers, 6 tissues.

### Why Build It?

We needed a truth set where each marker was linked to:

- the reported cell type label,
- the marker gene,
- the source sentence or figure,
- the differential expression table/data ID that could support it.

**Short answer:** LLMarkers lets us evaluate whether marker claims can be recovered from the data alone, from LLM prior knowledge, or from manuscript text.

### Source Modality Split

Of 1,560 unique cell type-gene pairs:

- 1,151 are figure-only, 74%.
- 256 are text-only, 16%.
- 153 appear in both, 10%.

**Why this matters:** Text-only extraction can never recover figure-only markers unless the figure content is also processed.

### DEG Table Linkage

The benchmark links reported markers to differential expression gene tables where possible.

Key numbers:

- DEG tables contain 224,084 total entries across 39 supplementary data sources.
- Overlap between curated markers and DEG tables ranges from 18% in bone to 97% in lung.

**If asked:** This shows that some reported markers are not simply entries from a ranked DEG table. They can come from prior knowledge, protein validation, visual inspection, or a different comparison.

## Figure 2: Expert Marker Curation

### What Was Tested?

We asked whether a simple DEG rank cutoff could recover author-reported marker genes.

Procedure:

1. Rank each cell type's DEGs.
2. Treat the top `N` genes as predicted markers.
3. Sweep `N`.
4. Compute precision, recall, and F1 against human-curated reported markers.

### What Is F1?

F1 is the harmonic mean of precision and recall.

`F1 = 2 * precision * recall / (precision + recall)`.

**Interpretation:** A high F1 requires both few false positives and few missed reported markers.

### Main Result

Reported markers are enriched among strong DEGs, but no simple rank threshold recovers them well.

Poster numbers:

- Mean peak F1 for text markers: 0.41.
- Mean peak F1 for image markers: 0.50.

**Short answer:** Differential expression strength helps, but it does not fully explain which markers authors report.

### Why Rank Cutoffs Fail

Authors do not select markers only by rank. They also use prior biological knowledge, known canonical markers, protein-level evidence, visualization, and local context.

**Example:** PDGFRA can be a field-consensus ASPC marker even if it is not differentially expressed across every ASPC subpopulation comparison.

### Important Interpretation

This result motivates LLM extraction. The missing information is in the manuscript and the way authors explain their marker choices, not only in the DEG ranking.

## Figure 3: LLM Marker Curation

### The Three LLM Tasks

Generation: The LLM receives cell type names and proposes marker genes from prior knowledge.

Selection: The LLM receives ranked DEG tables and chooses markers from the provided genes.

Extraction: The LLM reads manuscript text and extracts the marker claims authors actually made.

Extraction + data linkage: The LLM must also recover the supporting DEG data ID.

### Why These Tasks Are Ordered

They differ by how much study-specific context the model sees.

- Generation sees no study-specific data.
- Selection sees the DEG data but not the text.
- Extraction sees the text where authors state the claim.
- Data linkage asks whether the extracted claim can be tied back to the supporting comparison.

### Main Result

Extraction works best because marker claims are made in text.

Poster phrasing:

- Generation F1 is low because it produces plausible canonical markers, not necessarily the paper's markers.
- Selection F1 is low because DEG tables alone omit the manuscript reasoning.
- Extraction performs best because it recovers what the paper actually reports.

### Exact Numbers to Remember

From the current figure summary:

- Generation mean pair F1: about 0.16.
- Selection mean pair F1: about 0.16.
- Extraction mean pair F1: about 0.65.
- Extraction + data source mean F1: about 0.57.

From the manuscript table snapshot:

- Extraction mean pair F1: 0.69.
- Extraction + data source mean F1: 0.60.

**Talk track:** The exact rounded value depends on the evaluation snapshot, but the result is stable: extraction is far better than generation or selection, and data linkage remains harder but still feasible.

### Why Generation Does Poorly

The model knows broad marker associations from the literature, but it does not know the local partition used in a specific paper.

**Example answer:** It may know common T cell markers, but not which marker list an author used for a specific T cell subtype in a specific atlas.

### Why Selection Does Poorly

Selection has access to ranked DEGs, but not the author's text. It therefore cannot know which DEGs the authors chose to report, validate, or interpret.

**Short answer:** The data alone are not the paper's claim.

### Why Extraction Is the Right Task

Extraction starts from the claim authors made. It can then verify the source sentence and optionally link the claim back to the supporting data table.

**If asked about hallucination:** We verify source text by exact matching and check whether both the cell type label and gene label appear in the extracted sentence.

## Large-Scale Extraction

### What Corpus Was Used?

We ran `mrkr` extraction on:

- 504 bioRxiv preprints.
- 434 HCA-linked publications.

Together, `mrkr` extracted 32,621 marker associations from 855 papers with non-empty marker output.

### Why 855 Papers If 504 + 434 = 938?

938 is the input set shown on the poster table. 855 is the number of papers with non-empty marker associations.

**Short answer:** Some input papers yielded no extracted marker records.

### Filtering for Cross-Study Analysis

For cross-study analysis we kept records that were:

- verified against source text,
- human,
- mapped to Ensembl gene IDs,
- deduplicated within each paper,
- part of a profile with at least three marker genes.

### Analysis-Ready Corpus Numbers

After filtering:

- 24,139 analysis-ready marker records.
- 3,351 analyzed profiles.
- bioRxiv: 7,153 records and 954 profiles.
- HCA: 16,986 records and 2,397 profiles.

### Human Versus Non-Human Profiles

Before the final human Ensembl-ID analysis filter, verified profiles with at least three marker names were:

- bioRxiv: 1,015 human, 420 non-human.
- HCA: 2,443 human, 97 non-human.
- Total: 3,458 human, 517 non-human.

**Why this matters:** The extraction tool can find non-human markers, but the cross-study gene-ID analysis is restricted to human Ensembl IDs.

### Why Ensembl IDs?

Gene symbols have aliases and ambiguity. Ensembl IDs give a stable representation for Jaccard comparisons.

**Example:** Protein labels such as PD-1, TIM-3, or CD25 need to map to their corresponding gene IDs when possible.

## Figure 4A: Corpus-Level Joint Distribution

### What Was Computed?

All cross-paper profile pairs were compared by:

- label relation: exact, partial, or different;
- marker relation: exact Jaccard, partial Jaccard, or none.

### Main Numbers

Most cross-paper pairs are unrelated:

- Different labels, no shared genes: 5,443,977 pairs, 97.3%.

Informative cases:

- Exact label, partial genes: 2,403 pairs.
- Different labels, partial genes: 102,369 pairs.
- Different labels, exact genes: 76 pairs.

**Short answer:** The rare bins are the interesting ones because they expose label-marker discordance.

### How to Explain the Partial Column

The partial marker-overlap column contains the cases where profiles are related but not identical. These are the cases most likely to reveal subtype, state, tissue, disease, assay, or comparison effects.

## Figure 4B: Nearest-Neighbor Ties

### What Are Marker Neighbors?

For each profile, marker neighbors are profiles from other papers with the most similar marker-gene sets.

### What Are Label Neighbors?

For each profile, label neighbors are profiles from other papers with the most similar reported labels.

### Main Marker-Neighbor Result

Among top marker-neighbor ties:

- 85.7% have different labels.
- 8.9% have partially matching labels.
- 5.4% have exact matching labels.

**Interpretation:** Marker genes often connect profiles that are not named the same way.

### Main Label-Neighbor Result

Among top label-neighbor ties:

- 0.17% have exact marker agreement.
- 19.0% have partial marker overlap.
- 80.9% have no shared marker genes.

**Interpretation:** Similar names often do not guarantee similar marker profiles.

### Clean Answer

Labels and marker genes are related views of the same biology, but they are not interchangeable.

## Figure 4C: Neighborhood Overlap

### What Was Measured?

For each profile, compare its top 10 marker-gene neighbors to its top 10 label neighbors.

### Main Result

The observed overlap is 7.1% on average, compared with 0.31% for a random cross-paper baseline.

### Interpretation

The label space and marker-gene space are more concordant than random, but still very different.

**Short answer:** Labels contain biological information, but marker genes add a distinct signal.

## Figure 4D/E: Coherence of Labels and Marker Groups

### What Is a Silhouette Score?

A silhouette score measures whether items are closer to their own group than to other groups.

Range:

- Positive: group is coherent.
- Near zero: weak or overlapping structure.
- Negative: group may be less coherent than alternatives.

### Label-to-Marker Analysis

For each exact cell type label, we asked whether profiles with that label group together in marker-gene space.

Key examples:

- "T cell": 38 profiles, mean silhouette -0.015.
- "TREG": 15 profiles, mean silhouette 0.006.

**Interpretation:** These labels are frequent but not clean marker-defined groups.

### Marker-to-Label Analysis

For each marker-gene cluster, we asked whether its profiles group coherently by label tokens.

Key example:

- TREG-enriched marker cluster: 56 profiles, 39 papers, 45 reported labels, label silhouette -0.022.

**Interpretation:** A marker-defined immune program can cut across many reported names.

## Figure 4F: Coverage, Purity, and Gene F1

### Why This Analysis Exists

We want a practical way to ask whether a gene behaves like a stable cell type marker or a context-dependent state marker.

### Coverage

Coverage asks:

`P(gene is reported | group)`.

**Plain English:** Among profiles in this group, how often does the gene appear?

### Purity

Purity asks:

`P(group | gene is reported)`.

**Plain English:** Among all profiles that report this gene, how often do they belong to this group?

### Gene F1

Gene F1 is the harmonic mean of coverage and purity.

**Interpretation:** A gene gets a high score only if it appears often within a group and is relatively specific to that group.

### Why Compare Label-Defined and Marker-Defined Groups?

If a gene is strong in the label-defined group and in the marker-defined group, it behaves like a stable marker for that cell type.

If a gene is weak in the label-defined group but strong in the marker-defined group, it may mark a state program that crosses labels.

### TREG Example

FOXP3 has balanced support in both views, consistent with a stable regulatory T-cell feature.

HAVCR2, LAG3, and PDCD1 are stronger in the marker-defined cluster than in the TREG label group, consistent with a checkpoint/exhaustion-like state program that crosses reported labels.

**Careful wording:** These are putative classifications from literature-derived marker profiles, not final biological validation.

## Specific Biological Examples

### Monocyte Example

Monocyte-containing profiles show label reuse across contexts.

Key number:

- 29 bioRxiv preprints.
- Mean pairwise marker Jaccard: 0.063.
- Median pairwise marker Jaccard: 0.

**Interpretation:** The word "monocyte" is used across different tissues, diseases, assays, and comparisons, each with different reported marker programs.

### Naive-Like TREG Example

A liver cancer study used CCR7, LEF1, SELL, and TCF7 as well-defined naive T cell markers.

The marker graph connected that profile to a "Treg.1" profile from a lung cancer study with the same genes.

The source text described "Treg.1" as having elevated expression of naive markers.

**Interpretation:** This is not a merge between naive T cells and regulatory T cells. It is evidence for a naive-like state program within a regulatory T-cell subtype.

### Macrophage Example

Two papers both reported macrophage profiles and shared broad macrophage genes such as CD14 and FCGR3A, but differed in the remaining genes.

- C1QB points toward complement macrophage programs.
- VCAN points toward inflammatory monocyte-like programs.

**Interpretation:** The shared label supports broad macrophage relatedness, but nonshared markers show why the label alone is not enough.

## LLMarkersDB

### What Is It?

LLMarkersDB is a searchable database of marker profiles, source text, labels, and mapped genes.

### How Search Works

Text search:

- Source sentences and paper context are embedded with `sentence-transformers/all-MiniLM-L6-v2`.
- Queries retrieve profiles by cosine similarity.

Gene search:

- Profiles store Ensembl gene IDs.
- Gene sets can be compared by Jaccard similarity.

### Why It Matters

An AI agent or researcher can ask for a cell type or gene set and retrieve provenance-linked marker profiles, not just an unsupported marker list.

## Common Questions

### How Did You Pick the Figure 1 Toy Examples?

The examples were chosen manually to make the ambiguity modes visible in a small, readable figure. They are not meant to estimate frequencies. The corpus-level frequencies are shown later in Figure 4A.

**Short answer:** Figure 1 is a conceptual map using real marker-profile patterns. It deliberately includes examples spanning same label/same genes, same label/different genes, different labels/shared genes, and partial overlap.

### Why Is One Figure 1 Cell Type "CD4-C2-KLF2" or "CD8-C2-KLF2"?

That is intentionally a weird example. It shows a marker-defined naming convention where the marker gene becomes part of the reported cell type label.

**Talk track:** I included it because it makes the label-marker coupling explicit. The label is not a classical cell type name; it is a cluster-style label that encodes KLF2. That is exactly the kind of nomenclature problem we are trying to make machine-readable.

**Careful wording:** I would not present KLF2 as the biological center of the story. It is an illustrative naming case.

### Were the Figure 1 Examples Selected to Be Biologically Important?

Not all of them. Some were selected because they are biologically interpretable, such as regulatory T cell and exhausted T cell markers. Others were selected because they expose a reporting pattern, such as marker-defined labels.

**Safe answer:** Figure 1 motivates the representational problem. The biological claims come from the scaled corpus analysis and reviewed examples.

### Why Does the Bone Dataset Have Low DEG Overlap?

The bone dataset has low overlap because many curated markers, especially image-derived markers, do not appear in the specific DEG tables we parsed and linked.

Key table values:

- Bone overall: 370 curated pairs.
- Text: 98 pairs, 53% found in DEG tables.
- Image: 309 pairs, 13% found in DEG tables.
- Overall overlap is therefore low, about 18%.

**Interpretation:** This does not mean the bone markers are wrong or not biologically meaningful. It means many reported markers were not recoverable from the available linked DEG tables under our exact matching rules.

### Why Would Some Papers Have Better DEG Overlap Than Others?

DEG overlap depends on how the paper reports markers and how its supplementary tables are structured.

High overlap happens when the paper reports markers directly from accessible DEG tables using matching cell type and gene labels.

Low overlap happens when markers are:

- shown mostly in figures,
- drawn from known marker panels,
- validated by protein staining or prior knowledge,
- described with labels that do not exactly match the DEG table labels,
- tied to a comparison not present in the parsed DEG files.

**Safe answer:** The variation is itself part of the result. Marker reporting is not standardized across papers.

### Did You Test the Reverse Generation Task?

Yes. In the generation analysis, we also tested whether the model could infer the cell type label from anonymized gene lists.

The strict exact-label prediction accuracy was low:

- Mean prediction accuracy: 15%.
- Lung was highest at 40%.
- Bone was lowest at 4%.

**Takeaway:** LLMs know broad marker-cell type associations, but exact paper-specific cell type labels are hard. This supports the main argument that labels are local and underspecified.

### Why Is Reverse Label Prediction So Low?

The evaluation is strict. The model has to recover the reported label, not just a plausible broad cell type.

**Example answer:** If a gene list suggests a T cell state, the model may answer "T cell" or "memory T cell" while the paper reports a study-specific label. That is biologically close but counted as wrong under exact evaluation.

**Interpretation:** This is not a failure of biological knowledge. It shows that paper-specific nomenclature is not recoverable from genes alone.

### What Did the LLM Tasks Cost?

Average cost per paper:

- Generation: $0.33 per paper.
- Selection: $0.85 per paper.
- Extraction: $0.54 per paper.

Total cost across seven benchmark papers:

- Generation: $2.30.
- Selection: $5.94.
- Extraction: $3.77.

**Talk track:** Generation was cheapest but least grounded. Selection was most expensive and did not improve performance. Extraction was intermediate in cost and best matched the paper's reported claims.

### Why Was Selection More Expensive?

Selection was run across ranked DEG inputs and top-N settings. It also sends larger structured gene lists to the model than generation.

**Short answer:** Selection gives the model more data, but that data alone did not contain enough information to recover the author's reported markers.

### How Were Label Neighbors Defined?

Each profile has a normalized cell type label. Labels were compared with a simple string/token similarity:

- exact match gets similarity 1.0;
- substring containment gets similarity 0.75;
- otherwise, similarity is token Jaccard after removing generic words like "cell", "cells", "cluster", and "population";
- no shared informative tokens gets 0.

For each profile, label neighbors are profiles from other papers with the highest label similarity.

**Careful wording:** This is intentionally not an ontology. It is a transparent string baseline.

### How Were Marker Neighbors Defined?

Each profile is encoded as a binary vector of Ensembl gene IDs. Marker similarity is Jaccard similarity between the two gene sets:

`J = |genes A intersect genes B| / |genes A union genes B|`.

For each profile, marker neighbors are profiles from other papers with the highest nonzero marker-gene Jaccard similarity.

**Important detail:** Comparisons are cross-paper. We avoid interpreting same-paper duplicated or related profiles as cross-study evidence.

### Why Compare Label Neighbors and Marker Neighbors?

This asks whether names and genes point to the same nearby profiles.

**Result:** They overlap more than random, but weakly. The top 10 marker-gene neighbors overlap the top 10 label neighbors by 7.1% on average, compared with 0.31% for random cross-paper neighbors.

**Interpretation:** Labels and marker genes both carry biological signal, but each misses relationships captured by the other.

### What Do the Colors Mean in the Final Coverage-Purity Panel?

The final panel compares each gene's F1 score in a label-defined group versus a matched marker-defined cluster.

Axes:

- x-axis: F1 in the label group.
- y-axis: F1 in the marker cluster.

Colors are heuristic regions:

- Blue, shared high F1: strong in both the label group and marker cluster. Candidate stable cell type marker.
- Green, marker-cluster enriched: stronger in the marker cluster than in the label group. Candidate state or context program crossing labels.
- Orange, label enriched: stronger in the label group than in the marker cluster. Candidate label-specific marker or marker-cluster mismatch.
- Gray, weak in both: not strongly informative in either view.

**Careful wording:** The colors are interpretive guides, not definitive biological classes.

### How Should I Explain FOXP3 Versus PDCD1/HAVCR2/LAG3?

FOXP3 has balanced support in both TREG-labeled profiles and the matched marker-defined cluster, so it behaves like a stable regulatory T-cell feature in this analysis.

PDCD1, HAVCR2, and LAG3 are stronger in the marker-defined cluster than in the TREG label group, so they behave more like a checkpoint/exhaustion-like state program that cuts across reported labels.

**Safe answer:** This is a nomination from literature-derived marker profiles, not a final validated cell-state taxonomy.

### Are You Saying Marker Genes Are Bad?

No. Marker genes are useful because they compress complex data into a practical, testable form. The point is that the compression is lossy, especially across studies.

### Are You Replacing Ontologies?

No. Ontologies standardize names. This work adds evidence underneath the names: which genes, from which paper, in which context, and from which comparison.

### Does Marker Overlap Prove Two Cell Types Are the Same?

No. Marker overlap nominates a relationship. Source text and biological context are needed to interpret that relationship.

### Why Not Just Reanalyze the Matrices?

Reanalysis is ideal when the data are available and comparable. But many marker claims are distributed across papers, figures, text, and supplementary tables. This work builds a literature-scale index of those claims.

### Why LLMs?

Because marker claims are written in language. LLMs can recover the sentences where authors name cell types, list markers, and explain the claim. DEG tables alone do not contain that narrative context.

### What Is the Biggest Limitation?

Large-scale extraction is text-only. It misses figure-only markers and does not fully link every extracted marker to the original DEG table across the large corpus.

### What Is the Safest Claim?

LLM extraction can create provenance-linked marker profiles at scale, and those profiles reveal label-marker discordance that can be used to nominate candidate cell type versus cell state distinctions.

### What Is the Risky Claim?

Saying that the method definitively resolves cell type versus cell state. It does not. It provides a prototype and candidate relationships that need biological review and validation.

## Numbers to Memorize

- LLMarkers: 2,528 reported marker records.
- LLMarkers: 168 cell types.
- LLMarkers: 641 Ensembl-mapped genes.
- LLMarkers: 1,560 unique cell type-gene pairs.
- Figure-only marker pairs: 74%.
- Text-only marker pairs: 16%.
- Both text and figure: 10%.
- Rank-cutoff peak F1: 0.41 text, 0.50 image.
- Large corpus inputs: 504 bioRxiv, 434 HCA-linked.
- Raw extracted marker associations: 32,621 from 855 non-empty papers.
- Analysis-ready marker records: 24,139.
- Analyzed profiles: 3,351.
- Different label, no shared marker genes: 97.3% of cross-paper pairs.
- Different labels, partial marker overlap: 102,369 pairs.
- Different labels, exact marker profiles: 76 pairs.
- Top marker-neighbor ties with different labels: 85.7%.
- Top label-neighbor ties with no shared marker genes: 80.9%.
- Top 10 marker-label neighborhood overlap: 7.1% observed versus 0.31% random.

## Short Closing Answer

The paper is not just about extracting markers. The extraction creates a machine-readable, provenance-linked marker corpus. Once markers are represented as paper-level gene profiles, we can compare them across studies and ask where labels and marker evidence agree or disagree. That gives a practical way to nominate stable cell type markers and context-dependent state markers from the literature.
