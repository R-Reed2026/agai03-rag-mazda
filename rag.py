import chromadb
from sentence_transformers import SentenceTransformer
import requests
import json

# LLM CONFIG (Ollama)
LLM_API_URL = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "llama3"

def get_retriever():
    client = chromadb.PersistentClient(path="vectorstore")
    collection = client.get_or_create_collection("mazda_rag")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return collection, model

def retrieve(query, n_results=5):
    collection, model = get_retriever()
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0]

def generate_answer(question, context_chunks):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a helpful assistant answering questions using ONLY the context below.

CONTEXT:
{context}

QUESTION:
{question}

If the answer is not in the context, say "The answer is not in the provided documents."
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(LLM_API_URL, json=payload)
    data = response.json()

    return data["choices"][0]["message"]["content"]

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question: ")
        chunks = retrieve(q)
        answer = generate_answer(q, chunks)
        print("\nANSWER:\n", answer, "\n")
