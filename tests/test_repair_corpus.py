from copy import deepcopy
import sys
from pathlib import Path


ANALYSIS = Path(__file__).parents[1] / "analysis"
sys.path.insert(0, str(ANALYSIS))

from repair_corpus import drop_invalid_claims, drop_mismatched_gene  # noqa: E402


def claim(claim_id: str, genes: list[tuple[str, str]]) -> dict:
    return {
        "claim_id": claim_id,
        "terms": [
            {
                "term_type": "celltype",
                "normalized_label": "T cell",
                "sub_span": "T cell",
            },
            *[
                {
                    "term_type": "gene",
                    "normalized_label": label,
                    "sub_span": span,
                }
                for label, span in genes
            ],
        ],
    }


def test_drop_invalid_claims_removes_only_reported_claims() -> None:
    document = {"claims": [claim("a", [("CD3D", "CD3D")]), claim("b", [("CD4", "CD4")])]}
    validation = {
        "errors": [
            {
                "code": "claim.span_offset",
                "path": "claims[1].span_offset",
                "message": "bad offset",
            }
        ]
    }

    actions = drop_invalid_claims(document, validation)

    assert [item["claim_id"] for item in document["claims"]] == ["a"]
    assert actions[0]["claim_id"] == "b"


def test_drop_mismatched_gene_preserves_other_genes() -> None:
    document = {"claims": [claim("a", [("CD3D", "CD3"), ("CD4", "CD4")])]}

    actions = drop_mismatched_gene(document, "CD3D", "CD3")

    genes = [
        term["normalized_label"]
        for term in document["claims"][0]["terms"]
        if term["term_type"] == "gene"
    ]
    assert genes == ["CD4"]
    assert [action["action"] for action in actions] == ["drop_gene_term"]


def test_drop_mismatched_gene_drops_empty_claim() -> None:
    document = {"claims": [claim("a", [("CD3D", "CD3")])]}
    original = deepcopy(document)

    actions = drop_mismatched_gene(document, "CD3D", "CD3")

    assert original["claims"]
    assert document["claims"] == []
    assert [action["action"] for action in actions] == [
        "drop_gene_term",
        "drop_claim",
    ]
