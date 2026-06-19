from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from build_tcell_program_summary import PROGRAMS, is_tcell_label, program_memberships
from cross_study_gene_space import build_gene_name_map, ids_to_names, normalize_text, standardize_marker_records


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "analysis" / "results"

MARKER_RECORDS_PATH = RESULTS_DIR / "cross_study_marker_records.tsv"
PAIR_PATH = RESULTS_DIR / "cross_study_candidate_profile_pairs.tsv"

FOCUS_PROGRAMS = ["resting_naive_memory", "exhaustion_inhibitory"]

FOCUS_CTP_PATHS = [
    REPO_ROOT / "archive" / "parct" / "examples" / "Szabo2019" / "szabo2019_tcells.ctp.yaml",
    REPO_ROOT / "archive" / "parct" / "examples" / "Wong2016" / "wong2016_tcells.ctp.yaml",
    REPO_ROOT / "archive" / "parct" / "examples" / "adipose_emont2022_tcells.ctp.yaml",
    REPO_ROOT / "archive" / "parct" / "examples" / "biorxiv_meca" / "03092aac_escc_tcells.ctp.yaml",
    REPO_ROOT / "archive" / "parct" / "examples" / "biorxiv_meca" / "1e500b21_brain_metastasis_cd8_tcells.ctp.yaml",
]

FOCUS_CTP_TARGETS = {
    "resting_naive_memory": {"TCF7", "CCR7", "LEF1", "SELL", "CD62L", "IL7R", "KLF2"},
    "exhaustion_inhibitory": {"PDCD1", "PD-1", "LAG3", "LAG-3", "HAVCR2", "TIM-3", "TOX", "TIGIT", "IL7R", "TCF7"},
}

PROFILE_OUT = RESULTS_DIR / "tcell_story_focus_profiles.tsv"
FAMILY_SUMMARY_OUT = RESULTS_DIR / "tcell_story_label_family_summary.tsv"
PAIR_OUT = RESULTS_DIR / "tcell_story_focus_pairs.tsv"
CTP_BRIDGE_OUT = RESULTS_DIR / "tcell_ctp_axis_bridge.tsv"
REPORT_OUT = RESULTS_DIR / "tcell_story_report.md"


def aggregate_profile_context(group: pd.DataFrame) -> str:
    snippets = []
    seen = set()
    for value in group["source_rationale"]:
        text = normalize_text(value)
        if not text or text in seen:
            continue
        seen.add(text)
        snippets.append(text)
    snippets.sort(key=len, reverse=True)
    return " ".join(snippets[:2])


def label_family(label: str) -> str:
    text = normalize_text(label).upper()
    if "TREG" in text or "REGULATORY" in text:
        return "regulatory"
    if any(term in text for term in ["EXHAUST", "TEX", "DYSFUNCTION", "PD-1", "PDCD1", "LAG3"]):
        return "exhaustion_or_inhibitory"
    if any(term in text for term in ["NAIVE", "NAÏVE", "TN", "TCM", "MEMORY", "CM"]):
        return "naive_or_memory"
    if any(term in text for term in ["ACTIVATED", "EFFECTOR", "CYTOTOX", "TRM", "TEM", "TEMRA"]):
        return "activated_or_effector"
    if any(term in text for term in ["CD4", "CD8", "T CELL", "T CELLS"]):
        return "generic_lineage"
    return "other"


def build_focus_profiles() -> pd.DataFrame:
    records_df = pd.read_csv(MARKER_RECORDS_PATH, sep="\t").fillna("")
    records_df = standardize_marker_records(records_df)
    records_df = records_df.loc[records_df["group_name"].map(is_tcell_label)].copy()
    id_to_name = build_gene_name_map(records_df)

    rows = []
    grouped = records_df.groupby(["source_corpus", "paper_id", "paper_key", "group_name"], sort=False)
    for (source_corpus, paper_id, paper_key, cell_type), group in grouped:
        marker_ids = sorted({normalize_text(value) for value in group["feature_id_std"] if normalize_text(value)})
        programs = program_memberships(marker_ids)
        focus_programs = [program for program in programs if program in FOCUS_PROGRAMS]
        if not focus_programs:
            continue
        manuscript_path = next((normalize_text(path) for path in group["manuscript_path"] if normalize_text(path)), "")
        rows.append(
            {
                "source_corpus": source_corpus,
                "paper_id": paper_id,
                "paper_key": paper_key,
                "cell_type": cell_type,
                "label_family": label_family(cell_type),
                "marker_ids": ";".join(marker_ids),
                "marker_names": ";".join(ids_to_names(marker_ids, id_to_name)),
                "focus_programs": ";".join(focus_programs),
                "context_snippet": aggregate_profile_context(group),
                "manuscript_path": manuscript_path,
            }
        )
    return pd.DataFrame(rows)


