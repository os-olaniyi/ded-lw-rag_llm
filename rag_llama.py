
from langchain_community.document_loaders import TextLoader, PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import streamlit as st
import ollama

import os
import re

def clean_citations(text: str) -> str:
    text = re.sub(r'\[\d+(,\s?\d+)*\]', '', text)                                   # e.g., [1], [1, 2]
    text = re.sub(r'\([A-Za-z]+ et al\.,? \d{4}\)', '', text)                       # e.g., (Smith et al., 2021)
    text = re.sub(r'doi:\s?\S+', '', text)                                          # Remove DOIs
    text = re.sub(r'\s?\d+\s?', ' ', text)                                          # Superscript or footnote numbers
    text = re.sub(r'\s{2,}', ' ', text)                                             # Double/triple spaces
    return text.strip()

def load_pdf_documents(folder_path):
    pdf_files = [os.path.join(folder_path, f)  for f in os.listdir(folder_path) if f.endswith(".pdf")]
    all_documents = [ ]

    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        docs = loader.load()

        source_name = os.path.basename(pdf)

         # Apply citation cleaning per page
        for doc in docs:
            doc.page_content = clean_citations(doc.page_content)
            doc.metadata["source"] = source_name 

        all_documents.extend(docs)


    return all_documents


# Clean Chunks
def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)

    return splitter.split_documents(documents = documents)


def store_in_chroma(chunks, persist_dir = "./chroma_index"):
    embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    vector_store = Chroma(
        persist_directory = persist_dir,
        collection_name = "lmd_knowledge",
        embedding_function = embedding_model
    )
    #vector_store.add_documents(chunks)
    #vector_store.persist()
    print(f"Stored {len(chunks)} chunks in ChromaDB")

pdf_dir = "./docs"

pdf_docs = load_pdf_documents(pdf_dir)
print(f"Loaded {len(pdf_docs)} pages from PDFs.")

chunks = chunk_documents(pdf_docs)
print(f"Chunked into {len(chunks)} segments.")

store_in_chroma(chunks = chunks)
print("🎉 ChromaDB knowledge base ready.")

persist_dir = "./chroma_index"

embedding_model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
db = Chroma(
    persist_directory = persist_dir,
    collection_name = "lmd_knowledge",
    embedding_function = embedding_model
)

def generate_with_llama3(prompt):
    response = ollama.chat(model = "llama3", messages = [{"role": "user", "content": prompt}])
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