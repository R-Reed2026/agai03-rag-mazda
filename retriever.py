import chromadb
from sentence_transformers import SentenceTransformer

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

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question: ")
        answers = retrieve(q)
        print("\nTop chunks:")
        for a in answers:
            print("—", a[:200], "...\n")
