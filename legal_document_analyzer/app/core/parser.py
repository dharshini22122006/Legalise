"""Document parsing module for PDF, DOCX, and TXT files."""

import fitz  # PyMuPDF
from docx import Document
from typing import List, Dict, Any
import os
try:
    from ..utils import get_logger
except ImportError:
    # Fallback for when running as script
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from utils import get_logger

logger = get_logger(__name__)

class DocumentParser:
    """Document parser for multiple file formats."""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.txt']
    
    def parse_document(self, file_path: str) -> Dict[str, Any]:
        """Parse document and extract text content."""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return self._parse_pdf(file_path)
            elif file_extension == '.docx':
                return self._parse_docx(file_path)
            elif file_extension == '.txt':
                return self._parse_txt(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            logger.error(f"Error parsing document {file_path}: {str(e)}")
            raise
    
    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Parse PDF document."""
        try:
            doc = fitz.open(file_path)
            pages = []
            full_text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                pages.append({
                    'page_number': page_num + 1,
                    'text': text
                })
                full_text += text + "\n"
            
            doc.close()
            
            return {
                'file_type': 'pdf',
                'total_pages': len(pages),
                'pages': pages,
                'full_text': full_text.strip(),
                'metadata': {
                    'file_name': os.path.basename(file_path),
                    'file_size': os.path.getsize(file_path)
                }
            }
            
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {str(e)}")
            raise
    
    def _parse_docx(self, file_path: str) -> Dict[str, Any]:
        """Parse DOCX document."""
        try:
            doc = Document(file_path)
            paragraphs = []
            full_text = ""
            
            for i, paragraph in enumerate(doc.paragraphs):
                if paragraph.text.strip():
                    paragraphs.append({
                        'paragraph_number': i + 1,
                        'text': paragraph.text
                    })
                    full_text += paragraph.text + "\n"
            
            return {
                'file_type': 'docx',
                'total_paragraphs': len(paragraphs),
                'paragraphs': paragraphs,
                'full_text': full_text.strip(),
                'metadata': {
                    'file_name': os.path.basename(file_path),
                    'file_size': os.path.getsize(file_path)
                }
            }
            
        except Exception as e:
            logger.error(f"Error parsing DOCX {file_path}: {str(e)}")
            raise
    
    def _parse_txt(self, file_path: str) -> Dict[str, Any]:
        """Parse TXT document."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            return {
                'file_type': 'txt',
                'total_lines': len(lines),
                'non_empty_lines': len(non_empty_lines),
                'full_text': content,
                'metadata': {
                    'file_name': os.path.basename(file_path),
                    'file_size': os.path.getsize(file_path)
                }
            }
            
        except Exception as e:
            logger.error(f"Error parsing TXT {file_path}: {str(e)}")
            raise
    
    def extract_clauses(self, text: str) -> List[str]:
        """Extract individual clauses from text."""
        # Simple clause extraction based on common patterns
        clauses = []
        
        # Split by common clause indicators
        clause_indicators = [
            '\n\n',  # Double newline
            '. ',    # Period followed by space
            '; ',    # Semicolon followed by space
        ]
        
        current_text = text
        for indicator in clause_indicators:
            parts = current_text.split(indicator)
            if len(parts) > 1:
                clauses.extend([part.strip() for part in parts if part.strip()])
                break
        
        # If no clauses found, return the whole text as one clause
        if not clauses:
            clauses = [text.strip()]
        
        # Filter out very short clauses (likely not meaningful)
        meaningful_clauses = [clause for clause in clauses if len(clause) > 50]
        
        return meaningful_clauses if meaningful_clauses else clauses