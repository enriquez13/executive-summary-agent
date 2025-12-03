# 🚀 Executive Summary Agent

**An intelligent RAG system that automatically extracts and summarizes annual financial reports.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-orange.svg)](https://www.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📊 What Problem Does It Solve?

Executives and consultants waste **hours reading 100+ page annual reports** to extract key financial insights. This agent automates that process:

- **Extracts** critical financial information from complex PDFs
- **Analyzes** trends and annual comparisons
- **Generates** structured executive summaries in seconds
- **Focuses** on what really matters: actionable data

## 🎯 Example Results (Adidas Annual Report 2024)

**Actual system performance:**

```text
🎯 KEY RESULTS (TOP 5)
• Net sales: €23.683 billion in 2024 vs. €21.427 billion in 2023 (11% increase)
• Operating profit: €1.337 billion in 2024 vs. €268 million in 2023 (398% increase)
• Operating profit margin: 5.6% in 2024 vs. 1.3% in 2023 (4.4pp increase)
• Dividend per share: €2.00 in 2024 vs. €0.70 in 2023 (186% increase)
• Operating cash flow: €2.91 billion (↑14% vs. 2023)

📊 OUTLOOK FOR 2025
• Net sales: high-single-digit growth
• Projected operating profit: €1.7-1.8 billion
```

## ✨ Key Features

- ## Smart Extraction:    Automatically identifies financial tables, KPIs, and key data
- ## Advanced Cleaning:    Removes repetitive headers, page numbers, and PDF noise
- ## Semantic Search:    Finds relevant content using embeddings + keywords
- ## Value Filterin:    Prioritizes chunks with concrete numerical and financial data
- ## Structured Generation:    Produces summaries with professional executive formatting
- ## Fast Processing:    3-5 minutes for reports of 100+ pages

```text
graph LR
    A[PDF Input] --> B[Extract Text<br/>pdfplumber]
    B --> C[Clean Text<br/>regex patterns]
    C --> D[Chunk Text<br/>RecursiveTextSplitter]
    D --> E[Create Embeddings<br/>SentenceTransformer]
    E --> F[Vector Store<br/>FAISS]
    F --> G[Retrieve Financial Chunks<br/>Hybrid Search]
    G --> H[Filter Executive Content<br/>Scoring System]
    H --> I[Generate Summary<br/>LLaMA 3.3 70B via Groq]
    I --> J[Executive Summary Output]
```
📦 Quick Installation
1. Clone the repository
git clone https://github.com/enriquez1/executive-summary-agent.git
cd executive-summary-agent

2. Create a virtual environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Configure Groq API Key
# Windows (PowerShell)
$env:GROQ_API_KEY="your_key_here"

# Linux/Mac
export GROQ_API_KEY="your_key_here"


📁 Project Structure
executive-summary-agent/
│
├── app.ipynb                 # Main flow of the agent
├── requirements.txt          # Dependencies
├── README.md                 
│
├── examples/                 # Examples and outputs
│   ├── adidas_2024_summary.txt
│   └── chunks_ejecutivos.txt
│
├── docs/                    # Documentation
│   └── architecture.md
│
└── test.ipynb

## 🛠️ Technologies Used
LangChain    LLM orchestration framework    0.2+
Sentence Transformers   - Embeddings for semantic search  -  all-MiniLM-L6-v2
FAISS -   Vector database for fast retrieval  -  CPU
Groq API  -  High-speed LLM (Llama 3.3 70B)   - LLaMA 3.3
pdfplumber -   Advanced PDF extraction -   0.10+
Python  -  Main language  -  3.9+

🎯 Use Cases in Consulting
1. Accelerated Due Diligence
Problem: Analyzing 10 annual reports for a merger takes 40+ hours.
Solution: This agent does it in 30-50 minutes, extracting key financial KPIs.

2. Competitive Benchmarking
Problem: Manually comparing results from 5 competitors.
Solution: Process all reports and generate an automatic comparison table.

3. Weekly Executive Update
Problem: Preparing summaries of earnings calls and reports for leadership.
Solution: Automated pipeline that processes documents and sends summaries.

🔧 Customization
Adapt to Other Domains
# Cambiar la consulta para análisis ESG
esg_query = """
ESG metrics: carbon emissions, diversity ratios, 
water usage, board diversity, sustainability targets
"""

# Change the prompt for market analysis
market_prompt = “”"
You are a market analyst. Extract:
1. Market share by region
2. Consumer trends
3. Competitive analysis

"""
## 📞 Contact
Alejandro Enríquez

LinkedIn: https://www.linkedin.com/in/alejandro-enríquez-3611931b3/

Project: https://github.com/enriquez13/executive-summary-agent
