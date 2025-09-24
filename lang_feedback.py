import logging
from typing import List, Dict, Any, Optional
import re

class LanguageFeedback:
    def __init__(self):
        self.language_tool = None
        self._initialize_language_tool()
    
    def _initialize_language_tool(self):
        """Initialize LanguageTool with proper error handling"""
        try:
            import language_tool_python
            self.language_tool = language_tool_python.LanguageTool('en-US')
            logging.info("LanguageTool initialized successfully")
        except ImportError:
            logging.warning(
                "LanguageTool not available atm.
                أداة اللغة غير متوفرة في الوقت الحالي"
            )
            self.language_tool = None
        except Exception as e:
            logging.warning(f"Failed to initialize LanguageTool: {e}")
            self.language_tool = None
    
    def get_feedback(self, text: str) -> Dict[str, Any]:
        """Get comprehensive language feedback for the given text"""
        if not text or not text.strip():
            return {"error": "No text provided", "suggestions": []}
        
        feedback = {
            "grammar_issues": [],
            "spelling_issues": [],
            "style_suggestions": [],
            "overall_score": 0,
            "word_count": len(text.split()),
            "character_count": len(text)
        }
        
        # Basic grammar and spelling checks as fallback
        feedback.update(self._basic_checks(text))
        
        # Advanced checks with LanguageTool if available
        if self.language_tool is not None:
            try:
                advanced_feedback = self._advanced_checks(text)
                feedback.update(advanced_feedback)
            except Exception as e:
                logging.error(f"Advanced checks failed: {e}")
                # Fallback to basic checks only
        
        return feedback
    
    def _basic_checks(self, text: str) -> Dict[str, Any]:
        """Perform basic grammar and spelling checks as fallback"""
        suggestions = []
        
        # Common spelling mistakes pattern (basic fallback)
        common_mistakes = {
            'recieve': 'receive',
            'seperate': 'separate',
            'definately': 'definitely',
            'occured': 'occurred',
            'untill': 'until',
            'accomodate': 'accommodate'
        }
        
        for wrong, correct in common_mistakes.items():
            if wrong in text.lower():
                suggestions.append({
                    "issue": f"Spelling: '{wrong}'",
                    "suggestion": f"Use '{correct}' instead",
                    "category": "spelling"
                })
        
        # Basic punctuation checks
        if not text.strip().endswith(('.', '!', '?')):
            suggestions.append({
                "issue": "Missing ending punctuation",
                "suggestion": "Add proper punctuation at the end (. ! ?)",
                "category": "punctuation"
            })
        
        # Check for multiple spaces
        if '  ' in text:
            suggestions.append({
                "issue": "Multiple consecutive spaces",
                "suggestion": "Use single spaces between words",
                "category": "formatting"
            })
        
        return {"suggestions": suggestions}
    
    def _advanced_checks(self, text: str) -> Dict[str, Any]:
        """Perform advanced checks using LanguageTool"""
        matches = self.language_tool.check(text)
        
        grammar_issues = []
        spelling_issues = []
        style_suggestions = []
        
        for match in matches:
            issue = {
                "issue": match.message,
                "suggestion": match.replacements[:3] if match.replacements else [],
                "offset": match.offset,
                "length": match.errorLength,
                "category": match.rule.category
            }
            
            if match.rule.category == 'Grammar':
                grammar_issues.append(issue)
            elif match.rule.category == 'Spelling':
                spelling_issues.append(issue)
            elif match.rule.category in ['Style', 'Punctuation']:
                style_suggestions.append(issue)
        
        # Calculate a basic score (higher is better)
        total_issues = len(grammar_issues) + len(spelling_issues)
        word_count = len(text.split())
        if word_count > 0:
            issue_density = total_issues / word_count
            overall_score = max(0, 100 - (issue_density * 1000))  # Scale factor
        else:
            overall_score = 0
        
        return {
            "grammar_issues": grammar_issues,
            "spelling_issues": spelling_issues,
            "style_suggestions": style_suggestions,
            "overall_score": round(overall_score, 1)
        }
    
    def get_installation_instruction(self) -> str:
        """Get installation instructions if LanguageTool is not available"""
        if self.language_tool is None:
            return (
                "For enhanced grammar checking, install LanguageTool:\n"
                "pip install language-tool-python"
            )
        return "LanguageTool is available and working correctly."

# Singleton instance for easy access
language_feedback = LanguageFeedback()
