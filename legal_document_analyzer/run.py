"""Application entry point for the Legal Document Analyzer."""

import sys
import os
import subprocess
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def run_streamlit():
    """Run the Streamlit application."""
    try:
        # Set environment variables
        os.environ["STREAMLIT_SERVER_PORT"] = "8501"
        os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
        
        # Check if we can import the full version
        main_file = "main.py"
        try:
            # Test import to see if ML dependencies are available
            import transformers
            print("✅ ML dependencies available - using full version")
        except ImportError:
            print("⚠️  ML dependencies not available - using minimal version")
            main_file = "main_minimal.py"
        
        # Run Streamlit
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            str(app_dir / main_file),
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--server.headless=true"
        ]
        
        print("🚀 Starting Legal Document Analyzer...")
        print("📍 Application will be available at: http://localhost:8501")
        if main_file == "main.py":
            print("⚖️ Powered by Granite AI Model")
        else:
            print("🔧 Running in Minimal Mode (Rule-based Analysis)")
        print("-" * 50)
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")
        sys.exit(1)

def main():
    """Main entry point."""
    print("⚖️ Legal Document Analyzer")
    print("=" * 50)
    
    # Check if required directories exist
    required_dirs = [
        app_dir,
        app_dir / "core",
        app_dir / "utils"
    ]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            print(f"❌ Required directory not found: {dir_path}")
            sys.exit(1)
    
    # Run the application
    run_streamlit()

if __name__ == "__main__":
    main()