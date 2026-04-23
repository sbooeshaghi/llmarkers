# Manuscript Compliance Rules for `paper/main.tex`

This document defines rules for generating, editing, and validating `paper/main.tex`.

The goal is not to enforce generic scientific writing rules. The goal is to keep this manuscript internally consistent with its current structure, methods, claims, figures, tables, and audit workflow.

This is version 1. It is intentionally practical. It focuses on rules that are easy to check and that matter for this paper.

## 1. Scope

These rules apply to:

- `paper/main.tex`
- figure captions and table captions in `paper/main.tex`
- claims attached with `\claim{...}{...}` and `\source{...}`
- any text added to Introduction, Results, Discussion, Limitations, Supplementary Material, or Methods

These rules do not yet define:

- journal-specific bibliography style
- line-breaking or TeX typography details
- automated grammar linting thresholds

## 2. Rule Classes

The rules are grouped into five classes:

1. Structure and section coverage
2. Evidence and claim traceability
3. Results and methods separation
4. Style and wording
5. Consistency and terminology

## 3. Structure and Section Coverage

### 3.1 Required top-level sections

`paper/main.tex` must contain these top-level sections, in this order:

1. `Introduction`
2. `Results`
3. `Discussion`
4. `Limitations`
5. `Supplementary Material`
6. `Methods`
7. `Acknowledgements`
8. `Author contributions`
9. `Disclosures`
10. `Claim Sources`

### 3.2 Required Results subsections

The `Results` section must contain these subsections, in this order:

1. `\texttt{LLMarkers} benchmark`
2. `Expert marker curation`
3. `LLM marker curation`
4. `Automated extraction from bioRxiv`
5. `The \texttt{LLMarkersDB}`

If a subsection is renamed, the compliance file must be updated at the same time.

### 3.3 Required Methods subsections

The `Methods` section must contain these subsections, in this order:

1. `Benchmark construction and verification`
2. `Marker strength analysis`
3. `LLM generation and extraction`
4. `bioRxiv`
5. `Gene ID mapping`
6. `Cross-paper cell type analysis`
7. `Data and code availability`

### 3.4 Section purpose rules

Each section has a fixed role.

- `Introduction` explains the problem, why it matters, and what this paper does.
- `Results` states what was found, with numbers.
- `Discussion` interprets the findings.
- `Limitations` states what the paper does not establish.
- `Methods` states what was done, with inputs, outputs, and filtering choices.

Text should not drift across these roles.

## 4. Evidence and Claim Traceability

### 4.1 Quantitative claims must be tagged

Any sentence that introduces a new quantitative result must be wrapped in a `\claim{tag}{...}` and followed by at least one `\source{...}`.

Examples:

- counts
- percentages
- averages
- medians
- F1 scores
- Jaccard values
- costs
- runtimes
- profile counts

### 4.2 Figures and tables must be source-linked

Every figure and table caption must be accompanied by:

- `\claim{...}{}`
- one or more `\source{...}`

### 4.3 One claim, one main result

Each `\claim{...}{...}` should state one main result. Do not pack unrelated numbers into one claim unless they come from one analysis and are interpreted together.

### 4.4 Sources must be primary analysis artifacts

` \source{...}` should point to the analysis artifact that directly generated or verified the claim.

Preferred sources:

- `analysis/*.ipynb`
- `analysis/*.py`
- generated CSV provenance files

Avoid citing a downstream figure file when the notebook is the true source.

### 4.5 Claims must not outrun sources

If a notebook supports a count, the text may report that count. If the notebook does not support the interpretation, the text must soften the interpretation or remove it.

Allowed phrasing when interpretation exceeds direct measurement:

- `This suggests...`
- `This likely reflects...`
- `This is consistent with...`

Disallowed phrasing unless directly shown:

- `This proves...`
- `This demonstrates` followed by a broad causal claim not measured in the source

## 5. Results and Methods Separation

### 5.1 Results must lead with findings

Results paragraphs should usually follow this order:

1. what was measured
2. what was found
3. one short interpretation

Do not lead a Results paragraph with implementation detail unless the paragraph is defining the analysis object.

### 5.2 Methods must define inputs and outputs

Each Methods subsection should state:

- what data it took as input
- what transformation or filtering was applied
- what output object it produced

For example:

- marker records
- DEG-matched marker tables
- paper-level profiles
- mapped Ensembl IDs
- cross-paper Jaccard graph

### 5.3 Avoid duplicate reporting

The same numeric result should not be fully re-stated in both Results and Methods unless Methods needs it to define a filter or dataset.

### 5.4 Benchmark versus bioRxiv must stay separate

The manuscript uses two distinct corpora:

- the seven-study `LLMarkers` benchmark
- the 504-paper bioRxiv extraction corpus

Counts, mappings, costs, and conclusions must be attributed to the correct corpus.

## 6. Style and Wording

### 6.1 Sentence style

Use short declarative sentences.

Prefer:

- `We built...`
- `We extracted...`
- `We found...`
- `This yielded...`

Avoid inflated phrasing such as:

- `leverages`
- `novel paradigm`
- `enables` without saying how
- `robustly` unless a metric is given

### 6.2 Define terms on first use

The first time a technical term appears, define it in plain language.

Examples already used in the manuscript:

