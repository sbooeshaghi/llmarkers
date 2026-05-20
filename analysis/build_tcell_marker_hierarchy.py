from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist

from build_marker_stability_prototype import assign_neighborhood, build_records
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR, build_profile_summary, split_marker_text


FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

MIN_MARKERS = 3
DISPLAY_MIN_MODULE_HITS = 1

FIGURE_PATH = FIGURE_DIR / "fig_tcell_marker_hierarchy.pdf"
FIGURE_PNG_PATH = FIGURE_DIR / "fig_tcell_marker_hierarchy.png"
PROFILE_PATH = RESULTS_DIR / "tcell_marker_hierarchy_profiles.tsv"
PROGRAM_PATH = RESULTS_DIR / "tcell_marker_hierarchy_programs.tsv"
GENE_SCORE_PATH = RESULTS_DIR / "tcell_marker_hierarchy_gene_scores.tsv"
REPORT_PATH = RESULTS_DIR / "tcell_marker_hierarchy_report.md"

STATE_MODULES = OrderedDict(
    [
        ("T cell lineage", ["CD3D", "CD3E", "CD2", "LCK", "ZAP70"]),
        ("Naive/memory", ["CCR7", "SELL", "TCF7", "LEF1", "IL7R", "KLF2"]),
        ("Cytotoxic", ["NKG7", "GNLY", "PRF1", "GZMA", "GZMB", "GZMH", "GZMK", "CCL5"]),
        ("Exhaustion", ["PDCD1", "LAG3", "HAVCR2", "TIGIT", "TOX", "CXCL13", "CTLA4"]),
        ("Regulatory", ["FOXP3", "IL2RA", "IKZF2", "TNFRSF18", "TNFRSF4"]),
        ("Proliferation", ["MKI67", "TOP2A", "STMN1", "TYMS"]),
        ("Residency", ["ITGAE", "CXCR6", "ZNF683", "CD69"]),
        ("Activation", ["IFNG", "CCL3", "CCL4", "CD38"]),
    ]
)

MODULE_COLORS = {
    "T cell lineage": "#5B8FA8",
    "Naive/memory": "#A8D8CF",
    "Cytotoxic": "#D97B66",
    "Exhaustion": "#8E6BBE",
    "Regulatory": "#DDA15E",
    "Proliferation": "#C44E52",
    "Residency": "#7A9E7E",
    "Activation": "#E0C36E",
}


def marker_sets(profiles_df: pd.DataFrame) -> list[set[str]]:
    return [set(split_marker_text(marker_ids)) for marker_ids in profiles_df["marker_ids"]]


def build_name_to_ids(records_df: pd.DataFrame) -> dict[str, list[str]]:
    subset = records_df.loc[
        records_df["feature_name_std"].ne("") & records_df["feature_id_std"].ne(""),
        ["feature_name_std", "feature_id_std"],
    ].drop_duplicates()
    return (
        subset.groupby("feature_name_std")["feature_id_std"]
        .agg(lambda values: sorted(set(values)))
        .to_dict()
    )


def module_gene_rows(name_to_ids: dict[str, list[str]], gene_vocab: set[str]) -> pd.DataFrame:
    rows = []
    used_gene_ids: set[str] = set()
    for module, gene_names in STATE_MODULES.items():
        for gene_name in gene_names:
            matching_ids = [gene_id for gene_id in name_to_ids.get(gene_name, []) if gene_id in gene_vocab]
            for gene_id in matching_ids:
                if gene_id in used_gene_ids:
                    continue
                used_gene_ids.add(gene_id)
                rows.append({"module": module, "gene_name": gene_name, "gene_id": gene_id})
    return pd.DataFrame(rows)


def profile_module_scores(
    profile_gene_sets: list[set[str]],
    module_genes_df: pd.DataFrame,
) -> pd.DataFrame:
    module_to_ids = (
        module_genes_df.groupby("module")["gene_id"].agg(lambda values: set(values)).to_dict()
        if not module_genes_df.empty
        else {}
    )
    rows = []
    for profile_idx, genes in enumerate(profile_gene_sets):
        row = {"profile_index": profile_idx}
        best_module = "Other"
        best_count = 0
        for module in STATE_MODULES:
            count = len(genes & module_to_ids.get(module, set()))
            row[f"{module}_hits"] = count
            if count > best_count and module != "T cell lineage":
                best_module = module
                best_count = count
        row["dominant_module"] = best_module if best_count > 0 else "Other"
        rows.append(row)
    return pd.DataFrame(rows)


