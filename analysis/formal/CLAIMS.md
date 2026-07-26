# Marker Identifiability Claims

This directory formalizes the combinatorial part of marker-gene selection under
binarization. The formal model intentionally does not assert biological truth.
It says what follows once we represent reported marker claims as a binary matrix.

## Setup

Let `Cell` be a finite set of cell types, marker profiles, ontology groups, or
context-conditioned groups. Let `Gene` be a set of marker genes. A binary marker
matrix is

```text
X : Cell -> Gene -> Bool
```

where `X c g = true` means that gene `g` is reported as a marker for `c`.

For LLMarkers, `Cell` can be instantiated in multiple ways:

- reported cell type labels
- marker-derived clusters
- ontology-mapped labels
- tissue-, disease-, assay-, or paper-conditioned labels
- expert-defined immune states

The matrix is a reported-marker matrix. A zero means "not reported as a marker"
in the available corpus, not necessarily "not expressed."

## Formal Claims Already Proved

1. **Signature injection.** If a marker panel separates all cell types, then the
   map from each cell type to its binary marker signature is injective.

2. **Panel-level failure.** If two distinct cell types have the same binary
   signature on a marker panel, that full panel does not separate the comparison
   set. This claim is about sets of genes, not only single genes.

3. **Hitting-set equivalence.** For a finite candidate gene universe, a marker
   panel separates a comparison set if and only if it intersects every pairwise
   difference set `D_ab = {g | X[a,g] != X[b,g]}`. This is the formal bridge to
   ILP-style marker-panel selection.

4. **Target-specific marker panels.** For a fixed target group and comparison
   family, a marker panel is a hitting set over the pairwise marker sets: every
   comparison group must be covered by at least one selected gene. Singleton
   panels coincide with the strict single-gene marker definition, but multi-gene
   panels can cover all comparisons even when the strict marker-gene
   intersection is empty.

5. **Marker-panel axioms and uniqueness.** The file states minimal axioms for a
   marker-panel rule: the empty comparison family is neutral, a singleton
   comparison family is covered exactly when the panel intersects the
   corresponding pairwise marker set, and coverage over a union of comparison
   families is conjunctive. These axioms force the hitting-set representation,
   so any marker-panel rule satisfying them is unique.

6. **Panel-defined cell types.** A marker-panel-defined cell type is a nonempty
   finite family of scoped local groups together with a finite marker panel that
   covers every scoped comparison family. The singleton-panel theorem proves
   that a one-gene marker-panel-defined cell type reduces to the existing shared
   single-marker-gene definition. Adding local instances makes the shared-panel
   requirement harder, so a panel that supports a broader family of instances
   also supports any restricted subfamily.

7. **Panel sensitivity-specificity tradeoff.** For a finite set of positive
   contexts and negative contexts, panel performance separates into positive
   coverage and off-target hits. Adding genes can only increase positive
   coverage, but it can also only increase off-target hits, equivalently
   decreasing the number of negative contexts avoided. The marginal positive
   coverage gained by adding a gene is diminishing: adding the same gene to a
   larger panel can cover no more new contexts than adding it to a smaller
   panel. This formalizes the panel-size tradeoff underlying sensitivity,
   specificity, and marker-panel Pareto curves.

8. **Constrained and Pareto marker panels.** The file defines feasible panels as
   panels that achieve at least a requested positive coverage count while
   hitting at most a requested number of negative contexts. It also defines weak
   and strict Pareto dominance over positive coverage, off-target hits, and
   panel size. A Pareto-optimal marker panel is one that is not strictly
   dominated by another panel. If a feasible panel is weakly dominated by
   another panel, the dominating panel is also feasible; therefore dominated
   feasible panels can be discarded. The marker-panel axioms define what counts
   as a valid panel; sensitivity, off-target hits, and size define the
   optimization problem over such panels.

9. **Panel hierarchy and type/state scopes.** The hierarchy and type/state
   scope theorems lift to panels. A panel valid over a parent/global comparison
   scope is valid over any child/local comparison scope. Likewise, a panel valid
   at broader cell-type scope is valid at restricted cell-state scope. The
   converses are not guaranteed because restricted scopes are easier to cover.

10. **Information bound.** If a marker panel `S` separates `k` cell types, then
   `k <= 2 ^ |S|`. The familiar `ceil(log2 k)` lower-bound interpretation is
   not stated as a separate Lean theorem.

11. **Monotonicity of separation.** If `S` separates the cell types, then every
   superset of `S` also separates them.

12. **Hierarchy/refinement.** Adding markers refines the induced partition. If
   two profiles agree on a larger marker panel, they also agree on every smaller
   panel.

