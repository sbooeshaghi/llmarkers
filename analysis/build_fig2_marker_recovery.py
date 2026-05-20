from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
RESULTS_DIR = REPO_ROOT / "analysis" / "results"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = [
    ("adipose_Emont2022", "Emont"),
    ("adipose_Hildreth2021", "Hildreth"),
    ("bone_He2021", "He"),
    ("eye_Gautam2021", "Gautam"),
    ("lung_Adams2020", "Adams"),
    ("ovary_Wagner2020", "Wagner"),
    ("testis_Shamis2020", "Shamis"),
]

N_VALUES = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500]
EXTRACTION_PRIMARY = "extracted_txt_rerun.json"
EXTRACTION_FALLBACK = "extracted_txt.json"

SOURCE_COLORS = {"image": "#4C78A8", "text": "#F58518"}
MEAN_LINE_COLORS = {"image": "#A7C7E7", "text": "#F4C28B"}
METHODS = [
    ("gen_pair_f1", "Generation\nnames only", "#E8913A"),
    ("sel_pair_f1", "Selection\nDEGs only", "#5B8DC9"),
    ("ext_pair_f1", "Extraction\ntext pair", "#5AAE61"),
    ("ext_data_f1", "Extraction\n+ data source", "#3A7F49"),
]


def clean_text(value: object) -> str:
    return str(value or "").strip()


def clean_upper(value: object) -> str:
    return clean_text(value).upper()


def load_records(path: Path) -> pd.DataFrame:
    df = pd.read_json(path)
    for col in ["data_id", "group_name", "feature_id", "source_type"]:
        if col not in df:
            df[col] = ""
    df["data_id"] = df["data_id"].map(clean_text)
    df["group_name"] = df["group_name"].map(clean_upper)
    df["feature_id"] = df["feature_id"].map(clean_text)
    df["source_type"] = df["source_type"].map(clean_text).str.lower()
    return df


