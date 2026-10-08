"""
Unit 6 System Evaluation
Explainable Human-in-the-Loop Import Compliance Document Screening System

This evaluation uses labeled synthetic declarations only.

It measures:
1. Target-rule detection accuracy across the 15 configured prototype rules.
2. False-positive rate on known compliant synthetic declarations.
3. Screening-pipeline latency.
4. Screening throughput.

The results must not be interpreted as production or legal accuracy.
"""

import csv
import statistics
import sys
import time
from pathlib import Path


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
OUTPUT_DIR = PROJECT_ROOT / "evaluation"

sys.path.insert(0, str(SRC_DIR))


from app import prepare_screening_fields  # noqa: E402
from rule_engine import evaluate_rules  # noqa: E402


# ---------------------------------------------------------
# Synthetic declaration builder
# ---------------------------------------------------------

def build_document(
    reference,
    product="Electric Bicycle",
    declared_value="850.00",
    hs_code="8711.60",
    importer="Sample Trading Ltd",
    country="China",
    permit_reference="",
):
    """
    Construct a synthetic ASYCUDA-aligned import declaration.
    """

    return (
        f"Declaration Reference: {reference}\n"
        f"Declaration Type: IM4\n"
        f"Customs Office Code: MBJ\n"
        f"Importer: {importer}\n"
        f"Product: {product}\n"
        f"Declared Value: {declared_value}\n"
        f"HS Code: {hs_code}\n"
        f"Country of Origin: {country}\n"
        f"Permit Reference: {permit_reference}\n"
    )


# ---------------------------------------------------------
# 15 labeled target-rule cases
# ---------------------------------------------------------

TARGET_CASES = [
    {
        "case_id": "EVAL-001",
        "target_rule": "DOC-001",
        "expected_status": "FLAG",
        "description": "Missing mandatory importer",
        "document": build_document(
            reference="EVAL-001",
            importer="",
        ),
    },
    {
        "case_id": "EVAL-002",
        "target_rule": "VAL-001",
        "expected_status": "FLAG",
        "description": "Zero declared value",
        "document": build_document(
            reference="EVAL-002",
            declared_value="0",
        ),
    },
    {
        "case_id": "EVAL-003",
        "target_rule": "HS-001",
        "expected_status": "FLAG",
        "description": "Product description inconsistent with prototype HS reference",
        "document": build_document(
            reference="EVAL-003",
            product="Cotton T-Shirts",
            hs_code="8711.60",
        ),
    },
    {
        "case_id": "EVAL-004",
        "target_rule": "RES-001",
        "expected_status": "FLAG",
        "description": "Frozen chicken meat without permit reference",
        "document": build_document(
            reference="EVAL-004",
            product="Frozen chicken meat",
        ),
    },
    {
        "case_id": "EVAL-005",
        "target_rule": "RES-002",
        "expected_status": "FLAG",
        "description": "Fresh vegetables without permit reference",
        "document": build_document(
            reference="EVAL-005",
            product="Fresh vegetables",
        ),
    },
    {
        "case_id": "EVAL-006",
        "target_rule": "RES-003",
        "expected_status": "FLAG",
        "description": "Human ashes without permit reference",
        "document": build_document(
            reference="EVAL-006",
            product="Human ashes",
        ),
    },
    {
        "case_id": "EVAL-007",
        "target_rule": "RES-004",
        "expected_status": "FLAG",
        "description": "Prescription medication without permit reference",
        "document": build_document(
            reference="EVAL-007",
            product="Prescription medication",
        ),
    },
    {
        "case_id": "EVAL-008",
        "target_rule": "RES-005",
        "expected_status": "FLAG",
        "description": "Agricultural pesticide without permit reference",
        "document": build_document(
            reference="EVAL-008",
            product="Agricultural pesticide",
        ),
    },
    {
        "case_id": "EVAL-009",
        "target_rule": "RES-006",
        "expected_status": "FLAG",
        "description": "Firearm without permit reference",
        "document": build_document(
            reference="EVAL-009",
            product="Firearm",
        ),
    },
    {
        "case_id": "EVAL-010",
        "target_rule": "RES-007",
        "expected_status": "FLAG",
        "description": "Toy gun without permit reference",
        "document": build_document(
            reference="EVAL-010",
            product="Toy gun",
        ),
    },
    {
        "case_id": "EVAL-011",
        "target_rule": "RES-008",
        "expected_status": "FLAG",
        "description": "Camouflage jacket without permit reference",
        "document": build_document(
            reference="EVAL-011",
            product="Camouflage jacket",
        ),
    },
    {
        "case_id": "EVAL-012",
        "target_rule": "RES-009",
        "expected_status": "FLAG",
        "description": "Motor vehicle without permit reference",
        "document": build_document(
            reference="EVAL-012",
            product="Motor vehicle",
        ),
    },
    {
        "case_id": "EVAL-013",
        "target_rule": "PRO-001",
        "expected_status": "FLAG",
        "description": "Natural honey prohibited-goods prototype case",
        "document": build_document(
            reference="EVAL-013",
            product="Natural honey",
        ),
    },
    {
        "case_id": "EVAL-014",
        "target_rule": "PRO-002",
        "expected_status": "FLAG",
        "description": "Counterfeit coins prohibited-goods prototype case",
        "document": build_document(
            reference="EVAL-014",
            product="Counterfeit coins",
        ),
    },
    {
        "case_id": "EVAL-015",
        "target_rule": "PRO-003",
        "expected_status": "FLAG",
        "description": "Obscene publication prohibited-goods prototype case",
        "document": build_document(
            reference="EVAL-015",
            product="Obscene publication",
        ),
    },
]


