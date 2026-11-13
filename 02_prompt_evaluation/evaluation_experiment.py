
import json
import time
import sys
from pathlib import Path

from ollama import chat


# Make the project root accessible for imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from data.claims_dataset import claims_dataset


MODEL = "qwen2.5:7b"

RESULTS_DIR = PROJECT_ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

RESULTS_FILE = RESULTS_DIR / "evaluation_results.jsonl"


# Original prompt: basic instructions
def original_prompt(claim: str) -> str:
    return f"""
Classify this insurance claim and identify missing information.

Claim:
{claim}

Return your answer as JSON with these fields:
- category
- summary
- missing_information
- priority
- human_review
"""


# Enhanced prompt: detailed instructions and constraints
def enhanced_prompt(claim: str) -> str:
    return f"""
ROLE:
You are a preliminary insurance-claim triage assistant.

OBJECTIVE:
Classify the insurance claim and identify missing information.

ALLOWED CLAIM CATEGORIES:
- Property Damage
- Vehicle Damage
- Medical Expense
- Theft
- Other

RULES:
- Select exactly one category from the allowed list.
- Do not invent facts.
- Do not approve or deny claims.
- Identify information that is not provided.
- Recommend human review when appropriate.

INPUT CLAIM:
<claim>
{claim}
</claim>

OUTPUT REQUIREMENTS:
Return valid JSON using exactly these fields:
- category: string
- summary: string
- missing_information: array of strings
- priority: Low, Medium, or High
- human_review: Yes or No
"""


def run_model(prompt: str) -> tuple[str, float]:
    start = time.perf_counter()

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        format="json",
        options={"temperature": 0},
    )

    latency_seconds = time.perf_counter() - start

    return response.message.content, latency_seconds


def evaluate_output(raw_output: str, item: dict) -> dict:
    try:
        parsed = json.loads(raw_output)

        predicted_category = str(
            parsed.get("category", "")
        ).strip().lower()

        expected_category = item["expected_category"].strip().lower()

        category_correct = (
            predicted_category == expected_category
        )

        missing_information = parsed.get(
            "missing_information", []
        )

        if isinstance(missing_information, str):
            missing_information = [missing_information]

        missing_text = " ".join(
            str(value).lower()
            for value in missing_information
        )

        required_missing = item["required_missing"]

        matched_missing = [
            field
            for field in required_missing
            if field.lower() in missing_text
        ]

        missing_coverage = (
            len(matched_missing) / len(required_missing)
            if required_missing
            else 1.0
        )

        return {
            "parsed_output": parsed,
            "category_correct": category_correct,
            "matched_missing": matched_missing,
            "missing_coverage": missing_coverage,
        }

    except (json.JSONDecodeError, AttributeError, TypeError):
        return {
            "parsed_output": None,
            "category_correct": False,
            "matched_missing": [],
            "missing_coverage": 0.0,
        }


# Run the evaluation experiment
evaluation_summary = {
    "original": {
        "correct_categories": 0,
        "missing_coverage": 0.0,
        "total_latency": 0.0,
    },
    "enhanced": {
        "correct_categories": 0,
        "missing_coverage": 0.0,
        "total_latency": 0.0,
    },
}

total_runs = len(claims_dataset)

with open(RESULTS_FILE, "w", encoding="utf-8") as output_file:

    for item in claims_dataset:

        for version, prompt_function in [
            ("original", original_prompt),
            ("enhanced", enhanced_prompt),
        ]:

            raw_output, latency = run_model(
                prompt_function(item["claim"])
            )

            evaluation = evaluate_output(raw_output, item)

            record = {
                "id": item["id"],
                "version": version,
                "expected_category": item["expected_category"],
                "required_missing": item["required_missing"],
                "claim": item["claim"],
                "raw_output": raw_output,
                "parsed_output": evaluation["parsed_output"],
                "category_correct": evaluation["category_correct"],
                "matched_missing": evaluation["matched_missing"],
                "missing_coverage": round(
                    evaluation["missing_coverage"], 2
                ),
                "latency_seconds": round(latency, 3),
            }

            output_file.write(
                json.dumps(record, ensure_ascii=False) + "\n"
            )

            summary = evaluation_summary[version]

            if evaluation["category_correct"]:
                summary["correct_categories"] += 1

            summary["missing_coverage"] += (
                evaluation["missing_coverage"]
            )

            summary["total_latency"] += latency

            print("\n" + "=" * 60)
            print(f"CLAIM {item['id']} | {version.upper()}")
            print("=" * 60)
            print("Claim:", item["claim"])
            print("Expected category:", item["expected_category"])
            print("Category correct:", evaluation["category_correct"])
            print("Missing information matched:", evaluation["matched_missing"])
            print("Missing information coverage:",
                  f"{evaluation['missing_coverage'] * 100:.1f}%")
            print(f"Latency: {latency:.2f}s")
            print("\nModel output:")
            print(raw_output)


# Print final comparison
print("\n" + "=" * 60)
print("FINAL EVALUATION SUMMARY")
print("=" * 60)

for version, summary in evaluation_summary.items():

    accuracy = (
        summary["correct_categories"] / total_runs
    ) * 100

    average_missing_coverage = (
        summary["missing_coverage"] / total_runs
    ) * 100

    average_latency = (
        summary["total_latency"] / total_runs
    )

    print(f"\n{version.upper()} PROMPT")
    print(f"Category accuracy: {accuracy:.1f}%")
    print(f"Missing information coverage: {average_missing_coverage:.1f}%")
    print(f"Average latency: {average_latency:.2f}s")

print("\nResults saved to:", RESULTS_FILE)
