"""Core analysis modules for the legal document analyzer."""

# Always use minimal version first to avoid import issues
print("🔄 Using minimal analyzer...")

from analyzer_minimal import MinimalLegalDocumentAnalyzer

# Use minimal analyzer as default
LegalDocumentAnalyzer = MinimalLegalDocumentAnalyzer
ML_AVAILABLE = False

# Create dummy classes for compatibility
class DocumentParser:
    pass
class TextPreprocessor:
    pass
class LegalNER:
    pass
class DocumentClassifier:
    pass
class GraniteSimplifier:
    pass

# Try to import ML-based components if available
try:
    from analyzer import LegalDocumentAnalyzer as OriginalAnalyzer
    from analyzer_optimized import OptimizedLegalDocumentAnalyzer
    from parser import DocumentParser
    from preprocessor import TextPreprocessor
    from ner import LegalNER
    from classifier import DocumentClassifier
    from simplifier import GraniteSimplifier
    
    # Use optimized analyzer if ML dependencies are available
    LegalDocumentAnalyzer = OptimizedLegalDocumentAnalyzer
    ML_AVAILABLE = True
    print("✅ ML dependencies available - using full version")
    
except ImportError as e:
    print(f"⚠️  ML dependencies not available: {e}")
    # Keep using minimal analyzer

__all__ = [
    'LegalDocumentAnalyzer',
    'DocumentParser',
    'TextPreprocessor',
    'LegalNER',
    'DocumentClassifier',
    'GraniteSimplifier',
    'ML_AVAILABLE'
]