def build_family_summary(focus_profiles_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for program in FOCUS_PROGRAMS:
        sub = focus_profiles_df.loc[focus_profiles_df["focus_programs"].str.contains(program, regex=False)].copy()
        if sub.empty:
            continue
        counts = sub["label_family"].value_counts().sort_values(ascending=False)
        total = counts.sum()
        for family, count in counts.items():
            rows.append(
                {
                    "program": program,
                    "label_family": family,
                    "count": int(count),
                    "fraction": float(count / total),
                }
            )
    return pd.DataFrame(rows)


def build_focus_pairs(focus_profiles_df: pd.DataFrame) -> pd.DataFrame:
    pair_df = pd.read_csv(PAIR_PATH, sep="\t")
    rows = []
    focus_map = {
        (row.source_corpus, row.paper_id, row.cell_type): row
        for row in focus_profiles_df.itertuples(index=False)
    }
    for row in pair_df.itertuples(index=False):
        left_key = (row.source_corpus_a, row.paper_id_a, row.cell_type_a)
        right_key = (row.source_corpus_b, row.paper_id_b, row.cell_type_b)
        left = focus_map.get(left_key)
        right = focus_map.get(right_key)
        if left is None or right is None:
            continue
        if row.paper_key_a == row.paper_key_b:
            continue
        shared_programs = sorted(set(left.focus_programs.split(";")) & set(right.focus_programs.split(";")))
        if not shared_programs:
            continue
        rows.append(
            {
                "programs": ";".join(shared_programs),
                "jaccard": row.jaccard,
                "same_name": bool(row.same_name),
                "paper_key_1": row.paper_key_a,
                "cell_type_1": row.cell_type_a,
                "label_family_1": left.label_family,
                "paper_key_2": row.paper_key_b,
                "cell_type_2": row.cell_type_b,
                "label_family_2": right.label_family,
                "marker_ids_1": left.marker_ids,
                "marker_names_1": left.marker_names,
                "marker_ids_2": right.marker_ids,
                "marker_names_2": right.marker_names,
                "context_1": left.context_snippet,
                "context_2": right.context_snippet,
            }
        )
    focus_pair_df = pd.DataFrame(rows)
    if focus_pair_df.empty:
        return focus_pair_df
    return focus_pair_df.sort_values(["programs", "jaccard", "same_name"], ascending=[True, False, True]).reset_index(drop=True)


def traverse_ctp(node: dict, path_labels: list[str], out_rows: list[dict], source_path: Path) -> None:
    label = normalize_text(node.get("label"))
    next_path = [*path_labels, label] if label else list(path_labels)
    context = node.get("context") or {}
    params = context.get("params") or []
    genes = []
    evidence_texts = []
    for param in params:
        param_label = normalize_text(param.get("param_label"))
        value = normalize_text(param.get("value")).lower()
        if not param_label:
            continue
        if value in {"positive", "present", "elevated", "high"}:
            genes.append(param_label)
        evidence = param.get("evidence") or []
        for item in evidence[:1]:
            text = normalize_text(item.get("text"))
            if text:
                evidence_texts.append(text)
    out_rows.append(
        {
            "source_file": str(source_path.relative_to(REPO_ROOT)),
            "node_label": label,
            "node_path": " > ".join(next_path),
            "context_type": normalize_text(context.get("context_type")),
            "gene_labels": ";".join(sorted(set(genes))),
            "evidence_text": " ".join(evidence_texts[:2]),
        }
    )
    for child in node.get("partition") or []:
        traverse_ctp(child, next_path, out_rows, source_path)


def build_ctp_bridge() -> pd.DataFrame:
    rows = []
    for path in FOCUS_CTP_PATHS:
        if not path.exists():
            continue
        doc = yaml.safe_load(path.read_text())
        traverse_ctp(doc["root"], [], rows, path)

    ctp_df = pd.DataFrame(rows)
    bridge_rows = []
    for program in FOCUS_PROGRAMS:
        targets = {target.upper() for target in FOCUS_CTP_TARGETS[program]}
        for row in ctp_df.itertuples(index=False):
            genes = {value.strip().upper() for value in row.gene_labels.split(";") if value.strip()}
            matched = sorted(targets & genes)
            if len(matched) < 2 and program == "resting_naive_memory":
                continue
            if len(matched) < 2 and program == "exhaustion_inhibitory" and row.context_type not in {"exhaustion_state", "intratumoral_cd8_state"}:
                continue
            if program == "exhaustion_inhibitory" and row.context_type not in {"exhaustion_state", "intratumoral_cd8_state"} and not {"PDCD1", "LAG3", "HAVCR2"} & set(matched):
                continue
            bridge_rows.append(
                {
                    "program": program,
                    "source_file": row.source_file,
                    "context_type": row.context_type,
                    "node_label": row.node_label,
                    "node_path": row.node_path,
                    "matched_gene_labels": ";".join(matched),
                    "evidence_text": row.evidence_text,
                }
            )
    bridge_df = pd.DataFrame(bridge_rows)
    if bridge_df.empty:
        return bridge_df
    return bridge_df.sort_values(["program", "source_file", "node_path"]).reset_index(drop=True)


def write_report(focus_profiles_df: pd.DataFrame, family_summary_df: pd.DataFrame, focus_pair_df: pd.DataFrame, ctp_bridge_df: pd.DataFrame) -> None:
    lines = [
        "# T-cell Cross-Study Story",
        "",
        "This report summarizes the T-cell programs that remain stable after collapsing the whole corpus into standardized gene-id space.",
        "The goal is to test whether LLM-extracted marker profiles recover interpretable T-cell state programs across studies, and whether curated CTPs describe those same programs with richer local axes.",
        "",
    ]

    for program in FOCUS_PROGRAMS:
        sub = focus_profiles_df.loc[focus_profiles_df["focus_programs"].str.contains(program, regex=False)].copy()
        if sub.empty:
            continue
        program_genes = "; ".join(ids_to_names(sorted(PROGRAMS[program]), {}))
        lines.append(f"## {program}")
        lines.append("")
        lines.append(
            f"- Profiles: **{len(sub)}**"
            f"; labels: **{sub['cell_type'].nunique()}**"
            f"; papers: **{sub['paper_key'].nunique()}**"
            f"; corpora: **{sub['source_corpus'].nunique()}**"
        )
        lines.append(f"- Core gene IDs: `{'; '.join(sorted(PROGRAMS[program]))}`")
        lines.append("")

        family_sub = family_summary_df.loc[family_summary_df["program"] == program].copy()
        if not family_sub.empty:
            lines.append("### Label families")
            lines.append("")
            lines.append("| Family | Count | Fraction |")
            lines.append("|---|---:|---:|")
            for row in family_sub.itertuples(index=False):
                lines.append(f"| {row.label_family} | {row.count} | {row.fraction:.2f} |")
            lines.append("")

        lines.append("### Representative profiles")
        lines.append("")
        lines.append("| Corpus | Paper | Cell type | Family | Markers | Context |")
        lines.append("|---|---|---|---|---|---|")
        for row in sub.head(12).itertuples(index=False):
            lines.append(
                f"| {row.source_corpus} | {row.paper_key} | {row.cell_type} | {row.label_family} | {row.marker_names} | {row.context_snippet or '—'} |"
            )
        lines.append("")

        pair_sub = focus_pair_df.loc[focus_pair_df["programs"].str.contains(program, regex=False)].copy()
        if not pair_sub.empty:
            lines.append("### Top cross-study pairs")
            lines.append("")
            lines.append("| J | Paper 1 | Label 1 | Family 1 | Paper 2 | Label 2 | Family 2 |")
            lines.append("|---:|---|---|---|---|---|---|")
            for row in pair_sub.head(8).itertuples(index=False):
                lines.append(
                    f"| {row.jaccard:.2f} | {row.paper_key_1} | {row.cell_type_1} | {row.label_family_1} | {row.paper_key_2} | {row.cell_type_2} | {row.label_family_2} |"
                )
            lines.append("")

        bridge_sub = ctp_bridge_df.loc[ctp_bridge_df["program"] == program].copy()
        if not bridge_sub.empty:
            lines.append("### CTP bridge")
            lines.append("")
            lines.append("| CTP file | Context type | Node | Matched genes | Evidence |")
            lines.append("|---|---|---|---|---|")
            for row in bridge_sub.itertuples(index=False):
                lines.append(
                    f"| {row.source_file} | {row.context_type or '—'} | {row.node_path} | {row.matched_gene_labels} | {row.evidence_text or '—'} |"
                )
            lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("- The resting/naive-memory module is the clearest example of a stable transcriptional program that spans naive, memory, and even regulatory labels across studies.")
    lines.append("- The inhibitory/exhaustion module is more context-sensitive: it cleanly recovers exhausted CD8 labels, but also appears in generic CD8 and Treg labels, which means the checkpoint program still needs lineage and local study context to be interpreted correctly.")
    REPORT_OUT.write_text("\n".join(lines))


def main() -> None:
    focus_profiles_df = build_focus_profiles()
    family_summary_df = build_family_summary(focus_profiles_df)
    focus_pair_df = build_focus_pairs(focus_profiles_df)
    ctp_bridge_df = build_ctp_bridge()

    focus_profiles_df.to_csv(PROFILE_OUT, sep="\t", index=False)
    family_summary_df.to_csv(FAMILY_SUMMARY_OUT, sep="\t", index=False)
    focus_pair_df.to_csv(PAIR_OUT, sep="\t", index=False)
    ctp_bridge_df.to_csv(CTP_BRIDGE_OUT, sep="\t", index=False)
    write_report(focus_profiles_df, family_summary_df, focus_pair_df, ctp_bridge_df)

    print(f"Wrote focus profiles to {PROFILE_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote label-family summary to {FAMILY_SUMMARY_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote focus-pair summary to {PAIR_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote CTP bridge table to {CTP_BRIDGE_OUT.relative_to(REPO_ROOT)}")
    print(f"Wrote report to {REPORT_OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
