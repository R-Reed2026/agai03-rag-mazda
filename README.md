# 🚗 Mazda RAG Chatbot  
A Retrieval‑Augmented Generation (RAG) system built using

- Web scraping (Wikipedia pages)
- Text chunking
- Embedding generation (SentenceTransformers)
- Vector database (ChromaDB)
- Local LLM inference (Llama 3 via Ollama)
- Streamlit web interface
- Synthetic QA dataset generation (100–200+ pairs)

This project answers questions about Mazda vehicles, engines, and technologies using grounded context retrieved from scraped documents.

---

## 📁 Project Structure
rag-chatbot/
│
├── data/
│   ├── txt/            # Raw scraped text files
│   ├── chunks/         # Chunked text files
│
├── vectorstore/        # ChromaDB persistent storage
│
├── scraper.py          # Phase 1: Scraping
├── chunker.py          # Phase 1: Chunking
├── embeddings.py       # Phase 2: Embeddings
├── retriever.py        # Phase 3: Retrieval
├── rag.py              # Phase 4: RAG answer generator
├── qa_generator.py     # Phase 2: Synthetic Q/A generation
├── streamlit_app.py    # Phase 5: Streamlit UI
│
├── qa_dataset.csv      # Generated Q/A dataset
├── qa_dataset.json     # Generated Q/A dataset
│
└── README.md


---

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd rag-chatbot

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Start your local LLM (Ollama)

ollama run llama3

###Leave this running in its own terminal.

### 4. Run the Streamlit app
streamlit run streamlit_app.py

###The app will open

http://localhost:8501
