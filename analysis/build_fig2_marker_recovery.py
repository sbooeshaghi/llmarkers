from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
FIGURE_DIR = REPO_ROOT / "analysis" / "figures"
RESULTS_DIR = REPO_ROOT / "analysis" / "artifacts"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

PANEL_A_PATH = FIGURE_DIR / "fig2_panel_a_modality_deg_presence.pdf"
PANEL_A_PNG_PATH = FIGURE_DIR / "fig2_panel_a_modality_deg_presence.png"
PANEL_B_PATH = FIGURE_DIR / "fig2_panel_b_rank_recovery.pdf"
PANEL_B_PNG_PATH = FIGURE_DIR / "fig2_panel_b_rank_recovery.png"
RANK_RECOVERY_N_MAX = 200
PANEL_C_PATH = FIGURE_DIR / "fig2_panel_c_llm_recovery.pdf"
PANEL_C_PNG_PATH = FIGURE_DIR / "fig2_panel_c_llm_recovery.png"

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
SOURCE_DISPLAY = {"image": "Figure", "text": "Text"}
BOTH_COLOR = "#B0B0B0"
PRESENCE_COLOR = "#D9D9D9"
MEAN_LINE_COLORS = {"image": "#A7C7E7", "text": "#F4C28B"}
METHODS = [
    ("gen_pair_f1", "Generation\n(cell type names)", "#E8913A"),
    ("sel_pair_f1", "Selection\n(DEGs)", "#5B8DC9"),
    ("joint_pair_f1", "Extraction\n(cell type + gene)", "#5AAE61"),
    (
        "joint_triple_f1",
        "Extraction\n(+ data ID)",
        "#3A7F49",
    ),
]

JOINT_RESULTS_PATH = (
    RESULTS_DIR
    / "mrkr_benchmark_pilot_20260721"
    / "joint_deg_extraction_v1"
    / "joint_extraction_papers.tsv"
)
BENCHMARK_ROOT = RESULTS_DIR / "benchmark_evidence_v1" / "papers"
DATASET_TO_PAPER = {
    dataset: dataset.split("_", 1)[1] for dataset, _short_name in DATASETS
}


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


def human_records(df: pd.DataFrame) -> pd.DataFrame:
    if "organism" not in df:
        return df.copy()
    organism = (
        df["organism"].fillna("").astype(str).str.casefold().str.replace("_", " ")
    )
    return df[organism.isin({"homo sapiens", "human"})].copy()


def benchmark_human_text_facts(
    dataset: str,
) -> tuple[set[tuple[str, str]], set[tuple[str, str, str]]]:
    paper_id = DATASET_TO_PAPER[dataset]
    path = BENCHMARK_ROOT / paper_id / "primary" / "text.claims.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    pairs: set[tuple[str, str]] = set()
    triples: set[tuple[str, str, str]] = set()
    for claim in document["claims"]:
        organism = next(
            term for term in claim["terms"] if term["term_type"] == "organism"
        )
        if organism.get("ontology_term") != "NCBITaxon:9606":
            continue
        target = next(
            term for term in claim["terms"] if term["term_type"] == "celltype"
        )
        label = clean_upper(
            target.get("legacy_normalized_label") or target.get("normalized_label")
        )
        data_id = clean_text(claim["evidence"].get("data_id"))
        for gene in claim["terms"]:
            gene_id = clean_text(gene.get("ontology_term"))
            if gene["term_type"] != "gene" or not gene_id:
                continue
            pairs.add((label, gene_id))
            if data_id:
                triples.add((data_id, label, gene_id))
    return pairs, triples


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


def matched_pair_ranks(human: pd.DataFrame, deg: pd.DataFrame, source_type: str) -> np.ndarray:
    """DEG-table rank for each reported (data_id, cell type, gene) association."""
    cols = ["data_id", "group_name", "feature_id"]
    reported = key_frame(human[human["source_type"] == source_type], cols)
    ranked = deg.dropna(subset=["metrics_rank"]).sort_values("metrics_rank")
    ranked = key_frame(ranked, cols).join(ranked["metrics_rank"])
    ranked = ranked.drop_duplicates(subset=cols, keep="first")
    merged = reported.merge(ranked, on=cols, how="inner")
    return merged["metrics_rank"].astype(int).to_numpy()


