import re

from rules_config import (
    HS_REFERENCE,
    PROHIBITED_GOODS_RULES,
    RESTRICTED_GOODS_RULES,
)


def _contains_keyword(product_text, keywords):
    """
    Return True when the product description contains one of the
    configured keywords as a complete word or phrase.
    """
    product_text = (product_text or "").lower()

    for keyword in keywords:
        pattern = rf"\b{re.escape(keyword.lower())}\b"

        if re.search(pattern, product_text):
            return True

    return False


def _evaluate_restricted_goods(product, permit_reference):
    """
    Evaluate configured restricted-goods rules.

    The prototype checks only whether synthetic permit information
    was supplied. It does not verify the authenticity, validity,
    expiry, quantity, or legal sufficiency of a permit.
    """
    results = []

    permit_reference = str(permit_reference or "").strip()

    for rule in RESTRICTED_GOODS_RULES:
        if not _contains_keyword(product, rule["keywords"]):
            continue

        if permit_reference:
            results.append({
                "rule_id": rule["rule_id"],
                "status": "PASS",
                "explanation": (
                    f"{rule['name']} was detected and permit or licence "
                    f"information was supplied as {permit_reference}. "
                    f"The reference must still be validated by an "
                    f"authorized human reviewer. Prototype authority: "
                    f"{rule['authority']}."
                ),
            })
        else:
            results.append({
                "rule_id": rule["rule_id"],
                "status": "FLAG",
                "explanation": (
                    f"{rule['name']} was detected but no permit or licence "
                    f"reference was supplied. Human review is required. "
                    f"Prototype authority: {rule['authority']}."
                ),
            })

    return results


def _evaluate_prohibited_goods(product):
    """
    Evaluate configured prohibited-goods rules.

    A detected prohibited-goods keyword produces a FLAG for human review.
    """
    results = []

    for rule in PROHIBITED_GOODS_RULES:
        if not _contains_keyword(product, rule["keywords"]):
            continue

        results.append({
            "rule_id": rule["rule_id"],
            "status": "FLAG",
            "explanation": (
                f"{rule['name']} matches a prohibited-goods rule in the "
                f"prototype reference configuration. Human review is "
                f"required. Prototype authority: {rule['authority']}."
            ),
        })

    return results


def evaluate_rules(fields):
    results = []

    # Rule DOC-001: required fields must be present
    required_fields = {
        "importer": "Importer",
        "product": "Product",
        "declared_value": "Declared Value",
        "hs_code": "HS Code",
        "country_of_origin": "Country of Origin",
    }

    missing_fields = [
        label
        for key, label in required_fields.items()
        if not str(fields.get(key) or "").strip()
    ]

    if missing_fields:
        results.append({
            "rule_id": "DOC-001",
            "status": "FLAG",
            "explanation": (
                "Mandatory-field completeness check failed. "
                "Missing field(s): " + ", ".join(missing_fields)
            ),
        })
    else:
        results.append({
            "rule_id": "DOC-001",
            "status": "PASS",
            "explanation": (
                "All mandatory prototype document fields were extracted."
            ),
        })

    # Rule VAL-001: declared value must be a positive number
    declared_value = fields.get("declared_value")

    if declared_value:
        try:
            value = float(declared_value)

            if value <= 0:
                results.append({
                    "rule_id": "VAL-001",
                    "status": "FLAG",
                    "explanation": (
                        "Declared value must be greater than zero."
                    ),
                })
            else:
                results.append({
                    "rule_id": "VAL-001",
                    "status": "PASS",
                    "explanation": (
                        f"Declared value {declared_value} is a "
                        f"positive numeric value."
                    ),
                })

        except ValueError:
            results.append({
                "rule_id": "VAL-001",
                "status": "FLAG",
                "explanation": (
                    "Declared value could not be interpreted "
                    "as a valid number."
                ),
            })

    # Rule HS-001: prototype HS code-description reference check
    hs_code = str(fields.get("hs_code") or "").strip()
    product = str(fields.get("product") or "").strip()

    if hs_code in HS_REFERENCE:
        expected_terms = HS_REFERENCE[hs_code]

        if any(term in product.lower() for term in expected_terms):
            results.append({
                "rule_id": "HS-001",
                "status": "PASS",
                "explanation": (
                    f"Product description is consistent with the prototype "
                    f"reference entry for HS code {hs_code}."
                ),
            })
        else:
            results.append({
                "rule_id": "HS-001",
                "status": "FLAG",
                "explanation": (
                    f"Product description does not match the predefined "
                    f"prototype reference entry for HS code {hs_code}."
                ),
            })

    elif hs_code:
        results.append({
            "rule_id": "HS-001",
            "status": "FLAG",
            "explanation": (
                f"HS code {hs_code} is not available in the current "
                f"prototype reference table and requires human review."
            ),
        })

    # Rules RES-001 through RES-009:
    # restricted-goods permit-information screening
    permit_reference = fields.get("permit_reference")

    results.extend(
        _evaluate_restricted_goods(
            product=product,
            permit_reference=permit_reference,
        )
    )

    # Rules PRO-001 through PRO-003:
    # prohibited-goods screening
    results.extend(
        _evaluate_prohibited_goods(product)
    )

    return results