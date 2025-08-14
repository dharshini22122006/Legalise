# ⚖️ Legal Document Analyzer

An AI-powered legal document analysis tool that uses the Granite model from Hugging Face to simplify complex legal documents and extract key information.

## 🌟 Features

- **📄 Multi-Format Support**: Upload PDF, DOCX, or TXT legal documents
- **🤖 AI-Powered Analysis**: Uses Granite 3B Code Instruct model for intelligent text processing
- **🏷️ Named Entity Recognition**: Automatically identifies parties, dates, monetary values, and legal terms
- **📋 Document Classification**: Classifies documents into types (NDA, Employment Contract, Service Agreement, etc.)
- **🔄 Clause Simplification**: Converts complex legal jargon into plain English
- **📊 Interactive Dashboard**: User-friendly Streamlit interface with analytics
- **💾 Export Options**: Download results in JSON, CSV, or text report formats

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- At least 4GB RAM (8GB recommended for optimal performance)

### Installation

1. **Clone or download the project**:
   ```bash
   cd legal_document_analyzer
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:8501
   ```

## 📖 Usage

### Document Analysis

1. **Upload Document**: Click "Choose a legal document" and select a PDF, DOCX, or TXT file
2. **Configure Settings**: Use the sidebar to adjust analysis options
3. **Analyze**: Click "🔍 Analyze Document" to start the analysis
4. **Review Results**: Explore the comprehensive analysis results including:
   - Document classification and confidence score
   - Extracted entities (parties, dates, monetary values)
   - Simplified clauses in plain English
   - Key findings and recommendations
5. **Export**: Download results in your preferred format

### Quick Analysis

1. Navigate to the "🔍 Quick Analysis" tab
2. Paste legal text directly into the text area
3. Click "🔍 Quick Analyze" for instant results

### Analytics Dashboard

1. Visit the "📊 Analytics" tab to view:
   - Analysis history and trends
   - Document type distribution
   - Performance metrics

## 🔧 Configuration

### Model Configuration

The application uses the Granite model by default. You can modify the model settings in `app/utils/config.py`:

```python
GRANITE_MODEL_NAME = "ibm-granite/granite-3b-code-instruct"
```

### Analysis Settings

Adjust analysis parameters in the sidebar:
- **Include Clause Simplification**: Enable/disable AI-powered clause simplification
- **Max Clauses to Analyze**: Limit the number of clauses processed (1-20)

## 📁 Project Structure

```
legal_document_analyzer/
├── app/
│   ├── main.py                 # Main Streamlit application
│   ├── core/
│   │   ├── analyzer.py         # Main analysis orchestrator
│   │   ├── parser.py           # Document parsing (PDF, DOCX, TXT)
│   │   ├── preprocessor.py     # Text cleaning and preprocessing
│   │   ├── ner.py              # Named Entity Recognition
│   │   ├── classifier.py       # Document type classification
│   │   └── simplifier.py       # Granite-powered clause simplification
│   └── utils/
│       ├── config.py           # Configuration management
│       ├── cache.py            # Caching utilities
│       └── logging_config.py   # Logging setup
├── test/
│   └── sample_documents/       # Sample legal documents for testing
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
└── README.md                   # This file
```

## 🧪 Sample Documents

The project includes sample legal documents for testing:

- **sample_nda.txt**: Non-Disclosure Agreement
- **sample_employment_contract.txt**: Employment Contract
- **sample_service_agreement.txt**: Professional Services Agreement

## 🔍 Analysis Capabilities

### Document Types Supported

- Non-Disclosure Agreements (NDA)
- Employment Contracts
- Service Agreements
- Lease Agreements
- Purchase Agreements
- Partnership Agreements
- License Agreements
- Loan Agreements

### Entity Extraction

- **Parties**: Companies, individuals, legal entities
- **Dates**: Effective dates, deadlines, expiration dates
- **Monetary Values**: Fees, salaries, penalties, deposits
- **Legal Terms**: Obligations, liabilities, confidentiality clauses
- **Contact Information**: Addresses, phone numbers, emails

### Clause Simplification

The Granite AI model converts complex legal language into:
- Plain English explanations
- Key point summaries
- Practical implications
- User-friendly terminology

## 🛠️ Troubleshooting

### Common Issues

1. **Model Loading Errors**:
   - Ensure you have sufficient RAM (8GB recommended)
   - Check internet connection for model download
   - Try restarting the application

2. **File Upload Issues**:
   - Verify file format (PDF, DOCX, TXT only)
   - Check file size (max 10MB)
   - Ensure file is not corrupted

3. **Performance Issues**:
   - Reduce max clauses to analyze
   - Disable clause simplification for faster processing
   - Close other memory-intensive applications

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Try with sample documents first
4. Restart the application

## 🔒 Privacy & Security

- All document processing is performed locally
- No data is sent to external servers (except for model downloads)
- Uploaded documents are temporarily stored and automatically deleted
- Analysis results are stored only in your browser session

## 📊 Performance

- **Processing Speed**: 1-3 minutes per document (depending on size and complexity)
- **Memory Usage**: 2-6GB RAM during analysis
- **Supported File Sizes**: Up to 10MB per document
- **Concurrent Users**: Single-user application (local deployment)

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Report bugs and issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Hugging Face** for the Granite model and transformers library
- **Streamlit** for the excellent web framework
- **PyMuPDF** and **python-docx** for document parsing capabilities
- The open-source community for various supporting libraries

---

**⚖️ Legal Document Analyzer** - Making legal documents accessible to everyone through AI-powered analysis and simplification.