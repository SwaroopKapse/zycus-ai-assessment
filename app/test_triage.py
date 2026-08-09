from app.data_loader import load_tickets
from app.triage import triage_ticket


tickets = load_tickets()

ticket = tickets[0]

result = triage_ticket(ticket)

print("\n===== TRIAGE RESULT =====\n")

print(result)

print("\n===== AS DICTIONARY =====\n")

print(result.model_dump())