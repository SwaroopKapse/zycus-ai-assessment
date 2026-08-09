import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.llm_client import create_llm_client


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_accounts():
    with open(DATA_DIR / "accounts.json", "r") as file:
        return json.load(file)


def load_tickets():
    with open(DATA_DIR / "tickets.json", "r") as file:
        return json.load(file)


def get_account(account_id):
    accounts = load_accounts()

    for account in accounts:
        if account.get("account_id") == account_id:
            return account

    return None


def get_account_tickets(account_id):
    tickets = load_tickets()

    account_tickets = []

    for ticket in tickets:
        if ticket.get("account_id") == account_id:
            account_tickets.append(ticket)

    return account_tickets


def filter_last_90_days(tickets):
    if not tickets:
        return []

    dates = []

    for ticket in tickets:
        try:
            date = datetime.fromisoformat(
                ticket["created_at"].replace("Z", "+00:00")
            )
            dates.append(date)
        except (KeyError, ValueError):
            continue

    if not dates:
        return []

    # Use the latest dataset timestamp as the reference date.
    # This keeps the mock dataset meaningful and reproducible.
    reference_date = max(dates)

    cutoff_date = reference_date - timedelta(days=90)

    recent_tickets = []

    for ticket in tickets:
        try:
            created_at = datetime.fromisoformat(
                ticket["created_at"].replace("Z", "+00:00")
            )

            if created_at >= cutoff_date:
                recent_tickets.append(ticket)

        except (KeyError, ValueError):
            continue

    return recent_tickets


def find_risk_candidates(tickets):
    risk_keywords = [
        "cancel",
        "cancellation",
        "churn",
        "competitor",
        "escalat",
        "unhappy",
        "dissatisfied",
        "renewal",
        "renew",
        "terminate",
        "executive",
        "urgent",
        "critical",
        "complaint",
        "breach",
    ]

    candidates = []

    for ticket in tickets:

        text = (
            ticket.get("subject", "")
            + " "
            + ticket.get("body", "")
        ).lower()

        matched_keywords = []

        for keyword in risk_keywords:
            if keyword in text:
                matched_keywords.append(keyword)

        if matched_keywords:
            candidates.append({
                "ticket_id": ticket.get("ticket_id"),
                "subject": ticket.get("subject"),
                "body": ticket.get("body"),
                "status": ticket.get("status"),
                "urgency": ticket.get("urgency"),
                "matched_keywords": matched_keywords
            })

    return candidates


def build_account_context(account, tickets, risk_candidates):

    return f"""
CUSTOMER ACCOUNT

{json.dumps(account, indent=2)}

RECENT TICKETS - LAST 90 DAYS

{json.dumps(tickets, indent=2)}

POTENTIAL RISK TICKETS

{json.dumps(risk_candidates, indent=2)}
"""


def generate_account_brief(account_id):

    # -----------------------------
    # 1. Load accounts.json
    # -----------------------------

    accounts_path = Path(__file__).resolve().parent.parent / "data" / "accounts.json"

    with open(accounts_path, "r") as file:
        accounts = json.load(file)

    # Find requested account
    account = next(
        (a for a in accounts if a["account_id"] == account_id),
        None
    )

    if account is None:
        raise ValueError(f"Account {account_id} not found")


    # -----------------------------
    # 2. Load tickets.json
    # -----------------------------

    tickets_path = Path(__file__).resolve().parent.parent / "data" / "tickets.json"

    with open(tickets_path, "r") as file:
        tickets = json.load(file)


    # -----------------------------
    # 3. Get this account's tickets
    # -----------------------------

    account_tickets = [
        ticket
        for ticket in tickets
        if ticket["account_id"] == account_id
    ]


    # -----------------------------
    # 4. Calculate deterministic
    #    90-day window
    # -----------------------------

    if tickets:

        dataset_latest_date = max(
            datetime.fromisoformat(
                ticket["created_at"].replace("Z", "+00:00")
            )
            for ticket in tickets
        )

    else:

        dataset_latest_date = datetime.now(timezone.utc)


    cutoff_date = dataset_latest_date - timedelta(days=90)


    # -----------------------------
    # 5. Keep last 90 days
    # -----------------------------

    recent_tickets = [
        ticket
        for ticket in account_tickets
        if datetime.fromisoformat(
            ticket["created_at"].replace("Z", "+00:00")
        ) >= cutoff_date
    ]

    user_prompt = f"""
Create an account health brief using ONLY the supplied account
information and ticket information.

ACCOUNT DATA:
{json.dumps(account, indent=2)}

TICKETS FROM THE LAST 90 DAYS:
{json.dumps(recent_tickets, indent=2)}

IMPORTANT RULES:

1. Do not invent information.
2. Do not use external knowledge.
3. Distinguish account-level risks from ticket-level risks.
4. Any ticket-based risk MUST include the exact ticket ID.
5. Any ticket-based risk MUST include a direct quote copied from
the ticket body.
6. Never invent or manufacture a quote.
7. If there is no direct ticket evidence for churn risk, say so.
8. Only analyze the supplied last-90-day tickets.

Return exactly these sections:

EXECUTIVE SUMMARY:
3-5 sentences.

OPEN RISKS & FLAGGED ISSUES:
List important risks.
For each ticket-based risk include:
- Ticket ID
- Risk
- Direct quote
- Why it matters

RECOMMENDED TALKING POINTS:
Actionable bullet points for the TAM.
"""

    client = create_llm_client()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a precise customer-success analysis assistant. "
                    "Use only supplied data. Never invent facts."
                )
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0
    )

    output = response.choices[0].message.content.strip()
    # print("\n========== RAW TASK 2 OUTPUT ==========\n")
    # print(output)
    # print("\n========== END RAW OUTPUT ==========\n")
    #     # Remove markdown code fences if the model adds them.
    # if output.startswith("```"):
    #     output = output.replace("```json", "")
    #     output = output.replace("```", "")
    #     output = output.strip()

    # result = json.loads(output)

    return output