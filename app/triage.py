import json

from app.llm_client import create_llm_client
from app.prompts import SYSTEM_PROMPT
from app.schemas import TriageResult
from app.retriever import search_knowledge_base
from app.kb_loader import load_knowledge_base

def triage_ticket(ticket):

    # Load knowledge base
    documents = load_knowledge_base()

    # Create retrieval query
    query = f"""
    {ticket["subject"]}

    {ticket["body"]}
    """

    # Retrieve relevant documents
    retrieved_docs = search_knowledge_base(
        query,
        documents,
        product=ticket.get("product"),
        top_k=3
    )

    # Prepare knowledge context
    knowledge_context = "\n\n".join(
        f"DOCUMENT: {doc['filename']}\n{doc['content']}"
        for doc in retrieved_docs
    )

    # Build prompt
    user_prompt = f"""
    Analyze this support ticket.

    TICKET

    Subject:
    {ticket["subject"]}

    Body:
    {ticket["body"]}

    RETRIEVED KNOWLEDGE BASE

    {knowledge_context}

    Return a JSON object with exactly these fields:

    - product_area
    - issue_category
    - urgency
    - reasoning
    - known_issue
    - relevant_documents
    - recommended_team
    - draft_response
    """

    # Create LLM client
    client = create_llm_client()

    # Call LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0
    )

    llm_output = response.choices[0].message.content


    # Remove Markdown code fences if the LLM adds them
    cleaned_output = llm_output.strip()

    if cleaned_output.startswith("```json"):
        cleaned_output = cleaned_output[len("```json"):].strip()

    if cleaned_output.endswith("```"):
        cleaned_output = cleaned_output[:-3].strip()

    # Convert JSON string to Python dictionary
    result_data = json.loads(cleaned_output)

    # Validate with Pydantic
    result = TriageResult(**result_data)

    return result