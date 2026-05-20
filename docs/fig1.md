# Figure specification: paper-celltype joint analysis

A three-panel figure showing how marker-gene annotations from multiple papers can be compared along two independent axes (celltype label, marker gene set) and summarized as a joint interpretation map.

The target rendering is a single horizontal figure with three panels side by side: a paper-marker profile table on the left, the two-graph decomposition in the middle, and the joint interpretation map on the right. The implementer is expected to use LaTeX with TikZ. The right panel should not show empirical corpus counts in Figure 1; it should explain how combinations of label similarity and marker-gene similarity motivate later context-aware resolution analyses.

## Current real-data instance

The manuscript figure uses selected real T-cell examples from the extracted marker corpus. Profiles were built from verified human marker records with mapped Ensembl gene IDs, then deduplicated by `(paper, cell type, gene ID)`. The goal is not to enumerate all corpus relationships. The goal is to show that paper-marker profiles can occupy different cells of the label-by-gene relation map.

| Paper label | Citation | Paper key | Cell type | Display | Marker genes shown | Relation highlighted |
|-------------|----------|-----------|-----------|---------|--------------------|----------------------|
| Sade-Feldman 2018 | `SadeFeldman2018` | `manual:melanoma_t_cell_exhaustion_2019` | CD8_B | B | CD38, ENTPD1, BATF, PTPN6; +4 shared | partial label, partial genes |
| Wu 2026 | `Wu2026` | `manual:revitalizing_t_cells_exhaustion_2025` | exhausted T cells | EX | TIGIT, PRDM1, TBX21, EOMES, IL2RB, IL7R; +4 shared | partial label, partial genes |
| Krishna 2021 | `Krishna2021ccrcc` | `hca:10.1016/j.ccell.2021.03.007` | CD8A+ Exhausted | KE | TOX; +3 shared | partial label, partial genes |
| Wu 2026 | `Wu2026` | `manual:revitalizing_t_cells_exhaustion_2025` | regulatory T cells | R4 | CD39, CD73 | exact label, none genes |
| Schafflick 2020 | `Schafflick2020ms` | `hca:10.1038/s41467-019-14118-w` | regulatory T cells | R1 | FOXP3, CTLA4 | exact label, strict genes |
| Dominguez Conde 2022 | `Dominguez2022celltypist` | `hca:10.1126/science.abl5197` | regulatory T cells | R2 | FOXP3, CTLA4 | exact label, strict genes |
| Egozi 2023 | `Egozi2023nec` | `hca:10.1371/journal.pbio.3002124` | regulatory T cells | R3 | SELL, CCR7, SOCS1, TIGIT, ICOS, TNFRSF4, IL2RA; +1 shared | exact label, partial genes |
| Lopez-Cobo 2024 | `LopezCobo2024` | `manual:car_t_suv39h1_solid_tumor_2023` | CD4-C2-KLF2 | K4 | KLF2 | partial label, strict genes |
| Lopez-Cobo 2024 | `LopezCobo2024` | `manual:car_t_suv39h1_solid_tumor_2023` | CD8-C2-KLF2 | K8 | KLF2 | partial label, strict genes |

Label relations in this compact example are derived from normalized label strings. The regulatory T-cell profiles are exact label matches. Krishna CD8A+ Exhausted and Wu exhausted T-cell profiles are connected because `Exh.` is normalized to exhausted. Sade-Feldman CD8_B, Krishna CD8A+ Exhausted, and Lopez-Cobo CD8-C2-KLF2 are connected through the shared CD8 token. The CD4-C2-KLF2 and CD8-C2-KLF2 profiles are connected because they share the reported C2-KLF2 program string. Gene relations are computed on full deduplicated mapped marker profiles. The table abbreviates some full profiles by showing distinguishing genes and collapsing shared genes as `+n shared`. Marker graph edge widths scale with the Jaccard similarity between the full mapped marker sets.

Full-profile marker-graph Jaccard values:

