"""Minimal version of the legal document analyzer that runs with basic dependencies."""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, List
import re

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

class MinimalDocumentParser:
    """Minimal document parser for text files."""
    
    def parse_text_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return {
                'file_type': 'txt',
                'full_text': content,
                'metadata': {
                    'file_name': os.path.basename(file_path),
                    'file_size': len(content),
                    'word_count': len(content.split()),
                    'character_count': len(content)
                }
            }
        except Exception as e:
            raise Exception(f"Error parsing text file: {str(e)}")

class MinimalTextProcessor:
    """Minimal text processing utilities."""
    
    def clean_text(self, text: str) -> str:
        """Basic text cleaning."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep legal punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\"\'\/\$\%]', '', text)
        return text.strip()
    
    def extract_basic_statistics(self, text: str) -> Dict[str, Any]:
        """Extract basic text statistics."""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        return {
            'word_count': len(words),
            'character_count': len(text),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'average_sentence_length': len(words) / len(sentences) if sentences else 0
        }

class MinimalLegalAnalyzer:
    """Minimal legal document analyzer using rule-based approaches."""
    
    def __init__(self):
        self.parser = MinimalDocumentParser()
        self.processor = MinimalTextProcessor()
        
        # Legal document patterns
        self.document_patterns = {
            'nda': [
                r'non.?disclosure', r'confidential', r'proprietary', r'trade secret'
            ],
            'employment_contract': [
                r'employment', r'employee', r'employer', r'salary', r'compensation'
            ],
            'service_agreement': [
                r'service', r'provider', r'client', r'deliverable', r'scope of work'
            ],
            'lease_agreement': [
                r'lease', r'rent', r'tenant', r'landlord', r'property'
            ],
            'purchase_agreement': [
                r'purchase', r'buyer', r'seller', r'sale', r'goods'
            ]
        }
        
        # Entity patterns
        self.entity_patterns = {
            'monetary_values': r'\$[\d,]+(?:\.\d{2})?',
            'dates': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            'percentages': r'\d+(?:\.\d+)?%',
            'phone_numbers': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email_addresses': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
    
    def classify_document(self, text: str) -> Dict[str, Any]:
        """Classify document type using pattern matching."""
        text_lower = text.lower()
        scores = {}
        
        for doc_type, patterns in self.document_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            scores[doc_type] = score
        
        # Find the document type with highest score
        predicted_type = max(scores, key=scores.get) if scores else 'unknown'
        max_score = scores.get(predicted_type, 0)
        
        # Calculate confidence based on score and text length
        confidence = min(max_score / (len(text.split()) / 100), 1.0)
        
        return {
            'predicted_type': predicted_type,
            'confidence': confidence,
            'is_confident': confidence > 0.3,
            'scores': scores
        }
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities using regex patterns."""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities[entity_type] = [
                {'text': match, 'type': entity_type}
                for match in set(matches)  # Remove duplicates
            ]
        
        return {
            'entities': entities,
            'total_entities': sum(len(entity_list) for entity_list in entities.values())
        }
    
    def extract_clauses(self, text: str) -> List[str]:
        """Extract potential clauses using simple heuristics."""
        # Split by numbered sections or paragraphs
        clauses = []
        
        # Pattern for numbered sections (1., 2., etc.)
        numbered_sections = re.split(r'\n\s*\d+\.\s*', text)
        if len(numbered_sections) > 1:
            clauses.extend([clause.strip() for clause in numbered_sections[1:] if clause.strip()])
        
        # Pattern for lettered sections (a), b), etc.)
        lettered_sections = re.split(r'\n\s*[a-z]\)\s*', text)
        if len(lettered_sections) > 1:
            clauses.extend([clause.strip() for clause in lettered_sections[1:] if clause.strip()])
        
        # If no structured sections found, split by paragraphs
        if not clauses:
            paragraphs = text.split('\n\n')
            clauses = [p.strip() for p in paragraphs if len(p.strip()) > 50]  # Only substantial paragraphs
        
        return clauses[:10]  # Limit to first 10 clauses
    
    def analyze_document(self, file_path: str) -> Dict[str, Any]:
        """Analyze a legal document."""
        try:
            print(f"📄 Analyzing document: {os.path.basename(file_path)}")
            start_time = time.time()
            
            # Parse document
            parsed_doc = self.parser.parse_text_file(file_path)
            text = parsed_doc['full_text']
            
            # Clean text
            cleaned_text = self.processor.clean_text(text)
            
            # Get statistics
            statistics = self.processor.extract_basic_statistics(cleaned_text)
            
            # Classify document
            classification = self.classify_document(cleaned_text)
            
            # Extract entities
            entities = self.extract_entities(cleaned_text)
            
            # Extract clauses
            clauses = self.extract_clauses(cleaned_text)
            
            # Generate summary
            summary = self._generate_summary(classification, entities, statistics)
            
            analysis_time = time.time() - start_time
            
            result = {
                'document_info': parsed_doc['metadata'],
                'classification': classification,
                'text_statistics': statistics,
                'entities': entities,
                'clauses': {
                    'total_count': len(clauses),
                    'extracted_clauses': clauses
                },
                'summary': summary,
                'analysis_time': analysis_time,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"✅ Analysis completed in {analysis_time:.2f} seconds")
            return result
            
        except Exception as e:
            print(f"❌ Error analyzing document: {str(e)}")
            raise
    
    def _generate_summary(self, classification: Dict, entities: Dict, statistics: Dict) -> Dict[str, Any]:
        """Generate a document summary."""
        summary = {
            'document_type': classification['predicted_type'].replace('_', ' ').title(),
            'confidence': f"{classification['confidence']:.1%}",
            'complexity': self._assess_complexity(statistics),
            'key_findings': []
        }
        
        # Add findings based on entities
        for entity_type, entity_list in entities['entities'].items():
            if entity_list:
                count = len(entity_list)
                summary['key_findings'].append(
                    f"Found {count} {entity_type.replace('_', ' ')}"
                )
        
        return summary
    
    def _assess_complexity(self, statistics: Dict) -> str:
        """Assess document complexity."""
        word_count = statistics.get('word_count', 0)
        avg_sentence_length = statistics.get('average_sentence_length', 0)
        
        if word_count < 500 and avg_sentence_length < 20:
            return 'Low'
        elif word_count < 2000 and avg_sentence_length < 30:
            return 'Medium'
        else:
            return 'High'

