from __future__ import annotations

import re
import unicodedata

import pandas as pd

from build_tcell_marker_cluster_summary import normalize_label
from cross_study_gene_space import REPO_ROOT, RESULTS_DIR


SUMMARY_PATH = RESULTS_DIR / "tcell_marker_cluster_summary.tsv"
MEMBERSHIP_PATH = RESULTS_DIR / "tcell_marker_cluster_membership.tsv"
TABLE_PATH = REPO_ROOT / "docs" / "paper" / "src" / "tables" / "tcell_marker_clusters.tex"


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
    text = re.sub(r"\s+", " ", str(value)).strip()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return "".join(LATEX_SPECIALS.get(char, char) for char in text)


def unique_reported_labels(membership_df: pd.DataFrame, component: int) -> str:
    labels = sorted(
        set(membership_df.loc[membership_df["component"].eq(component), "cell_type"]),
        key=lambda label: normalize_label(label),
    )
    return "; ".join(latex_escape(label) for label in labels)


def format_fraction(value: object) -> str:
    return f"{100 * float(value):.0f}\\%"


def build_table(summary_df: pd.DataFrame, membership_df: pd.DataFrame) -> str:
    rows = []
    for row in summary_df.itertuples(index=False):
        component = int(row.component)
        rows.append(
            "  "
            + " & ".join(
                [
                    f"C{component}",
                    str(int(row.profiles)),
                    str(int(row.papers)),
                    latex_escape(row.core_marker_genes),
                    unique_reported_labels(membership_df, component),
                    (
                        f"{format_fraction(row.exact_label_fraction)} / "
                        f"{format_fraction(row.partial_label_fraction)} / "
                        f"{format_fraction(row.different_label_fraction)}"
                    ),
                ]
            )
            + r" \\ [3pt]"
        )

    return "\n".join(
        [
            r"\begin{table*}[ht!]",
            r"  \centering",
            r"  \caption{\textbf{T-cell marker-gene clusters}. Marker-derived T-cell profile clusters used in the T-cell marker-profile analysis. Profiles are paper-level cell type marker profiles, and clusters are connected components of cross-paper profiles with marker-gene Jaccard similarity $\geq 0.5$. Reported labels are shown verbatim after normalization only for sorting. Label-pair percentages summarize exact, partial, and different reported-label relations across cross-paper profile pairs within each marker-gene cluster.}",
            r"  \label{tab:tcell_marker_clusters}%",
            r"  \claim{tab-tcell-marker-clusters}{}%",
            r"  \source{analysis/build_tcell_marker_cluster_summary.py}%",
            r"  \source{analysis/results/tcell_marker_cluster_summary.tsv}%",
            r"  \source{analysis/results/tcell_marker_cluster_membership.tsv}%",
            r"  \footnotesize",
            r"  \setlength{\tabcolsep}{3pt}",
            r"  \begin{tabular}{@{}l r r p{2.7cm} p{8.0cm} r@{}}",
            r"  \toprule",
            r"  Cluster & Profiles & Papers & Core marker genes & Reported labels & Exact / Partial / Diff. \\",
            r"  \midrule",
            *rows,
            r"  \bottomrule",
            r"  \end{tabular}",
            r"\end{table*}",
            "",
        ]
    )


def main() -> None:
    summary_df = pd.read_csv(SUMMARY_PATH, sep="\t")
    membership_df = pd.read_csv(MEMBERSHIP_PATH, sep="\t")
    TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TABLE_PATH.write_text(build_table(summary_df, membership_df), encoding="utf-8")
    print(f"Wrote {TABLE_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