def build_rank_recovery() -> pd.DataFrame:
    rows = []
    for dataset, short_name in DATASETS:
        base = DATA_DIR / dataset
        human = valid_marker_records(load_records(base / "evidence_human" / "extracted.json"))
        deg = valid_marker_records(load_records(base / "evidence_deg" / "extracted.json"))
        for source_type in ["image", "text"]:
            for rank in matched_pair_ranks(human, deg, source_type):
                rows.append({"study": short_name, "source_type": source_type, "rank": int(rank)})
    ranks_df = pd.DataFrame(rows)
    ranks_df.to_csv(RESULTS_DIR / "fig2_rank_recovery.tsv", sep="\t", index=False)

    ns = np.arange(1, RANK_RECOVERY_N_MAX + 1)
    summary_rows = []
    for source_type in ["image", "text"]:
        pooled = ranks_df.loc[ranks_df["source_type"] == source_type, "rank"].to_numpy()
        f1_curves = []
        for study in ranks_df["study"].unique():
            study_ranks = np.array(
                sorted(set(ranks_df.query("study == @study and source_type == @source_type")["rank"]))
            )
            if not len(study_ranks):
                continue
            recovered = (study_ranks[None, :] <= ns[:, None]).sum(axis=1)
            precision = recovered / ns
            recall = recovered / len(study_ranks)
            with np.errstate(invalid="ignore", divide="ignore"):
                f1 = np.where(precision + recall > 0, 2 * precision * recall / (precision + recall), 0.0)
            f1_curves.append(f1)
        mean_f1 = np.mean(f1_curves, axis=0)
        best = int(np.argmax(mean_f1))
        summary_rows.append(
            {
                "source_type": source_type,
                "n_matched": len(pooled),
                "pooled_recall_top50": float(np.mean(pooled <= 50)),
                "pooled_recall_top100": float(np.mean(pooled <= 100)),
                "mean_f1_peak_n": int(ns[best]),
                "mean_f1_peak": float(mean_f1[best]),
            }
        )
    pd.DataFrame(summary_rows).to_csv(RESULTS_DIR / "fig2_rank_recovery_summary.tsv", sep="\t", index=False)
    return ranks_df


