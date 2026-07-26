from __future__ import annotations

import json
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.lines import Line2D

from cross_study_gene_space import (
    REPO_ROOT,
    RESULTS_DIR,
    build_profile_summary,
    normalize_text,
    split_marker_text,
    standardize_marker_records,
)


DATASETS = {
    "biorxiv": REPO_ROOT / "data" / "biorxiv" / "meca",
    "hca": REPO_ROOT / "data" / "hca" / "manuscripts",
}

MIN_MARKERS = 3
EPS = 1e-6

SCORES_PATH = RESULTS_DIR / "marker_corpus_scores.tsv"
REPORT_PATH = RESULTS_DIR / "marker_corpus_examples.md"
FIGURES_DIR = REPO_ROOT / "analysis" / "figures"
PLOT_PATH = FIGURES_DIR / "marker_strength_coverage_purity.pdf"
PLOT_PNG_PATH = FIGURES_DIR / "marker_strength_coverage_purity.png"
PAGES_PATH = FIGURES_DIR / "marker_strength_coverage_purity_pages.pdf"
CCDF_PATH = FIGURES_DIR / "marker_strength_reverse_cdf.pdf"
CCDF_PNG_PATH = FIGURES_DIR / "marker_strength_reverse_cdf.png"
MAIN_PLOT_PATH = FIGURES_DIR / "fig_marker_stability.pdf"
MAIN_PLOT_PNG_PATH = FIGURES_DIR / "fig_marker_stability.png"

PUTATIVE_CELL_TYPE_MARKERS = {
    "CD3D",
    "CD3E",
    "CD14",
    "CD19",
    "CD68",
    "CD79A",
    "CD79B",
    "CD1C",
    "CDH5",
    "CLEC9A",
    "CLDN5",
    "DCN",
    "KLRD1",
    "KRT5",
    "KRT14",
    "MS4A1",
    "NCAM1",
    "NKG7",
    "PECAM1",
    "PDGFRA",
    "VWF",
}

PUTATIVE_CELL_STATE_MARKERS = {
    "C1QB",
    "CCR7",
    "CD27",
    "CD38",
    "CTLA4",
    "FCGR3A",
    "GZMK",
    "IL7R",
    "LAG3",
    "LEF1",
    "MUC2",
    "MZB1",
    "PDCD1",
    "SELL",
    "TCF7",
    "TIGIT",
    "VCAN",
    "XBP1",
}

SPOTLIGHT_GENES = [
    "CD14",
    "CD68",
    "CD79A",
    "MS4A1",
    "PECAM1",
    "VWF",
    "CLEC9A",
    "CD1C",
    "KRT5",
    "MUC2",
    "C1QB",
    "VCAN",
    "CCR7",
    "SELL",
    "TCF7",
    "GZMK",
]

MAIN_NEIGHBORHOODS = [
    "T cell",
    "monocyte/macrophage",
    "B cell",
    "dendritic cell",
    "epithelial",
    "endothelial",
]

MAIN_LABEL_GENES = {
    "T cell": ["CD3D", "CD3E", "CCR7", "SELL", "TCF7", "GZMK"],
    "monocyte/macrophage": ["CD14", "CD68", "C1QB", "VCAN", "S100A8", "S100A9"],
    "B cell": ["CD79A", "MS4A1", "CD19", "CD27", "MZB1"],
    "dendritic cell": ["CLEC9A", "CD1C", "BATF3", "VCAN"],
    "epithelial": ["KRT5", "KRT14", "TP63", "MUC2", "EPCAM"],
    "endothelial": ["PECAM1", "VWF", "CDH5", "CLDN5"],
}

CATEGORY_STYLES = {
    "putative cell-type marker": {"marker": "o", "facecolor": "white"},
    "putative cell-state marker": {"marker": "^", "facecolor": "#D9D9D9"},
}


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def clean_upper(value: object) -> str:
    return clean_text(value).upper()


def maybe_float(value: object) -> float:
    if value in (None, ""):
        return np.nan
    try:
        return float(value)
    except (TypeError, ValueError):
        return np.nan


def extract_hca_doi(folder_name: str) -> str:
    parts = folder_name.split("_")
    if len(parts) >= 3 and parts[1].startswith("10."):
        return parts[1]
    return ""


