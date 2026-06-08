#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Ridge
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import normalize


REPO_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = REPO_ROOT / "docs" / "llmarkers.sqlite"
RESULTS_DIR = REPO_ROOT / "analysis" / "results"
EMBED_MODEL_NAME = "sentence-transformers_all-MiniLM-L6-v2@float16"

DESCRIPTOR_STOPWORDS = {
    "CELL",
    "CELLS",
    "OTHER",
    "REPORTED",
    "TYPE",
    "TYPES",
    "LIKE",
    "SUBPOPULATION",
    "SUBPOPULATIONS",
    "POPULATION",
    "POPULATIONS",
}


TEXT_QUERIES = {
    "regulatory_t_cell": "regulatory T cell Treg FOXP3 IL2RA CTLA4 immune suppressive CD4 T cell",
    "exhausted_cd8_t_cell": "exhausted CD8 T cell checkpoint PDCD1 HAVCR2 LAG3 cytotoxic T cell",
    "classical_monocyte": "classical monocyte inflammatory CD14 LST1 S100A8 S100A9 FCN1 LYZ",
    "macrophage": "macrophage tissue resident APOE C1QA C1QB CD68 LYZ",
    "b_cell": "B cell CD79A CD79B MS4A1 antibody lymphocyte",
}

GENE_SET_QUERIES = {
    "treg_core": ["FOXP3", "IL2RA", "CTLA4"],
    "exhaustion_checkpoint": ["PDCD1", "HAVCR2", "LAG3"],
    "classical_monocyte": ["CD14", "LST1", "S100A8", "S100A9", "FCN1", "LYZ"],
    "macrophage": ["CD68", "APOE", "C1QA", "C1QB", "LYZ"],
    "b_cell": ["MS4A1", "CD79A", "CD79B"],
}


@dataclass(frozen=True)
class SplitData:
    train_idx: np.ndarray
    test_idx: np.ndarray
    gene_mask: np.ndarray
    y_train: sparse.csr_matrix
    y_test: sparse.csr_matrix


def normalize_label(text: str) -> str:
    return " ".join(str(text).upper().split())


def label_tokens(text: str) -> set[str]:
    tokens = re.findall(r"[A-Z0-9]+", normalize_label(text))
    return {
        token
        for token in tokens
        if token not in DESCRIPTOR_STOPWORDS and (len(token) >= 3 or token in {"B", "T", "NK", "DC"})
    }


def label_relation(left: str, right: str) -> str:
    left_norm = normalize_label(left)
    right_norm = normalize_label(right)
    if left_norm == right_norm:
        return "exact"
    if left_norm and right_norm and (left_norm in right_norm or right_norm in left_norm):
        return "partial"
    if label_tokens(left_norm) & label_tokens(right_norm):
        return "partial"
    return "different"


def load_profiles() -> tuple[pd.DataFrame, np.ndarray]:
    with sqlite3.connect(DB_PATH) as conn:
        profiles = pd.read_sql_query(
            """
            SELECT
                p.profile_id,
                p.paper_id,
                p.collection,
                p.organism,
                p.group_name,
                p.text_blob,
                p.paper_context_blob,
                p.gene_names_json,
                p.gene_ids_json,
                p.n_gene_ids,
                pa.doi,
                pa.title,
                pa.year,
                e.dim,
                e.text_embedding_blob
            FROM profiles AS p
            JOIN papers AS pa ON pa.paper_id = p.paper_id
            JOIN profile_embeddings_biomed AS e ON e.profile_id = p.profile_id
            WHERE e.model_name = ?
            AND p.organism = 'homo_sapiens'
            AND p.n_gene_ids >= 2
            ORDER BY p.profile_id
            """,
            conn,
            params=(EMBED_MODEL_NAME,),
        )

    if profiles.empty:
        raise RuntimeError("No eligible human profiles were found in docs/llmarkers.sqlite")

    profiles["gene_names"] = profiles["gene_names_json"].map(json.loads)
    profiles["gene_ids"] = profiles["gene_ids_json"].map(json.loads)
    text_embeddings = np.vstack(
        [np.frombuffer(blob, dtype="<f2").astype("float32") for blob in profiles["text_embedding_blob"]]
    )
    return profiles, normalize(text_embeddings)


