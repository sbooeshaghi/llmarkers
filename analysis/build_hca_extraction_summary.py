from __future__ import annotations

from pathlib import Path
import json

import matplotlib.pyplot as plt
import pandas as pd


ANALYSIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = ANALYSIS_DIR.parent
HCA_DIR = REPO_ROOT / "data" / "hca"
MANUSCRIPT_DIR = HCA_DIR / "manuscripts"
MANIFEST_PATH = HCA_DIR / "manuscripts_manifest.tsv"
RESULTS_DIR = ANALYSIS_DIR / "results"
FIGURES_DIR = ANALYSIS_DIR / "figures"


def dataframe_to_markdown(df: pd.DataFrame) -> str:
    header = "| " + " | ".join(str(col) for col in df.columns) + " |"
    divider = "| " + " | ".join("---" for _ in df.columns) + " |"
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in df.itertuples(index=False, name=None)
    ]
    return "\n".join([header, divider, *rows])


def load_manifest() -> pd.DataFrame:
    manifest = pd.read_csv(MANIFEST_PATH, sep="\t").fillna("")
    manifest["folder"] = manifest["folder"].astype(str)
    return manifest


def classify_paper_status(manuscript_exists: bool, metrics_exists: bool, markers: list[dict] | None) -> str:
    if not manuscript_exists:
        return "no_markdown"
    if markers is not None and len(markers) > 0:
        return "nonempty"
    if markers is not None and len(markers) == 0:
        return "empty_json"
    if metrics_exists:
        return "zero_no_markers"
    return "unprocessed"


