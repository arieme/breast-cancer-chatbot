"""
CONFIGURATION CENTRALE -  ici pour modifier le comportement
"""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class RAGConfig:
    # Chargeurs disponibles
    loader_type: str = "pdf"  # "pdf", "graph", "text"
    data_path: str = "data/pdfs"
    
    # Générateurs disponibles  
    generator_type: str = "ollama"  # "ollama", "simple"
    llm_model: str = "llama2"
    
    # Paramètres RAG
    chunk_size: int = 1000
    chunk_overlap: int = 200
    similarity_top_k: int = 3
    
    # Embeddings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

# Configuration globale - MODIFIEZ ICI POUR CHANGER LE COMPORTEMENT
CURRENT_CONFIG = RAGConfig(
    loader_type="pdf",  # Au lieu de "graph"
    data_path="sprint-1/data/pdfs",
    generator_type="ollama"
)