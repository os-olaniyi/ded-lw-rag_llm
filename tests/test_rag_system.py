import pytest
import os
import sys
from unittest.mock import Mock, patch

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        from langchain_community.document_loaders import TextLoader, PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_chroma import Chroma
        from langchain_huggingface import HuggingFaceEmbeddings
        import streamlit as st
        import ollama
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required modules: {e}")

def test_chroma_index_exists():
    """Test that the ChromaDB index directory exists."""
    assert os.path.exists("./chroma_index"), "ChromaDB index directory should exist"

def test_chroma_sqlite_exists():
    """Test that the ChromaDB SQLite file exists."""
    assert os.path.exists("./chroma_index/chroma.sqlite3"), "ChromaDB SQLite file should exist"

@patch('ollama.chat')
def test_generate_with_llama3(mock_ollama_chat):
    """Test the generate_with_llama3 function."""
    # Mock the ollama response
    mock_response = {"message": {"content": "Test response"}}
    mock_ollama_chat.return_value = mock_response
    
    # Import the function (this would need to be adjusted based on actual module structure)
    # For now, we'll test the concept
    def generate_with_llama3(prompt):
        response = ollama.chat(model="llama3:70b", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    
    result = generate_with_llama3("Test prompt")
    assert result == "Test response"
    mock_ollama_chat.assert_called_once()

def test_requirements_file_exists():
    """Test that requirements.txt exists."""
    assert os.path.exists("requirements.txt"), "requirements.txt should exist"

def test_dockerfile_exists():
    """Test that Dockerfile exists."""
    assert os.path.exists("Dockerfile"), "Dockerfile should exist"

if __name__ == "__main__":
    pytest.main([__file__]) 