# ---------------------------------------------------------
# Known-compliant synthetic cases
# ---------------------------------------------------------

CLEAN_CASES = []

for number in range(1, 11):
    CLEAN_CASES.append(
        {
            "case_id": f"CLEAN-{number:02d}",
            "document": build_document(
                reference=f"CLEAN-{number:02d}",
                importer=f"Compliant Importer {number}",
                product="Electric Bicycle",
                declared_value=f"{800 + number * 10}.00",
                hs_code="8711.60",
                country="China",
            ),
        }
    )


# ---------------------------------------------------------
# Screening functions
# ---------------------------------------------------------

def run_screening(document_text):
    """
    Execute the integrated screening pipeline used for evaluation.

    Raw synthetic declaration
        -> extraction
        -> ASYCUDA adapter
        -> normalized fields
        -> compliance rule engine
    """

    screening_fields = prepare_screening_fields(document_text)
    return evaluate_rules(screening_fields)


def find_rule_result(results, rule_id):
    """
    Locate one rule result by rule ID.
    """

    for result in results:
        if result.get("rule_id") == rule_id:
            return result

    return None


# ---------------------------------------------------------
# Accuracy evaluation
# ---------------------------------------------------------

def evaluate_target_rules():
    """
    Measure whether each of the 15 configured prototype rules produces
    the expected labeled outcome in its designated synthetic case.
    """

    rows = []
    correct = 0

    print()
    print("=" * 72)
    print("TARGET-RULE DETECTION EVALUATION")
    print("=" * 72)

    for case in TARGET_CASES:
        results = run_screening(case["document"])

        target_result = find_rule_result(
            results,
            case["target_rule"],
        )

        if target_result is None:
            actual_status = "NOT_RETURNED"
        else:
            actual_status = target_result.get(
                "status",
                "UNKNOWN",
            )

        passed = actual_status == case["expected_status"]

        if passed:
            correct += 1

        flag_ids = [
            result.get("rule_id")
            for result in results
            if result.get("status") == "FLAG"
        ]

        rows.append(
            {
                "case_id": case["case_id"],
                "description": case["description"],
                "target_rule": case["target_rule"],
                "expected_status": case["expected_status"],
                "actual_status": actual_status,
                "target_correct": passed,
                "all_flagged_rules": ", ".join(flag_ids),
            }
        )

        result_text = "CORRECT" if passed else "INCORRECT"

        print(
            f"{case['case_id']} | "
            f"{case['target_rule']} | "
            f"Expected {case['expected_status']} | "
            f"Actual {actual_status} | "
            f"{result_text}"
        )

    accuracy = (
        correct / len(TARGET_CASES) * 100
        if TARGET_CASES
        else 0.0
    )

    return rows, correct, accuracy


# ---------------------------------------------------------
# False-positive evaluation
# ---------------------------------------------------------

