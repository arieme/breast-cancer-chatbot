import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama

class VectorStore:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.vector_store = None
        self.llm = Ollama(model="llama3:8b")  # Change to your local model
        
    def load_documents(self, file_path):
        """Load and process PDF documents"""
        try:
            # Load PDF
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            # Split text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            
            # Create vector store
            self.vector_store = Chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            
            return True
            
        except Exception as e:
            print(f"Error loading documents: {e}")
            return False
    
    def ask_question(self, question):
        """Ask a question and get answer using RAG"""
        if self.vector_store is None:
            return "No documents loaded. Please upload documents first."
        
        # Search for relevant documents
        docs = self.vector_store.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Create prompt
        prompt = f"""
        You are a medical assistant specialized in breast cancer. 
        Answer the question based ONLY on the following context.
        If you don't know the answer, say you don't know.
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        # Generate answer
        try:
            answer = self.llm.invoke(prompt)
            return answer
        except Exception as e:
            return f"Error generating answer: {e}"
    
    def is_ready(self):
        """Check if vector store is ready"""
        return self.vector_store is not None