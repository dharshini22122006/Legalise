"""Optimized analyzer orchestrator for legal document analysis."""

import asyncio
import concurrent.futures
from typing import Dict, Any, List, Optional
from functools import lru_cache
import threading
from .parser import DocumentParser
from .preprocessor import TextPreprocessor
from .ner import LegalNER
from .classifier import DocumentClassifier
from .simplifier import GraniteSimplifier
from ..utils import get_logger, cached

logger = get_logger(__name__)

class OptimizedLegalDocumentAnalyzer:
    """Optimized orchestrator for legal document analysis with performance improvements."""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Singleton pattern to avoid multiple model loadings."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self.parser = DocumentParser()
        self.preprocessor = TextPreprocessor()
        self.ner = LegalNER()
        self.classifier = DocumentClassifier()
        self.simplifier = GraniteSimplifier()
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self._initialized = True
    
    async def analyze_document(self, file_path: str, include_simplification: bool = True) -> Dict[str, Any]:
        """Complete document analysis pipeline with optimizations."""
        try:
            logger.info(f"Starting optimized analysis of document: {file_path}")
            
            # Step 1: Parse document (async)
            logger.info("Step 1: Parsing document...")
            parsed_doc = await self._parse_document_async(file_path)
            
            # Step 2: Preprocess text (async)
            logger.info("Step 2: Preprocessing text...")
            preprocessed = await self._preprocess_text_async(parsed_doc['full_text'])
            
            # Step 3-4: Run classification and entity extraction in parallel
            logger.info("Steps 3-4: Running classification and entity extraction in parallel...")
            classification_task = self._classify_document_async(preprocessed['cleaned_text'])
            entities_task = self._extract_entities_async(preprocessed['cleaned_text'])
            
            classification, entities = await asyncio.gather(
                classification_task,
                entities_task
            )
            
            # Step 5: Extract clauses (optimized chunking)
            logger.info("Step 5: Extracting clauses with chunking...")
            clauses = await self._extract_clauses_async(preprocessed['cleaned_text'])
            
            # Step 6: Simplify clauses (truly async with batching)
            simplified_clauses = []
            if include_simplification and clauses:
                logger.info("Step 6: Simplifying clauses in batches...")
                simplified_clauses = await self._simplify_clauses_batch_async(clauses)
            
            # Step 7: Generate document characteristics (async)
            logger.info("Step 7: Analyzing document characteristics...")
            characteristics = await self._get_characteristics_async(
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
            
            logger.info("Optimized document analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in optimized document analysis: {str(e)}")
            raise
    
    async def _parse_document_async(self, file_path: str) -> Dict[str, Any]:
        """Parse document asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.parser.parse_document, file_path)
    
    async def _preprocess_text_async(self, text: str) -> Dict[str, Any]:
        """Preprocess text asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.preprocessor.preprocess_document, text)
    
    async def _classify_document_async(self, text: str) -> Dict[str, Any]:
        """Classify document asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.classifier.classify_document, text)
    
    async def _extract_entities_async(self, text: str) -> Dict[str, Any]:
        """Extract entities asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.ner.analyze_document_entities, text)
    
    async def _extract_clauses_async(self, text: str) -> List[str]:
        """Extract clauses asynchronously with chunking for large documents."""
        loop = asyncio.get_event_loop()
        
        # For large documents, process in chunks
        if len(text) > 10000:  # 10k characters threshold
            chunks = self._chunk_text(text, chunk_size=5000, overlap=500)
            clause_tasks = [
                loop.run_in_executor(self.executor, self.parser.extract_clauses, chunk)
                for chunk in chunks
            ]
            chunk_clauses = await asyncio.gather(*clause_tasks)
            
            # Flatten and deduplicate clauses
            all_clauses = []
            for clauses in chunk_clauses:
                all_clauses.extend(clauses)
            
            return self._deduplicate_clauses(all_clauses)
        else:
            return await loop.run_in_executor(self.executor, self.parser.extract_clauses, text)
    
    async def _get_characteristics_async(self, text: str, doc_type: str) -> Dict[str, Any]:
        """Get document characteristics asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            self.classifier.get_document_characteristics, 
            text, 
            doc_type
        )
    
    async def _simplify_clauses_batch_async(self, clauses: List[str], batch_size: int = 3) -> List[Dict[str, Any]]:
        """Simplify clauses in batches asynchronously."""
        try:
            simplified_clauses = []
            
            # Process clauses in batches to avoid overwhelming the model
            for i in range(0, min(len(clauses), 10), batch_size):  # Limit to first 10 clauses
                batch = clauses[i:i + batch_size]
                logger.info(f"Simplifying batch {i//batch_size + 1} ({len(batch)} clauses)")
                
                # Process batch in parallel
                batch_tasks = [
                    self._simplify_single_clause_async(clause)
                    for clause in batch
                ]
                
                batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
                
                # Filter out exceptions and add successful results
                for result in batch_results:
                    if not isinstance(result, Exception):
                        simplified_clauses.append(result)
                
                # Small delay between batches to prevent overwhelming the model
                await asyncio.sleep(0.1)
            
            return simplified_clauses
            
        except Exception as e:
            logger.error(f"Error in batch clause simplification: {str(e)}")
            return []
    
    async def _simplify_single_clause_async(self, clause: str) -> Dict[str, Any]:
        """Simplify a single clause asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, self.simplifier.simplify_clause, clause)
    
    def _chunk_text(self, text: str, chunk_size: int = 5000, overlap: int = 500) -> List[str]:
        """Split text into overlapping chunks for processing."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence ending within the last 200 characters
                sentence_end = text.rfind('.', end - 200, end)
                if sentence_end != -1:
                    end = sentence_end + 1
            
            chunks.append(text[start:end])
            start = end - overlap if end < len(text) else end
        
        return chunks
    
    def _deduplicate_clauses(self, clauses: List[str]) -> List[str]:
        """Remove duplicate clauses based on similarity."""
        unique_clauses = []
        
        for clause in clauses:
            # Simple deduplication based on first 100 characters
            clause_start = clause[:100].strip()
            
            is_duplicate = False
            for existing in unique_clauses:
                if existing[:100].strip() == clause_start:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_clauses.append(clause)
        
        return unique_clauses
    
    @lru_cache(maxsize=128)
    def _generate_document_summary(self, classification: Dict, entities: Dict, 
                                 characteristics: Dict, statistics: Dict) -> Dict[str, Any]:
        """Generate a comprehensive document summary with caching."""
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
        """Quick analysis for text snippets with caching."""
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
    
    def __del__(self):
        """Cleanup resources."""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=True)