def evaluate_clean_cases():
    """
    Measure false positives using known-compliant synthetic declarations.

    A false positive occurs when any compliance rule returns FLAG for
    one of these pre-labeled clean electric-bicycle declarations.
    """

    rows = []
    false_positive_cases = 0

    print()
    print("=" * 72)
    print("CLEAN-CASE FALSE-POSITIVE EVALUATION")
    print("=" * 72)

    for case in CLEAN_CASES:
        results = run_screening(case["document"])

        flag_ids = [
            result.get("rule_id")
            for result in results
            if result.get("status") == "FLAG"
        ]

        has_false_positive = len(flag_ids) > 0

        if has_false_positive:
            false_positive_cases += 1

        rows.append(
            {
                "case_id": case["case_id"],
                "false_positive": has_false_positive,
                "flagged_rules": ", ".join(flag_ids),
            }
        )

        print(
            f"{case['case_id']} | "
            f"Flags: "
            f"{', '.join(flag_ids) if flag_ids else 'None'}"
        )

    false_positive_rate = (
        false_positive_cases / len(CLEAN_CASES) * 100
        if CLEAN_CASES
        else 0.0
    )

    clean_pass_rate = 100.0 - false_positive_rate

    return (
        rows,
        false_positive_cases,
        false_positive_rate,
        clean_pass_rate,
    )


# ---------------------------------------------------------
# Latency and throughput evaluation
# ---------------------------------------------------------

def evaluate_latency():
    """
    Measure local processing latency for the integrated screening pipeline.

    Database persistence, browser rendering, and network latency are
    intentionally excluded. The metric represents only:

        extraction
        -> ASYCUDA normalization
        -> rule evaluation

    Results therefore describe prototype screening-pipeline performance
    on the local development computer.
    """

    documents = (
        [case["document"] for case in TARGET_CASES]
        + [case["document"] for case in CLEAN_CASES]
    )

    # Warm-up runs reduce one-time interpreter/cache effects.
    for document in documents:
        run_screening(document)

    timings_ms = []

    repetitions = 100

    print()
    print("=" * 72)
    print("SCREENING LATENCY EVALUATION")
    print("=" * 72)
    print(
        f"Documents: {len(documents)} | "
        f"Repetitions per document: {repetitions}"
    )

    total_start = time.perf_counter()

    for _ in range(repetitions):
        for document in documents:
            start = time.perf_counter()

            run_screening(document)

            end = time.perf_counter()

            timings_ms.append(
                (end - start) * 1000
            )

    total_elapsed = time.perf_counter() - total_start

    average_ms = statistics.mean(timings_ms)
    median_ms = statistics.median(timings_ms)

    sorted_timings = sorted(timings_ms)

    p95_index = max(
        0,
        int(len(sorted_timings) * 0.95) - 1,
    )

    p95_ms = sorted_timings[p95_index]

    total_runs = len(timings_ms)

    throughput = (
        total_runs / total_elapsed
        if total_elapsed > 0
        else 0.0
    )

    return {
        "runs": total_runs,
        "average_ms": average_ms,
        "median_ms": median_ms,
        "p95_ms": p95_ms,
        "throughput_per_second": throughput,
    }


# ---------------------------------------------------------
# Output files
# ---------------------------------------------------------

