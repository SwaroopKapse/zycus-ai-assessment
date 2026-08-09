from pathlib import Path


KB_PATH = Path("knowlege-base")


def load_knowledge_base():
    documents = []

    for file_path in KB_PATH.rglob("*.md"):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        documents.append({
            "filename": file_path.name,
            "path": str(file_path),
            "content": content
        })

    return documents


if __name__ == "__main__":
    documents = load_knowledge_base()

    print("Number of documents:", len(documents))

    for document in documents:
        print(document["filename"])