| Pair | Shared genes | Jaccard | Joint cell |
|------|--------------|---------|------------|
| R1--R2 | FOXP3, CTLA4 | 1.00 | exact label, strict genes |
| R1--R3 | CTLA4 | 0.11 | exact label, partial genes |
| R2--R3 | CTLA4 | 0.11 | exact label, partial genes |
| R1--R4 | none | 0.00 | exact label, none genes |
| R2--R4 | none | 0.00 | exact label, none genes |
| R3--R4 | none | 0.00 | exact label, none genes |
| R1--B | CTLA4 | 0.11 | different label, partial genes |
| R1--EX | CTLA4 | 0.09 | different label, partial genes |
| R2--B | CTLA4 | 0.11 | different label, partial genes |
| R2--EX | CTLA4 | 0.09 | different label, partial genes |
| R3--B | CTLA4 | 0.07 | different label, partial genes |
| R3--EX | CTLA4, TIGIT | 0.12 | different label, partial genes |
| R4--B | CD39/ENTPD1 | 0.11 | different label, partial genes |
| B--EX | PDCD1, HAVCR2, LAG3, CTLA4 | 0.29 | different label, partial genes |
| B--KE | PDCD1, HAVCR2, LAG3 | 0.33 | partial label, partial genes |
| KE--EX | PDCD1, HAVCR2, LAG3 | 0.27 | partial label, partial genes |
| K4--K8 | KLF2 | 1.00 | partial label, strict genes |
| B--K8 | none | 0.00 | partial label, none genes |
| KE--K8 | none | 0.00 | partial label, none genes |

The example highlights the main ambiguity classes we want the reader to carry forward. The same regulatory T-cell label can recover the same marker profile across papers, can point to a partially overlapping disease-specific neonatal intestine profile, or can point to a disjoint CD39/CD73 profile in an exhaustion review. A single marker program can appear under related CD4 and CD8 CAR-T subset labels. Exhaustion-associated profiles can have different names and tissue or treatment contexts but still share canonical exhaustion markers. These cases motivate a corpus-level analysis that separates exact label agreement from marker-gene-set agreement.

The Figure 1 matrix displays measured label-marker relationships and a conservative three-class triage:

|                 | strict gene (`J=1`) | partial gene (`0<J<1`) | none gene (`J=0`) |
|-----------------|---------------------|-------------------------|-------------------|
| **exact label** | likely same cell type | context clarifies cell type vs. state | context clarifies cell type vs. state |
| **partial label** | context clarifies cell type vs. state | context clarifies cell type vs. state | context clarifies cell type vs. state |
| **different label** | context clarifies cell type vs. state | context clarifies cell type vs. state | likely different cell type |

## 1. Conceptual model

### 1.1 Data unit

The atomic unit is a *highlight*: a tuple `(paper_id, celltype_label, gene)` indicating that a paper annotated a gene as a marker for a celltype. Highlights are aggregated by `(paper_id, celltype_label)` into a **PCT node** (paper-celltype). Each PCT node carries:

- a paper identifier (e.g., `P1`)
- a celltype label string (e.g., `Proximal tubule`)
- a marker gene set (e.g., `{SLC34A1, LRP2, GATM, SLC22A6}`)

Multiple PCT nodes from the same paper are allowed (one paper annotates multiple celltypes). Multiple PCT nodes can share a celltype label across papers (the central comparison case).

### 1.2 Two pairwise relations

For any unordered pair of PCT nodes `(A, B)`, two independent relations are computed.

**Label relation.** Compares the celltype label strings.
- *strict* (also called *exact*): `A.label == B.label` after normalization.
- *partial* (also called *similar*): the labels are not equal but are mapped to the same group by an external similarity rule (e.g., a Cell Ontology mapping, or a curated synonym table). In the toy data, `{Proximal tubule, PT cell}` is the only similar-label group.
- *none* (also called *different*): neither strict nor partial.

**Gene-set relation.** Compares the marker gene sets `G_A` and `G_B`.
- *strict* (also called *J=1*): `G_A == G_B`, equivalently Jaccard index = 1.
- *partial* (`0 < J < 1`): the sets share at least one gene but are not equal. Two sub-cases are tracked but visualized as one tier:
  - *subset*: `G_A ⊂ G_B` or `G_B ⊂ G_A` (proper subset).
  - *generic partial*: overlap exists but neither is a subset of the other.
