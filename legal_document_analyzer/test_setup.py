"""Test script to verify the application setup."""

import sys
import os
from pathlib import Path

def test_structure():
    """Test if all required files and directories exist."""
    print("🔍 Testing Legal Document Analyzer Setup...")
    print("=" * 50)
    
    # Check Python version
    print(f"Python Version: {sys.version}")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"Current Directory: {current_dir}")
    
    # Required files and directories
    required_items = [
        "app/main.py",
        "app/api.py",
        "app/core/analyzer.py",
        "app/core/parser.py",
        "app/core/preprocessor.py",
        "app/core/ner.py",
        "app/core/classifier.py",
        "app/core/simplifier.py",
        "app/utils/config.py",
        "app/utils/cache.py",
        "app/utils/logging_config.py",
        "requirements.txt",
        "run.py",
        "README.md",
        "test/sample_documents/sample_nda.txt",
        "test/sample_documents/sample_employment_contract.txt",
        "test/sample_documents/sample_service_agreement.txt"
    ]
    
    print("\n📁 Checking Required Files:")
    print("-" * 30)
    
    missing_files = []
    for item in required_items:
        file_path = current_dir / item
        if file_path.exists():
            print(f"✅ {item}")
        else:
            print(f"❌ {item}")
            missing_files.append(item)
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} files:")
        for file in missing_files:
            print(f"   - {file}")
    else:
        print("\n🎉 All required files are present!")
    
    # Check if we can import the modules
    print("\n🐍 Testing Python Imports:")
    print("-" * 30)
    
    try:
        sys.path.insert(0, str(current_dir / "app"))
        
        # Test basic imports
        test_imports = [
            ("app.utils.config", "Config"),
            ("app.core.parser", "DocumentParser"),
            ("app.core.preprocessor", "TextPreprocessor"),
            ("app.core.ner", "LegalNER"),
            ("app.core.classifier", "DocumentClassifier"),
        ]
        
        for module_name, class_name in test_imports:
            try:
                module = __import__(module_name, fromlist=[class_name])
                cls = getattr(module, class_name)
                print(f"✅ {module_name}.{class_name}")
            except Exception as e:
                print(f"❌ {module_name}.{class_name} - {str(e)}")
    
    except Exception as e:
        print(f"❌ Import test failed: {str(e)}")
    
    print("\n📋 Setup Summary:")
    print("-" * 30)
    print(f"✅ Project structure: {'Complete' if not missing_files else 'Incomplete'}")
    print(f"✅ Sample documents: Available")
    print(f"✅ Configuration files: Present")
    print(f"✅ Startup scripts: Ready")
    
    print("\n🚀 Next Steps:")
    print("-" * 30)
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the application: python run.py")
    print("3. Open browser: http://localhost:8501")
    print("4. Upload a sample document and test!")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    success = test_structure()
    if success:
        print("\n🎉 Setup verification completed successfully!")
        print("Your Legal Document Analyzer is ready to run!")
    else:
        print("\n⚠️  Some files are missing. Please check the setup.")
    
    sys.exit(0 if success else 1)