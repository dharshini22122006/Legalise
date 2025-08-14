"""Fallback clause simplifier without heavy ML dependencies."""

import re
from typing import List, Dict, Any
from ..utils import get_logger

logger = get_logger(__name__)

class FallbackSimplifier:
    """Fallback legal clause simplifier using rule-based approaches."""
    
    def __init__(self):
        # Legal jargon to plain English mappings
        self.simplification_rules = {
            # Common legal terms
            r'\bheretofore\b': 'before this',
            r'\bhereinafter\b': 'from now on',
            r'\bwhereas\b': 'since',
            r'\btherefore\b': 'so',
            r'\bnotwithstanding\b': 'despite',
            r'\bpursuant to\b': 'according to',
            r'\bin consideration of\b': 'in exchange for',
            r'\bshall\b': 'will',
            r'\bmay not\b': 'cannot',
            r'\bprovided that\b': 'if',
            r'\bsubject to\b': 'depending on',
            
            # Complex phrases
            r'\bin the event that\b': 'if',
            r'\bfor the purpose of\b': 'to',
            r'\bwith respect to\b': 'about',
            r'\bin accordance with\b': 'following',
            r'\bprior to\b': 'before',
            r'\bsubsequent to\b': 'after',
            r'\bin lieu of\b': 'instead of',
            r'\bby virtue of\b': 'because of',
            
            # Redundant phrases
            r'\bnull and void\b': 'invalid',
            r'\beach and every\b': 'all',
            r'\bfull and complete\b': 'complete',
            r'\bfinal and binding\b': 'final',
            r'\bterms and conditions\b': 'terms',
            
            # Time references
            r'\bforthwith\b': 'immediately',
            r'\bhenceforth\b': 'from now on',
            r'\bheretofore\b': 'until now',
        }
        
        # Sentence structure improvements
        self.structure_rules = [
            # Remove excessive "the said", "such", etc.
            (r'\bthe said\b', 'the'),
            (r'\bsuch\s+(\w+)\s+as\s+aforesaid\b', r'the \1'),
            (r'\baforesaid\b', 'mentioned'),
            
            # Simplify passive voice where possible
            (r'\bis hereby\s+(\w+ed)\b', r'is \1'),
            (r'\bshall be deemed to be\b', 'is considered'),
            (r'\bshall be construed as\b', 'means'),
        ]
    
    def simplify_clause(self, clause: str) -> Dict[str, Any]:
        """Simplify a legal clause using rule-based approach."""
        try:
            original_clause = clause.strip()
            simplified_clause = self._apply_simplification_rules(original_clause)
            
            # Generate plain English summary
            plain_english = self._generate_plain_english_summary(simplified_clause)
            
            # Extract key points
            key_points = self._extract_key_points(simplified_clause)
            
            # Calculate simplification score
            simplification_score = self._calculate_simplification_score(
                original_clause, simplified_clause
            )
            
            return {
                'original_clause': original_clause,
                'simplified_clause': simplified_clause,
                'plain_english_summary': plain_english,
                'key_points': key_points,
                'simplification_score': simplification_score,
                'method': 'rule_based'
            }
            
        except Exception as e:
            logger.error(f"Error simplifying clause: {str(e)}")
            return {
                'original_clause': clause,
                'simplified_clause': clause,
                'plain_english_summary': 'Unable to simplify this clause.',
                'key_points': [],
                'simplification_score': 0.0,
                'method': 'fallback'
            }
    
    def _apply_simplification_rules(self, text: str) -> str:
        """Apply simplification rules to text."""
        simplified = text
        
        # Apply word/phrase replacements
        for pattern, replacement in self.simplification_rules.items():
            simplified = re.sub(pattern, replacement, simplified, flags=re.IGNORECASE)
        
        # Apply structure improvements
        for pattern, replacement in self.structure_rules:
            simplified = re.sub(pattern, replacement, simplified, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        simplified = re.sub(r'\s+', ' ', simplified).strip()
        
        return simplified
    
    def _generate_plain_english_summary(self, clause: str) -> str:
        """Generate a plain English summary of the clause."""
        # Simple heuristics for common clause types
        clause_lower = clause.lower()
        
        if 'payment' in clause_lower or 'pay' in clause_lower or '$' in clause:
            return "This clause deals with payment terms and amounts."
        elif 'termination' in clause_lower or 'terminate' in clause_lower:
            return "This clause explains how the agreement can be ended."
        elif 'confidential' in clause_lower or 'non-disclosure' in clause_lower:
            return "This clause requires keeping information secret."
        elif 'liability' in clause_lower or 'responsible' in clause_lower:
            return "This clause defines who is responsible for what."
        elif 'intellectual property' in clause_lower or 'copyright' in clause_lower:
            return "This clause deals with ownership of ideas and creations."
        elif 'dispute' in clause_lower or 'arbitration' in clause_lower:
            return "This clause explains how disagreements will be resolved."
        elif 'force majeure' in clause_lower or 'act of god' in clause_lower:
            return "This clause covers situations beyond anyone's control."
        else:
            # Extract first sentence as summary
            sentences = re.split(r'[.!?]+', clause)
            if sentences:
                first_sentence = sentences[0].strip()
                if len(first_sentence) > 20:
                    return f"In simple terms: {first_sentence.lower()}."
        
        return "This clause contains important legal terms and conditions."
    
    def _extract_key_points(self, clause: str) -> List[str]:
        """Extract key points from the clause."""
        key_points = []
        
        # Look for monetary amounts
        money_matches = re.findall(r'\$[\d,]+(?:\.\d{2})?', clause)
        if money_matches:
            key_points.append(f"Involves money: {', '.join(money_matches)}")
        
        # Look for time periods
        time_matches = re.findall(r'\b\d+\s+(?:days?|weeks?|months?|years?)\b', clause, re.IGNORECASE)
        if time_matches:
            key_points.append(f"Time periods: {', '.join(time_matches)}")
        
        # Look for percentages
        percent_matches = re.findall(r'\d+(?:\.\d+)?%', clause)
        if percent_matches:
            key_points.append(f"Percentages: {', '.join(percent_matches)}")
        
        # Look for obligations (must, shall, will)
        obligation_words = ['must', 'shall', 'will', 'required', 'obligated']
        obligations = []
        for word in obligation_words:
            if word in clause.lower():
                obligations.append(word)
        if obligations:
            key_points.append(f"Creates obligations: {', '.join(set(obligations))}")
        
        # Look for conditions (if, unless, provided)
        condition_words = ['if', 'unless', 'provided', 'subject to', 'in case']
        conditions = []
        for word in condition_words:
            if word in clause.lower():
                conditions.append(word)
        if conditions:
            key_points.append(f"Has conditions: {', '.join(set(conditions))}")
        
        return key_points[:5]  # Limit to 5 key points
    
    def _calculate_simplification_score(self, original: str, simplified: str) -> float:
        """Calculate how much the text was simplified."""
        try:
            # Compare word counts
            original_words = len(original.split())
            simplified_words = len(simplified.split())
            
            # Compare complexity (average word length)
            original_avg_word_len = sum(len(word) for word in original.split()) / original_words if original_words > 0 else 0
            simplified_avg_word_len = sum(len(word) for word in simplified.split()) / simplified_words if simplified_words > 0 else 0
            
            # Calculate reduction in word count
            word_reduction = (original_words - simplified_words) / original_words if original_words > 0 else 0
            
            # Calculate reduction in word complexity
            complexity_reduction = (original_avg_word_len - simplified_avg_word_len) / original_avg_word_len if original_avg_word_len > 0 else 0
            
            # Combined score (weighted average)
            score = (word_reduction * 0.3 + complexity_reduction * 0.7)
            
            # Ensure score is between 0 and 1
            return max(0.0, min(1.0, score))
            
        except Exception:
            return 0.1  # Default low score if calculation fails