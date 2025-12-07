import re
from typing import List

class FinancialRetriever:
    def __init__(self, vectorstore):
        # Asegurarse de que vectorstore no sea None
        if vectorstore is None:
            raise ValueError("vectorstore no puede ser None")
        self.vectorstore = vectorstore
        self.financial_keywords = [
            'revenue', 'income', 'profit', 'ebitda', 'margin',
            'cash flow', 'balance sheet', 'financial statement',
            'euro', 'million', 'billion', '%', 'growth',
            'sales', 'net income', 'operating', 'segment',
            'quarter', 'annual', 'forecast', 'guidance'
        ]
    
    def retrieve_financial_chunks(self, query: str, top_k: int = 10) -> List[str]:
        """Recupera chunks relevantes para consultas financieras"""
        if self.vectorstore is None:
            raise ValueError("El vectorstore no está inicializado. Por favor, proporcione un vectorstore válido.")
        
        # Implementar búsqueda híbrida semántica + keyword-based
        docs = self.vectorstore.similarity_search(query, k=top_k * 2)
        
        # Sistema de puntuación
        scored_docs = []
        for doc in docs:
            score = self._calculate_financial_score(doc.page_content)
            scored_docs.append((score, doc))
        
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc.page_content for _, doc in scored_docs[:top_k]]
    
    def _calculate_financial_score(self, text: str) -> int:
        """Calcula puntuación financiera de un chunk"""
        score = 0
        text_lower = text.lower()
        
        for keyword in self.financial_keywords:
            if keyword in text_lower:
                score += 1
        
        if re.search(r'\d+[\.,]\d+', text):
            score += 2
        if re.search(r'[€$\£]', text):
            score += 3
        if re.search(r'\d+\s*%', text):
            score += 2
            
        return score