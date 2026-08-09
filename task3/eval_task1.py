import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.triage import triage_ticket
from app.data_loader import load_tickets


def score_result(result, expected):
    score = 0.0
    checks = 0

    # Product area
    if str(result.product_area.value) == expected["product_area"]:
        score += 1
    checks += 1

    # Category
    if str(result.issue_category.value) == expected["issue_category"]:
        score += 1
    checks += 1

    # Urgency
    if str(result.urgency.value) == expected["urgency"]:
        score += 1
    checks += 1

    # Known issue
    if result.known_issue == expected["known_issue"]:
        score += 1
    checks += 1

    return score / checks


def run_task1_evaluation():
    tickets = load_tickets()

    # Use known tickets from the supplied dataset
    test_ids = [
        "TKT-10000",
        "TKT-10010",
        "TKT-10020",
        "TKT-10030",
    ]

    tests = []

    expected = {
        "TKT-10000": {
            "product_area": "Data Ingestion",
            "issue_category": "Feature Request",
            "urgency": "P2",
            "known_issue": False,
        },
        "TKT-10010": {
            "product_area": "Permissions",
            "issue_category": "How-To",
            "urgency": "P3",
            "known_issue": False,
        },
        "TKT-10020": {
            "product_area": "Key Management",
            "issue_category": "Bug",
            "urgency": "P1",
            "known_issue": False,
        },
        "TKT-10030": {
            "product_area": "Data Ingestion",
            "issue_category": "Data Loss",
            "urgency": "P1",
            "known_issue": False,
        },
    }

    for ticket_id in test_ids:
        ticket = next(
            (t for t in tickets if t["ticket_id"] == ticket_id),
            None
        )

        if not ticket:
            continue

        try:
            result = triage_ticket(ticket)
            score = score_result(result, expected[ticket_id])

            tests.append({
                "ticket_id": ticket_id,
                "score": round(score, 2),
                "passed": score >= 0.75,
            })

        except Exception as e:
            tests.append({
                "ticket_id": ticket_id,
                "score": 0.0,
                "passed": False,
                "error": str(e),
            })

    # Adversarial test
    adversarial_ticket = {
        "ticket_id": "ADVERSARIAL-001",
        "subject": "Something is not working",
        "body": "Please help. We are having an issue.",
        "product": "DataBridge Pro",
    }

    try:
        result = triage_ticket(adversarial_ticket)

        # We only check that the system handles ambiguity
        valid = (
            result.product_area is not None
            and result.issue_category is not None
            and result.urgency is not None
        )

        tests.append({
            "ticket_id": "ADVERSARIAL-001",
            "score": 1.0 if valid else 0.0,
            "passed": valid,
        })

    except Exception as e:
        tests.append({
            "ticket_id": "ADVERSARIAL-001",
            "score": 0.0,
            "passed": False,
            "error": str(e),
        })

    return tests


if __name__ == "__main__":
    results = run_task1_evaluation()

    print("\nTASK 1 EVALUATION")
    print("=" * 60)

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"
        print(
            f'{result["ticket_id"]:20} '
            f'{status:5} '
            f'{result["score"]:.2f}'
        )