def ordered_cluster_labels(raw_clusters: np.ndarray, leaves: list[int]) -> np.ndarray:
    seen = []
    for leaf in leaves:
        cluster = raw_clusters[leaf]
        if cluster not in seen:
            seen.append(cluster)
    cluster_map = {cluster: idx + 1 for idx, cluster in enumerate(seen)}
    return np.array([cluster_map[cluster] for cluster in raw_clusters])


def summarize_programs(tcell_df: pd.DataFrame, profile_gene_sets: list[set[str]], id_to_name: dict[str, str]) -> pd.DataFrame:
    rows = []
    program_order = [module for module in STATE_MODULES if module != "T cell lineage"] + ["Other"]
    for program in program_order:
        cluster_df = tcell_df.loc[tcell_df["dominant_module"].eq(program)]
        if cluster_df.empty:
            continue
        indices = cluster_df["profile_index"].to_numpy()
        cluster_gene_sets = [profile_gene_sets[idx] for idx in indices]
        cluster_genes = set().union(*cluster_gene_sets) if cluster_gene_sets else set()
        gene_stats = []
        for gene_id in cluster_genes:
            inside = sum(gene_id in genes for genes in cluster_gene_sets)
            global_count = sum(gene_id in genes for genes in profile_gene_sets)
            coverage = inside / len(cluster_gene_sets) if cluster_gene_sets else 0.0
            purity = inside / global_count if global_count else 0.0
            strength = 2 * coverage * purity / (coverage + purity) if coverage + purity else 0.0
            gene_stats.append((strength, coverage, purity, inside, gene_id))
        top_genes = [
            id_to_name.get(gene_id, gene_id)
            for _, _, _, _, gene_id in sorted(gene_stats, reverse=True)[:8]
        ]
        module_fraction = {
            module: float((cluster_df[f"{module}_hits"] > 0).mean())
            for module in STATE_MODULES
        }
        top_modules = sorted(module_fraction.items(), key=lambda item: item[1], reverse=True)[:3]
        top_labels = (
            cluster_df["cell_type"]
            .value_counts()
            .head(5)
            .rename_axis("label")
            .reset_index(name="count")
        )
        rows.append(
            {
                "program": program,
                "profiles": len(cluster_df),
                "papers": cluster_df["paper_key"].nunique(),
                "labels": cluster_df["cell_type"].nunique(),
                "module_fraction": "; ".join(f"{module} ({fraction:.2f})" for module, fraction in top_modules if fraction > 0),
                "top_marker_genes": "; ".join(top_genes),
                "top_labels": "; ".join(f"{row.label} ({row.count})" for row in top_labels.itertuples(index=False)),
                **{f"module_fraction_{module}": fraction for module, fraction in module_fraction.items()},
            }
        )
    return pd.DataFrame(rows)


def score_program_genes(tcell_df: pd.DataFrame, profile_gene_sets: list[set[str]], id_to_name: dict[str, str]) -> pd.DataFrame:
    rows = []
    n_profiles = len(profile_gene_sets)
    all_genes = sorted(set().union(*profile_gene_sets)) if profile_gene_sets else []
    global_counts = {gene_id: sum(gene_id in genes for genes in profile_gene_sets) for gene_id in all_genes}
    program_order = [module for module in STATE_MODULES if module != "T cell lineage"] + ["Other"]
    for program in program_order:
        cluster_df = tcell_df.loc[tcell_df["dominant_module"].eq(program)]
        if cluster_df.empty:
            continue
        indices = cluster_df["profile_index"].to_numpy()
        inside_sets = [profile_gene_sets[idx] for idx in indices]
        outside_n = n_profiles - len(inside_sets)
        for gene_id in sorted(set().union(*inside_sets)):
            inside = sum(gene_id in genes for genes in inside_sets)
            outside = global_counts[gene_id] - inside
            coverage = inside / len(inside_sets) if inside_sets else 0.0
            purity = inside / global_counts[gene_id] if global_counts[gene_id] else 0.0
            outside_prevalence = outside / outside_n if outside_n else 0.0
            strength = 2 * coverage * purity / (coverage + purity) if coverage + purity else 0.0
            rows.append(
                {
                    "program": program,
                    "gene_id": gene_id,
                    "gene_name": id_to_name.get(gene_id, gene_id),
                    "profiles_in_cluster": len(inside_sets),
                    "profiles_with_gene_in_cluster": inside,
                    "profiles_with_gene_total": global_counts[gene_id],
                    "coverage": coverage,
                    "purity": purity,
                    "outside_prevalence": outside_prevalence,
                    "marker_strength": strength,
                }
            )
    return pd.DataFrame(rows).sort_values(
        ["program", "marker_strength", "profiles_with_gene_in_cluster"],
        ascending=[True, False, False],
    )


