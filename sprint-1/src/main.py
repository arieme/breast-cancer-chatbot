"""
Breast Cancer Chatbot - Sprint 1
Basic RAG System for Medical Information
"""

import os
import streamlit as st
from rag.vector_store import VectorStore

def main():
    st.title("🎗️ Breast Cancer Information Assistant")
    st.write("**Sprint 1**: Basic RAG System")
    
    # Initialize vector store
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = VectorStore()
    
    # Document upload section
    st.sidebar.header("📚 Document Management")
    uploaded_file = st.sidebar.file_uploader(
        "Upload a PDF about breast cancer", 
        type="pdf"
    )
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_document.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Load document into vector store
        st.session_state.vector_store.load_documents("temp_document.pdf")
        st.sidebar.success("✅ Document loaded successfully!")
    
    # Chat interface
    st.header("💬 Ask questions about breast cancer")
    
    question = st.text_input("Your question:")
    
    if question and st.button("Get Answer"):
        if st.session_state.vector_store.is_ready():
            answer = st.session_state.vector_store.ask_question(question)
            st.write("**Answer:**", answer)
        else:
            st.warning("⚠️ Please upload a document first")

if __name__ == "__main__":
    main()