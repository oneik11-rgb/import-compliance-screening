import sys

import pytest

sys.path.insert(0, "src")

from rule_engine import evaluate_rules


def make_fields(
    product,
    permit_reference="",
    hs_code="9999.99",
):
    return {
        "importer": "Sample Trading Ltd",
        "product": product,
        "declared_value": "850.00",
        "hs_code": hs_code,
        "country_of_origin": "United States",
        "permit_reference": permit_reference,
    }


def get_result(results, rule_id):
    return next(
        result
        for result in results
        if result["rule_id"] == rule_id
    )


@pytest.mark.parametrize(
    "rule_id,product",
    [
        ("RES-001", "Frozen chicken meat"),
        ("RES-002", "Fresh vegetables"),
        ("RES-003", "Human ashes"),
        ("RES-004", "Prescription medication"),
        ("RES-005", "Agricultural pesticide"),
        ("RES-006", "Firearm"),
        ("RES-007", "Toy gun"),
        ("RES-008", "Camouflage jacket"),
        ("RES-009", "Motor vehicle"),
    ],
)
def test_restricted_goods_without_permit_are_flagged(
    rule_id,
    product,
):
    results = evaluate_rules(
        make_fields(product)
    )

    result = get_result(results, rule_id)

    assert result["status"] == "FLAG"
    assert "Human review is required" in result["explanation"]


@pytest.mark.parametrize(
    "rule_id,product",
    [
        ("RES-001", "Frozen chicken meat"),
        ("RES-002", "Fresh vegetables"),
        ("RES-003", "Human ashes"),
        ("RES-004", "Prescription medication"),
        ("RES-005", "Agricultural pesticide"),
        ("RES-006", "Firearm"),
        ("RES-007", "Toy gun"),
        ("RES-008", "Camouflage jacket"),
        ("RES-009", "Motor vehicle"),
    ],
)
def test_restricted_goods_with_permit_reference_pass_prototype_check(
    rule_id,
    product,
):
    results = evaluate_rules(
        make_fields(
            product,
            permit_reference="PERMIT-2026-001",
        )
    )

    result = get_result(results, rule_id)

    assert result["status"] == "PASS"
    assert "PERMIT-2026-001" in result["explanation"]
    assert "authorized human reviewer" in result["explanation"]


@pytest.mark.parametrize(
    "rule_id,product",
    [
        ("PRO-001", "Natural honey"),
        ("PRO-002", "Counterfeit coins"),
        ("PRO-003", "Obscene publication"),
    ],
)
def test_prohibited_goods_are_flagged(
    rule_id,
    product,
):
    results = evaluate_rules(
        make_fields(product)
    )

    result = get_result(results, rule_id)

    assert result["status"] == "FLAG"
    assert "Human review is required" in result["explanation"]


def test_normal_electric_bicycle_does_not_trigger_regulatory_goods_rules():
    fields = make_fields(
        "Electric Bicycle",
        hs_code="8711.60",
    )

    results = evaluate_rules(fields)

    regulatory_results = [
        result
        for result in results
        if result["rule_id"].startswith(("RES-", "PRO-"))
    ]

    assert regulatory_results == []


def test_restricted_rule_does_not_treat_permit_reference_as_live_validation():
    results = evaluate_rules(
        make_fields(
            "Agricultural pesticide",
            permit_reference="SYNTHETIC-PERMIT-001",
        )
    )

    result = get_result(results, "RES-005")

    assert result["status"] == "PASS"
    assert "must still be validated" in result["explanation"]