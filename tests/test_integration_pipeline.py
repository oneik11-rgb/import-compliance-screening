import sys

sys.path.insert(0, "src")

from app import prepare_screening_fields
from rule_engine import evaluate_rules


def _get_result(results, rule_id):
    return next(
        result
        for result in results
        if result["rule_id"] == rule_id
    )


def test_asycuda_aligned_document_flows_into_screening_fields():
    document_text = (
        "Declaration Reference: C87-2026-001\r\n"
        "Declaration Type: IM4\r\n"
        "Customs Office Code: MBJ\r\n"
        "Importer: Sample Trading Ltd\r\n"
        "Product: Electric Bicycle\r\n"
        "Declared Value: 850.00\r\n"
        "HS Code: 8711.60\r\n"
        "Country of Origin: China\r\n"
        "Permit Reference:\r\n"
    )

    fields = prepare_screening_fields(document_text)

    assert fields["declaration_reference"] == "C87-2026-001"
    assert fields["declaration_type"] == "IM4"
    assert fields["customs_office_code"] == "MBJ"
    assert fields["importer"] == "Sample Trading Ltd"
    assert fields["product"] == "Electric Bicycle"
    assert fields["declared_value"] == "850.00"
    assert fields["hs_code"] == "8711.60"
    assert fields["country_of_origin"] == "China"
    assert fields["permit_reference"] == ""


def test_standard_document_reaches_core_rule_engine():
    document_text = (
        "Importer: Sample Trading Ltd\n"
        "Product: Electric Bicycle\n"
        "Declared Value: 850.00\n"
        "HS Code: 8711.60\n"
        "Country of Origin: China\n"
    )

    fields = prepare_screening_fields(document_text)
    results = evaluate_rules(fields)

    assert _get_result(results, "DOC-001")["status"] == "PASS"
    assert _get_result(results, "VAL-001")["status"] == "PASS"
    assert _get_result(results, "HS-001")["status"] == "PASS"


def test_restricted_goods_flow_from_document_to_regulatory_rule():
    document_text = (
        "Declaration Reference: C87-2026-002\n"
        "Declaration Type: IM4\n"
        "Customs Office Code: MBJ\n"
        "Importer: Sample Trading Ltd\n"
        "Product: Agricultural pesticide\n"
        "Declared Value: 1200.00\n"
        "HS Code: 9999.99\n"
        "Country of Origin: United States\n"
        "Permit Reference:\n"
    )

    fields = prepare_screening_fields(document_text)
    results = evaluate_rules(fields)

    restricted_result = _get_result(results, "RES-005")

    assert restricted_result["status"] == "FLAG"
    assert "Human review is required" in restricted_result["explanation"]


def test_permit_reference_flows_through_adapter_to_rule_engine():
    document_text = (
        "Declaration Reference: C87-2026-003\n"
        "Declaration Type: IM4\n"
        "Customs Office Code: MBJ\n"
        "Importer: Sample Trading Ltd\n"
        "Product: Agricultural pesticide\n"
        "Declared Value: 1200.00\n"
        "HS Code: 9999.99\n"
        "Country of Origin: United States\n"
        "Permit Reference: PCA-2026-001\n"
    )

    fields = prepare_screening_fields(document_text)
    results = evaluate_rules(fields)

    restricted_result = _get_result(results, "RES-005")

    assert restricted_result["status"] == "PASS"
    assert "PCA-2026-001" in restricted_result["explanation"]
    assert "must still be validated" in restricted_result["explanation"]


def test_prohibited_goods_flow_from_document_to_rule_engine():
    document_text = (
        "Declaration Reference: C87-2026-004\n"
        "Declaration Type: IM4\n"
        "Customs Office Code: MBJ\n"
        "Importer: Sample Trading Ltd\n"
        "Product: Natural honey\n"
        "Declared Value: 300.00\n"
        "HS Code: 9999.99\n"
        "Country of Origin: United States\n"
        "Permit Reference:\n"
    )

    fields = prepare_screening_fields(document_text)
    results = evaluate_rules(fields)

    prohibited_result = _get_result(results, "PRO-001")

    assert prohibited_result["status"] == "FLAG"
    assert "Human review is required" in prohibited_result["explanation"]