def build_tables() -> tuple[pd.DataFrame, pd.DataFrame]:
    manifest = load_manifest()

    paper_rows = []
    record_rows = []

    for row in manifest.itertuples(index=False):
        folder = str(row.folder)
        paper_dir = MANUSCRIPT_DIR / folder
        manuscript_path = paper_dir / "manuscript.md"
        metrics_path = paper_dir / "metrics.json"
        markers_path = paper_dir / "markers.json"

        manuscript_exists = manuscript_path.exists()
        metrics_exists = metrics_path.exists()
        markers = None
        metrics = {}

        if metrics_exists:
            metrics = json.loads(metrics_path.read_text())
        if markers_path.exists():
            markers = json.loads(markers_path.read_text())
            if not isinstance(markers, list):
                raise ValueError(f"{markers_path} did not contain a JSON array")

        status = classify_paper_status(
            manuscript_exists=manuscript_exists,
            metrics_exists=metrics_exists,
            markers=markers,
        )

        paper_data = markers if isinstance(markers, list) else []
        n_records = len(paper_data)
        unique_pairs = len(
            {
                (
                    str(rec.get("organism") or ""),
                    str(rec.get("group_name") or ""),
                    str(rec.get("feature_name") or ""),
                )
                for rec in paper_data
            }
        )
        unique_cell_types = len({str(rec.get("group_name") or "") for rec in paper_data})
        unique_genes = len({str(rec.get("feature_name") or "") for rec in paper_data})
        unique_gene_ids = len(
            {str(rec.get("feature_id")) for rec in paper_data if rec.get("feature_id")}
        )
        rationale_lengths = [
            len(str(rec.get("source_rationale") or ""))
            for rec in paper_data
            if rec.get("source_rationale")
        ]
        human_records = sum(
            1 for rec in paper_data if (rec.get("organism") or "").strip().lower() == "homo_sapiens"
        )
        nonhuman_records = sum(
            1
            for rec in paper_data
            if rec.get("organism") and (rec.get("organism") or "").strip().lower() != "homo_sapiens"
        )
        organism_counts = (
            pd.Series([(rec.get("organism") or "").strip().lower() or "missing" for rec in paper_data])
            .value_counts()
            .to_dict()
            if paper_data
            else {}
        )
        dominant_organism = max(organism_counts, key=organism_counts.get) if organism_counts else ""
        source_type_counts = (
            pd.Series([(rec.get("source_type") or "").strip().lower() or "missing" for rec in paper_data])
            .value_counts()
            .to_dict()
            if paper_data
            else {}
        )

        verification = [rec.get("_verification") or {} for rec in paper_data]
        source_rationale_frac = (
            sum(1 for v in verification if v.get("source_rationale_found")) / n_records if n_records else None
        )
        group_verified_frac = (
            sum(1 for v in verification if v.get("group_label_found")) / n_records if n_records else None
        )
        feature_verified_frac = (
            sum(1 for v in verification if v.get("feature_label_found")) / n_records if n_records else None
        )
        all_verified_frac = (
            sum(1 for v in verification if v.get("all_verified")) / n_records if n_records else None
        )
        mapped_frac = (
            sum(1 for rec in paper_data if rec.get("feature_id")) / n_records if n_records else None
        )
        human_mapped_frac = (
            sum(
                1
                for rec in paper_data
                if (rec.get("organism") or "").strip().lower() == "homo_sapiens" and rec.get("feature_id")
            )
            / human_records
            if human_records
            else None
        )
        duplicate_pair_frac = (
            1.0 - (unique_pairs / n_records)
            if n_records
            else None
        )

        paper_rows.append(
            {
                "folder": folder,
                "doi": row.doi,
                "publication_title": row.publication_title,
                "project_count": int(row.project_count) if str(row.project_count) else 0,
                "status": status,
                "manuscript_exists": manuscript_exists,
                "metrics_exists": metrics_exists,
                "markers_exists": markers is not None,
                "n_records": n_records,
                "unique_pairs": unique_pairs,
                "unique_cell_types": unique_cell_types,
                "unique_genes": unique_genes,
                "unique_gene_ids": unique_gene_ids,
                "human_records": human_records,
                "nonhuman_records": nonhuman_records,
                "human_frac": (human_records / n_records) if n_records else None,
                "nonhuman_frac": (nonhuman_records / n_records) if n_records else None,
                "dominant_organism": dominant_organism,
                "source_rationale_frac": source_rationale_frac,
                "group_verified_frac": group_verified_frac,
                "feature_verified_frac": feature_verified_frac,
                "all_verified_frac": all_verified_frac,
                "mapped_frac": mapped_frac,
                "human_mapped_frac": human_mapped_frac,
                "duplicate_pair_frac": duplicate_pair_frac,
                "median_rationale_chars": pd.Series(rationale_lengths).median() if rationale_lengths else None,
                "mean_rationale_chars": pd.Series(rationale_lengths).mean() if rationale_lengths else None,
                "source_type_counts_json": json.dumps(source_type_counts, sort_keys=True),
                "organism_counts_json": json.dumps(organism_counts, sort_keys=True),
                "total_cost": metrics.get("total_cost"),
                "processing_time_sec": metrics.get("processing_time_sec"),
                "input_tokens": metrics.get("input_tokens"),
                "output_tokens": metrics.get("output_tokens"),
                "total_tokens": metrics.get("total_tokens"),
            }
        )

        for rec in paper_data:
            v = rec.get("_verification") or {}
            record_rows.append(
                {
                    "folder": folder,
                    "doi": row.doi,
                    "publication_title": row.publication_title,
                    "organism": (rec.get("organism") or "").strip().lower() or "missing",
                    "group_name": rec.get("group_name"),
                    "feature_name": rec.get("feature_name"),
                    "feature_id": rec.get("feature_id"),
                    "source_type": rec.get("source_type"),
                    "source_rationale_method": v.get("source_rationale_method"),
                    "source_rationale_found": bool(v.get("source_rationale_found")),
                    "group_label_found": bool(v.get("group_label_found")),
                    "feature_label_found": bool(v.get("feature_label_found")),
                    "all_verified": bool(v.get("all_verified")),
                    "rationale_chars": len(str(rec.get("source_rationale") or "")),
                }
            )

    paper_df = pd.DataFrame(paper_rows).sort_values("folder").reset_index(drop=True)
    record_df = pd.DataFrame(record_rows).sort_values(["folder", "group_name", "feature_name"]).reset_index(drop=True)
    return paper_df, record_df


