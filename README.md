# RAG LLM - Laser Metal Deposition Knowledge Base

A comprehensive Retrieval-Augmented Generation (RAG) system for Laser Metal Deposition (LMD) knowledge using Llama3, ChromaDB, and advanced features with dual-version support.

## 🚀 Features

### Core RAG System
- **Dual Version Support**: Original and Enhanced RAG implementations
- **Vector Database**: ChromaDB for efficient document retrieval
- **LLM Integration**: Ollama with Llama3:70b model
- **Web Interface**: Streamlit-based user interface with custom theming

### Enhanced RAG Features (RAG_LLAMAv2)
- **📤 Real-time PDF Upload**: Drag-and-drop PDF processing
- **🔄 File Deduplication**: Hash-based duplicate detection
- **🎨 Keyword Highlighting**: Domain-specific term highlighting
- **🧹 Citation Cleaning**: Automatic academic citation removal
- **💾 Conversation History**: Session-based chat history
- **⭐ User Feedback**: Helpful/Not helpful rating system
- **🎨 Custom Branding**: Professional logo and theming
- **📊 Database Tracking**: SQLite-based upload management

### Security & Quality
- **🔒 Multi-layer Security**: CodeQL, Semgrep, and Bandit scanning
- **🧪 Comprehensive Testing**: Multi-Python version testing
- **📈 Code Quality**: Linting, formatting, and coverage reporting
- **🐳 Docker Support**: Containerized deployment options

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

### Original RAG Version
```bash
# Development mode
streamlit run rag_llama.py

# Production mode
streamlit run rag_llama_deploy.py
```

### Enhanced RAG Version (Recommended)
```bash
# Navigate to enhanced version
cd RAG_LLAMAv2
streamlit run rag_llama_deploy_1.1av.py
```

### Docker Deployment
```bash
# Original version
docker build -t rag-llm:original .

# Enhanced version
docker build -f Dockerfile.enhanced -t rag-llm:enhanced .

# Run enhanced version
docker run -p 8501:8501 rag-llm:enhanced
```

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=./ --cov-report=html
```

### Test Enhanced Features
```bash
pytest tests/test_enhanced_features.py
```

## 🔧 CI/CD Pipeline

The project includes a comprehensive GitHub Actions workflow with **separate test steps** for easy debugging:

### Triggers
- Push to `master`, `deployment`, or `DRL-*` branches
- Pull requests to `master` branch
- Manual workflow dispatch

### Jobs

#### 1. **Test Job** (Multi-Python Matrix)
- **Python Versions**: 3.9, 3.10, 3.11
- **Separate Test Steps**:
  - 📦 **Test Original RAG Version** (clickable)
  - 🚀 **Test Enhanced RAG Version** (clickable)
  - **Run tests with coverage** (clickable)
- **Quality Checks**: Linting (flake8, black, isort)
- **Coverage Reporting**: Codecov integration

#### 2. **Security Scanning**
- **🔒 CodeQL**: GitHub's built-in security analysis
- **🛡️ Semgrep**: Comprehensive security rules
- **🔍 Bandit**: Python-specific security scanning
- **📊 Dual Reports**: Separate scans for original and enhanced versions

#### 3. **Feature Tests** (Enhanced RAG)
- **📤 Test File Upload System** (clickable)
- **🎨 Test Keyword Highlighting** (clickable)
- **🧹 Test Citation Cleaning** (clickable)
- **📋 Feature Tests Summary** (clickable)

#### 4. **Build & Deploy**
- **📦 Dual Deployment Packages**: Original and enhanced versions
- **🐳 Docker Images**: Both versions containerized
- **📁 Artifact Management**: Organized deployment packages

### Workflow Files
- `.github/workflows/ci-cd.yml` - Main CI/CD pipeline
- `Dockerfile` - Original version container
- `Dockerfile.enhanced` - Enhanced version container
- `.dockerignore` - Docker build exclusions
- `pyproject.toml` - Tool configurations
- `requirements.txt` - Python dependencies

## 📁 Project Structure

```
ded-lw-rag_llm/
├── .github/
│   ├── workflows/
│   │   └── ci-cd.yml          # GitHub Actions workflow
│   └── CODEOWNERS            # Repository ownership
├── RAG_LLAMAv2/              # Enhanced RAG System
│   ├── .streamlit/
│   │   └── config.toml       # Custom Streamlit theming
│   ├── chroma_index/         # Vector database
│   ├── upload_hashes.db      # File deduplication
│   ├── LOGO3b.png           # Custom branding
│   └── rag_llama_deploy_1.1av.py  # Enhanced app
├── chroma_index/             # Original vector database
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_rag_system.py   # Original tests
│   └── test_enhanced_features.py  # Enhanced tests
├── rag_llama.py             # Original development version
├── rag_llama_deploy.py      # Original production version
├── requirements.txt         # Python dependencies
├── Dockerfile              # Original container
├── Dockerfile.enhanced     # Enhanced container
├── .dockerignore           # Docker exclusions
├── pyproject.toml          # Tool configurations
├── .flake8                # Linting configuration
├── .gitignore             # Git exclusions
├── LICENSE                # MIT License
└── README.md              # This file
```

## 🔒 Security Features

### Multi-Layer Security Scanning
- **CodeQL**: GitHub's built-in SAST analysis
- **Semgrep**: Comprehensive security rules and custom patterns
- **Bandit**: Python-specific vulnerability detection
- **Dual Coverage**: Both original and enhanced versions scanned

### Security Best Practices
- **No hardcoded secrets** in repository
- **Secure file handling** with proper validation
- **Input sanitization** for user uploads
- **Database security** with proper connection handling

## 🎯 Enhanced RAG Features

### File Upload System
- **Real-time PDF processing** with drag-and-drop
- **Hash-based deduplication** prevents re-processing
- **SQLite database** tracks uploaded files
- **Threaded processing** for better performance

### Text Processing
- **Citation cleaning** removes academic references
- **Keyword highlighting** for domain-specific terms
- **Smart chunking** with overlap for better context
- **Metadata preservation** for source tracking

### User Experience
- **Custom branding** with professional logo
- **Green theme** (#4CAF50) for consistent branding
- **Conversation history** with session management
- **Feedback system** for continuous improvement

## 📊 CI/CD Benefits

### Easy Debugging
- **Clickable test steps** in GitHub Actions
- **Separate logs** for each test type
- **Clear error identification** by version and feature
- **Conditional artifact uploads** for flexible testing

### Comprehensive Coverage
- **Multi-Python testing** (3.9, 3.10, 3.11)
- **Dual version testing** (Original + Enhanced)
- **Feature-specific tests** for enhanced capabilities
- **Security scanning** across all components

### Professional Deployment
- **Dual Docker images** for both versions
- **Organized artifacts** with clear structure
- **Automated quality gates** with comprehensive checks
- **Flexible deployment** options

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

### Automated CI/CD Pipeline
The pipeline automatically:
- ✅ **Tests both versions** on multiple Python versions
- ✅ **Scans for security** vulnerabilities
- ✅ **Builds Docker images** for both versions
- ✅ **Creates deployment packages** with all assets
- ✅ **Uploads artifacts** for easy deployment

### Manual Deployment
```bash
# Enhanced version (recommended)
cd RAG_LLAMAv2
streamlit run rag_llama_deploy_1.1av.py

# Docker deployment
docker run -p 8501:8501 rag-llm:enhanced
```

### Production Recommendations
- Use the **Enhanced RAG version** for production
- Deploy with **Docker** for consistency
- Enable **GitHub Actions** for automated testing
- Monitor **security scan results** regularly 