from data_loader import load_tickets
from triage import triage_ticket


tickets = load_tickets()

test_indexes = [0, 10, 20, 30, 40]

for index in test_indexes:

    ticket = tickets[index]

    print("\n" + "=" * 70)

    print("TICKET:", ticket["ticket_id"])
    print("SUBJECT:", ticket["subject"])

    result = triage_ticket(ticket)

    print("\nRESULT")
    print("Product Area:", result.product_area.value)
    print("Category:", result.issue_category.value)
    print("Urgency:", result.urgency.value)
    print("Known Issue:", result.known_issue)
    print("Documents:", result.relevant_documents)
    print("Team:", result.recommended_team)