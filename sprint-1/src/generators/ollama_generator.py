"""
GÉNÉRATEUR OLLAMA - Modulaire
"""
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser

class OllamaGenerator:
    def __init__(self, model: str = "llama2"):
        try:
            self.llm = Ollama(model=model)
            self.available = True
        except:
            self.available = False
    
    def generate_response(self, question: str, context: str) -> str:
        if not self.available:
            return f"📚 Contexte pertinent:\n\n{context}"
        
        prompt = PromptTemplate(
            template="""Tu es un expert médical. Réponds en français en utilisant UNIQUEMENT ce contexte:

CONTEXTE:
{context}

QUESTION: {question}

Si l'information n'est pas dans le contexte, dis-le.

RÉPONSE:""",
            input_variables=["context", "question"]
        )
        
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({"context": context, "question": question})