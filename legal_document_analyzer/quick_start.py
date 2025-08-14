"""Quick start script for testing the legal document analyzer without heavy dependencies."""

import sys
import os
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def test_basic_functionality():
    """Test basic functionality without heavy ML models."""
    print("🔍 Testing Legal Document Analyzer Components...")
    print("=" * 60)
    
    try:
        # Test imports
        print("✅ Testing imports...")
        from app.utils.config import Config
        from app.utils.logging_config import setup_logging, get_logger
        
        # Setup logging
        setup_logging()
        logger = get_logger(__name__)
        
        print("✅ Configuration and logging modules loaded successfully")
        
        # Test configuration
        print("✅ Testing configuration...")
        model_config = Config.get_model_config()
        processing_config = Config.get_processing_config()
        
        print(f"   Model: {model_config['model_name']}")
        print(f"   Max file size: {processing_config['max_file_size'] / (1024*1024):.1f}MB")
        print(f"   Supported formats: {processing_config['supported_formats']}")
        
        # Test document parser (without actual parsing)
        print("✅ Testing document parser structure...")
        from app.core.parser import DocumentParser
        parser = DocumentParser()
        print(f"   Supported formats: {parser.supported_formats}")
        
        # Test cache system
        print("✅ Testing optimized cache system...")
        from app.utils.cache import cache
        
        # Test cache operations
        cache.set("test_key", "test_value")
        cached_value = cache.get("test_key")
        assert cached_value == "test_value", "Cache test failed"
        
        stats = cache.get_stats()
        print(f"   Cache stats: {stats}")
        
        print("\n🎉 Basic functionality test completed successfully!")
        print("📊 System is ready for full analysis once dependencies are installed.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

def check_dependencies():
    """Check which dependencies are available."""
    print("\n🔍 Checking Dependencies...")
    print("=" * 40)
    
    dependencies = [
        ("streamlit", "Web UI framework"),
        ("fastapi", "API framework"),
        ("transformers", "ML models"),
        ("torch", "PyTorch"),
        ("PyMuPDF", "PDF processing"),
        ("python-docx", "Word document processing"),
        ("spacy", "NLP processing"),
        ("pandas", "Data processing"),
        ("numpy", "Numerical computing")
    ]
    
    available = []
    missing = []
    
    for dep, description in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            available.append((dep, description))
            print(f"✅ {dep:<15} - {description}")
        except ImportError:
            missing.append((dep, description))
            print(f"❌ {dep:<15} - {description} (Not installed)")
    
    print(f"\n📊 Summary: {len(available)}/{len(dependencies)} dependencies available")
    
    if missing:
        print("\n📦 To install missing dependencies:")
        print("   pip install " + " ".join([dep for dep, _ in missing]))
    
    return len(missing) == 0

def main():
    """Main function."""
    print("⚖️ Legal Document Analyzer - Quick Start")
    print("=" * 50)
    
    # Test basic functionality
    basic_test_passed = test_basic_functionality()
    
    # Check dependencies
    all_deps_available = check_dependencies()
    
    if basic_test_passed and all_deps_available:
        print("\n🚀 Ready to run full application!")
        print("   Run: python run.py")
    elif basic_test_passed:
        print("\n⚠️  Basic functionality works, but some dependencies are missing.")
        print("   Install missing dependencies and then run: python run.py")
    else:
        print("\n❌ Basic functionality test failed. Please check the setup.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()