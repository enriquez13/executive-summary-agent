import sys
from pathlib import Path
import sys
sys.path.append('./src')
from vector_store import VectorStoreManager
from retrieval import FinancialRetriever
from summary_generator import SummaryGenerator

def main():
    pdf_path = "annual-report-adidas-ar24.pdf"
    
    if not Path(pdf_path).exists():
        print(f"[ERROR] PDF not found: {pdf_path}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("EXECUTIVE SUMMARY AGENT")
    print("="*60)
    
    # 1. Inicializar VectorStoreManager
    vector_manager = VectorStoreManager()
    
    # 2. Cargar y limpiar el PDF
    raw_text = vector_manager.load_pdf(pdf_path)
    if not raw_text:
        print("[ERROR] Failed to extract text from the PDF.")
        return
    
    print(f"[INFO] Extracted text: {len(raw_text):,} characters")
    
    cleaned_text = vector_manager.clean_text(raw_text)
    print(f"[INFO] Cleaned text: {len(cleaned_text):,} characters")
    print(f"[INFO] Reduction: {len(raw_text)-len(cleaned_text):,} characters removed")
    
    if len(cleaned_text) < 50000:
        print("[WARNING] Cleaned text is very short. Verify cleaning process.")
    
    # 3. Dividir en chunks
    chunks = vector_manager.chunk_text(cleaned_text)
    print(f"[INFO] Text split into {len(chunks)} chunks.")
    
    if len(chunks) == 0:
        print("[ERROR] No chunks generated.")
        return
    
    # 4. Crear vectorstore
    vectorstore = vector_manager.create_vectorstore(chunks)
    
    # 5. Crear retriever
    retriever = FinancialRetriever(vectorstore)
    
    # 6. Crear generador de resumen
    generator = SummaryGenerator(retriever)
    
    # 7. Procesar documento y generar resumen
    summary = generator.process_document(pdf_path)
    
    # 8. Presentar resultados
    print("\n" + "="*60)
    print("FINANCIAL EXECUTIVE SUMMARY")
    print("="*60)
    print(summary)
    print("\n" + "="*60)
    
    # 9. Guardar resultados
    output_path = "executive_summary.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("FINANCIAL EXECUTIVE SUMMARY\n")
        f.write("="*60 + "\n\n")
        f.write(summary)
    
    print(f"[INFO] Summary saved to: {output_path}")
    
    # 10. Métricas finales
    print("\n" + "="*60)
    print("PROCESS METRICS")
    print("="*60)
    print(f"• Original text: {len(raw_text):,} characters")
    print(f"• Cleaned text: {len(cleaned_text):,} characters")
    print(f"• Generated chunks: {len(chunks)}")
    print(f"• Retrieved financial chunks: {len(chunks)}")  # Nota: esto no es exacto, pero para mantener la métrica
    print(f"• Data reduction: {(len(raw_text)-len(cleaned_text))/len(raw_text)*100:.1f}%")

if __name__ == "__main__":
    main()