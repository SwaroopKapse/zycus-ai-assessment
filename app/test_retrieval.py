from app.data_loader import load_tickets
from app.kb_loader import load_knowledge_base
from app.retriever import search_knowledge_base


tickets = load_tickets()
documents = load_knowledge_base()

ticket = tickets[0]

query = ticket["subject"] + " " + ticket["body"]

results = search_knowledge_base(
    query,
    documents,
    product=ticket["product"],
    top_k=3
)

print("\nTICKET")
print("Subject:", ticket["subject"])
print("Product:", ticket["product"])
print("Product Area:", ticket["product_area"])
print("Category:", ticket["category"])
print("Urgency:", ticket["urgency"])

print("\nRETRIEVED DOCUMENTS")

for result in results:
    print(
        result["filename"],
        "Score:",
        result["score"]
    )