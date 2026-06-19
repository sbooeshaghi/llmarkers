from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from build_marker_corpus import assign_neighborhood, build_records
from cross_study_gene_space import (
    REPO_ROOT,
    RESULTS_DIR,
    build_gene_name_map,
    build_profile_summary,
    ids_to_names,
    normalize_text,
    split_marker_text,
    standardize_marker_records,
)
from marker_label_utils import label_relation, normalize_label


CAP_MARKERS_PATH = REPO_ROOT / "data" / "cell_annotation_platform" / "markers.json"

RESOURCE_SUMMARY_PATH = RESULTS_DIR / "cap_llmarkers_resource_summary.tsv"
JOINT_DISTRIBUTION_PATH = RESULTS_DIR / "cap_llmarkers_label_marker_joint_distribution.tsv"
PAIR_SUMMARY_PATH = RESULTS_DIR / "cap_llmarkers_pair_summary.tsv"
LABEL_COHERENCE_PATH = RESULTS_DIR / "cap_llmarkers_label_coherence.tsv"
PROFILE_LIFTOVER_PATH = RESULTS_DIR / "cap_llmarkers_profile_liftover.tsv"
STUDY_METADATA_PATH = RESULTS_DIR / "cap_llmarkers_study_metadata.tsv"
NOMENCLATURE_EXAMPLES_PATH = RESULTS_DIR / "cap_llmarkers_nomenclature_examples.tsv"
EXACT_LABEL_PROJECT_SPLIT_PATH = RESULTS_DIR / "cap_llmarkers_exact_label_project_split.tsv"
REPORT_PATH = RESULTS_DIR / "cap_llmarkers_comparison_report.md"

MIN_MARKERS = 3
MIN_LABEL_PROFILES = 3
MIN_LABEL_STUDIES = 2


def jaccard(a: set[str], b: set[str]) -> tuple[int, int, float]:
    shared = len(a & b)
    union = len(a | b)
    return shared, union, shared / union if union else 0.0


def marker_relation(marker_jaccard: float) -> str:
    if marker_jaccard == 1.0:
        return "Exact"
    if marker_jaccard > 0.0:
        return "Partial"
    return "Different"


def summarize_values(values: list[float], shared_counts: list[int]) -> dict[str, object]:
    if not values:
        return {
            "n_pairs": 0,
            "mean_jaccard": np.nan,
            "median_jaccard": np.nan,
            "q25_jaccard": np.nan,
            "q75_jaccard": np.nan,
            "pct_jaccard_eq_0": np.nan,
            "pct_jaccard_gt_0": np.nan,
            "pct_jaccard_ge_0_10": np.nan,
            "pct_jaccard_ge_0_25": np.nan,
            "pct_jaccard_eq_1": np.nan,
            "mean_shared_genes": np.nan,
        }
    arr = np.asarray(values, dtype=float)
    shared_arr = np.asarray(shared_counts, dtype=float)
    return {
        "n_pairs": len(values),
        "mean_jaccard": float(arr.mean()),
        "median_jaccard": float(np.median(arr)),
        "q25_jaccard": float(np.quantile(arr, 0.25)),
        "q75_jaccard": float(np.quantile(arr, 0.75)),
        "pct_jaccard_eq_0": float((arr == 0.0).mean()),
        "pct_jaccard_gt_0": float((arr > 0.0).mean()),
        "pct_jaccard_ge_0_10": float((arr >= 0.10).mean()),
        "pct_jaccard_ge_0_25": float((arr >= 0.25).mean()),
        "pct_jaccard_eq_1": float((arr == 1.0).mean()),
        "mean_shared_genes": float(shared_arr.mean()),
    }


def format_float(value: object) -> str:
    if value is None:
        return ""
    try:
        if math.isnan(float(value)):
            return ""
    except (TypeError, ValueError):
        return str(value)
    return f"{float(value):.3f}"


def markdown_table(df: pd.DataFrame) -> str:
    string_df = df.fillna("").astype(str)
    header = "| " + " | ".join(string_df.columns) + " |"
    separator = "| " + " | ".join(["---"] * len(string_df.columns)) + " |"
    rows = ["| " + " | ".join(row) + " |" for row in string_df.itertuples(index=False, name=None)]
    return "\n".join([header, separator, *rows])


def choose_label(values: pd.Series) -> str:
    counts = Counter(normalize_text(value) for value in values if normalize_text(value))
    if not counts:
        return ""
    return counts.most_common(1)[0][0]


