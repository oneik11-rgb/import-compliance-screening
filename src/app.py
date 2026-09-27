import re

from flask import Flask, render_template, request

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
    patterns = {
        "importer": r"(?im)^Importer:\s*(.+)$",
        "product": r"(?im)^Product:\s*(.+)$",
        "declared_value": r"(?im)^Declared Value:\s*([0-9]+(?:\.[0-9]+)?)\s*$",
        "hs_code": r"(?im)^HS Code:\s*([0-9.]+)\s*$",
        "country_of_origin": r"(?im)^Country of Origin:\s*(.+)$",
    }

    extracted = {}

    for field, pattern in patterns.items():
        match = re.search(pattern, document_text)
        extracted[field] = match.group(1).strip() if match else None

    return extracted


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/screen", methods=["POST"])
def screen_document():
    document_text = request.form.get("document_text", "")

    extracted_fields = extract_fields(document_text)
    rule_results = evaluate_rules(extracted_fields)

    screening_id = save_screening(
        document_text,
        extracted_fields,
    )

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
    audit_id = request.form.get("audit_id", type=int)
    decision = request.form.get("decision", "").strip()
    reviewer_note = request.form.get("reviewer_note", "").strip()

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