def key_frame(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    keyed = df[cols].dropna().copy()
    for col in cols:
        keyed = keyed[keyed[col].astype(str).str.len() > 0]
    return keyed.drop_duplicates()


def key_set(df: pd.DataFrame, cols: list[str]) -> set[tuple[str, ...]]:
    keyed = key_frame(df, cols)
    return set(map(tuple, keyed[cols].to_numpy()))


def pair_metrics(predicted: set[tuple[str, ...]], truth: set[tuple[str, ...]]) -> tuple[float, float, float]:
    if not predicted and not truth:
        return 0.0, 0.0, 0.0
    true_positives = len(predicted & truth)
    precision = true_positives / len(predicted) if predicted else 0.0
    recall = true_positives / len(truth) if truth else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def reported_deg_ranks(human: pd.DataFrame, deg: pd.DataFrame, source_type: str) -> list[int]:
    cols = ["data_id", "group_name", "feature_id"]
    reported = key_frame(human[human["source_type"] == source_type], cols)
    deg_ranked = deg[cols + ["metrics_rank"]].dropna(subset=cols + ["metrics_rank"]).copy()
    if reported.empty or deg_ranked.empty:
        return []
    matched = reported.merge(deg_ranked, on=cols, how="inner")
    return sorted(set(matched["metrics_rank"].astype(int)))


def best_rank_recovery(ranks: list[int], max_n: int = 20_000, step: int = 5) -> tuple[int, float]:
    if not ranks:
        return 0, 0.0
    rank_values = np.array(sorted(set(ranks)), dtype=int)
    best_n = 0
    best_f1 = 0.0
    for n in range(1, max_n + 1, step):
        recovered = np.searchsorted(rank_values, n, side="right")
        precision = recovered / n
        recall = recovered / len(rank_values)
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        if f1 > best_f1:
            best_n = n
            best_f1 = f1
    return best_n, best_f1


def upper_bound_pair_f1(truth_pairs: set[tuple[str, str]], deg: pd.DataFrame, top_n: int) -> float:
    deg_top = deg[deg["metrics_rank"] <= top_n]
    deg_pairs = key_set(deg_top, ["group_name", "feature_id"])
    overlap = len(truth_pairs & deg_pairs)
    return 2 * overlap / (len(truth_pairs) + overlap) if overlap else 0.0


def build_cutoff_results() -> pd.DataFrame:
    rows = []
    for dataset, short_name in DATASETS:
        base = DATA_DIR / dataset
        human = load_records(base / "evidence_human" / "extracted.json")
        deg = load_records(base / "evidence_deg" / "extracted.json")
        for source_type in ["image", "text"]:
            ranks = reported_deg_ranks(human, deg, source_type)
            best_n, best_f1 = best_rank_recovery(ranks)
            rows.append(
                {
                    "dataset": dataset,
                    "study": short_name,
                    "source_type": source_type,
                    "optimal_n": best_n,
                    "best_f1": best_f1,
                    "matched_reported_ranks": len(ranks),
                }
            )
    cutoffs = pd.DataFrame(rows)
    cutoffs.to_csv(RESULTS_DIR / "fig2_optimal_deg_cutoff.tsv", sep="\t", index=False)
    return cutoffs


def build_benchmark_summary() -> pd.DataFrame:
    # Keep this panel consistent with Supplementary Table 1.
    summary = pd.DataFrame(
        [
            {"study": "Emont 2022", "label": "Emont", "tissue": "adipose", "cell_types": 45, "genes": 105, "pairs": 346},
            {"study": "Hildreth 2021", "label": "Hildreth", "tissue": "adipose", "cell_types": 31, "genes": 141, "pairs": 234},
            {"study": "He 2021", "label": "He", "tissue": "bone marrow", "cell_types": 27, "genes": 75, "pairs": 370},
            {"study": "Gautam 2021", "label": "Gautam", "tissue": "retina", "cell_types": 32, "genes": 94, "pairs": 251},
            {"study": "Adams 2020", "label": "Adams", "tissue": "lung", "cell_types": 20, "genes": 124, "pairs": 135},
            {"study": "Wagner 2020", "label": "Wagner", "tissue": "ovary", "cell_types": 7, "genes": 62, "pairs": 58},
            {"study": "Shamis 2020", "label": "Shamis", "tissue": "testis", "cell_types": 19, "genes": 125, "pairs": 171},
            {"study": "Total", "label": "", "tissue": "6 tissues", "cell_types": 168, "genes": 641, "pairs": 1_560},
        ]
    )
    summary.to_csv(RESULTS_DIR / "fig2_benchmark_summary.tsv", sep="\t", index=False)
    return summary


def build_llm_results() -> pd.DataFrame:
    rows = []
    for dataset, short_name in DATASETS:
        base = DATA_DIR / dataset
        human = load_records(base / "evidence_human" / "extracted.json")
        human_text = human[human["source_type"] == "text"].copy()
        generated = load_records(base / "evidence_generated" / "extracted.json")
        extraction_path = base / "evidence_llm" / EXTRACTION_PRIMARY
        if not extraction_path.exists():
            extraction_path = base / "evidence_llm" / EXTRACTION_FALLBACK
        extracted = load_records(extraction_path)
        deg = load_records(base / "evidence_deg" / "extracted.json")

        truth_pairs = key_set(human_text, ["group_name", "feature_id"])
        truth_triples = key_set(human_text, ["data_id", "group_name", "feature_id"])

        gen_precision, gen_recall, gen_f1 = pair_metrics(
            key_set(generated, ["group_name", "feature_id"]),
            truth_pairs,
        )

        selection_rows = []
        for n in N_VALUES:
            path = base / "evidence_selected" / f"selected_top{n}.json"
            if not path.exists():
                continue
            selected = load_records(path)
            precision, recall, f1 = pair_metrics(
                key_set(selected, ["group_name", "feature_id"]),
                truth_pairs,
            )
            selection_rows.append(
                {
                    "best_n": n,
                    "sel_precision": precision,
                    "sel_recall": recall,
                    "sel_pair_f1": f1,
                    "sel_bound_f1": upper_bound_pair_f1(truth_pairs, deg, n),
                }
            )
        best_selection = max(selection_rows, key=lambda row: row["sel_pair_f1"])

        ext_precision, ext_recall, ext_f1 = pair_metrics(
            key_set(extracted, ["group_name", "feature_id"]),
            truth_pairs,
        )
        data_precision, data_recall, data_f1 = pair_metrics(
            key_set(extracted, ["data_id", "group_name", "feature_id"]),
            truth_triples,
        )

        rows.append(
            {
                "dataset": dataset,
                "study": short_name,
                "truth_pairs": len(truth_pairs),
                "truth_triples": len(truth_triples),
                "gen_precision": gen_precision,
                "gen_recall": gen_recall,
                "gen_pair_f1": gen_f1,
                **best_selection,
                "ext_precision": ext_precision,
                "ext_recall": ext_recall,
                "ext_pair_f1": ext_f1,
                "ext_data_precision": data_precision,
                "ext_data_recall": data_recall,
                "ext_data_f1": data_f1,
            }
        )
    results = pd.DataFrame(rows)
    results.to_csv(RESULTS_DIR / "fig2_llm_recovery.tsv", sep="\t", index=False)
    return results


def format_int(value: object) -> str:
    if pd.isna(value):
        return ""
    return f"{int(value):,}"


def format_percent(value: object) -> str:
    if pd.isna(value):
        return ""
    return f"{float(value):.0f}%"


def plot_summary_table(ax: plt.Axes, summary: pd.DataFrame) -> None:
    ax.axis("off")
    ax.text(-0.05, 1.04, "A", transform=ax.transAxes, fontsize=11, fontweight="bold", va="top")
    ax.text(
        0.0,
        1.02,
        "LLMarkers benchmark",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10.0,
        fontweight="bold",
    )
    ax.text(
        0.0,
        0.93,
        "7 single-cell studies",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=7.8,
        color="#444444",
    )

    columns = [
        ("study", "Paper"),
        ("cell_types", "CTs"),
        ("genes", "Genes"),
        ("pairs", "Pairs"),
        ("tissue", "Tissue"),
    ]
    left_edges = np.array([0.00, 0.41, 0.54, 0.68, 0.82])
    right_edges = np.array([0.37, 0.50, 0.64, 0.78, 1.00])
    header_y = 0.775
    row_y0 = 0.66
    row_step = 0.087

    ax.hlines(0.855, 0, 1, color="black", linewidth=0.85, transform=ax.transAxes)
    ax.hlines(0.715, 0, 1, color="black", linewidth=0.55, transform=ax.transAxes)
    ax.hlines(-0.015, 0, 1, color="black", linewidth=0.85, transform=ax.transAxes, clip_on=False)
    ax.hlines(0.095, 0, 1, color="black", linewidth=0.45, transform=ax.transAxes)

    for idx, (_field, label) in enumerate(columns):
        ha = "left" if idx in {0, 4} else "right"
        x = left_edges[idx] if idx in {0, 4} else right_edges[idx]
        ax.text(
            x,
            header_y,
            label,
            transform=ax.transAxes,
            ha=ha,
            va="center",
            fontsize=7.7,
            fontweight="bold",
        )

    for row_idx, row in summary.iterrows():
        y = row_y0 - row_idx * row_step
        is_overall = row["study"] == "Total"
        values = {
            "study": row["study"],
            "cell_types": format_int(row["cell_types"]),
            "genes": format_int(row["genes"]),
            "pairs": format_int(row["pairs"]),
            "tissue": row["tissue"],
        }
        for col_idx, (field, _label) in enumerate(columns):
            ha = "left" if col_idx in {0, 4} else "right"
            x = left_edges[col_idx] if col_idx in {0, 4} else right_edges[col_idx]
            ax.text(
                x,
                y,
                values[field],
                transform=ax.transAxes,
                ha=ha,
                va="center",
                fontsize=7.5,
                fontweight="bold" if is_overall else "normal",
            )


def plot_cutoff_panel(ax: plt.Axes, cutoffs: pd.DataFrame) -> None:
    ax.set_xlim(0, max(180, cutoffs["optimal_n"].max() + 15))
    ax.set_ylim(0, 1.0)
    for source_type in ["image", "text"]:
        source_cutoffs = cutoffs[cutoffs["source_type"] == source_type]
        mean_n = source_cutoffs["optimal_n"].mean()
        mean_f1 = source_cutoffs["best_f1"].mean()
        ax.axvline(mean_n, color=MEAN_LINE_COLORS[source_type], linestyle=(0, (3, 2)), linewidth=1.0, zorder=1)
        ax.axhline(mean_f1, color=MEAN_LINE_COLORS[source_type], linestyle=(0, (3, 2)), linewidth=1.0, zorder=1)

    label_offsets = {
        ("Emont", "image"): (4, 0.010),
        ("Emont", "text"): (4, -0.030),
        ("Hildreth", "image"): (4, 0.018),
        ("Hildreth", "text"): (4, -0.028),
        ("He", "image"): (4, -0.030),
        ("He", "text"): (4, 0.018),
        ("Gautam", "image"): (4, 0.015),
        ("Gautam", "text"): (4, -0.030),
        ("Adams", "image"): (4, 0.015),
        ("Adams", "text"): (-31, -0.030),
        ("Wagner", "image"): (4, -0.030),
        ("Wagner", "text"): (4, 0.015),
        ("Shamis", "image"): (4, 0.015),
        ("Shamis", "text"): (-32, -0.030),
    }
    for _, row in cutoffs.iterrows():
        ax.scatter(
            row["optimal_n"],
            row["best_f1"],
            s=36,
            color=SOURCE_COLORS[row["source_type"]],
            edgecolor="black",
            linewidth=0.45,
            zorder=3,
        )
        dx, dy = label_offsets.get((row["study"], row["source_type"]), (4, 0.01))
        ax.annotate(
            row["study"],
            xy=(row["optimal_n"], row["best_f1"]),
            xytext=(dx, dy),
            textcoords="offset points",
            ha="left" if dx >= 0 else "right",
            va="center",
            fontsize=6.5,
        )

    for source_type, color in SOURCE_COLORS.items():
        ax.scatter([], [], s=36, color=color, edgecolor="black", linewidth=0.45, label=source_type.title())
    ax.set_xlabel("Optimal number of DEGs")
    ax.set_ylabel("F-score at optimum")
    ax.legend(frameon=False, loc="upper right", handletextpad=0.4)
    ax.text(-0.13, 1.09, "B", transform=ax.transAxes, fontsize=11, fontweight="bold", va="top")


def plot_llm_panel(ax: plt.Axes, results: pd.DataFrame) -> None:
    x_positions = np.arange(len(METHODS))
    jitter = np.linspace(-0.10, 0.10, len(DATASETS))
    for method_idx, (col, label, color) in enumerate(METHODS):
        values = results[col].to_numpy()
        ax.scatter(
            np.full(len(values), method_idx) + jitter,
            values,
            s=34,
            color=color,
            edgecolor="black",
            linewidth=0.45,
            zorder=3,
        )
        mean_value = values.mean()
        ax.plot(
            [method_idx - 0.22, method_idx + 0.22],
            [mean_value, mean_value],
            color="black",
            linewidth=1.4,
            zorder=4,
        )
        ax.text(method_idx, mean_value + 0.035, f"{mean_value:.2f}", ha="center", va="bottom", fontsize=7.5)

    for row_idx, row in results.iterrows():
        ax.plot(
            [2 + jitter[row_idx], 3 + jitter[row_idx]],
            [row["ext_pair_f1"], row["ext_data_f1"]],
            color="#9A9A9A",
            linewidth=0.7,
            alpha=0.8,
            zorder=1,
        )

    ax.set_xticks(x_positions)
    ax.set_xticklabels([label for _, label, _ in METHODS])
    ax.set_ylabel("F-score")
    ax.set_ylim(0, 1.0)
    ax.set_xlim(-0.55, len(METHODS) - 0.45)
    ax.axhline(0.5, color="#D0D0D0", linewidth=0.8, zorder=0)
    ax.tick_params(axis="x", length=0)
    ax.text(-0.13, 1.09, "C", transform=ax.transAxes, fontsize=11, fontweight="bold", va="top")


def main() -> None:
    plt.rcParams.update(
        {
            "font.size": 8.5,
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    summary = build_benchmark_summary()
    cutoffs = build_cutoff_results()
    llm_results = build_llm_results()

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(12.8, 3.35),
        gridspec_kw={"width_ratios": [1.12, 1.04, 1.20]},
    )
    plot_summary_table(axes[0], summary)
    plot_cutoff_panel(axes[1], cutoffs)
    plot_llm_panel(axes[2], llm_results)
    fig.subplots_adjust(left=0.04, right=0.99, bottom=0.22, top=0.93, wspace=0.36)

    fig.savefig(FIGURE_DIR / "fig_marker_recovery.pdf", bbox_inches="tight")
    fig.savefig(FIGURE_DIR / "fig_marker_recovery.png", bbox_inches="tight", dpi=240)
    print(f"saved {FIGURE_DIR / 'fig_marker_recovery.pdf'}")
    print(cutoffs[["study", "source_type", "optimal_n", "best_f1"]].to_string(index=False))
    print(llm_results[[col for col, _, _ in METHODS]].mean().to_string(float_format=lambda value: f"{value:.3f}"))


if __name__ == "__main__":
    main()
