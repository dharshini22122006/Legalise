"""Standalone Streamlit app for Legal Document Analyzer."""

import streamlit as st
import os
import sys
import asyncio
import tempfile
import json
import re
import time
import threading
import concurrent.futures
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Document processing imports
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import fitz  # PyMuPDF as fallback
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

# Page configuration
st.set_page_config(
    page_title="Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c5aa0;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .entity-tag {
        background-color: #e1f5fe;
        color: #01579b;
        padding: 0.2rem 0.5rem;
        border-radius: 0.3rem;
        margin: 0.1rem;
        display: inline-block;
    }
    .clause-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-left: 4px solid #4a5568;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Georgia', serif;
        line-height: 1.6;
    }
    .simplified-clause {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        border-left: 4px solid #2d7d32;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        font-family: 'Arial', sans-serif;
        line-height: 1.6;
    }
    .clause-header {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    .file-support-info {
        background: linear-gradient(45deg, #3498db, #2c3e50);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.3rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class StandaloneLegalAnalyzer:
    """Standalone legal document analyzer with multi-format support."""
    
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.supported_formats = self._get_supported_formats()
        
        # Document classification patterns
        self.document_patterns = {
            'nda': [
                r'non.?disclosure', r'confidential', r'proprietary', r'trade secret',
                r'confidentiality agreement'
            ],
            'employment_contract': [
                r'employment', r'employee', r'employer', r'salary', r'compensation',
                r'job description', r'work agreement'
            ],
            'service_agreement': [
                r'service', r'provider', r'client', r'deliverable', r'scope of work',
                r'consulting', r'professional services'
            ],
            'lease_agreement': [
                r'lease', r'rent', r'tenant', r'landlord', r'property',
                r'rental agreement'
            ],
            'purchase_agreement': [
                r'purchase', r'buyer', r'seller', r'sale', r'goods',
                r'sales agreement'
            ]
        }
        
        # Entity extraction patterns
        self.entity_patterns = {
            'monetary_values': r'\$[\d,]+(?:\.\d{2})?',
            'dates': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            'percentages': r'\d+(?:\.\d+)?%',
            'phone_numbers': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email_addresses': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
        
        # Legal jargon simplification rules
        self.simplification_rules = {
            r'\bheretofore\b': 'before this',
            r'\bhereinafter\b': 'from now on',
            r'\bwhereas\b': 'since',
            r'\btherefore\b': 'so',
            r'\bnotwithstanding\b': 'despite',
            r'\bpursuant to\b': 'according to',
            r'\bshall\b': 'will',
            r'\bin the event that\b': 'if',
            r'\bprior to\b': 'before',
            r'\bsubsequent to\b': 'after'
        }
    
    def _get_supported_formats(self) -> Dict[str, bool]:
        """Get supported file formats."""
        return {
            'txt': True,
            'docx': DOCX_AVAILABLE,
            'pdf': PDF_AVAILABLE or PYMUPDF_AVAILABLE
        }
    
    def _parse_pdf(self, file_path: str) -> str:
        """Parse PDF file with fallback support."""
        text = ""

        # Try PyPDF2 first
        if PDF_AVAILABLE:
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                if text.strip():  # If we got text, return it
                    return text
            except Exception as e:
                print(f"PyPDF2 failed: {e}, trying PyMuPDF...")

        # Try PyMuPDF as fallback
        if PYMUPDF_AVAILABLE:
            try:
                import fitz
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text() + "\n"
                doc.close()
                if text.strip():
                    return text
            except Exception as e:
                print(f"PyMuPDF failed: {e}")

        # If both failed
        if not PDF_AVAILABLE and not PYMUPDF_AVAILABLE:
            raise ValueError("PDF support not available. Install PyPDF2 or PyMuPDF.")
        else:
            raise ValueError(f"Error reading PDF file. The file may be corrupted or password-protected.")
    
    def _parse_docx(self, file_path: str) -> str:
        """Parse DOCX file."""
        if not DOCX_AVAILABLE:
            raise ValueError("DOCX support not available. Install python-docx.")
        
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise ValueError(f"Error reading DOCX: {str(e)}")
        
        return text
    
    def _parse_txt(self, file_path: str) -> str:
        """Parse TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Error reading TXT: {str(e)}")
    
    def _parse_document_by_type(self, file_path: str, file_extension: str) -> str:
        """Parse document based on file type."""
        if file_extension == '.txt':
            return self._parse_txt(file_path)
        elif file_extension == '.docx':
            return self._parse_docx(file_path)
        elif file_extension == '.pdf':
            return self._parse_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def analyze_document(self, file_path: str, max_clauses: int = 20) -> Dict[str, Any]:
        """Analyze a legal document."""
        try:
            # Parse document based on file type
            file_extension = os.path.splitext(file_path)[1].lower()
            content = self._parse_document_by_type(file_path, file_extension)
            
            # Clean text
            cleaned_text = re.sub(r'\s+', ' ', content).strip()
            
            # Calculate statistics
            words = cleaned_text.split()
            sentences = re.split(r'[.!?]+', cleaned_text)
            
            statistics = {
                'word_count': len(words),
                'character_count': len(cleaned_text),
                'sentence_count': len([s for s in sentences if s.strip()]),
                'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
                'average_sentence_length': len(words) / len(sentences) if sentences else 0
            }
            
            # Classify document
            classification = self._classify_document(cleaned_text)
            
            # Extract entities
            entities = self._extract_entities(cleaned_text)
            
            # Extract clauses
            clauses = self._extract_clauses(cleaned_text)
            
            # Simplify clauses based on user settings
            simplified_clauses = []
            actual_max_clauses = min(len(clauses), max_clauses)
            for i, clause in enumerate(clauses[:actual_max_clauses]):
                simplified = self._simplify_clause(clause)
                simplified['clause_number'] = i + 1
                simplified_clauses.append(simplified)
            
            # Generate summary
            summary = self._generate_summary(classification, entities, statistics)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(classification, entities)
            
            return {
                'document_info': {
                    'file_name': os.path.basename(file_path),
                    'file_type': file_extension.replace('.', ''),
                    'file_size': len(content),
                    'analysis_timestamp': datetime.now().isoformat()
                },
                'classification': classification,
                'text_statistics': statistics,
                'entities': entities,
                'clauses': {
                    'total_count': len(clauses),
                    'extracted_clauses': clauses,
                    'simplified_clauses': simplified_clauses
                },
                'summary': summary,
                'recommendations': recommendations
            }
            
        except Exception as e:
            st.error(f"Error analyzing document: {str(e)}")
            raise
    
    def _classify_document(self, text: str) -> Dict[str, Any]:
        """Classify document type."""
        text_lower = text.lower()
        scores = {}
        
        for doc_type, patterns in self.document_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            scores[doc_type] = score
        
        predicted_type = max(scores, key=scores.get) if scores else 'unknown'
        max_score = scores.get(predicted_type, 0)
        confidence = min(max_score / (len(text.split()) / 100), 1.0)
        
        return {
            'predicted_type': predicted_type,
            'confidence': confidence,
            'is_confident': confidence > 0.3,
            'scores': scores
        }
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities."""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities[entity_type] = [
                {'text': match, 'type': entity_type, 'confidence': 0.8}
                for match in set(matches)
            ]
        
        # Extract key parties
        key_parties = []
        party_patterns = [
            r'\b([A-Z][a-z]+ (?:Inc|LLC|Corp|Corporation|Company|Ltd)\.?)\b',
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b'
        ]
        
        for pattern in party_patterns:
            matches = re.findall(pattern, text)
            for match in matches[:5]:
                key_parties.append({
                    'name': match, 
                    'type': 'organization' if any(x in match for x in ['Inc', 'LLC', 'Corp']) else 'person'
                })
        
        return {
            'entities': entities,
            'key_parties': key_parties,
            'total_entities': sum(len(entity_list) for entity_list in entities.values())
        }
    
    def _extract_clauses(self, text: str) -> List[str]:
        """Extract clauses using multiple methods."""
        clauses = []
        
        # Method 1: Extract numbered sections (most reliable for legal documents)
        lines = text.split('\n')
        current_clause = ""
        current_number = None
        current_title = ""
        
        for line in lines:
            line_stripped = line.strip()
            
            # Check if line starts with a number followed by period and uppercase title
            match = re.match(r'^(\d+)\.\s+([A-Z][A-Z\s]+[A-Z])$', line_stripped)
            if match:
                # Save previous clause if exists
                if current_clause and current_number:
                    full_clause = f"{current_number}. {current_title}\n{current_clause.strip()}"
                    clauses.append(full_clause)
                
                # Start new clause
                current_number = match.group(1)
                current_title = match.group(2).strip()
                current_clause = ""
            elif current_number and line_stripped:
                # Continue current clause (skip empty lines)
                current_clause += line_stripped + " "
        
        # Add final clause
        if current_clause and current_number:
            full_clause = f"{current_number}. {current_title}\n{current_clause.strip()}"
            clauses.append(full_clause)
        
        # Method 2: If no numbered sections found, try paragraph-based extraction
        if not clauses:
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            for i, paragraph in enumerate(paragraphs):
                if len(paragraph) > 100:  # Only substantial paragraphs
                    # Check if paragraph contains numbered sections
                    if re.search(r'^\d+\.', paragraph):
                        clauses.append(paragraph)
                    elif i > 0:  # Skip title paragraph
                        clauses.append(f"Section {i}: {paragraph}")
        
        # Method 3: Force split by sentences for very long documents
        if not clauses and len(text) > 1000:
            # Split into logical chunks based on sentence endings
            sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
            current_chunk = ""
            chunk_num = 1
            
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence:
                    current_chunk += sentence + " "
                    
                    # If chunk is getting long enough, save it
                    if len(current_chunk) > 400:
                        clauses.append(f"Clause {chunk_num}: {current_chunk.strip()}")
                        current_chunk = ""
                        chunk_num += 1
            
            # Add remaining text as final clause
            if current_chunk.strip():
                clauses.append(f"Clause {chunk_num}: {current_chunk.strip()}")
        
        # Method 4: Final fallback - split into equal chunks
        if not clauses:
            chunk_size = max(400, len(text) // 10)  # Create ~10 chunks minimum
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i+chunk_size].strip()
                if chunk:
                    clauses.append(f"Part {i//chunk_size + 1}: {chunk}")
        
        # Clean up clauses - remove very short ones and limit length
        cleaned_clauses = []
        for clause in clauses:
            if len(clause) > 50:  # Minimum length
                # Truncate very long clauses but keep them readable
                if len(clause) > 1500:
                    # Find a good breaking point (end of sentence)
                    truncate_point = clause.rfind('.', 0, 1500)
                    if truncate_point > 1000:
                        clause = clause[:truncate_point + 1] + "\n\n[Content truncated for display...]"
                    else:
                        clause = clause[:1500] + "..."
                cleaned_clauses.append(clause)
        
        return cleaned_clauses
    
    def _simplify_clause(self, clause: str) -> Dict[str, Any]:
        """Simplify a clause."""
        original_clause = clause.strip()
        simplified_clause = original_clause
        
        # Apply simplification rules
        for pattern, replacement in self.simplification_rules.items():
            simplified_clause = re.sub(pattern, replacement, simplified_clause, flags=re.IGNORECASE)
        
        # Generate plain English summary
        plain_english = self._generate_plain_english_summary(simplified_clause)
        
        # Extract key points
        key_points = self._extract_key_points(simplified_clause)
        
        return {
            'original_clause': original_clause,
            'simplified_clause': simplified_clause,
            'plain_english_summary': plain_english,
            'key_points': key_points,
            'simplification_score': 0.3  # Default score
        }
    
    def _generate_plain_english_summary(self, clause: str) -> str:
        """Generate plain English summary."""
        clause_lower = clause.lower()
        
        if 'payment' in clause_lower or '$' in clause:
            return "This clause deals with payment terms and amounts."
        elif 'termination' in clause_lower:
            return "This clause explains how the agreement can be ended."
        elif 'confidential' in clause_lower:
            return "This clause requires keeping information secret."
        elif 'liability' in clause_lower:
            return "This clause defines who is responsible for what."
        else:
            return "This clause contains important legal terms and conditions."
    
    def _extract_key_points(self, clause: str) -> List[str]:
        """Extract key points."""
        key_points = []
        
        # Look for monetary amounts
        money_matches = re.findall(r'\$[\d,]+(?:\.\d{2})?', clause)
        if money_matches:
            key_points.append(f"Involves money: {', '.join(money_matches)}")
        
        # Look for time periods
        time_matches = re.findall(r'\b\d+\s+(?:days?|weeks?|months?|years?)\b', clause, re.IGNORECASE)
        if time_matches:
            key_points.append(f"Time periods: {', '.join(time_matches)}")
        
        return key_points[:3]
    
    def _generate_summary(self, classification: Dict, entities: Dict, statistics: Dict) -> Dict[str, Any]:
        """Generate document summary."""
        summary = {
            'document_type': classification['predicted_type'].replace('_', ' ').title(),
            'confidence': f"{classification['confidence']:.1%}",
            'complexity': self._assess_complexity(statistics),
            'key_findings': []
        }
        
        # Add findings based on entities
        for entity_type, entity_list in entities['entities'].items():
            if entity_list:
                count = len(entity_list)
                summary['key_findings'].append(
                    f"Found {count} {entity_type.replace('_', ' ')}"
                )
        
        return summary
    
    def _generate_recommendations(self, classification: Dict, entities: Dict) -> List[str]:
        """Generate recommendations."""
        recommendations = []
        doc_type = classification['predicted_type']
        
        if doc_type == 'nda':
            recommendations.extend([
                "Review confidentiality scope and duration",
                "Ensure mutual obligations are clearly defined"
            ])
        elif doc_type == 'employment_contract':
            recommendations.extend([
                "Review compensation and benefits details",
                "Check termination and notice period clauses"
            ])
        elif doc_type == 'service_agreement':
            recommendations.extend([
                "Clarify scope of work and deliverables",
                "Review payment terms and schedule"
            ])
        
        return recommendations[:5]
    
    def _assess_complexity(self, statistics: Dict) -> str:
        """Assess document complexity."""
        word_count = statistics.get('word_count', 0)
        
        if word_count < 500:
            return 'Low'
        elif word_count < 2000:
            return 'Medium'
        else:
            return 'High'

def main():
    """Main Streamlit application."""
    
    # Initialize analyzer
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = StandaloneLegalAnalyzer()
    
    analyzer = st.session_state.analyzer
    
    # Header
    st.markdown('<h1 class="main-header">⚖️ Legal Document Analyzer</h1>', unsafe_allow_html=True)
    
    # Mode information and file support
    supported_formats = analyzer.supported_formats
    available_formats = [fmt.upper() for fmt, available in supported_formats.items() if available]
    
    st.markdown(f"""
    <div class="file-support-info">
        <strong>📁 Multi-Format Document Analyzer</strong><br>
        <strong>Supported formats:</strong> {', '.join(available_formats)}<br>
        <strong>Analysis mode:</strong> Rule-based with enhanced clause simplification<br>
        <strong>Clause processing:</strong> Up to 20 clauses with full simplification
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("📋 Analysis Options")
    
    # Clause processing options
    st.sidebar.subheader("🔧 Clause Processing")
    max_clauses_to_process = st.sidebar.slider("Max Clauses to Process", 5, 50, 20)
    show_original_clauses = st.sidebar.checkbox("Show Original Clauses", value=True)
    show_simplified_clauses = st.sidebar.checkbox("Show Simplified Clauses", value=True)
    
    # File format support
    st.sidebar.subheader("📁 Supported Formats")
    for fmt, available in supported_formats.items():
        status = "✅" if available else "❌"
        st.sidebar.write(f"{status} {fmt.upper()} files")
    
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.info(
        "Enhanced Legal Document Analyzer:\n\n"
        "• Multi-format support (TXT, DOCX, PDF)\n"
        "• Advanced document classification\n"
        "• Comprehensive entity extraction\n"
        "• Full clause simplification\n"
        "• Beautiful gradient backgrounds\n"
        "• Export capabilities"
    )
    
    # Main content
    tab1, tab2 = st.tabs(["📄 Document Analysis", "🔍 Quick Analysis"])
    
    with tab1:
        st.markdown('<h2 class="section-header">Upload Document for Analysis</h2>', unsafe_allow_html=True)
        
        # File upload with dynamic format support
        available_extensions = [fmt for fmt, available in supported_formats.items() if available]
        
        st.info(f"📁 Upload a legal document in any supported format: {', '.join([f.upper() for f in available_extensions])}")
        uploaded_file = st.file_uploader(
            "Choose a legal document",
            type=available_extensions,
            help=f"Upload a legal document for analysis. Supported formats: {', '.join(available_extensions)}"
        )
        
        if uploaded_file is not None:
            # Display file info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Name", uploaded_file.name)
            with col2:
                st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
            with col3:
                st.metric("File Type", uploaded_file.type)
            
            # Analyze button
            if st.button("🔍 Analyze Document", type="primary"):
                try:
                    # Save uploaded file temporarily with correct extension
                    file_extension = os.path.splitext(uploaded_file.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # Analyze document with user settings
                    with st.spinner("Analyzing document..."):
                        analysis_result = analyzer.analyze_document(tmp_file_path, max_clauses_to_process)
                    
                    # Clean up temporary file
                    os.unlink(tmp_file_path)
                    
                    # Display results
                    st.success("✅ Analysis completed successfully!")
                    
                    # Document Overview
                    st.markdown('<h2 class="section-header">📋 Document Overview</h2>', unsafe_allow_html=True)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Document Type", analysis_result['classification']['predicted_type'].replace('_', ' ').title())
                    with col2:
                        st.metric("Confidence", f"{analysis_result['classification']['confidence']:.1%}")
                    with col3:
                        st.metric("Word Count", analysis_result['text_statistics']['word_count'])
                    with col4:
                        st.metric("Clauses Found", analysis_result['clauses']['total_count'])
                    
                    # Document Summary
                    st.markdown('<h2 class="section-header">📝 Document Summary</h2>', unsafe_allow_html=True)
                    summary = analysis_result.get('summary', {})
                    
                    if summary.get('key_findings'):
                        st.write("**Key Findings:**")
                        for finding in summary['key_findings']:
                            st.write(f"• {finding}")
                    
                    if analysis_result.get('recommendations'):
                        st.write("**Recommendations:**")
                        for recommendation in analysis_result['recommendations']:
                            st.write(f"• {recommendation}")
                    
                    # Named Entities
                    st.markdown('<h2 class="section-header">🏷️ Extracted Entities</h2>', unsafe_allow_html=True)
                    entities = analysis_result['entities']
                    
                    if entities.get('key_parties'):
                        st.write("**Key Parties:**")
                        parties_html = ""
                        for party in entities['key_parties'][:5]:
                            parties_html += f'<span class="entity-tag">{party["name"]}</span> '
                        st.markdown(parties_html, unsafe_allow_html=True)
                    
                    if entities.get('entities', {}).get('monetary_values'):
                        st.write("**Monetary Values:**")
                        money_html = ""
                        for money in entities['entities']['monetary_values'][:5]:
                            money_html += f'<span class="entity-tag">{money["text"]}</span> '
                        st.markdown(money_html, unsafe_allow_html=True)
                    
                    # Enhanced Clauses Display
                    if analysis_result['clauses']['simplified_clauses']:
                        st.markdown('<h2 class="section-header">📋 Legal Clauses Analysis</h2>', unsafe_allow_html=True)
                        
                        # Show processing info
                        total_clauses = len(analysis_result['clauses']['simplified_clauses'])
                        st.info(f"📊 Processed {total_clauses} clauses with full simplification")
                        
                        for clause_data in analysis_result['clauses']['simplified_clauses']:
                            clause_num = clause_data.get('clause_number', 'N/A')
                            with st.expander(f"📄 Clause {clause_num} - Click to expand", expanded=False):
                                
                                # Show original clause if enabled
                                if show_original_clauses:
                                    st.markdown('<div class="clause-header">📜 Original Legal Text:</div>', unsafe_allow_html=True)
                                    original_text = clause_data["original_clause"]
                                    if len(original_text) > 1000:
                                        original_text = original_text[:1000] + "..."
                                    st.markdown(f'<div class="clause-box">{original_text}</div>', unsafe_allow_html=True)
                                
                                # Show simplified clause if enabled
                                if show_simplified_clauses:
                                    st.markdown('<div class="clause-header">✨ Simplified Version:</div>', unsafe_allow_html=True)
                                    simplified_text = clause_data["simplified_clause"]
                                    if len(simplified_text) > 1000:
                                        simplified_text = simplified_text[:1000] + "..."
                                    st.markdown(f'<div class="simplified-clause">{simplified_text}</div>', unsafe_allow_html=True)
                                
                                # Plain English Summary
                                if clause_data.get('plain_english_summary'):
                                    st.markdown("**🎯 Plain English Summary:**")
                                    st.success(clause_data['plain_english_summary'])
                                
                                # Key Points
                                if clause_data.get('key_points'):
                                    st.markdown("**🔑 Key Points:**")
                                    for point in clause_data['key_points']:
                                        st.write(f"• {point}")
                                
                                # Simplification score
                                score = clause_data.get('simplification_score', 0)
                                st.metric("Simplification Score", f"{score:.1%}", help="How much the clause was simplified")
                    
                    # Export options
                    st.markdown('<h2 class="section-header">💾 Export Results</h2>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        json_data = json.dumps(analysis_result, indent=2, default=str)
                        st.download_button(
                            label="📄 Download JSON",
                            data=json_data,
                            file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            mime="application/json"
                        )
                    
                    with col2:
                        summary_report = f"""LEGAL DOCUMENT ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DOCUMENT INFORMATION
====================
File: {analysis_result['document_info']['file_name']}
Type: {analysis_result['classification']['predicted_type'].replace('_', ' ').title()}
Confidence: {analysis_result['classification']['confidence']:.1%}
Word Count: {analysis_result['text_statistics']['word_count']}
Clauses Found: {analysis_result['clauses']['total_count']}

SUMMARY
=======
Key Findings:
{chr(10).join(['• ' + finding for finding in summary.get('key_findings', [])])}

Recommendations:
{chr(10).join(['• ' + rec for rec in analysis_result.get('recommendations', [])])}
"""
                        st.download_button(
                            label="📋 Download Report",
                            data=summary_report,
                            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    
                except Exception as e:
                    st.error(f"Error analyzing document: {str(e)}")
    
    with tab2:
        st.markdown('<h2 class="section-header">Quick Text Analysis</h2>', unsafe_allow_html=True)
        
        st.write("Paste a legal text snippet for quick analysis:")
        
        text_input = st.text_area(
            "Legal Text",
            height=200,
            placeholder="Paste your legal text here..."
        )
        
        if st.button("🔍 Quick Analyze", type="primary") and text_input.strip():
            try:
                with st.spinner("Analyzing text..."):
                    # Quick analysis
                    classification = analyzer._classify_document(text_input)
                    entities = analyzer._extract_entities(text_input)
                    
                    result = {
                        'classification': classification,
                        'entities': entities,
                        'word_count': len(text_input.split()),
                        'character_count': len(text_input)
                    }
                
                # Display quick results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Document Type", result['classification']['predicted_type'].replace('_', ' ').title())
                with col2:
                    st.metric("Word Count", result['word_count'])
                with col3:
                    st.metric("Character Count", result['character_count'])
                
                if result.get('entities', {}).get('entities'):
                    st.write("**Entities Found:**")
                    for entity_type, entities in result['entities']['entities'].items():
                        if entities:
                            st.write(f"• {entity_type.replace('_', ' ').title()}: {len(entities)}")
                
            except Exception as e:
                st.error(f"Error in quick analysis: {str(e)}")

if __name__ == "__main__":
    main()