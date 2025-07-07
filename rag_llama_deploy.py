from langchain_community.document_loaders import TextLoader, PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import streamlit as st
import ollama

import os
import re


persist_dir = "./chroma_index"

embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
db = Chroma(
    persist_directory = persist_dir,
    collection_name = "lmd_knowledge",
    embedding_function = embedding_model
)

if db:
    print("🎉 ChromaDB knowledge base ready.")

def generate_with_llama3(prompt):
    response = ollama.chat(model = "llama3:70b", messages = [{"role": "user", "content": prompt}])
    return response["message"]["content"]


def rag_query(query):
    results = db.similarity_search(query, k = 3)
    context = "\n\n".join([f"[{doc.metadata.get('source')}] {doc.page_content}" for doc in results])
    prompt = f"""You are an expert in Laser Metal Deposition Process and Transformer Algorithm and Architecture. Based on the context below, answer the question:

Context:
{context}

Question:
{query}

Answer:"""
    answer = generate_with_llama3(prompt)
    return answer, context

st.set_page_config(page_title = "LMD RAG Assistance", layout = "wide")

st.title("🔍 RAG Question Answering System")
st.markdown("Ask any question related to Laser Metal Deposition...")

user_query = st.text_input("Enter your question")


if user_query:
    with st.spinner("Reasoning....."):
        answer, context = rag_query(user_query)

        st.subheader("📘 Answer")
        st.write(answer)

        with st.expander("🔎 Supporting Context from Knowledge Base"):
            st.markdown(f"```\n{context}\n```")