def build_gene_matrix(profiles: pd.DataFrame) -> tuple[sparse.csr_matrix, list[str]]:
    gene_vocab = sorted({gene_id for gene_ids in profiles["gene_ids"] for gene_id in gene_ids})
    gene_index = {gene_id: i for i, gene_id in enumerate(gene_vocab)}
    rows: list[int] = []
    cols: list[int] = []
    for row_idx, gene_ids in enumerate(profiles["gene_ids"]):
        for gene_id in gene_ids:
            rows.append(row_idx)
            cols.append(gene_index[gene_id])
    matrix = sparse.csr_matrix(
        (np.ones(len(rows), dtype=np.float32), (rows, cols)),
        shape=(len(profiles), len(gene_vocab)),
    )
    return matrix, gene_vocab


def make_split(profiles: pd.DataFrame, gene_matrix: sparse.csr_matrix, split_seed: int) -> SplitData:
    splitter = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=split_seed)
    train_idx, test_idx = next(splitter.split(profiles, groups=profiles["paper_id"]))
    train_gene_counts = np.asarray(gene_matrix[train_idx].sum(axis=0)).ravel()
    gene_mask = train_gene_counts > 0
    y_all = gene_matrix[:, gene_mask].tocsr()
    test_seen_counts = np.asarray(y_all[test_idx].sum(axis=1)).ravel()
    test_idx = test_idx[test_seen_counts >= 2]
    return SplitData(
        train_idx=train_idx,
        test_idx=test_idx,
        gene_mask=gene_mask,
        y_train=y_all[train_idx].astype("float32"),
        y_test=y_all[test_idx].astype("float32"),
    )


def gene_prediction_metrics(scores: np.ndarray, y_true: sparse.csr_matrix, method: str, split_seed: int) -> dict[str, float | str | int]:
    recall_at_m: list[float] = []
    recall_at_10: list[float] = []
    precision_at_10: list[float] = []
    any_hit_at_m: list[float] = []

    for row_idx in range(y_true.shape[0]):
        true = set(y_true[row_idx].indices)
        if not true:
            continue
        n_true = len(true)
        k = min(max(n_true, 10), scores.shape[1])
        candidate = np.argpartition(scores[row_idx], -k)[-k:]
        ranked = candidate[np.argsort(scores[row_idx, candidate])]
        top_m = set(ranked[-n_true:])
        top_10 = set(ranked[-min(10, scores.shape[1]) :])
        recall_at_m.append(len(true & top_m) / n_true)
        recall_at_10.append(len(true & top_10) / n_true)
        precision_at_10.append(len(true & top_10) / min(10, scores.shape[1]))
        any_hit_at_m.append(float(bool(true & top_m)))

    return {
        "split_seed": split_seed,
        "direction": "text_to_genes",
        "method": method,
        "n_eval": len(recall_at_m),
        "mean_recall_at_true_gene_count": float(np.mean(recall_at_m)),
        "median_recall_at_true_gene_count": float(np.median(recall_at_m)),
        "mean_recall_at_10": float(np.mean(recall_at_10)),
        "mean_precision_at_10": float(np.mean(precision_at_10)),
        "any_hit_at_true_gene_count": float(np.mean(any_hit_at_m)),
    }


def marker_jaccard(left: sparse.csr_matrix, right: sparse.csr_matrix) -> np.ndarray:
    intersections = left @ right.T
    left_sizes = np.asarray(left.sum(axis=1)).ravel()
    right_sizes = np.asarray(right.sum(axis=1)).ravel()
    rows: list[np.ndarray] = []
    for row_idx in range(left.shape[0]):
        intersection = intersections.getrow(row_idx).toarray().ravel()
        denominator = left_sizes[row_idx] + right_sizes - intersection
        rows.append(np.divide(intersection, denominator, out=np.zeros_like(intersection), where=denominator > 0))
    return np.vstack(rows)


