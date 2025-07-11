import pytest
import os
import sys
import tempfile
import sqlite3
import hashlib
from unittest.mock import Mock, patch

# Add the parent directory to the path to import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_enhanced_imports():
    """Test that enhanced RAG modules can be imported."""
    try:
        sys.path.append('RAG_LLAMAv2')
        from rag_llama_deploy_1_1av import (
            init_db, compute_file_hash, hash_exists, store_hash,
            clean_citations, highlight_keywords, generate_with_llama3, rag_query
        )
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import enhanced RAG modules: {e}")

def test_database_initialization():
    """Test SQLite database initialization."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        sys.path.append('RAG_LLAMAv2')
        from rag_llama_deploy_1_1av import init_db
        
        conn = init_db()
        assert conn is not None
        
        # Check if table exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file_hashes'")
        result = cursor.fetchone()
        assert result is not None
        
        conn.close()
    finally:
        os.unlink(db_path)

def test_file_hash_computation():
    """Test file hash computation functionality."""
    sys.path.append('RAG_LLAMAv2')
    from rag_llama_deploy_1_1av import compute_file_hash
    
    test_content = b"test file content for hashing"
    expected_hash = hashlib.sha256(test_content).hexdigest()
    
    computed_hash = compute_file_hash(test_content)
    assert computed_hash == expected_hash
    assert len(computed_hash) == 64  # SHA256 hash length

def test_hash_storage_and_retrieval():
    """Test hash storage and retrieval functionality."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        sys.path.append('RAG_LLAMAv2')
        from rag_llama_deploy_1_1av import init_db, compute_file_hash, hash_exists, store_hash
        
        conn = init_db()
        
        # Test hash storage
        test_bytes = b"test file for storage"
        file_hash = compute_file_hash(test_bytes)
        filename = "test.pdf"
        
        # Initially should not exist
        assert not hash_exists(conn, file_hash)
        
        # Store the hash
        store_hash(conn, file_hash, filename)
        
        # Now should exist
        assert hash_exists(conn, file_hash)
        
        conn.close()
    finally:
        os.unlink(db_path)

def test_citation_cleaning():
    """Test citation cleaning functionality."""
    sys.path.append('RAG_LLAMAv2')
    from rag_llama_deploy_1_1av import clean_citations
    
    test_text = "This process [1, 2] shows (Smith et al., 2021) doi:10.1234/abc and some text"
    cleaned = clean_citations(test_text)
    
    # Should remove citations
    assert "[1, 2]" not in cleaned
    assert "(Smith et al., 2021)" not in cleaned
    assert "doi:10.1234/abc" not in cleaned
    
    # Should preserve meaningful content
    assert "This process" in cleaned
    assert "shows" in cleaned
    assert "and some text" in cleaned

def test_keyword_highlighting():
    """Test keyword highlighting functionality."""
    sys.path.append('RAG_LLAMAv2')
    from rag_llama_deploy_1_1av import highlight_keywords
    
    test_text = "This LMD process uses laser deposition on alloy substrate with powder."
    highlighted = highlight_keywords(test_text)
    
    # Should highlight LMD keywords
    assert "LMD" in highlighted
    assert "laser" in highlighted
    assert "deposition" in highlighted
    assert "alloy" in highlighted
    assert "substrate" in highlighted
    assert "powder" in highlighted
    
    # Should contain HTML highlighting
    assert "background-color:#FFEB3B" in highlighted

@patch('ollama.chat')
def test_llama3_generation(mock_chat):
    """Test LLaMA3 generation functionality."""
    sys.path.append('RAG_LLAMAv2')
    from rag_llama_deploy_1_1av import generate_with_llama3
    
    # Mock the ollama response
    mock_chat.return_value = {
        "message": {
            "content": "This is a test response from LLaMA3"
        }
    }
    
    prompt = "Test prompt"
    response = generate_with_llama3(prompt)
    
    assert response == "This is a test response from LLaMA3"
    mock_chat.assert_called_once_with(
        model="llama3", 
        messages=[{"role": "user", "content": prompt}]
    )

@patch('ollama.chat')
def test_rag_query_function(mock_chat):
    """Test RAG query functionality."""
    sys.path.append('RAG_LLAMAv2')
    from rag_llama_deploy_1_1av import rag_query
    
    # Mock the ollama response
    mock_chat.return_value = {
        "message": {
            "content": "This is a RAG response"
        }
    }
    
    query = "What is LMD?"
    answer, context = rag_query(query)
    
    assert answer == "This is a RAG response"
    assert isinstance(context, str)
    mock_chat.assert_called_once()

def test_enhanced_features_integration():
    """Test integration of enhanced features."""
    sys.path.append('RAG_LLAMAv2')
    from rag_llama_deploy_1_1av import (
        init_db, compute_file_hash, store_hash, hash_exists,
        clean_citations, highlight_keywords
    )
    
    # Test complete workflow
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    try:
        # Initialize database
        conn = init_db()
        
        # Process a test file
        test_content = b"LMD process [1] with (Smith et al., 2021) laser deposition"
        file_hash = compute_file_hash(test_content)
        
        # Store file hash
        store_hash(conn, file_hash, "test_lmd.pdf")
        
        # Verify storage
        assert hash_exists(conn, file_hash)
        
        # Test citation cleaning
        cleaned_text = clean_citations(test_content.decode())
        assert "[1]" not in cleaned_text
        assert "(Smith et al., 2021)" not in cleaned_text
        
        # Test keyword highlighting
        highlighted = highlight_keywords(cleaned_text)
        assert "background-color:#FFEB3B" in highlighted
        
        conn.close()
        
    finally:
        os.unlink(db_path)

if __name__ == "__main__":
    pytest.main([__file__]) 