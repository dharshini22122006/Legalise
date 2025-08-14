"""Setup script for the Legal Document Analyzer."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="legal-document-analyzer",
    version="1.0.0",
    author="Legal Document Analyzer Team",
    author_email="team@legaldocanalyzer.com",
    description="AI-powered legal document analysis using Granite model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/legal-document-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Legal",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.28.1",
        "transformers>=4.35.2",
        "torch>=2.1.1",
        "PyMuPDF>=1.23.8",
        "python-docx>=0.8.11",
        "spacy>=3.7.2",
        "pandas>=2.1.3",
        "numpy>=1.24.3",
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "python-multipart>=0.0.6",
        "aiofiles>=23.2.1",
        "pydantic>=2.5.0",
        "requests>=2.31.0",
        "Pillow>=10.1.0",
        "plotly>=5.17.0",
        "nltk>=3.8.1",
        "scikit-learn>=1.3.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "legal-analyzer=run:main",
        ],
    },
)