def write_case_results(target_rows, clean_rows):
    """
    Save detailed evaluation cases to CSV.
    """

    output_path = OUTPUT_DIR / "evaluation_case_results.csv"

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        fieldnames = [
            "evaluation_group",
            "case_id",
            "description",
            "target_rule",
            "expected_status",
            "actual_status",
            "correct",
            "flagged_rules",
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in target_rows:
            writer.writerow(
                {
                    "evaluation_group": "Target-rule detection",
                    "case_id": row["case_id"],
                    "description": row["description"],
                    "target_rule": row["target_rule"],
                    "expected_status": row["expected_status"],
                    "actual_status": row["actual_status"],
                    "correct": row["target_correct"],
                    "flagged_rules": row["all_flagged_rules"],
                }
            )

        for row in clean_rows:
            writer.writerow(
                {
                    "evaluation_group": "Clean-case false-positive check",
                    "case_id": row["case_id"],
                    "description": "Known-compliant electric bicycle",
                    "target_rule": "",
                    "expected_status": "NO FLAG",
                    "actual_status": (
                        "FLAG"
                        if row["false_positive"]
                        else "NO FLAG"
                    ),
                    "correct": not row["false_positive"],
                    "flagged_rules": row["flagged_rules"],
                }
            )

    return output_path


def write_summary(
    target_correct,
    target_accuracy,
    false_positive_cases,
    false_positive_rate,
    clean_pass_rate,
    latency,
):
    """
    Save summary metrics to a text file and CSV.
    """

    text_path = OUTPUT_DIR / "evaluation_summary.txt"

    summary_lines = [
        "UNIT 6 SYSTEM EVALUATION SUMMARY",
        "=" * 50,
        "",
        "Evaluation scope:",
        "Synthetic prototype declarations only.",
        "These results do not represent production or legal accuracy.",
        "",
        "Quantitative Metrics",
        "--------------------",
        (
            "Target-rule detection accuracy: "
            f"{target_accuracy:.2f}% "
            f"({target_correct}/{len(TARGET_CASES)} cases)"
        ),
        (
            "False-positive rate on clean cases: "
            f"{false_positive_rate:.2f}% "
            f"({false_positive_cases}/{len(CLEAN_CASES)} cases)"
        ),
        (
            "Clean-case pass rate: "
            f"{clean_pass_rate:.2f}%"
        ),
        (
            "Average screening-pipeline latency: "
            f"{latency['average_ms']:.4f} ms"
        ),
        (
            "Median screening-pipeline latency: "
            f"{latency['median_ms']:.4f} ms"
        ),
        (
            "95th-percentile screening latency: "
            f"{latency['p95_ms']:.4f} ms"
        ),
        (
            "Approximate local pipeline throughput: "
            f"{latency['throughput_per_second']:.2f} "
            "screenings/second"
        ),
        (
            "Timed pipeline executions: "
            f"{latency['runs']}"
        ),
        "",
        "Interpretation note:",
        (
            "Accuracy measures whether each labeled synthetic case "
            "produced the expected outcome for its designated prototype "
            "rule. It does not establish legal correctness or real-world "
            "customs screening accuracy."
        ),
        (
            "Latency measures extraction, ASYCUDA-aligned normalization, "
            "and rule evaluation on the local development computer. "
            "Browser rendering, network communication, human review, "
            "and database persistence are excluded."
        ),
    ]

    text_path.write_text(
        "\n".join(summary_lines),
        encoding="utf-8",
    )

    csv_path = OUTPUT_DIR / "evaluation_metrics.csv"

    metrics = [
        [
            "Target-rule detection accuracy",
            f"{target_accuracy:.2f}",
            "percent",
        ],
        [
            "False-positive rate",
            f"{false_positive_rate:.2f}",
            "percent",
        ],
        [
            "Clean-case pass rate",
            f"{clean_pass_rate:.2f}",
            "percent",
        ],
        [
            "Average pipeline latency",
            f"{latency['average_ms']:.4f}",
            "milliseconds",
        ],
        [
            "Median pipeline latency",
            f"{latency['median_ms']:.4f}",
            "milliseconds",
        ],
        [
            "95th-percentile pipeline latency",
            f"{latency['p95_ms']:.4f}",
            "milliseconds",
        ],
        [
            "Local pipeline throughput",
            f"{latency['throughput_per_second']:.2f}",
            "screenings per second",
        ],
    ]

    with csv_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.writer(csv_file)

        writer.writerow(
            [
                "Metric",
                "Value",
                "Unit",
            ]
        )

        writer.writerows(metrics)

    return text_path, csv_path


# ---------------------------------------------------------
# SVG chart
# ---------------------------------------------------------

def write_svg_chart(
    target_accuracy,
    clean_pass_rate,
):
    """
    Create a dependency-free SVG visualization of percentage metrics.
    """

    output_path = OUTPUT_DIR / "evaluation_chart.svg"

    width = 900
    height = 500

    chart_left = 280
    chart_width = 520

    bar_height = 65

    first_y = 170
    second_y = 300

    first_width = (
        chart_width * target_accuracy / 100.0
    )

    second_width = (
        chart_width * clean_pass_rate / 100.0
    )

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="{height}"
    viewBox="0 0 {width} {height}"
>
    <rect
        width="100%"
        height="100%"
        fill="white"
    />

    <text
        x="450"
        y="55"
        text-anchor="middle"
        font-family="Arial"
        font-size="26"
        font-weight="bold"
    >
        Unit 6 Synthetic Evaluation Results
    </text>

    <text
        x="450"
        y="88"
        text-anchor="middle"
        font-family="Arial"
        font-size="15"
    >
        Percentage-based prototype evaluation metrics
    </text>

    <text
        x="30"
        y="{first_y + 40}"
        font-family="Arial"
        font-size="17"
    >
        Target-rule detection accuracy
    </text>

    <rect
        x="{chart_left}"
        y="{first_y}"
        width="{chart_width}"
        height="{bar_height}"
        fill="#e8edf2"
    />

    <rect
        x="{chart_left}"
        y="{first_y}"
        width="{first_width}"
        height="{bar_height}"
        fill="#355c7d"
    />

    <text
        x="{chart_left + chart_width + 15}"
        y="{first_y + 42}"
        font-family="Arial"
        font-size="18"
        font-weight="bold"
    >
        {target_accuracy:.1f}%
    </text>

    <text
        x="30"
        y="{second_y + 40}"
        font-family="Arial"
        font-size="17"
    >
        Clean-case pass rate
    </text>

    <rect
        x="{chart_left}"
        y="{second_y}"
        width="{chart_width}"
        height="{bar_height}"
        fill="#e8edf2"
    />

    <rect
        x="{chart_left}"
        y="{second_y}"
        width="{second_width}"
        height="{bar_height}"
        fill="#4f7d6b"
    />

    <text
        x="{chart_left + chart_width + 15}"
        y="{second_y + 42}"
        font-family="Arial"
        font-size="18"
        font-weight="bold"
    >
        {clean_pass_rate:.1f}%
    </text>

    <line
        x1="{chart_left}"
        y1="405"
        x2="{chart_left + chart_width}"
        y2="405"
        stroke="black"
        stroke-width="1"
    />

    <text
        x="{chart_left}"
        y="435"
        text-anchor="middle"
        font-family="Arial"
        font-size="14"
    >
        0%
    </text>

    <text
        x="{chart_left + chart_width / 2}"
        y="435"
        text-anchor="middle"
        font-family="Arial"
        font-size="14"
    >
        50%
    </text>

    <text
        x="{chart_left + chart_width}"
        y="435"
        text-anchor="middle"
        font-family="Arial"
        font-size="14"
    >
        100%
    </text>

    <text
        x="450"
        y="475"
        text-anchor="middle"
        font-family="Arial"
        font-size="13"
    >
        Labeled synthetic prototype cases; not production customs accuracy
    </text>
</svg>
"""

    output_path.write_text(
        svg,
        encoding="utf-8",
    )

    return output_path


# ---------------------------------------------------------
# Main evaluation
# ---------------------------------------------------------

def main():
    print()
    print("=" * 72)
    print("UNIT 6 - IMPORT COMPLIANCE SCREENING SYSTEM EVALUATION")
    print("=" * 72)

    target_rows, target_correct, target_accuracy = (
        evaluate_target_rules()
    )

    (
        clean_rows,
        false_positive_cases,
        false_positive_rate,
        clean_pass_rate,
    ) = evaluate_clean_cases()

    latency = evaluate_latency()

    case_csv = write_case_results(
        target_rows,
        clean_rows,
    )

    summary_txt, metrics_csv = write_summary(
        target_correct,
        target_accuracy,
        false_positive_cases,
        false_positive_rate,
        clean_pass_rate,
        latency,
    )

    chart_path = write_svg_chart(
        target_accuracy,
        clean_pass_rate,
    )

    print()
    print("=" * 72)
    print("FINAL RESULTS")
    print("=" * 72)

    print(
        "Target-rule detection accuracy: "
        f"{target_accuracy:.2f}% "
        f"({target_correct}/{len(TARGET_CASES)})"
    )

    print(
        "False-positive rate: "
        f"{false_positive_rate:.2f}% "
        f"({false_positive_cases}/{len(CLEAN_CASES)})"
    )

    print(
        "Clean-case pass rate: "
        f"{clean_pass_rate:.2f}%"
    )

    print(
        "Average pipeline latency: "
        f"{latency['average_ms']:.4f} ms"
    )

    print(
        "Median pipeline latency: "
        f"{latency['median_ms']:.4f} ms"
    )

    print(
        "95th-percentile latency: "
        f"{latency['p95_ms']:.4f} ms"
    )

    print(
        "Approximate local throughput: "
        f"{latency['throughput_per_second']:.2f} "
        "screenings/second"
    )

    print(
        "Timed pipeline runs: "
        f"{latency['runs']}"
    )

    print()
    print("Generated evaluation evidence:")
    print(f"  {case_csv}")
    print(f"  {metrics_csv}")
    print(f"  {summary_txt}")
    print(f"  {chart_path}")

    print()
    print(
        "IMPORTANT: Results describe performance on labeled "
        "synthetic prototype cases only."
    )


if __name__ == "__main__":
    main()