def iter_marker_records(source_corpus: str, base_dir: Path):
    for markers_path in sorted(base_dir.rglob("markers.json")):
        paper_dir = markers_path.parent
        try:
            markers = json.loads(markers_path.read_text())
        except Exception:
            continue
        if not isinstance(markers, list):
            continue

        manuscript_path = paper_dir / "manuscript.md"
        paper_id = paper_dir.name
        paper_key = f"{source_corpus}:{paper_id}"
        paper_doi = extract_hca_doi(paper_id) if source_corpus == "hca" else ""

        for row_idx, marker in enumerate(markers):
            verification = marker.get("_verification") or {}
            yield {
                "source_corpus": source_corpus,
                "paper_id": paper_id,
                "paper_key": paper_key,
                "paper_doi": paper_doi,
                "record_index": row_idx,
                "markers_path": str(markers_path.relative_to(REPO_ROOT)),
                "manuscript_path": str(manuscript_path.relative_to(REPO_ROOT)) if manuscript_path.exists() else "",
                "source_type": clean_text(marker.get("source_type")),
                "source_id": clean_text(marker.get("source_id")),
                "data_id": clean_text(marker.get("data_id")),
                "organism": clean_text(marker.get("organism")).lower(),
                "group_label": clean_text(marker.get("group_label")),
                "group_name": clean_text(marker.get("group_name")),
                "group_name_norm": clean_upper(marker.get("group_name")),
                "feature_label": clean_text(marker.get("feature_label")),
                "feature_name": clean_text(marker.get("feature_name")),
                "feature_name_norm": clean_upper(marker.get("feature_name")),
                "feature_id": clean_text(marker.get("feature_id")),
                "metrics_rank": maybe_float(marker.get("metrics_rank")),
                "metrics_logfc": maybe_float(marker.get("metrics_logfc")),
                "metrics_pcorr": maybe_float(marker.get("metrics_pcorr")),
                "source_rationale": clean_text(marker.get("source_rationale")),
                "source_rationale_found": bool(verification.get("source_rationale_found")),
                "group_label_found": bool(verification.get("group_label_found")),
                "feature_label_found": bool(verification.get("feature_label_found")),
                "all_verified": bool(verification.get("all_verified")),
            }


def normalize_label(value: object) -> str:
    label = clean_upper(value)
    label = label.replace("Ï", "I")
    label = re.sub(r"[^A-Z0-9+/.-]+", " ", label)
    return re.sub(r"\s+", " ", label).strip()


NEIGHBORHOOD_RULES = [
    ("NK cell", re.compile(r"\b(NK|NATURAL KILLER|NKG7|GNLY)\b")),
    (
        "T cell",
        re.compile(
            r"\b(T[\s-]*CELL|T[\s-]*CELLS|CD4|CD8|TREG|TREG\.|NAIVE T|NAIVE CD4|"
            r"TCM|TEM|TRM|TEMRA|TN|MAIT|CYTOTOXIC T|EXHAUSTED T|T/NK)\b"
        ),
    ),
    ("B cell", re.compile(r"\b(B[\s-]*CELL|B[\s-]*CELLS|B LYMPH|PLASMA|PLASMABLAST|DN2 CELL)\b")),
    (
        "monocyte/macrophage",
        re.compile(r"\b(MONOCYTE|MONOCYTES|MACROPHAGE|MACROPHAGES|MAC|MYELOID|MDSC|MICROGLIA|TRAM|MOAM)\b"),
    ),
    ("dendritic cell", re.compile(r"\b(DENDRITIC|PDC|CDC1|CDC2|CDC| DC |MIGRATORY DC)\b")),
    ("epithelial", re.compile(r"\b(EPITHELIAL|EPIDERMIS|KERATINOCYTE|BASAL|CILIATED|SECRETORY|GOBLET|ENTEROCYTE)\b")),
    ("fibroblast/stromal", re.compile(r"\b(FIBROBLAST|STROMAL|CAF|MESENCHYMAL|SMC|SMOOTH MUSCLE|PERICYTE)\b")),
    ("endothelial", re.compile(r"\b(ENDOTHELIAL|VASCULAR|LYMPHATIC)\b")),
]


def assign_neighborhood(label: object) -> str:
    normalized = f" {normalize_label(label)} "
    hits = [name for name, pattern in NEIGHBORHOOD_RULES if pattern.search(normalized)]
    if len(hits) > 1 and {"T cell", "NK cell"}.issubset(set(hits)):
        return "T/NK cell"
    return hits[0] if hits else ""


def entropy(values: pd.Series) -> float:
    counts = values.value_counts()
    if counts.empty:
        return 0.0
    probabilities = counts / counts.sum()
    return float(-(probabilities * np.log2(probabilities)).sum())


