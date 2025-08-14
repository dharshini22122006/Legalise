"""Granite-powered clause simplification module."""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List, Dict, Any, Optional
from ..utils import get_logger, cached, Config

logger = get_logger(__name__)

class GraniteSimplifier:
    """Granite model-powered legal clause simplifier."""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_config = Config.get_model_config()
        self._load_model()
    
    def _load_model(self):
        """Load the Granite model and tokenizer."""
        try:
            logger.info(f"Loading Granite model: {self.model_config['model_name']}")
            
            # Try to load the primary model
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_config['model_name'],
                    trust_remote_code=True
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_config['model_name'],
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                    device_map="auto" if torch.cuda.is_available() else None,
                    trust_remote_code=True
                )
                
                # Set pad token if not exists
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                logger.info("Granite model loaded successfully")
                
            except Exception as e:
                logger.warning(f"Failed to load primary model: {str(e)}")
                logger.info("Loading fallback model...")
                
                # Fallback to a simpler model
                self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
                self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
                
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                logger.info("Fallback model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    @cached(ttl=3600)
    def simplify_clause(self, clause: str, context: str = "") -> Dict[str, Any]:
        """Simplify a legal clause using the Granite model."""
        try:
            if not clause.strip():
                return {
                    'original_clause': clause,
                    'simplified_clause': clause,
                    'simplification_score': 0.0,
                    'key_points': [],
                    'plain_english_summary': clause
                }
            
            # Create prompt for simplification
            prompt = self._create_simplification_prompt(clause, context)
            
            # Generate simplified version
            simplified_text = self._generate_text(prompt)
            
            # Extract key points
            key_points = self._extract_key_points(clause)
            
            # Create plain English summary
            summary = self._create_plain_english_summary(clause, simplified_text)
            
            # Calculate simplification score
            score = self._calculate_simplification_score(clause, simplified_text)
            
            return {
                'original_clause': clause,
                'simplified_clause': simplified_text,
                'simplification_score': score,
                'key_points': key_points,
                'plain_english_summary': summary,
                'word_count_reduction': len(clause.split()) - len(simplified_text.split())
            }
            
        except Exception as e:
            logger.error(f"Error simplifying clause: {str(e)}")
            return {
                'original_clause': clause,
                'simplified_clause': self._fallback_simplification(clause),
                'simplification_score': 0.5,
                'key_points': self._extract_key_points(clause),
                'plain_english_summary': self._fallback_simplification(clause)
            }
    
    def _create_simplification_prompt(self, clause: str, context: str = "") -> str:
        """Create a prompt for clause simplification."""
        prompt = f"""
Task: Simplify the following legal clause into plain English that anyone can understand.

Instructions:
- Remove legal jargon and complex terms
- Use simple, everyday language
- Keep the same meaning and legal intent
- Make it conversational and easy to read
- Focus on what it means in practical terms

Legal Clause: {clause}

Simplified Version:"""
        
        return prompt
    
    def _generate_text(self, prompt: str) -> str:
        """Generate text using the loaded model."""
        try:
            # Tokenize input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt", truncate=True, max_length=512)
            inputs = inputs.to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 150,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1,
                    no_repeat_ngram_size=2
                )
            
            # Decode response
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part (after the prompt)
            if "Simplified Version:" in generated_text:
                simplified = generated_text.split("Simplified Version:")[-1].strip()
            else:
                simplified = generated_text[len(prompt):].strip()
            
            # Clean up the response
            simplified = self._clean_generated_text(simplified)
            
            return simplified if simplified else self._fallback_simplification(prompt)
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            return self._fallback_simplification(prompt)
    
    def _clean_generated_text(self, text: str) -> str:
        """Clean up generated text."""
        # Remove common artifacts
        text = text.replace("</s>", "").replace("<s>", "")
        text = text.replace("[INST]", "").replace("[/INST]", "")
        
        # Take only the first paragraph/sentence if multiple
        lines = text.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('Task:', 'Instructions:', 'Legal Clause:')):
                cleaned_lines.append(line)
        
        result = ' '.join(cleaned_lines)
        
        # Limit length
        words = result.split()
        if len(words) > 100:
            result = ' '.join(words[:100]) + "..."
        
        return result.strip()
    
    def _fallback_simplification(self, clause: str) -> str:
        """Provide fallback simplification when model fails."""
        # Simple rule-based simplification
        simplified = clause
        
        # Replace common legal terms
        replacements = {
            'whereas': 'while',
            'hereby': 'by this document',
            'herein': 'in this document',
            'hereof': 'of this document',
            'hereunder': 'under this document',
            'notwithstanding': 'despite',
            'pursuant to': 'according to',
            'shall': 'will',
            'covenant': 'promise',
            'indemnify': 'protect from loss',
            'liability': 'responsibility for damages',
            'breach': 'breaking the agreement',
            'termination': 'ending the agreement'
        }
        
        for legal_term, simple_term in replacements.items():
            simplified = simplified.replace(legal_term, simple_term)
        
        return simplified
    
    def _extract_key_points(self, clause: str) -> List[str]:
        """Extract key points from a clause."""
        key_points = []
        
        # Look for key action words and phrases
        action_patterns = [
            r'shall\s+([^.]+)',
            r'must\s+([^.]+)',
            r'will\s+([^.]+)',
            r'agree\s+to\s+([^.]+)',
            r'responsible\s+for\s+([^.]+)',
            r'obligated\s+to\s+([^.]+)'
        ]
        
        import re
        for pattern in action_patterns:
            matches = re.findall(pattern, clause, re.IGNORECASE)
            for match in matches:
                key_points.append(match.strip())
        
        # If no specific patterns found, extract sentences
        if not key_points:
            sentences = clause.split('.')
            for sentence in sentences[:3]:  # Take first 3 sentences
                if len(sentence.strip()) > 20:
                    key_points.append(sentence.strip())
        
        return key_points[:5]  # Limit to 5 key points
    
    def _create_plain_english_summary(self, original: str, simplified: str) -> str:
        """Create a plain English summary."""
        if len(simplified) > 10:
            return simplified
        
        # Fallback summary
        summary = f"This clause means: {self._fallback_simplification(original)}"
        return summary[:200] + "..." if len(summary) > 200 else summary
    
    def _calculate_simplification_score(self, original: str, simplified: str) -> float:
        """Calculate how much the text was simplified."""
        try:
            # Simple metrics for simplification
            original_words = len(original.split())
            simplified_words = len(simplified.split())
            
            # Word reduction score
            word_reduction = (original_words - simplified_words) / original_words if original_words > 0 else 0
            
            # Complexity reduction (based on average word length)
            original_avg_word_len = sum(len(word) for word in original.split()) / original_words if original_words > 0 else 0
            simplified_avg_word_len = sum(len(word) for word in simplified.split()) / simplified_words if simplified_words > 0 else 0
            
            complexity_reduction = (original_avg_word_len - simplified_avg_word_len) / original_avg_word_len if original_avg_word_len > 0 else 0
            
            # Combined score
            score = (word_reduction + complexity_reduction) / 2
            return max(0.0, min(1.0, score))  # Clamp between 0 and 1
            
        except:
            return 0.5
    
    def simplify_document_clauses(self, clauses: List[str], context: str = "") -> List[Dict[str, Any]]:
        """Simplify multiple clauses from a document."""
        try:
            simplified_clauses = []
            
            for i, clause in enumerate(clauses):
                logger.info(f"Simplifying clause {i+1}/{len(clauses)}")
                simplified = self.simplify_clause(clause, context)
                simplified_clauses.append(simplified)
            
            return simplified_clauses
            
        except Exception as e:
            logger.error(f"Error simplifying document clauses: {str(e)}")
            raise