- *none* (also called *J=0*): the sets are disjoint.

The two relations are independent: a pair can have any combination of (label relation, gene relation), giving a 3×3 joint distribution.

### 1.3 Two graphs

Over the same PCT node set, define:

- **Label graph.** Edge between `A` and `B` iff their label relation is strict or partial.
- **Gene graph.** Edge between `A` and `B` iff their gene relation is strict or partial.

The two graphs share node positions in the figure (this is the load-bearing design choice — see §3.2). The joint distribution heatmap is the cross-tabulation of edge presence/strength across the two graphs.

### 1.4 Visual encoding convention (used uniformly across panels)

| Tier | Color | Style | Meaning in label graph | Meaning in gene graph |
|------|-------|-------|------------------------|------------------------|
| strict | teal `#1D9E75` | solid, 2.5pt | exact label match | `J = 1` |
| partial | amber `#BA7517` | dashed (6,3), 2.2pt | similar label | `0 < J < 1` |
| none | gray | no edge | different label | disjoint genes |

Subset is a *property* of a partial gene edge, marked with a small `⊂` glyph at the edge midpoint inside a white-filled circle of radius 9pt. It is not a separate color or style.

## 2. Toy dataset

8 PCT nodes from 4 papers. The dataset is constructed so that 7 of the 9 cells of the joint distribution are non-empty, including the scientifically interesting off-diagonal cases.

| Node ID | Paper | Celltype label | Gene set | Label group |
|---------|-------|----------------|----------|-------------|
| P1.PT   | P1 | Proximal tubule | SLC34A1, LRP2, GATM, SLC22A6 | A |
| P2.PT   | P2 | Proximal tubule | SLC34A1, LRP2, GATM, SLC22A6 | A |
| P3.PT   | P3 | Proximal tubule | SLC34A1, LRP2 | A |
| P4.PTc  | P4 | PT cell | SLC34A1, LRP2, GATM, SLC22A6 | A' |
| P1.DT   | P1 | Distal tubule | SLC12A3, CALB1 | B |
| P2.DT   | P2 | Distal tubule | SLC12A3, KCNJ1, CLCNKB | B |
| P3.DT   | P3 | Distal tubule | UMOD, CLDN16 | B |
| P4.Pod  | P4 | Podocyte | NPHS1, NPHS2, WT1 | C |

Label groups: `{A, A'}` are similar to each other (PT ↔ PT cell); `B` and `C` are distinct from everything else.

Node fill colors (used in the table panel and as small filled circles in the graph):

| Group | Fill | Stroke |
|-------|------|--------|
| A (Proximal tubule)   | `#FAC775` (amber-200) | `#854F0B` (amber-600) |
| A' (PT cell)          | `#AFA9EC` (purple-200) | `#3C3489` (purple-700) |
| B (Distal tubule)     | `#5DCAA5` (teal-200)  | `#085041` (teal-700) |
| C (Podocyte)          | `#ED93B1` (pink-200)  | `#72243E` (pink-700) |

Note: the amber/teal node fills are unrelated to the amber/teal edge encoding. Node colors are categorical labels for celltype groups; edge colors are the strict/partial encoding. Implementers should pick distinct hues if this collision is a concern; the rationale for the current scheme is that the node-fill amber matches the most populous label group and the edge-encoding amber is dark enough (`#BA7517`) that the two read as different intensities.

### 2.1 Computed edges (28 unordered pairs)

Below, edges are listed grouped by joint-distribution cell. This is the ground truth the figure must display.

**(strict label, strict gene) — 1 pair**
- P1.PT — P2.PT

**(strict label, partial gene, subset) — 2 pairs**
- P1.PT — P3.PT  (P3.PT ⊂ P1.PT)
- P2.PT — P3.PT  (P3.PT ⊂ P2.PT)

**(strict label, partial gene, generic) — 1 pair**
- P1.DT — P2.DT  (overlap on SLC12A3 only, neither is a subset)

**(strict label, none gene) — 2 pairs**
- P1.DT — P3.DT
- P2.DT — P3.DT

