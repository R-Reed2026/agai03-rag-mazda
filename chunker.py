import os
import tiktoken

def load_text_files(folder="data/txt"):
    docs = {}
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                docs[filename] = f.read()
    return docs

def chunk_text(text, max_tokens=400, overlap=50):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + max_tokens
        chunk = enc.decode(tokens[start:end])
        chunks.append(chunk)
        start += max_tokens - overlap

    return chunks

def chunk_all(folder="data/txt", out_folder="data/chunks"):
    os.makedirs(out_folder, exist_ok=True)
    docs = load_text_files(folder)

    for name, text in docs.items():
        chunks = chunk_text(text)
        out_path = os.path.join(out_folder, name.replace(".txt", "_chunks.txt"))

        with open(out_path, "w", encoding="utf-8") as f:
            for i, chunk in enumerate(chunks):
                f.write(f"### CHUNK {i}\n{chunk}\n\n")

        print(f"Chunked {name} → {len(chunks)} chunks")

if __name__ == "__main__":
    chunk_all()