def reviewed_gene_sets(name_to_ids: dict[str, set[str]]) -> tuple[set[str], set[str]]:
    context_signal_ids: set[str] = set()
    state_bridge_ids: set[str] = set()

    same_label_path = RESULTS_DIR / "cross_study_row3_name_judgment_same_label_partial.tsv"
    if same_label_path.exists():
        same_label = pd.read_csv(same_label_path, sep="\t").fillna("")
        context_rows = same_label.loc[
            same_label["name_judgment"].eq("Context distinction")
            | same_label["review_resolution_class"].eq("same_entity_state_context")
        ]
        for row in context_rows.itertuples(index=False):
            for gene_name in split_marker_text(row.unique_markers_1) + split_marker_text(row.unique_markers_2):
                context_signal_ids.update(name_to_ids.get(normalize_text(gene_name).upper(), set()))

    diff_label_path = RESULTS_DIR / "cross_study_row3_name_judgment_diff_labels_j1.tsv"
    if diff_label_path.exists():
        diff_label = pd.read_csv(diff_label_path, sep="\t").fillna("")
        context_rows = diff_label.loc[diff_label["name_judgment"].eq("Context distinction")]
        for row in context_rows.itertuples(index=False):
            for gene_name in split_marker_text(row.markers_1):
                state_bridge_ids.update(name_to_ids.get(normalize_text(gene_name).upper(), set()))

    return context_signal_ids, state_bridge_ids


def build_records() -> pd.DataFrame:
    records = []
    for source_corpus, base_dir in DATASETS.items():
        records.extend(iter_marker_records(source_corpus, base_dir))
    records_df = pd.DataFrame(records)
    if records_df.empty:
        return records_df

    records_df = standardize_marker_records(records_df)
    canonical_df = records_df.loc[
        records_df["organism"].eq("homo_sapiens")
        & records_df["feature_id_std"].ne("")
        & records_df["group_name_norm"].ne("")
        & records_df["all_verified"]
    ].copy()
    canonical_df = (
        canonical_df.sort_values(["source_corpus", "paper_id", "group_name_norm", "feature_id_std", "record_index"])
        .drop_duplicates(subset=["source_corpus", "paper_id", "group_name_norm", "feature_id_std"], keep="first")
        .reset_index(drop=True)
    )
    return canonical_df


