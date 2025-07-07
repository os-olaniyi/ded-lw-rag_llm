# RAG LLM - Laser Metal Deposition Knowledge Base

A Retrieval-Augmented Generation (RAG) system for Laser Metal Deposition (LMD) knowledge using Llama3 and ChromaDB.

## 🚀 Features

- **RAG System**: Question-answering system based on LMD knowledge base
- **Vector Database**: ChromaDB for efficient document retrieval
- **LLM Integration**: Ollama with Llama3:70b model
- **Web Interface**: Streamlit-based user interface
- **CI/CD Pipeline**: Automated testing and deployment

## 📋 Prerequisites

- Python 3.9+
- Ollama (with Llama3:70b model installed)
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ded-lw-rag_llm
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**
   ```bash
   # Install Ollama (follow instructions at https://ollama.ai)
   ollama pull llama3:70b
   ```

4. **Prepare knowledge base** (if needed)
   ```bash
   # Place your PDF documents in a 'docs' folder
   mkdir docs
   # Add your PDF files to the docs folder
   python rag_llama.py
   ```

## 🚀 Usage

### Development Mode
```bash
streamlit run rag_llama.py
```

### Production Mode
```bash
streamlit run rag_llama_deploy.py
```

### Docker Deployment
```bash
# Build the Docker image
docker build -t rag-llm .

# Run the container
docker run -p 8501:8501 rag-llm
```

## 🧪 Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=./ --cov-report=html
```

## 🔧 CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow that:

### Triggers
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### Jobs

1. **Test Job**
   - Runs on multiple Python versions (3.9, 3.10, 3.11)
   - Installs dependencies with caching
   - Runs linting (flake8, black, isort)
   - Executes tests with coverage reporting
   - Uploads coverage to Codecov

2. **Build Job** (main branch only)
   - Creates deployment package
   - Uploads build artifacts

3. **Security Scan**
   - Runs Bandit security analysis
   - Uploads security scan results

4. **Docker Build** (main branch only)
   - Builds Docker image with caching
   - Prepares for deployment

### Workflow Files
- `.github/workflows/ci-cd.yml` - Main CI/CD pipeline
- `Dockerfile` - Container configuration
- `.dockerignore` - Docker build exclusions
- `pyproject.toml` - Tool configurations
- `requirements.txt` - Python dependencies

## 📁 Project Structure

```
ded-lw-rag_llm/
├── .github/
│   ├── workflows/
│   │   └── ci-cd.yml          # GitHub Actions workflow
│   ├── CODEOWNERS            # Repository ownership
│   └── PULL_REQUEST_TEMPLATE.md
├── chroma_index/             # Vector database
│   └── chroma.sqlite3
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_rag_system.py
├── rag_llama.py             # Development version
├── rag_llama_deploy.py      # Production version
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── .dockerignore           # Docker exclusions
├── pyproject.toml          # Tool configurations
├── .gitignore             # Git exclusions
├── LICENSE                # MIT License
└── README.md              # This file
```

## 🔒 Security

- The `docs/` directory containing PDF files is excluded from version control
- Security scanning is performed in the CI/CD pipeline
- Sensitive data is not committed to the repository

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Contact

- **Maintainer**: @os-olaniyi
- **Email**: os.olaniyi@outlook.com, suol0008@student.hv.se

## 🚀 Deployment

The CI/CD pipeline automatically:
- Tests the application on multiple Python versions
- Builds a Docker image
- Creates deployment artifacts
- Performs security scans

For manual deployment, use the Docker image or run the Streamlit application directly. 