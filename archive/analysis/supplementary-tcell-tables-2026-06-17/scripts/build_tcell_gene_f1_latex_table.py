from __future__ import annotations

import math
import re
import unicodedata

import pandas as pd

from cross_study_gene_space import REPO_ROOT, RESULTS_DIR


SOURCE_PATH = RESULTS_DIR / "tcell_gene_f1_ratio_by_cluster.tsv"
TABLE_PATH = REPO_ROOT / "docs" / "paper" / "src" / "tables" / "tcell_gene_f1_ratios.tex"
MAX_GENES_PER_CLUSTER = 5
MIN_MARKER_F1 = 0.12

LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def latex_escape(value: object) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return "".join(LATEX_SPECIALS.get(char, char) for char in text)


def fmt_float(value: object) -> str:
    if value is None or pd.isna(value):
        return "--"
    return f"{float(value):.2f}"


def fmt_ratio(value: object) -> str:
    if value is None or pd.isna(value):
        return "--"
    numeric = float(value)
    if math.isinf(numeric):
        return r"$\infty$"
    if numeric >= 100:
        return r"$>$100"
    return f"{numeric:.1f}"


def select_rows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.loc[df["gene_name"].astype(str).str.len().gt(1)].copy()
    selected = []
    for component, group_df in df.groupby("component", sort=True):
        candidates = group_df.loc[group_df["marker_cluster_f1"].ge(MIN_MARKER_F1)].copy()
        if candidates.empty:
            candidates = group_df.copy()
        top_df = candidates.sort_values(
            ["marker_cluster_f1", "log2_marker_to_label_f1_ratio"],
            ascending=[False, False],
        ).head(MAX_GENES_PER_CLUSTER)
        selected.append(top_df)
    return pd.concat(selected, ignore_index=True)


def build_table(rows_df: pd.DataFrame) -> str:
    body = []
    for component, group_df in rows_df.groupby("component", sort=True):
        first = True
        for row in group_df.itertuples(index=False):
            cluster = f"C{int(component)}" if first else ""
            program = latex_escape(row.dominant_program) if first else ""
            gene = rf"\textit{{{latex_escape(row.gene_name)}}}"
            best_label = latex_escape(row.best_label_group) if pd.notna(row.best_label_group) else "--"
            body.append(
                "  "
                + " & ".join(
                    [
                        cluster,
                        program,
                        gene,
                        fmt_float(row.marker_cluster_f1),
                        fmt_float(row.best_label_f1),
                        fmt_ratio(row.marker_to_label_f1_ratio),
                        best_label,
                    ]
                )
                + r" \\"
            )
            first = False
        body.append(r"  \addlinespace[2pt]")

    return "\n".join(
        [
            r"\begin{table*}[ht!]",
            r"  \centering",
            r"  \caption{\textbf{T-cell marker-cluster gene F1 ratios}. Top genes from each T-cell marker-gene cluster, ranked by marker-cluster F1. Marker-cluster F1 measures each gene's coverage and purity within a marker-derived T-cell cluster relative to all profiles. Best label F1 is the best coverage--purity F1 for the same gene across repeated exact T-cell labels. The ratio therefore asks whether a gene is better explained by marker-gene neighborhoods than by repeated cell type labels alone.}",
            r"  \label{tab:tcell_gene_f1_ratios}%",
            r"  \claim{tab-tcell-gene-f1-ratios}{}%",
            r"  \source{analysis/build_fig5_nomenclature_weights.py}%",
            r"  \source{analysis/build_tcell_gene_f1_latex_table.py}%",
            r"  \source{analysis/results/tcell_gene_f1_ratio_by_cluster.tsv}%",
            r"  \footnotesize",
            r"  \setlength{\tabcolsep}{4pt}",
            r"  \begin{tabular}{@{}l l l r r r l@{}}",
            r"  \toprule",
            r"  Cluster & Program & Gene & Marker F1 & Label F1 & Ratio & Best repeated label \\",
            r"  \midrule",
            *body,
            r"  \bottomrule",
            r"  \end{tabular}",
            r"\end{table*}",
            "",
        ]
    )


def main() -> None:
    df = pd.read_csv(SOURCE_PATH, sep="\t")
    rows_df = select_rows(df)
    TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TABLE_PATH.write_text(build_table(rows_df), encoding="utf-8")
    print(f"Wrote {TABLE_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
