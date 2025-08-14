#!/usr/bin/env python3
"""
Enhanced Legal Document Analyzer Runner
Provides multiple ways to run and test the analyzer.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'docx',
        'PyPDF2',
        'fitz',  # PyMuPDF
        'pandas',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'docx':
                import docx
            elif package == 'fitz':
                import fitz
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All dependencies are installed!")
    return True

def run_streamlit_app(port=8501):
    """Run the Streamlit app."""
    print(f"🚀 Starting Streamlit app on port {port}...")
    
    try:
        cmd = [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", str(port)]
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Streamlit app: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped by user")
        return True

def run_tests():
    """Run all tests."""
    print("🧪 Running tests...")
    
    test_files = [
        "test_streamlit_app.py",
        "test_multi_format.py"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📋 Running {test_file}...")
            try:
                result = subprocess.run([sys.executable, test_file], 
                                      capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"✅ {test_file} passed")
                else:
                    print(f"❌ {test_file} failed")
                    print(result.stderr)
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_file} timed out")
            except Exception as e:
                print(f"❌ Error running {test_file}: {e}")
        else:
            print(f"⚠️ {test_file} not found")

def run_demo():
    """Run the comprehensive demo."""
    print("🎬 Running comprehensive demo...")
    
    if os.path.exists("demo_multi_format.py"):
        try:
            subprocess.run([sys.executable, "demo_multi_format.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Demo failed: {e}")
        except KeyboardInterrupt:
            print("\n👋 Demo stopped by user")
    else:
        print("⚠️ demo_multi_format.py not found")

def show_info():
    """Show information about the analyzer."""
    print("📋 LEGAL DOCUMENT ANALYZER INFORMATION")
    print("=" * 50)
    print("🎯 Features:")
    print("  • Multi-format support (TXT, DOCX, PDF)")
    print("  • Document classification (NDA, Employment, Service Agreement, etc.)")
    print("  • Entity extraction (parties, dates, money, emails, phones)")
    print("  • Clause extraction and simplification")
    print("  • Plain English summaries")
    print("  • Interactive Streamlit web interface")
    print("  • Export capabilities (JSON, TXT reports)")
    
    print("\n🔧 Supported File Formats:")
    print("  • TXT - Plain text files")
    print("  • DOCX - Microsoft Word documents")
    print("  • PDF - Portable Document Format (with PyPDF2)")
    
    print("\n📁 Sample Documents Available:")
    sample_dir = Path("sample_documents")
    if sample_dir.exists():
        for file in sample_dir.glob("*.txt"):
            print(f"  • {file.name}")
    
    print("\n🚀 Usage:")
    print("  python run_analyzer.py --streamlit    # Run web interface")
    print("  python run_analyzer.py --test         # Run tests")
    print("  python run_analyzer.py --demo         # Run demo")
    print("  python run_analyzer.py --check        # Check dependencies")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Legal Document Analyzer Runner")
    parser.add_argument("--streamlit", action="store_true", help="Run Streamlit app")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    parser.add_argument("--check", action="store_true", help="Check dependencies")
    parser.add_argument("--port", type=int, default=8501, help="Streamlit port (default: 8501)")
    parser.add_argument("--info", action="store_true", help="Show information")
    
    args = parser.parse_args()
    
    # If no arguments provided, show info and run streamlit
    if not any([args.streamlit, args.test, args.demo, args.check, args.info]):
        show_info()
        print("\n🚀 Starting Streamlit app by default...")
        args.streamlit = True
    
    if args.info:
        show_info()
    
    if args.check:
        if not check_dependencies():
            sys.exit(1)
    
    if args.test:
        run_tests()
    
    if args.demo:
        run_demo()
    
    if args.streamlit:
        # Check dependencies first
        if not check_dependencies():
            print("❌ Cannot start Streamlit app due to missing dependencies")
            sys.exit(1)
        
        run_streamlit_app(args.port)

if __name__ == "__main__":
    main()
