from __future__ import annotations

import re
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = REPO_ROOT / "analysis" / "results"


# A small explicit alias table is enough here because the primary representation is gene ID.
# These aliases are only used to stabilize display names and fix a few known noncanonical labels.
FEATURE_NAME_ALIASES = {
    "BDCA-2": "CLEC4C",
    "BDCA2": "CLEC4C",
    "BLIMP1": "PRDM1",
    "CD11C": "ITGAX",
    "CD127": "IL7R",
    "CD25": "IL2RA",
    "CD274": "CD274",
    "CD31": "PECAM1",
    "CD335": "NCR1",
    "CD56": "NCAM1",
    "CD62L": "SELL",
    "CLEC4C": "CLEC4C",
    "CTLA-4": "CTLA4",
    "HER-2": "ERBB2",
    "HER2": "ERBB2",
    "IFN-Γ": "IFNG",
    "IFNΓ": "IFNG",
    "IL 22": "IL22",
    "IL-22": "IL22",
    "IL-32": "IL32",
    "IL-7R": "IL7R",
    "IL7RA": "IL7R",
    "IL8": "CXCL8",
    "IL-8": "CXCL8",
    "KI-67": "MKI67",
    "KI67": "MKI67",
    "LAG-3": "LAG3",
    "MKI67": "MKI67",
    "MIK67": "MKI67",
    "NCAM": "NCAM1",
    "OCT3/4": "POU5F1",
    "OCT4": "POU5F1",
    "PD-1": "PDCD1",
    "PD1": "PDCD1",
    "PD-L1": "CD274",
    "PDGFR-Α": "PDGFRA",
    "PDGFR-Β": "PDGFRB",
    "PDL1": "CD274",
    "PECAM": "PECAM1",
    "PECAM 1": "PECAM1",
    "PECAM-1": "PECAM1",
    "SELP": "SELENOP",
    "SEPP1": "SELENOP",
    "SCL17A7": "SLC17A7",
    "T-BET": "TBX21",
    "TCF-1": "TCF7",
    "TCF1": "TCF7",
    "THY-1": "THY1",
    "TIM-3": "HAVCR2",
    "TIM3": "HAVCR2",
    "TROP-2": "TACSTD2",
    "TROP2": "TACSTD2",
    "VGLUT1": "SLC17A7",
}

# Only override IDs where the corpus stores a stable noncanonical mapping or where the name is
# a well-known protein alias whose intended gene is unambiguous in this context.
FEATURE_NAME_TO_CANONICAL_ID = {
    "CD25": "ENSG00000134460",   # IL2RA
    "CD127": "ENSG00000168685",  # IL7R
    "CD62L": "ENSG00000188404",  # SELL
    "CTLA-4": "ENSG00000163599", # CTLA4
    "LAG-3": "ENSG00000089692",  # LAG3
    "PD-1": "ENSG00000188389",   # PDCD1
    "PD1": "ENSG00000188389",
    "T-BET": "ENSG00000104856",  # TBX21
    "TCF-1": "ENSG00000081059",  # TCF7
    "TCF1": "ENSG00000081059",
    "TIM-3": "ENSG00000135077",  # HAVCR2
    "TIM3": "ENSG00000135077",
}

GENE_SYMBOL_RE = re.compile(r"^[A-Z0-9]+$")


def normalize_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return " ".join(str(value).split())


def normalize_gene_name(value: object) -> str:
    return normalize_text(value).upper()


def canonical_gene_symbol(value: object) -> str:
    text = normalize_gene_name(value)
    if not text:
        return ""
    return FEATURE_NAME_ALIASES.get(text, text)


def canonical_gene_id(raw_feature_id: object, raw_feature_name: object) -> str:
    raw_id = normalize_text(raw_feature_id)
    raw_name = normalize_gene_name(raw_feature_name)
    if raw_name in FEATURE_NAME_TO_CANONICAL_ID:
        return FEATURE_NAME_TO_CANONICAL_ID[raw_name]
    return raw_id


def _name_score(name: str) -> tuple[int, int, int, str]:
    symbol_like = int(bool(GENE_SYMBOL_RE.fullmatch(name)))
    clean = int(all(char not in name for char in "- /"))
    length_penalty = -len(name)
    return (symbol_like, clean, length_penalty, name)


def choose_preferred_name(names: pd.Series) -> str:
    counts: dict[str, int] = defaultdict(int)
    for value in names:
        name = canonical_gene_symbol(value)
        if name:
            counts[name] += 1
    if not counts:
        return ""
    ranked = sorted(counts.items(), key=lambda item: (item[1], *_name_score(item[0])), reverse=True)
    return ranked[0][0]


def standardize_marker_records(records_df: pd.DataFrame) -> pd.DataFrame:
    df = records_df.copy()
    df["feature_name_std"] = df["feature_name"].map(canonical_gene_symbol)
    df["feature_id_std"] = [
        canonical_gene_id(raw_id, raw_name)
        for raw_id, raw_name in zip(df["feature_id"], df["feature_name"], strict=True)
    ]

    preferred_names = (
        df.loc[df["feature_id_std"].ne("") & df["feature_name_std"].ne(""), ["feature_id_std", "feature_name_std"]]
        .groupby("feature_id_std")["feature_name_std"]
        .apply(choose_preferred_name)
        .to_dict()
    )
    df["feature_name_std"] = [
        preferred_names.get(feature_id_std, feature_name_std)
        for feature_id_std, feature_name_std in zip(df["feature_id_std"], df["feature_name_std"], strict=True)
    ]

    return df


