"""
CHARGEUR PDF - Modulaire
"""
import os
from langchain_community.document_loaders import PyPDFLoader

class PDFLoader:
    def __init__(self, data_path: str):
        self.data_path = data_path
    
    def load_documents(self):
        """Charge tous les PDFs du dossier"""
        documents = []
        
        if not os.path.exists(self.data_path):
            print(f"❌ Dossier {self.data_path} non trouvé")
            return documents
        
        for pdf_file in os.listdir(self.data_path):
            if pdf_file.endswith(".pdf"):
                pdf_path = os.path.join(self.data_path, pdf_file)
                try:
                    loader = PyPDFLoader(pdf_path)
                    docs = loader.load()
                    documents.extend(docs)
                    print(f"✅ PDF chargé: {pdf_file} ({len(docs)} pages)")
                except Exception as e:
                    print(f"❌ Erreur {pdf_file}: {e}")
        
        return documents