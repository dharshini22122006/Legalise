# 🎉 Legal Document Analyzer - Complete Setup & Usage Guide

## 📋 Project Overview

You now have a complete **Legal Document Analyzer** powered by the **Granite AI model** from Hugging Face! This application provides:

✅ **Document Upload**: PDF, DOCX, TXT support  
✅ **AI-Powered Analysis**: Using Granite 3B Code Instruct model  
✅ **Named Entity Recognition**: Parties, dates, monetary values, legal terms  
✅ **Document Classification**: NDA, Employment Contract, Service Agreement, etc.  
✅ **Clause Simplification**: Complex legal text → Plain English  
✅ **Interactive Web Interface**: Built with Streamlit  
✅ **REST API**: FastAPI backend for programmatic access  
✅ **Export Options**: JSON, CSV, Text reports  

## 🚀 Quick Start Commands

### Step 1: Setup Environment

**Windows (Recommended - Use PowerShell as Administrator):**
```powershell
# Navigate to project
cd d:\legal\legal_document_analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Alternative for Windows (Command Prompt):**
```cmd
cd d:\legal\legal_document_analyzer
python -m venv venv
venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Run the Application

**Option A: Use the Startup Scripts (Easiest)**
```powershell
# PowerShell (Recommended)
.\start_analyzer.ps1

# Or Batch file
.\start_analyzer.bat
```

**Option B: Manual Start**
```powershell
# Activate environment
.\venv\Scripts\Activate.ps1

# Run the application
python run.py
```

**Option C: Direct Streamlit**
```powershell
# Activate environment first
.\venv\Scripts\Activate.ps1

# Run Streamlit directly
streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0
```

### Step 3: Access the Application

Open your web browser and go to:
```
http://localhost:8501
```

## 📁 Complete Project Structure

```
legal_document_analyzer/
├── 📱 app/                          # Main application
│   ├── main.py                      # Streamlit web interface
│   ├── api.py                       # FastAPI REST endpoints
│   ├── 🧠 core/                     # AI analysis modules
│   │   ├── analyzer.py              # Main orchestrator
│   │   ├── parser.py                # Document parsing (PDF/DOCX/TXT)
│   │   ├── preprocessor.py          # Text cleaning & preprocessing
│   │   ├── ner.py                   # Named Entity Recognition
│   │   ├── classifier.py            # Document type classification
│   │   └── simplifier.py            # Granite-powered simplification
│   ├── ⚙️ utils/                    # Utilities
│   │   ├── config.py                # Configuration management
│   │   ├── cache.py                 # Caching system
│   │   └── logging_config.py        # Logging setup
│   └── 🎨 static/                   # Static assets
│       └── css/custom.css           # Custom styling
├── 🧪 tests/                        # Test suite
│   ├── test_analyzer.py             # Core functionality tests
│   ├── test_api.py                  # API endpoint tests
│   └── sample_documents/            # Sample legal documents
│       ├── sample_nda.txt           # Non-Disclosure Agreement
│       ├── sample_employment_contract.txt  # Employment Contract
│       └── sample_service_agreement.txt    # Service Agreement
├── 🚀 deployment/                   # Deployment configurations
│   ├── Dockerfile                   # Docker container
│   ├── docker-compose.yml           # Multi-service deployment
│   ├── nginx.conf                   # Nginx reverse proxy
│   └── heroku/                      # Heroku deployment
├── 📚 docs/                         # Documentation
│   └── API.md                       # API documentation
├── 📋 Configuration Files
│   ├── requirements.txt             # Python dependencies
│   ├── requirements-dev.txt         # Development dependencies
│   ├── setup.py                     # Package setup
│   ├── .env.example                 # Environment variables template
│   └── .gitignore                   # Git ignore rules
├── 🎯 Startup Scripts
│   ├── run.py                       # Main entry point
│   ├── start_analyzer.bat           # Windows batch script
│   ├── start_analyzer.ps1           # PowerShell script
│   └── test_setup.py                # Setup verification
└── 📖 Documentation
    ├── README.md                    # Project overview
    ├── COMMANDS.md                  # All available commands
    └── FINAL_INSTRUCTIONS.md       # This file
```

## 🔧 Key Features & Usage

### 1. Document Analysis
- **Upload**: Drag & drop PDF, DOCX, or TXT files
- **Analysis**: AI-powered classification and entity extraction
- **Simplification**: Complex legal clauses → Plain English
- **Export**: Download results as JSON, CSV, or text report

### 2. Quick Text Analysis
- **Paste Text**: Analyze legal text snippets instantly
- **Fast Results**: Classification and entity extraction
- **No File Upload**: Direct text input

### 3. Analytics Dashboard
- **History**: View past analyses
- **Statistics**: Document type distribution
- **Trends**: Analysis patterns over time

