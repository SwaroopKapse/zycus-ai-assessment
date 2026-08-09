from app.schemas import TriageResult


result = TriageResult(
    product_area="Data Ingestion",
    issue_category="Performance",
    urgency="P2",
    reasoning="The customer reports degraded processing performance.",
    known_issue=True,
    relevant_documents=[
        "databridge-pro.md",
        "performance-and-integrations.md"
    ],
    recommended_team="Data Platform Support",
    draft_response="Thank you for reporting this issue. We are reviewing the reported performance problem."
)


print(result)
print()
print(result.model_dump())