def flatten_list_values(values: pd.Series) -> list[str]:
    flattened: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value is None:
            continue
        items = value if isinstance(value, list) else [value]
        for item in items:
            text = normalize_text(item)
            if text and text not in seen:
                seen.add(text)
                flattened.append(text)
    return flattened


def split_semicolon_values(value: object) -> list[str]:
    if pd.isna(value):
        return []
    text = normalize_text(value)
    if not text or text.lower() == "nan":
        return []
    return split_marker_text(text.replace("; ", ";"))


def build_llmarkers_profiles() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, str]]:
    records_df = build_records()
    records_df = records_df.loc[records_df["organism"].eq("homo_sapiens")].copy()
    records_df = standardize_marker_records(records_df)
    records_df = records_df.loc[records_df["feature_id_std"].map(normalize_text).ne("")].copy()

    _profiles_df, filtered_profiles_df, _profiles, id_to_name = build_profile_summary(
        records_df,
        min_markers=MIN_MARKERS,
        feature_id_col="feature_id_std",
        feature_name_col="feature_name_std",
    )
    profiles_df = filtered_profiles_df.copy().reset_index(drop=True)
    profiles_df["resource"] = "LLMarkers"
    profiles_df["context_uid"] = [
        f"llmarkers|{row.source_corpus}|{row.paper_id}" for row in profiles_df.itertuples(index=False)
    ]
    profiles_df["study_uid"] = profiles_df["context_uid"]
    profiles_df["study_label"] = profiles_df["paper_key"]
    profiles_df["labelset"] = ""
    profiles_df["dataset_id"] = profiles_df["paper_id"]
    profiles_df["profile_uid"] = [
        f"LLMarkers|{row.context_uid}|{row.cell_type}" for row in profiles_df.itertuples(index=False)
    ]
    profiles_df["marker_set"] = profiles_df["marker_ids"].map(lambda value: set(split_marker_text(value)))
    profiles_df["normalized_cell_type"] = profiles_df["cell_type"].map(normalize_label)
    profiles_df["neighborhood"] = profiles_df["cell_type"].map(assign_neighborhood)
    return profiles_df, records_df, id_to_name


def build_cap_human_profiles() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, str]]:
    if not CAP_MARKERS_PATH.exists():
        raise FileNotFoundError(f"Missing CAP markers file: {CAP_MARKERS_PATH}")

    records_df = pd.DataFrame(json.loads(CAP_MARKERS_PATH.read_text(encoding="utf-8")))
    records_df = records_df.loc[
        records_df["organism"].eq("homo_sapiens")
        & records_df["feature_id"].map(normalize_text).str.startswith("ENSG")
    ].copy()
    records_df = standardize_marker_records(records_df)
    records_df = records_df.loc[records_df["feature_id_std"].map(normalize_text).ne("")].copy()
    id_to_name = build_gene_name_map(
        records_df,
        feature_id_col="feature_id_std",
        feature_name_col="feature_name_std",
    )

    profile_rows = []
    group_cols = [
        "_cap_dataset_id",
        "_cap_project_id",
        "_cap_dataset_name",
        "_cap_labelset_name",
        "group_name",
    ]
    for (dataset_id, project_id, dataset_name, labelset, group_name), group in records_df.groupby(
        group_cols, sort=True, dropna=False
    ):
        marker_ids = sorted({normalize_text(value) for value in group["feature_id_std"] if normalize_text(value)})
        if len(marker_ids) < MIN_MARKERS:
            continue

        cell_type = choose_label(group["group_label"])
        if not cell_type:
            cell_type = normalize_text(group_name)

        dataset_id = normalize_text(dataset_id)
        project_id = normalize_text(project_id)
        dataset_name = normalize_text(dataset_name)
        labelset = normalize_text(labelset)
        group_name = normalize_text(group_name)
        context_uid = f"cap|{dataset_id}|{labelset}"
        study_uid = f"cap|{dataset_id}"
        source_id = choose_label(group["source_id"])
        ontology_term_id = choose_label(group["_cap_ontology_term_id"])
        ontology_term = choose_label(group["_cap_ontology_term"])
        category_ontology_term_id = choose_label(group["_cap_category_ontology_term_id"])
        category_ontology_term = choose_label(group["_cap_category_ontology_term"])
        ontology_term_exists = any(value is True for value in group["_cap_ontology_term_exists"])
        rationale_dois = flatten_list_values(
            group["_cap_rationale_dois_normalized"]
            if "_cap_rationale_dois_normalized" in group
            else group["_cap_rationale_dois"]
        )

        profile_rows.append(
            {
                "resource": "CAP",
                "source_corpus": "cap",
                "paper_id": f"{dataset_id}:{labelset}",
                "paper_key": f"CAP {dataset_id} {labelset}",
                "context_uid": context_uid,
                "study_uid": study_uid,
                "study_label": dataset_name,
                "dataset_id": dataset_id,
                "project_id": project_id,
                "labelset": labelset,
                "cell_type": cell_type,
                "group_name": group_name,
                "cap_ontology_term_id": ontology_term_id,
                "cap_ontology_term": ontology_term,
                "cap_ontology_term_exists": ontology_term_exists,
                "cap_category_ontology_term_id": category_ontology_term_id,
                "cap_category_ontology_term": category_ontology_term,
                "source_id": source_id,
                "rationale_dois": "; ".join(rationale_dois),
                "n_markers": len(marker_ids),
                "marker_ids": ";".join(marker_ids),
                "marker_names": ";".join(ids_to_names(marker_ids, id_to_name)),
                "marker_set": set(marker_ids),
            }
        )

    profiles_df = pd.DataFrame(profile_rows)
    if profiles_df.empty:
        raise ValueError("No CAP human profiles were built.")
    profiles_df["profile_uid"] = [
        f"CAP|{row.context_uid}|{row.group_name}" for row in profiles_df.itertuples(index=False)
    ]
    profiles_df["normalized_cell_type"] = profiles_df["cell_type"].map(normalize_label)
    profiles_df["neighborhood"] = profiles_df["cell_type"].map(assign_neighborhood)
    return profiles_df.reset_index(drop=True), records_df, id_to_name


