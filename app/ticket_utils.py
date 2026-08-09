def find_tickets_by_product(tickets , product_name):
    results = []
    for ticket in tickets:
        if ticket["product"] == product_name:
            results.append(tickets)

    return results
# 
def find_tickets_by_urgency(tickets, urgency):
    results = []
    for ticket in tickets:
        if ticket["urgency"] == urgency:
            results.append(ticket)
    return results
