"""Minimal analyzer that works without heavy ML dependencies."""

import asyncio
import concurrent.futures
from typing import Dict, Any, List, Optional
import threading
import re
import os
from datetime import datetime

try:
    import sys
    import os
    # Add parent directory to path for utils import
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback logger when utils are not available
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

class MinimalLegalDocumentAnalyzer:
    """Minimal legal document analyzer using rule-based approaches."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self._initialized = True
        
        # Document classification patterns
        self.document_patterns = {
            'nda': [
                r'non.?disclosure', r'confidential', r'proprietary', r'trade secret',
                r'confidentiality agreement'
            ],
            'employment_contract': [
                r'employment', r'employee', r'employer', r'salary', r'compensation',
                r'job description', r'work agreement'
            ],
            'service_agreement': [
                r'service', r'provider', r'client', r'deliverable', r'scope of work',
                r'consulting', r'professional services'
            ],
            'lease_agreement': [
                r'lease', r'rent', r'tenant', r'landlord', r'property',
                r'rental agreement'
            ],
            'purchase_agreement': [
                r'purchase', r'buyer', r'seller', r'sale', r'goods',
                r'sales agreement'
            ]
        }
        
        # Entity extraction patterns
        self.entity_patterns = {
            'monetary_values': r'\$[\d,]+(?:\.\d{2})?',
            'dates': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            'percentages': r'\d+(?:\.\d+)?%',
            'phone_numbers': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email_addresses': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
        
        # Legal jargon simplification rules
        self.simplification_rules = {
            r'\bheretofore\b': 'before this',
            r'\bhereinafter\b': 'from now on',
            r'\bwhereas\b': 'since',
            r'\btherefore\b': 'so',
            r'\bnotwithstanding\b': 'despite',
            r'\bpursuant to\b': 'according to',
            r'\bshall\b': 'will',
            r'\bin the event that\b': 'if',
            r'\bprior to\b': 'before',
            r'\bsubsequent to\b': 'after'
        }
    
    async def analyze_document(self, file_path: str, include_simplification: bool = True) -> Dict[str, Any]:
        """Complete document analysis pipeline."""
        try:
            logger.info(f"Starting minimal analysis of document: {file_path}")
            
            # Step 1: Parse document
            parsed_doc = await self._parse_document_async(file_path)
            
            # Step 2: Preprocess text
            preprocessed = await self._preprocess_text_async(parsed_doc['full_text'])
            
            # Step 3-4: Run classification and entity extraction in parallel
            classification_task = self._classify_document_async(preprocessed['cleaned_text'])
            entities_task = self._extract_entities_async(preprocessed['cleaned_text'])
            
            classification, entities = await asyncio.gather(
                classification_task,
                entities_task
            )
            
            # Step 5: Extract clauses
            clauses = await self._extract_clauses_async(preprocessed['cleaned_text'])
            
            # Step 6: Simplify clauses if requested
            simplified_clauses = []
            if include_simplification and clauses:
                simplified_clauses = await self._simplify_clauses_async(clauses)
            
            # Step 7: Generate characteristics
            characteristics = self._get_document_characteristics(
                preprocessed['cleaned_text'], 
                classification['predicted_type']
            )
            
            # Compile results
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
            
            logger.info("Minimal document analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in minimal document analysis: {str(e)}")
            raise
    
    async def _parse_document_async(self, file_path: str) -> Dict[str, Any]:
        """Parse document asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._parse_document, file_path)
    
    def _parse_document(self, file_path: str) -> Dict[str, Any]:
        """Parse document (currently supports text files only)."""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                return {
                    'file_type': 'txt',
                    'full_text': content,
                    'metadata': {
                        'file_name': os.path.basename(file_path),
                        'file_size': len(content)
                    }
                }
            else:
                raise ValueError(f"Unsupported file format: {file_extension}. Only .txt files supported in minimal mode.")
                
        except Exception as e:
            logger.error(f"Error parsing document {file_path}: {str(e)}")
            raise
    
    async def _preprocess_text_async(self, text: str) -> Dict[str, Any]:
        """Preprocess text asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._preprocess_text, text)
    
    def _preprocess_text(self, text: str) -> Dict[str, Any]:
        """Preprocess text."""
        # Clean text
        cleaned_text = re.sub(r'\s+', ' ', text)
        cleaned_text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\"\'\/\$\%]', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        # Calculate statistics
        words = cleaned_text.split()
        sentences = re.split(r'[.!?]+', cleaned_text)
        
        statistics = {
            'word_count': len(words),
            'character_count': len(cleaned_text),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'average_sentence_length': len(words) / len(sentences) if sentences else 0
        }
        
        return {
            'cleaned_text': cleaned_text,
            'statistics': statistics
        }
    
    async def _classify_document_async(self, text: str) -> Dict[str, Any]:
        """Classify document asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._classify_document, text)
    
    def _classify_document(self, text: str) -> Dict[str, Any]:
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
        
        # Calculate confidence
        confidence = min(max_score / (len(text.split()) / 100), 1.0)
        
        return {
            'predicted_type': predicted_type,
            'confidence': confidence,
            'is_confident': confidence > 0.3,
            'scores': scores
        }
    
    async def _extract_entities_async(self, text: str) -> Dict[str, Any]:
        """Extract entities asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._extract_entities, text)
    
    def _extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities using regex patterns."""
        entities = {}
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities[entity_type] = [
                {'text': match, 'type': entity_type, 'confidence': 0.8}
                for match in set(matches)
            ]
        
        # Extract key parties (simple heuristic)
        key_parties = []
        party_patterns = [
            r'\b([A-Z][a-z]+ (?:Inc|LLC|Corp|Corporation|Company|Ltd)\.?)\b',
            r'\b([A-Z][a-z]+ [A-Z][a-z]+)\b'  # Person names
        ]
        
        for pattern in party_patterns:
            matches = re.findall(pattern, text)
            for match in matches[:5]:  # Limit to 5 parties
                key_parties.append({'name': match, 'type': 'organization' if any(x in match for x in ['Inc', 'LLC', 'Corp']) else 'person'})
        
        # Extract obligations
        obligations = []
        obligation_patterns = [
            r'[^.]*(?:shall|must|will|required to|obligated to)[^.]*\.',
            r'[^.]*(?:agrees to|undertakes to)[^.]*\.'
        ]
        
        for pattern in obligation_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches[:5]:
                obligations.append({'text': match.strip(), 'type': 'obligation'})
        
        # Extract dates and deadlines
        dates_and_deadlines = []
        for date_match in entities.get('dates', []):
            dates_and_deadlines.append({
                'text': date_match['text'],
                'type': 'date',
                'confidence': 0.8
            })
        
        return {
            'entities': entities,
            'key_parties': key_parties,
            'obligations': obligations,
            'dates_and_deadlines': dates_and_deadlines
        }
    
    async def _extract_clauses_async(self, text: str) -> List[str]:
        """Extract clauses asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._extract_clauses, text)
    
    def _extract_clauses(self, text: str) -> List[str]:
        """Extract clauses using simple heuristics."""
        clauses = []
        
        # Pattern for numbered sections
        numbered_sections = re.split(r'\n\s*\d+\.\s*', text)
        if len(numbered_sections) > 1:
            clauses.extend([clause.strip() for clause in numbered_sections[1:] if clause.strip()])
        
        # Pattern for lettered sections
        lettered_sections = re.split(r'\n\s*[a-z]\)\s*', text)
        if len(lettered_sections) > 1:
            clauses.extend([clause.strip() for clause in lettered_sections[1:] if clause.strip()])
        
        # If no structured sections, split by paragraphs
        if not clauses:
            paragraphs = text.split('\n\n')
            clauses = [p.strip() for p in paragraphs if len(p.strip()) > 50]
        
        return clauses[:10]  # Limit to first 10 clauses
    
    async def _simplify_clauses_async(self, clauses: List[str]) -> List[Dict[str, Any]]:
        """Simplify clauses asynchronously."""
        simplified_clauses = []
        
        for clause in clauses[:5]:  # Limit to 5 clauses
            simplified = await self._simplify_single_clause_async(clause)
            simplified_clauses.append(simplified)
        
        return simplified_clauses
    
    async def _simplify_single_clause_async(self, clause: str) -> Dict[str, Any]:
        """Simplify a single clause asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self._simplify_clause, clause)
    
    def _simplify_clause(self, clause: str) -> Dict[str, Any]:
        """Simplify a clause using rule-based approach."""
        original_clause = clause.strip()
        simplified_clause = original_clause
        
        # Apply simplification rules
        for pattern, replacement in self.simplification_rules.items():
            simplified_clause = re.sub(pattern, replacement, simplified_clause, flags=re.IGNORECASE)
        
        # Generate plain English summary
        plain_english = self._generate_plain_english_summary(simplified_clause)
        
        # Extract key points
        key_points = self._extract_key_points(simplified_clause)
        
        # Calculate simplification score
        word_reduction = (len(original_clause.split()) - len(simplified_clause.split())) / len(original_clause.split()) if original_clause.split() else 0
        simplification_score = max(0.1, word_reduction)
        
        return {
            'original_clause': original_clause,
            'simplified_clause': simplified_clause,
            'plain_english_summary': plain_english,
            'key_points': key_points,
            'simplification_score': simplification_score
        }
    
    def _generate_plain_english_summary(self, clause: str) -> str:
        """Generate plain English summary."""
        clause_lower = clause.lower()
        
        if 'payment' in clause_lower or '$' in clause:
            return "This clause deals with payment terms and amounts."
        elif 'termination' in clause_lower:
            return "This clause explains how the agreement can be ended."
        elif 'confidential' in clause_lower:
            return "This clause requires keeping information secret."
        elif 'liability' in clause_lower:
            return "This clause defines who is responsible for what."
        else:
            return "This clause contains important legal terms and conditions."
    
    def _extract_key_points(self, clause: str) -> List[str]:
        """Extract key points from clause."""
        key_points = []
        
        # Look for monetary amounts
        money_matches = re.findall(r'\$[\d,]+(?:\.\d{2})?', clause)
        if money_matches:
            key_points.append(f"Involves money: {', '.join(money_matches)}")
        
        # Look for time periods
        time_matches = re.findall(r'\b\d+\s+(?:days?|weeks?|months?|years?)\b', clause, re.IGNORECASE)
        if time_matches:
            key_points.append(f"Time periods: {', '.join(time_matches)}")
        
        return key_points[:3]
    
    def _get_document_characteristics(self, text: str, doc_type: str) -> Dict[str, Any]:
        """Get document characteristics."""
        return {
            'document_type': doc_type,
            'complexity': self._assess_complexity({'word_count': len(text.split())}),
            'key_sections': self._identify_key_sections(text)
        }
    
    def _identify_key_sections(self, text: str) -> List[str]:
        """Identify key sections in the document."""
        sections = []
        
        # Look for common legal sections
        section_patterns = [
            r'(?i)\b(?:whereas|recitals?)\b',
            r'(?i)\b(?:definitions?|terms?)\b',
            r'(?i)\b(?:obligations?|duties)\b',
            r'(?i)\b(?:payment|compensation)\b',
            r'(?i)\b(?:termination|expiration)\b',
            r'(?i)\b(?:confidentiality|non-disclosure)\b',
            r'(?i)\b(?:liability|indemnification)\b',
            r'(?i)\b(?:dispute|arbitration)\b'
        ]
        
        for pattern in section_patterns:
            if re.search(pattern, text):
                section_name = pattern.replace('(?i)\\b(?:', '').replace(')\\b', '').split('|')[0]
                sections.append(section_name.title())
        
        return sections
    
    def _generate_document_summary(self, classification: Dict, entities: Dict, 
                                 characteristics: Dict, statistics: Dict) -> Dict[str, Any]:
        """Generate document summary."""
        summary = {
            'document_type': classification['predicted_type'],
            'confidence': classification['confidence'],
            'key_findings': [],
            'important_entities': {},
            'document_complexity': self._assess_complexity(statistics)
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
        
        # Generate key findings
        if classification['is_confident']:
            summary['key_findings'].append(f"Document identified as {classification['predicted_type'].replace('_', ' ').title()}")
        
        if entities.get('key_parties'):
            summary['key_findings'].append(f"Found {len(entities['key_parties'])} key parties involved")
        
        return summary
    
    def _generate_recommendations(self, classification: Dict, entities: Dict) -> List[str]:
        """Generate recommendations."""
        recommendations = []
        doc_type = classification['predicted_type']
        
        if doc_type == 'nda':
            recommendations.extend([
                "Review confidentiality scope and duration",
                "Ensure mutual obligations are clearly defined"
            ])
        elif doc_type == 'employment_contract':
            recommendations.extend([
                "Review compensation and benefits details",
                "Check termination and notice period clauses"
            ])
        elif doc_type == 'service_agreement':
            recommendations.extend([
                "Clarify scope of work and deliverables",
                "Review payment terms and schedule"
            ])
        
        return recommendations[:5]
    
    def _assess_complexity(self, statistics: Dict) -> str:
        """Assess document complexity."""
        word_count = statistics.get('word_count', 0)
        
        if word_count < 500:
            return 'Low'
        elif word_count < 2000:
            return 'Medium'
        else:
            return 'High'
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        return datetime.now().isoformat()
    
    def quick_analyze(self, text: str) -> Dict[str, Any]:
        """Quick analysis for text snippets."""
        try:
            classification = self._classify_document(text)
            entities = self._extract_entities(text)
            
            return {
                'classification': classification,
                'entities': entities,
                'word_count': len(text.split()),
                'character_count': len(text)
            }
            
        except Exception as e:
            logger.error(f"Error in quick analysis: {str(e)}")
            raise
