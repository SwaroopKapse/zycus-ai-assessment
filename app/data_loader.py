import json
def load_tickets():
    with open("data/tickets.json", "r") as file:
        tickets = json.load(file)
    return tickets
tickets = load_tickets()
print("Number Of Tickets:", len(tickets))

