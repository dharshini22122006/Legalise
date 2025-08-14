#!/usr/bin/env python3
"""Test script to check if the Streamlit app works correctly."""

import sys
import os
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def test_imports():
    """Test if all imports work correctly."""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from docx import Document
        print("✅ python-docx imported successfully")
    except ImportError as e:
        print(f"⚠️ python-docx import failed: {e}")
    
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"⚠️ PyPDF2 import failed: {e}")
    
    try:
        import fitz  # PyMuPDF
        print("✅ PyMuPDF imported successfully")
    except ImportError as e:
        print(f"⚠️ PyMuPDF import failed: {e}")
    
    return True

def test_analyzer():
    """Test the standalone analyzer."""
    print("\nTesting StandaloneLegalAnalyzer...")
    
    try:
        # Import the analyzer from streamlit_app
        from streamlit_app import StandaloneLegalAnalyzer
        
        analyzer = StandaloneLegalAnalyzer()
        print("✅ StandaloneLegalAnalyzer created successfully")
        
        # Test with sample text
        sample_text = """
        This is a Non-Disclosure Agreement between Company A and Company B.
        The parties agree to keep confidential information secret for a period of 2 years.
        Payment of $10,000 is due within 30 days.
        """
        
        # Test classification
        classification = analyzer._classify_document(sample_text)
        print(f"✅ Document classification: {classification['predicted_type']}")
        
        # Test entity extraction
        entities = analyzer._extract_entities(sample_text)
        print(f"✅ Entity extraction completed: {entities['total_entities']} entities found")
        
        # Test clause extraction
        clauses = analyzer._extract_clauses(sample_text)
        print(f"✅ Clause extraction completed: {len(clauses)} clauses found")
        
        return True
        
    except Exception as e:
        print(f"❌ Analyzer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sample_document():
    """Test with a sample document."""
    print("\nTesting with sample document...")
    
    try:
        from streamlit_app import StandaloneLegalAnalyzer
        
        analyzer = StandaloneLegalAnalyzer()
        
        # Test with sample NDA
        sample_file = "sample_documents/sample_nda.txt"
        if os.path.exists(sample_file):
            result = analyzer.analyze_document(sample_file, max_clauses=5)
            print(f"✅ Sample document analysis completed")
            print(f"   - Document type: {result['classification']['predicted_type']}")
            print(f"   - Confidence: {result['classification']['confidence']:.2%}")
            print(f"   - Word count: {result['text_statistics']['word_count']}")
            print(f"   - Clauses found: {result['clauses']['total_count']}")
            return True
        else:
            print(f"⚠️ Sample file not found: {sample_file}")
            return False
            
    except Exception as e:
        print(f"❌ Sample document test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🔍 Testing Legal Document Analyzer Streamlit App")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test analyzer
    if not test_analyzer():
        success = False
    
    # Test sample document
    if not test_sample_document():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! The app should work correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    main()
