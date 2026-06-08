# Atlas scope bounds

This deterministic table uses a simple restricted-scope model.

- `K`: target cell types.
- `G`: protein-coding gene universe.
- `r`: maximum cell types jointly compared in one experiment.
- `f`: context group size as a fraction of `K`.
- `f=1`: complete global comparison over all cell types.
- `f<1`: cell types are partitioned into context groups of size about `fK`; only within-group pairs are required.

The experiment lower bound is pair-coverage. `local marker LB` is `ceil(log2(min(r, max context group size)))`, the best-case binary-feature lower bound inside one local experiment. `atlas marker LB` is `ceil(log2(max context group size))`, the best-case lower bound for the full required scope. Neither marker value is an empirical marker-panel size.

| Scope | K | G | r cell types/experiment | f | groups | max group | pairs | pair fraction | experiments LB | local marker LB | atlas marker LB |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| C. elegans adult | 146 | 20000 | 20 | 1.00 | 1 | 146 | 10585 | 1.000 | 56 | 5 | 8 |
| C. elegans adult | 146 | 20000 | 20 | 0.25 | 4 | 37 | 2593 | 0.245 | 16 | 5 | 6 |
| C. elegans adult | 146 | 20000 | 20 | 0.10 | 10 | 15 | 1000 | 0.094 | 10 | 4 | 4 |
| C. elegans adult | 146 | 20000 | 20 | 0.05 | 19 | 8 | 505 | 0.048 | 19 | 3 | 3 |
| C. elegans adult | 146 | 20000 | 50 | 1.00 | 1 | 146 | 10585 | 1.000 | 9 | 6 | 8 |
| C. elegans adult | 146 | 20000 | 50 | 0.25 | 4 | 37 | 2593 | 0.245 | 4 | 6 | 6 |
| C. elegans adult | 146 | 20000 | 50 | 0.10 | 10 | 15 | 1000 | 0.094 | 10 | 4 | 4 |
| C. elegans adult | 146 | 20000 | 50 | 0.05 | 19 | 8 | 505 | 0.048 | 19 | 3 | 3 |
| C. elegans adult | 146 | 20000 | 100 | 1.00 | 1 | 146 | 10585 | 1.000 | 3 | 7 | 8 |
| C. elegans adult | 146 | 20000 | 100 | 0.25 | 4 | 37 | 2593 | 0.245 | 4 | 6 | 6 |
| C. elegans adult | 146 | 20000 | 100 | 0.10 | 10 | 15 | 1000 | 0.094 | 10 | 4 | 4 |
| C. elegans adult | 146 | 20000 | 100 | 0.05 | 19 | 8 | 505 | 0.048 | 19 | 3 | 3 |
| Drosophila adult | 250 | 13900 | 20 | 1.00 | 1 | 250 | 31125 | 1.000 | 164 | 5 | 8 |
| Drosophila adult | 250 | 13900 | 20 | 0.25 | 4 | 63 | 7689 | 0.247 | 43 | 5 | 6 |
| Drosophila adult | 250 | 13900 | 20 | 0.10 | 10 | 25 | 3000 | 0.096 | 20 | 5 | 5 |
| Drosophila adult | 250 | 13900 | 20 | 0.05 | 20 | 13 | 1485 | 0.048 | 20 | 4 | 4 |
| Drosophila adult | 250 | 13900 | 50 | 1.00 | 1 | 250 | 31125 | 1.000 | 26 | 6 | 8 |
| Drosophila adult | 250 | 13900 | 50 | 0.25 | 4 | 63 | 7689 | 0.247 | 8 | 6 | 6 |
| Drosophila adult | 250 | 13900 | 50 | 0.10 | 10 | 25 | 3000 | 0.096 | 10 | 5 | 5 |
| Drosophila adult | 250 | 13900 | 50 | 0.05 | 20 | 13 | 1485 | 0.048 | 20 | 4 | 4 |
| Drosophila adult | 250 | 13900 | 100 | 1.00 | 1 | 250 | 31125 | 1.000 | 7 | 7 | 8 |
| Drosophila adult | 250 | 13900 | 100 | 0.25 | 4 | 63 | 7689 | 0.247 | 4 | 6 | 6 |
| Drosophila adult | 250 | 13900 | 100 | 0.10 | 10 | 25 | 3000 | 0.096 | 10 | 5 | 5 |
| Drosophila adult | 250 | 13900 | 100 | 0.05 | 20 | 13 | 1485 | 0.048 | 20 | 4 | 4 |
| Human major cell types | 400 | 20000 | 20 | 1.00 | 1 | 400 | 79800 | 1.000 | 420 | 5 | 9 |
| Human major cell types | 400 | 20000 | 20 | 0.25 | 4 | 100 | 19800 | 0.248 | 108 | 5 | 7 |
| Human major cell types | 400 | 20000 | 20 | 0.10 | 10 | 40 | 7800 | 0.098 | 50 | 5 | 6 |
| Human major cell types | 400 | 20000 | 20 | 0.05 | 20 | 20 | 3800 | 0.048 | 20 | 5 | 5 |
| Human major cell types | 400 | 20000 | 50 | 1.00 | 1 | 400 | 79800 | 1.000 | 66 | 6 | 9 |
| Human major cell types | 400 | 20000 | 50 | 0.25 | 4 | 100 | 19800 | 0.248 | 20 | 6 | 7 |
| Human major cell types | 400 | 20000 | 50 | 0.10 | 10 | 40 | 7800 | 0.098 | 10 | 6 | 6 |
| Human major cell types | 400 | 20000 | 50 | 0.05 | 20 | 20 | 3800 | 0.048 | 20 | 5 | 5 |
| Human major cell types | 400 | 20000 | 100 | 1.00 | 1 | 400 | 79800 | 1.000 | 17 | 7 | 9 |
| Human major cell types | 400 | 20000 | 100 | 0.25 | 4 | 100 | 19800 | 0.248 | 4 | 7 | 7 |
| Human major cell types | 400 | 20000 | 100 | 0.10 | 10 | 40 | 7800 | 0.098 | 10 | 6 | 6 |
| Human major cell types | 400 | 20000 | 100 | 0.05 | 20 | 20 | 3800 | 0.048 | 20 | 5 | 5 |
| Human fine cell types | 3358 | 20000 | 20 | 1.00 | 1 | 3358 | 5636403 | 1.000 | 29666 | 5 | 12 |
| Human fine cell types | 3358 | 20000 | 20 | 0.25 | 4 | 840 | 1407843 | 0.250 | 7411 | 5 | 10 |
| Human fine cell types | 3358 | 20000 | 20 | 0.10 | 10 | 336 | 562131 | 0.100 | 2966 | 5 | 9 |
| Human fine cell types | 3358 | 20000 | 20 | 0.05 | 20 | 168 | 280227 | 0.050 | 1479 | 5 | 8 |
| Human fine cell types | 3358 | 20000 | 50 | 1.00 | 1 | 3358 | 5636403 | 1.000 | 4602 | 6 | 12 |
| Human fine cell types | 3358 | 20000 | 50 | 0.25 | 4 | 840 | 1407843 | 0.250 | 1151 | 6 | 10 |
| Human fine cell types | 3358 | 20000 | 50 | 0.10 | 10 | 336 | 562131 | 0.100 | 460 | 6 | 9 |
| Human fine cell types | 3358 | 20000 | 50 | 0.05 | 20 | 168 | 280227 | 0.050 | 240 | 6 | 8 |
| Human fine cell types | 3358 | 20000 | 100 | 1.00 | 1 | 3358 | 5636403 | 1.000 | 1139 | 7 | 12 |
| Human fine cell types | 3358 | 20000 | 100 | 0.25 | 4 | 840 | 1407843 | 0.250 | 287 | 7 | 10 |
| Human fine cell types | 3358 | 20000 | 100 | 0.10 | 10 | 336 | 562131 | 0.100 | 120 | 7 | 9 |
| Human fine cell types | 3358 | 20000 | 100 | 0.05 | 20 | 168 | 280227 | 0.050 | 60 | 7 | 8 |
| Mouse brain major types | 300 | 22000 | 20 | 1.00 | 1 | 300 | 44850 | 1.000 | 237 | 5 | 9 |
| Mouse brain major types | 300 | 22000 | 20 | 0.25 | 4 | 75 | 11100 | 0.247 | 60 | 5 | 7 |
| Mouse brain major types | 300 | 22000 | 20 | 0.10 | 10 | 30 | 4350 | 0.097 | 30 | 5 | 5 |
| Mouse brain major types | 300 | 22000 | 20 | 0.05 | 20 | 15 | 2100 | 0.047 | 20 | 4 | 4 |
| Mouse brain major types | 300 | 22000 | 50 | 1.00 | 1 | 300 | 44850 | 1.000 | 37 | 6 | 9 |
| Mouse brain major types | 300 | 22000 | 50 | 0.25 | 4 | 75 | 11100 | 0.247 | 12 | 6 | 7 |
| Mouse brain major types | 300 | 22000 | 50 | 0.10 | 10 | 30 | 4350 | 0.097 | 10 | 5 | 5 |
| Mouse brain major types | 300 | 22000 | 50 | 0.05 | 20 | 15 | 2100 | 0.047 | 20 | 4 | 4 |
| Mouse brain major types | 300 | 22000 | 100 | 1.00 | 1 | 300 | 44850 | 1.000 | 10 | 7 | 9 |
| Mouse brain major types | 300 | 22000 | 100 | 0.25 | 4 | 75 | 11100 | 0.247 | 4 | 7 | 7 |
| Mouse brain major types | 300 | 22000 | 100 | 0.10 | 10 | 30 | 4350 | 0.097 | 10 | 5 | 5 |
| Mouse brain major types | 300 | 22000 | 100 | 0.05 | 20 | 15 | 2100 | 0.047 | 20 | 4 | 4 |
| Mouse brain clusters | 5322 | 22000 | 20 | 1.00 | 1 | 5322 | 14159181 | 1.000 | 74523 | 5 | 13 |
| Mouse brain clusters | 5322 | 22000 | 20 | 0.25 | 4 | 1331 | 3537801 | 0.250 | 18622 | 5 | 11 |
| Mouse brain clusters | 5322 | 22000 | 20 | 0.10 | 10 | 533 | 1413552 | 0.100 | 7447 | 5 | 10 |
| Mouse brain clusters | 5322 | 22000 | 20 | 0.05 | 20 | 267 | 705585 | 0.050 | 3716 | 5 | 9 |
| Mouse brain clusters | 5322 | 22000 | 50 | 1.00 | 1 | 5322 | 14159181 | 1.000 | 11559 | 6 | 13 |
| Mouse brain clusters | 5322 | 22000 | 50 | 0.25 | 4 | 1331 | 3537801 | 0.250 | 2890 | 6 | 11 |
| Mouse brain clusters | 5322 | 22000 | 50 | 0.10 | 10 | 533 | 1413552 | 0.100 | 1157 | 6 | 10 |
| Mouse brain clusters | 5322 | 22000 | 50 | 0.05 | 20 | 267 | 705585 | 0.050 | 577 | 6 | 9 |
| Mouse brain clusters | 5322 | 22000 | 100 | 1.00 | 1 | 5322 | 14159181 | 1.000 | 2861 | 7 | 13 |
| Mouse brain clusters | 5322 | 22000 | 100 | 0.25 | 4 | 1331 | 3537801 | 0.250 | 716 | 7 | 11 |
| Mouse brain clusters | 5322 | 22000 | 100 | 0.10 | 10 | 533 | 1413552 | 0.100 | 289 | 7 | 10 |
| Mouse brain clusters | 5322 | 22000 | 100 | 0.05 | 20 | 267 | 705585 | 0.050 | 159 | 7 | 9 |
