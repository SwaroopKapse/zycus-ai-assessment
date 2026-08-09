# Task 4 — Production Design Note

## 1. Failure Modes

The top three production failure modes for this solution are LLM failures, retrieval failures, and data/API failures.

### LLM failures

The LLM may return malformed JSON, incomplete fields, hallucinated information, or an unexpected response format. This is especially important because Task 1 and Task 2 depend on structured outputs.

To detect this, the application validates LLM responses using JSON parsing and Pydantic schemas where applicable. Invalid responses should be logged with the ticket/account ID and model response metadata.

To mitigate the problem, the system should use strict structured-output requirements, low temperature, schema validation, and a limited retry mechanism. A fallback response can be returned when the model remains unavailable or produces invalid output.

### Retrieval failures

The knowledge-base retriever currently uses lightweight keyword matching. A relevant document may therefore be missed when a ticket uses different terminology, synonyms, or unusual wording. Incorrect retrieval can result in an incorrect classification or recommendation.

This can be detected by monitoring retrieval scores and checking whether the retrieved documents actually relate to the product and issue. Low-confidence retrieval should be flagged rather than blindly passed to the LLM.

The mitigation would be to improve the retrieval layer using hybrid search: combine keyword/BM25 retrieval with embedding-based semantic search, followed by reranking. Product-specific filtering can also reduce irrelevant documents.

### External API and service failures

The application depends on the LLM API. Network failures, API rate limits, provider outages, or timeouts can prevent tickets from being processed.

These failures can be detected through request timeouts, HTTP/API error monitoring, latency metrics, and error-rate monitoring.

Mitigation includes retries with exponential backoff, request timeouts, rate limiting, caching where appropriate, and a fallback queue. Tickets that cannot be processed immediately should be stored and retried rather than lost.

---

## 2. Latency vs Quality

A concrete trade-off in this solution is the use of a relatively capable LLM together with retrieval context for better reasoning and more accurate support responses.

Sending the ticket together with multiple retrieved knowledge-base documents increases prompt size and therefore increases response latency and token usage. However, this improves output quality because the model has product-specific information instead of relying only on its general knowledge.

The current design prioritizes correctness over minimum latency because support triage benefits from reliable classification and routing.

If latency became the hard constraint, I would reduce the number of retrieved documents, truncate unnecessary document content, use a smaller/faster model, and perform simple deterministic classification before calling the LLM. For example, product detection and obvious category detection could be handled with rules, while the LLM would only process ambiguous cases.

---

## 3. Data Sensitivity

Ticket and account information may contain personally identifiable information (PII), customer information, credentials, or other sensitive business data.

The application should follow a data-minimisation principle. Only the information required for classification or account analysis should be sent to the external LLM API. Sensitive fields that are not required should be removed or redacted before constructing the prompt.

API credentials must never be included in source code or committed to GitHub. The application uses environment variables for secrets, with `.env` excluded through `.gitignore` and `.env.example` containing only the expected configuration structure.

In a production environment, I would additionally implement PII detection and redaction before external API calls, encrypt data in transit and at rest, apply strict access controls, maintain audit logs, and select an LLM provider with appropriate enterprise data-retention and privacy controls.

For particularly sensitive customers, an internally hosted model could be used so that customer data does not leave the controlled environment.

---

## 4. Scaling

The current solution works well for the provided dataset, but at 10× the ticket volume the main bottlenecks would be repeated LLM calls, knowledge-base loading, and synchronous processing.

The first major bottleneck would likely be LLM API throughput and rate limits because each ticket can require an external model request. Processing thousands of tickets synchronously would increase total processing time and could cause rate-limit failures.

The knowledge base should also not be loaded from disk for every ticket. Instead, it should be loaded once and kept in memory, with a persistent search index for larger datasets.

To scale the system, I would introduce a queue-based architecture. Incoming tickets would be placed into a message queue and processed by multiple workers. Workers could process tickets concurrently while respecting LLM provider rate limits.

I would also cache repeated retrieval results, maintain an indexed knowledge base, batch operations where possible, add structured logging and metrics, and monitor throughput, latency, error rate, queue depth, and LLM usage.

At 10× volume, this architecture would allow horizontal scaling by increasing the number of workers rather than changing the core triage logic.