def markdown_table(df: pd.DataFrame) -> str:
    """Write a small GitHub-flavored markdown table without optional dependencies."""
    if df.empty:
        return "_No rows._"
    text_df = df.copy()
    for column in text_df.columns:
        if pd.api.types.is_float_dtype(text_df[column]):
            text_df[column] = text_df[column].map(lambda value: f"{value:.3f}")
        else:
            text_df[column] = text_df[column].astype(str)
        text_df[column] = text_df[column].str.replace("|", "\\|", regex=False)
    header = "| " + " | ".join(text_df.columns) + " |"
    divider = "| " + " | ".join(["---"] * len(text_df.columns)) + " |"
    rows = ["| " + " | ".join(row) + " |" for row in text_df.to_numpy()]
    return "\n".join([header, divider, *rows])


def plot_hierarchy(
    linkage_matrix: np.ndarray,
    leaves: list[int],
    display_df: pd.DataFrame,
    plot_matrix: np.ndarray,
    module_genes_df: pd.DataFrame,
    program_summary_df: pd.DataFrame,
) -> None:
    fig = plt.figure(figsize=(7.4, 4.8))
    grid = fig.add_gridspec(
        3,
        2,
        width_ratios=[3.8, 1.2],
        height_ratios=[0.68, 3.1, 0.2],
        wspace=0.32,
        hspace=0.04,
    )
    ax_tree = fig.add_subplot(grid[0, 0])
    ax_heat = fig.add_subplot(grid[1, 0])
    ax_strip = fig.add_subplot(grid[2, 0])
    ax_program = fig.add_subplot(grid[:, 1])

    dendrogram(linkage_matrix, ax=ax_tree, no_labels=True, color_threshold=0, above_threshold_color="#555555")
    for collection in ax_tree.collections:
        collection.set_linewidth(0.35)
    ax_tree.set_ylabel("Jaccard\ndistance", fontsize=7.5)
    ax_tree.tick_params(axis="both", labelsize=6, length=2)
    ax_tree.spines["top"].set_visible(False)
    ax_tree.spines["right"].set_visible(False)
    ax_tree.spines["bottom"].set_visible(False)

    ordered_matrix = plot_matrix[:, leaves]
    ax_heat.imshow(ordered_matrix, aspect="auto", interpolation="nearest", cmap=ListedColormap(["white", "#222222"]))
    ax_heat.set_yticks(np.arange(len(module_genes_df)))
    ax_heat.set_yticklabels(module_genes_df["gene_name"], fontsize=6.4)
    ax_heat.set_xticks([])
    ax_heat.tick_params(axis="y", length=0)
    for spine in ax_heat.spines.values():
        spine.set_visible(False)

    current_module = None
    for row_idx, module in enumerate(module_genes_df["module"]):
        ax_heat.add_patch(
            plt.Rectangle(
                (-4.4, row_idx - 0.5),
                2.8,
                1,
                facecolor=MODULE_COLORS[module],
                edgecolor="none",
                clip_on=False,
            )
        )
        if module != current_module:
            ax_heat.axhline(row_idx - 0.5, color="#BDBDBD", linewidth=0.5)
            current_module = module
    ax_heat.axhline(len(module_genes_df) - 0.5, color="#BDBDBD", linewidth=0.5)
    ax_heat.set_title("Selected state genes", loc="left", fontsize=7.5, pad=2)

    ordered_programs = display_df.iloc[leaves]["dominant_module"].to_numpy()
    program_order = [module for module in STATE_MODULES if module != "T cell lineage"] + ["Other"]
    program_to_idx = {program: idx for idx, program in enumerate(program_order)}
    program_palette = np.array(
        [
            MODULE_COLORS.get(program, "#BDBDBD")
            for program in program_order
        ]
    )
    strip_values = np.array([[program_to_idx.get(program, program_to_idx["Other"]) for program in ordered_programs]])
    ax_strip.imshow(strip_values, aspect="auto", interpolation="nearest", cmap=ListedColormap(program_palette))
    ax_strip.set_xticks([])
    ax_strip.set_yticks([])
    for spine in ax_strip.spines.values():
        spine.set_visible(False)

    plot_summary = program_summary_df.loc[program_summary_df["program"].ne("Other")].copy()
    plot_summary["program"] = pd.Categorical(plot_summary["program"], categories=program_order, ordered=True)
    plot_summary = plot_summary.sort_values("program")
    y = np.arange(len(plot_summary))
    colors = [MODULE_COLORS.get(program, "#BDBDBD") for program in plot_summary["program"]]
    ax_program.barh(y, plot_summary["profiles"], color=colors, edgecolor="#222222", linewidth=0.45)
    ax_program.set_yticks(y)
    ax_program.set_yticklabels(plot_summary["program"], fontsize=6.5)
    ax_program.invert_yaxis()
    ax_program.set_xlabel("Profiles", fontsize=7.5)
    ax_program.set_title("Dominant\nstate program", fontsize=7.5)
    ax_program.tick_params(axis="x", labelsize=6, length=2)
    ax_program.tick_params(axis="y", length=0)
    ax_program.spines["top"].set_visible(False)
    ax_program.spines["right"].set_visible(False)
    for row in plot_summary.itertuples(index=False):
        row_idx = int(np.where(plot_summary["program"].to_numpy() == row.program)[0][0])
        ax_program.text(row.profiles + 1, row_idx, str(row.profiles), va="center", ha="left", fontsize=6)
    xmax = max(plot_summary["profiles"].max() * 1.18, 10)
    ax_program.set_xlim(0, xmax)

    fig.suptitle("T-cell marker-profile hierarchy", fontsize=9.5, y=0.985)
    fig.text(
        0.015,
        0.01,
        "Leaves are paper-celltype marker profiles with at least one selected state gene, ordered by full binary marker-gene Jaccard distance.",
        ha="left",
        va="bottom",
        fontsize=6.4,
    )
    fig.savefig(FIGURE_PATH, bbox_inches="tight")
    fig.savefig(FIGURE_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)


