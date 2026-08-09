from app.llm_client import create_llm_client


client = create_llm_client()

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "What is RAG in one sentence?"
        }
    ]
)

print(response.choices[0].message.content)