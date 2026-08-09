import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from task2.account_health import generate_account_brief
import json


def run_task2_evaluation():
    # Accounts confirmed to exist in the supplied dataset
    account_ids = [
        "ACC-3336",
        "ACC-3033",
        "ACC-7893",
    ]

    tests = []

    for account_id in account_ids:

        try:
            result = generate_account_brief(account_id)

            # Account brief should contain useful sections.
            if isinstance(result, dict):
                text = json.dumps(result)
            else:
                text = str(result)

            required_sections = [
                "EXECUTIVE SUMMARY",
                "OPEN RISKS",
                "RECOMMENDED TALKING POINTS",
            ]

            found = sum(
                section.lower() in text.lower()
                for section in required_sections
            )

            score = found / len(required_sections)

            tests.append({
                "account_id": account_id,
                "score": round(score, 2),
                "passed": score >= 0.66,
            })

        except Exception as e:
            tests.append({
                "account_id": account_id,
                "score": 0.0,
                "passed": False,
                "error": str(e),
            })

    # Adversarial / invalid account
    try:
        generate_account_brief("ACC-DOES-NOT-EXIST")

        tests.append({
            "account_id": "ADVERSARIAL-001",
            "score": 0.0,
            "passed": False,
        })

    except ValueError:
        # Correct behavior: invalid account should be rejected.
        tests.append({
            "account_id": "ADVERSARIAL-001",
            "score": 1.0,
            "passed": True,
        })

    except Exception as e:
        tests.append({
            "account_id": "ADVERSARIAL-001",
            "score": 0.0,
            "passed": False,
            "error": str(e),
        })

    return tests


if __name__ == "__main__":
    results = run_task2_evaluation()

    print("\nTASK 2 EVALUATION")
    print("=" * 60)

    for result in results:
        status = "PASS" if result["passed"] else "FAIL"

        print(
            f'{result["account_id"]:20} '
            f'{status:5} '
            f'{result["score"]:.2f}'
        )