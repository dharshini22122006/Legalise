# 🚀 LEGAL DOCUMENT ANALYZER - FINAL RUN COMMANDS

## ⚡ **QUICK START (Copy & Paste These Commands)**

### **Step 1: Open PowerShell as Administrator**
```powershell
# Navigate to the project directory
cd d:\legal\legal_document_analyzer
```

### **Step 2: Verify Installation**
```powershell
# Check if everything is properly set up
python verify_installation.py
```

### **Step 3: Install Dependencies**
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
pip install streamlit==1.28.1 transformers==4.35.2 torch==2.1.1 fastapi==0.104.1 uvicorn==0.24.0 pandas==2.1.3 numpy==1.24.3 requests==2.31.0 pydantic==2.5.0 python-multipart==0.0.6 aiofiles==23.2.1 PyMuPDF==1.23.8 python-docx==0.8.11 spacy==3.7.2 scikit-learn==1.3.2 nltk==3.8.1 plotly==5.17.0 Pillow==10.1.0
```

### **Step 4: Run the Application**
```powershell
# Start the Legal Document Analyzer
python run.py
```

### **Step 5: Access the Application**
```
🌐 Open your browser and go to: http://localhost:8501
```

---

## 🎯 **ALTERNATIVE METHODS**

### **Method A: Automated Script (Easiest)**
```powershell
# Run the automated setup script
.\start_analyzer.ps1
```

### **Method B: Using Requirements File**
```powershell
# Activate environment and install from requirements
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

### **Method C: Direct Streamlit**
```powershell
# Run Streamlit directly
.\venv\Scripts\Activate.ps1
streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0
```

---

## 🧪 **TESTING COMMANDS**

### **Test with Sample Documents**
1. **Start the application** using any method above
2. **Open browser**: http://localhost:8501
3. **Upload sample document**: Use files from `test/sample_documents/`
4. **Click "Analyze Document"**
5. **Review AI-powered results**

### **Test API Endpoints**
```powershell
# In a new PowerShell window, test the API
curl http://localhost:8000/health
curl http://localhost:8000/analyze/supported-types
```

### **Run Test Suite**
```powershell
# Install test dependencies and run tests
pip install pytest pytest-asyncio
pytest tests/ -v
```

---

## 🔧 **TROUBLESHOOTING COMMANDS**

### **If Python is not found:**
```powershell
# Check Python installation
python --version
py --version

# If not found, install Python 3.8+ from python.org
```

### **If virtual environment issues:**
```powershell
# Recreate virtual environment
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### **If port is already in use:**
```powershell
# Use different port
streamlit run app/main.py --server.port=8502
```

### **If memory issues:**
```powershell
# Force CPU usage (no GPU)
$env:TORCH_DEVICE="cpu"
python run.py
```

---

## 📋 **WHAT YOU'LL SEE WHEN IT WORKS**

### **✅ Success Indicators:**
1. **Console shows**: "Starting Legal Document Analyzer..."
2. **Browser opens**: Streamlit interface at localhost:8501
3. **Interface displays**: Upload area and analysis options
4. **Sample documents**: Can be uploaded and analyzed
5. **Results show**: Document classification, entities, simplified clauses
6. **Export works**: Can download JSON, CSV, text reports

### **🎯 Ready to Use When:**
- ✅ Web interface loads without errors
- ✅ File upload area is visible
- ✅ Sidebar shows analysis options
- ✅ Sample documents analyze successfully
- ✅ Results display classification and entities
- ✅ Clause simplification works (if enabled)

---

## 🎉 **FINAL VERIFICATION CHECKLIST**

### **Before You Start:**
- [ ] Python 3.8+ installed
- [ ] PowerShell available
- [ ] Internet connection active
- [ ] At least 4GB RAM available
- [ ] 5GB free disk space

### **After Running Commands:**
- [ ] Virtual environment activated
- [ ] Dependencies installed successfully
- [ ] Application starts without errors
- [ ] Web interface loads at localhost:8501
- [ ] Sample document analysis works
- [ ] Export functions generate files

---

## 🚀 **LAUNCH SEQUENCE**

### **🎬 Copy and paste these commands in order:**

```powershell
# 1. Navigate to project
cd d:\legal\legal_document_analyzer

# 2. Activate environment
.\venv\Scripts\Activate.ps1

# 3. Install core dependencies
pip install streamlit transformers torch fastapi uvicorn pandas numpy requests

# 4. Install additional dependencies
pip install pydantic python-multipart aiofiles PyMuPDF python-docx spacy scikit-learn nltk plotly Pillow

# 5. Start the application
python run.py
```

### **🌐 Then open your browser to:**
```
http://localhost:8501
```

---

## 🎊 **CONGRATULATIONS!**

### **🏆 You now have a fully functional AI-powered Legal Document Analyzer!**

**Key Features Ready to Use:**
- 📄 **Multi-format document upload** (PDF, DOCX, TXT)
- 🤖 **AI-powered analysis** using Granite model
- 🏷️ **Named entity recognition** (parties, dates, money, terms)
- 📋 **Document classification** (NDA, contracts, agreements)
- 🔄 **Clause simplification** (legal jargon → plain English)
- 📊 **Interactive web interface** with Streamlit
- 🔌 **REST API** for programmatic access
- 💾 **Export options** (JSON, CSV, text reports)
- 📈 **Analytics dashboard** with usage statistics

### **🎯 Start Analyzing Legal Documents Now!**

1. **Upload** a sample document from `test/sample_documents/`
2. **Click** "Analyze Document"
3. **Review** the AI-powered insights
4. **Export** results in your preferred format
5. **Explore** all features and capabilities

---

**🎉 ENJOY YOUR AI-POWERED LEGAL DOCUMENT ANALYZER! 🎉**

*Built with Python, Streamlit, FastAPI, and Granite AI Model from Hugging Face*