def write_report(
    tcell_df: pd.DataFrame,
    display_df: pd.DataFrame,
    program_summary_df: pd.DataFrame,
    gene_score_df: pd.DataFrame,
    module_genes_df: pd.DataFrame,
) -> None:
    report = [
        "# T-cell Marker Hierarchy Prototype",
        "",
        "## Assumptions",
        "",
        "- Unit of analysis is one paper-celltype marker profile: a paper, a reported cell type label, and a binary vector of mapped Ensembl gene IDs.",
        "- Profiles are restricted to human, source-verified marker records with at least three mapped marker genes.",
        "- T-cell profiles are selected by the existing regex-based neighborhood assignment; mixed T/NK labels are not included in this first pass.",
        "- The displayed hierarchy is built from full marker-gene Jaccard distance, not from the selected state genes shown in the heatmap.",
        "- The display is restricted to profiles with at least one selected immune-state gene so the heatmap is readable.",
        "- State-gene modules are manually specified immune programs used to interpret branches; they are not learned from the data or proposed as a taxonomy.",
        "",
        "## Outputs",
        "",
        f"- Figure: `{FIGURE_PATH.relative_to(REPO_ROOT)}`",
        f"- Profile annotations: `{PROFILE_PATH.relative_to(REPO_ROOT)}`",
        f"- Program summaries: `{PROGRAM_PATH.relative_to(REPO_ROOT)}`",
        f"- Program gene scores: `{GENE_SCORE_PATH.relative_to(REPO_ROOT)}`",
        "",
        "## Counts",
        "",
        f"- T-cell profiles: {len(tcell_df):,}",
        f"- Displayed module-positive profiles: {len(display_df):,}",
        f"- Papers: {tcell_df['paper_key'].nunique():,}",
        f"- Reported labels: {tcell_df['cell_type'].nunique():,}",
        f"- State genes shown: {len(module_genes_df):,}",
        "",
        "## Program Summary",
        "",
        markdown_table(
            program_summary_df[
                ["program", "profiles", "papers", "labels", "module_fraction", "top_marker_genes", "top_labels"]
            ]
        ),
        "",
        "## Top Program Genes",
        "",
    ]
    for program, group in gene_score_df.groupby("program", sort=False):
        report.extend(
            [
                f"### {program}",
                "",
                group[
                    [
                        "gene_name",
                        "profiles_with_gene_in_cluster",
                        "profiles_with_gene_total",
                        "coverage",
                        "purity",
                        "marker_strength",
                    ]
                ]
                .head(12)
                .pipe(markdown_table),
                "",
            ]
        )
    REPORT_PATH.write_text("\n".join(report))


