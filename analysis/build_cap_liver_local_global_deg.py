from __future__ import annotations

import json
import math
import os
import re
from collections import Counter
from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd
import scipy.sparse as sp

os.environ.setdefault("MPLCONFIGDIR", "/tmp/llmarkers-matplotlib")

import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[1]
CAP_DIR = REPO_ROOT / "data" / "cell_annotation_platform"
ANNDATA_DIR = CAP_DIR / "anndata"
RESULTS_DIR = REPO_ROOT / "analysis" / "artifacts"
FIGURES_DIR = REPO_ROOT / "analysis" / "figures"
PANEL_G_PATH = FIGURES_DIR / "fig3_panel_g_cap_liver_reported_marker_recovery.pdf"
PANEL_G_PNG_PATH = FIGURES_DIR / "fig3_panel_g_cap_liver_reported_marker_recovery.png"
PANEL_H_PATH = FIGURES_DIR / "fig3_panel_h_cap_liver_de_stability.pdf"
PANEL_H_PNG_PATH = FIGURES_DIR / "fig3_panel_h_cap_liver_de_stability.png"
PANEL_I_PATH = FIGURES_DIR / "fig3_panel_i_cap_liver_marker_retrieval.pdf"
PANEL_I_PNG_PATH = FIGURES_DIR / "fig3_panel_i_cap_liver_marker_retrieval.png"
RECOVERY_SUBSAMPLING_PATH = RESULTS_DIR / "cap_liver_local_global_recovery_subsampling.tsv"
RECOVERY_SUBSAMPLING_SUMMARY_PATH = RESULTS_DIR / "cap_liver_local_global_recovery_subsampling_summary.tsv"

ALL_CELLS_PATH = ANNDATA_DIR / "cap_1437_liver_all_cells.h5ad"
MYELOID_PATH = ANNDATA_DIR / "cap_1440_liver_myeloid.h5ad"
CAP_MARKERS_PATH = CAP_DIR / "markers.json"

LABEL_COL = "author_cell_type"
LAYER = "user_provided"
TOP_K_VALUES = (25, 50, 100, 200)
SUBSAMPLING_REPS = int(os.environ.get("CAP_LIVER_SUBSAMPLING_REPS", "50"))
SUBSAMPLING_FRACTION = float(os.environ.get("CAP_LIVER_SUBSAMPLING_FRACTION", "0.8"))
SUBSAMPLING_MAX_PER_CELL_TYPE = int(os.environ.get("CAP_LIVER_SUBSAMPLING_MAX_PER_CELL_TYPE", "10000"))
SUBSAMPLING_SEED = int(os.environ.get("CAP_LIVER_SUBSAMPLING_SEED", "1440"))

# CAP ontology columns show that these local myeloid labels map onto the broad
# author labels used in the all-cells liver atlas.
LOCAL_TO_GLOBAL_LABEL = {
    "Mac1": "Macrophages",
    "immature LAMs": "Macrophages",
    "mature LAMs": "Macrophages",
    "Pre-moKCs and moKCs": "Macrophages",
    "ResKCs": "Macrophages",
    "Mono": "Mono+mono derived cells",
    "Pat Mono": "Mono+mono derived cells",
    "cDC1s": "cDC1s",
    "cDC2s": "cDC2s",
    "Mig cDCs": "Mig.cDCs",
}


def normalize_text(value: object) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    return re.sub(r"\s+", " ", str(value).strip())


def normalize_key(value: object) -> str:
    return normalize_text(value).casefold()


def as_dense_vector(value: object) -> np.ndarray:
    return np.asarray(value).ravel().astype(float)


def marker_records() -> pd.DataFrame:
    records = pd.DataFrame(json.loads(CAP_MARKERS_PATH.read_text(encoding="utf-8")))
    records = records.loc[
        records["organism"].eq("homo_sapiens")
        & records["feature_id"].map(normalize_text).str.startswith("ENSG")
    ].copy()
    records["_cap_dataset_id"] = records["_cap_dataset_id"].astype(str)
    records["_label_key"] = records["group_label"].map(normalize_key)
    records["feature_id"] = records["feature_id"].map(normalize_text)
    records["feature_name"] = records["feature_name"].map(normalize_text)
    return records