def build_profile_gene_table(filtered_profiles_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for row in filtered_profiles_df.itertuples(index=False):
        profile_uid = f"{row.source_corpus}|{row.paper_id}|{row.cell_type}"
        for gene_id in split_marker_text(row.marker_ids):
            rows.append(
                {
                    "profile_uid": profile_uid,
                    "source_corpus": row.source_corpus,
                    "paper_id": row.paper_id,
                    "paper_key": row.paper_key,
                    "cell_type": row.cell_type,
                    "neighborhood": row.neighborhood,
                    "gene_id": gene_id,
                }
            )
    return pd.DataFrame(rows)


def classify_marker_category(row: pd.Series) -> str:
    gene_name = clean_upper(row["gene_name"])

    if (
        gene_name in PUTATIVE_CELL_TYPE_MARKERS
        and row["prevalence"] >= 0.05
        and row["cluster_purity"] >= 0.25
        and row["n_papers_with_gene"] >= 5
    ):
        return "putative cell-type marker"

    if gene_name in PUTATIVE_CELL_STATE_MARKERS or row["reviewed_context_signal"] or row["reviewed_state_bridge"]:
        return "putative cell-state marker"

    if (
        row["prevalence"] >= 0.10
        and row["cluster_purity"] >= 0.35
        and row["n_papers_with_gene"] >= 5
        and row["n_cell_type_labels_with_gene"] >= 2
        and row["specificity_ratio"] >= 5.0
    ):
        return "putative cell-type marker"

    if (
        row["prevalence"] < 0.10
        and row["cluster_purity"] >= 0.30
        and row["n_papers_with_gene"] >= 3
        and row["specificity_ratio"] >= 5.0
    ):
        return "putative cell-state marker"

    return ""


def format_float(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{value:.2f}"


def markdown_table(df: pd.DataFrame, columns: list[str], limit: int | None = None) -> str:
    table = df.loc[:, columns].copy()
    if limit is not None:
        table = table.head(limit)
    if table.empty:
        return "_No rows._"
    display = table.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(format_float)
        else:
            display[col] = display[col].map(lambda value: str(value).replace("\n", " ").replace("|", "\\|"))

    header = "| " + " | ".join(display.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(display.columns)) + " |"
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in display.itertuples(index=False, name=None)
    ]
    return "\n".join([header, separator, *rows])


def label_rows_for_plot(df: pd.DataFrame, max_labels: int = 12) -> pd.DataFrame:
    candidates = df.loc[df["marker_category"].ne("")].copy()
    spotlight = candidates.loc[candidates["gene_name"].isin(SPOTLIGHT_GENES)].sort_values(
        ["marker_strength", "n_papers_with_gene"],
        ascending=[False, False],
    )
    reviewed = candidates.loc[candidates["reviewed_context_signal"] | candidates["reviewed_state_bridge"]].sort_values(
        ["marker_strength", "n_papers_with_gene"],
        ascending=[False, False],
    )
    strong = candidates.sort_values(
        ["marker_strength", "n_papers_with_gene"],
        ascending=[False, False],
    )
    labeled = pd.concat([strong.head(4), spotlight, reviewed.head(4)], ignore_index=True)
    return labeled.drop_duplicates("gene_id").head(max_labels)


def label_rows_for_main_plot(df: pd.DataFrame, neighborhood: str) -> pd.DataFrame:
    preferred = MAIN_LABEL_GENES.get(neighborhood, [])
    preferred_order = {gene: idx for idx, gene in enumerate(preferred)}
    labeled = df.loc[df["gene_name"].isin(preferred)].copy()
    if labeled.empty:
        labeled = label_rows_for_plot(df, max_labels=5)
    else:
        labeled["preferred_order"] = labeled["gene_name"].map(preferred_order)
        labeled = labeled.sort_values(["preferred_order", "marker_strength"], ascending=[True, False])
    return labeled.drop_duplicates("gene_id").head(6)


def plot_neighborhood(ax: plt.Axes, df: pd.DataFrame, neighborhood: str, max_labels: int = 0) -> None:
    plot_df = df.loc[df["neighborhood"].eq(neighborhood)].copy()
    if plot_df.empty:
        ax.axis("off")
        return

    sizes = 12 + 10 * np.sqrt(plot_df["n_papers_with_gene"].clip(lower=1))
    ax.scatter(
        plot_df["prevalence"],
        plot_df["cluster_purity"],
        s=sizes,
        c="#6E6E6E",
        edgecolors="none",
        alpha=0.55,
        zorder=2,
    )

    if max_labels:
        labeled = label_rows_for_plot(plot_df, max_labels=max_labels)
        for category, style in CATEGORY_STYLES.items():
            label_df = labeled.loc[labeled["marker_category"].eq(category)]
            if label_df.empty:
                continue
            ax.scatter(
                label_df["prevalence"],
                label_df["cluster_purity"],
                s=42,
                marker=style["marker"],
                facecolors=style["facecolor"],
                edgecolors="#111111",
                linewidths=0.8,
                zorder=4,
            )

        ordered = labeled.sort_values(["cluster_purity", "prevalence"], ascending=[False, False]).reset_index(drop=True)
        y_positions = np.linspace(0.90, 0.16, len(ordered))
        for text_y, row in zip(y_positions, ordered.itertuples(index=False), strict=True):
            ax.annotate(
                row.gene_name,
                xy=(row.prevalence, row.cluster_purity),
                xycoords="data",
                xytext=(0.63, text_y),
                textcoords="axes fraction",
                ha="left",
                va="center",
                fontsize=6.5,
                color="#111111",
                arrowprops={
                    "arrowstyle": "-",
                    "color": "#555555",
                    "linewidth": 0.55,
                    "shrinkA": 1,
                    "shrinkB": 3,
                },
                zorder=5,
            )

    ax.set_title(f"{neighborhood} ({len(plot_df):,} genes)", fontsize=10)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.tick_params(labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def plot_main_neighborhood(ax: plt.Axes, df: pd.DataFrame, neighborhood: str) -> None:
    plot_df = df.loc[df["neighborhood"].eq(neighborhood)].copy()
    if plot_df.empty:
        ax.axis("off")
        return

    sizes = 10 + 7 * np.sqrt(plot_df["n_papers_with_gene"].clip(lower=1))
    ax.scatter(
        plot_df["prevalence"],
        plot_df["cluster_purity"],
        s=sizes,
        c="#7A7A7A",
        edgecolors="none",
        alpha=0.5,
        zorder=2,
    )

    labeled = label_rows_for_main_plot(plot_df, neighborhood)
    for category, style in CATEGORY_STYLES.items():
        label_df = labeled.loc[labeled["marker_category"].eq(category)]
        if label_df.empty:
            continue
        ax.scatter(
            label_df["prevalence"],
            label_df["cluster_purity"],
            s=38,
            marker=style["marker"],
            facecolors=style["facecolor"],
            edgecolors="#111111",
            linewidths=0.8,
            zorder=4,
        )

    if not labeled.empty:
        ordered = labeled.sort_values(["cluster_purity", "prevalence"], ascending=[False, False]).reset_index(drop=True)
        y_positions = np.linspace(0.86, 0.18, len(ordered))
        for text_y, row in zip(y_positions, ordered.itertuples(index=False), strict=True):
            ax.annotate(
                row.gene_name,
                xy=(row.prevalence, row.cluster_purity),
                xycoords="data",
                xytext=(0.62, text_y),
                textcoords="axes fraction",
                ha="left",
                va="center",
                fontsize=6.7,
                color="#111111",
                arrowprops={
                    "arrowstyle": "-",
                    "color": "#555555",
                    "linewidth": 0.5,
                    "shrinkA": 1,
                    "shrinkB": 3,
                },
                zorder=5,
            )

    n_profiles = int(plot_df["n_profiles_neighborhood"].max())
    ax.set_title(f"{neighborhood} ({n_profiles:,} profiles)", fontsize=8.8)
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.tick_params(labelsize=7.2, length=2.5, width=0.6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(0.7)
    ax.spines["bottom"].set_linewidth(0.7)


def plot_main_prevalence_landscape(scores_df: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(7.1, 4.7), squeeze=False)
    for ax, neighborhood in zip(axes.ravel(), MAIN_NEIGHBORHOODS, strict=True):
        plot_main_neighborhood(ax, scores_df, neighborhood)

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker=style["marker"],
            color="none",
            markerfacecolor=style["facecolor"],
            markeredgecolor="#111111",
            markeredgewidth=0.8,
            markersize=5.5,
            label=category,
        )
        for category, style in CATEGORY_STYLES.items()
    ]
    fig.legend(handles=legend_handles, loc="upper center", ncol=2, frameon=False, fontsize=7.4)
    fig.supxlabel("Coverage: P(gene reported | C)", fontsize=8.4)
    fig.supylabel("Purity: P(C | gene reported)", fontsize=8.4)
    fig.tight_layout(rect=(0.035, 0.045, 1, 0.925))
    fig.savefig(MAIN_PLOT_PATH)
    fig.savefig(MAIN_PLOT_PNG_PATH, dpi=300)
    plt.close(fig)


def plot_prevalence_landscape(scores_df: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    neighborhoods = (
        scores_df.groupby("neighborhood")["n_profiles_neighborhood"]
        .max()
        .sort_values(ascending=False)
        .index.tolist()
    )
    ncols = 3
    nrows = math.ceil(len(neighborhoods) / ncols)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(9.5, 3.1 * nrows), squeeze=False)

    for ax, neighborhood in zip(axes.ravel(), neighborhoods, strict=False):
        plot_neighborhood(ax, scores_df, neighborhood, max_labels=5)

    for ax in axes.ravel()[len(neighborhoods):]:
        ax.axis("off")

    legend_handles = [
        Line2D(
            [0],
            [0],
            marker=style["marker"],
            color="none",
            markerfacecolor=style["facecolor"],
            markeredgecolor="#111111",
            markeredgewidth=0.8,
            markersize=6,
            label=category,
        )
        for category, style in CATEGORY_STYLES.items()
    ]
    fig.legend(handles=legend_handles, loc="upper center", ncol=2, frameon=False, fontsize=9)
    fig.supxlabel("Coverage: fraction of profiles in C that report the gene", fontsize=11)
    fig.supylabel("Purity: fraction of gene-reporting profiles assigned to C", fontsize=11)
    fig.tight_layout(rect=(0.03, 0.03, 1, 0.95))
    fig.savefig(PLOT_PATH)
    fig.savefig(PLOT_PNG_PATH, dpi=300)
    plt.close(fig)

    with PdfPages(PAGES_PATH) as pdf:
        for neighborhood in neighborhoods:
            fig, ax = plt.subplots(figsize=(5.2, 5.2))
            plot_neighborhood(ax, scores_df, neighborhood, max_labels=10)
            ax.set_xlabel("Coverage: P(gene reported | C)", fontsize=10)
            ax.set_ylabel("Purity: P(C | gene reported)", fontsize=10)
            fig.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)