### 4. REST API
- **Endpoints**: Full programmatic access
- **Documentation**: Interactive docs at `/docs`
- **Integration**: Easy integration with other applications

## 🧪 Testing with Sample Documents

The project includes three sample legal documents:

1. **Non-Disclosure Agreement** (`sample_nda.txt`)
2. **Employment Contract** (`sample_employment_contract.txt`)
3. **Service Agreement** (`sample_service_agreement.txt`)

**To test:**
1. Start the application
2. Go to "Document Analysis" tab
3. Upload one of the sample documents from `test/sample_documents/`
4. Click "Analyze Document"
5. Explore the results!

## 🤖 AI Model Information

**Primary Model**: `ibm-granite/granite-3b-code-instruct`
- **Purpose**: Legal text simplification and analysis
- **Size**: ~3B parameters
- **Capabilities**: Text generation, simplification, analysis
- **Fallback**: Microsoft DialoGPT-medium (if primary fails)

**Model Features:**
- ✅ Legal clause simplification
- ✅ Plain English translation
- ✅ Key point extraction
- ✅ Context-aware processing

## 🔧 Advanced Usage

### Run FastAPI Backend Separately
```powershell
# Terminal 1 - API Backend
.\venv\Scripts\Activate.ps1
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Streamlit Frontend
.\venv\Scripts\Activate.ps1
streamlit run app/main.py --server.port=8501
```

### Docker Deployment
```bash
# Build and run with Docker
docker build -t legal-analyzer -f deployment/Dockerfile .
docker run -p 8501:8501 legal-analyzer

# Or use Docker Compose
docker-compose -f deployment/docker-compose.yml up -d
```

### Development Mode
```powershell
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Code formatting
black app/ tests/
```

## 🌐 Access URLs

After starting the application:

- **Main Application**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🛠️ Troubleshooting

### Common Issues & Solutions

**1. "Module not found" errors:**
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**2. "Port already in use":**
```powershell
# Use different port
streamlit run app/main.py --server.port=8502
```

**3. "CUDA out of memory":**
```powershell
# Force CPU usage
$env:TORCH_DEVICE="cpu"
python run.py
```

**4. Model download issues:**
- Ensure stable internet connection
- Check firewall settings
- Try running again (models are cached after first download)

**5. Permission errors:**
- Run PowerShell as Administrator
- Check antivirus software
- Ensure write permissions in project directory

### System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- 2GB free disk space
- Internet connection (for model download)

**Recommended:**
- Python 3.10+
- 8GB RAM
- 5GB free disk space
- GPU with CUDA support (optional, for faster processing)

## 📊 Performance Expectations

- **Startup Time**: 30-60 seconds (first run, model download)
- **Analysis Time**: 1-3 minutes per document
- **Memory Usage**: 2-6GB during analysis
- **File Size Limit**: 10MB per document
- **Supported Languages**: English

## 🔒 Privacy & Security

- ✅ **Local Processing**: All analysis happens on your machine
- ✅ **No Data Transmission**: Documents never leave your system
- ✅ **Temporary Storage**: Files automatically deleted after processing
- ✅ **Session-Based**: Results stored only in browser session

## 🎯 Next Steps

1. **Start the Application**: Use one of the startup methods above
2. **Test with Samples**: Upload sample documents to verify functionality
3. **Explore Features**: Try all tabs and options
4. **Analyze Your Documents**: Upload your own legal documents
5. **Use the API**: Integrate with other applications if needed
6. **Customize**: Modify settings and configurations as needed

## 🆘 Getting Help

If you encounter issues:

1. **Check the console output** for error messages
2. **Verify Python version**: `python --version` (should be 3.8+)
3. **Ensure dependencies are installed**: `pip list`
4. **Try with sample documents first**
5. **Check system resources** (RAM, disk space)
6. **Restart the application**

## 🎉 Success Indicators

You'll know everything is working when:

✅ Application starts without errors  
✅ Web interface loads at http://localhost:8501  
✅ Sample documents can be uploaded and analyzed  
✅ Results show document classification and entities  
✅ Clause simplification works (if enabled)  
✅ Export functions generate downloadable files  

---

## 🏆 Congratulations!

You now have a fully functional **AI-powered Legal Document Analyzer**! 

**Key Capabilities:**
- 📄 Multi-format document support (PDF, DOCX, TXT)
- 🤖 AI-powered analysis using Granite model
- 🏷️ Named entity recognition and extraction
- 📋 Document type classification
- 🔄 Legal clause simplification
- 📊 Interactive web interface
- 🔌 REST API for integration
- 💾 Multiple export formats

**Start analyzing legal documents with AI today!** 🚀⚖️

---

*Powered by Granite AI Model from Hugging Face | Built with Streamlit & FastAPI*