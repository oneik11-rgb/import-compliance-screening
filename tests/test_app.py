import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from app import extract_fields


def test_blank_importer_does_not_consume_product_line():
    document_text = (
        "Importer:   \r\n"
        "Product: Electric Bicycle\r\n"
        "Declared Value: 850\r\n"
        "HS Code: 8711.60\r\n"
        "Country of Origin: China\r\n"
    )

    fields = extract_fields(document_text)

    assert fields["importer"] == ""
    assert fields["product"] == "Electric Bicycle"
    assert fields["declared_value"] == "850"
    assert fields["hs_code"] == "8711.60"
    assert fields["country_of_origin"] == "China"


def test_non_numeric_declared_value_is_preserved_for_validation():
    document_text = (
        "Importer: Sample Trading Ltd\r\n"
        "Product: Electric Bicycle\r\n"
        "Declared Value: not-a-number\r\n"
        "HS Code: 8711.60\r\n"
        "Country of Origin: China\r\n"
    )

    fields = extract_fields(document_text)

    assert fields["importer"] == "Sample Trading Ltd"
    assert fields["product"] == "Electric Bicycle"
    assert fields["declared_value"] == "not-a-number"
    assert fields["hs_code"] == "8711.60"
    assert fields["country_of_origin"] == "China"