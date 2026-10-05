import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from rule_engine import evaluate_rules


def test_matching_electric_bicycle_passes_hs_check():
    fields = {
        "importer": "Sample Trading Ltd",
        "product": "Electric Bicycle",
        "declared_value": "850",
        "hs_code": "8711.60",
        "country_of_origin": "China",
    }

    results = evaluate_rules(fields)

    hs_result = next(
        result for result in results
        if result["rule_id"] == "HS-001"
    )

    assert hs_result["status"] == "PASS"


def test_mismatched_product_flags_hs_check():
    fields = {
        "importer": "Sample Trading Ltd",
        "product": "Cotton T-Shirts",
        "declared_value": "850",
        "hs_code": "8711.60",
        "country_of_origin": "China",
    }

    results = evaluate_rules(fields)

    hs_result = next(
        result for result in results
        if result["rule_id"] == "HS-001"
    )

    assert hs_result["status"] == "FLAG"


def test_missing_required_field_is_flagged():
    fields = {
        "importer": "",
        "product": "Electric Bicycle",
        "declared_value": "850",
        "hs_code": "8711.60",
        "country_of_origin": "China",
    }

    results = evaluate_rules(fields)

    doc_result = next(
        result for result in results
        if result["rule_id"] == "DOC-001"
    )

    assert doc_result["status"] == "FLAG"
    assert "Importer" in doc_result["explanation"]


def test_whitespace_only_required_field_is_flagged():
    fields = {
        "importer": "   ",
        "product": "Electric Bicycle",
        "declared_value": "850",
        "hs_code": "8711.60",
        "country_of_origin": "China",
    }

    results = evaluate_rules(fields)

    doc_result = next(
        result for result in results
        if result["rule_id"] == "DOC-001"
    )

    assert doc_result["status"] == "FLAG"
    assert "Importer" in doc_result["explanation"]


def test_unknown_hs_code_requires_human_review():
    fields = {
        "importer": "Sample Trading Ltd",
        "product": "Cotton T-Shirts",
        "declared_value": "850",
        "hs_code": "6109.10",
        "country_of_origin": "China",
    }

    results = evaluate_rules(fields)

    hs_result = next(
        result for result in results
        if result["rule_id"] == "HS-001"
    )

    assert hs_result["status"] == "FLAG"
    assert "requires human review" in hs_result["explanation"]


def test_zero_declared_value_is_flagged():
    fields = {
        "importer": "Sample Trading Ltd",
        "product": "Electric Bicycle",
        "declared_value": "0",
        "hs_code": "8711.60",
        "country_of_origin": "China",
    }

    results = evaluate_rules(fields)

    value_result = next(
        result for result in results
        if result["rule_id"] == "VAL-001"
    )

    assert value_result["status"] == "FLAG"
    assert "greater than zero" in value_result["explanation"]


def test_non_numeric_declared_value_is_flagged():
    fields = {
        "importer": "Sample Trading Ltd",
        "product": "Electric Bicycle",
        "declared_value": "not-a-number",
        "hs_code": "8711.60",
        "country_of_origin": "China",
    }

    results = evaluate_rules(fields)

    value_result = next(
        result for result in results
        if result["rule_id"] == "VAL-001"
    )

    assert value_result["status"] == "FLAG"
    assert "valid number" in value_result["explanation"]