- marker genes
- differential expression gene (DEG) table
- generation / selection / extraction
- profile

### 6.3 Prefer concrete nouns over abstractions

Prefer:

- `paper-level profiles`
- `quoted sentence`
- `DEG table`
- `cell type label`

Avoid vague phrases like:

- `information landscape`
- `latent biological signal`
- `knowledge representation framework`

### 6.4 Use explicit contrasts

This manuscript often depends on contrasts. When useful, state them directly:

- binary markers versus quantitative evidence
- expert curation versus LLM generation / selection / extraction
- benchmark versus bioRxiv
- text-derived markers versus image-derived markers
- canonical markers versus study-specific markers

### 6.5 Keep method names stable

Use the same names throughout:

- `generation`
- `selection`
- `extraction`

Do not introduce synonyms such as:

- `retrieval mode`
- `annotation mode`
- `knowledge-only mode`

unless they are explicitly defined.

## 7. Consistency and Terminology

### 7.1 Database and tool names

These names should be written consistently:

- `\texttt{LLMarkers}`
- `\texttt{mrkr}`
- `\texttt{LLMarkersDB}`

### 7.2 Species scope must be explicit

When a result is restricted to human markers, the text must say so.

Examples:

- mapped human markers
- human-only cross-paper analysis
- human benchmark

Do not let a human-only result read as if it applied to all species in the extracted corpus.

### 7.3 Similarity metrics must be named explicitly

Whenever similarity is reported, the metric must be named.

Examples:

- Jaccard similarity
- cosine similarity
- Spearman correlation

Do not write `similarity` alone when the metric matters.

### 7.4 Costs and runtimes need units

Any cost or time claim must include units and scope.

Examples:

- total cost
- cost per paper
- seconds per paper
- total tokens

### 7.5 Numbers must carry context

Raw numbers should usually include at least one of:

- denominator
- percentage
- comparison to a baseline
- dataset or corpus name

Bad:

- `421 papers yielded markers.`

Better:

- `Of the 504 papers, 421 (84\%) yielded at least one marker gene--cell type association.`

## 8. Section-Specific Content Rules

### 8.1 Abstract

The abstract must contain all five of these elements:

1. marker genes are useful but lossy
2. the `LLMarkers` benchmark quantifies that loss
3. LLM generation and DEG selection do not recover study-specific markers well
4. manuscript extraction works better
5. the bioRxiv-scale extraction produced `LLMarkersDB`

The abstract should not introduce details that never appear in Results.

### 8.2 Introduction

The Introduction must bridge from marker-gene history to the LLM problem through a scaling problem:

- markers are useful
- manual curation does not scale
- current automated methods bypass the manuscript
- LLM extraction reads the manuscript directly

### 8.3 Results

Every Results subsection should contain at least one explicit quantitative claim with a source.

The `LLMarkersDB` subsection must describe both search modes:

- free-text profile retrieval
- gene-set retrieval

### 8.4 Methods

Methods should report key filters and exclusions explicitly.

Examples already present in the paper:

- verification by exact substring matching
- mapped human markers only
- profiles with fewer than three markers excluded

## 9. Grammar and Formatting Rules

### 9.1 Basic grammar

The manuscript should avoid:

- subject-verb disagreement
- duplicated words
- undefined abbreviations
- inconsistent capitalization of named tools and datasets

### 9.2 Citations

Historical, biological, or benchmarking claims that are not generated by the paper must have citations.

### 9.3 Footnotes

Footnotes should be used sparingly. They are appropriate when:

- a compact clarification would interrupt the main paragraph
- a citation-backed edge case needs explanation

They should not carry core results.

### 9.4 Parentheticals

Avoid stacking multiple parenthetical clauses in one sentence unless the sentence contains a quantitative result that needs them.

## 10. Validation Checklist

Use this checklist when auditing the manuscript.

### 10.1 Structure

- Are all required sections present and in order?
- Are all required Results and Methods subsections present and in order?

### 10.2 Claims

- Does every new quantitative result have a `\claim` and `\source`?
- Does every figure and table have a source pointer?
- Does each claim point to the primary notebook or provenance file?

### 10.3 Consistency

- Do all counts match the current notebooks?
- Are benchmark and bioRxiv numbers kept separate?
- Are human-only analyses labeled as human-only?
- Are database names and tool names consistent?

### 10.4 Writing

- Do Results paragraphs lead with findings instead of implementation detail?
- Do Methods paragraphs define inputs, transforms, and outputs?
- Are interpretations softer than the evidence when needed?
- Does the prose avoid vague or inflated language?

### 10.5 Search and database content

- Does the `LLMarkersDB` subsection describe the current search behavior accurately?
- Are the number of profiles, corpora, and search modes consistent with `analysis/virtual_cell_mvp.ipynb` and the website implementation?

## 11. Non-goals

This document does not yet define:

- how to score novelty claims
- how to validate external citations automatically
- how to verify every biological interpretation beyond the linked analysis source

Those checks belong in separate audit documents.

## 12. Maintenance Rule

Whenever one of these changes, `compliance.md` should be reviewed in the same edit:

- section layout
- naming of the three LLM modes
- benchmark totals
- bioRxiv totals
- `LLMarkersDB` search behavior
- claim/source macro conventions
