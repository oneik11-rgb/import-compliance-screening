"""
Synthetic ASYCUDA-aligned declaration adapter.

This module does not connect to the live Jamaica Customs Agency
ASYCUDA World environment. It normalizes synthetic declaration data
into the internal field structure used by the compliance screening
prototype.
"""


ASYCUDA_ALIGNED_FIELDS = (
    "declaration_reference",
    "declaration_type",
    "customs_office_code",
    "importer",
    "product",
    "declared_value",
    "hs_code",
    "country_of_origin",
    "permit_reference",
)


def _normalize_text(value):
    """
    Convert a supplied value to a trimmed string.

    None becomes an empty string so missing values remain visible
    to the downstream validation rules.
    """
    if value is None:
        return ""

    return str(value).strip()


def normalize_asycuda_declaration(declaration):
    """
    Normalize a synthetic ASYCUDA-aligned declaration.

    Parameters
    ----------
    declaration : dict
        Synthetic declaration data supplied to the prototype.

    Returns
    -------
    dict
        Normalized declaration fields ready for the rule engine.

    Raises
    ------
    TypeError
        If declaration is not supplied as a dictionary.
    """
    if not isinstance(declaration, dict):
        raise TypeError("Declaration must be supplied as a dictionary.")

    normalized = {}

    for field in ASYCUDA_ALIGNED_FIELDS:
        normalized[field] = _normalize_text(declaration.get(field))

    return normalized


def to_screening_fields(declaration):
    """
    Convert a synthetic ASYCUDA-aligned declaration into the internal
    field structure consumed by the compliance rule engine.

    Declaration metadata is retained so it can later be displayed,
    audited, or used by additional compliance rules.
    """
    normalized = normalize_asycuda_declaration(declaration)

    return {
        "declaration_reference": normalized["declaration_reference"],
        "declaration_type": normalized["declaration_type"],
        "customs_office_code": normalized["customs_office_code"],
        "importer": normalized["importer"],
        "product": normalized["product"],
        "declared_value": normalized["declared_value"],
        "hs_code": normalized["hs_code"],
        "country_of_origin": normalized["country_of_origin"],
        "permit_reference": normalized["permit_reference"],
    }