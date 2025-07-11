import streamlit as st
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import ollama
from PIL import Image

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import re
import sqlite3
import hashlib
from concurrent.futures import ThreadPoolExecutor

# === Constants ===
DB_FILE = "upload_hashes.db"
TABLE_NAME = "file_hashes"
CHROMA_DIR = "./chroma_index"
MODEL_NAME = "all-MiniLM-L12-v2"

# === Streamlit Config ===
logo = Image.open("LOGO3b.png")
st.set_page_config(page_title = "LMD RAG Assistant", layout = "wide", page_icon = logo)

# === Sidebar ===
st.sidebar.image(logo, use_container_width = True)
st.sidebar.markdown("### 🧠 LMD RAG Assistant")
st.sidebar.markdown("Get answers from academic documents on Laser Metal Deposition using Retrieval-Augmented Generation and LLaMA 3.")

# === CSS Styling ===
st.markdown("""
    <style>
        .big-font { font-size: 26px !important; font-weight: 600; color: #4CAF50; }
        .context-box {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 8px;
            border-left: 6px solid #4CAF50;
            font-family: monospace;
            white-space: pre-wrap;
        }
        .footer {
            font-size: 13px;
            color: #777;
            margin-top: 40px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# === SQLite DB Functions ===
def init_db():
    conn = sqlite3.connect(DB_FILE)
    with conn:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                hash TEXT PRIMARY KEY,
                filename TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    return conn

def compute_file_hash(file_bytes):
    return hashlib.sha256(file_bytes).hexdigest()

def hash_exists(conn, file_hash):
    cur = conn.cursor()
    cur.execute(f"SELECT 1 FROM {TABLE_NAME} WHERE hash = ?", (file_hash,))
    return cur.fetchone() is not None

def store_hash(conn, file_hash, filename):
    with conn:
        conn.execute(f"INSERT INTO {TABLE_NAME} (hash, filename) VALUES (?, ?)", (file_hash, filename))

conn = init_db()

# === Cached Resources ===
@st.cache_resource
def load_embedding_model():
    return HuggingFaceEmbeddings(model_name = MODEL_NAME)

@st.cache_resource
def load_chroma_db():
    return Chroma(
        persist_directory=CHROMA_DIR,
        collection_name="lmd_knowledge",
        embedding_function=load_embedding_model()
    )

db = load_chroma_db()
if db:
    st.sidebar.success("✅ Knowledge base ready")

# === PDF Processing Functions ===
def clean_citations(text: str) -> str:
    text = re.sub(r'\[\d+(,\s?\d+)*\]', '', text)
    text = re.sub(r'\([A-Za-z]+ et al\.,? \d{4}\)', '', text)
    text = re.sub(r'doi:\s?\S+', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def clean_and_tag_page(page, source_name):
    page.page_content = clean_citations(page.page_content)
    page.metadata["source"] = source_name
    return page

# === Upload Handling ===
uploaded_file = st.sidebar.file_uploader("📤 Upload PDF", type=["pdf"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    file_hash = compute_file_hash(file_bytes)

    if hash_exists(conn, file_hash):
        st.sidebar.warning("⚠️ This file has already been uploaded based on content.")
    else:
        st.sidebar.info("⏳ Processing uploaded PDF...")

        with tempfile.NamedTemporaryFile(delete = False, suffix = ".pdf") as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        loader = PyPDFLoader(tmp_path)
        pages = loader.load()

        with ThreadPoolExecutor() as executor:
            pages = list(executor.map(lambda p: clean_and_tag_page(p, uploaded_file.name), pages))

        splitter = RecursiveCharacterTextSplitter(chunk_size = 800, chunk_overlap = 100)
        chunks = splitter.split_documents(pages)

        db.add_documents(chunks)
        store_hash(conn, file_hash, uploaded_file.name)

        st.sidebar.success(f"✅ Added {len(chunks)} chunks from {uploaded_file.name}")

# === Query Section ===
def highlight_keywords(text):
    keywords = ["LMD", "deposition", "alloy", "substrate", "powder", "laser", "cladding", "repair", "microstructure"]
    for kw in keywords:
        pattern = r'(?i)\\b' + re.escape(kw) + r'\\b'
        text = re.sub(pattern, r"<span style='background-color:#FFEB3B'>\\g<0></span>", text)
    return text

def generate_with_llama3(prompt):
    response = ollama.chat(model = "llama3", messages = [{"role": "user", "content": prompt}])
    return response["message"]["content"]

def rag_query(query):
    results = db.similarity_search(query, k = 3)
    context = "\n\n".join([f"[{doc.metadata.get('source', 'Unknown')}] {doc.page_content}" for doc in results])
    prompt = f"""You are an expert in Laser Metal Deposition Process and Transformer Architectures. Based on the context below, answer the question:

Context:
{context}

Question:
{query}

Answer:"""
    answer = generate_with_llama3(prompt)
    return answer, context

# === Main UI ===
st.markdown('<div class="big-font">🔍 Ask a question about Laser Metal Deposition</div>', unsafe_allow_html=True)
user_query = st.text_input("Enter your question")

if user_query:
    with st.spinner("Reasoning..."):
        answer, context = rag_query(user_query)

        st.subheader("📘 Answer")
        st.markdown(highlight_keywords(answer), unsafe_allow_html = True)

        with st.expander("🔎 Supporting Context"):
            st.markdown(f'<div class="context-box">{context}</div>', unsafe_allow_html = True)

        if "history" not in st.session_state:
            st.session_state.history = []

        st.session_state.history.append({"question": user_query, "answer": answer})

        st.markdown("#### ✅ Rate this Answer:")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("👍 Helpful"):
                st.success("Thanks for your feedback!")
        with col2:
            if st.button("👎 Not Helpful"):
                st.warning("We'll improve this in future.")

if "history" in st.session_state and st.session_state.history:
    st.markdown("---")
    st.markdown("### 🧾 Conversation History")
    for i, entry in enumerate(reversed(st.session_state.history[-5:]), 1):
        st.markdown(f"**{i}. Q:** {entry['question']}")
        st.markdown(f"**A:** {highlight_keywords(entry['answer'])}", unsafe_allow_html = True)

# === Footer ===
st.markdown("""
<div class="footer">
Built with ❤️ by Fourier · Powered by Streamlit, LangChain, and LLaMA 3
</div>
""", unsafe_allow_html = True)
