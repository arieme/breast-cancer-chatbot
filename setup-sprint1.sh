#!/bin/bash

echo "🚀 Setting up Sprint 1 structure..."

# Create sprint directories
mkdir -p sprint-1/{src,tests,docs,data,reports}
mkdir -p sprint-1/src/{core,rag,interfaces}
mkdir -p sprint-1/data/{knowledge_base,test_cases}
mkdir -p shared-resources

# Create initial files
touch sprint-1/README.md
touch sprint-1/requirements.txt
touch sprint-1/src/main.py
touch sprint-1/src/__init__.py

# Create __init__.py files for Python packages
touch sprint-1/src/core/__init__.py
touch sprint-1/src/rag/__init__.py
touch sprint-1/src/interfaces/__init__.py

# Create basic documentation
echo "# Sprint 1: Basic RAG System" > sprint-1/README.md
echo "# Breast Cancer Chatbot - Sprint 1" > sprint-1/docs/requirements.md

echo "✅ Sprint 1 structure created!"
echo "📁 Folders created:"
find sprint-1 -type d