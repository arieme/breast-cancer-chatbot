"""
CLASSE MÈRE RAG - Tous les composants interchangeables
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from core.config import RAGConfig, CURRENT_CONFIG

class BaseRAG(ABC):
    def __init__(self, config: RAGConfig = CURRENT_CONFIG):
        self.config = config
        self.vector_store = None
        self.embeddings = None
        self.loader = None
        self.generator = None
        
    def setup(self):
        """Setup modulaire - charge les composants configurés"""
        self._setup_embeddings()
        self._setup_loader()
        self._setup_generator()
        self._load_data()
    
    def _setup_embeddings(self):
        from langchain_community.embeddings import HuggingFaceEmbeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.config.embedding_model
        )
    
    def _setup_loader(self):
        """Charge le loader configuré"""
        loader_map = {
            "pdf": "loaders.pdf_loader.PDFLoader",
            #"text": "loaders.text_loader.TextLoader",
            "graph": "loaders.graph_loader.GraphLoader"  
        }
        
        if self.config.loader_type in loader_map:
            module_path, class_name = loader_map[self.config.loader_type].rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            loader_class = getattr(module, class_name)
            self.loader = loader_class(self.config.data_path)
        else:
            raise ValueError(f"Loader non supporté: {self.config.loader_type}")
    
    def _setup_generator(self):
        """Charge le générateur """
        generator_map = {
            "ollama": "generators.ollama_generator.OllamaGenerator",
            
        }
        
        if self.config.generator_type in generator_map:
            module_path, class_name = generator_map[self.config.generator_type].rsplit('.', 1)
            module = __import__(module_path, fromlist=[class_name])
            generator_class = getattr(module, class_name)
            self.generator = generator_class()
        else:
            raise ValueError(f"Générateur non supporté: {self.config.generator_type}")
    
    def _load_data(self):
        """Charge les données via le loader configuré"""
        documents = self.loader.load_documents()
        
        if documents:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            from langchain_community.vectorstores import Chroma
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap
            )
            chunks = text_splitter.split_documents(documents)
            
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory="sprint-1/chroma_db"
            )
            print(f"✅ Données chargées: {len(chunks)} chunks")
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Pose une question - RAG complet modulaire"""
        if not self.vector_store:
            return {"error": "Aucune donnée chargée"}
        
        # 1. RETRIEVAL avec le vector store
        relevant_docs = self.vector_store.similarity_search(
            question, 
            k=self.config.similarity_top_k
        )
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # 2. GENERATION 
        response = self.generator.generate_response(question, context)
        
        return {
            "question": question,
            "response": response,
            "sources": list(set([doc.metadata.get('source', 'Inconnu') for doc in relevant_docs])),
            "context_used": len(relevant_docs),
            "loader": self.config.loader_type,
            "generator": self.config.generator_type
        }