**(partial label, strict gene) — 2 pairs**
- P1.PT — P4.PTc
- P2.PT — P4.PTc

**(partial label, partial gene, subset) — 1 pair**
- P3.PT — P4.PTc  (P3.PT ⊂ P4.PTc)

**(partial label, partial gene, generic) — 0 pairs**

**(partial label, none gene) — 0 pairs**

**(none label, *) — 19 pairs** (all default to *none gene* in the toy)

Joint distribution counts (3×3):

|                 | strict gene | partial gene | none gene |
|-----------------|:-----------:|:------------:|:---------:|
| **strict label**  | 1           | 3            | 2         |
| **partial label** | 2           | 1            | 0         |
| **none label**    | 0           | 0            | 19        |

Total = 28 = C(8, 2).

## 3. Layout

The figure is one wide horizontal frame. Suggested aspect ratio: roughly 16:9 or 2:1. The implementer should target a `\linewidth`-spanning figure in a single-column manuscript.

Three panels, left to right:

```
┌─────────────────┬──────────────────────────┬────────────────┐
│ Panel A         │ Panel B                  │ Panel C        │
│ PCT node table  │ Label graph │ Gene graph │ Joint heatmap  │
│ (~30% width)    │ (~50% width, two columns)│ (~20% width)   │
└─────────────────┴──────────────────────────┴────────────────┘
```

The exact widths can be tuned, but panel B should be the widest because it contains two side-by-side graphs that need room to breathe.

### 3.1 Panel A — PCT node table

A vertical list of 8 rows, one per PCT node. Each row is a rounded rectangle (corner radius ~3pt) with:

- Node ID (e.g., `P1.PT`) on the left in bold.
- Celltype label below or beside the ID in a slightly smaller weight.
- Gene set as a comma-separated list, smaller still, possibly truncated with `...` if the implementer wants a width cap.
- Background fill = node group color (50-stop equivalent, lighter than the node circle fill in panel B).
- Border stroke = node group stroke color.

Row order (top to bottom): P1.PT, P2.PT, P3.PT, P4.PTc, P1.DT, P2.DT, P3.DT, P4.Pod. This groups the PT-family at the top, then the DT-family, then the singleton podocyte. Add a small horizontal gap (~6pt) between the PT-family block and the DT-family block to suggest celltype grouping.

A short caption above the table reads `paper-celltype (PCT) nodes`. A footnote-style line below the table maps fill colors to label groups: `Proximal tubule (amber), PT cell (purple, similar to amber), Distal tubule (teal), Podocyte (pink)`.

### 3.2 Panel B — two graphs sharing node positions

Two subpanels side by side, separated by a thin vertical dashed divider.

Each subpanel:

- Header row: panel name (`label graph` / `gene graph`) above a one-line subtitle clarifying what an edge means.
- Below the header: a circular node layout with all 8 PCT nodes placed at identical relative positions in both subpanels. The shared layout is the central pedagogical device — an edge present in one graph but not the other is read by spatial correspondence.

**Node layout (circular, 8 nodes equally spaced).** Place the nodes on a circle in this clockwise order starting from 12 o'clock:

1. P1.PT     — 12 o'clock (top)
2. P2.PT     — 1:30
3. P4.PTc    — 3 o'clock
4. P3.PT     — 4:30
5. P4.Pod    — 6 o'clock (bottom)
6. P1.DT     — 7:30
7. P2.DT     — 9 o'clock
8. P3.DT     — 10:30

This ordering keeps the PT-family contiguous on the right half of the circle, the DT-family contiguous on the left half, and Podocyte at the bottom — so within-family edges are short and cross-family edges traverse the circle, making the structure easy to read.

The circle should have a faint dashed guide stroke (very light gray, dashed pattern) so the layout is visible but not distracting. Optional — the implementer can omit it if it adds clutter.

**Node rendering in panel B.** Each node is a small filled circle (radius ~5pt) with a 1pt stroke. Fill and stroke colors come from the node group table in §2. Node labels (e.g., `P1.PT`) are placed *outside* the circle, radially — labels at the top sit above the node, labels on the right sit to the right with `text-anchor=start`, etc. The label is small (≈9pt sans-serif).

