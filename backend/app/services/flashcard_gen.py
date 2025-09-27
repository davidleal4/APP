from typing import List, Dict
import openai
from app.core.config import settings

class FlashcardGenerator:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
    
    def generate_flashcards_from_content(self, content: str, num_cards: int = 10) -> List[Dict]:
        """
        Generate flashcards from study material content using AI
        """
        if not settings.OPENAI_API_KEY:
            return self._generate_simple_flashcards(content, num_cards)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"""Create {num_cards} educational flashcards from the provided content. 
                        Each flashcard should have a clear question and a concise answer.
                        Focus on key concepts, definitions, and important facts.
                        Return as JSON array with 'question' and 'answer' fields."""
                    },
                    {"role": "user", "content": content}
                ],
                max_tokens=1000
            )
            
            # In production, you'd properly parse this JSON response
            ai_response = response.choices[0].message.content
            
            # Placeholder parsing - in production, use proper JSON parsing
            return self._parse_ai_flashcards(ai_response)
            
        except Exception as e:
            print(f"AI flashcard generation failed: {e}")
            return self._generate_simple_flashcards(content, num_cards)
    
    def generate_from_topic(self, topic: str, difficulty: str = "medium", num_cards: int = 5) -> List[Dict]:
        """
        Generate flashcards for a specific topic
        """
        if not settings.OPENAI_API_KEY:
            return []
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"""Create {num_cards} flashcards about {topic} at {difficulty} difficulty level.
                        Include a mix of definition questions, concept explanations, and practical applications.
                        Return as JSON array with 'question', 'answer', and 'difficulty' fields."""
                    },
                    {"role": "user", "content": f"Generate flashcards about: {topic}"}
                ],
                max_tokens=800
            )
            
            ai_response = response.choices[0].message.content
            return self._parse_ai_flashcards(ai_response, difficulty)
            
        except Exception as e:
            print(f"Topic flashcard generation failed: {e}")
            return []
    
    def _generate_simple_flashcards(self, content: str, num_cards: int) -> List[Dict]:
        """
        Fallback method for generating flashcards without AI
        """
        # Simple keyword extraction approach
        sentences = content.split('.')
        flashcards = []
        
        for i, sentence in enumerate(sentences[:num_cards]):
            sentence = sentence.strip()
            if len(sentence) > 20:  # Only use substantial sentences
                # Create a simple question by replacing key terms
                words = sentence.split()
                if len(words) > 5:
                    # Replace a key word with a blank
                    key_word_idx = len(words) // 2
                    key_word = words[key_word_idx]
                    
                    question = sentence.replace(key_word, "______")
                    answer = key_word
                    
                    flashcards.append({
                        "question": f"Fill in the blank: {question}",
                        "answer": answer,
                        "difficulty": "medium"
                    })
        
        return flashcards
    
    def _parse_ai_flashcards(self, ai_response: str, default_difficulty: str = "medium") -> List[Dict]:
        """
        Parse AI response into flashcard format
        In production, this would use proper JSON parsing
        """
        # Placeholder implementation
        # In real app, you'd parse the JSON response from AI
        return [
            {
                "question": "What is the main topic discussed?",
                "answer": "The content provided by the user",
                "difficulty": default_difficulty
            }
        ]
    
    def optimize_flashcard_difficulty(self, flashcards: List[Dict], user_performance: Dict) -> List[Dict]:
        """
        Adjust flashcard difficulty based on user performance
        """
        optimized = []
        
        for card in flashcards:
            # Adjust difficulty based on user's success rate
            success_rate = user_performance.get('success_rate', 0.5)
            
            current_difficulty = card.get('difficulty', 'medium')
            
            if success_rate > 0.8 and current_difficulty != 'hard':
                # User is doing well, increase difficulty
                if current_difficulty == 'easy':
                    card['difficulty'] = 'medium'
                elif current_difficulty == 'medium':
                    card['difficulty'] = 'hard'
            elif success_rate < 0.4 and current_difficulty != 'easy':
                # User struggling, decrease difficulty
                if current_difficulty == 'hard':
                    card['difficulty'] = 'medium'
                elif current_difficulty == 'medium':
                    card['difficulty'] = 'easy'
            
            optimized.append(card)
        
        return optimized