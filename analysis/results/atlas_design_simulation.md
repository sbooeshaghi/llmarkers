# Atlas design simulation

This simulation starts with organism-scale cell-type counts, assigns cell types to tissue/admissibility contexts, and computes three quantities: admissible pair count, experiment lower bounds, and marker-gene sufficiency estimates. The cell-type distributions are assumptions, not empirical ontology claims.

## Model

- Cell types have one primary context.
- A fraction of cell types is shared across additional contexts.
- Two cell types are admissibly comparable if they share a context.
- An experiment can jointly compare at most `r` cell types from one context.
- The marker-gene estimate uses a random-gene model: each candidate gene separates any admissible pair with probability `q`.

The experiment values are lower bounds. The random-gene marker values are sufficient sizes under a union bound and are not minimum hitting-set optima.

| Scope | K | Contexts | Max context K | Admissible pairs | Pair fraction | Exp LB r=20 | Exp LB r=50 | Complete LB r=50 | Binary marker LB | Random genes q=.1 | Random genes q=.02 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C. elegans adult | 146 | 12 | 32 | 1501 | 0.142 | 8 | 4 | 9 | 5 | 98 | 511 |
| Drosophila adult | 250 | 20 | 43 | 3266 | 0.105 | 18 | 4 | 26 | 6 | 106 | 549 |
| Human major cell types | 400 | 45 | 42 | 5693 | 0.071 | 30 | 7 | 66 | 6 | 111 | 577 |
| Human fine cell types | 3358 | 70 | 233 | 227574 | 0.040 | 1198 | 186 | 4602 | 8 | 146 | 759 |
| Mouse brain major types | 300 | 25 | 49 | 4347 | 0.097 | 23 | 5 | 37 | 6 | 108 | 563 |
| Mouse brain clusters | 5322 | 80 | 372 | 468232 | 0.033 | 2465 | 383 | 11559 | 9 | 153 | 795 |

## Interpretation

Tissue/admissibility constraints can reduce the comparison graph by orders of magnitude relative to the complete graph. They do not remove the marker-selection problem; they define which pairwise difference constraints must be hit by a marker panel.
