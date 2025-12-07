import os
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class SummaryGenerator:
    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = self.initialize_groq_llm()
        self.chain = self.create_chain()
    
    def initialize_groq_llm(self, model_name: str = "llama-3.3-70b-versatile"):
        """Initialize the Groq client."""
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("ERROR: GROQ_API_KEY not found.")
        
        try:
            llm = ChatGroq(
                groq_api_key=api_key,
                model_name=model_name,
                temperature=0.2,
                max_tokens=1500
            )
            return llm
        except Exception as e:
            print(f"[WARNING] Error with model {model_name}: {e}")
            print("[WARNING] Trying alternative model 'mixtral-8x7b-32768'...")
            return ChatGroq(
                groq_api_key=api_key,
                model_name="mixtral-8x7b-32768",
                temperature=0.2,
                max_tokens=1500
            )
    
    def create_chain(self):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are the CFO of a consulting firm, preparing an URGENT executive briefing for the CEO.

ABSOLUTE RULES:
1. Use ONLY the information provided in the context. DO NOT invent data.
2. Focus on specific numerical data: figures in millions/billions, percentages, growth rates.
3. Extract and present the most important data from the financial tables.
4. MANDATORY structure:
   ---
   FINANCIAL EXECUTIVE SUMMARY
   ---
   
   🎯 KEY RESULTS (TOP 5)
   • [Metric 1]: [2024 value] vs [2023 value] ([% change] if available)
   • [Metric 2]: [2024 value] vs [2023 value] ([% change] if available)
   • ... (maximum 5 points)
   
   📊 DETAILED ANALYSIS
   1. Profitability: [Operating profit, net income, margins]
   2. Sales/Revenue: [Revenue, sales, segments]
   3. Efficiency: [Cash flow, working capital, ratios]
   4. Outlook: [Any projections or guidance mentioned]
   
   ⚠️ RISKS/OPPORTUNITIES (maximum 3 of each, only if mentioned in the document)
   • [Risk 1]: [Brief explanation]
   • [Opportunity 1]: [Brief explanation]
   (If no risks/opportunities are mentioned, omit this entire section)
   
   💡 EXECUTIVE RECOMMENDATION (1-2 sentences)

5. ALWAYS include units (€ million, %, etc.).
6. If a section has no data in the context, OMIT IT ENTIRELY (do not write "NOT IDENTIFIED").
7. Use emojis to improve readability.
8. Maximum 400 words.
9. Respond in ENGLISH."""),
            
            ("human", """RAW CONTEXT EXTRACTED FROM THE ANNUAL REPORT:
{context}

--- 
GENERATE THE EXECUTIVE SUMMARY STRICTLY FOLLOWING THE ABOVE RULES.""")
        ])
        
        chain = (
            {"context": RunnablePassthrough()}
            | prompt_template
            | self.llm
            | StrOutputParser()
        )
        return chain
    
    def filter_executive_chunks(self, all_chunks: list[str], min_financial_score: int = 20, max_chunks: int = 5) -> list[str]:
        """
        Filter chunks to keep only those with high executive value.
        """
        scored = []
        
        for i, chunk in enumerate(all_chunks):
            score = 0
            
            # High points for financial tables
            if re.search(r'\d{4}\s+\d{4}\s+\d{4}\s+\d{4}', chunk):  # Table pattern
                score += 50
            
            # Points for financial figures in €
            if re.search(r'€\s*\d+[\.,]\d+', chunk):
                score += 30
                
            # Points for percentages
            if re.search(r'\d+\.?\d*\s*%', chunk):
                score += 20
                
            # Penalize residual headers
            if 'TO OUR GROUP MANAGEMENT REPORT' in chunk:
                score -= 40
                
            scored.append((score, chunk))
        
        # Order by score and take the best
        scored.sort(key=lambda x: x[0], reverse=True)
        best_chunks = [chunk for score, chunk in scored if score >= min_financial_score][:max_chunks]
        
        print(f"[FILTER] Top 3 scores: {[s for s, _ in scored[:3]]}")
        print(f"[FILTER] {len(best_chunks)}/{len(all_chunks)} chunks selected")
        
        return best_chunks
    
    def process_document(self, pdf_path: str) -> str:
        """Procesa un documento PDF y genera un resumen ejecutivo"""
        # Nota: En esta refactorización, asumimos que el vectorstore ya está creado y pasado al retriever.
        # Por lo tanto, no necesitamos cargar el PDF aquí nuevamente.
        # Sin embargo, si necesitas cargar el PDF en este punto, deberás ajustar.
        
        # En el flujo original, el vectorstore se crea en main y se pasa al retriever.
        # Luego, aquí solo usamos el retriever para obtener los chunks financieros.
        financial_query = """
        Financial results 2024 vs 2023: 
        Operating profit, Revenue, Sales, Net income, EBITDA, 
        Gross margin, Operating margin, Cash flow, 
        Segment performance (Footwear, Apparel, Accessories),
        Regional results (North America, EMEA, Asia-Pacific),
        Financial guidance 2025,
        Risks mentioned, Opportunities mentioned.
        """
        
        # 1. Recuperar chunks financieros
        print("[INFO] Searching for specific financial content...")
        financial_chunks = self.retriever.retrieve_financial_chunks(financial_query, top_k=10)
        print(f"[INFO] Initially retrieved {len(financial_chunks)} financial chunks.")
        
        # 2. Filtrar por valor ejecutivo
        print("\n[INFO] Filtering chunks by executive value...")
        executive_chunks = self.filter_executive_chunks(financial_chunks, min_financial_score=20, max_chunks=5)
        
        if not executive_chunks:
            print("[WARNING] Filter too strict. Using top 3 chunks.")
            executive_chunks = financial_chunks[:3]
        
        print(f"[INFO] Final executive chunks: {len(executive_chunks)}")
        
        # 3. Generar resumen ejecutivo
        print("\n[INFO] Generating executive summary...")
        context = "\n\n---\n\n".join(executive_chunks)
        summary = self.chain.invoke(context)
        
        return summary