def plot_marker_strength_ccdf(scores_df: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    neighborhoods = (
        scores_df.groupby("neighborhood")["n_profiles_neighborhood"]
        .max()
        .sort_values(ascending=False)
        .index.tolist()
    )
    ncols = 3
    nrows = math.ceil(len(neighborhoods) / ncols)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(9.5, 2.8 * nrows), squeeze=False)

    for ax, neighborhood in zip(axes.ravel(), neighborhoods, strict=False):
        plot_df = scores_df.loc[scores_df["neighborhood"].eq(neighborhood)].sort_values("marker_strength").copy()
        if plot_df.empty:
            ax.axis("off")
            continue
        plot_df["ccdf"] = np.arange(len(plot_df), 0, -1) / len(plot_df)
        sizes = 8 + 6 * np.sqrt(plot_df["n_papers_with_gene"].clip(lower=1))

        ax.step(plot_df["marker_strength"], plot_df["ccdf"], where="post", color="#111111", linewidth=0.9, alpha=0.65)
        ax.scatter(
            plot_df["marker_strength"],
            plot_df["ccdf"],
            s=sizes,
            color="#777777",
            alpha=0.45,
            edgecolors="none",
            zorder=2,
        )

        ax.set_title(f"{neighborhood} ({len(plot_df):,} genes)", fontsize=10)
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
        ax.tick_params(labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        labeled = pd.concat(
            [
                plot_df.sort_values("marker_strength", ascending=False).head(4),
                plot_df.loc[plot_df["gene_name"].isin(SPOTLIGHT_GENES)],
                plot_df.loc[plot_df["reviewed_context_signal"] | plot_df["reviewed_state_bridge"]]
                .sort_values("marker_strength", ascending=False)
                .head(3),
            ],
            ignore_index=True,
        ).drop_duplicates("gene_id").head(12)

        if not labeled.empty:
            ax.scatter(
                labeled["marker_strength"],
                labeled["ccdf"],
                s=38,
                facecolors="white",
                edgecolors="#111111",
                linewidths=0.8,
                zorder=4,
            )

            ordered = labeled.sort_values(["ccdf", "marker_strength"], ascending=[False, False]).reset_index(drop=True)
            y_positions = np.linspace(0.92, 0.12, len(ordered))
            for text_y, row in zip(y_positions, ordered.itertuples(index=False), strict=True):
                ax.annotate(
                    row.gene_name,
                    xy=(row.marker_strength, row.ccdf),
                    xycoords="data",
                    xytext=(0.62, text_y),
                    textcoords="axes fraction",
                    ha="left",
                    va="center",
                    fontsize=6.5,
                    color="#111111",
                    arrowprops={
                        "arrowstyle": "-",
                        "color": "#555555",
                        "linewidth": 0.55,
                        "shrinkA": 1,
                        "shrinkB": 3,
                    },
                    zorder=5,
                )

    for ax in axes.ravel()[len(neighborhoods):]:
        ax.axis("off")

    fig.supxlabel("Marker strength: harmonic mean of coverage and purity", fontsize=11)
    fig.supylabel("Fraction of genes with strength >= x", fontsize=11)
    fig.tight_layout(rect=(0.03, 0.03, 1, 0.98))
    fig.savefig(CCDF_PATH)
    fig.savefig(CCDF_PNG_PATH, dpi=300)
    plt.close(fig)


def write_report(
    scores_df: pd.DataFrame,
    records_df: pd.DataFrame,
    profiles_df: pd.DataFrame,
    filtered_profiles_df: pd.DataFrame,
) -> None:
    summary = (
        filtered_profiles_df.loc[filtered_profiles_df["neighborhood"].ne("")]
        .groupby("neighborhood")
        .agg(
            profiles=("profile_uid", "nunique"),
            papers=("paper_key", "nunique"),
            cell_type_labels=("cell_type", "nunique"),
        )
        .sort_values("profiles", ascending=False)
        .reset_index()
    )

    cell_type_markers = scores_df.loc[scores_df["marker_category"].eq("putative cell-type marker")].sort_values(
        ["neighborhood", "marker_strength", "n_papers_with_gene"], ascending=[True, False, False]
    )
    cell_state_markers = scores_df.loc[scores_df["marker_category"].eq("putative cell-state marker")].sort_values(
        ["reviewed_context_signal", "reviewed_state_bridge", "context_score", "n_papers_with_gene"],
        ascending=[False, False, False, False],
    )

    spotlight = scores_df.loc[scores_df["gene_name"].isin(SPOTLIGHT_GENES)].sort_values(
        ["neighborhood", "marker_category", "marker_strength", "gene_name"],
        ascending=[True, True, False, True],
    )

    columns = [
        "neighborhood",
        "gene_name",
        "gene_id",
        "prevalence",
        "cluster_purity",
        "marker_strength",
        "n_papers_with_gene",
        "n_cell_type_labels_with_gene",
        "outside_prevalence",
        "specificity_ratio",
        "marker_category",
        "profile_examples",
    ]
    concise_columns = [
        "neighborhood",
        "gene_name",
        "prevalence",
        "cluster_purity",
        "marker_strength",
        "n_papers_with_gene",
        "n_cell_type_labels_with_gene",
        "marker_category",
    ]

    report = [
        "# Marker Corpus Summary",
        "",
        "This report estimates how strongly a reported gene functions as a marker for each literature-defined cell-type neighborhood.",
        "",
        "## Assumptions",
        "",
        "- The unit is a reported marker profile: one paper, one reported cell type label, and a binary vector of Ensembl gene IDs.",
        "- Inputs are regenerated from raw `markers.json` files in `data/biorxiv/meca` and `data/hca/manuscripts`.",
        "- Rows are restricted to human markers with a mapped gene ID and source verification.",
        f"- Profiles with fewer than {MIN_MARKERS} markers are excluded.",
        "- Cell-type neighborhoods are assigned with explicit regular expressions over reported labels, not ontology mapping.",
        "- Stability here means stability of literature reporting across papers, not invariant expression across all cells or conditions.",
        "- Candidate labels are restricted to two categories: `putative cell-type marker` and `putative cell-state marker`. Weak or underpowered rows are left unlabeled.",
        "",
        "## Counts",
        "",
        f"- Analysis-ready marker rows: {len(records_df):,}",
        f"- Marker profiles before size filtering: {len(profiles_df):,}",
        f"- Marker profiles with at least {MIN_MARKERS} markers: {len(filtered_profiles_df):,}",
        f"- Profiles assigned to a neighborhood: {filtered_profiles_df['neighborhood'].ne('').sum():,}",
        "",
        "## Diagnostic Plot",
        "",
        f"- Coverage-purity panel: `{PLOT_PATH.relative_to(REPO_ROOT)}`",
        f"- Coverage-purity pages: `{PAGES_PATH.relative_to(REPO_ROOT)}`",
        f"- Marker-strength reverse CDF: `{CCDF_PATH.relative_to(REPO_ROOT)}`",
        "",
        "Each point is a gene within a neighborhood C. The x-axis is coverage, P(gene reported | C). The y-axis is purity, P(C | gene reported). Broad canonical markers should move toward the upper right. State or subtype markers can have high purity but lower coverage.",
        "",
        "Marker strength is the harmonic mean of coverage and purity, analogous to an F1 score over reported marker profiles. The reverse CDF shows the fraction of genes in each neighborhood with marker strength at least x. Individual genes are plotted as points; outlined labels mark the strongest genes, reviewed ambiguity genes, and spotlight genes.",
        "",
        "## Neighborhood Summary",
        "",
        markdown_table(summary, ["neighborhood", "profiles", "papers", "cell_type_labels"]),
        "",
        "## Putative Cell-Type Markers",
        "",
        "These markers recur across multiple papers and labels within a neighborhood, while remaining relatively specific against profiles outside that neighborhood.",
        "",
        markdown_table(cell_type_markers, columns, limit=30),
        "",
        "## Putative Cell-State Markers",
        "",
        "These markers are lower-coverage within a broad neighborhood, appear in reviewed cross-study ambiguity pairs, or correspond to known state and subtype programs in the manuscript evidence.",
        "",
        markdown_table(cell_state_markers, columns, limit=30),
        "",
        "## Spotlight Genes",
        "",
        "The rows below are useful sanity checks for the manuscript story. Broad markers such as CD14, CD79A, MS4A1, PECAM1, and CLEC9A behave as putative cell-type markers in this corpus. Markers such as C1QB, VCAN, CCR7, SELL, TCF7, and GZMK behave as putative cell-state markers because they resolve narrower programs within a broader neighborhood.",
        "",
        markdown_table(spotlight, concise_columns),
        "",
    ]
    REPORT_PATH.write_text("\n".join(report))


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    records_df = build_records()
    if records_df.empty:
        raise SystemExit("No marker records found.")

    profiles_df, filtered_profiles_df, _filtered_profiles, id_to_name = build_profile_summary(
        records_df,
        min_markers=MIN_MARKERS,
        feature_id_col="feature_id_std",
        feature_name_col="feature_name_std",
    )
    filtered_profiles_df["neighborhood"] = filtered_profiles_df["cell_type"].map(assign_neighborhood)
    filtered_profiles_df["profile_uid"] = [
        f"{row.source_corpus}|{row.paper_id}|{row.cell_type}" for row in filtered_profiles_df.itertuples(index=False)
    ]

    assigned_profiles = filtered_profiles_df.loc[filtered_profiles_df["neighborhood"].ne("")].copy()
    profile_gene_df = build_profile_gene_table(assigned_profiles)
    all_profile_gene_df = build_profile_gene_table(filtered_profiles_df)

    name_to_ids = (
        records_df.loc[records_df["feature_name_std"].ne("") & records_df["feature_id_std"].ne("")]
        .groupby("feature_name_std")["feature_id_std"]
        .agg(lambda values: set(values))
        .to_dict()
    )
    context_signal_ids, state_bridge_ids = reviewed_gene_sets(name_to_ids)

    total_profiles = filtered_profiles_df["profile_uid"].nunique()
    total_by_neighborhood = assigned_profiles.groupby("neighborhood")["profile_uid"].nunique().to_dict()
    all_gene_profile_counts = all_profile_gene_df.groupby("gene_id")["profile_uid"].nunique().to_dict()

    score_rows = []
    for neighborhood, group in profile_gene_df.groupby("neighborhood", sort=True):
        n_profiles_neighborhood = total_by_neighborhood[neighborhood]
        outside_n = total_profiles - n_profiles_neighborhood
        for gene_id, gene_group in group.groupby("gene_id", sort=True):
            profile_uids = sorted(gene_group["profile_uid"].unique())
            n_profiles_with_gene = len(profile_uids)
            n_papers_with_gene = gene_group["paper_key"].nunique()
            n_corpora_with_gene = gene_group["source_corpus"].nunique()
            n_labels_with_gene = gene_group["cell_type"].nunique()
            prevalence = n_profiles_with_gene / n_profiles_neighborhood if n_profiles_neighborhood else 0.0
            global_profiles_with_gene = all_gene_profile_counts.get(gene_id, 0)
            outside_profiles_with_gene = max(global_profiles_with_gene - n_profiles_with_gene, 0)
            outside_prevalence = outside_profiles_with_gene / outside_n if outside_n else 0.0
            cluster_purity = n_profiles_with_gene / global_profiles_with_gene if global_profiles_with_gene else 0.0
            specificity_ratio = (prevalence + EPS) / (outside_prevalence + EPS)
            support_score = min(1.0, math.log1p(n_papers_with_gene) / math.log1p(10))
            specificity_score = min(1.0, math.log2(specificity_ratio + 1.0) / math.log2(10.0))
            stability_score = 0.5 * prevalence + 0.25 * support_score + 0.25 * specificity_score
            context_score = (1.0 - prevalence) * support_score * specificity_score
            marker_strength = (
                2 * prevalence * cluster_purity / (prevalence + cluster_purity)
                if (prevalence + cluster_purity) > 0
                else 0.0
            )
            examples = (
                gene_group[["paper_key", "cell_type"]]
                .drop_duplicates()
                .sort_values(["paper_key", "cell_type"])
                .head(5)
            )
            profile_examples = "; ".join(f"{row.paper_key} ({row.cell_type})" for row in examples.itertuples(index=False))
            score_rows.append(
                {
                    "neighborhood": neighborhood,
                    "gene_id": gene_id,
                    "gene_name": id_to_name.get(gene_id, gene_id),
                    "n_profiles_neighborhood": n_profiles_neighborhood,
                    "n_profiles_with_gene": n_profiles_with_gene,
                    "prevalence": prevalence,
                    "n_papers_with_gene": n_papers_with_gene,
                    "n_corpora_with_gene": n_corpora_with_gene,
                    "n_cell_type_labels_with_gene": n_labels_with_gene,
                    "label_entropy": entropy(gene_group["cell_type"]),
                    "corpus_entropy": entropy(gene_group["source_corpus"]),
                    "global_profiles_with_gene": global_profiles_with_gene,
                    "outside_profiles_with_gene": outside_profiles_with_gene,
                    "outside_prevalence": outside_prevalence,
                    "cluster_purity": cluster_purity,
                    "specificity_ratio": specificity_ratio,
                    "support_score": support_score,
                    "stability_score": stability_score,
                    "context_score": context_score,
                    "marker_strength": marker_strength,
                    "reviewed_context_signal": gene_id in context_signal_ids,
                    "reviewed_state_bridge": gene_id in state_bridge_ids,
                    "profile_examples": profile_examples,
                }
            )

    scores_df = pd.DataFrame(score_rows)
    scores_df["marker_category"] = scores_df.apply(classify_marker_category, axis=1)
    scores_df = scores_df.sort_values(
        ["neighborhood", "marker_category", "stability_score", "n_papers_with_gene"],
        ascending=[True, True, False, False],
    ).reset_index(drop=True)

    scores_df.to_csv(SCORES_PATH, sep="\t", index=False)
    plot_prevalence_landscape(scores_df)
    plot_main_prevalence_landscape(scores_df)
    plot_marker_strength_ccdf(scores_df)
    write_report(scores_df, records_df, profiles_df, filtered_profiles_df)

    print(f"Wrote {SCORES_PATH.relative_to(REPO_ROOT)} ({len(scores_df):,} rows)")
    print(f"Wrote {REPORT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PLOT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MAIN_PLOT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PAGES_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {CCDF_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
