# Executive Summary Agent

## What does it do?
It automatically extracts and summarizes annual financial reports using RAG.

## Example result (Adidas 2024):
- Sales: €23.683 billion (↑11% vs. 2023)
- Operating Profit: €1.337 billion (↑398%)
- Operating Margin: 5.6% (vs. 1.3% in 2023)

## Technologies:
- PDF Processing: pdfplumber
- Embeddings: SentenceTransformer (all-MiniLM-L6-v2)
- Vectorstore: FAISS
- LLM: Groq (Llama 3.3 70B)
- Framework: LangChain

## How to run:
pip install -r requirements.txt
python app.py