**Edges in the label graph.** Draw an edge between two nodes iff their label relation is strict or partial:

- Strict (exact label): solid teal `#1D9E75`, line width 2.5pt.
- Partial (similar label): dashed teal-amber-amber `#BA7517`, line width 2.2pt, dash pattern `(6pt, 3pt)`.

For the toy data, the label graph edges are:

- Strict: P1.PT–P2.PT, P1.PT–P3.PT, P2.PT–P3.PT (PT triangle); P1.DT–P2.DT, P1.DT–P3.DT, P2.DT–P3.DT (DT triangle). Total: 6.
- Partial: P1.PT–P4.PTc, P2.PT–P4.PTc, P3.PT–P4.PTc. Total: 3.

**Edges in the gene graph.** Draw an edge between two nodes iff their gene relation is strict or partial:

- Strict (J = 1): solid teal `#1D9E75`, line width 2.5pt.
- Partial (0 < J < 1): dashed amber `#BA7517`, line width 2.2pt, dash pattern `(6pt, 3pt)`.

For partial edges that are *strict subsets* (one gene set is a proper subset of the other), additionally draw a `⊂` annotation at the edge midpoint:

- A small filled circle of radius 9pt at the midpoint, fill = page background (white), stroke = `#BA7517` at 0.5pt.
- Inside the circle, the glyph `⊂` in `#854F0B` (amber-600), font-size ~12pt, font-weight 500, anchored at the circle center.

For the toy data, the gene graph edges are:

- Strict: P1.PT–P2.PT, P1.PT–P4.PTc, P2.PT–P4.PTc. Total: 3.
- Partial (with `⊂`): P1.PT–P3.PT, P2.PT–P3.PT, P3.PT–P4.PTc. Total: 3.
- Partial (no `⊂`, generic overlap): P1.DT–P2.DT. Total: 1.

**Edge legend (centered below both subgraphs in panel B).**

A single horizontal legend with three entries:

1. Solid teal short line, label `strict match`.
2. Dashed amber short line, label `partial match`.
3. Small white circle with `⊂` glyph, label `gene subset (annotation)`.

**Cross-graph reading guide.** Below the legend, a short three-line italic block (small font) explaining how to read the two graphs against each other. Suggested text:

> read across the two graphs:
> · edge in label graph only (e.g. P1.DT–P3.DT) → same name, no shared markers
> · edge in gene graph only (none in this toy, but expected in real data) → same markers, different name
> · edge in both → field agrees on both name and markers

### 3.3 Panel C — joint distribution heatmap

A 3×3 grid of cells. Rows are the label relation (top to bottom: strict, partial, none). Columns are the gene relation (left to right: strict, partial, none). Each cell shows a count.

Cell sizes: equal, e.g., 36pt × 36pt. Total grid: 108pt × 108pt plus axis labels.

**Axis labels.**

- Above the grid, centered: italic `Marker Genes*`.
- Above each column, in a smaller font: column header (`strict (J = 1)`, `partial (0 < J < 1)`, `none (J = 0)`).
- Below the grid, centered: italic `*J = |G_1 ∩ G_2| / |G_1 ∪ G_2|`.
- To the left of the grid, vertically centered: italic `Celltype Labels`.
- To the left of each row, in a smaller font: row label (`strict (exact)`, `partial (similar)`, `none (different)`).

**Cell colors and counts.** Use the same teal/amber/gray vocabulary from panels A and B. The diagonal cells get the most saturated color of their tier; off-diagonals get desaturated versions of the dominant tier.

| Row \ Col | strict gene | partial gene | none gene |
|-----------|-------------|--------------|-----------|
| **strict label**  | teal 0.85α, count = 1, white text | teal 0.6α (lighter), count = 3, dark text | neutral gray fill, count = 2, dark text |
| **partial label** | amber 0.6α (lighter), count = 2, dark text | amber 0.85α, count = 1, white text | neutral gray fill, count = 0, muted gray text |
| **none label**    | neutral gray fill, count = 0, muted gray text | neutral gray fill, count = 0, muted gray text | darker gray 0.7α, count = 19, dark text |

