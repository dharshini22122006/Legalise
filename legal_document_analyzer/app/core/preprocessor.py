"""Text preprocessing module for legal documents."""

import re
from typing import List, Dict, Any
from ..utils import get_logger

logger = get_logger(__name__)

class TextPreprocessor:
    """Text preprocessing for legal documents."""
    
    def __init__(self):
        # Common legal document patterns to clean
        self.noise_patterns = [
            r'\s+',  # Multiple whitespaces
            r'\n+',  # Multiple newlines
            r'\t+',  # Multiple tabs
        ]
        
        # Legal-specific cleaning patterns
        self.legal_patterns = {
            'page_numbers': r'Page\s+\d+\s+of\s+\d+',
            'footer_headers': r'(CONFIDENTIAL|PROPRIETARY|DRAFT)',
            'section_numbers': r'^\d+\.\d*\s*',
            'subsection_letters': r'^\([a-z]\)\s*',
        }
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        try:
            # Remove extra whitespaces
            text = re.sub(r'\s+', ' ', text)
            
            # Remove page numbers and headers/footers
            for pattern_name, pattern in self.legal_patterns.items():
                text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
            
            # Normalize quotes
            text = text.replace('"', '"').replace('"', '"')
            text = text.replace(''', "'").replace(''', "'")
            
            # Remove excessive punctuation
            text = re.sub(r'\.{2,}', '.', text)
            text = re.sub(r',{2,}', ',', text)
            
            # Clean up spacing around punctuation
            text = re.sub(r'\s+([,.;:!?])', r'\1', text)
            text = re.sub(r'([,.;:!?])\s+', r'\1 ', text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error cleaning text: {str(e)}")
            return text
    
    def chunk_text(self, text: str, max_chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks."""
        try:
            words = text.split()
            chunks = []
            
            if len(words) <= max_chunk_size:
                return [{
                    'chunk_id': 0,
                    'text': text,
                    'word_count': len(words),
                    'start_word': 0,
                    'end_word': len(words)
                }]
            
            start = 0
            chunk_id = 0
            
            while start < len(words):
                end = min(start + max_chunk_size, len(words))
                chunk_words = words[start:end]
                chunk_text = ' '.join(chunk_words)
                
                chunks.append({
                    'chunk_id': chunk_id,
                    'text': chunk_text,
                    'word_count': len(chunk_words),
                    'start_word': start,
                    'end_word': end
                })
                
                # Move start position with overlap
                start = end - overlap if end < len(words) else end
                chunk_id += 1
                
                if start >= len(words):
                    break
            
            return chunks
            
        except Exception as e:
            logger.error(f"Error chunking text: {str(e)}")
            return [{'chunk_id': 0, 'text': text, 'word_count': len(text.split()), 'start_word': 0, 'end_word': len(text.split())}]
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text."""
        try:
            # Simple sentence splitting
            sentences = re.split(r'[.!?]+', text)
            
            # Clean and filter sentences
            cleaned_sentences = []
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 10:  # Filter out very short sentences
                    cleaned_sentences.append(sentence)
            
            return cleaned_sentences
            
        except Exception as e:
            logger.error(f"Error extracting sentences: {str(e)}")
            return [text]
    
    def remove_duplicates(self, texts: List[str], similarity_threshold: float = 0.8) -> List[str]:
        """Remove duplicate or highly similar texts."""
        try:
            unique_texts = []
            
            for text in texts:
                is_duplicate = False
                text_words = set(text.lower().split())
                
                for existing_text in unique_texts:
                    existing_words = set(existing_text.lower().split())
                    
                    # Calculate Jaccard similarity
                    if len(text_words) > 0 and len(existing_words) > 0:
                        intersection = len(text_words.intersection(existing_words))
                        union = len(text_words.union(existing_words))
                        similarity = intersection / union
                        
                        if similarity > similarity_threshold:
                            is_duplicate = True
                            break
                
                if not is_duplicate:
                    unique_texts.append(text)
            
            return unique_texts
            
        except Exception as e:
            logger.error(f"Error removing duplicates: {str(e)}")
            return texts
    
    def preprocess_document(self, text: str, max_chunk_size: int = 1000) -> Dict[str, Any]:
        """Complete preprocessing pipeline."""
        try:
            # Clean text
            cleaned_text = self.clean_text(text)
            
            # Extract sentences
            sentences = self.extract_sentences(cleaned_text)
            
            # Remove duplicates
            unique_sentences = self.remove_duplicates(sentences)
            
            # Chunk text
            chunks = self.chunk_text(cleaned_text, max_chunk_size)
            
            return {
                'original_text': text,
                'cleaned_text': cleaned_text,
                'sentences': unique_sentences,
                'chunks': chunks,
                'statistics': {
                    'original_length': len(text),
                    'cleaned_length': len(cleaned_text),
                    'sentence_count': len(unique_sentences),
                    'chunk_count': len(chunks),
                    'word_count': len(cleaned_text.split())
                }
            }
            
        except Exception as e:
            logger.error(f"Error in preprocessing pipeline: {str(e)}")
            raise