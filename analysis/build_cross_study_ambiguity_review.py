from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "analysis" / "results"

DIFF_REVIEW_PATH = RESULTS_DIR / "cross_study_context_comparison_review_anchored.tsv"
PARTIAL_REVIEW_PATH = RESULTS_DIR / "cross_study_same_label_partial_pairs_review.tsv"

PAIRS_OUT_PATH = RESULTS_DIR / "cross_study_ambiguity_review_pairs.tsv"
EXCLUDED_PAIRS_OUT_PATH = RESULTS_DIR / "cross_study_ambiguity_review_pairs_excluded_same_paper_versions.tsv"
MARKDOWN_OUT_PATH = RESULTS_DIR / "cross_study_context_comparison_review_anchored.md"

MODE_DIFF = "Different labels, exact marker match (J=1)"
MODE_PARTIAL = "Same label, partial marker overlap (0<J<1)"

MODE_ORDER = [MODE_DIFF, MODE_PARTIAL]
RESULT_ORDER = [
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


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return " ".join(str(value).split())


def split_markers(value: object) -> list[str]:
    text = normalize_text(value)
    if not text:
        return []
    return [item.strip() for item in text.split(";") if item.strip()]


def join_markers(value: object) -> str:
    markers = split_markers(value)
    return "; ".join(markers) if markers else ""


def to_abs_path(relative_path: object) -> Path | None:
    rel = normalize_text(relative_path)
    if not rel:
        return None
    return REPO_ROOT / rel


def manuscript_title(relative_path: object) -> str:
    path = to_abs_path(relative_path)
    if path is None or not path.exists():
        return ""
    with path.open() as handle:
        for line in handle:
            text = line.strip()
            if not text:
                continue
            text = re.sub(r"^#+\s*", "", text).strip()
            if text:
                return text
    return ""


def escape_md(value: object) -> str:
    text = normalize_text(value)
    if not text:
        return "—"
    return text.replace("|", "\\|")


def code_or_dash(value: object) -> str:
    text = normalize_text(value)
    if not text:
        return "—"
    return f"`{text.replace('`', '')}`"


def manuscript_link(relative_path: object, line_number: object | None = None) -> str:
    path = to_abs_path(relative_path)
    if path is None:
        return "—"
    target = str(path)
    if line_number is not None and not pd.isna(line_number):
        target = f"{target}#L{int(line_number)}"
    return f"[open manuscript]({target})"


def classify_mode(name_match: str, jaccard: float) -> str:
    if name_match == "Different labels" and round(jaccard, 6) == 1.0:
        return MODE_DIFF
    if name_match == "Same label" and 0 < jaccard < 1:
        return MODE_PARTIAL
    raise ValueError(f"Unsupported pair classification: name_match={name_match}, jaccard={jaccard}")


def same_paper_version_reason(paper_1: object, paper_2: object) -> str:
    pair = frozenset({normalize_text(paper_1), normalize_text(paper_2)})
    return SAME_PAPER_VERSION_EXCLUSIONS.get(pair, "")


def build_diff_pairs() -> pd.DataFrame:
    df = pd.read_csv(DIFF_REVIEW_PATH, sep="\t")
    df = df.loc[df["jaccard"].round(6) == 1.0].copy()
    df["paper_title_1"] = df["paper_1_title"].map(normalize_text)
    df["paper_title_2"] = df["paper_2_title"].map(normalize_text)
    df["paper_title_1"] = df["paper_title_1"].where(df["paper_title_1"] != "", df["manuscript_1"].map(manuscript_title))
    df["paper_title_2"] = df["paper_title_2"].where(df["paper_title_2"] != "", df["manuscript_2"].map(manuscript_title))
    df["name_match"] = "Different labels"
    df["marker_overlap"] = "Exact marker match (J=1)"
    df["mode"] = MODE_DIFF
    df["reviewed_result"] = df["skos_relation_from_1_to_2"].map(DIFF_JUDGMENT_MAP)
    df["labels"] = df["cell_type_1"].map(normalize_text) + " vs " + df["cell_type_2"].map(normalize_text)
    df["shared_markers"] = df["shared_markers"].map(join_markers)
    df["unique_markers_1"] = df["unique_markers_1"].map(join_markers)
    df["unique_markers_2"] = df["unique_markers_2"].map(join_markers)
    df["markers_1"] = df["markers_1"].map(join_markers)
    df["markers_2"] = df["markers_2"].map(join_markers)
    df["context_summary_1"] = df["reviewed_context_1"].map(normalize_text)
    df["context_summary_2"] = df["reviewed_context_2"].map(normalize_text)
    df["context_snippet_1"] = df["context_1"].map(normalize_text)
    df["context_snippet_2"] = df["context_2"].map(normalize_text)
    df["review_class"] = df["skos_relation_from_1_to_2"].map(normalize_text)
    df["classification_note"] = df["skos_evidence"].map(normalize_text)
    df["interpretation_note_1"] = df["naming_difference_summary"].map(normalize_text)
    df["interpretation_note_2"] = df["marker_relationship_summary"].map(normalize_text)
    df["interpretation_note_3"] = df["contextual_covariates"].map(normalize_text)
    keep_cols = [
        "mode",
        "name_match",
        "marker_overlap",
        "reviewed_result",
        "review_confidence",
        "review_class",
        "classification_note",
        "pairwise_assessment",
        "followup_flag",
        "jaccard",
        "paper_1",
        "paper_title_1",
        "cell_type_1",
        "markers_1",
        "shared_markers",
        "unique_markers_1",
        "context_summary_1",
        "context_snippet_1",
        "manuscript_1",
        "evidence_line_1",
        "paper_2",
        "paper_title_2",
        "cell_type_2",
        "markers_2",
        "unique_markers_2",
        "context_summary_2",
        "context_snippet_2",
        "manuscript_2",
        "evidence_line_2",
        "interpretation_note_1",
        "interpretation_note_2",
        "interpretation_note_3",
        "labels",
    ]
    return df.loc[:, keep_cols]


def build_partial_pairs() -> pd.DataFrame:
    df = pd.read_csv(PARTIAL_REVIEW_PATH, sep="\t")
    df = df.loc[df["review_resolution_class"].notna()].copy()
    df["paper_title_1"] = df["manuscript_1"].map(manuscript_title)
    df["paper_title_2"] = df["manuscript_2"].map(manuscript_title)
    df["name_match"] = "Same label"
    df["marker_overlap"] = "Partial marker overlap (0<J<1)"
    df["mode"] = MODE_PARTIAL
    df["reviewed_result"] = df["review_resolution_class"].map(PARTIAL_JUDGMENT_MAP)
    df["cell_type_1"] = df["cell_type"].map(normalize_text)
    df["cell_type_2"] = df["cell_type"].map(normalize_text)
    df["paper_1"] = df["paper_key_1"].map(normalize_text)
    df["paper_2"] = df["paper_key_2"].map(normalize_text)
    df["labels"] = df["cell_type"].map(normalize_text)
    df["jaccard"] = df["top_label_neighbor_marker_jaccard"]
    df["markers_1"] = df["marker_names_1"].map(join_markers)
    df["markers_2"] = df["marker_names_2"].map(join_markers)
    df["shared_markers"] = df["shared_markers"].map(join_markers)
    df["unique_markers_1"] = df["unique_markers_1"].map(join_markers)
    df["unique_markers_2"] = df["unique_markers_2"].map(join_markers)
    df["context_summary_1"] = ""
    df["context_summary_2"] = ""
    df["context_snippet_1"] = df["context_1"].map(normalize_text)
    df["context_snippet_2"] = df["context_2"].map(normalize_text)
    df["evidence_line_1"] = pd.NA
    df["evidence_line_2"] = pd.NA
    df["review_class"] = df["review_resolution_class"].map(normalize_text)
    df["classification_note"] = ""
    df["interpretation_note_1"] = df["shared_program_summary"].map(normalize_text)
    df["interpretation_note_2"] = df["marker_difference_summary"].map(normalize_text)
    df["interpretation_note_3"] = df["context_resolution_summary"].map(normalize_text)
    keep_cols = [
        "mode",
        "name_match",
        "marker_overlap",
        "reviewed_result",
        "review_confidence",
        "review_class",
        "classification_note",
        "pairwise_assessment",
        "followup_flag",
        "jaccard",
        "paper_1",
        "paper_title_1",
        "cell_type_1",
        "markers_1",
        "shared_markers",
        "unique_markers_1",
        "context_summary_1",
        "context_snippet_1",
        "manuscript_1",
        "evidence_line_1",
        "paper_2",
        "paper_title_2",
        "cell_type_2",
        "markers_2",
        "unique_markers_2",
        "context_summary_2",
        "context_snippet_2",
        "manuscript_2",
        "evidence_line_2",
        "interpretation_note_1",
        "interpretation_note_2",
        "interpretation_note_3",
        "labels",
    ]
    return df.loc[:, keep_cols]


def build_combined_pairs() -> tuple[pd.DataFrame, pd.DataFrame]:
    diff_df = build_diff_pairs()
    partial_df = build_partial_pairs()
    combined = pd.concat([diff_df, partial_df], ignore_index=True)
    combined["excluded_pair_reason"] = [
        same_paper_version_reason(paper_1, paper_2)
        for paper_1, paper_2 in zip(combined["paper_1"], combined["paper_2"], strict=True)
    ]
    excluded = combined.loc[combined["excluded_pair_reason"] != ""].copy()
    combined = combined.loc[combined["excluded_pair_reason"] == ""].copy()
    combined = combined.drop(columns=["excluded_pair_reason"]).reset_index(drop=True)

    combined["mode"] = pd.Categorical(combined["mode"], categories=MODE_ORDER, ordered=True)
    combined["reviewed_result"] = pd.Categorical(
        combined["reviewed_result"],
        categories=RESULT_ORDER,
        ordered=True,
    )
    combined = combined.sort_values(
        ["mode", "reviewed_result", "review_confidence", "paper_1", "cell_type_1", "paper_2", "cell_type_2"],
        ascending=[True, True, True, True, True, True, True],
    ).reset_index(drop=True)
    combined["pair_id"] = [f"P{idx:02d}" for idx in range(1, len(combined) + 1)]
    combined["mode"] = combined["mode"].astype(str)
    combined["reviewed_result"] = combined["reviewed_result"].astype(str)
    excluded["mode"] = excluded["mode"].astype(str)
    excluded["reviewed_result"] = excluded["reviewed_result"].astype(str)
    return combined, excluded


def summary_table(combined: pd.DataFrame) -> pd.DataFrame:
    summary = (
        combined.groupby(["mode", "reviewed_result"], dropna=False)
        .size()
        .rename("count")
        .reset_index()
    )
    totals = combined.groupby("mode").size().rename("total").reset_index()
    summary = summary.merge(totals, on="mode", how="left")
    summary["fraction"] = summary["count"] / summary["total"]
    summary["reviewed_result"] = pd.Categorical(summary["reviewed_result"], categories=RESULT_ORDER, ordered=True)
    summary["mode"] = pd.Categorical(summary["mode"], categories=MODE_ORDER, ordered=True)
    return summary.sort_values(["mode", "reviewed_result"]).reset_index(drop=True)


def write_pairs_tsv(combined: pd.DataFrame) -> None:
    out_df = combined.copy()
    out_df["mode"] = out_df["mode"].astype(str)
    out_df["reviewed_result"] = out_df["reviewed_result"].astype(str)
    out_df.to_csv(PAIRS_OUT_PATH, sep="\t", index=False)


def write_excluded_pairs_tsv(excluded: pd.DataFrame) -> None:
    out_df = excluded.copy()
    out_df.to_csv(EXCLUDED_PAIRS_OUT_PATH, sep="\t", index=False)


def write_markdown(combined: pd.DataFrame, summary: pd.DataFrame) -> None:
    lines: list[str] = []
    lines.append("# Cross-Study Ambiguity Review")
    lines.append("")
    lines.append(
        "This document is the single review artifact backing row 3 of the cross-study analysis. "
        "It consolidates the reviewed pairs into one place and makes the classification explicit along two axes: "
        "whether the retrieved pair kept the same cell-type name, and whether the marker overlap was exact or partial."
    )
    lines.append("")
    lines.append(
        "The reviewed result answers one question for each pair: does manuscript context support using the same unqualified name for the two profiles?"
    )
    lines.append("")
    lines.append(f"- Reviewed pairs in this artifact: **{len(combined)}**")
    lines.append(f"- Modes covered: **{len(MODE_ORDER)}**")
    lines.append("")
    lines.append("## Naming Judgment Summary")
    lines.append("")
    lines.append("| Ambiguity mode | Same name supported | Context distinction | Unresolved |")
    lines.append("|---|---:|---:|---:|")
    for mode in MODE_ORDER:
        sub = summary.loc[summary["mode"] == mode]
        counts = {row.reviewed_result: int(row.count) for row in sub.itertuples(index=False)}
        total = int(sub["total"].iloc[0]) if not sub.empty else 0
        lines.append(
            f"| {escape_md(mode)} | "
            f"{counts.get('Same name supported', 0)}/{total} | "
            f"{counts.get('Context distinction', 0)}/{total} | "
            f"{counts.get('Unresolved', 0)}/{total} |"
        )
    lines.append("")
    lines.append("## Pair Index")
    lines.append("")
    lines.append("| ID | Name match | Marker overlap | Labels | J | Reviewed result | Paper 1 | Paper 2 |")
    lines.append("|---|---|---|---|---:|---|---|---|")
    for row in combined.itertuples(index=False):
        if row.name_match == "Different labels":
            label_text = f"`{escape_md(row.cell_type_1)}` vs `{escape_md(row.cell_type_2)}`"
        else:
            label_text = f"`{escape_md(row.cell_type_1)}`"
        lines.append(
            f"| {row.pair_id} | {escape_md(row.name_match)} | {escape_md(row.marker_overlap)} | "
            f"{label_text} | {row.jaccard:.2f} | {escape_md(row.reviewed_result)} | "
            f"{code_or_dash(row.paper_1)} | {code_or_dash(row.paper_2)} |"
        )
    lines.append("")

    for mode in MODE_ORDER:
        sub_df = combined.loc[combined["mode"] == mode].reset_index(drop=True)
        lines.append(f"## {mode}")
        lines.append("")
        if mode == MODE_DIFF:
            lines.append(
                "These pairs have exact marker matches (`J=1`) but different reported labels. "
                "The review asks whether the shared marker program is strong enough, in context, to support the same name."
            )
        else:
            lines.append(
                "These pairs keep the same reported label but only partially overlap in marker space (`0<J<1`). "
                "The review asks whether the marker differences are minor reporting variation or evidence for a context distinction."
            )
        lines.append("")
        for row in sub_df.itertuples(index=False):
            summary_title = (
                f"{row.pair_id}. {row.cell_type_1} ↔ {row.cell_type_2}"
                if row.name_match == "Different labels"
                else f"{row.pair_id}. {row.cell_type_1}"
            )
            lines.append("<details>")
            lines.append(
                f"<summary><strong>{escape_md(summary_title)} · J={row.jaccard:.2f}</strong> · "
                f"{escape_md(row.reviewed_result)}</summary>"
            )
            lines.append("")
            lines.append("### Classification")
            lines.append("")
            lines.append("| Field | Value |")
            lines.append("|---|---|")
            lines.append(f"| Pair ID | `{row.pair_id}` |")
            lines.append(f"| Name match at retrieval | {escape_md(row.name_match)} |")
            lines.append(f"| Marker overlap at retrieval | {escape_md(row.marker_overlap)} |")
            lines.append(f"| Jaccard | {row.jaccard:.2f} |")
            lines.append(f"| Reviewed result | {escape_md(row.reviewed_result)} |")
            lines.append(f"| Review confidence | {escape_md(row.review_confidence)} |")
            lines.append(f"| Source review class | {escape_md(row.review_class)} |")
            if normalize_text(row.classification_note):
                lines.append(f"| Classification note | {escape_md(row.classification_note)} |")
            if normalize_text(row.followup_flag):
                lines.append(f"| Follow-up flag | {escape_md(row.followup_flag)} |")
            lines.append("")
            lines.append("### Supporting Evidence")
            lines.append("")
            lines.append("| Field | Paper 1 | Paper 2 |")
            lines.append("|---|---|---|")
            lines.append(f"| Title | {escape_md(row.paper_title_1)} | {escape_md(row.paper_title_2)} |")
            lines.append(f"| Paper key | {code_or_dash(row.paper_1)} | {code_or_dash(row.paper_2)} |")
            lines.append(
                f"| Local manuscript | {manuscript_link(row.manuscript_1, row.evidence_line_1)} | "
                f"{manuscript_link(row.manuscript_2, row.evidence_line_2)} |"
            )
            lines.append(f"| Cell label | {code_or_dash(row.cell_type_1)} | {code_or_dash(row.cell_type_2)} |")
            lines.append(f"| Marker profile | {escape_md(row.markers_1)} | {escape_md(row.markers_2)} |")
            if normalize_text(row.context_summary_1) or normalize_text(row.context_summary_2):
                lines.append(
                    f"| Study context | {escape_md(row.context_summary_1)} | {escape_md(row.context_summary_2)} |"
                )
            lines.append(
                f"| Evidence snippet | {escape_md(row.context_snippet_1)} | {escape_md(row.context_snippet_2)} |"
            )
            lines.append("")
            lines.append("### Marker Decomposition")
            lines.append("")
            lines.append("| Field | Value |")
            lines.append("|---|---|")
            lines.append(f"| Shared markers | {escape_md(row.shared_markers)} |")
            lines.append(f"| Unique to Paper 1 | {escape_md(row.unique_markers_1)} |")
            lines.append(f"| Unique to Paper 2 | {escape_md(row.unique_markers_2)} |")
            lines.append("")
            lines.append("### Interpretation")
            lines.append("")
            lines.append("| Field | Value |")
            lines.append("|---|---|")
            lines.append(f"| Pairwise assessment | {escape_md(row.pairwise_assessment)} |")
            lines.append(f"| Reviewed result | {escape_md(row.reviewed_result)} |")
            if normalize_text(row.interpretation_note_1):
                label = "Naming summary" if mode == MODE_DIFF else "Shared program summary"
                lines.append(f"| {label} | {escape_md(row.interpretation_note_1)} |")
            if normalize_text(row.interpretation_note_2):
                label = "Marker relationship summary" if mode == MODE_DIFF else "Marker difference summary"
                lines.append(f"| {label} | {escape_md(row.interpretation_note_2)} |")
            if normalize_text(row.interpretation_note_3):
                label = "Context covariates" if mode == MODE_DIFF else "Context resolution summary"
                lines.append(f"| {label} | {escape_md(row.interpretation_note_3)} |")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    MARKDOWN_OUT_PATH.write_text("\n".join(lines))


def main() -> None:
    combined, excluded = build_combined_pairs()
    combined["mode_check"] = [
        classify_mode(name_match, float(jaccard))
        for name_match, jaccard in zip(combined["name_match"], combined["jaccard"], strict=True)
    ]
    if not (combined["mode"] == combined["mode_check"]).all():
        raise RuntimeError("Mode classification mismatch while building combined ambiguity review.")
    combined = combined.drop(columns=["mode_check"])

    summary = summary_table(combined)
    write_pairs_tsv(combined)
    write_excluded_pairs_tsv(excluded)
    write_markdown(combined, summary)

    print(f"Wrote {PAIRS_OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {EXCLUDED_PAIRS_OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"Wrote {MARKDOWN_OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
