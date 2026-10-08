import re

from flask import Flask, render_template, request

from asycuda_adapter import to_screening_fields
from database import (
    initialize_database,
    save_reviewer_decision,
    save_rule_results,
    save_screening,
)
from rule_engine import evaluate_rules


app = Flask(__name__)

initialize_database()


ALLOWED_DECISIONS = {
    "CONFIRM_FLAG",
    "OVERRIDE_FLAG",
    "NEEDS_FURTHER_REVIEW",
}


def extract_fields(document_text):
    """
    Extract supported fields from the synthetic import declaration.

    Regular expressions are restricted to individual lines so that
    an empty field cannot consume the following declaration field.
    """

    patterns = {
        "declaration_reference":
            r"(?im)^Declaration Reference:[ \t]*([^\r\n]*)",

        "declaration_type":
            r"(?im)^Declaration Type:[ \t]*([^\r\n]*)",

        "customs_office_code":
            r"(?im)^Customs Office Code:[ \t]*([^\r\n]*)",

        "importer":
            r"(?im)^Importer:[ \t]*([^\r\n]*)",

        "product":
            r"(?im)^Product:[ \t]*([^\r\n]*)",

        "declared_value":
            r"(?im)^Declared Value:[ \t]*([^\r\n]*)",

        "hs_code":
            r"(?im)^HS Code:[ \t]*([^\r\n]*)",

        "country_of_origin":
            r"(?im)^Country of Origin:[ \t]*([^\r\n]*)",

        "permit_reference":
            r"(?im)^Permit Reference:[ \t]*([^\r\n]*)",
    }

    extracted = {}

    for field, pattern in patterns.items():
        match = re.search(pattern, document_text)

        if match:
            extracted[field] = match.group(1).strip()
        else:
            extracted[field] = None

    return extracted


def prepare_screening_fields(document_text):
    """
    Convert a raw synthetic declaration into normalized screening fields.

    Integration flow:
        raw declaration text
        -> field extraction
        -> ASYCUDA-aligned adapter
        -> normalized screening fields
    """

    extracted_fields = extract_fields(document_text)

    screening_fields = to_screening_fields(
        extracted_fields
    )

    return screening_fields


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/screen", methods=["POST"])
def screen_document():
    """
    Process a synthetic ASYCUDA-aligned declaration through the
    integrated compliance-screening workflow.
    """

    document_text = request.form.get(
        "document_text",
        "",
    )

    # Extract fields for display and persistence.
    extracted_fields = extract_fields(
        document_text
    )

    # Pass the raw declaration through the integration boundary:
    # extraction -> ASYCUDA adapter -> normalized screening fields.
    screening_fields = prepare_screening_fields(
        document_text
    )

    # Run the normalized declaration through the compliance rule engine.
    rule_results = evaluate_rules(
        screening_fields
    )

    # Save declaration and extracted data.
    screening_id = save_screening(
        document_text,
        extracted_fields,
    )

    # Save automated rule results for auditability.
    saved_results = save_rule_results(
        screening_id,
        rule_results,
    )

    return render_template(
        "results.html",
        document_text=document_text,
        fields=extracted_fields,
        results=saved_results,
        screening_id=screening_id,
    )


@app.route("/review", methods=["POST"])
def review_result():
    """
    Record the authorized human reviewer's decision for a flagged
    compliance result.
    """

    audit_id = request.form.get(
        "audit_id",
        type=int,
    )

    decision = request.form.get(
        "decision",
        "",
    ).strip()

    reviewer_note = request.form.get(
        "reviewer_note",
        "",
    ).strip()

    if audit_id is None or decision not in ALLOWED_DECISIONS:
        return "Invalid reviewer decision request.", 400

    save_reviewer_decision(
        audit_id,
        decision,
        reviewer_note,
    )

    return render_template(
        "review_saved.html",
        audit_id=audit_id,
        decision=decision,
        reviewer_note=reviewer_note,
    )


if __name__ == "__main__":
    app.run(debug=True)