import streamlit as st
import chromadb
from sentence_transformers import SentenceTransformer
import requests

# LLM CONFIG (Ollama)
LLM_API_URL = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "llama3"

@st.cache_resource
def load_retriever():
    client = chromadb.PersistentClient(path="vectorstore")
    collection = client.get_or_create_collection("mazda_rag")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return collection, model

def retrieve(query, n_results=5):
    collection, model = load_retriever()
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

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🚗 Mazda RAG Chatbot")
st.write("Ask any question about Mazda cars, engines, or technology.")

user_question = st.text_input("Your question:")

if st.button("Ask"):
    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving information..."):
            chunks = retrieve(user_question)

        with st.spinner("Generating answer..."):
            answer = generate_answer(user_question, chunks)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Retrieved Chunks")
        for c in chunks:
            st.code(c[:500] + "...")
