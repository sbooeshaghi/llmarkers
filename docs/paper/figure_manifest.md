# Paper Figure Manifest

This manifest records manuscript-facing figure inputs. A file listed here as
active should stay in the main tree.

## Active Manuscript Dependencies

`docs/paper/src/main.tex` imports thin LaTeX wrappers from `docs/paper/src/figures/`.

| Role | Paper reference | LaTeX wrapper/body | Figure artifacts | Source |
| --- | --- | --- | --- | --- |
| Figure 1 | `fig:paper_celltype_joint` | `docs/paper/src/figures/fig_paper_celltype_joint.tex`, `docs/paper/src/figures/fig_paper_celltype_joint_body.tex` | TikZ in body file | `docs/notes/fig1.md` |
| Figure 2 | `fig:marker_selection`, `fig:llm_curation` | `docs/paper/src/figures/fig2_marker_recovery.tex`, `docs/paper/src/figures/fig2_marker_recovery_body.tex` | `analysis/figures/fig2_panel_a_benchmark_summary.pdf`, `analysis/figures/fig2_panel_b_optimal_deg_cutoff.pdf`, `analysis/figures/fig2_panel_c_llm_recovery.pdf` | `analysis/build_fig2_marker_recovery.py` |
| Figure 3 A-F | `fig:cross_study_unification` | `docs/paper/src/figures/fig3_cross_study_unification.tex`, `docs/paper/src/figures/fig3_cross_study_unification_body.tex` | `analysis/figures/fig3_panel_a_joint_distribution.pdf` through `analysis/figures/fig3_panel_f_cap_local_global_recovery.pdf` | `analysis/build_fig3_local_global_marker_identifiability.py` |
| Figure 3 G-I | `fig:cross_study_unification` | same wrapper/body as Figure 3 A-F | `analysis/figures/fig3_panel_g_cap_liver_reported_marker_recovery.pdf`, `analysis/figures/fig3_panel_h_cap_liver_de_stability.pdf`, `analysis/figures/fig3_panel_i_cap_liver_marker_retrieval.pdf` | `analysis/build_cap_liver_local_global_deg.py` |
| Supplementary Hildreth figure | `fig:hildreth_detail` | `docs/paper/src/figures/figs1_hildreth_detail.tex` | `analysis/figures/fig_hildreth_detail.pdf` | `analysis/lfc_comparison.ipynb` |
| Supplementary benchmark table | `tab:benchmark` | inline in `docs/paper/src/main.tex` | table source in manuscript tree | benchmark curation notebooks |
| Supplementary LLM curation table | `tab:llm_curation` | inline in `docs/paper/src/main.tex` | table source in manuscript tree | `analysis/build_fig2_marker_recovery.py` |

Render standalone figure wrappers with:

```bash
bash analysis/scripts/render_paper_standalone_figures.sh
```

Outputs are written to `docs/paper/src/figures/standalone/build/`, which is ignored
as LaTeX build output.

## Active Figure Result Files

Figure 2:

- `analysis/results/fig2_benchmark_summary.tsv`
- `analysis/results/fig2_optimal_deg_cutoff.tsv`
- `analysis/results/fig2_llm_recovery.tsv`

Figure 3 A-F:

- `analysis/results/cross_study_label_marker_joint_distribution.tsv`
- `analysis/results/fig3_different_label_shared_marker_examples.tsv`
- `analysis/results/fig3_same_label_weak_marker_examples.tsv`
- `analysis/results/fig3_label_local_global_marker_recovery.tsv`
- `analysis/results/fig3_same_label_marker_jaccard_values.tsv`
- `analysis/results/fig3_same_label_marker_jaccard_summary.tsv`
- `analysis/results/fig3_cap_cross_project_label_marker_joint_distribution.tsv`
- `analysis/results/fig3_cap_cross_project_ontology_marker_joint_distribution.tsv`
- `analysis/results/fig3_cap_different_label_shared_marker_examples.tsv`
- `analysis/results/fig3_cap_same_label_weak_marker_examples.tsv`
- `analysis/results/fig3_cap_ontology_local_global_marker_recovery.tsv`
- `analysis/results/fig3_global_recovery_permutation_draws.tsv`
- `analysis/results/fig3_global_recovery_permutation_summary.tsv`
- `analysis/results/fig3_global_recovery_profile_values.tsv`
- `analysis/results/fig3_local_global_marker_identifiability_report.md`

Figure 3 G-I:

- `analysis/results/cap_liver_local_global_deg_summary.tsv`
- `analysis/results/cap_liver_local_global_reported_marker_ranks.tsv`
- `analysis/results/cap_liver_local_global_top_degs.tsv`
- `analysis/results/cap_liver_local_global_recovery_subsampling.tsv`
- `analysis/results/cap_liver_local_global_recovery_subsampling_summary.tsv`

Shared upstream tables used by Figure 3:

- `analysis/results/fig3_local_global_pair_summary.tsv`
- `analysis/results/fig3_local_global_pair_values_sample.tsv`
- `analysis/results/local_global_label_coherence_summary.tsv`
- `analysis/results/local_global_marker_pair_summary.tsv`
- `analysis/results/local_global_paper_marker_summary.tsv`
- `analysis/results/local_global_profile_marker_liftover.tsv`
- `analysis/results/local_global_marker_transfer_lift_by_label.tsv`
- `analysis/results/local_global_marker_transfer_lift_summary.tsv`
- `analysis/results/marker_identifiability_partition_summary.tsv`
- `analysis/results/marker_identifiability_selected_genes.tsv`

## Active Sources To Keep

- `analysis/build_fig2_marker_recovery.py`
- `analysis/build_fig3_local_global_marker_identifiability.py`
- `analysis/build_cap_liver_local_global_deg.py`
- `analysis/build_cap_llmarkers_comparison.py`
- `analysis/build_marker_corpus.py`
- `analysis/build_hca_extraction_summary.py`
- `analysis/build_local_global_marker_analysis.py`
- `analysis/build_local_global_marker_lift.py`
- `analysis/build_marker_identifiability_analysis.py`
- `analysis/cross_study_gene_space.py`
- `analysis/scripts/ingest_cap_datasets.py`
- `analysis/scripts/render_paper_standalone_figures.sh`
- `analysis/formal/`
