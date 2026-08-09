from fastapi import FastAPI
from pydantic import BaseModel

from app.triage import triage_ticket

app = FastAPI(
    title="AI Support Triage API",
    description="LLM-powered support ticket triage system",
    version="1.0.0"
)


class TicketRequest(BaseModel):
    subject: str
    body: str
    product: str | None = None


@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "AI Support Triage API"
    }


@app.post("/triage")
def triage(request: TicketRequest):

    ticket = {
        "subject": request.subject,
        "body": request.body,
        "product": request.product
    }

    result = triage_ticket(ticket)

    return result.model_dump(mode="json")