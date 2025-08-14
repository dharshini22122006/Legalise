"""Document type classification module."""

import re
from typing import Dict, List, Tuple, Any
from ..utils import get_logger

logger = get_logger(__name__)

class DocumentClassifier:
    """Legal document type classifier."""
    
    def __init__(self):
        # Document type keywords and patterns
        self.document_patterns = {
            'nda': {
                'keywords': [
                    'non-disclosure', 'confidentiality', 'confidential information',
                    'proprietary information', 'trade secrets', 'non-disclosure agreement',
                    'confidentiality agreement', 'secrecy agreement'
                ],
                'patterns': [
                    r'non[- ]disclosure',
                    r'confidential(?:ity)?',
                    r'proprietary\s+information',
                    r'trade\s+secrets?'
                ],
                'weight': 1.0
            },
            'employment_contract': {
                'keywords': [
                    'employment', 'employee', 'employer', 'job', 'position',
                    'salary', 'wages', 'benefits', 'termination', 'resignation',
                    'work schedule', 'duties', 'responsibilities'
                ],
                'patterns': [
                    r'employment\s+(?:agreement|contract)',
                    r'employee\s+handbook',
                    r'job\s+description',
                    r'salary\s+and\s+benefits'
                ],
                'weight': 1.0
            },
            'service_agreement': {
                'keywords': [
                    'service', 'services', 'provider', 'client', 'customer',
                    'deliverables', 'scope of work', 'statement of work',
                    'professional services', 'consulting'
                ],
                'patterns': [
                    r'service\s+agreement',
                    r'professional\s+services',
                    r'scope\s+of\s+work',
                    r'statement\s+of\s+work'
                ],
                'weight': 1.0
            },
            'lease_agreement': {
                'keywords': [
                    'lease', 'rent', 'tenant', 'landlord', 'property',
                    'premises', 'rental', 'lease term', 'security deposit',
                    'monthly rent'
                ],
                'patterns': [
                    r'lease\s+agreement',
                    r'rental\s+agreement',
                    r'landlord\s+and\s+tenant',
                    r'monthly\s+rent'
                ],
                'weight': 1.0
            },
            'purchase_agreement': {
                'keywords': [
                    'purchase', 'sale', 'buyer', 'seller', 'goods',
                    'merchandise', 'purchase price', 'delivery',
                    'payment terms', 'invoice'
                ],
                'patterns': [
                    r'purchase\s+agreement',
                    r'sale\s+agreement',
                    r'buyer\s+and\s+seller',
                    r'purchase\s+price'
                ],
                'weight': 1.0
            },
            'partnership_agreement': {
                'keywords': [
                    'partnership', 'partners', 'joint venture', 'collaboration',
                    'profit sharing', 'equity', 'capital contribution',
                    'management', 'dissolution'
                ],
                'patterns': [
                    r'partnership\s+agreement',
                    r'joint\s+venture',
                    r'profit\s+sharing',
                    r'capital\s+contribution'
                ],
                'weight': 1.0
            },
            'license_agreement': {
                'keywords': [
                    'license', 'licensing', 'licensor', 'licensee',
                    'intellectual property', 'copyright', 'trademark',
                    'patent', 'royalty', 'usage rights'
                ],
                'patterns': [
                    r'license\s+agreement',
                    r'licensing\s+agreement',
                    r'intellectual\s+property',
                    r'usage\s+rights'
                ],
                'weight': 1.0
            },
            'loan_agreement': {
                'keywords': [
                    'loan', 'lender', 'borrower', 'principal', 'interest',
                    'repayment', 'default', 'collateral', 'credit',
                    'promissory note'
                ],
                'patterns': [
                    r'loan\s+agreement',
                    r'promissory\s+note',
                    r'lender\s+and\s+borrower',
                    r'interest\s+rate'
                ],
                'weight': 1.0
            }
        }
    
    def classify_document(self, text: str) -> Dict[str, Any]:
        """Classify document type based on content."""
        try:
            text_lower = text.lower()
            scores = {}
            
            # Calculate scores for each document type
            for doc_type, config in self.document_patterns.items():
                score = 0.0
                matched_keywords = []
                matched_patterns = []
                
                # Check keywords
                for keyword in config['keywords']:
                    if keyword.lower() in text_lower:
                        score += 1.0
                        matched_keywords.append(keyword)
                
                # Check patterns
                for pattern in config['patterns']:
                    matches = re.findall(pattern, text_lower)
                    if matches:
                        score += 2.0  # Patterns have higher weight
                        matched_patterns.extend(matches)
                
                # Apply document type weight
                score *= config['weight']
                
                scores[doc_type] = {
                    'score': score,
                    'matched_keywords': matched_keywords,
                    'matched_patterns': matched_patterns,
                    'confidence': min(score / 10.0, 1.0)  # Normalize to 0-1
                }
            
            # Find the best match
            best_match = max(scores.items(), key=lambda x: x[1]['score'])
            
            # Determine if classification is confident enough
            threshold = 2.0
            is_confident = best_match[1]['score'] >= threshold
            
            return {
                'predicted_type': best_match[0] if is_confident else 'unknown',
                'confidence': best_match[1]['confidence'],
                'is_confident': is_confident,
                'all_scores': scores,
                'matched_indicators': {
                    'keywords': best_match[1]['matched_keywords'],
                    'patterns': best_match[1]['matched_patterns']
                }
            }
            
        except Exception as e:
            logger.error(f"Error classifying document: {str(e)}")
            return {
                'predicted_type': 'unknown',
                'confidence': 0.0,
                'is_confident': False,
                'all_scores': {},
                'matched_indicators': {'keywords': [], 'patterns': []}
            }
    
    def get_document_characteristics(self, text: str, doc_type: str) -> Dict[str, Any]:
        """Get specific characteristics based on document type."""
        try:
            characteristics = {}
            
            if doc_type == 'nda':
                characteristics = self._analyze_nda(text)
            elif doc_type == 'employment_contract':
                characteristics = self._analyze_employment_contract(text)
            elif doc_type == 'service_agreement':
                characteristics = self._analyze_service_agreement(text)
            elif doc_type == 'lease_agreement':
                characteristics = self._analyze_lease_agreement(text)
            else:
                characteristics = self._analyze_general_contract(text)
            
            return characteristics
            
        except Exception as e:
            logger.error(f"Error analyzing document characteristics: {str(e)}")
            return {}
    
    def _analyze_nda(self, text: str) -> Dict[str, Any]:
        """Analyze NDA-specific characteristics."""
        characteristics = {
            'type': 'Non-Disclosure Agreement',
            'key_elements': []
        }
        
        # Check for mutual vs unilateral
        if re.search(r'mutual(?:ly)?', text, re.IGNORECASE):
            characteristics['nda_type'] = 'Mutual NDA'
        else:
            characteristics['nda_type'] = 'Unilateral NDA'
        
        # Look for duration
        duration_match = re.search(r'(?:for a period of|duration of|term of)\s+([^,\n]+)', text, re.IGNORECASE)
        if duration_match:
            characteristics['duration'] = duration_match.group(1).strip()
        
        return characteristics
    
    def _analyze_employment_contract(self, text: str) -> Dict[str, Any]:
        """Analyze employment contract characteristics."""
        characteristics = {
            'type': 'Employment Contract',
            'key_elements': []
        }
        
        # Look for employment type
        if re.search(r'full[- ]time', text, re.IGNORECASE):
            characteristics['employment_type'] = 'Full-time'
        elif re.search(r'part[- ]time', text, re.IGNORECASE):
            characteristics['employment_type'] = 'Part-time'
        elif re.search(r'contract(?:or|ual)?', text, re.IGNORECASE):
            characteristics['employment_type'] = 'Contract'
        
        return characteristics
    
    def _analyze_service_agreement(self, text: str) -> Dict[str, Any]:
        """Analyze service agreement characteristics."""
        characteristics = {
            'type': 'Service Agreement',
            'key_elements': []
        }
        
        # Look for service type
        if re.search(r'consulting', text, re.IGNORECASE):
            characteristics['service_type'] = 'Consulting'
        elif re.search(r'professional\s+services', text, re.IGNORECASE):
            characteristics['service_type'] = 'Professional Services'
        
        return characteristics
    
    def _analyze_lease_agreement(self, text: str) -> Dict[str, Any]:
        """Analyze lease agreement characteristics."""
        characteristics = {
            'type': 'Lease Agreement',
            'key_elements': []
        }
        
        # Look for property type
        if re.search(r'residential', text, re.IGNORECASE):
            characteristics['property_type'] = 'Residential'
        elif re.search(r'commercial', text, re.IGNORECASE):
            characteristics['property_type'] = 'Commercial'
        
        return characteristics
    
    def _analyze_general_contract(self, text: str) -> Dict[str, Any]:
        """Analyze general contract characteristics."""
        return {
            'type': 'General Contract',
            'key_elements': []
        }