def create_sample_documents():
    """Create sample legal documents for testing."""
    samples_dir = Path("sample_documents")
    samples_dir.mkdir(exist_ok=True)
    
    samples = {
        "sample_nda.txt": """NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement (NDA) is entered into on January 15, 2024, between:

Company A Inc., a corporation organized under the laws of Delaware
Company B LLC, a limited liability company organized under the laws of California

1. CONFIDENTIAL INFORMATION
For purposes of this Agreement, "Confidential Information" means any proprietary information, technical data, trade secrets, or know-how disclosed by either party.

2. OBLIGATIONS
Each party agrees to:
a) Maintain strict confidentiality of all Confidential Information
b) Use Confidential Information solely for evaluation purposes
c) Not disclose Confidential Information to third parties

3. TERM
This Agreement shall remain in effect for a period of 5 years from the date of execution.

4. RETURN OF INFORMATION
Upon termination, each party shall return or destroy all Confidential Information.

Contact: legal@companya.com
Phone: 555-123-4567
Value of potential deal: $2,500,000""",

        "sample_employment.txt": """EMPLOYMENT AGREEMENT

This Employment Agreement is made on March 1, 2024, between XYZ Corporation and John Smith.

1. POSITION AND DUTIES
Employee shall serve as Senior Software Engineer and shall perform the following duties:
a) Design and develop software applications
b) Conduct code reviews and testing
c) Mentor junior developers
d) Participate in project planning meetings

2. COMPENSATION
Employee shall receive:
a) Base salary of $95,000 per year
b) Performance bonus up to 15% of base salary
c) Stock options for 1,000 shares

3. BENEFITS
Employee is entitled to:
a) Health insurance (company pays 80%)
b) Dental and vision coverage
c) 401(k) with 4% company matching
d) 20 days paid vacation annually

4. TERMINATION
Either party may terminate this agreement with 30 days written notice.

HR Contact: hr@xyzcorp.com
Start Date: April 1, 2024""",

        "sample_service.txt": """SERVICE AGREEMENT

This Service Agreement is entered into on February 10, 2024, between ABC Consulting Services and Tech Startup Inc.

1. SCOPE OF WORK
Provider agrees to deliver the following services:
a) Web application development using React and Node.js
b) Database design and implementation
c) User interface design and user experience optimization
d) Quality assurance testing and bug fixes
e) Deployment and maintenance services

2. TIMELINE AND DELIVERABLES
Phase 1: Requirements and Design (4 weeks) - Due March 10, 2024
Phase 2: Development (8 weeks) - Due May 5, 2024
Phase 3: Testing and Deployment (2 weeks) - Due May 19, 2024

3. PAYMENT TERMS
Total project cost: $75,000
Payment schedule:
a) 30% upon signing ($22,500)
b) 40% upon Phase 1 completion ($30,000)
c) 30% upon final delivery ($22,500)

4. INTELLECTUAL PROPERTY
All work products shall be owned by Client upon full payment.

Project Manager: pm@abcconsulting.com
Client Contact: cto@techstartup.com"""
    }
    
    for filename, content in samples.items():
        file_path = samples_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return samples_dir

def main():
    """Main function to run the minimal analyzer."""
    print("⚖️ Minimal Legal Document Analyzer")
    print("=" * 50)
    print("🔧 Running with basic dependencies only")
    print("💡 This version uses rule-based analysis instead of ML models")
    print()
    
    # Create sample documents
    print("📁 Creating sample documents...")
    samples_dir = create_sample_documents()
    print(f"✅ Sample documents created in: {samples_dir}")
    
    # Initialize analyzer
    analyzer = MinimalLegalAnalyzer()
    
    # Analyze sample documents
    sample_files = list(samples_dir.glob("*.txt"))
    
    for file_path in sample_files:
        print(f"\n{'='*60}")
        try:
            result = analyzer.analyze_document(file_path)
            
            # Display results
            print(f"📋 Document: {result['document_info']['file_name']}")
            print(f"📊 Type: {result['summary']['document_type']} (Confidence: {result['summary']['confidence']})")
            print(f"📈 Complexity: {result['summary']['complexity']}")
            print(f"📝 Words: {result['text_statistics']['word_count']}")
            print(f"🔍 Entities found: {result['entities']['total_entities']}")
            print(f"📄 Clauses extracted: {result['clauses']['total_count']}")
            
            if result['summary']['key_findings']:
                print("🎯 Key Findings:")
                for finding in result['summary']['key_findings']:
                    print(f"   • {finding}")
            
            # Save results
            output_file = samples_dir / f"{file_path.stem}_analysis.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"💾 Analysis saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {str(e)}")
    
    print(f"\n{'='*60}")
    print("🎉 Analysis completed!")
    print("📊 This demonstrates the core functionality with minimal dependencies.")
    print("🚀 For full ML-powered analysis, install the complete requirements.")

if __name__ == "__main__":
    main()