def build_gene_name_map(records_df: pd.DataFrame, feature_id_col: str = "feature_id_std", feature_name_col: str = "feature_name_std") -> dict[str, str]:
    subset = records_df.loc[
        records_df[feature_id_col].map(normalize_text).ne("")
        & records_df[feature_name_col].map(normalize_text).ne(""),
        [feature_id_col, feature_name_col],
    ].copy()
    if subset.empty:
        return {}
    grouped = subset.groupby(feature_id_col)[feature_name_col].apply(choose_preferred_name)
    return grouped.to_dict()


def split_marker_text(value: object) -> list[str]:
    text = normalize_text(value)
    if not text:
        return []
    return [item.strip() for item in text.split(";") if item.strip()]


def ids_to_names(marker_ids: list[str], id_to_name: dict[str, str]) -> list[str]:
    names = []
    seen = set()
    for marker_id in marker_ids:
        name = id_to_name.get(marker_id, marker_id)
        if name and name not in seen:
            seen.add(name)
            names.append(name)
    return names


def build_profile_summary(
    records_df: pd.DataFrame,
    min_markers: int = 3,
    feature_id_col: str = "feature_id_std",
    feature_name_col: str = "feature_name_std",
) -> tuple[pd.DataFrame, pd.DataFrame, dict[tuple[str, str, str], set[str]], dict[str, str]]:
    id_to_name = build_gene_name_map(records_df, feature_id_col=feature_id_col, feature_name_col=feature_name_col)

    group_cols = ["source_corpus", "paper_id", "paper_key", "group_name"]
    profile_rows = []
    profiles: dict[tuple[str, str, str], set[str]] = {}

    grouped = records_df.groupby(group_cols, sort=True)
    for (source_corpus, paper_id, paper_key, cell_type), group in grouped:
        marker_ids = sorted({normalize_text(value) for value in group[feature_id_col] if normalize_text(value)})
        if not marker_ids:
            continue
        marker_names = ids_to_names(marker_ids, id_to_name)
        profile_rows.append(
            {
                "source_corpus": source_corpus,
                "paper_id": paper_id,
                "paper_key": paper_key,
                "cell_type": cell_type,
                "n_markers": len(marker_ids),
                "marker_ids": ";".join(marker_ids),
                "marker_names": ";".join(marker_names),
            }
        )
        profiles[(source_corpus, paper_id, cell_type)] = set(marker_ids)

    profiles_df = pd.DataFrame(profile_rows).sort_values(["source_corpus", "paper_id", "cell_type"]).reset_index(drop=True)
    filtered_profiles_df = profiles_df.loc[profiles_df["n_markers"] >= min_markers].copy()
    filtered_keys = [
        (row.source_corpus, row.paper_id, row.cell_type)
        for row in filtered_profiles_df.itertuples(index=False)
    ]
    filtered_profiles = {key: profiles[key] for key in filtered_keys}
    return profiles_df, filtered_profiles_df, filtered_profiles, id_to_name


def build_candidate_pairs(filtered_profiles_df: pd.DataFrame, filtered_profiles: dict[tuple[str, str, str], set[str]]) -> pd.DataFrame:
    profile_rows = list(filtered_profiles_df.itertuples(index=False))
    gene_to_indices: dict[str, list[int]] = defaultdict(list)

    for idx, row in enumerate(profile_rows):
        genes = filtered_profiles[(row.source_corpus, row.paper_id, row.cell_type)]
        for gene in genes:
            gene_to_indices[gene].append(idx)

    pair_to_shared: dict[tuple[int, int], set[str]] = defaultdict(set)
    for gene, indices in gene_to_indices.items():
        unique_indices = sorted(set(indices))
        for left, right in combinations(unique_indices, 2):
            pair_to_shared[(left, right)].add(gene)

    pair_rows = []
    for (left, right), shared_genes in pair_to_shared.items():
        row_a = profile_rows[left]
        row_b = profile_rows[right]
        genes_a = filtered_profiles[(row_a.source_corpus, row_a.paper_id, row_a.cell_type)]
        genes_b = filtered_profiles[(row_b.source_corpus, row_b.paper_id, row_b.cell_type)]
        union_n = len(genes_a | genes_b)
        shared_n = len(shared_genes)
        jaccard = shared_n / union_n if union_n else 0.0
        pair_rows.append(
            {
                "source_corpus_a": row_a.source_corpus,
                "source_corpus_b": row_b.source_corpus,
                "paper_id_a": row_a.paper_id,
                "paper_id_b": row_b.paper_id,
                "paper_key_a": row_a.paper_key,
                "paper_key_b": row_b.paper_key,
                "cell_type_a": row_a.cell_type,
                "cell_type_b": row_b.cell_type,
                "n_markers_a": row_a.n_markers,
                "n_markers_b": row_b.n_markers,
                "n_shared": shared_n,
                "n_union": union_n,
                "jaccard": jaccard,
                "same_name": row_a.cell_type == row_b.cell_type,
                "same_corpus": row_a.source_corpus == row_b.source_corpus,
                "corpus_pair": "__".join(sorted([row_a.source_corpus, row_b.source_corpus])),
            }
        )

    pair_df = pd.DataFrame(pair_rows).sort_values(["jaccard", "n_shared"], ascending=[False, False]).reset_index(drop=True)
    return pair_df