def reported_marker_set(records: pd.DataFrame, dataset_id: str, label: str) -> tuple[set[str], dict[str, str]]:
    subset = records.loc[
        records["_cap_dataset_id"].eq(str(dataset_id)) & records["_label_key"].eq(normalize_key(label))
    ]
    id_to_name = {
        row.feature_id: row.feature_name
        for row in subset.itertuples(index=False)
        if normalize_text(row.feature_id)
    }
    return set(id_to_name), id_to_name


def load_expression(path: Path) -> tuple[ad.AnnData, sp.csr_matrix, pd.DataFrame, np.ndarray, dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing AnnData file: {path}")
    adata = ad.read_h5ad(path, backed="r")
    matrix = adata.layers[LAYER] if LAYER in adata.layers else adata.X
    if hasattr(matrix, "to_memory"):
        matrix = matrix.to_memory()
    if not sp.issparse(matrix):
        matrix = sp.csr_matrix(matrix)
    else:
        matrix = matrix.tocsr()

    gene_ids = np.asarray(adata.var_names.astype(str))
    gene_names = adata.var.get("feature_name", adata.var.get("gene_names", pd.Series(gene_ids, index=adata.var.index)))
    id_to_name = {gene_id: normalize_text(name) for gene_id, name in zip(gene_ids, gene_names)}
    return adata, matrix, adata.obs.copy(), gene_ids, id_to_name


def compute_one_vs_rest(
    matrix: sp.csr_matrix,
    labels: pd.Series,
    target_labels: list[str],
    gene_ids: np.ndarray,
) -> dict[str, dict[str, object]]:
    labels = labels.astype(str)
    n_cells, n_genes = matrix.shape
    total_sum = as_dense_vector(matrix.sum(axis=0))
    total_sumsq = as_dense_vector(matrix.power(2).sum(axis=0))
    total_nnz = np.asarray(matrix.getnnz(axis=0)).ravel().astype(float)

    results: dict[str, dict[str, object]] = {}
    for target in target_labels:
        mask = labels.eq(target).to_numpy()
        n_in = int(mask.sum())
        n_out = int(n_cells - n_in)
        if n_in == 0 or n_out == 0:
            raise ValueError(f"Cannot compute one-vs-rest for {target!r}: n_in={n_in}, n_out={n_out}")

        target_matrix = matrix[mask]
        in_sum = as_dense_vector(target_matrix.sum(axis=0))
        in_sumsq = as_dense_vector(target_matrix.power(2).sum(axis=0))
        in_nnz = np.asarray(target_matrix.getnnz(axis=0)).ravel().astype(float)

        out_sum = total_sum - in_sum
        out_sumsq = total_sumsq - in_sumsq
        out_nnz = total_nnz - in_nnz

        mean_in = in_sum / n_in
        mean_out = out_sum / n_out
        var_in = np.maximum(in_sumsq / n_in - mean_in**2, 0.0)
        var_out = np.maximum(out_sumsq / n_out - mean_out**2, 0.0)
        se = np.sqrt(var_in / n_in + var_out / n_out)
        score = np.divide(mean_in - mean_out, se, out=np.zeros(n_genes, dtype=float), where=se > 0)
        log2fc = np.log2((mean_in + 1e-9) / (mean_out + 1e-9))
        pct_in = in_nnz / n_in
        pct_out = out_nnz / n_out

        order = np.argsort(-score, kind="mergesort")
        ranks = np.empty(n_genes, dtype=int)
        ranks[order] = np.arange(1, n_genes + 1)
        gene_to_index = {gene_id: idx for idx, gene_id in enumerate(gene_ids)}

        results[target] = {
            "n_cells": n_in,
            "score": score,
            "log2fc": log2fc,
            "mean_in": mean_in,
            "mean_out": mean_out,
            "pct_in": pct_in,
            "pct_out": pct_out,
            "rank": ranks,
            "order": order,
            "gene_to_index": gene_to_index,
            "top_sets": {k: set(gene_ids[order[:k]]) for k in TOP_K_VALUES},
        }
    return results


def subsample_size(n_items: int) -> int:
    if n_items <= 0:
        return 0
    return min(
        n_items,
        max(2, min(SUBSAMPLING_MAX_PER_CELL_TYPE, math.ceil(n_items * SUBSAMPLING_FRACTION))),
    )


def label_index_map(labels: np.ndarray) -> dict[str, np.ndarray]:
    return {label: np.flatnonzero(labels == label) for label in np.unique(labels)}


def compute_stratified_subsampled_top_sets(
    matrix: sp.csr_matrix,
    label_indices: dict[str, np.ndarray],
    target_labels: list[str],
    gene_ids: np.ndarray,
    rng: np.random.Generator,
    top_k: int = 100,
) -> dict[str, set[str]]:
    sampled_by_label: dict[str, np.ndarray] = {}
    sampled_indices: list[np.ndarray] = []
    for label, indices in label_indices.items():
        n_sample = subsample_size(len(indices))
        if n_sample == 0:
            continue
        sample = rng.choice(indices, size=n_sample, replace=False)
        sampled_by_label[label] = sample
        sampled_indices.append(sample)

    if not sampled_indices:
        raise ValueError("Cannot compute stratified subsampling without sampled cells")

    all_sampled = np.concatenate(sampled_indices)
    sampled_matrix = matrix[all_sampled]
    total_n = len(all_sampled)
    total_sum = as_dense_vector(sampled_matrix.sum(axis=0))
    total_sumsq = as_dense_vector(sampled_matrix.power(2).sum(axis=0))

    top_sets: dict[str, set[str]] = {}
    for target_label in target_labels:
        target_sample = sampled_by_label.get(target_label)
        if target_sample is None or len(target_sample) == 0:
            raise ValueError(f"Cannot subsample one-vs-rest for {target_label!r}")
        n_target = len(target_sample)
        n_background = total_n - n_target
        if n_background == 0:
            raise ValueError(f"Cannot subsample one-vs-rest for {target_label!r}: no background cells")

        target_matrix = matrix[target_sample]
        target_sum = as_dense_vector(target_matrix.sum(axis=0))
        target_sumsq = as_dense_vector(target_matrix.power(2).sum(axis=0))
        background_sum = total_sum - target_sum
        background_sumsq = total_sumsq - target_sumsq

        mean_target = target_sum / n_target
        mean_background = background_sum / n_background
        var_target = np.maximum(target_sumsq / n_target - mean_target**2, 0.0)
        var_background = np.maximum(background_sumsq / n_background - mean_background**2, 0.0)
        se = np.sqrt(var_target / n_target + var_background / n_background)
        score = np.divide(
            mean_target - mean_background,
            se,
            out=np.zeros(len(gene_ids), dtype=float),
            where=se > 0,
        )
        top_idx = np.argpartition(-score, top_k - 1)[:top_k]
        top_sets[target_label] = set(gene_ids[top_idx])

    return top_sets


def summarize_subsampling(draws_df: pd.DataFrame, summary_df: pd.DataFrame) -> pd.DataFrame:
    observed = []
    for row in summary_df.itertuples(index=False):
        observed.append(
            {
                "local_label": row.local_label,
                "context": "local",
                "observed": row.local_reported_recovery_top100,
            }
        )
        observed.append(
            {
                "local_label": row.local_label,
                "context": "global",
                "observed": row.global_recovery_of_local_reported_top100,
            }
        )
    observed_df = pd.DataFrame(observed)
    grouped = (
        draws_df.groupby(["local_label", "global_label", "context"], sort=False)["recovery_top100"]
        .agg(
            n_reps="count",
            mean="mean",
            sd="std",
            q025=lambda x: float(np.quantile(x, 0.025)),
            q975=lambda x: float(np.quantile(x, 0.975)),
        )
        .reset_index()
    )
    grouped["sem"] = grouped["sd"] / np.sqrt(grouped["n_reps"])
    grouped = grouped.merge(observed_df, on=["local_label", "context"], how="left")
    grouped["subsampling_fraction"] = SUBSAMPLING_FRACTION
    grouped["max_cells_per_cell_type"] = SUBSAMPLING_MAX_PER_CELL_TYPE
    grouped["seed"] = SUBSAMPLING_SEED
    return grouped


def compute_recovery_subsampling(
    records: pd.DataFrame,
    local_matrix: sp.csr_matrix,
    global_matrix: sp.csr_matrix,
    local_obs: pd.DataFrame,
    global_obs: pd.DataFrame,
    gene_ids: np.ndarray,
    summary_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(SUBSAMPLING_SEED)
    gene_universe = set(gene_ids)
    reported_sets = {}
    for local_label in LOCAL_TO_GLOBAL_LABEL:
        local_reported, _names = reported_marker_set(records, "1440", local_label)
        reported_sets[local_label] = {gene for gene in local_reported if gene in gene_universe}

    local_labels = list(LOCAL_TO_GLOBAL_LABEL)
    global_labels = sorted(set(LOCAL_TO_GLOBAL_LABEL.values()))
    local_label_indices = label_index_map(local_obs[LABEL_COL].astype(str).to_numpy())
    global_label_indices = label_index_map(global_obs[LABEL_COL].astype(str).to_numpy())
    draw_rows = []

    for rep in range(SUBSAMPLING_REPS):
        top_sets = compute_stratified_subsampled_top_sets(
            local_matrix,
            local_label_indices,
            local_labels,
            gene_ids,
            rng,
        )
        for local_label, global_label in LOCAL_TO_GLOBAL_LABEL.items():
            markers = reported_sets[local_label]
            if not markers:
                continue
            top_set = top_sets[local_label]
            draw_rows.append(
                {
                    "local_label": local_label,
                    "global_label": global_label,
                    "context": "local",
                    "replicate": rep,
                    "recovery_top100": len(markers & top_set) / len(markers),
                }
            )

    global_to_local_labels: dict[str, list[str]] = {}
    for local_label, global_label in LOCAL_TO_GLOBAL_LABEL.items():
        global_to_local_labels.setdefault(global_label, []).append(local_label)

    for rep in range(SUBSAMPLING_REPS):
        top_sets = compute_stratified_subsampled_top_sets(
            global_matrix,
            global_label_indices,
            global_labels,
            gene_ids,
            rng,
        )
        for global_label, mapped_local_labels in global_to_local_labels.items():
            top_set = top_sets[global_label]
            for local_label in mapped_local_labels:
                markers = reported_sets[local_label]
                if not markers:
                    continue
                draw_rows.append(
                    {
                        "local_label": local_label,
                        "global_label": global_label,
                        "context": "global",
                        "replicate": rep,
                        "recovery_top100": len(markers & top_set) / len(markers),
                    }
                )

    draws_df = pd.DataFrame(draw_rows)
    interval_df = summarize_subsampling(draws_df, summary_df)
    return draws_df, interval_df


def summarize_ranks(gene_set: set[str], ranks: dict[str, int]) -> tuple[float, float]:
    observed = [ranks[gene] for gene in gene_set if gene in ranks]
    if not observed:
        return math.nan, math.nan
    return float(np.median(observed)), float(np.mean(observed))


def jaccard(a: set[str], b: set[str]) -> float:
    return len(a & b) / len(a | b) if a or b else math.nan


def rank_lookup(de_result: dict[str, object], gene_ids: np.ndarray) -> dict[str, int]:
    ranks = de_result["rank"]
    return {gene_id: int(ranks[idx]) for idx, gene_id in enumerate(gene_ids)}


def stat_lookup(de_result: dict[str, object], gene_id: str) -> dict[str, float | int | None]:
    idx = de_result["gene_to_index"].get(gene_id)
    if idx is None:
        return {
            "rank": None,
            "score": math.nan,
            "log2fc": math.nan,
            "pct_in": math.nan,
            "pct_out": math.nan,
            "mean_in": math.nan,
            "mean_out": math.nan,
        }
    return {
        "rank": int(de_result["rank"][idx]),
        "score": float(de_result["score"][idx]),
        "log2fc": float(de_result["log2fc"][idx]),
        "pct_in": float(de_result["pct_in"][idx]),
        "pct_out": float(de_result["pct_out"][idx]),
        "mean_in": float(de_result["mean_in"][idx]),
        "mean_out": float(de_result["mean_out"][idx]),
    }


def classify_marker(local_rank: int | None, global_rank: int | None, k: int = 100) -> str:
    local_hit = local_rank is not None and local_rank <= k
    global_hit = global_rank is not None and global_rank <= k
    if local_hit and global_hit:
        return "local_and_global"
    if local_hit:
        return "local_only"
    if global_hit:
        return "global_only"
    return "neither"


def retrieval_metrics(positives: set[str], de_result: dict[str, object], gene_ids: np.ndarray) -> dict[str, float | int]:
    positives = {gene for gene in positives if gene in set(gene_ids)}
    n_pos = len(positives)
    if n_pos == 0:
        return {
            "average_precision": math.nan,
            "max_f1": math.nan,
            "f1_at_n_reported": math.nan,
            "f1_at_100": math.nan,
            "best_rank_cutoff": 0,
        }

    hits = np.asarray([gene_ids[idx] in positives for idx in de_result["order"]], dtype=bool)
    hit_positions = np.flatnonzero(hits) + 1
    cumulative_hits = np.cumsum(hits)
    precision_at_hits = cumulative_hits[hit_positions - 1] / hit_positions
    average_precision = float(precision_at_hits.sum() / n_pos)

    candidate_positions = np.unique(np.concatenate([hit_positions, np.asarray([n_pos, 100])]))
    candidate_positions = candidate_positions[(candidate_positions >= 1) & (candidate_positions <= len(hits))]
    best_f1 = 0.0
    best_k = 0
    f1_at_n = math.nan
    f1_at_100 = math.nan
    for k in candidate_positions:
        tp = float(cumulative_hits[k - 1])
        precision = tp / float(k)
        recall = tp / float(n_pos)
        f1 = 2.0 * precision * recall / (precision + recall) if precision + recall > 0 else 0.0
        if f1 > best_f1:
            best_f1 = f1
            best_k = int(k)
        if int(k) == n_pos:
            f1_at_n = float(f1)
        if int(k) == 100:
            f1_at_100 = float(f1)

    return {
        "average_precision": average_precision,
        "max_f1": float(best_f1),
        "f1_at_n_reported": f1_at_n,
        "f1_at_100": f1_at_100,
        "best_rank_cutoff": best_k,
    }


def write_outputs(
    summary_df: pd.DataFrame,
    marker_df: pd.DataFrame,
    top_df: pd.DataFrame,
    subsampling_df: pd.DataFrame | None = None,
    subsampling_summary_df: pd.DataFrame | None = None,
) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    summary_path = RESULTS_DIR / "cap_liver_local_global_deg_summary.tsv"
    marker_path = RESULTS_DIR / "cap_liver_local_global_reported_marker_ranks.tsv"
    top_path = RESULTS_DIR / "cap_liver_local_global_top_degs.tsv"
    summary_df.to_csv(summary_path, sep="\t", index=False)
    marker_df.to_csv(marker_path, sep="\t", index=False)
    top_df.to_csv(top_path, sep="\t", index=False)
    if subsampling_df is not None and subsampling_summary_df is not None:
        subsampling_df.to_csv(RECOVERY_SUBSAMPLING_PATH, sep="\t", index=False)
        subsampling_summary_df.to_csv(RECOVERY_SUBSAMPLING_SUMMARY_PATH, sep="\t", index=False)

    plot_summary(summary_df, marker_df, subsampling_summary_df)
    print(f"Wrote {summary_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {marker_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {top_path.relative_to(REPO_ROOT)}")
    if subsampling_df is not None and subsampling_summary_df is not None:
        print(f"Wrote {RECOVERY_SUBSAMPLING_PATH.relative_to(REPO_ROOT)}")
        print(f"Wrote {RECOVERY_SUBSAMPLING_SUMMARY_PATH.relative_to(REPO_ROOT)}")


def plot_summary(
    summary_df: pd.DataFrame,
    marker_df: pd.DataFrame,
    subsampling_summary_df: pd.DataFrame | None = None,
) -> None:
    ordered_rows = summary_df.sort_values("global_label").copy()
    label_order = ordered_rows.local_label.tolist()
    display_label_order = [
        f"{row.local_label} ({row.global_label})"
        for row in ordered_rows.itertuples(index=False)
    ]
    y = np.arange(len(label_order))
    ordered = summary_df.set_index("local_label").loc[label_order]

    save_single_panel(
        PANEL_G_PATH,
        PANEL_G_PNG_PATH,
        lambda ax: draw_marker_recovery_panel(
            ax,
            ordered,
            y,
            display_label_order,
            show_ylabels=True,
            title_size=9,
            subsampling_summary_df=subsampling_summary_df,
        ),
        figsize=(4.0, 3.6),
        adjust={"left": 0.54, "right": 0.97, "bottom": 0.20, "top": 0.82},
    )
    save_single_panel(
        PANEL_H_PATH,
        PANEL_H_PNG_PATH,
        lambda ax: draw_de_stability_panel(ax, ordered, y, display_label_order, show_ylabels=False, title_size=9),
        figsize=(4.0, 3.6),
        adjust={"left": 0.16, "right": 0.97, "bottom": 0.20, "top": 0.82},
    )
    save_single_panel(
        PANEL_I_PATH,
        PANEL_I_PNG_PATH,
        lambda ax: draw_marker_retrieval_panel(ax, ordered, y, display_label_order, show_ylabels=False, title_size=9),
        figsize=(4.0, 3.6),
        adjust={"left": 0.16, "right": 0.97, "bottom": 0.20, "top": 0.82},
    )


def style_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def draw_marker_recovery_panel(
    ax: plt.Axes,
    ordered: pd.DataFrame,
    y: np.ndarray,
    label_order: list[str],
    show_ylabels: bool,
    title_size: float = 10,
    subsampling_summary_df: pd.DataFrame | None = None,
) -> None:
    height = 0.38
    ax.barh(
        y - height / 2,
        ordered["local_reported_recovery_top100"],
        height=height,
        facecolor="white",
        edgecolor="black",
        linewidth=0.55,
        label="local DE",
    )
    ax.barh(
        y + height / 2,
        ordered["global_recovery_of_local_reported_top100"],
        height=height,
        facecolor="black",
        edgecolor="black",
        linewidth=0.55,
        label="global DE",
    )
    if subsampling_summary_df is not None and not subsampling_summary_df.empty:
        interval_lookup = subsampling_summary_df.set_index(["local_label", "context"])
        for row_idx, row in enumerate(ordered.itertuples(index=False)):
            local_label = ordered.index[row_idx]
            for context, y_value, observed_col in [
                ("local", y[row_idx] - height / 2, "local_reported_recovery_top100"),
                ("global", y[row_idx] + height / 2, "global_recovery_of_local_reported_top100"),
            ]:
                key = (local_label, context)
                if key not in interval_lookup.index:
                    continue
                interval = interval_lookup.loc[key]
                observed = float(getattr(row, observed_col))
                low = max(0.0, float(interval["q025"]))
                high = min(1.0, float(interval["q975"]))
                cap_half_height = height * 0.23
                ax.hlines(y_value, low, high, color="black", linewidth=0.7, zorder=5)
                ax.vlines([low, high], y_value - cap_half_height, y_value + cap_half_height, color="black", linewidth=0.7, zorder=5)
    ax.set_yticks(y)
    ax.set_yticklabels(label_order if show_ylabels else [], fontsize=5.7)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Fraction of reported markers\nrecovered in top 100", fontsize=8)
    ax.tick_params(axis="both", labelsize=7.2)
    ax.legend(frameon=False, fontsize=7, loc="lower right")
    ax.set_title("Reported Marker Recovery", fontsize=title_size, weight="bold")
    style_axis(ax)


def draw_de_stability_panel(
    ax: plt.Axes,
    ordered: pd.DataFrame,
    y: np.ndarray,
    label_order: list[str],
    show_ylabels: bool,
    title_size: float = 10,
) -> None:
    ax.barh(
        y,
        ordered["local_top100_vs_global_top100_jaccard"],
        facecolor="#D9D9D9",
        edgecolor="black",
        linewidth=0.6,
        zorder=2,
    )
    ax.set_yticks(y)
    ax.set_yticklabels(label_order if show_ylabels else [], fontsize=7.2)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Jaccard(top 100 local DE,\ntop 100 global DE)", fontsize=8)
    ax.tick_params(axis="both", labelsize=7.2)
    ax.set_title("Local vs Global DE Stability", fontsize=title_size, weight="bold")
    style_axis(ax)


def draw_marker_retrieval_panel(
    ax: plt.Axes,
    ordered: pd.DataFrame,
    y: np.ndarray,
    label_order: list[str],
    show_ylabels: bool,
    title_size: float = 10,
) -> None:
    local_col = "local_reported_max_f1"
    global_col = "global_recovery_of_local_reported_max_f1"
    for i, row in enumerate(ordered.itertuples(index=False)):
        ax.plot(
            [getattr(row, global_col), getattr(row, local_col)],
            [i, i],
            color="#B0B0B0",
            linewidth=1.0,
            zorder=1,
        )
    ax.scatter(
        ordered[global_col],
        y,
        facecolor="black",
        edgecolor="black",
        linewidth=0.75,
        s=24,
        label="global DE",
        zorder=3,
    )
    ax.scatter(
        ordered[local_col],
        y,
        facecolor="white",
        edgecolor="black",
        linewidth=0.75,
        s=24,
        label="local DE",
        zorder=2,
    )
    ax.set_yticks(y)
    ax.set_yticklabels(label_order if show_ylabels else [], fontsize=7.2)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Maximum F1", fontsize=8)
    ax.tick_params(axis="both", labelsize=7.2)
    ax.set_title("Reported Marker Retrieval", fontsize=title_size, weight="bold")
    ax.legend(frameon=False, fontsize=7, loc="lower right")
    style_axis(ax)


def save_single_panel(
    pdf_path: Path,
    png_path: Path,
    draw,
    figsize: tuple[float, float],
    adjust: dict[str, float] | None = None,
) -> None:
    fig, ax = plt.subplots(figsize=figsize)
    draw(ax)
    if adjust is not None:
        fig.subplots_adjust(**adjust)
    fig.savefig(pdf_path)
    fig.savefig(png_path, dpi=300)
    plt.close(fig)


def main() -> None:
    records = marker_records()

    print("Loading local myeloid AnnData")
    local_adata, local_x, local_obs, local_gene_ids, local_id_to_name = load_expression(MYELOID_PATH)
    print("Loading global all-cells AnnData")
    global_adata, global_x, global_obs, global_gene_ids, global_id_to_name = load_expression(ALL_CELLS_PATH)

    if list(local_gene_ids) != list(global_gene_ids):
        raise ValueError("Local and global AnnData objects have different gene axes.")

    local_labels = list(LOCAL_TO_GLOBAL_LABEL)
    global_labels = sorted(set(LOCAL_TO_GLOBAL_LABEL.values()))
    print(f"Computing local one-vs-rest rankings for {len(local_labels)} labels")
    local_de = compute_one_vs_rest(local_x, local_obs[LABEL_COL], local_labels, local_gene_ids)
    print(f"Computing global one-vs-rest rankings for {len(global_labels)} labels")
    global_de = compute_one_vs_rest(global_x, global_obs[LABEL_COL], global_labels, global_gene_ids)

    summary_rows = []
    marker_rows = []
    top_rows = []
    for local_label, global_label in LOCAL_TO_GLOBAL_LABEL.items():
        local_reported, local_marker_names = reported_marker_set(records, "1440", local_label)
        global_reported, global_marker_names = reported_marker_set(records, "1437", global_label)
        local_reported = {gene for gene in local_reported if gene in set(local_gene_ids)}
        global_reported = {gene for gene in global_reported if gene in set(global_gene_ids)}

        local_ranks = rank_lookup(local_de[local_label], local_gene_ids)
        global_ranks = rank_lookup(global_de[global_label], global_gene_ids)
        local_median_rank, local_mean_rank = summarize_ranks(local_reported, local_ranks)
        global_median_rank, global_mean_rank = summarize_ranks(local_reported, global_ranks)
        local_retrieval = retrieval_metrics(local_reported, local_de[local_label], local_gene_ids)
        global_retrieval = retrieval_metrics(local_reported, global_de[global_label], global_gene_ids)

        row = {
            "local_dataset_id": "1440",
            "global_dataset_id": "1437",
            "local_label": local_label,
            "global_label": global_label,
            "local_n_cells": local_de[local_label]["n_cells"],
            "global_n_cells": global_de[global_label]["n_cells"],
            "n_local_reported_markers": len(local_reported),
            "n_global_reported_markers": len(global_reported),
            "local_reported_vs_global_reported_jaccard": jaccard(local_reported, global_reported),
            "local_reported_median_local_rank": local_median_rank,
            "local_reported_median_global_rank": global_median_rank,
            "local_reported_mean_local_rank": local_mean_rank,
            "local_reported_mean_global_rank": global_mean_rank,
        }
        for metric, value in local_retrieval.items():
            row[f"local_reported_{metric}"] = value
        for metric, value in global_retrieval.items():
            row[f"global_recovery_of_local_reported_{metric}"] = value
        for k in TOP_K_VALUES:
            local_top = local_de[local_label]["top_sets"][k]
            global_top = global_de[global_label]["top_sets"][k]
            row[f"local_reported_recovery_top{k}"] = len(local_reported & local_top) / len(local_reported)
            row[f"global_recovery_of_local_reported_top{k}"] = len(local_reported & global_top) / len(local_reported)
            row[f"global_reported_recovery_top{k}"] = len(global_reported & global_top) / len(global_reported) if global_reported else math.nan
            row[f"local_top{k}_vs_global_top{k}_jaccard"] = jaccard(local_top, global_top)
        summary_rows.append(row)

        for gene_id in sorted(local_reported):
            local_stats = stat_lookup(local_de[local_label], gene_id)
            global_stats = stat_lookup(global_de[global_label], gene_id)
            marker_rows.append(
                {
                    "local_label": local_label,
                    "global_label": global_label,
                    "feature_id": gene_id,
                    "feature_name": local_marker_names.get(gene_id) or global_id_to_name.get(gene_id, gene_id),
                    "local_rank": local_stats["rank"],
                    "global_rank": global_stats["rank"],
                    "local_score": local_stats["score"],
                    "global_score": global_stats["score"],
                    "local_log2fc": local_stats["log2fc"],
                    "global_log2fc": global_stats["log2fc"],
                    "local_pct_in": local_stats["pct_in"],
                    "local_pct_out": local_stats["pct_out"],
                    "global_pct_in": global_stats["pct_in"],
                    "global_pct_out": global_stats["pct_out"],
                    "rank_category_top100": classify_marker(local_stats["rank"], global_stats["rank"], k=100),
                }
            )

        for context, de_result in [("local", local_de[local_label]), ("global", global_de[global_label])]:
            for rank, idx in enumerate(de_result["order"][:200], start=1):
                gene_id = local_gene_ids[idx]
                top_rows.append(
                    {
                        "local_label": local_label,
                        "global_label": global_label,
                        "context": context,
                        "rank": rank,
                        "feature_id": gene_id,
                        "feature_name": local_id_to_name.get(gene_id, gene_id),
                        "score": float(de_result["score"][idx]),
                        "log2fc": float(de_result["log2fc"][idx]),
                        "pct_in": float(de_result["pct_in"][idx]),
                        "pct_out": float(de_result["pct_out"][idx]),
                    }
                )

    summary_df = pd.DataFrame(summary_rows)
    marker_df = pd.DataFrame(marker_rows)
    top_df = pd.DataFrame(top_rows)
    print(
        "Computing stratified subsampling intervals "
        f"({SUBSAMPLING_REPS} reps; max per cell type={SUBSAMPLING_MAX_PER_CELL_TYPE})"
    )
    subsampling_df, subsampling_summary_df = compute_recovery_subsampling(
        records,
        local_x,
        global_x,
        local_obs,
        global_obs,
        local_gene_ids,
        summary_df,
    )

    local_adata.file.close()
    global_adata.file.close()

    write_outputs(summary_df, marker_df, top_df, subsampling_df, subsampling_summary_df)

    print("\nSummary:")
    cols = [
        "local_label",
        "global_label",
        "local_reported_recovery_top100",
        "global_recovery_of_local_reported_top100",
        "local_reported_average_precision",
        "global_recovery_of_local_reported_average_precision",
        "local_reported_max_f1",
        "global_recovery_of_local_reported_max_f1",
        "local_top100_vs_global_top100_jaccard",
        "local_reported_vs_global_reported_jaccard",
    ]
    print(summary_df[cols].to_string(index=False))


if __name__ == "__main__":
    main()
