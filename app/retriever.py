from app.kb_loader import load_knowledge_base

def search_knowledge_base(query, documents, product=None, top_k=3):
    query_words = set(query.lower().split())

    results = []

    for document in documents:
        content = document["content"].lower()
        filename = document["filename"].lower()

        score = 0

        # Match words from the query
        for word in query_words:
            if word in content:
                score += 1

        # Give extra importance to the product name
        if product and product.lower() in content:
            score += 5

        # Give a small boost if product name appears in filename
        if product and product.lower().replace(" ", "-") in filename:
            score += 3

        results.append({
            "filename": document["filename"],
            "score": score,
            "content": document["content"]
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":
    documents = load_knowledge_base()

    query = "DataBridge pipeline slow throughput"

    results = search_knowledge_base(
        query,
        documents,
        product="DataBridge Pro"
    )

    for result in results:
        print(
            result["filename"],
            "Score:",
            result["score"]
        )