Concrete fills:

- Teal saturated: `#1D9E75` at 0.85 opacity
- Teal light: `#5DCAA5` at 0.6 opacity
- Amber saturated: `#BA7517` at 0.85 opacity
- Amber light: `#FAC775` at 0.6 opacity
- Neutral light gray (zero/empty cells): `#F1EFE8`
- Neutral medium gray (the dominant `(none, none)` cell): `#B4B2A9` at 0.7 opacity

Each cell has a thin border (~0.5pt) in a gray that matches the page text. The count is centered in each cell at ~14pt sans-serif, weight 500.

### 3.4 Reading the figure

The narrative should flow left to right:

1. Panel A introduces the data unit (PCT node).
2. Panel B shows the two pairwise relations as separate graphs, with the same node layout so the reader can compare edge sets visually.
3. Panel C summarizes the cross-tabulation.

The implementer can add small horizontal arrows between the panels (panel A → panel B → panel C) with short labels (`compare pairs` between A and B, `tally` between B and C). These are optional but help guide the eye.

## 4. Technical notes for the LaTeX/TikZ implementation

### 4.1 Suggested package set

- `tikz` for the panels.
- `tikz` libraries: `positioning`, `shapes.geometric`, `arrows.meta`, `decorations.pathreplacing`, `calc`, `matrix`.
- `xcolor` with color definitions for the eight palette entries (teal, amber, purple, pink, green, gray strong, gray light, gray medium).
- `pgfplots` is optional. The 3×3 heatmap is small enough to draw as nine `\node[rectangle, fill=...]` cells inside a `tikzpicture`; `pgfplots` is overkill unless the implementer prefers a single `\addplot` interface.

### 4.2 Suggested data-driven structure

Rather than hardcoding 28 edge `\draw` commands, the implementer should define the node and edge data as TikZ-readable lists at the top of the figure file, then loop over them. Pseudo-code:

```latex
% nodes: id, group, cx, cy
\def\nodes{%
  P1.PT/A/0:90,
  P2.PT/A/0:45,
  P4.PTc/Aprime/0:0,
  P3.PT/A/0:-45,
  P4.Pod/C/0:-90,
  P1.DT/B/0:-135,
  P2.DT/B/0:180,
  P3.DT/B/0:135%
}

% label edges: u, v, tier (strict|partial)
\def\labeledges{%
  P1.PT/P2.PT/strict,
  P1.PT/P3.PT/strict,
  P2.PT/P3.PT/strict,
  P1.DT/P2.DT/strict,
  P1.DT/P3.DT/strict,
  P2.DT/P3.DT/strict,
  P1.PT/P4.PTc/partial,
  P2.PT/P4.PTc/partial,
  P3.PT/P4.PTc/partial%
}

% gene edges: u, v, tier (strict|partial), subset_flag (yes|no)
\def\geneedges{%
  P1.PT/P2.PT/strict/no,
  P1.PT/P4.PTc/strict/no,
  P2.PT/P4.PTc/strict/no,
  P1.PT/P3.PT/partial/yes,
  P2.PT/P3.PT/partial/yes,
  P3.PT/P4.PTc/partial/yes,
  P1.DT/P2.DT/partial/no%
}
```

Then `\foreach \u/\v/\tier in \labeledges` etc. to draw. This makes regenerating the figure with real data a matter of replacing the three lists.

### 4.3 Color definitions (xcolor)

```latex
\definecolor{tierStrict}{HTML}{1D9E75}
\definecolor{tierPartial}{HTML}{BA7517}
\definecolor{tierStrictLight}{HTML}{5DCAA5}
\definecolor{tierPartialLight}{HTML}{FAC775}
\definecolor{groupAfill}{HTML}{FAC775}   % proximal tubule
\definecolor{groupAstroke}{HTML}{854F0B}
\definecolor{groupAprimefill}{HTML}{AFA9EC}  % PT cell
\definecolor{groupAprimestroke}{HTML}{3C3489}
\definecolor{groupBfill}{HTML}{5DCAA5}   % distal tubule
\definecolor{groupBstroke}{HTML}{085041}
\definecolor{groupCfill}{HTML}{ED93B1}   % podocyte
\definecolor{groupCstroke}{HTML}{72243E}
\definecolor{neutralLight}{HTML}{F1EFE8}
\definecolor{neutralMid}{HTML}{B4B2A9}
\definecolor{mutedText}{HTML}{888780}
```

