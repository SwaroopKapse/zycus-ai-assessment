
# import json
# def load_tickets():
#     with open("data/tickets.json", "r") as file:
#         tickets = json.load(file)
#     return tickets
# tickets = load_tickets()
# first_ticket = tickets[0]

# print("Number Of Tickets:", len(tickets))
# print("\nFields:")
# for field in first_ticket.items():
#     print("-", field)

# print("company:", tickets[0]["company"])
# print("product:", tickets[0]["product"])
# print("tags:", tickets[0]["tags"])
# count=0
# for ticket in tickets:
#     if ticket["product"] == "DataBridge Pro":
#         print("Ticket ID:", ticket["ticket_id"])
#         count+=1
# print("Total Tickets for DataBridge Pro:", count)

# function call from ticket_utils.py
import json

from app.ticket_utils import find_tickets_by_product
from app.ticket_utils import find_tickets_by_urgency

with open("data/tickets.json", "r") as file:
    tickets = json.load(file)
p1_tickets = find_tickets_by_urgency(tickets, "P1")
print("P1 tickets:", len(p1_tickets))
# databridge_tickets = find_tickets_by_product(
#     tickets,
#     "DataBridge Pro"
# )

# print("DataBridge Pro tickets:", len(databridge_tickets))