def build_headline_metrics(paper_df: pd.DataFrame, record_df: pd.DataFrame) -> dict[str, float | int]:
    processed = paper_df[paper_df["status"].isin(["nonempty", "empty_json", "zero_no_markers"])]
    nonempty = paper_df[paper_df["status"] == "nonempty"]
    empty = paper_df[paper_df["status"].isin(["empty_json", "zero_no_markers"])]
    human_records = record_df[record_df["organism"] == "homo_sapiens"]
    nonhuman_records = record_df[record_df["organism"] != "homo_sapiens"]

    return {
        "manifest_papers": int(len(paper_df)),
        "markdown_papers": int((paper_df["manuscript_exists"]).sum()),
        "processed_papers": int(len(processed)),
        "no_markdown_papers": int((paper_df["status"] == "no_markdown").sum()),
        "nonempty_papers": int(len(nonempty)),
        "empty_papers": int(len(empty)),
        "empty_json_papers": int((paper_df["status"] == "empty_json").sum()),
        "zero_no_markers_papers": int((paper_df["status"] == "zero_no_markers").sum()),
        "total_records": int(len(record_df)),
        "human_records": int(len(human_records)),
        "nonhuman_records": int(len(nonhuman_records)),
        "unique_paper_pairs": int(nonempty["unique_pairs"].sum()),
        "unique_gene_ids": int(record_df["feature_id"].dropna().nunique()),
        "unique_gene_names": int(record_df["feature_name"].dropna().nunique()),
        "unique_cell_type_names": int(record_df["group_name"].dropna().nunique()),
        "source_rationale_frac": float(record_df["source_rationale_found"].mean()) if len(record_df) else 0.0,
        "group_verified_frac": float(record_df["group_label_found"].mean()) if len(record_df) else 0.0,
        "feature_verified_frac": float(record_df["feature_label_found"].mean()) if len(record_df) else 0.0,
        "all_verified_frac": float(record_df["all_verified"].mean()) if len(record_df) else 0.0,
        "mapped_frac_all": float(record_df["feature_id"].notna().mean()) if len(record_df) else 0.0,
        "mapped_frac_human": float(human_records["feature_id"].notna().mean()) if len(human_records) else 0.0,
        "papers_with_nonhuman": int((nonempty["nonhuman_records"] > 0).sum()),
        "papers_with_nonhuman_ge_25pct": int((nonempty["nonhuman_frac"] >= 0.25).sum()),
        "median_records_per_nonempty_paper": float(nonempty["n_records"].median()) if len(nonempty) else 0.0,
        "median_all_verified_frac": float(nonempty["all_verified_frac"].median()) if len(nonempty) else 0.0,
        "papers_all_verified_lt_80pct": int((nonempty["all_verified_frac"] < 0.8).sum()),
        "papers_all_verified_lt_50pct": int((nonempty["all_verified_frac"] < 0.5).sum()),
        "processed_total_cost": float(processed["total_cost"].fillna(0).sum()),
        "empty_total_cost": float(empty["total_cost"].fillna(0).sum()),
        "nonempty_total_cost": float(nonempty["total_cost"].fillna(0).sum()),
        "processed_total_processing_time_sec": float(processed["processing_time_sec"].fillna(0).sum()),
        "nonempty_total_processing_time_sec": float(nonempty["processing_time_sec"].fillna(0).sum()),
    }


