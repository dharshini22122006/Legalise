#!/usr/bin/env python3
"""
Verification script for Legal Document Analyzer installation.
This script checks if all components are properly installed and configured.
"""

import sys
import os
import importlib
from pathlib import Path

def print_header(title):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_status(item, status, details=""):
    """Print status with formatting."""
    status_symbol = "✅" if status else "❌"
    print(f"{status_symbol} {item:<40} {details}")

def check_python_version():
    """Check Python version."""
    print_header("PYTHON VERSION CHECK")
    
    version = sys.version_info
    required_major, required_minor = 3, 8
    
    is_valid = version.major >= required_major and version.minor >= required_minor
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_status("Python Version", is_valid, f"v{version_str}")
    
    if not is_valid:
        print(f"❌ Python {required_major}.{required_minor}+ required, found {version_str}")
        return False
    
    return True

def check_project_structure():
    """Check if all required files and directories exist."""
    print_header("PROJECT STRUCTURE CHECK")
    
    base_path = Path(__file__).parent
    
    required_files = [
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
        "README.md"
    ]
    
    required_dirs = [
        "app",
        "app/core",
        "app/utils",
        "app/static",
        "app/static/css",
        "tests",
        "tests/sample_documents",
        "deployment",
        "docs"
    ]
    
    all_good = True
    
    # Check directories
    for dir_path in required_dirs:
        full_path = base_path / dir_path
        exists = full_path.exists() and full_path.is_dir()
        print_status(f"Directory: {dir_path}", exists)
        if not exists:
            all_good = False
    
    # Check files
    for file_path in required_files:
        full_path = base_path / file_path
        exists = full_path.exists() and full_path.is_file()
        print_status(f"File: {file_path}", exists)
        if not exists:
            all_good = False
    
    return all_good

def check_dependencies():
    """Check if required Python packages are available."""
    print_header("DEPENDENCY CHECK")
    
    # Core dependencies that should be available
    core_deps = [
        "pathlib",
        "json",
        "re",
        "datetime",
        "asyncio",
        "typing",
        "logging",
        "tempfile",
        "os",
        "sys"
    ]
    
    # Optional dependencies (will be installed via requirements.txt)
    optional_deps = [
        ("streamlit", "Streamlit web framework"),
        ("transformers", "Hugging Face Transformers"),
        ("torch", "PyTorch deep learning framework"),
        ("fastapi", "FastAPI web framework"),
        ("pandas", "Data manipulation library"),
        ("numpy", "Numerical computing library"),
        ("requests", "HTTP library"),
        ("pydantic", "Data validation library")
    ]
    
    all_good = True
    
    # Check core dependencies
    for dep in core_deps:
        try:
            importlib.import_module(dep)
            print_status(f"Core: {dep}", True, "Built-in")
        except ImportError:
            print_status(f"Core: {dep}", False, "Missing")
            all_good = False
    
    # Check optional dependencies
    for dep, description in optional_deps:
        try:
            importlib.import_module(dep)
            print_status(f"Optional: {dep}", True, description)
        except ImportError:
            print_status(f"Optional: {dep}", False, f"{description} (install with pip)")
    
    return all_good

def check_sample_documents():
    """Check if sample documents exist."""
    print_header("SAMPLE DOCUMENTS CHECK")
    
    base_path = Path(__file__).parent
    sample_dir = base_path / "tests" / "sample_documents"
    
    sample_files = [
        "sample_nda.txt",
        "sample_employment_contract.txt",
        "sample_service_agreement.txt",
        "sample_agreement.txt"
    ]
    
    all_good = True
    
    for file_name in sample_files:
        file_path = sample_dir / file_name
        exists = file_path.exists()
        size = file_path.stat().st_size if exists else 0
        print_status(f"Sample: {file_name}", exists, f"{size} bytes" if exists else "Missing")
        if not exists:
            all_good = False
    
    return all_good

def check_app_imports():
    """Check if app modules can be imported."""
    print_header("APPLICATION IMPORTS CHECK")
    
    # Add app directory to path
    app_path = Path(__file__).parent / "app"
    sys.path.insert(0, str(app_path))
    
    app_modules = [
        ("app.utils.config", "Configuration management"),
        ("app.utils.cache", "Caching utilities"),
        ("app.utils.logging_config", "Logging setup"),
        ("app.core.parser", "Document parser"),
        ("app.core.preprocessor", "Text preprocessor"),
        ("app.core.ner", "Named Entity Recognition"),
        ("app.core.classifier", "Document classifier"),
        ("app.core.simplifier", "Clause simplifier"),
        ("app.core.analyzer", "Main analyzer")
    ]
    
    all_good = True
    
    for module_name, description in app_modules:
        try:
            importlib.import_module(module_name)
            print_status(f"Module: {module_name.split('.')[-1]}", True, description)
        except ImportError as e:
            print_status(f"Module: {module_name.split('.')[-1]}", False, f"Import error: {str(e)}")
            all_good = False
        except Exception as e:
            print_status(f"Module: {module_name.split('.')[-1]}", False, f"Error: {str(e)}")
            all_good = False
    
    return all_good

def generate_installation_report():
    """Generate a comprehensive installation report."""
    print_header("LEGAL DOCUMENT ANALYZER - INSTALLATION VERIFICATION")
    print("🤖 AI-Powered Legal Document Analysis using Granite Model")
    print("📅 Verification Date:", __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Project Structure", check_project_structure),
        ("Dependencies", check_dependencies),
        ("Sample Documents", check_sample_documents),
        ("Application Imports", check_app_imports)
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"❌ Error running {check_name} check: {str(e)}")
            results[check_name] = False
    
    # Summary
    print_header("VERIFICATION SUMMARY")
    
    total_checks = len(results)
    passed_checks = sum(results.values())
    
    for check_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print_status(check_name, passed, status)
    
    print(f"\n📊 Overall Result: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("\n🎉 INSTALLATION VERIFICATION SUCCESSFUL!")
        print("✅ Your Legal Document Analyzer is ready to use!")
        print("\n🚀 Next Steps:")
        print("   1. Install dependencies: pip install -r requirements.txt")
        print("   2. Run the application: python run.py")
        print("   3. Open browser: http://localhost:8501")
        print("   4. Upload a sample document and test!")
    else:
        print("\n⚠️  INSTALLATION VERIFICATION INCOMPLETE")
        print("❌ Some components are missing or not properly configured.")
        print("\n🔧 Recommended Actions:")
        
        if not results.get("Python Version", True):
            print("   • Install Python 3.8 or higher")
        
        if not results.get("Project Structure", True):
            print("   • Ensure all project files are present")
        
        if not results.get("Dependencies", True):
            print("   • Install required dependencies: pip install -r requirements.txt")
        
        if not results.get("Sample Documents", True):
            print("   • Verify sample documents are in tests/sample_documents/")
        
        if not results.get("Application Imports", True):
            print("   • Check for syntax errors in application modules")
    
    return passed_checks == total_checks

def main():
    """Main verification function."""
    try:
        success = generate_installation_report()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during verification: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()