from __future__ import annotations

from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "analysis" / "results"

DIFF_REVIEW_PATH = RESULTS_DIR / "cross_study_context_comparison_review_anchored.tsv"
PARTIAL_REVIEW_PATH = RESULTS_DIR / "cross_study_same_label_partial_pairs_review.tsv"

DIFF_OUT_PATH = RESULTS_DIR / "cross_study_row3_name_judgment_diff_labels_j1.tsv"
PARTIAL_OUT_PATH = RESULTS_DIR / "cross_study_row3_name_judgment_same_label_partial.tsv"
EXCLUDED_OUT_PATH = RESULTS_DIR / "cross_study_row3_name_judgment_excluded_same_paper_versions.tsv"
SUMMARY_OUT_PATH = RESULTS_DIR / "cross_study_row3_name_judgment_summary.tsv"


MODE_DIFF = "Different labels, exact marker match (J=1)"
MODE_PARTIAL = "Same label, partial marker overlap (0<J<1)"

JUDGMENT_ORDER = [
    "Same name supported",
    "Context distinction",
    "Unresolved",
]

DIFF_JUDGMENT_MAP = {
    "exactMatch": "Same name supported",
    "closeMatch": "Context distinction",
    "broadMatch": "Context distinction",
    "narrowMatch": "Context distinction",
    "relatedMatch": "Context distinction",
    "unresolved": "Unresolved",
}

PARTIAL_JUDGMENT_MAP = {
    "same_entity_reporting_detail": "Same name supported",
    "same_entity_state_context": "Context distinction",
    "same_entity_granularity": "Context distinction",
}

SAME_PAPER_VERSION_EXCLUSIONS = {
    frozenset(
        {
            "biorxiv:9f9eded3-6d6e-1014-996d-af8f6f192d54",
            "hca:0134_10.3389_fimmu.2021.636720_9a958ecc4e",
        }
    ): "same paper/version: PBMC activation preprint and published HCA record",
    frozenset(
        {
            "biorxiv:78211bc7-6c0f-1014-bc42-c103d41718b8",
            "hca:0048_10.1038_s41588-022-01243-4_ae2af85553",
        }
    ): "same paper/version: lung spatial atlas preprint and published HCA record",
}


def same_paper_version_reason(paper_1: object, paper_2: object) -> str:
    pair = frozenset({str(paper_1), str(paper_2)})
    return SAME_PAPER_VERSION_EXCLUSIONS.get(pair, "")


def build_diff_table() -> pd.DataFrame:
    df = pd.read_csv(DIFF_REVIEW_PATH, sep="\t")
    df = df.loc[df["jaccard"].round(6) == 1.0].copy()
    df["name_judgment"] = df["skos_relation_from_1_to_2"].map(DIFF_JUDGMENT_MAP)
    df["mode"] = MODE_DIFF
    df["excluded_pair_reason"] = [
        same_paper_version_reason(paper_1, paper_2)
        for paper_1, paper_2 in zip(df["paper_1"], df["paper_2"], strict=True)
    ]
    keep_cols = [
        "mode",
        "name_judgment",
        "skos_relation_from_1_to_2",
        "cell_type_1",
        "cell_type_2",
        "paper_1",
        "paper_2",
        "markers_1",
        "markers_2",
        "pairwise_assessment",
        "followup_flag",
        "jaccard",
        "excluded_pair_reason",
    ]
    return df.loc[:, keep_cols]


def build_partial_table() -> pd.DataFrame:
    df = pd.read_csv(PARTIAL_REVIEW_PATH, sep="\t")
    df = df.loc[df["review_resolution_class"].notna()].copy()
    df["name_judgment"] = df["review_resolution_class"].map(PARTIAL_JUDGMENT_MAP)
    df["mode"] = MODE_PARTIAL
    df["excluded_pair_reason"] = [
        same_paper_version_reason(paper_1, paper_2)
        for paper_1, paper_2 in zip(df["paper_key_1"], df["paper_key_2"], strict=True)
    ]
    keep_cols = [
        "mode",
        "name_judgment",
        "review_resolution_class",
        "cell_type",
        "paper_key_1",
        "paper_key_2",
        "shared_markers",
        "unique_markers_1",
        "unique_markers_2",
        "pairwise_assessment",
        "top_label_neighbor_marker_jaccard",
        "excluded_pair_reason",
    ]
    return df.loc[:, keep_cols]


def build_summary(diff_df: pd.DataFrame, partial_df: pd.DataFrame) -> pd.DataFrame:
    combined = pd.concat(
        [
            diff_df.loc[:, ["mode", "name_judgment"]],
            partial_df.loc[:, ["mode", "name_judgment"]],
        ],
        ignore_index=True,
    )
    summary = (
        combined.groupby(["mode", "name_judgment"], dropna=False)
        .size()
        .rename("count")
        .reset_index()
    )

    totals = summary.groupby("mode")["count"].transform("sum")
    summary["fraction"] = summary["count"] / totals

    mode_order = [MODE_DIFF, MODE_PARTIAL]
    summary["mode"] = pd.Categorical(summary["mode"], categories=mode_order, ordered=True)
    summary["name_judgment"] = pd.Categorical(
        summary["name_judgment"],
        categories=JUDGMENT_ORDER,
        ordered=True,
    )
    summary = summary.sort_values(["mode", "name_judgment"]).reset_index(drop=True)
    return summary


def main() -> None:
    diff_df = build_diff_table()
    partial_df = build_partial_table()
    excluded_df = pd.concat(
        [
            diff_df.loc[diff_df["excluded_pair_reason"] != ""].copy(),
            partial_df.loc[partial_df["excluded_pair_reason"] != ""].copy(),
        ],
        ignore_index=True,
    )
    diff_df = diff_df.loc[diff_df["excluded_pair_reason"] == ""].drop(columns=["excluded_pair_reason"])
    partial_df = partial_df.loc[partial_df["excluded_pair_reason"] == ""].drop(columns=["excluded_pair_reason"])
    summary_df = build_summary(diff_df, partial_df)

    diff_df.to_csv(DIFF_OUT_PATH, sep="\t", index=False)
    partial_df.to_csv(PARTIAL_OUT_PATH, sep="\t", index=False)
    excluded_df.to_csv(EXCLUDED_OUT_PATH, sep="\t", index=False)
    summary_df.to_csv(SUMMARY_OUT_PATH, sep="\t", index=False)

    print(f"Wrote {DIFF_OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {PARTIAL_OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {EXCLUDED_OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {SUMMARY_OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