def nearest_marker_neighbors(pair_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    neighbor_a = pair_df.rename(
        columns={
            "source_corpus_a": "source_corpus",
            "paper_id_a": "paper_id",
            "paper_key_a": "paper_key",
            "cell_type_a": "cell_type",
            "source_corpus_b": "neighbor_source_corpus",
            "paper_id_b": "neighbor_paper_id",
            "paper_key_b": "neighbor_paper_key",
            "cell_type_b": "neighbor_cell_type",
        }
    )
    neighbor_b = pair_df.rename(
        columns={
            "source_corpus_b": "source_corpus",
            "paper_id_b": "paper_id",
            "paper_key_b": "paper_key",
            "cell_type_b": "cell_type",
            "source_corpus_a": "neighbor_source_corpus",
            "paper_id_a": "neighbor_paper_id",
            "paper_key_a": "neighbor_paper_key",
            "cell_type_a": "neighbor_cell_type",
        }
    )
    neighbor_cols = [
        "source_corpus",
        "paper_id",
        "paper_key",
        "cell_type",
        "neighbor_source_corpus",
        "neighbor_paper_id",
        "neighbor_paper_key",
        "neighbor_cell_type",
        "jaccard",
        "n_shared",
        "same_name",
    ]
    candidate_df = pd.concat([neighbor_a[neighbor_cols], neighbor_b[neighbor_cols]], ignore_index=True)
    candidate_df["top_jaccard"] = candidate_df.groupby(["source_corpus", "paper_id", "cell_type"])["jaccard"].transform("max")
    top_ties_df = candidate_df.loc[candidate_df["jaccard"] == candidate_df["top_jaccard"]].copy()
    nearest_df = (
        top_ties_df.groupby(["source_corpus", "paper_id", "paper_key", "cell_type"], sort=False)
        .agg(
            top_jaccard=("jaccard", "max"),
            top_neighbor_count=("jaccard", "size"),
            n_same_name_top=("same_name", "sum"),
        )
        .reset_index()
    )
    nearest_df["n_different_name_top"] = nearest_df["top_neighbor_count"] - nearest_df["n_same_name_top"]
    nearest_df["nearest_name_relation"] = np.select(
        [
            (nearest_df["n_same_name_top"] > 0) & (nearest_df["n_different_name_top"] == 0),
            (nearest_df["n_same_name_top"] == 0) & (nearest_df["n_different_name_top"] > 0),
        ],
        ["Same label", "Different label"],
        default="Mixed top tie",
    )
    summary_df = pd.DataFrame(
        [
            {
                "profiles": len(nearest_df),
                "mean_top_jaccard": float(nearest_df["top_jaccard"].mean()) if len(nearest_df) else 0.0,
                "median_top_jaccard": float(nearest_df["top_jaccard"].median()) if len(nearest_df) else 0.0,
                "q25_top_jaccard": float(nearest_df["top_jaccard"].quantile(0.25)) if len(nearest_df) else 0.0,
                "q75_top_jaccard": float(nearest_df["top_jaccard"].quantile(0.75)) if len(nearest_df) else 0.0,
                "profiles_ge_0_25": int((nearest_df["top_jaccard"] >= 0.25).sum()),
                "profiles_ge_0_50": int((nearest_df["top_jaccard"] >= 0.50).sum()),
            }
        ]
    )
    return nearest_df, summary_df


def add_marker_name_columns(pair_df: pd.DataFrame, id_to_name: dict[str, str], filtered_profiles: dict[tuple[str, str, str], set[str]]) -> pd.DataFrame:
    rows = []
    for row in pair_df.itertuples(index=False):
        genes_a = filtered_profiles[(row.source_corpus_a, row.paper_id_a, row.cell_type_a)]
        genes_b = filtered_profiles[(row.source_corpus_b, row.paper_id_b, row.cell_type_b)]
        shared = sorted(genes_a & genes_b)
        only_a = sorted(genes_a - genes_b)
        only_b = sorted(genes_b - genes_a)
        rows.append(
            {
                "shared_gene_ids": ";".join(shared),
                "only_a_gene_ids": ";".join(only_a),
                "only_b_gene_ids": ";".join(only_b),
                "shared_gene_names": ";".join(ids_to_names(shared, id_to_name)),
                "only_a_gene_names": ";".join(ids_to_names(only_a, id_to_name)),
                "only_b_gene_names": ";".join(ids_to_names(only_b, id_to_name)),
            }
        )
    return pd.concat([pair_df.reset_index(drop=True), pd.DataFrame(rows)], axis=1)

