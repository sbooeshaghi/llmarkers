# Paper Figure Manifest

This manifest records the active manuscript figure inputs.

## Active Figures

| Role | Paper reference | LaTeX wrapper/body | Figure artifacts | Source |
| --- | --- | --- | --- | --- |
| Figure 1 | `fig:mrkr_overview` | `tex-figures/fig1_mrkr_overview.tex`, `tex-figures/fig1_mrkr_overview_body.tex` | TikZ in the body file | `tex-figures/fig1_mrkr_overview_body.tex` |
| Figure 2 | `fig:marker_selection`, `fig:llm_curation` | `tex-figures/fig2_marker_recovery.tex`, `tex-figures/fig2_marker_recovery_body.tex` | `analysis/figures/fig2_panel_a_benchmark_summary.pdf`, `fig2_panel_b_optimal_deg_cutoff.pdf`, `fig2_panel_c_llm_recovery.pdf` | `analysis/build_fig2_marker_recovery.py` |
| Figure 3 | `fig:corpus_marker_reuse` | `tex-figures/fig3_mrkr_corpus_reuse.tex` | `analysis/artifacts/mrkr_corpus_analysis_v1/fig_mrkr_corpus_reuse_v1.pdf` | `analysis/analyze_mrkr_corpus.py` |
| Figure 4 | `fig:cap_partition` | `tex-figures/fig4_cap_partition.tex`, `tex-figures/fig4_cap_partition_body.tex` | `analysis/figures/fig3_panel_g_cap_liver_reported_marker_recovery.pdf`, `fig3_panel_h_cap_liver_de_stability.pdf`, `fig3_panel_i_cap_liver_marker_retrieval.pdf` | `analysis/build_cap_liver_local_global_deg.py` |
| Supplementary Figure S1 | `fig:hildreth_detail` | `tex-figures/figs1_hildreth_detail.tex` | `analysis/figures/fig_hildreth_detail.pdf` | `analysis/lfc_comparison.ipynb` |
| Supplementary Figure S2 | `fig:paper_celltype_joint` | `tex-figures/fig_paper_celltype_joint.tex`, `tex-figures/fig_paper_celltype_joint_body.tex` | TikZ in the body file | `tex-figures/fig_paper_celltype_joint_body.tex` |

## Active Result Files

Figure 2:

- `analysis/artifacts/fig2_benchmark_summary.tsv`
- `analysis/artifacts/fig2_optimal_deg_cutoff.tsv`
- `analysis/artifacts/fig2_llm_recovery.tsv`
- `analysis/artifacts/fig2_llm_recovery_current.tsv`
- `analysis/artifacts/mrkr_benchmark_pilot_20260721/joint_deg_extraction_v1/joint_extraction_papers.tsv`

Figure 3:

- `analysis/artifacts/mrkr_corpus_analysis_v1/corpus_summary.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/term_coverage.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/label_balanced_pair_summary.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/matched_background_seed_sensitivity.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/cell_ontology_label_audit.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/ontology_pair_summary.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/stable_identifier_linkage_summary.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/same_label_pairs.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/coreported_context_metrics.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/coreported_context_fit.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/label_intersection_accumulation.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/ontology_intersection_accumulation.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/minimum_marker_sensitivity.tsv`
- `analysis/artifacts/mrkr_corpus_analysis_v1/report.md`
- `analysis/artifacts/mrkr_corpus_analysis_v1/run_metadata.json`

Figure 4:

- `analysis/artifacts/cap_liver_local_global_deg_summary.tsv`
- `analysis/artifacts/cap_liver_local_global_reported_marker_ranks.tsv`
- `analysis/artifacts/cap_liver_local_global_top_degs.tsv`
- `analysis/artifacts/cap_liver_local_global_recovery_subsampling.tsv`
- `analysis/artifacts/cap_liver_local_global_recovery_subsampling_summary.tsv`

## Rendering

Render the standalone figure wrappers from the repository root:

```bash
bash analysis/render_paper_standalone_figures.sh
```

The PDFs are written to `docs/paper/biorxiv/tex-figures/standalone/build/`,
which is ignored as LaTeX build output.
