import json
from datetime import datetime

from .eval_task1 import run_task1_evaluation
from .eval_task2 import run_task2_evaluation


def main():

    print("\n" + "=" * 70)
    print("ZYCUS AI SUPPORT ASSESSMENT - EVALUATION HARNESS")
    print("=" * 70)

    # -------------------------
    # TASK 1
    # -------------------------

    print("\nTASK 1 - TICKET TRIAGE")
    print("-" * 70)

    task1_results = run_task1_evaluation()

    for result in task1_results:
        status = "PASS" if result["passed"] else "FAIL"

        print(
            f'{result["ticket_id"]:25} '
            f'{status:6} '
            f'Score: {result["score"]:.2f}'
        )

    task1_score = (
        sum(r["score"] for r in task1_results)
        / len(task1_results)
        if task1_results
        else 0
    )

    # -------------------------
    # TASK 2
    # -------------------------

    print("\nTASK 2 - ACCOUNT HEALTH")
    print("-" * 70)

    task2_results = run_task2_evaluation()

    for result in task2_results:
        status = "PASS" if result["passed"] else "FAIL"

        print(
            f'{result["account_id"]:25} '
            f'{status:6} '
            f'Score: {result["score"]:.2f}'
        )

    task2_score = (
        sum(r["score"] for r in task2_results)
        / len(task2_results)
        if task2_results
        else 0
    )

    # -------------------------
    # OVERALL
    # -------------------------

    overall_score = (task1_score + task2_score) / 2

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "task1": {
            "tests": task1_results,
            "average_score": round(task1_score, 2),
        },
        "task2": {
            "tests": task2_results,
            "average_score": round(task2_score, 2),
        },
        "overall_score": round(overall_score, 2),
    }

    print("\n" + "=" * 70)
    print("EVALUATION SUMMARY")
    print("=" * 70)

    print(f"Task 1 Score : {task1_score:.2f}")
    print(f"Task 2 Score : {task2_score:.2f}")
    print(f"Overall Score: {overall_score:.2f}")

    with open("task3/eval_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nReport saved to:")
    print("task3/eval_report.json")


if __name__ == "__main__":
    main()