def gene_to_text_retrieval_metrics(
    similarities: np.ndarray,
    y_query: sparse.csr_matrix,
    y_candidates: sparse.csr_matrix,
    profiles: pd.DataFrame,
    query_idx: np.ndarray,
    candidate_idx: np.ndarray,
    method: str,
    split_seed: int,
) -> dict[str, float | str | int]:
    exact_top1 = 0
    partial_top1 = 0
    exact_top5 = 0
    partial_top5 = 0
    top1_jaccard: list[float] = []

    for row_idx, profile_idx in enumerate(query_idx):
        order = np.argsort(similarities[row_idx])[-5:][::-1]
        query_label = profiles.iloc[profile_idx]["group_name"]
        relations = [
            label_relation(query_label, profiles.iloc[candidate_idx[candidate_pos]]["group_name"])
            for candidate_pos in order
        ]
        exact_top1 += relations[0] == "exact"
        partial_top1 += relations[0] in {"exact", "partial"}
        exact_top5 += any(relation == "exact" for relation in relations)
        partial_top5 += any(relation in {"exact", "partial"} for relation in relations)
        query_genes = set(y_query[row_idx].indices)
        candidate_genes = set(y_candidates[order[0]].indices)
        union = query_genes | candidate_genes
        top1_jaccard.append(len(query_genes & candidate_genes) / len(union) if union else 0.0)

    n_eval = len(query_idx)
    return {
        "split_seed": split_seed,
        "direction": "genes_to_text",
        "method": method,
        "n_eval": n_eval,
        "top1_exact_label": exact_top1 / n_eval,
        "top1_exact_or_partial_label": partial_top1 / n_eval,
        "top5_exact_label": exact_top5 / n_eval,
        "top5_exact_or_partial_label": partial_top5 / n_eval,
        "mean_top1_marker_jaccard": float(np.mean(top1_jaccard)),
    }


def evaluate_split(
    profiles: pd.DataFrame,
    text_embeddings: np.ndarray,
    gene_matrix: sparse.csr_matrix,
    split_seed: int,
) -> tuple[list[dict[str, float | str | int]], SplitData]:
    split = make_split(profiles, gene_matrix, split_seed)
    train_idx = split.train_idx
    test_idx = split.test_idx
    x_train = text_embeddings[train_idx]
    x_test = text_embeddings[test_idx]

    metrics: list[dict[str, float | str | int]] = []

    minilm_model = Ridge(alpha=10.0)
    minilm_model.fit(x_train, split.y_train.toarray())
    minilm_scores = minilm_model.predict(x_test)
    metrics.append(gene_prediction_metrics(minilm_scores, split.y_test, "MiniLM text embedding + ridge", split_seed))

    vectorizer = TfidfVectorizer(
        max_features=50_000,
        lowercase=True,
        ngram_range=(1, 2),
        min_df=1,
        token_pattern=r"(?u)\b[\w+\-]+\b",
    )
    x_train_tfidf = vectorizer.fit_transform(profiles.iloc[train_idx]["text_blob"].tolist())
    x_test_tfidf = vectorizer.transform(profiles.iloc[test_idx]["text_blob"].tolist())
    tfidf_model = Ridge(alpha=1.0)
    tfidf_model.fit(x_train_tfidf, split.y_train.toarray())
    tfidf_scores = tfidf_model.predict(x_test_tfidf)
    metrics.append(gene_prediction_metrics(tfidf_scores, split.y_test, "TF-IDF text + ridge", split_seed))

    popularity_scores = np.tile(np.asarray(split.y_train.sum(axis=0)).ravel(), (split.y_test.shape[0], 1))
    metrics.append(gene_prediction_metrics(popularity_scores, split.y_test, "training gene popularity", split_seed))

    n_components = min(128, split.y_train.shape[0] - 1, split.y_train.shape[1] - 1)
    svd = TruncatedSVD(n_components=n_components, random_state=split_seed)
    gene_train_embedding = normalize(svd.fit_transform(split.y_train))
    gene_test_embedding = normalize(svd.transform(split.y_test))
    bridge = Ridge(alpha=1.0)
    bridge.fit(gene_train_embedding, x_train)
    predicted_text = normalize(bridge.predict(gene_test_embedding))
    learned_similarities = predicted_text @ x_train.T
    metrics.append(
        gene_to_text_retrieval_metrics(
            learned_similarities,
            split.y_test,
            split.y_train,
            profiles,
            test_idx,
            train_idx,
            "gene SVD + ridge to MiniLM text",
            split_seed,
        )
    )

    raw_gene_similarities = marker_jaccard(split.y_test, split.y_train)
    metrics.append(
        gene_to_text_retrieval_metrics(
            raw_gene_similarities,
            split.y_test,
            split.y_train,
            profiles,
            test_idx,
            train_idx,
            "raw marker Jaccard neighbor",
            split_seed,
        )
    )

    random = np.random.default_rng(split_seed)
    random_similarities = random.random((split.y_test.shape[0], split.y_train.shape[0]))
    metrics.append(
        gene_to_text_retrieval_metrics(
            random_similarities,
            split.y_test,
            split.y_train,
            profiles,
            test_idx,
            train_idx,
            "random train profile",
            split_seed,
        )
    )

    return metrics, split


