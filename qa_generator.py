import os
import json
import csv
import requests

# -----------------------------
# CONFIG — CHANGE IF NEEDED
# -----------------------------
LLM_API_URL = "http://localhost:11434/v1/chat/completions"  # Ollama
MODEL_NAME = "llama3"
DATA_FOLDER = "data/txt"
OUTPUT_CSV = "qa_dataset.csv"
OUTPUT_JSON = "qa_dataset.json"
NUM_QA_PER_FILE = 20  # Increase to 30–40 if you want 200+ total
# -----------------------------

def call_llm(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(LLM_API_URL, json=payload)
    data = response.json()
    return data["choices"][0]["message"]["content"]

def generate_qa_from_text(text, source_page, count=20):
    prompt = f"""
Generate {count} high-quality question-answer pairs based ONLY on the text below.
Each Q/A must be factual, specific, and grounded in the content.

Return the output in JSON list format:
[
  {{"question": "...", "answer": "...", "source_page": "..."}},
  ...
]

TEXT:
{text}
"""

    response = call_llm(prompt)

    try:
        qa_list = json.loads(response)
        return qa_list
    except:
        print("LLM returned invalid JSON. Skipping this file.")
        return []

def main():
    all_qa = []

    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_FOLDER, filename)
            print(f"Processing {filename}...")

            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

            qa_pairs = generate_qa_from_text(text, filename, NUM_QA_PER_FILE)
            all_qa.extend(qa_pairs)

    # Save JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_qa, f, indent=4)

    # Save CSV
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["question", "answer", "source_page"])
        for qa in all_qa:
            writer.writerow([qa["question"], qa["answer"], qa["source_page"]])

    print(f"\nGenerated {len(all_qa)} Q/A pairs.")
    print(f"Saved to {OUTPUT_CSV} and {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
