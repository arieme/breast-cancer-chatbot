"""
RAG MODULAIRE 
"""
from core.base_rag import BaseRAG
from core.config import CURRENT_CONFIG, RAGConfig

def main():
    print(" RAG MODULAIRE - Cancer du Sein")
    print("=" * 50)
    
   
    
    rag_default = BaseRAG(CURRENT_CONFIG)
    rag_default.setup()
    
   
    
    
    test_questions = [
        "Quels sont les facteurs de risque?",
        "Quels sont les symptômes du cancer du sein?"
    ]
    
    for question in test_questions:
        print(f"\n Question: {question}")
        
        print(f"\n RAG (PDF+Ollama):")
        result1 = rag_default.ask_question(question)
        print(f"   Réponse: {result1['response']}...")
        print(f"   Loader: {result1['loader']}, Generator: {result1['generator']}")
        
        
        # 2. WITHOUT RAG (LLM only - its base knowledge)
        print("\n WITHOUT RAG (LLM base knowledge):")
        # Direct LLM call without context
        direct_response = rag_default.generator.llm.invoke(question)
        print(f"   {direct_response}")
    
        
        
        print("-" * 50)

if __name__ == "__main__":
    main()