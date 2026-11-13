
from ollama import chat


def build_prompt(claim):
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
- Do not approve or deny the claim.
- Identify information that is missing.
- Recommend human review when appropriate.

INPUT CLAIM:
<claim>
{claim}
</claim>

OUTPUT REQUIREMENTS:
Provide:
1. Claim category
2. Brief summary
3. Missing information
4. Priority: Low, Medium, or High
5. Human-review recommendation: Yes or No
"""


test_claims = [
    "A pipe burst in my house, but I have no repair estimate.",
    "My car was hit in a parking lot, and the other driver left.",
    "My laptop was stolen from my office, but I have no police report.",
]

for index, claim in enumerate(test_claims, start=1):
    prompt = build_prompt(claim)

    response = chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    print(f"\n{'=' * 60}")
    print(f"TEST CLAIM {index}: {claim}")
    print("=" * 60)
    print(response.message.content)
