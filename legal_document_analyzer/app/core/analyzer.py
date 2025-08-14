"""Main analyzer orchestrator for legal document analysis."""

import asyncio
from typing import Dict, Any, List, Optional
from .parser import DocumentParser
from .preprocessor import TextPreprocessor
from .ner import LegalNER
from .classifier import DocumentClassifier
from .simplifier import GraniteSimplifier
from ..utils import get_logger, cached

logger = get_logger(__name__)

class LegalDocumentAnalyzer:
    """Main orchestrator for legal document analysis."""
    
    def __init__(self):
        self.parser = DocumentParser()
        self.preprocessor = TextPreprocessor()
        self.ner = LegalNER()
        self.classifier = DocumentClassifier()
        self.simplifier = GraniteSimplifier()
    
    async def analyze_document(self, file_path: str, include_simplification: bool = True) -> Dict[str, Any]:
        """Complete document analysis pipeline."""
        try:
            logger.info(f"Starting analysis of document: {file_path}")
            
            # Step 1: Parse document
            logger.info("Step 1: Parsing document...")
            parsed_doc = self.parser.parse_document(file_path)
            
            # Step 2: Preprocess text
            logger.info("Step 2: Preprocessing text...")
            preprocessed = self.preprocessor.preprocess_document(parsed_doc['full_text'])
            
            # Step 3: Classify document type
            logger.info("Step 3: Classifying document type...")
            classification = self.classifier.classify_document(preprocessed['cleaned_text'])
            
            # Step 4: Extract entities
            logger.info("Step 4: Extracting named entities...")
            entities = self.ner.analyze_document_entities(preprocessed['cleaned_text'])
            
            # Step 5: Extract clauses
            logger.info("Step 5: Extracting clauses...")
            clauses = self.parser.extract_clauses(preprocessed['cleaned_text'])
            
            # Step 6: Simplify clauses (if requested)
            simplified_clauses = []
            if include_simplification and clauses:
                logger.info("Step 6: Simplifying clauses...")
                simplified_clauses = await self._simplify_clauses_async(clauses)
            
            # Step 7: Generate document characteristics
            logger.info("Step 7: Analyzing document characteristics...")
            characteristics = self.classifier.get_document_characteristics(
                preprocessed['cleaned_text'], 
                classification['predicted_type']
            )
            
            # Step 8: Compile comprehensive analysis
            analysis_result = {
                'document_info': {
                    'file_name': parsed_doc['metadata']['file_name'],
                    'file_type': parsed_doc['file_type'],
                    'file_size': parsed_doc['metadata']['file_size'],
                    'analysis_timestamp': self._get_timestamp()
                },
                'classification': classification,
                'characteristics': characteristics,
                'text_statistics': preprocessed['statistics'],
                'entities': entities,
                'clauses': {
                    'total_count': len(clauses),
                    'extracted_clauses': clauses,
                    'simplified_clauses': simplified_clauses
                },
                'summary': self._generate_document_summary(
                    classification, entities, characteristics, preprocessed['statistics']
                ),
                'recommendations': self._generate_recommendations(classification, entities)
            }
            
            logger.info("Document analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in document analysis: {str(e)}")
            raise
    
    async def _simplify_clauses_async(self, clauses: List[str]) -> List[Dict[str, Any]]:
        """Simplify clauses asynchronously."""
        try:
            # For now, we'll run synchronously but can be made async later
            simplified_clauses = []
            
            for i, clause in enumerate(clauses[:10]):  # Limit to first 10 clauses
                logger.info(f"Simplifying clause {i+1}/{min(len(clauses), 10)}")
                simplified = self.simplifier.simplify_clause(clause)
                simplified_clauses.append(simplified)
            
            return simplified_clauses
            
        except Exception as e:
            logger.error(f"Error simplifying clauses: {str(e)}")
            return []
    
    def _generate_document_summary(self, classification: Dict, entities: Dict, 
                                 characteristics: Dict, statistics: Dict) -> Dict[str, Any]:
        """Generate a comprehensive document summary."""
        try:
            summary = {
                'document_type': classification['predicted_type'],
                'confidence': classification['confidence'],
                'key_findings': [],
                'important_entities': {},
                'document_complexity': self._assess_complexity(statistics),
                'key_recommendations': []
            }
            
            # Extract important entities
            if entities.get('key_parties'):
                summary['important_entities']['parties'] = [
                    party['name'] for party in entities['key_parties'][:3]
                ]
            
            if entities.get('entities', {}).get('monetary_values'):
                summary['important_entities']['monetary_values'] = [
                    entity['text'] for entity in entities['entities']['monetary_values'][:3]
                ]
            
            if entities.get('dates_and_deadlines'):
                summary['important_entities']['important_dates'] = [
                    date['text'] for date in entities['dates_and_deadlines'][:3]
                ]
            
            # Generate key findings
            summary['key_findings'] = self._generate_key_findings(classification, entities, characteristics)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating document summary: {str(e)}")
            return {'document_type': 'unknown', 'confidence': 0.0, 'key_findings': []}
    
    def _generate_key_findings(self, classification: Dict, entities: Dict, characteristics: Dict) -> List[str]:
        """Generate key findings from the analysis."""
        findings = []
        
        # Document type finding
        if classification['is_confident']:
            findings.append(f"Document identified as {classification['predicted_type'].replace('_', ' ').title()}")
        
        # Entity findings
        if entities.get('key_parties'):
            party_count = len(entities['key_parties'])
            findings.append(f"Found {party_count} key parties involved")
        
        if entities.get('obligations'):
            obligation_count = len(entities['obligations'])
            findings.append(f"Identified {obligation_count} obligations or responsibilities")
        
        if entities.get('dates_and_deadlines'):
            date_count = len(entities['dates_and_deadlines'])
            findings.append(f"Found {date_count} important dates or deadlines")
        
        # Monetary findings
        monetary_entities = entities.get('entities', {}).get('monetary_values', [])
        if monetary_entities:
            findings.append(f"Contains {len(monetary_entities)} monetary references")
        
        return findings[:5]  # Limit to top 5 findings
    
    def _generate_recommendations(self, classification: Dict, entities: Dict) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Type-specific recommendations
        doc_type = classification['predicted_type']
        
        if doc_type == 'nda':
            recommendations.extend([
                "Review confidentiality scope and duration",
                "Ensure mutual obligations are clearly defined",
                "Verify return/destruction of confidential information clauses"
            ])
        elif doc_type == 'employment_contract':
            recommendations.extend([
                "Review compensation and benefits details",
                "Check termination and notice period clauses",
                "Verify non-compete and confidentiality provisions"
            ])
        elif doc_type == 'service_agreement':
            recommendations.extend([
                "Clarify scope of work and deliverables",
                "Review payment terms and schedule",
                "Check liability and indemnification clauses"
            ])
        elif doc_type == 'lease_agreement':
            recommendations.extend([
                "Verify rent amount and payment schedule",
                "Review security deposit and return conditions",
                "Check maintenance and repair responsibilities"
            ])
        
        # General recommendations
        if entities.get('dates_and_deadlines'):
            recommendations.append("Pay attention to all dates and deadlines mentioned")
        
        if entities.get('obligations'):
            recommendations.append("Carefully review all obligations and responsibilities")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    def _assess_complexity(self, statistics: Dict) -> str:
        """Assess document complexity based on statistics."""
        word_count = statistics.get('word_count', 0)
        sentence_count = statistics.get('sentence_count', 0)
        
        if word_count < 500:
            return 'Low'
        elif word_count < 2000:
            return 'Medium'
        else:
            return 'High'
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    @cached(ttl=1800)  # Cache for 30 minutes
    def quick_analyze(self, text: str) -> Dict[str, Any]:
        """Quick analysis for text snippets."""
        try:
            # Quick preprocessing
            cleaned_text = self.preprocessor.clean_text(text)
            
            # Quick classification
            classification = self.classifier.classify_document(cleaned_text)
            
            # Quick entity extraction
            entities = self.ner.extract_entities(cleaned_text)
            
            return {
                'classification': classification,
                'entities': entities,
                'word_count': len(cleaned_text.split()),
                'character_count': len(cleaned_text)
            }
            
        except Exception as e:
            logger.error(f"Error in quick analysis: {str(e)}")
            raise