import sys
from pathlib import Path


SRC_PATH = Path(__file__).resolve().parent.parent / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


from rule_engine import evaluate_rules


def get_result(results, rule_id):
    return next(
        result
        for result in results
        if result["rule_id"] == rule_id
    )


def test_matching_electric_bicycle_passes_hs_check():
    fields = {
        "importer": "Sample Trading Ltd",
        "product": "Electric Bicycle",
        "declared_value": "850.00",
        "hs_code": "8711.60",
        "country_of_origin": "China",
    }

    results = evaluate_rules(fields)

    hs_result = get_result(results, "HS-001")

    assert hs_result["status"] == "PASS"


def test_mismatched_product_flags_hs_check():
    fields = {
        "importer": "Sample Trading Ltd",
        "product": "Cotton T-Shirts",
        "declared_value": "850.00",
        "hs_code": "8711.60",
        "country_of_origin": "China",
    }

    results = evaluate_rules(fields)

    hs_result = get_result(results, "HS-001")

    assert hs_result["status"] == "FLAG"


def test_missing_required_field_is_flagged():
    fields = {
        "importer": "Sample Trading Ltd",
        "product": "Electric Bicycle",
        "declared_value": "850.00",
        "hs_code": "8711.60",
        "country_of_origin": None,
    }

    results = evaluate_rules(fields)

    document_result = get_result(results, "DOC-001")

    assert document_result["status"] == "FLAG"
    assert "Country of Origin" in document_result["explanation"]