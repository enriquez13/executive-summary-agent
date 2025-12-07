import re
from pathlib import Path
from typing import Optional
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, chunk_size: int = 4000, chunk_overlap: int = 500):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def load_pdf(self, file_path: Path) -> Optional[str]:
        """Carga y extrae texto de un PDF"""
        if not file_path.exists():
            return None
            
        try:
            with pdfplumber.open(file_path) as pdf:
                return "\n\n".join(page.extract_text() for page in pdf.pages)
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return None
    
    def clean_text(self, text: str) -> str:
        """Limpia el texto de encabezados repetitivos"""
        # Implementar lógica de limpieza
        lines = text.split('\n')
        cleaned_lines = []
        
        adidas_header = r'^TO OUR GROUP MANAGEMENT REPORT – GROUP MANAGEMENT REPORT – GROUP MANAGEMENT REPORT – CONSOLIDATED ADDITIONAL$'
        
        for line in lines:
            stripped = line.strip()
            if re.match(adidas_header, stripped):
                continue
            if stripped == "SHAREHOLDERS OUR COMPANY FINANCIAL REVIEW SUSTAINABILITY STATEMENT FINANCIAL STATEMENTS INFORMATION":
                continue
            if len(stripped) > 20:
                cleaned_lines.append(stripped)
                
        return '\n'.join(cleaned_lines)
    
    def chunk_text(self, text: str) -> list[str]:
        """Divide el texto en chunks"""
        if not text:
            return []
            
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.split_text(text)