def profile_signature_counts(profiles_df: pd.DataFrame, group_col: str | None = None) -> pd.Series:
    signatures = profiles_df["marker_set"].map(lambda marker_set: tuple(sorted(marker_set)))
    if group_col is None:
        return signatures.map(signatures.value_counts())
    counts = (
        profiles_df.assign(_signature=signatures)
        .groupby([group_col, "_signature"], sort=False)
        .size()
        .rename("_count")
        .reset_index()
    )
    key_to_count = {
        (row[group_col], row["_signature"]): int(row["_count"]) for _, row in counts.iterrows()
    }
    return pd.Series(
        [
            key_to_count[(row[group_col], tuple(sorted(row["marker_set"])))]
            for _, row in profiles_df.iterrows()
        ],
        index=profiles_df.index,
    )


def signature_label_counts(profiles_df: pd.DataFrame) -> pd.Series:
    signature_to_labels: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for row in profiles_df.itertuples(index=False):
        signature_to_labels[tuple(sorted(row.marker_set))].add(row.normalized_cell_type)
    return profiles_df["marker_set"].map(lambda marker_set: len(signature_to_labels[tuple(sorted(marker_set))]))


def build_resource_summary(profiles_df: pd.DataFrame, records_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for resource, resource_profiles in profiles_df.groupby("resource", sort=True):
        resource_records = records_df.loc[records_df["resource"].eq(resource)] if "resource" in records_df else records_df
        local_signature_counts = profile_signature_counts(resource_profiles, "context_uid")
        global_signature_counts = profile_signature_counts(resource_profiles)
        global_signature_label_counts = signature_label_counts(resource_profiles)

        local_identifiable = local_signature_counts.eq(1)
        global_unique = global_signature_counts.eq(1)
        global_label_consistent = global_signature_label_counts.eq(1)
        local_to_global_ambiguous = local_identifiable & ~global_label_consistent

        recurrent_label_counts = resource_profiles.groupby("normalized_cell_type")["study_uid"].nunique()
        recurrent_labels = recurrent_label_counts[recurrent_label_counts.ge(2)]
        rows.append(
            {
                "resource": resource,
                "human_marker_records": len(resource_records),
                "studies": resource_profiles["study_uid"].nunique(),
                "local_contexts": resource_profiles["context_uid"].nunique(),
                "marker_profiles": len(resource_profiles),
                "reported_labels": resource_profiles["normalized_cell_type"].nunique(),
                "marker_genes": len(set().union(*resource_profiles["marker_set"])),
                "median_markers_per_profile": float(resource_profiles["n_markers"].median()),
                "mean_markers_per_profile": float(resource_profiles["n_markers"].mean()),
                "local_identifiable_profiles": int(local_identifiable.sum()),
                "local_identifiable_fraction": float(local_identifiable.mean()),
                "globally_unique_marker_set_profiles": int(global_unique.sum()),
                "globally_unique_marker_set_fraction": float(global_unique.mean()),
                "globally_label_consistent_marker_set_profiles": int(global_label_consistent.sum()),
                "globally_label_consistent_marker_set_fraction": float(global_label_consistent.mean()),
                "local_identifiable_but_globally_label_ambiguous_profiles": int(local_to_global_ambiguous.sum()),
                "local_identifiable_but_globally_label_ambiguous_fraction": float(local_to_global_ambiguous.mean()),
                "recurrent_exact_labels": len(recurrent_labels),
            }
        )
    return pd.DataFrame(rows)


def pair_bucket(row_a: object, row_b: object) -> str:
    same_context = row_a.context_uid == row_b.context_uid
    same_study = row_a.study_uid == row_b.study_uid
    relation = label_relation(row_a.normalized_cell_type, row_b.normalized_cell_type)

    if same_context and relation == "Exact":
        return "within_local_context_same_exact_label"
    if same_context:
        return "within_local_context_different_label"
    if same_study:
        return "same_study_different_labelset"
    if relation == "Exact":
        return "between_study_same_exact_label"
    if relation == "Partial":
        return "between_study_partial_label"
    return "between_study_different_label"


def build_pair_summary(profiles_df: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    for resource, resource_profiles in profiles_df.groupby("resource", sort=True):
        rows = list(resource_profiles.itertuples(index=False))
        values: dict[str, list[float]] = defaultdict(list)
        shared_counts: dict[str, list[int]] = defaultdict(list)
        for idx_a, idx_b in combinations(range(len(rows)), 2):
            shared, _union, value = jaccard(rows[idx_a].marker_set, rows[idx_b].marker_set)
            bucket = pair_bucket(rows[idx_a], rows[idx_b])
            values[bucket].append(value)
            shared_counts[bucket].append(shared)

        ordered_buckets = [
            "within_local_context_different_label",
            "within_local_context_same_exact_label",
            "same_study_different_labelset",
            "between_study_same_exact_label",
            "between_study_partial_label",
            "between_study_different_label",
        ]
        for bucket in ordered_buckets:
            summary_rows.append(
                {
                    "resource": resource,
                    "pair_category": bucket,
                    **summarize_values(values[bucket], shared_counts[bucket]),
                }
            )
    return pd.DataFrame(summary_rows)


def build_joint_distribution(profiles_df: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    for resource, resource_profiles in profiles_df.groupby("resource", sort=True):
        rows = list(resource_profiles.itertuples(index=False))
        counts: Counter[tuple[str, str]] = Counter()
        jaccards: dict[tuple[str, str], list[float]] = defaultdict(list)
        total_pairs = 0
        for idx_a, idx_b in combinations(range(len(rows)), 2):
            row_a = rows[idx_a]
            row_b = rows[idx_b]
            if row_a.study_uid == row_b.study_uid:
                continue
            _shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
            label_rel = label_relation(row_a.normalized_cell_type, row_b.normalized_cell_type)
            marker_rel = marker_relation(value)
            counts[(label_rel, marker_rel)] += 1
            jaccards[(label_rel, marker_rel)].append(value)
            total_pairs += 1

        for label_rel in ["Exact", "Partial", "Different"]:
            for marker_rel in ["Exact", "Partial", "Different"]:
                key = (label_rel, marker_rel)
                values = jaccards[key]
                summary_rows.append(
                    {
                        "resource": resource,
                        "label_relation": label_rel,
                        "marker_relation": marker_rel,
                        "n_pairs": counts[key],
                        "fraction_of_between_study_pairs": counts[key] / total_pairs if total_pairs else np.nan,
                        "mean_marker_jaccard": float(np.mean(values)) if values else np.nan,
                        "median_marker_jaccard": float(np.median(values)) if values else np.nan,
                    }
                )
    return pd.DataFrame(summary_rows)


def build_id_to_name_from_profiles(profiles_df: pd.DataFrame) -> dict[str, str]:
    id_to_name: dict[str, str] = {}
    for row in profiles_df.itertuples(index=False):
        marker_ids = split_marker_text(row.marker_ids)
        marker_names = split_marker_text(row.marker_names)
        for marker_id, marker_name in zip(marker_ids, marker_names, strict=False):
            if marker_id and marker_name and marker_id not in id_to_name:
                id_to_name[marker_id] = marker_name
    return id_to_name


def summarize_marker_names(marker_set: set[str], id_to_name: dict[str, str], limit: int = 12) -> str:
    names = [id_to_name.get(marker_id, marker_id) for marker_id in sorted(marker_set)]
    if len(names) <= limit:
        return "; ".join(names)
    return "; ".join(names[:limit]) + f"; +{len(names) - limit} more"


def add_candidate_example(
    examples: dict[tuple[str, str], list[dict[str, object]]],
    category: str,
    row_a: object,
    row_b: object,
    shared: int,
    union: int,
    value: float,
    label_rel: str,
    marker_rel: str,
    id_to_name: dict[str, str],
) -> None:
    shared_markers = row_a.marker_set & row_b.marker_set
    examples[(row_a.resource, category)].append(
        {
            "resource": row_a.resource,
            "example_category": category,
            "label_relation": label_rel,
            "marker_relation": marker_rel,
            "marker_jaccard": value,
            "shared_markers": shared,
            "union_markers": union,
            "shared_marker_names": summarize_marker_names(shared_markers, id_to_name, limit=20),
            "study_a": row_a.study_label,
            "labelset_a": row_a.labelset,
            "cell_type_a": row_a.cell_type,
            "marker_names_a": summarize_marker_names(row_a.marker_set, id_to_name),
            "study_b": row_b.study_label,
            "labelset_b": row_b.labelset,
            "cell_type_b": row_b.cell_type,
            "marker_names_b": summarize_marker_names(row_b.marker_set, id_to_name),
        }
    )


def build_nomenclature_examples(profiles_df: pd.DataFrame, max_per_category: int = 25) -> pd.DataFrame:
    id_to_name = build_id_to_name_from_profiles(profiles_df)
    examples: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    categories = {
        ("Exact", "Different"): "same_label_different_markers",
        ("Exact", "Partial"): "same_label_partial_markers",
        ("Different", "Exact"): "different_label_exact_markers",
        ("Partial", "Exact"): "partial_label_exact_markers",
        ("Different", "Partial"): "different_label_partial_markers",
    }

    for resource, resource_profiles in profiles_df.groupby("resource", sort=True):
        rows = list(resource_profiles.itertuples(index=False))
        for idx_a, idx_b in combinations(range(len(rows)), 2):
            row_a = rows[idx_a]
            row_b = rows[idx_b]
            if row_a.study_uid == row_b.study_uid:
                continue
            shared, union, value = jaccard(row_a.marker_set, row_b.marker_set)
            label_rel = label_relation(row_a.normalized_cell_type, row_b.normalized_cell_type)
            marker_rel = marker_relation(value)
            category = categories.get((label_rel, marker_rel))
            if not category:
                continue
            add_candidate_example(
                examples,
                category,
                row_a,
                row_b,
                shared,
                union,
                value,
                label_rel,
                marker_rel,
                id_to_name,
            )

    selected_rows = []
    category_order = {
        "different_label_exact_markers": 0,
        "partial_label_exact_markers": 1,
        "same_label_different_markers": 2,
        "same_label_partial_markers": 3,
        "different_label_partial_markers": 4,
    }
    for (resource, category), rows in examples.items():
        if category.endswith("partial_markers"):
            rows = sorted(rows, key=lambda row: (-float(row["marker_jaccard"]), str(row["cell_type_a"]), str(row["cell_type_b"])))
        else:
            rows = sorted(rows, key=lambda row: (str(row["cell_type_a"]), str(row["cell_type_b"]), str(row["study_a"])))
        selected_rows.extend(rows[:max_per_category])

    if not selected_rows:
        return pd.DataFrame()
    return pd.DataFrame(selected_rows).sort_values(
        ["resource", "example_category", "marker_jaccard"],
        key=lambda col: col.map(category_order) if col.name == "example_category" else col,
        ascending=[True, True, False],
    )


def project_relation(row_a: object, row_b: object) -> str:
    project_a = normalize_text(getattr(row_a, "project_id", ""))
    project_b = normalize_text(getattr(row_b, "project_id", ""))
    if project_a and project_b and project_a == project_b:
        return "same_project"
    return "different_project_or_unknown"


def build_exact_label_project_split(profiles_df: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    for resource, resource_profiles in profiles_df.groupby("resource", sort=True):
        rows = list(resource_profiles.itertuples(index=False))
        values: dict[tuple[str, str], list[float]] = defaultdict(list)
        shared_counts: dict[tuple[str, str], list[int]] = defaultdict(list)
        for idx_a, idx_b in combinations(range(len(rows)), 2):
            row_a = rows[idx_a]
            row_b = rows[idx_b]
            if row_a.study_uid == row_b.study_uid:
                continue
            if label_relation(row_a.normalized_cell_type, row_b.normalized_cell_type) != "Exact":
                continue
            shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
            split = project_relation(row_a, row_b)
            relation = marker_relation(value)
            values[(split, relation)].append(value)
            shared_counts[(split, relation)].append(shared)

        for split in ["same_project", "different_project_or_unknown"]:
            split_values = []
            split_shared = []
            for relation in ["Exact", "Partial", "Different"]:
                relation_values = values[(split, relation)]
                relation_shared = shared_counts[(split, relation)]
                summary_rows.append(
                    {
                        "resource": resource,
                        "project_relation": split,
                        "marker_relation": relation,
                        **summarize_values(relation_values, relation_shared),
                    }
                )
                split_values.extend(relation_values)
                split_shared.extend(relation_shared)
            summary_rows.append(
                {
                    "resource": resource,
                    "project_relation": split,
                    "marker_relation": "All",
                    **summarize_values(split_values, split_shared),
                }
            )
    return pd.DataFrame(summary_rows)


def build_label_coherence(profiles_df: pd.DataFrame) -> pd.DataFrame:
    summary_rows = []
    filtered = profiles_df.loc[profiles_df["normalized_cell_type"].ne("")].copy()
    for (resource, label), label_df in filtered.groupby(["resource", "normalized_cell_type"], sort=True):
        n_studies = label_df["study_uid"].nunique()
        if len(label_df) < MIN_LABEL_PROFILES or n_studies < MIN_LABEL_STUDIES:
            continue

        values = []
        shared_counts = []
        rows = list(label_df.itertuples(index=False))
        for row_a, row_b in combinations(rows, 2):
            if row_a.study_uid == row_b.study_uid:
                continue
            shared, _union, value = jaccard(row_a.marker_set, row_b.marker_set)
            values.append(value)
            shared_counts.append(shared)
        if not values:
            continue

        summary_rows.append(
            {
                "resource": resource,
                "normalized_cell_type": label,
                "n_profiles": len(label_df),
                "n_studies": n_studies,
                "example_reported_labels": "; ".join(sorted(set(label_df["cell_type"]))[:10]),
                **summarize_values(values, shared_counts),
                "underspecification_score": 1.0 - float(np.median(values)),
            }
        )
    return pd.DataFrame(summary_rows).sort_values(
        ["resource", "underspecification_score", "n_profiles"],
        ascending=[True, False, False],
    )


def build_profile_liftover(profiles_df: pd.DataFrame) -> pd.DataFrame:
    rows_out = []
    context_gene_counts: dict[str, Counter] = {}
    label_to_rows: dict[tuple[str, str], list[object]] = defaultdict(list)

    for context_uid, context_df in profiles_df.groupby("context_uid", sort=False):
        context_gene_counts[context_uid] = Counter(
            gene_id for marker_set in context_df["marker_set"] for gene_id in marker_set
        )
    for row in profiles_df.itertuples(index=False):
        if row.normalized_cell_type:
            label_to_rows[(row.resource, row.normalized_cell_type)].append(row)

    for row in profiles_df.itertuples(index=False):
        local_private = {
            gene_id
            for gene_id in row.marker_set
            if context_gene_counts[row.context_uid][gene_id] == 1
        }

        same_label_other_study_union: set[str] = set()
        same_label_other_study_profiles = 0
        for other in label_to_rows.get((row.resource, row.normalized_cell_type), []):
            if other.study_uid == row.study_uid:
                continue
            same_label_other_study_profiles += 1
            same_label_other_study_union |= other.marker_set

        rows_out.append(
            {
                "resource": row.resource,
                "study_uid": row.study_uid,
                "context_uid": row.context_uid,
                "study_label": row.study_label,
                "labelset": row.labelset,
                "cell_type": row.cell_type,
                "normalized_cell_type": row.normalized_cell_type,
                "n_markers": len(row.marker_set),
                "n_local_private_markers": len(local_private),
                "local_private_fraction": len(local_private) / len(row.marker_set) if row.marker_set else np.nan,
                "n_same_label_other_study_profiles": same_label_other_study_profiles,
                "marker_fraction_recovered_by_same_label_other_studies": (
                    len(row.marker_set & same_label_other_study_union) / len(row.marker_set)
                    if row.marker_set and same_label_other_study_profiles
                    else np.nan
                ),
                "local_private_fraction_recovered_by_same_label_other_studies": (
                    len(local_private & same_label_other_study_union) / len(local_private)
                    if local_private and same_label_other_study_profiles
                    else np.nan
                ),
            }
        )
    return pd.DataFrame(rows_out)


def build_study_metadata(profiles_df: pd.DataFrame) -> pd.DataFrame:
    rows_out = []
    for (resource, study_uid), study_df in profiles_df.groupby(["resource", "study_uid"], sort=True):
        doi_values = []
        if "rationale_dois" in study_df:
            for value in study_df["rationale_dois"]:
                doi_values.extend(split_semicolon_values(value))
        doi_values = sorted({normalize_text(value) for value in doi_values if normalize_text(value)})
        rows_out.append(
            {
                "resource": resource,
                "study_uid": study_uid,
                "study_label": choose_label(study_df["study_label"]),
                "dataset_ids": "; ".join(sorted(set(study_df["dataset_id"].map(normalize_text)))),
                "labelsets": "; ".join(sorted(set(study_df["labelset"].map(normalize_text)) - {""})),
                "local_contexts": study_df["context_uid"].nunique(),
                "marker_profiles": len(study_df),
                "reported_labels": study_df["normalized_cell_type"].nunique(),
                "marker_genes": len(set().union(*study_df["marker_set"])),
                "n_rationale_dois": len(doi_values),
                "rationale_dois": "; ".join(doi_values),
            }
        )
    return pd.DataFrame(rows_out)


def write_report(
    resource_summary_df: pd.DataFrame,
    joint_df: pd.DataFrame,
    pair_summary_df: pd.DataFrame,
    label_coherence_df: pd.DataFrame,
    profile_liftover_df: pd.DataFrame,
    study_metadata_df: pd.DataFrame,
    exact_label_project_split_df: pd.DataFrame,
) -> None:
    resource_display = resource_summary_df.copy()
    for col in resource_display.columns:
        if resource_display[col].dtype.kind == "f":
            resource_display[col] = resource_display[col].map(format_float)

    pair_display = pair_summary_df[
        [
            "resource",
            "pair_category",
            "n_pairs",
            "median_jaccard",
            "pct_jaccard_eq_0",
            "pct_jaccard_gt_0",
            "pct_jaccard_eq_1",
        ]
    ].copy()
    for col in ["median_jaccard", "pct_jaccard_eq_0", "pct_jaccard_gt_0", "pct_jaccard_eq_1"]:
        pair_display[col] = pair_display[col].map(format_float)

    joint_display = joint_df.copy()
    for col in ["fraction_of_between_study_pairs", "mean_marker_jaccard", "median_marker_jaccard"]:
        joint_display[col] = joint_display[col].map(format_float)

    label_display = (
        label_coherence_df.sort_values(["resource", "n_profiles"], ascending=[True, False])
        .groupby("resource", sort=False)
        .head(8)[
            [
                "resource",
                "normalized_cell_type",
                "n_profiles",
                "n_studies",
                "median_jaccard",
                "pct_jaccard_eq_0",
                "example_reported_labels",
            ]
        ]
        .copy()
    )
    for col in ["median_jaccard", "pct_jaccard_eq_0"]:
        label_display[col] = label_display[col].map(format_float)

    liftover_display = (
        profile_liftover_df.groupby("resource", sort=True)
        .agg(
            profiles_with_same_label_other_studies=(
                "n_same_label_other_study_profiles",
                lambda values: int((values > 0).sum()),
            ),
            median_marker_fraction_recovered=(
                "marker_fraction_recovered_by_same_label_other_studies",
                "median",
            ),
            median_local_private_fraction_recovered=(
                "local_private_fraction_recovered_by_same_label_other_studies",
                "median",
            ),
        )
        .reset_index()
    )
    for col in ["median_marker_fraction_recovered", "median_local_private_fraction_recovered"]:
        liftover_display[col] = liftover_display[col].map(format_float)

    project_split_display = exact_label_project_split_df.loc[
        exact_label_project_split_df["marker_relation"].eq("All"),
        [
            "resource",
            "project_relation",
            "n_pairs",
            "median_jaccard",
            "pct_jaccard_eq_0",
            "pct_jaccard_gt_0",
            "pct_jaccard_eq_1",
        ],
    ].copy()
    for col in ["median_jaccard", "pct_jaccard_eq_0", "pct_jaccard_gt_0", "pct_jaccard_eq_1"]:
        project_split_display[col] = project_split_display[col].map(format_float)

    lines = [
        "# CAP vs LLMarkers Human Marker Comparison",
        "",
        "This analysis compares two human marker resources using the same profile-level definitions.",
        "LLMarkers profiles are grouped by extracted paper. CAP profiles are grouped by dataset and labelset, because one dataset can carry multiple annotation schemes.",
        "Global comparisons are made across studies; CAP pairs from the same dataset are not counted as between-study pairs.",
        "",
        "Important caveat: marker absence means not reported as a marker in the resource, not absent expression.",
        "",
        "## Resource Summary",
        "",
        markdown_table(resource_display),
        "",
        "## Pairwise Marker Overlap",
        "",
        markdown_table(pair_display),
        "",
        "## Label-Marker Joint Distribution",
        "",
        markdown_table(joint_display),
        "",
        "## Same-Label Liftover",
        "",
        markdown_table(liftover_display),
        "",
        "## Exact-Label Pairs Split By Project",
        "",
        "CAP project IDs are used to separate repeated or related datasets from more independent cross-project comparisons.",
        "",
        markdown_table(project_split_display),
        "",
        "## Study DOI/Provenance Coverage",
        "",
        markdown_table(
            study_metadata_df.groupby("resource", sort=True)
            .agg(
                studies=("study_uid", "nunique"),
                studies_with_rationale_dois=("n_rationale_dois", lambda values: int((values > 0).sum())),
                total_unique_rationale_dois=(
                    "rationale_dois",
                    lambda values: len({doi for value in values for doi in split_semicolon_values(value)}),
                ),
            )
            .reset_index()
        ),
        "",
        "## Recurrent Exact Labels With Many Profiles",
        "",
        markdown_table(label_display),
        "",
        "## Interpretation",
        "",
        "The comparison asks whether a curated resource reduces the two issues measured in LLMarkers: variable naming and local-to-global marker transfer.",
        "A cleaner curated resource should have stronger same-label marker overlap across studies and fewer marker-identical pairs with different labels.",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    llmarkers_profiles_df, llmarkers_records_df, _ll_id_to_name = build_llmarkers_profiles()
    cap_profiles_df, cap_records_df, _cap_id_to_name = build_cap_human_profiles()

    profiles_df = pd.concat([llmarkers_profiles_df, cap_profiles_df], ignore_index=True, sort=False)
    records_df = pd.concat(
        [
            llmarkers_records_df.assign(resource="LLMarkers"),
            cap_records_df.assign(resource="CAP"),
        ],
        ignore_index=True,
        sort=False,
    )

    resource_summary_df = build_resource_summary(profiles_df, records_df)
    joint_df = build_joint_distribution(profiles_df)
    pair_summary_df = build_pair_summary(profiles_df)
    label_coherence_df = build_label_coherence(profiles_df)
    profile_liftover_df = build_profile_liftover(profiles_df)
    study_metadata_df = build_study_metadata(profiles_df)
    nomenclature_examples_df = build_nomenclature_examples(profiles_df)
    exact_label_project_split_df = build_exact_label_project_split(profiles_df)

    resource_summary_df.to_csv(RESOURCE_SUMMARY_PATH, sep="\t", index=False)
    joint_df.to_csv(JOINT_DISTRIBUTION_PATH, sep="\t", index=False)
    pair_summary_df.to_csv(PAIR_SUMMARY_PATH, sep="\t", index=False)
    label_coherence_df.to_csv(LABEL_COHERENCE_PATH, sep="\t", index=False)
    profile_liftover_df.to_csv(PROFILE_LIFTOVER_PATH, sep="\t", index=False)
    study_metadata_df.to_csv(STUDY_METADATA_PATH, sep="\t", index=False)
    nomenclature_examples_df.to_csv(NOMENCLATURE_EXAMPLES_PATH, sep="\t", index=False)
    exact_label_project_split_df.to_csv(EXACT_LABEL_PROJECT_SPLIT_PATH, sep="\t", index=False)
    write_report(
        resource_summary_df,
        joint_df,
        pair_summary_df,
        label_coherence_df,
        profile_liftover_df,
        study_metadata_df,
        exact_label_project_split_df,
    )

    for path in [
        RESOURCE_SUMMARY_PATH,
        JOINT_DISTRIBUTION_PATH,
        PAIR_SUMMARY_PATH,
        LABEL_COHERENCE_PATH,
        PROFILE_LIFTOVER_PATH,
        STUDY_METADATA_PATH,
        NOMENCLATURE_EXAMPLES_PATH,
        EXACT_LABEL_PROJECT_SPLIT_PATH,
        REPORT_PATH,
    ]:
        print(f"Wrote {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
