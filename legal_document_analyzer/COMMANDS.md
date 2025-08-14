# 🚀 Legal Document Analyzer - Commands to Run

## Quick Start (Recommended)

### Windows Users

**Option 1: Using Batch File (Easiest)**
```cmd
# Double-click the file or run in Command Prompt
start_analyzer.bat
```

**Option 2: Using PowerShell (Recommended)**
```powershell
# Right-click and "Run with PowerShell" or run in PowerShell
.\start_analyzer.ps1
```

### Manual Setup (All Platforms)

1. **Navigate to project directory:**
```bash
cd legal_document_analyzer
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**

**Windows:**
```cmd
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Run the application:**
```bash
python run.py
```

6. **Open your browser:**
```
http://localhost:8501
```

## Alternative Running Methods

### Method 1: Direct Streamlit
```bash
# Activate virtual environment first
streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0
```

### Method 2: FastAPI Only (API Backend)
```bash
# Activate virtual environment first
uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
```

### Method 3: Both Services
```bash
# Terminal 1 - Streamlit UI
streamlit run app/main.py --server.port=8501

# Terminal 2 - FastAPI Backend
uvicorn app.api:app --host 0.0.0.0 --port 8000
```

## Docker Deployment

### Single Container (Streamlit Only)
```bash
# Build image
docker build -t legal-analyzer -f deployment/Dockerfile .

# Run container
docker run -p 8501:8501 legal-analyzer
```

### Full Stack with Docker Compose
```bash
# Start all services
docker-compose -f deployment/docker-compose.yml up -d

# View logs
docker-compose -f deployment/docker-compose.yml logs -f

# Stop services
docker-compose -f deployment/docker-compose.yml down
```

### Development with Docker
```bash
# Development mode with hot reload
docker-compose -f deployment/docker-compose.yml -f deployment/docker-compose.dev.yml up
```

## Testing

### Run All Tests
```bash
# Activate virtual environment first
pip install -r requirements-dev.txt
pytest tests/ -v
```

### Run Specific Tests
```bash
# Core functionality tests
pytest tests/test_analyzer.py -v

# API tests
pytest tests/test_api.py -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

## Development Commands

### Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### Code Formatting
```bash
# Format code with black
black app/ tests/

# Sort imports
isort app/ tests/

# Lint code
flake8 app/ tests/
```

### Type Checking
```bash
mypy app/
```

## Troubleshooting Commands

### Check Python Version
```bash
python --version
# Should be 3.8 or higher
```

### Check Installed Packages
```bash
pip list
```

### Reinstall Dependencies
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Clear Cache
```bash
# Clear Python cache
find . -type d -name "__pycache__" -delete
find . -name "*.pyc" -delete

# Clear Streamlit cache
streamlit cache clear
```

### Check Port Usage
```bash
# Windows
netstat -an | findstr :8501
netstat -an | findstr :8000

# macOS/Linux
lsof -i :8501
lsof -i :8000
```

### Kill Process on Port
```bash
# Windows
taskkill /F /PID <PID>

# macOS/Linux
kill -9 <PID>
```

## Environment Variables

### Create .env file (optional)
```bash
cp .env.example .env
# Edit .env with your settings
```

### Common Environment Variables
```bash
# Model configuration
export GRANITE_MODEL_NAME="ibm-granite/granite-3b-code-instruct"
export HF_CACHE_DIR="./cache/huggingface"

# Application settings
export STREAMLIT_PORT=8501
export DEBUG_MODE=false
export LOG_LEVEL=INFO
```

## Performance Optimization

### For Better Performance
```bash
# Use GPU if available
export TORCH_DEVICE=cuda

# Increase memory for large documents
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

### Monitor Resource Usage
```bash
# Windows
tasklist | findstr python

# macOS/Linux
top -p $(pgrep -f python)
htop
```

## Production Deployment

### Heroku Deployment
```bash
# Install Heroku CLI first
heroku create your-app-name
heroku config:set STREAMLIT_SERVER_PORT=$PORT
git push heroku main
```

### AWS/GCP/Azure
```bash
# Build production image
docker build -t legal-analyzer:prod -f deployment/Dockerfile .

# Tag for registry
docker tag legal-analyzer:prod your-registry/legal-analyzer:latest

# Push to registry
docker push your-registry/legal-analyzer:latest
```

## Useful URLs

After starting the application, these URLs will be available:

- **Main Application**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs (if FastAPI is running)
- **API Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Common Issues and Solutions

### Issue: "Module not found"
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
```

### Issue: "Port already in use"
```bash
# Solution: Use different port
streamlit run app/main.py --server.port=8502
```

### Issue: "CUDA out of memory"
```bash
# Solution: Use CPU instead
export TORCH_DEVICE=cpu
```

### Issue: "Model download fails"
```bash
# Solution: Check internet connection and try again
# Or use offline mode with pre-downloaded models
```

### Issue: "Streamlit not found"
```bash
# Solution: Install streamlit
pip install streamlit
```

## Getting Help

1. **Check logs**: Look at console output for error messages
2. **Verify setup**: Ensure Python 3.8+ and all dependencies are installed
3. **Test with samples**: Use provided sample documents first
4. **Check resources**: Ensure sufficient RAM (8GB recommended)
5. **Update dependencies**: `pip install -r requirements.txt --upgrade`

## Next Steps

1. **Start the application** using one of the methods above
2. **Upload a sample document** from `test/sample_documents/`
3. **Explore the features** - classification, entity extraction, simplification
4. **Try the API** at http://localhost:8000/docs
5. **Customize settings** in the sidebar

---

**🎉 You're ready to analyze legal documents with AI!**