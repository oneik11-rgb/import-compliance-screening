import sys

import pytest

sys.path.insert(0, "src")

from asycuda_adapter import (
    ASYCUDA_ALIGNED_FIELDS,
    normalize_asycuda_declaration,
    to_screening_fields,
)


def test_asycuda_declaration_is_normalized():
    declaration = {
        "declaration_reference": " C87-2026-001 ",
        "declaration_type": " IM4 ",
        "customs_office_code": " MBJ ",
        "importer": " Sample Trading Ltd ",
        "product": " Electric Bicycle ",
        "declared_value": " 850.00 ",
        "hs_code": " 8711.60 ",
        "country_of_origin": " China ",
        "permit_reference": " ",
    }

    result = normalize_asycuda_declaration(declaration)

    assert result["declaration_reference"] == "C87-2026-001"
    assert result["declaration_type"] == "IM4"
    assert result["customs_office_code"] == "MBJ"
    assert result["importer"] == "Sample Trading Ltd"
    assert result["product"] == "Electric Bicycle"
    assert result["declared_value"] == "850.00"
    assert result["hs_code"] == "8711.60"
    assert result["country_of_origin"] == "China"
    assert result["permit_reference"] == ""


def test_missing_asycuda_fields_become_empty_strings():
    declaration = {
        "product": "Electric Bicycle",
        "hs_code": "8711.60",
    }

    result = normalize_asycuda_declaration(declaration)

    assert result["product"] == "Electric Bicycle"
    assert result["hs_code"] == "8711.60"
    assert result["importer"] == ""
    assert result["permit_reference"] == ""

    assert set(result.keys()) == set(ASYCUDA_ALIGNED_FIELDS)


def test_non_string_values_are_converted_to_strings():
    declaration = {
        "declared_value": 850.00,
        "declaration_reference": 12345,
    }

    result = normalize_asycuda_declaration(declaration)

    assert result["declared_value"] == "850.0"
    assert result["declaration_reference"] == "12345"


def test_to_screening_fields_preserves_all_normalized_fields():
    declaration = {
        "declaration_reference": "C87-2026-002",
        "declaration_type": "IM4",
        "customs_office_code": "MBJ",
        "importer": "Sample Trading Ltd",
        "product": "Electric Bicycle",
        "declared_value": "850.00",
        "hs_code": "8711.60",
        "country_of_origin": "China",
        "permit_reference": "PERMIT-001",
    }

    result = to_screening_fields(declaration)

    assert result == declaration


def test_adapter_rejects_non_dictionary_input():
    with pytest.raises(
        TypeError,
        match="Declaration must be supplied as a dictionary."
    ):
        normalize_asycuda_declaration("not a declaration")