"""Named Entity Recognition module for legal documents."""

import re
from typing import List, Dict, Any, Tuple
from datetime import datetime
from ..utils import get_logger

logger = get_logger(__name__)

class LegalNER:
    """Named Entity Recognition for legal documents."""
    
    def __init__(self):
        # Legal entity patterns
        self.patterns = {
            'dates': [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
                r'\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{2,4}\b',
                r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{2,4}\b',
            ],
            'monetary_values': [
                r'\$[\d,]+\.?\d*',  # $1,000.00
                r'\b\d+\s*dollars?\b',  # 1000 dollars
                r'\b\d+\s*USD\b',  # 1000 USD
            ],
            'parties': [
                r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\s*(?:Inc\.?|LLC|Corp\.?|Corporation|Company|Ltd\.?|Limited)?\b',
                r'\b(?:The\s+)?[A-Z][A-Za-z\s&]+(?:Inc\.?|LLC|Corp\.?|Corporation|Company|Ltd\.?|Limited)\b',
            ],
            'addresses': [
                r'\b\d+\s+[A-Za-z\s]+(?:Street|St\.?|Avenue|Ave\.?|Road|Rd\.?|Boulevard|Blvd\.?|Drive|Dr\.?|Lane|Ln\.?|Way|Court|Ct\.?)\b',
            ],
            'phone_numbers': [
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890
                r'\(\d{3}\)\s*\d{3}[-.]?\d{4}\b',  # (123) 456-7890
            ],
            'email_addresses': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            ],
            'legal_terms': [
                r'\b(?:whereas|therefore|hereby|herein|hereof|hereunder|notwithstanding|pursuant|covenant|indemnify|liability|breach|termination|confidential|proprietary)\b',
            ],
            'obligations': [
                r'\b(?:shall|must|will|agree to|required to|obligated to|responsible for)\b[^.]*',
            ],
            'durations': [
                r'\b\d+\s*(?:days?|weeks?|months?|years?)\b',
                r'\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:days?|weeks?|months?|years?)\b',
            ]
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        """Extract named entities from text."""
        try:
            entities = {}
            
            for entity_type, patterns in self.patterns.items():
                entities[entity_type] = []
                
                for pattern in patterns:
                    matches = re.finditer(pattern, text, re.IGNORECASE)
                    
                    for match in matches:
                        entity = {
                            'text': match.group(),
                            'start': match.start(),
                            'end': match.end(),
                            'confidence': 0.8,  # Simple confidence score
                            'context': self._get_context(text, match.start(), match.end())
                        }
                        
                        # Avoid duplicates
                        if not any(e['text'].lower() == entity['text'].lower() for e in entities[entity_type]):
                            entities[entity_type].append(entity)
            
            return entities
            
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return {}
    
    def _get_context(self, text: str, start: int, end: int, context_size: int = 50) -> str:
        """Get context around an entity."""
        try:
            context_start = max(0, start - context_size)
            context_end = min(len(text), end + context_size)
            return text[context_start:context_end].strip()
        except:
            return ""
    
    def extract_key_parties(self, text: str) -> List[Dict[str, Any]]:
        """Extract key parties from legal document."""
        try:
            parties = []
            
            # Look for common party indicators
            party_indicators = [
                r'(?:between|by and between)\s+([^,]+),?\s+(?:and|&)\s+([^,\n]+)',
                r'(?:party of the first part|first party)[:\s]+([^,\n]+)',
                r'(?:party of the second part|second party)[:\s]+([^,\n]+)',
                r'(?:client|customer|buyer|seller|lessor|lessee|employer|employee)[:\s]+([^,\n]+)',
            ]
            
            for pattern in party_indicators:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    for group in match.groups():
                        if group and len(group.strip()) > 2:
                            party = {
                                'name': group.strip(),
                                'type': 'party',
                                'context': self._get_context(text, match.start(), match.end())
                            }
                            parties.append(party)
            
            return parties
            
        except Exception as e:
            logger.error(f"Error extracting key parties: {str(e)}")
            return []
    
    def extract_obligations(self, text: str) -> List[Dict[str, Any]]:
        """Extract obligations and responsibilities."""
        try:
            obligations = []
            
            # Patterns for obligations
            obligation_patterns = [
                r'(?:shall|must|will|agree to|required to|obligated to|responsible for)\s+([^.]+)',
                r'(?:party|parties)\s+(?:shall|must|will|agree to)\s+([^.]+)',
                r'(?:obligations?|duties|responsibilities)\s*:?\s*([^.]+)',
            ]
            
            for pattern in obligation_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    obligation_text = match.group(1) if len(match.groups()) > 0 else match.group()
                    
                    obligation = {
                        'text': obligation_text.strip(),
                        'full_clause': match.group().strip(),
                        'start': match.start(),
                        'end': match.end(),
                        'context': self._get_context(text, match.start(), match.end())
                    }
                    obligations.append(obligation)
            
            return obligations
            
        except Exception as e:
            logger.error(f"Error extracting obligations: {str(e)}")
            return []
    
    def extract_dates_and_deadlines(self, text: str) -> List[Dict[str, Any]]:
        """Extract important dates and deadlines."""
        try:
            dates = []
            
            # Enhanced date patterns with context
            date_context_patterns = [
                r'(?:effective|start|begin|commence|end|expire|terminate|due|deadline|by)\s+(?:date|on)?\s*:?\s*([^,\n]+)',
                r'(?:within|after|before)\s+(\d+\s*(?:days?|weeks?|months?|years?))',
                r'(?:no later than|not later than|by)\s+([^,\n]+)',
            ]
            
            for pattern in date_context_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    date_info = {
                        'text': match.group(1).strip() if len(match.groups()) > 0 else match.group().strip(),
                        'full_clause': match.group().strip(),
                        'type': 'deadline',
                        'context': self._get_context(text, match.start(), match.end())
                    }
                    dates.append(date_info)
            
            return dates
            
        except Exception as e:
            logger.error(f"Error extracting dates and deadlines: {str(e)}")
            return []
    
    def analyze_document_entities(self, text: str) -> Dict[str, Any]:
        """Comprehensive entity analysis of the document."""
        try:
            # Extract all entity types
            entities = self.extract_entities(text)
            
            # Extract specialized entities
            key_parties = self.extract_key_parties(text)
            obligations = self.extract_obligations(text)
            dates_deadlines = self.extract_dates_and_deadlines(text)
            
            # Compile summary
            summary = {
                'total_entities': sum(len(entity_list) for entity_list in entities.values()),
                'entity_types': list(entities.keys()),
                'key_parties_count': len(key_parties),
                'obligations_count': len(obligations),
                'dates_deadlines_count': len(dates_deadlines)
            }
            
            return {
                'entities': entities,
                'key_parties': key_parties,
                'obligations': obligations,
                'dates_and_deadlines': dates_deadlines,
                'summary': summary
            }
            
        except Exception as e:
            logger.error(f"Error in comprehensive entity analysis: {str(e)}")
            raise