def main() -> None:
    records_df = build_records()
    profiles_df, filtered_profiles_df, _filtered_profiles, id_to_name = build_profile_summary(
        records_df,
        min_markers=MIN_MARKERS,
        feature_id_col="feature_id_std",
        feature_name_col="feature_name_std",
    )
    filtered_profiles_df["neighborhood"] = filtered_profiles_df["cell_type"].map(assign_neighborhood)
    tcell_df = filtered_profiles_df.loc[filtered_profiles_df["neighborhood"].eq("T cell")].copy().reset_index(drop=True)
    if len(tcell_df) < 2:
        raise SystemExit("Not enough T-cell profiles to cluster.")

    tcell_df["profile_index"] = np.arange(len(tcell_df))
    profile_gene_sets = marker_sets(tcell_df)
    gene_vocab = sorted(set().union(*profile_gene_sets))
    gene_to_col = {gene_id: idx for idx, gene_id in enumerate(gene_vocab)}
    binary = np.zeros((len(tcell_df), len(gene_vocab)), dtype=np.uint8)
    for row_idx, genes in enumerate(profile_gene_sets):
        for gene_id in genes:
            binary[row_idx, gene_to_col[gene_id]] = 1

    name_to_ids = build_name_to_ids(records_df)
    module_genes_df = module_gene_rows(name_to_ids, set(gene_vocab))
    module_scores_df = profile_module_scores(profile_gene_sets, module_genes_df)
    tcell_df = tcell_df.merge(module_scores_df, on="profile_index", how="left")

    module_hit_cols = [f"{module}_hits" for module in STATE_MODULES]
    tcell_df["selected_state_gene_hits"] = tcell_df[module_hit_cols].sum(axis=1)
    display_df = tcell_df.loc[tcell_df["selected_state_gene_hits"].ge(DISPLAY_MIN_MODULE_HITS)].copy().reset_index(drop=True)
    display_indices = display_df["profile_index"].to_numpy()
    display_binary = binary[display_indices, :]
    display_distances = pdist(display_binary, metric="jaccard")
    display_distances = np.nan_to_num(display_distances, nan=0.0)
    display_linkage_matrix = linkage(display_distances, method="average", optimal_ordering=True)
    display_leaves = dendrogram(display_linkage_matrix, no_plot=True)["leaves"]

    plot_gene_ids = module_genes_df["gene_id"].tolist()
    plot_matrix = display_binary[:, [gene_to_col[gene_id] for gene_id in plot_gene_ids]].T

    program_summary_df = summarize_programs(tcell_df, profile_gene_sets, id_to_name)
    gene_score_df = score_program_genes(tcell_df, profile_gene_sets, id_to_name)

    tcell_df.to_csv(PROFILE_PATH, sep="\t", index=False)
    program_summary_df.to_csv(PROGRAM_PATH, sep="\t", index=False)
    gene_score_df.to_csv(GENE_SCORE_PATH, sep="\t", index=False)
    plot_hierarchy(display_linkage_matrix, display_leaves, display_df, plot_matrix, module_genes_df, program_summary_df)
    write_report(tcell_df, display_df, program_summary_df, gene_score_df, module_genes_df)

    print(f"T-cell profiles: {len(tcell_df):,}")
    print(f"Displayed module-positive profiles: {len(display_df):,}")
    print(f"Papers: {tcell_df['paper_key'].nunique():,}")
    print(f"Labels: {tcell_df['cell_type'].nunique():,}")
    print(f"State genes shown: {len(module_genes_df):,}")
    print(f"Wrote {FIGURE_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