def build_gene_name_map(profiles: pd.DataFrame) -> tuple[dict[str, str], dict[str, str]]:
    symbol_to_id_counts: dict[str, dict[str, int]] = {}
    id_to_symbol_counts: dict[str, dict[str, int]] = {}
    for _, row in profiles.iterrows():
        for symbol, gene_id in zip(row["gene_names"], row["gene_ids"]):
            symbol_key = normalize_label(symbol)
            gene_id_key = normalize_label(gene_id)
            symbol_to_id_counts.setdefault(symbol_key, {})
            symbol_to_id_counts[symbol_key][gene_id_key] = symbol_to_id_counts[symbol_key].get(gene_id_key, 0) + 1
            id_to_symbol_counts.setdefault(gene_id_key, {})
            id_to_symbol_counts[gene_id_key][symbol_key] = id_to_symbol_counts[gene_id_key].get(symbol_key, 0) + 1

    symbol_to_id = {
        symbol: sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
        for symbol, counts in symbol_to_id_counts.items()
    }
    id_to_symbol = {
        gene_id: sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
        for gene_id, counts in id_to_symbol_counts.items()
    }
    return symbol_to_id, id_to_symbol


def custom_examples(
    profiles: pd.DataFrame,
    text_embeddings: np.ndarray,
    gene_matrix: sparse.csr_matrix,
    gene_vocab: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    symbol_to_id, id_to_symbol = build_gene_name_map(profiles)

    vectorizer = TfidfVectorizer(
        max_features=50_000,
        lowercase=True,
        ngram_range=(1, 2),
        min_df=1,
        token_pattern=r"(?u)\b[\w+\-]+\b",
    )
    text_matrix = vectorizer.fit_transform(profiles["text_blob"].tolist())
    text_to_gene = Ridge(alpha=1.0)
    text_to_gene.fit(text_matrix, gene_matrix.toarray())

    text_rows: list[dict[str, str | float | int]] = []
    for query_name, query_text in TEXT_QUERIES.items():
        scores = text_to_gene.predict(vectorizer.transform([query_text]))[0]
        top = np.argsort(scores)[-15:][::-1]
        for rank, gene_pos in enumerate(top, start=1):
            gene_id = gene_vocab[gene_pos]
            text_rows.append(
                {
                    "query": query_name,
                    "rank": rank,
                    "gene_symbol": id_to_symbol.get(gene_id, gene_id),
                    "gene_id": gene_id,
                    "score": float(scores[gene_pos]),
                }
            )

    n_components = min(128, gene_matrix.shape[0] - 1, gene_matrix.shape[1] - 1)
    svd = TruncatedSVD(n_components=n_components, random_state=17)
    gene_embedding = normalize(svd.fit_transform(gene_matrix))
    bridge = Ridge(alpha=1.0)
    bridge.fit(gene_embedding, text_embeddings)

    gene_rows: list[dict[str, str | float | int]] = []
    gene_index = {gene_id: i for i, gene_id in enumerate(gene_vocab)}
    for query_name, symbols in GENE_SET_QUERIES.items():
        resolved = [symbol_to_id.get(normalize_label(symbol)) for symbol in symbols]
        resolved = [gene_id for gene_id in resolved if gene_id in gene_index]
        if not resolved:
            continue
        cols = [gene_index[gene_id] for gene_id in resolved]
        query_vector = sparse.csr_matrix(
            (np.ones(len(cols), dtype=np.float32), ([0] * len(cols), cols)),
            shape=(1, gene_matrix.shape[1]),
        )
        predicted_text = normalize(bridge.predict(normalize(svd.transform(query_vector))))
        learned_similarity = (predicted_text @ text_embeddings.T).ravel()
        marker_similarity = marker_jaccard(query_vector, gene_matrix).ravel()

        for method_name, scores in [
            ("gene SVD + ridge to MiniLM text", learned_similarity),
            ("raw marker Jaccard neighbor", marker_similarity),
        ]:
            top = np.argsort(scores)[-5:][::-1]
            for rank, profile_pos in enumerate(top, start=1):
                gene_rows.append(
                    {
                        "query": query_name,
                        "input_symbols": ", ".join(symbols),
                        "resolved_gene_ids": ", ".join(resolved),
                        "method": method_name,
                        "rank": rank,
                        "score": float(scores[profile_pos]),
                        "profile_id": int(profiles.iloc[profile_pos]["profile_id"]),
                        "label": profiles.iloc[profile_pos]["group_name"],
                        "paper_title": profiles.iloc[profile_pos]["title"],
                        "year": int(profiles.iloc[profile_pos]["year"])
                        if not pd.isna(profiles.iloc[profile_pos]["year"])
                        else "",
                        "doi": profiles.iloc[profile_pos]["doi"],
                        "profile_genes": ", ".join(profiles.iloc[profile_pos]["gene_names"][:12]),
                    }
                )

    return pd.DataFrame(text_rows), pd.DataFrame(gene_rows)


def write_report(
    profiles: pd.DataFrame,
    gene_vocab: list[str],
    metrics: pd.DataFrame,
    text_examples: pd.DataFrame,
    gene_examples: pd.DataFrame,
) -> None:
    summary = (
        metrics.drop(columns=["split_seed"])
        .groupby(["direction", "method"], dropna=False)
        .agg(["mean", "std"])
        .reset_index()
    )
    summary.columns = [
        "_".join(str(part) for part in col if part)
        if isinstance(col, tuple)
        else str(col)
        for col in summary.columns
    ]

    text_to_gene = summary[summary["direction"] == "text_to_genes"].copy()
    gene_to_text = summary[summary["direction"] == "genes_to_text"].copy()

    text_to_gene_report = text_to_gene[
        [
            "method",
            "n_eval_mean",
            "mean_recall_at_true_gene_count_mean",
            "median_recall_at_true_gene_count_mean",
            "mean_recall_at_10_mean",
            "mean_precision_at_10_mean",
            "any_hit_at_true_gene_count_mean",
        ]
    ].copy()
    text_to_gene_report.columns = [
        "method",
        "n_eval",
        "mean recall at true gene count",
        "median recall at true gene count",
        "mean recall at 10",
        "mean precision at 10",
        "any hit at true gene count",
    ]

    gene_to_text_report = gene_to_text[
        [
            "method",
            "n_eval_mean",
            "top1_exact_label_mean",
            "top1_exact_or_partial_label_mean",
            "top5_exact_label_mean",
            "top5_exact_or_partial_label_mean",
            "mean_top1_marker_jaccard_mean",
        ]
    ].copy()
    gene_to_text_report.columns = [
        "method",
        "n_eval",
        "top1 exact label",
        "top1 exact or partial label",
        "top5 exact label",
        "top5 exact or partial label",
        "mean top1 marker Jaccard",
    ]

    strongest_text = text_to_gene.sort_values("mean_recall_at_10_mean", ascending=False).iloc[0]
    learned_gene = gene_to_text[gene_to_text["method"] == "gene SVD + ridge to MiniLM text"].iloc[0]
    raw_gene = gene_to_text[gene_to_text["method"] == "raw marker Jaccard neighbor"].iloc[0]

    if (
        strongest_text["mean_recall_at_10_mean"] >= 0.35
        and learned_gene["top1_exact_or_partial_label_mean"] > raw_gene["top1_exact_or_partial_label_mean"]
        and learned_gene["mean_top1_marker_jaccard_mean"] > raw_gene["mean_top1_marker_jaccard_mean"]
    ):
        decision = "GO"
        decision_text = (
            "The learned bidirectional bridge clears the inclusion bar: text-to-gene recovery is useful and "
            "the learned gene-to-text bridge improves over raw marker-neighbor retrieval."
        )
    else:
        decision = "NO-GO"
        decision_text = (
            "The prototype is useful as an internal sanity check, but it should not be promoted as a final "
            "main result yet. Text-to-gene prediction is above baseline, especially with lexical TF-IDF, "
            "but the learned gene-to-text bridge does not beat the simpler raw marker-overlap neighbor."
        )

    def markdown_table(frame: pd.DataFrame) -> str:
        formatted = frame.copy()
        for column in formatted.columns:
            if pd.api.types.is_float_dtype(formatted[column]):
                formatted[column] = formatted[column].map(lambda value: f"{value:.4f}")
            else:
                formatted[column] = formatted[column].map(lambda value: "" if pd.isna(value) else str(value))
        columns = list(formatted.columns)
        lines = [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join(["---"] * len(columns)) + " |",
        ]
        for _, row in formatted.iterrows():
            lines.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |")
        return "\n".join(lines)

    report_path = RESULTS_DIR / "text_marker_bridge_prototype_report.md"
    with report_path.open("w", encoding="utf-8") as handle:
        handle.write("# Text-marker bridge prototype\n\n")
        handle.write("## Dataset\n\n")
        handle.write(
            f"- Human profiles with at least two mapped Ensembl genes: {len(profiles):,}\n"
            f"- Papers represented: {profiles['paper_id'].nunique():,}\n"
            f"- Ensembl gene vocabulary: {len(gene_vocab):,}\n"
            "- Evaluation split: grouped by paper ID, so held-out profiles come from held-out papers.\n\n"
        )
        handle.write("## Decision\n\n")
        handle.write(f"**{decision}.** {decision_text}\n\n")
        handle.write("## Cross-paper text-to-gene evaluation\n\n")
        handle.write(markdown_table(text_to_gene_report))
        handle.write("\n\n")
        handle.write("## Cross-paper gene-to-text evaluation\n\n")
        handle.write(markdown_table(gene_to_text_report))
        handle.write("\n\n")
        handle.write("## Text query examples\n\n")
        handle.write(
            "These examples use the strongest text-to-gene prototype, a TF-IDF text model with ridge regression "
            "to a binary Ensembl gene vector. They are qualitative face-validity checks, not held-out metrics.\n\n"
        )
        handle.write(markdown_table(text_examples[text_examples["rank"] <= 10]))
        handle.write("\n\n")
        handle.write("## Gene-set query examples\n\n")
        handle.write(
            "For each input marker set, the learned bridge is compared to direct raw marker-overlap retrieval. "
            "If the learned bridge is not better than raw marker overlap, the model is not yet adding a new final result.\n\n"
        )
        handle.write(markdown_table(gene_examples))
        handle.write("\n")

    summary.to_csv(RESULTS_DIR / "text_marker_bridge_prototype_summary.tsv", sep="\t", index=False)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    profiles, text_embeddings = load_profiles()
    gene_matrix, gene_vocab = build_gene_matrix(profiles)

    split_metrics: list[dict[str, float | str | int]] = []
    for split_seed in [11, 17, 23]:
        metrics, _ = evaluate_split(profiles, text_embeddings, gene_matrix, split_seed)
        split_metrics.extend(metrics)

    metrics_df = pd.DataFrame(split_metrics)
    metrics_df.to_csv(RESULTS_DIR / "text_marker_bridge_prototype_metrics.tsv", sep="\t", index=False)

    text_examples, gene_examples = custom_examples(profiles, text_embeddings, gene_matrix, gene_vocab)
    text_examples.to_csv(RESULTS_DIR / "text_marker_bridge_text_query_examples.tsv", sep="\t", index=False)
    gene_examples.to_csv(RESULTS_DIR / "text_marker_bridge_gene_query_examples.tsv", sep="\t", index=False)

    write_report(profiles, gene_vocab, metrics_df, text_examples, gene_examples)
    print(f"Wrote {RESULTS_DIR / 'text_marker_bridge_prototype_report.md'}")


if __name__ == "__main__":
    main()