def build_downstream_tables(record_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    downstream_records = record_df[
        (record_df["organism"] == "homo_sapiens")
        & (record_df["feature_id"].notna())
        & (record_df["all_verified"])
    ].copy()

    downstream_records = downstream_records.sort_values(
        ["folder", "group_name", "feature_id", "feature_name"]
    ).reset_index(drop=True)

    downstream_pairs = (
        downstream_records.groupby(
            ["folder", "doi", "publication_title", "group_name", "feature_id"],
            dropna=False,
        )
        .agg(
            feature_names=("feature_name", lambda s: ";".join(sorted(pd.Series(s).dropna().astype(str).unique()))),
            n_mentions=("feature_id", "size"),
            mean_rationale_chars=("rationale_chars", "mean"),
            max_rationale_chars=("rationale_chars", "max"),
            source_types=("source_type", lambda s: ";".join(sorted(pd.Series(s).dropna().astype(str).unique()))),
        )
        .reset_index()
        .sort_values(["folder", "group_name", "feature_id"])
        .reset_index(drop=True)
    )

    return downstream_records, downstream_pairs


def add_downstream_metrics(
    metrics: dict[str, float | int],
    record_df: pd.DataFrame,
    downstream_records: pd.DataFrame,
    downstream_pairs: pd.DataFrame,
) -> dict[str, float | int]:
    updated = dict(metrics)
    updated.update(
        {
            "downstream_record_count": int(len(downstream_records)),
            "downstream_pair_count": int(len(downstream_pairs)),
            "downstream_papers": int(downstream_pairs["folder"].nunique()) if len(downstream_pairs) else 0,
            "downstream_gene_ids": int(downstream_pairs["feature_id"].nunique()) if len(downstream_pairs) else 0,
            "downstream_paper_celltypes": int(
                downstream_pairs[["folder", "group_name"]].drop_duplicates().shape[0]
            )
            if len(downstream_pairs)
            else 0,
            "downstream_fraction_of_all_records": float(len(downstream_records) / len(record_df))
            if len(record_df)
            else 0.0,
        }
    )
    return updated


def build_status_table(paper_df: pd.DataFrame) -> pd.DataFrame:
    status_df = (
        paper_df.groupby("status", dropna=False)
        .agg(
            n_papers=("folder", "size"),
            total_records=("n_records", "sum"),
            total_cost=("total_cost", lambda s: round(float(pd.Series(s).fillna(0).sum()), 4)),
        )
        .reset_index()
        .sort_values("status")
    )
    return status_df


def build_species_table(record_df: pd.DataFrame) -> pd.DataFrame:
    species_df = (
        record_df.groupby("organism", dropna=False)
        .agg(
            n_records=("organism", "size"),
            mapped_frac=("feature_id", lambda s: round(float(pd.Series(s).notna().mean()), 4)),
            all_verified_frac=("all_verified", lambda s: round(float(pd.Series(s).mean()), 4)),
        )
        .reset_index()
        .sort_values(["n_records", "organism"], ascending=[False, True])
    )
    return species_df


def build_unmapped_human_table(record_df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    unresolved = (
        record_df[
            (record_df["organism"] == "homo_sapiens")
            & (record_df["feature_id"].isna())
        ]
        .groupby("feature_name", dropna=False)
        .agg(
            n_records=("feature_name", "size"),
            n_papers=("folder", "nunique"),
        )
        .reset_index()
        .rename(columns={"feature_name": "unmapped_feature_name"})
        .sort_values(["n_records", "n_papers", "unmapped_feature_name"], ascending=[False, False, True])
        .head(top_n)
    )
    return unresolved


def build_low_quality_table(paper_df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    cols = [
        "folder",
        "doi",
        "n_records",
        "all_verified_frac",
        "group_verified_frac",
        "feature_verified_frac",
        "human_frac",
        "mapped_frac",
        "total_cost",
    ]
    low_quality = paper_df[paper_df["status"] == "nonempty"][cols].copy()
    low_quality = low_quality.sort_values(
        ["all_verified_frac", "human_frac", "n_records"],
        ascending=[True, True, False],
    ).head(top_n)
    return low_quality


def build_nonhuman_table(paper_df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    cols = [
        "folder",
        "doi",
        "n_records",
        "human_records",
        "nonhuman_records",
        "human_frac",
        "nonhuman_frac",
        "all_verified_frac",
    ]
    nonhuman = paper_df[
        (paper_df["status"] == "nonempty") & (paper_df["nonhuman_records"] > 0)
    ][cols].copy()
    nonhuman = nonhuman.sort_values(
        ["nonhuman_frac", "n_records"],
        ascending=[False, False],
    ).head(top_n)
    return nonhuman


def write_tables(
    paper_df: pd.DataFrame,
    record_df: pd.DataFrame,
    downstream_records: pd.DataFrame,
    downstream_pairs: pd.DataFrame,
    status_df: pd.DataFrame,
    species_df: pd.DataFrame,
    unresolved_df: pd.DataFrame,
    low_quality_df: pd.DataFrame,
    nonhuman_df: pd.DataFrame,
) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    paper_df.to_csv(RESULTS_DIR / "hca_extraction_paper_summary.tsv", sep="\t", index=False)
    record_df.to_csv(RESULTS_DIR / "hca_extraction_record_summary.tsv", sep="\t", index=False)
    downstream_records.to_csv(RESULTS_DIR / "hca_extraction_downstream_records.tsv", sep="\t", index=False)
    downstream_pairs.to_csv(RESULTS_DIR / "hca_extraction_downstream_pairs.tsv", sep="\t", index=False)
    status_df.to_csv(RESULTS_DIR / "hca_extraction_status_summary.tsv", sep="\t", index=False)
    species_df.to_csv(RESULTS_DIR / "hca_extraction_species_summary.tsv", sep="\t", index=False)
    unresolved_df.to_csv(RESULTS_DIR / "hca_extraction_top_unmapped_human.tsv", sep="\t", index=False)
    low_quality_df.to_csv(RESULTS_DIR / "hca_extraction_low_verification_papers.tsv", sep="\t", index=False)
    nonhuman_df.to_csv(RESULTS_DIR / "hca_extraction_nonhuman_papers.tsv", sep="\t", index=False)
    paper_df[paper_df["status"] != "nonempty"].to_csv(
        RESULTS_DIR / "hca_extraction_empty_or_missing_papers.tsv",
        sep="\t",
        index=False,
    )


def make_figure(
    paper_df: pd.DataFrame,
    unresolved_df: pd.DataFrame,
) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    nonempty = paper_df[paper_df["status"] == "nonempty"].copy()
    if nonempty.empty:
        return

    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)

    ax = axes[0, 0]
    ax.hist(nonempty["n_records"], bins=30, edgecolor="black", color="#cccccc")
    ax.set_title("Markers Per Paper")
    ax.set_xlabel("Extracted marker records")
    ax.set_ylabel("Number of papers")

    ax = axes[0, 1]
    ax.hist(nonempty["all_verified_frac"], bins=20, range=(0, 1), edgecolor="black", color="#cccccc")
    ax.axvline(nonempty["all_verified_frac"].median(), color="red", linestyle="--", linewidth=1.5)
    ax.set_title("Per-Paper Full Verification Rate")
    ax.set_xlabel("Fraction all_verified")
    ax.set_ylabel("Number of papers")

    ax = axes[1, 0]
    scatter = ax.scatter(
        nonempty["n_records"],
        nonempty["all_verified_frac"],
        c=nonempty["human_frac"],
        cmap="viridis",
        s=36,
        edgecolor="black",
        linewidth=0.25,
        alpha=0.9,
    )
    ax.set_xscale("log")
    ax.set_ylim(-0.02, 1.02)
    ax.set_title("Verification vs Marker Count")
    ax.set_xlabel("Extracted marker records per paper (log scale)")
    ax.set_ylabel("Fraction all_verified")
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Human record fraction")

    ax = axes[1, 1]
    top = unresolved_df.head(12).iloc[::-1]
    ax.barh(top["unmapped_feature_name"], top["n_records"], color="#999999", edgecolor="black")
    ax.set_title("Top Unmapped Human Labels")
    ax.set_xlabel("Unmapped records")
    ax.set_ylabel("")

    png_path = FIGURES_DIR / "hca_extraction_qc.png"
    pdf_path = FIGURES_DIR / "hca_extraction_qc.pdf"
    fig.savefig(png_path, dpi=200, bbox_inches="tight")
    fig.savefig(pdf_path, bbox_inches="tight")
    plt.close(fig)


def write_report(
    metrics: dict[str, float | int],
    status_df: pd.DataFrame,
    species_df: pd.DataFrame,
    downstream_pairs: pd.DataFrame,
    low_quality_df: pd.DataFrame,
    nonhuman_df: pd.DataFrame,
    unresolved_df: pd.DataFrame,
) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = RESULTS_DIR / "hca_extraction_report.md"

    headline_lines = [
        f"- Manifest papers: {metrics['manifest_papers']}",
        f"- Papers with `manuscript.md`: {metrics['markdown_papers']}",
        f"- Processed papers: {metrics['processed_papers']}",
        f"- Nonempty extraction papers: {metrics['nonempty_papers']}",
        f"- Empty extraction papers: {metrics['empty_papers']} ({metrics['empty_json_papers']} `[]`, {metrics['zero_no_markers_papers']} with metrics but no `markers.json`)",
        f"- No-markdown papers: {metrics['no_markdown_papers']}",
        f"- Total extracted records: {metrics['total_records']}",
        f"- Human records: {metrics['human_records']}",
        f"- Nonhuman records: {metrics['nonhuman_records']}",
        f"- Source-rationale exact-match rate: {metrics['source_rationale_frac']:.4f}",
        f"- Group-label alignment rate: {metrics['group_verified_frac']:.4f}",
        f"- Feature-label alignment rate: {metrics['feature_verified_frac']:.4f}",
        f"- Fully verified rate: {metrics['all_verified_frac']:.4f}",
        f"- Gene-id mapping rate (all records): {metrics['mapped_frac_all']:.4f}",
        f"- Gene-id mapping rate (human records): {metrics['mapped_frac_human']:.4f}",
        f"- Papers with any nonhuman records: {metrics['papers_with_nonhuman']}",
        f"- Papers with at least 25% nonhuman records: {metrics['papers_with_nonhuman_ge_25pct']}",
        f"- Median records per nonempty paper: {metrics['median_records_per_nonempty_paper']:.1f}",
        f"- Median per-paper full verification rate: {metrics['median_all_verified_frac']:.4f}",
        f"- Papers with full verification < 0.80: {metrics['papers_all_verified_lt_80pct']}",
        f"- Papers with full verification < 0.50: {metrics['papers_all_verified_lt_50pct']}",
        f"- Total model cost (all processed papers): ${metrics['processed_total_cost']:.2f}",
        f"- Model cost on empty extractions: ${metrics['empty_total_cost']:.2f}",
        f"- Model cost on nonempty extractions: ${metrics['nonempty_total_cost']:.2f}",
        f"- Total processing time (all processed papers): {metrics['processed_total_processing_time_sec'] / 3600:.2f} hours",
        f"- Processing time on nonempty extractions: {metrics['nonempty_total_processing_time_sec'] / 3600:.2f} hours",
    ]

    downstream_lines = [
        "- Filter: `organism == homo_sapiens`, `feature_id` present, and `all_verified == True`",
        "- Deduplication: within paper on `(folder, group_name, feature_id)`",
        f"- Filtered records: {metrics['downstream_record_count']}",
        f"- Filtered records as a fraction of all records: {metrics['downstream_fraction_of_all_records']:.4f}",
        f"- Deduplicated downstream pairs: {metrics['downstream_pair_count']}",
        f"- Papers retained in downstream cohort: {metrics['downstream_papers']}",
        f"- Distinct Ensembl ids in downstream cohort: {metrics['downstream_gene_ids']}",
        f"- Distinct `(paper, cell type)` groups in downstream cohort: {metrics['downstream_paper_celltypes']}",
    ]

    lines = [
        "# HCA Extraction Summary",
        "",
        "This report summarizes the `mrkr` extraction run over the HCA manuscript corpus.",
        "",
        "## Headline metrics",
        "",
        *headline_lines,
        "",
        "## Status breakdown",
        "",
        dataframe_to_markdown(status_df),
        "",
        "## Species breakdown",
        "",
        dataframe_to_markdown(species_df),
        "",
        "## Downstream cohort",
        "",
        *downstream_lines,
        "",
        dataframe_to_markdown(downstream_pairs.head(20)),
        "",
        "## Lowest-verification papers",
        "",
        dataframe_to_markdown(low_quality_df),
        "",
        "## Papers with the largest nonhuman fraction",
        "",
        dataframe_to_markdown(nonhuman_df),
        "",
        "## Top unmapped human labels",
        "",
        dataframe_to_markdown(unresolved_df),
        "",
    ]

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    paper_df, record_df = build_tables()
    downstream_records, downstream_pairs = build_downstream_tables(record_df)
    metrics = build_headline_metrics(paper_df, record_df)
    metrics = add_downstream_metrics(metrics, record_df, downstream_records, downstream_pairs)
    status_df = build_status_table(paper_df)
    species_df = build_species_table(record_df)
    unresolved_df = build_unmapped_human_table(record_df)
    low_quality_df = build_low_quality_table(paper_df)
    nonhuman_df = build_nonhuman_table(paper_df)

    write_tables(
        paper_df=paper_df,
        record_df=record_df,
        downstream_records=downstream_records,
        downstream_pairs=downstream_pairs,
        status_df=status_df,
        species_df=species_df,
        unresolved_df=unresolved_df,
        low_quality_df=low_quality_df,
        nonhuman_df=nonhuman_df,
    )
    make_figure(paper_df=paper_df, unresolved_df=unresolved_df)
    write_report(
        metrics=metrics,
        status_df=status_df,
        species_df=species_df,
        downstream_pairs=downstream_pairs,
        low_quality_df=low_quality_df,
        nonhuman_df=nonhuman_df,
        unresolved_df=unresolved_df,
    )

    print("Wrote HCA extraction summary to analysis/results and analysis/figures")
    print()
    print(pd.DataFrame([metrics]).to_string(index=False))


if __name__ == "__main__":
    main()
