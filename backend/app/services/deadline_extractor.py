import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import openai
from app.core.config import settings

class DeadlineExtractor:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
    
    def extract_deadlines_from_text(self, text: str) -> List[Dict]:
        """
        Extract deadlines from syllabus or assignment text using both regex and AI
        """
        deadlines = []
        
        # First try regex patterns
        regex_deadlines = self._extract_with_regex(text)
        deadlines.extend(regex_deadlines)
        
        # Then try AI extraction if available
        if settings.OPENAI_API_KEY:
            ai_deadlines = self._extract_with_ai(text)
            deadlines.extend(ai_deadlines)
        
        # Remove duplicates and return
        return self._deduplicate_deadlines(deadlines)
    
    def _extract_with_regex(self, text: str) -> List[Dict]:
        """Extract deadlines using regex patterns"""
        deadlines = []
        
        # Common date patterns
        date_patterns = [
            r'due\s+(?:on\s+)?(\w+\s+\d{1,2}(?:,\s*\d{4})?)',  # due March 15, 2024
            r'deadline[:\s]+(\w+\s+\d{1,2}(?:,\s*\d{4})?)',     # deadline: March 15
            r'submit\s+by\s+(\w+\s+\d{1,2}(?:,\s*\d{4})?)',     # submit by March 15
            r'(\d{1,2}/\d{1,2}/\d{2,4})',                       # 03/15/2024
            r'(\d{1,2}-\d{1,2}-\d{2,4})',                       # 03-15-2024
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    date_str = match.group(1)
                    parsed_date = self._parse_date_string(date_str)
                    if parsed_date:
                        # Extract surrounding context for assignment name
                        start = max(0, match.start() - 50)
                        end = min(len(text), match.end() + 50)
                        context = text[start:end].strip()
                        
                        deadlines.append({
                            'date': parsed_date,
                            'context': context,
                            'source': 'regex'
                        })
                except Exception:
                    continue
        
        return deadlines
    
    def _extract_with_ai(self, text: str) -> List[Dict]:
        """Extract deadlines using OpenAI"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "Extract all assignment deadlines from the given text. Return a JSON list with 'assignment_name', 'due_date' (YYYY-MM-DD format), and 'description' fields."
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=500
            )
            
            # Parse AI response (simplified - in production, you'd handle this more robustly)
            ai_result = response.choices[0].message.content
            # This would need proper JSON parsing in production
            return []  # Placeholder
            
        except Exception as e:
            print(f"AI extraction failed: {e}")
            return []
    
    def _parse_date_string(self, date_str: str) -> Optional[datetime]:
        """Parse various date string formats"""
        date_formats = [
            "%B %d, %Y",    # March 15, 2024
            "%B %d",        # March 15 (current year)
            "%m/%d/%Y",     # 03/15/2024
            "%m/%d/%y",     # 03/15/24
            "%m-%d-%Y",     # 03-15-2024
            "%m-%d-%y",     # 03-15-24
        ]
        
        for fmt in date_formats:
            try:
                parsed = datetime.strptime(date_str.strip(), fmt)
                # If no year specified, assume current year
                if parsed.year == 1900:
                    parsed = parsed.replace(year=datetime.now().year)
                return parsed
            except ValueError:
                continue
        
        return None
    
    def _deduplicate_deadlines(self, deadlines: List[Dict]) -> List[Dict]:
        """Remove duplicate deadlines based on date similarity"""
        unique_deadlines = []
        for deadline in deadlines:
            is_duplicate = False
            for existing in unique_deadlines:
                # Consider dates duplicate if within 1 day of each other
                if abs((deadline['date'] - existing['date']).days) <= 1:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                unique_deadlines.append(deadline)
        
        return unique_deadlines