import sys

sys.path.insert(0, "src")

from rules_config import (
    BASE_RULES,
    HS_REFERENCE,
    PROHIBITED_GOODS_RULES,
    RESTRICTED_GOODS_RULES,
    RULE_CATALOG,
    get_rule_ids,
    validate_rule_configuration,
)


def test_rule_catalog_contains_exactly_15_rules():
    assert len(RULE_CATALOG) == 15
    assert validate_rule_configuration() is True


def test_rule_ids_are_unique_and_expected():
    expected_ids = {
        "DOC-001",
        "VAL-001",
        "HS-001",
        "RES-001",
        "RES-002",
        "RES-003",
        "RES-004",
        "RES-005",
        "RES-006",
        "RES-007",
        "RES-008",
        "RES-009",
        "PRO-001",
        "PRO-002",
        "PRO-003",
    }

    rule_ids = get_rule_ids()

    assert len(rule_ids) == len(set(rule_ids))
    assert set(rule_ids) == expected_ids


def test_restricted_goods_configuration_is_complete():
    assert len(RESTRICTED_GOODS_RULES) == 9

    for rule in RESTRICTED_GOODS_RULES:
        assert rule["rule_id"].startswith("RES-")
        assert rule["category"] == "restricted_goods"
        assert rule["keywords"]
        assert rule["authority"]
        assert rule["permit_required"] is True


def test_prohibited_goods_configuration_is_complete():
    assert len(PROHIBITED_GOODS_RULES) == 3

    for rule in PROHIBITED_GOODS_RULES:
        assert rule["rule_id"].startswith("PRO-")
        assert rule["category"] == "prohibited_goods"
        assert rule["keywords"]
        assert rule["authority"]


def test_base_rules_and_hs_reference_are_available():
    assert len(BASE_RULES) == 3
    assert "8711.60" in HS_REFERENCE
    assert "electric bicycle" in HS_REFERENCE["8711.60"]