### 4.4 Edge style commands

```latex
\tikzset{
  edge strict/.style = {tierStrict, line width=2.5pt},
  edge partial/.style = {tierPartial, line width=2.2pt, dash pattern=on 6pt off 3pt},
  subset glyph/.style = {circle, draw=tierPartial, fill=white, line width=0.5pt, inner sep=1pt, minimum size=18pt},
  pct circle/.style = {circle, draw, line width=1pt, minimum size=10pt, inner sep=0pt}
}
```

For each subset edge, after drawing the line, place a `subset glyph` node at the midpoint with `\u` content `$\subset$` (the LaTeX subset symbol, which renders as ⊂). TikZ's `pos=0.5` on a path and `decorations.markings` can both achieve this; `\path (...) -- node[pos=0.5, subset glyph] {$\subset$} (...)` is the simplest form.

### 4.5 Heatmap as a TikZ matrix

The 3×3 cell grid can be a `matrix of nodes`:

```latex
\matrix (jd) [matrix of nodes, nodes={rectangle, draw=mutedText, line width=0.5pt, minimum width=36pt, minimum height=36pt, anchor=center, font=\sffamily\bfseries}, column sep=-0.5pt, row sep=-0.5pt] {
  |[fill=tierStrict, text=white]| 1 &
  |[fill=tierStrictLight!60]| 3 &
  |[fill=neutralLight]| 2 \\
  |[fill=tierPartialLight!60]| 2 &
  |[fill=tierPartial, text=white]| 1 &
  |[fill=neutralLight, text=mutedText]| 0 \\
  |[fill=neutralLight, text=mutedText]| 0 &
  |[fill=neutralLight, text=mutedText]| 0 &
  |[fill=neutralMid!70]| 19 \\
};
```

The `!60` suffix in `xcolor` produces a 60% mix with white, equivalent to opacity 0.6 on white. Adjust as needed.

### 4.6 Fonts and sizes

The figure should use a sans-serif font throughout (`\sffamily`). Suggested sizes:

- Panel headers (`label graph`, `gene graph`, `paper-celltype (PCT) nodes`, `joint distribution`): `\small\bfseries`.
- Subtitles below headers: `\footnotesize`.
- Node labels in panel B: `\scriptsize`.
- Heatmap counts: `\small\bfseries`.
- Heatmap row/column labels: `\footnotesize`.
- Cross-graph reading guide: `\scriptsize\itshape`.

### 4.7 Reproducibility note

The figure is constructed from three lists (nodes, label edges, gene edges) and a 3×3 count matrix. When the implementer swaps in real data, all four are recomputed by the analysis pipeline. The cell counts in the heatmap should always equal the edge counts in the two graphs cross-tabulated; an implementer-side assertion that `sum(jd) == C(N, 2)` for `N` PCT nodes is a useful sanity check.

## 5. Real-data adaptation notes (forward-looking)

When the figure is regenerated with real data, two things are likely to change:

1. **Edge density.** With more nodes, the gene graph will become a hairball if all partial edges are drawn. Apply a Jaccard threshold (e.g., `J ≥ 0.3`) to the partial tier and note the threshold in the caption. The strict and subset edges are sparse and can always be drawn.
2. **Node layout.** The circular layout works for 8 nodes. For more, run a force-directed layout on the *gene graph* (the more informative one for this analysis) and copy those positions to the label graph. The shared-position invariant is what makes the comparison work — do not let a layout algorithm decide them independently.

The bottom-right cell `(none label, none gene)` will dominate the heatmap as N grows. Two options:

- Log-color the heatmap (use `log(count + 1)` for fill intensity, but display the raw count).
- Drop the bottom-right cell and rebalance the other eight to sum to the count of "interesting" pairs (any pair with at least one non-`none` relation).

State the choice in the caption.
