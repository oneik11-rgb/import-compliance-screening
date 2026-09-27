import re

from flask import Flask, render_template, request

from rule_engine import evaluate_rules

app = Flask(__name__)


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

    return render_template(
        "results.html",
        document_text=document_text,
        fields=extracted_fields,
        results=rule_results,
    )


if __name__ == "__main__":
    app.run(debug=True)