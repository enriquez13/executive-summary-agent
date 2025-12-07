import os
import re
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
import pdfplumber

class VectorStoreManager:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.embeddings = SentenceTransformerEmbeddings(model_name=model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=500,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def load_pdf(self, file_path: str) -> str:
        """Load a PDF and extract its text using pdfplumber."""
        if not os.path.exists(file_path):
            return ""
        
        print(f"[INFO] Loading PDF with pdfplumber: {file_path}")
        extracted_text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text() + "\n\n"
        except Exception as e:
            print(f"[ERROR] Failed to process PDF: {e}")
            return ""
        
        return extracted_text.strip()
    
    def clean_text(self, text: str) -> str:
        """Improved cleaning for headers."""
        if not text:
            return ""
        
        lines = text.split('\n')
        cleaned_lines = []
        
        # Specific pattern for repetitive Adidas headers
        adidas_header_pattern = r'^TO OUR GROUP MANAGEMENT REPORT – GROUP MANAGEMENT REPORT – GROUP MANAGEMENT REPORT – CONSOLIDATED ADDITIONAL$'
        
        for line in lines:
            stripped = line.strip()
            
            # 1. Remove the exact repetitive header
            if re.match(adidas_header_pattern, stripped):
                continue
                
            # 2. Remove the section line (appears below the header)
            if stripped == "SHAREHOLDERS OUR COMPANY FINANCIAL REVIEW SUSTAINABILITY STATEMENT FINANCIAL STATEMENTS INFORMATION":
                continue
                
            # 3. Remove single numeric lines
            if re.fullmatch(r'(\d\s+)+\d', stripped):
                continue
                
            # 4. Keep lines with substantial content
            if len(stripped) > 20:
                cleaned_lines.append(stripped)
        
        result = '\n'.join(cleaned_lines)
        return result
    
    def chunk_text(self, text: str) -> list[str]:
        """Divide the text into overlapping fragments."""
        if not text:
            return []
        
        print(f"[INFO] Dividing text into chunks (size=4000, overlap=500)...")
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def create_vectorstore(self, chunks: list[str]) -> FAISS:
        """Create embeddings and build a FAISS index."""
        if not chunks:
            raise ValueError("No chunks provided to create vectorstore")
        
        print(f"[INFO] Creating embeddings and FAISS index for {len(chunks)} chunks...")
        vectorstore = FAISS.from_texts(
            texts=chunks,
            embedding=self.embeddings
        )
        print(f"[INFO] Vectorstore created with {vectorstore.index.ntotal} vectors.")
        return vectorstore

        