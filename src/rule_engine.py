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
        if not fields.get(key)
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
                        f"Declared value {declared_value} is a positive numeric value."
                    ),
                })

        except ValueError:
            results.append({
                "rule_id": "VAL-001",
                "status": "FLAG",
                "explanation": (
                    "Declared value could not be interpreted as a valid number."
                ),
            })

    # Rule HS-001: prototype HS code-description reference check
    hs_reference = {
        "8711.60": ["electric bicycle", "electric bike"]
    }

    hs_code = fields.get("hs_code")
    product = (fields.get("product") or "").lower()

    if hs_code in hs_reference:
        expected_terms = hs_reference[hs_code]

        if any(term in product for term in expected_terms):
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

    return results