def save_rank_recovery_panel(ranks_df: pd.DataFrame) -> None:
    ns = np.arange(1, RANK_RECOVERY_N_MAX + 1)
    fig, (ax, axm) = plt.subplots(
        2, 1, figsize=(3.9, 3.35), sharex=True,
        gridspec_kw={"height_ratios": [2.1, 1.0], "hspace": 0.14},
    )
    for (study, source_type), group in ranks_df.groupby(["study", "source_type"]):
        ranks = group["rank"].to_numpy()
        recall = (ranks[None, :] <= ns[:, None]).mean(axis=1)
        ax.plot(ns, recall, color=SOURCE_COLORS[source_type], linewidth=0.8, alpha=0.35)
    for source_type in ["image", "text"]:
        pooled = ranks_df.loc[ranks_df["source_type"] == source_type, "rank"].to_numpy()
        recall = (pooled[None, :] <= ns[:, None]).mean(axis=1)
        ax.plot(ns, recall, color=SOURCE_COLORS[source_type], linewidth=2.0, label=SOURCE_DISPLAY[source_type])
        for guide in (50, 100):
            ax.scatter([guide], [np.mean(pooled <= guide)], s=14, color=SOURCE_COLORS[source_type],
                       edgecolor="black", linewidth=0.5, zorder=4)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("Fraction of reported\nmarkers recovered", fontsize=8)
    ax.tick_params(axis="both", labelsize=7.2)
    ax.legend(frameon=False, fontsize=6.8, loc="lower right", handlelength=1.4)

    for source_type in ["image", "text"]:
        f1_curves = []
        for study in ranks_df["study"].unique():
            study_ranks = np.array(
                sorted(set(ranks_df.query("study == @study and source_type == @source_type")["rank"]))
            )
            if not len(study_ranks):
                continue
            recovered = (study_ranks[None, :] <= ns[:, None]).sum(axis=1)
            precision = recovered / ns
            recall = recovered / len(study_ranks)
            with np.errstate(invalid="ignore", divide="ignore"):
                f1 = np.where(precision + recall > 0, 2 * precision * recall / (precision + recall), 0.0)
            f1_curves.append(f1)
        mean_f1 = np.mean(f1_curves, axis=0)
        axm.plot(ns, mean_f1, color=SOURCE_COLORS[source_type], linewidth=1.6)
        best = int(np.argmax(mean_f1))
        axm.scatter([ns[best]], [mean_f1[best]], s=14, color=SOURCE_COLORS[source_type],
                    edgecolor="black", linewidth=0.5, zorder=4)
    axm.set_ylim(0, 0.6)
    axm.set_yticks([0, 0.25, 0.5])
    axm.set_ylabel("Mean F1", fontsize=8)
    axm.set_xlim(0, RANK_RECOVERY_N_MAX)
    axm.set_xticks([0, 50, 100, 150, 200])
    axm.set_xlabel("Top N DEGs")
    axm.tick_params(axis="both", labelsize=7.2)
    fig.savefig(PANEL_B_PATH, bbox_inches="tight")
    fig.savefig(PANEL_B_PNG_PATH, bbox_inches="tight", dpi=300)
    plt.close(fig)


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
        generated = human_records(
            load_records(base / "evidence_generated" / "extracted.json")
        )
        extraction_path = base / "evidence_llm" / EXTRACTION_PRIMARY
        if not extraction_path.exists():
            extraction_path = base / "evidence_llm" / EXTRACTION_FALLBACK
        extracted = human_records(load_records(extraction_path))
        deg = human_records(load_records(base / "evidence_deg" / "extracted.json"))

        truth_pairs, truth_triples = benchmark_human_text_facts(dataset)

        gen_precision, gen_recall, gen_f1 = pair_metrics(
            key_set(generated, ["group_name", "feature_id"]),
            truth_pairs,
        )

        selection_rows = []
        for n in N_VALUES:
            path = base / "evidence_selected" / f"selected_top{n}.json"
            if not path.exists():
                continue
            selected = human_records(load_records(path))
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

    paper_to_study = {
        dataset.split("_", 1)[1]: short_name for dataset, short_name in DATASETS
    }
    joint = pd.read_csv(JOINT_RESULTS_PATH, sep="\t")
    joint["study"] = joint["paper_id"].map(paper_to_study)
    if joint["study"].isna().any():
        missing = joint.loc[joint["study"].isna(), "paper_id"].tolist()
        raise ValueError(f"unknown joint-extraction papers: {missing}")
    joint = joint.rename(
        columns={
            "pair_precision": "joint_pair_precision",
            "pair_recall": "joint_pair_recall",
            "pair_f1": "joint_pair_f1",
            "triple_precision": "joint_triple_precision",
            "triple_recall": "joint_triple_recall",
            "triple_f1": "joint_triple_f1",
        }
    )
    merged = results.merge(
        joint[
            [
                "study",
                "joint_pair_precision",
                "joint_pair_recall",
                "joint_pair_f1",
                "joint_triple_precision",
                "joint_triple_recall",
                "joint_triple_f1",
            ]
        ],
        on="study",
        validate="one_to_one",
    )
    merged.to_csv(
        RESULTS_DIR / "fig2_llm_recovery_current.tsv", sep="\t", index=False
    )
    return merged


def valid_marker_records(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["group_name"] != "") & df["feature_id"].str.startswith("ENS")]


