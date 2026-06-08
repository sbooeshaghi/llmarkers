# Marker experiment covering bounds

For `K` target cell types and experiments that jointly compare at most `r` cell types, any design that certifies all pairwise marker separations needs at least

```text
ceil(choose(K, 2) / choose(r, 2))
```

experiments. The exact optimum is the covering design number `C(K, r, 2)`, which can be larger. The binary marker lower bound is `ceil(log2(K))`; it is an information-theoretic lower bound, not a claim that such a biological panel exists.

| Scope | K | Pairs | Binary markers | r=5 | r=10 | r=20 | r=50 | r=100 | r=500 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C. elegans adult, high-resolution cell classes | 146 | 10585 | 8 | 1059 | 236 | 56 | 9 | 3 | 1 |
| Drosophila adult, Fly Cell Atlas | 250 | 31125 | 8 | 3113 | 692 | 164 | 26 | 7 | 1 |
| Human Tabula Sapiens | 475 | 112575 | 9 | 11258 | 2502 | 593 | 92 | 23 | 1 |
| Human body, major cell-type estimate | 400 | 79800 | 9 | 7980 | 1774 | 420 | 66 | 17 | 1 |
| Human body, fine cell-type estimate | 3358 | 5636403 | 12 | 563641 | 125254 | 29666 | 4602 | 1139 | 46 |
| Mouse brain, major cell types | 300 | 44850 | 9 | 4485 | 997 | 237 | 37 | 10 | 1 |
| Mouse brain, transcriptomic clusters | 5322 | 14159181 | 13 | 1415919 | 314649 | 74523 | 11559 | 2861 | 114 |

## Scenario notes

- **C. elegans adult, high-resolution cell classes**: total cells = 959 somatic; genes = ~20,000; note = TF atlas high-resolution classes; sources = https://www.ncbi.nlm.nih.gov/books/NBK26861/; https://pmc.ncbi.nlm.nih.gov/articles/PMC4781646/; https://www.nature.com/articles/s41467-023-42677-6.
- **Drosophila adult, Fly Cell Atlas**: total cells = 580,000 sampled nuclei; genes = ~13,900; note = reported as >250 annotated cell types; rounded down; sources = https://pmc.ncbi.nlm.nih.gov/articles/PMC8944923/; https://academic.oup.com/genetics/article/201/3/815/5930114.
- **Human Tabula Sapiens**: total cells = ~500,000 sampled cells; genes = ~20,000; note = distinct annotated cell types; sources = https://pmc.ncbi.nlm.nih.gov/articles/PMC9812260/; https://pmc.ncbi.nlm.nih.gov/articles/PMC6413734/.
- **Human body, major cell-type estimate**: total cells = ~27-37 trillion; genes = ~20,000; note = major cell-type estimate; sources = https://www.nature.com/articles/s41597-026-06642-4.
- **Human body, fine cell-type estimate**: total cells = ~27-37 trillion; genes = ~20,000; note = fine cell-type estimate cited by HRA paper; sources = https://www.nature.com/articles/s41597-026-06642-4.
- **Mouse brain, major cell types**: total cells = >32 million characterized; genes = ~20,000-25,000; note = mouse whole-brain major cell types; sources = https://alleninstitute.org/news/scientists-unveil-first-complete-cellular-map-of-adult-mouse-brain; https://www.nature.com/articles/s41586-023-06808-9; https://pubmed.ncbi.nlm.nih.gov/28838066/.
- **Mouse brain, transcriptomic clusters**: total cells = >32 million characterized; genes = ~20,000-25,000; note = mouse whole-brain clusters; sources = https://alleninstitute.org/news/scientists-unveil-first-complete-cellular-map-of-adult-mouse-brain; https://www.nature.com/articles/s41586-023-06812-z; https://pubmed.ncbi.nlm.nih.gov/28838066/.
