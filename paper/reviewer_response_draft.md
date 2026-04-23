# Point-by-Point Responses

## Point 1
**Critique:** ("In single-cell biology, marker genes serve as shorthand for cell identity") this already brings into question what a marker gene is. Some marker genes serve as shorthand (CD4, CD8, CD69) but others are simply DE.

**Response:**
I agree. This is, in part, addressed in another paper where we point out that a DE gene is not a marker gene (https://www.biorxiv.org/content/10.1101/2022.05.06.490859v1.full). This paper also addresses this point, indirectly, by disentangling the two (deg selection from marker curation result).

## Point 2
**Critique:** ("By saying gene X marks cell type Y") who says this? Usually you hear "marker x is used for cell type y" or "x is a marker of Y." This may sound syntactic, but it is an important subtlety, especially since the next sentences critique this view and motivate the study based on "compression."

**Response:**
I agree that sentence structure implies different information about the gene-cell type relationship. "X is a marker of Y" implies a stronger, canonical claim (context-independent specificity), while "X marks Y" is more associative and less specific. But this is also part of the point of the paper: language compresses meaning. In any case, I changed the phrasing to "gene X is a marker for cell type Y" because I agree many biologists communicate markers specifically in this way.

## Point 3
**Critique:** ("This format is useful but lossy") this is accurate, but reads somewhat straw-man. Some people use shorthand, but others provide detailed context and quantitative evidence.

**Response:**
There is wide variance in how markers are presented (and some papers are specifically about establishing a novel marker). But even with careful reporting, markers are often reduced to binary pairs. My point is that this binary reduction delinks markers from context.

## Point 3 (abstract framing)
**Critique:** ("To quantify the impact this compression has on marker curation,") in abstract/introduction, briefly define traditional marker use, then explain why this can be lossy in modern scRNA-seq.

**Response:**
Great suggestion. I rewrote the beginning of the abstract to improve this setup and framing.

## Point 4
**Critique:** ("Cell types were first identified with low-resolution microscopy") ref?

**Response:**
I added a reference and sentence on Theodor Schwann's work (first identification of glial cells / early cell-type identification).

## Point 5
**Critique:** corresponding author detail: use one symbol and write "*to whom correspondence should be addressed: sinab@berkeley.edu, astreets@berkeley.edu"

**Response:**
I am not fully sure of the cleanest LaTeX formatting, but I will try to make this exact format work. If not, I may keep the current format.

## Point 6
**Critique:** ("Single-cell RNA sequencing changed how markers") intro is good, but historically much happened between the previous paragraph and scRNA-seq (multicolor flow, CD classification, etc).

**Response:**
Agreed. For this paper, I think the current historical scope is sufficient because it maps directly to the binary-vs-quantitative marker framing, but I agree this broader history is true.

## Point 7
**Critique:** ("identified by ranking genes") this should be ranking by differential abundance (fold change + significance), not absolute expression.

**Response:**
Fixed. Sentence now states differential abundance.

## Point 8
**Critique:** ("Their simplicity also enables automated extraction and curation...") another practical use is annotating clusters in large-scale scRNA-seq.

**Response:**
Agreed. I added a sentence and citation to CellTypist for this use case.

## Point 9
**Critique:** ("The second profiled preadipocytes with SCRB-Seq") differentiating preadipocytes.

**Response:**
Updated to "differentiating preadipocytes."

## Point 10
**Critique:** ("FACS-measured in vitro ... in vivo states measured by scRNA-seq") how are in vitro/in vivo being used here? both are generally in vitro measurements.

**Response:**
Agreed. I clarified this point as a modality mismatch (surface-protein-based definitions vs RNA-based states), not in vitro vs in vivo.

## Point 11
**Critique:** ("CD4+ T cells, classically defined as helpers, have been shown to be cytotoxic") this seems more like discovery of unexpected biology than failure of binary marker classification.

**Response:**
I agree. I switched to a better framing/reference context: cytotoxic CD4 subsets can be defined with cell-surface protein markers and functional assays, and RNA-only identification can remain challenging. I updated this section and references accordingly.

## Point 12
**Critique:** ("annotating cell types from DEG lists bypasses the manuscript...") important point but not clearly written.

**Response:**
Agreed. Rewritten as: "However, by solely relying on the DEG table to annotate cell types, LLMs ignore the manuscript and the specific markers that the authors---the domain experts---chose to report."

## Point 13
**Critique:** ("LLMs substantially outperform traditional annotation tools across 34 datasets") "outperform" is unclear in context.

**Response:**
I kept "outperform" as a quote from the source and clarified this in the manuscript with quotation marks plus context about the evaluation from the cited paper.

## Point 14
**Critique:** ("LLMs can instead engage with the authors' own claims...") is this established work or your proposal? It reads novel.

**Response:**
This is my proposed idea. I updated the text to make novelty explicit: "We propose an alternative approach..."

## Point 15
**Critique:** ("extraction mode") term of art or coined term?

**Response:**
I do not think this usage is unusual, but I agree it should be clearly defined in context, which I think it currently is.

## Point 16
**Critique:** ("In this study, we investigate marker genes reported...") transition is important; the intro should more directly build to explicit study questions and how they are answered.

**Response:**
I agree this is important. I do not yet have the best wording, and I will think this through further and revise the transition.

## Point 17
**Critique:** ("Our results show authors report strong marker genes") what does strong mean? consistent, or high fold-change?

**Response:**
Strong here means low rank / high differential abundance in the DEG table (LFC-based). I updated the text to clarify this.

## Point 18
**Critique:** ("drawn from a broader range of gene strengths...") unclear if term-of-art or new phrase.

**Response:**
I clarified this explicitly: generated and selected markers are drawn from a broader range of DEGs by LFC (i.e., not concentrated at the top the way author-reported markers are naively expected to be).

## Point 19
**Critique:** ("similar signatures despite different names") this may be one of the most important results.

**Response:**
Yes, this is a major result.

## Things I need to do

1. Tighten transition to end off the introduction, so the intro builds to the question being answered.
2. For Point 5, finalize one shared correspondence footnote if latex formatting cooperates.