def build_modality_presence() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Per-study report-location split and DE-table presence for reported markers."""
    mod_rows: list[dict] = []
    pres_rows: list[dict] = []
    global_text: set[tuple[str, str]] = set()
    global_image: set[tuple[str, str]] = set()
    for dataset, short_name in DATASETS:
        base = DATA_DIR / dataset
        human = valid_marker_records(load_records(base / "evidence_human" / "extracted.json"))
        deg = valid_marker_records(load_records(base / "evidence_deg" / "extracted.json"))
        text_pairs = key_set(human[human["source_type"] == "text"], ["group_name", "feature_id"])
        image_pairs = key_set(human[human["source_type"] == "image"], ["group_name", "feature_id"])
        mod_rows.append(
            {
                "study": short_name,
                "image_only": len(image_pairs - text_pairs),
                "text_only": len(text_pairs - image_pairs),
                "both": len(text_pairs & image_pairs),
            }
        )
        global_text |= text_pairs
        global_image |= image_pairs
        human_pairs = key_set(human, ["group_name", "feature_id"])
        deg_pairs = key_set(deg, ["group_name", "feature_id"])
        pres_rows.append(
            {
                "study": short_name,
                "n_reported": len(human_pairs),
                "n_in_deg": len(human_pairs & deg_pairs),
            }
        )
    mod_rows.append(
        {
            "study": "All",
            "image_only": len(global_image - global_text),
            "text_only": len(global_text - global_image),
            "both": len(global_text & global_image),
        }
    )
    pres_rows.append(
        {
            "study": "All",
            "n_reported": sum(row["n_reported"] for row in pres_rows),
            "n_in_deg": sum(row["n_in_deg"] for row in pres_rows),
        }
    )
    modality = pd.DataFrame(mod_rows)
    modality["n"] = modality[["image_only", "text_only", "both"]].sum(axis=1)
    presence = pd.DataFrame(pres_rows)
    presence["fraction_in_deg"] = presence["n_in_deg"] / presence["n_reported"]
    modality.to_csv(RESULTS_DIR / "fig2_modality.tsv", sep="\t", index=False)
    presence.to_csv(RESULTS_DIR / "fig2_deg_presence.tsv", sep="\t", index=False)
    return modality, presence


def plot_modality_presence_panel(ax: plt.Axes, modality: pd.DataFrame, presence: pd.DataFrame) -> None:
    ypos = np.arange(len(modality))
    for i, (mod_row, pres_row) in enumerate(zip(modality.itertuples(index=False), presence.itertuples(index=False))):
        n = mod_row.image_only + mod_row.text_only + mod_row.both
        fractions = [mod_row.image_only / n, mod_row.text_only / n, mod_row.both / n]
        left = 0.0
        for fraction, color in zip(fractions, [SOURCE_COLORS["image"], SOURCE_COLORS["text"], BOTH_COLOR]):
            ax.barh(i, -fraction, left=-left, height=0.62, facecolor=color, edgecolor="black", linewidth=0.55)
            left += fraction
        ax.barh(i, pres_row.fraction_in_deg, height=0.62, facecolor=PRESENCE_COLOR, edgecolor="black", linewidth=0.55)

    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_yticks(ypos)
    ax.set_yticklabels(
        [f"{row.study} (n={row.n:,})" for row in modality.itertuples(index=False)], fontsize=7.2
    )
    ax.tick_params(axis="y", length=0)
    ax.invert_yaxis()
    ax.set_xlim(-1.0, 1.0)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xticklabels(["1.0", "0.5", "0", "0.5", "1.0"], fontsize=7.2)
    ax.spines["left"].set_visible(False)
    ax.text(-0.5, -0.13, "Fraction of reported markers\nby source",
            transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=7.6)
    ax.text(0.5, -0.13, "Fraction of reported markers\nin DE tables",
            transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=7.6)
    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor="black", linewidth=0.55)
        for color in [SOURCE_COLORS["image"], SOURCE_COLORS["text"], BOTH_COLOR]
    ]
    ax.legend(handles, ["Figure only", "Text only", "Both"], frameon=False, fontsize=6.6,
              loc="upper center", bbox_to_anchor=(0.28, 1.14), ncol=3, columnspacing=0.8, handlelength=1.1)


def plot_cutoff_panel(ax: plt.Axes, cutoffs: pd.DataFrame) -> None:
    ax.set_xlim(0, max(180, cutoffs["optimal_n"].max() + 15))
    ax.set_ylim(0, 1.0)

    label_offsets = {
        ("Emont", "image"): (5, 4),
        ("Emont", "text"): (5, -8),
        ("Hildreth", "image"): (5, 4),
        ("Hildreth", "text"): (5, 7),
        ("He", "image"): (-6, -8),
        ("He", "text"): (5, 4),
        ("Gautam", "image"): (5, 4),
        ("Gautam", "text"): (-6, -8),
        ("Adams", "image"): (5, 4),
        ("Adams", "text"): (-6, -8),
        ("Wagner", "image"): (5, -10),
        ("Wagner", "text"): (-6, 7),
        ("Shamis", "image"): (-6, -10),
        ("Shamis", "text"): (5, -4),
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
        ax.scatter([], [], s=36, color=color, edgecolor="black", linewidth=0.45, label=SOURCE_DISPLAY[source_type])
    ax.set_xlabel("Optimal number of DEGs")
    ax.set_ylabel("F-score at optimum")
    ax.legend(frameon=False, loc="upper right", handletextpad=0.4)


def plot_llm_panel(ax: plt.Axes, results: pd.DataFrame) -> None:
    x_positions = np.arange(len(METHODS))
    jitter = np.linspace(-0.13, 0.13, len(DATASETS))
    for method_idx, (col, label, color) in enumerate(METHODS):
        values = results[col].to_numpy()
        ax.bar(
            x_positions[method_idx],
            values.mean(),
            width=0.58,
            facecolor=color,
            alpha=0.45,
            edgecolor="black",
            linewidth=0.7,
            zorder=2,
        )
        ax.scatter(
            np.full(len(values), method_idx) + jitter,
            values,
            s=26,
            color=color,
            edgecolor="black",
            linewidth=0.5,
            zorder=3,
        )

    # best achievable selection F1 if the model chose perfectly from the DEG list
    ax.scatter(
        1 + jitter,
        results["sel_bound_f1"],
        s=24,
        facecolor="white",
        edgecolor="#39618C",
        linewidth=1.0,
        zorder=3,
    )
    ax.hlines(
        results["sel_bound_f1"].mean(),
        1 - 0.29,
        1 + 0.29,
        color="#39618C",
        linewidth=1.2,
        linestyle=(0, (3, 2)),
        zorder=4,
    )

    ax.set_xticks(x_positions)
    ax.set_xticklabels([label for _, label, _ in METHODS])
    ax.set_ylabel("F-score")
    ax.set_ylim(0, 1.0)
    ax.set_xlim(-0.55, len(METHODS) - 0.45)
    ax.tick_params(axis="x", length=0)


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
    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, bbox_inches="tight", dpi=300)
    plt.close(fig)


def main() -> None:
    plt.rcParams.update(
        {
            "font.size": 8.5,
            "font.family": "DejaVu Sans",
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    build_benchmark_summary()
    modality, presence = build_modality_presence()
    ranks_df = build_rank_recovery()
    cutoffs = build_cutoff_results()
    llm_results = build_llm_results()

    save_single_panel(
        PANEL_A_PATH,
        PANEL_A_PNG_PATH,
        lambda ax: plot_modality_presence_panel(ax, modality, presence),
        figsize=(4.6, 3.35),
    )
    save_rank_recovery_panel(ranks_df)
    save_single_panel(
        PANEL_C_PATH,
        PANEL_C_PNG_PATH,
        lambda ax: plot_llm_panel(ax, llm_results),
        figsize=(4.3, 3.35),
        adjust={"left": 0.14, "right": 0.98, "bottom": 0.22, "top": 0.94},
    )
    print(f"saved {PANEL_A_PATH}")
    print(f"saved {PANEL_B_PATH}")
    print(f"saved {PANEL_C_PATH}")
    print(cutoffs[["study", "source_type", "optimal_n", "best_f1"]].to_string(index=False))
    print(llm_results[[col for col, _, _ in METHODS]].mean().to_string(float_format=lambda value: f"{value:.3f}"))


if __name__ == "__main__":
    main()