13. **Scope poset.** For a fixed comparison set, the separating marker panels are
   upward-closed under gene-set inclusion. For a fixed marker panel, the
   comparison sets it separates are downward-closed under cell-set inclusion.
   Equivalently, marker validity is monotone in added genes and antitone in
   added cell types.

14. **Comparison difficulty layer.** The file defines an optional
   comparison-difficulty burden for a target and comparison family. For
   nonnegative difficulty scores, enlarging a comparison family cannot decrease
   the burden. However, a formal example shows that one close comparison can
   have higher burden than two distant comparisons. Thus comparison-family
   cardinality alone does not determine biological difficulty. The file also
   defines high-similarity or high-difficulty subfamilies; a panel that covers
   the full family covers any such hard-neighbor subfamily.

15. **Non-uniqueness.** Minimum separating marker panels need not be unique. The
   formal example proves that two different one-gene panels can both be minimum
   separating panels.

16. **Gene classes.** The file defines essential, exchangeable, and redundant
   genes relative to the family of minimum separating panels.

17. **Local/global separation.** Separation over a global comparison set implies
   separation over every local subset. The converse is false: profiles can be
   separable within each paper but fail to be separable after pooling profiles
   across papers.

18. **Adding a comparison cell type can change marker status.** A one-gene panel
   can separate two cell types locally, then fail after a third cell type is
   added with the same marker signature as one of the original cell types. This
   formalizes the statement that marker claims are relative to the comparison
   set.

19. **Marker liftover.** The file defines separation of one profile from a
   finite comparison set. This captures whether a local marker claim remains
   distinguishing when lifted to outside-paper or atlas-scale profiles.

20. **Experiment pair coverage.** A global marker panel can be certified from
   local experiments if the experiments cover every pair of target cell types
   and the same panel separates each experiment. This makes the experiment
   design problem a pair-covering problem over the intended atlas scope.
   The proved counting bound uses ordered distinct pairs: if each experiment
   contributes at most `q` such pairs, then `K * K - K` is at most the number
   of experiments times `q`.

21. **Admissible comparison graphs.** If only some cell-type pairs are
   biologically or experimentally meaningful to compare, the required target is
   an admissible comparison graph rather than the complete graph on all cell
   types. A marker panel can then be certified for that graph if experiments
   cover every admissible edge and the panel separates each experiment. The
   complete-graph setting is the special case where every distinct pair is
   admissible.

22. **Ideal one-vs-all equivalence.** At the binary marker-signature level,
   one-vs-all separation is equivalent to pairwise global separation when
   "all" means every individual cell type in the complement. This is stronger
   than an aggregated one-vs-rest differential-expression test, which can be
   lossy.

23. **Recurrent local markers versus certified global markers.** A gene or
   marker panel can recur locally for the same label across studies without
   being certified globally. The equivalence holds only when the reported local
   comparison families cover every target-background pair required by the
   global marker statement. Thus a machine-readable marker report needs the
   target, comparison group, and pairwise result, not only `(label, gene)`.

## Claims We Can Make With LLMarkers

These are empirical claims supported by applying the formal definitions to the
LLMarkers matrix.

- LLMarkers lets us compute reported-marker identifiability for a proposed
  partition of cell types or states.
- For a given partition, we can estimate the lower and upper number of marker
  genes required to separate the groups.
- We can classify genes as essential, exchangeable, redundant, or contextual
  relative to that partition.
- We can compare label-derived partitions against marker-derived partitions.
- If a label requires many different exchangeable panels, the label is likely
  underspecified by reported markers.
- If a gene is weak globally but becomes separating after conditioning on
  tissue, disease, assay, perturbation, or paper context, it is a candidate
  context-dependent or state marker.
- We can quantify whether locally reported markers lift to the global atlas
  comparison set.
- We can identify labels whose profiles are locally distinguishable within
  papers but globally underspecified across papers.
- We can distinguish recurrent local evidence from certified global evidence by
  auditing target-background pair coverage.

## Claims We Should Not Make Without Additional Evidence

- We should not claim that a missing marker is not expressed.
- We should not claim that the minimum panel is biologically unique.
- We should not claim that a marker is canonical in an absolute sense.
  Canonicality is relative to a partition, context, and separation rule.
- We should not claim that reported-marker identifiability is equivalent to
  experimental identifiability in new data.
- We should not claim that local marker separation within one paper implies
  global atlas-scale separation.

## Practical Tool Direction

The natural tool is:

```text
input:  binary marker matrix X, proposed partition P, optional context strata
output: separating panels, bounds, essential/exchangeable/redundant/contextual genes
```

This connects LLMarkers to ILP-style marker selection. The ILP asks for a small
set of genes that intersects every pairwise difference set between groups. The
formal proof explains what such a selected set means.
