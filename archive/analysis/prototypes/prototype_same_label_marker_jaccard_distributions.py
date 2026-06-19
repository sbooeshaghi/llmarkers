from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "analysis"))

from build_cap_llmarkers_comparison import build_cap_human_profiles
from build_fig3_local_global_marker_identifiability import cap_profiles_with_ontology_terms
from build_local_global_marker_analysis import build_profiles, jaccard


ARCHIVE_ROOT = REPO_ROOT / "archive" / "analysis"
FIGURE_DIR = ARCHIVE_ROOT / "figures" / "archive-2026-06-13"
RESULTS_DIR = ARCHIVE_ROOT / "results" / "archive-2026-06-13"
OUT_VALUES = RESULTS_DIR / "prototype_same_label_marker_jaccard_values.tsv"
OUT_SUMMARY = RESULTS_DIR / "prototype_same_label_marker_jaccard_summary.tsv"
OUT_FIGURE = FIGURE_DIR / "prototype_same_label_marker_jaccard_distributions.pdf"
OUT_PNG = FIGURE_DIR / "prototype_same_label_marker_jaccard_distributions.png"


def sample_pairs(values: list[float], max_n: int, rng: np.random.Generator) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if len(arr) <= max_n:
        return arr
    return rng.choice(arr, size=max_n, replace=False)


def build_pairwise_distributions(
    profiles_df: pd.DataFrame,
    resource: str,
    label_col: str = "normalized_cell_type",
    context_col: str = "study_uid",
    max_random_pairs: int = 100_000,
    seed: int = 11,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    profiles = profiles_df.loc[profiles_df[label_col].fillna("").astype(str).str.strip().ne("")].copy()
    profiles = profiles.reset_index(drop=True)
    rows = list(profiles.itertuples(index=False))

    same_label_values: list[float] = []
    same_label_counts: dict[str, int] = defaultdict(int)
    for label, label_df in profiles.groupby(label_col, sort=True):
        if len(label_df) < 2 or label_df[context_col].nunique() < 2:
            continue
        for row_a, row_b in combinations(label_df.itertuples(index=False), 2):
            if getattr(row_a, context_col) == getattr(row_b, context_col):
                continue
            _shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
            same_label_values.append(value)
            same_label_counts[str(label)] += 1

    random_values: list[float] = []
    n = len(rows)
    attempts = 0
    target_attempts = max_random_pairs * 5
    while len(random_values) < max_random_pairs and attempts < target_attempts:
        attempts += 1
        idx_a, idx_b = rng.integers(0, n, size=2)
        if idx_a == idx_b:
            continue
        row_a = rows[int(idx_a)]
        row_b = rows[int(idx_b)]
        if getattr(row_a, context_col) == getattr(row_b, context_col):
            continue
        if getattr(row_a, label_col) == getattr(row_b, label_col):
            continue
        _shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
        random_values.append(value)

    value_rows = []
    for value in sample_pairs(same_label_values, 20_000, rng):
        value_rows.append({"resource": resource, "comparison": "Same label", "marker_jaccard": value})
    for value in sample_pairs(random_values, 20_000, rng):
        value_rows.append({"resource": resource, "comparison": "Random different labels", "marker_jaccard": value})

    summary_rows = []
    for comparison, values in [
        ("Same label", same_label_values),
        ("Random different labels", random_values),
    ]:
        arr = np.asarray(values, dtype=float)
        summary_rows.append(
            {
                "resource": resource,
                "comparison": comparison,
                "n_pairs": len(arr),
                "n_labels_with_pairs": len(same_label_counts) if comparison == "Same label" else np.nan,
                "mean_jaccard": float(arr.mean()) if len(arr) else np.nan,
                "median_jaccard": float(np.median(arr)) if len(arr) else np.nan,
                "q25_jaccard": float(np.quantile(arr, 0.25)) if len(arr) else np.nan,
                "q75_jaccard": float(np.quantile(arr, 0.75)) if len(arr) else np.nan,
                "pct_jaccard_eq_0": float((arr == 0).mean()) if len(arr) else np.nan,
                "pct_jaccard_gt_0": float((arr > 0).mean()) if len(arr) else np.nan,
                "pct_jaccard_ge_0_25": float((arr >= 0.25).mean()) if len(arr) else np.nan,
                "pct_jaccard_eq_1": float((arr == 1).mean()) if len(arr) else np.nan,
            }
        )

    return pd.DataFrame(value_rows), pd.DataFrame(summary_rows)


def plot_distributions(values_df: pd.DataFrame, summary_df: pd.DataFrame) -> None:
    resources = ["LLMarkers", "CAP ontology"]
    colors = {"Same label": "#4C78A8", "Random different labels": "#BAB0AC"}
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7), sharex=True, sharey=True)
    bins = np.linspace(0, 1, 26)

    for ax, resource in zip(axes, resources):
        for comparison in ["Random different labels", "Same label"]:
            subset = values_df.loc[
                values_df["resource"].eq(resource) & values_df["comparison"].eq(comparison),
                "marker_jaccard",
            ].to_numpy(dtype=float)
            ax.hist(
                subset,
                bins=bins,
                density=True,
                histtype="stepfilled" if comparison == "Same label" else "step",
                alpha=0.45 if comparison == "Same label" else 1.0,
                linewidth=1.2,
                color=colors[comparison],
                label=comparison,
            )
        same = summary_df.loc[
            summary_df["resource"].eq(resource) & summary_df["comparison"].eq("Same label")
        ].iloc[0]
        random = summary_df.loc[
            summary_df["resource"].eq(resource) & summary_df["comparison"].eq("Random different labels")
        ].iloc[0]
        ax.set_title(
            f"{resource}\nJ>0 {same.pct_jaccard_gt_0:.0%} vs {random.pct_jaccard_gt_0:.0%}; "
            f"mean J {same.mean_jaccard:.2f} vs {random.mean_jaccard:.3f}",
            fontsize=8.5,
            weight="bold",
        )
        ax.set_xlabel("Marker gene set Jaccard")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    axes[0].set_ylabel("Density")
    axes[0].legend(frameon=False, fontsize=7, loc="upper right")
    fig.tight_layout(w_pad=1.2)
    for path in [OUT_FIGURE, OUT_PNG]:
        fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    llmarkers_profiles, _id_to_name = build_profiles()
    cap_profiles, _cap_records, _cap_id_to_name = build_cap_human_profiles()
    cap_ontology_profiles = cap_profiles_with_ontology_terms(cap_profiles)

    values = []
    summaries = []
    for profiles, resource, context_col in [
        (llmarkers_profiles, "LLMarkers", "paper_uid"),
        (cap_ontology_profiles, "CAP ontology", "study_uid"),
    ]:
        value_df, summary_df = build_pairwise_distributions(
            profiles,
            resource=resource,
            label_col="normalized_cell_type",
            context_col=context_col,
        )
        values.append(value_df)
        summaries.append(summary_df)

    values_df = pd.concat(values, ignore_index=True)
    summary_df = pd.concat(summaries, ignore_index=True)
    values_df.to_csv(OUT_VALUES, sep="\t", index=False)
    summary_df.to_csv(OUT_SUMMARY, sep="\t", index=False)
    plot_distributions(values_df, summary_df)
    print(summary_df.to_string(index=False))
    print(f"Wrote {OUT_FIGURE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
