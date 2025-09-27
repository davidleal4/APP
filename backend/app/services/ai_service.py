import openai
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import re
from app.core.config import settings

# Initialize OpenAI
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY

class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
    
    def extract_deadlines(self, text: str) -> List[Dict[str, Any]]:
        """Extract assignment deadlines from syllabus text"""
        if not self.client:
            return self._mock_deadline_extraction(text)
        
        try:
            prompt = f"""
            Extract assignments and deadlines from the following syllabus text.
            Return a JSON array of assignments with the following structure:
            {{
                "title": "Assignment name",
                "due_date": "YYYY-MM-DD" or null if no date,
                "type": "homework|exam|project|quiz|other",
                "weight": percentage as float (0.0-1.0) or 0.0 if not specified
            }}
            
            Text:
            {text}
            
            Only extract clear assignments with deadlines. Be conservative.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            # Parse JSON from response
            assignments = json.loads(result)
            return assignments
            
        except Exception as e:
            print(f"Error extracting deadlines: {e}")
            return self._mock_deadline_extraction(text)
    
    def generate_flashcards(self, text: str, count: int = 10) -> List[Dict[str, str]]:
        """Generate flashcards from study material"""
        if not self.client:
            return self._mock_flashcards(count)
        
        try:
            prompt = f"""
            Generate {count} study flashcards from the following text.
            Return a JSON array with this exact structure:
            [
                {{
                    "question": "Clear, specific question",
                    "answer": "Concise, accurate answer"
                }}
            ]
            
            Make questions that test understanding, not just memorization.
            
            Text:
            {text}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            flashcards = json.loads(result)
            return flashcards
            
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return self._mock_flashcards(count)
    
    def generate_quiz(self, text: str, count: int = 5) -> List[Dict[str, Any]]:
        """Generate multiple choice quiz from study material"""
        if not self.client:
            return self._mock_quiz(count)
        
        try:
            prompt = f"""
            Generate {count} multiple choice questions from the following text.
            Return a JSON array with this exact structure:
            [
                {{
                    "question": "Question text",
                    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                    "correct_answer": "A",
                    "explanation": "Brief explanation of why this is correct"
                }}
            ]
            
            Text:
            {text}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            result = response.choices[0].message.content
            quiz = json.loads(result)
            return quiz
            
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return self._mock_quiz(count)
    
    def generate_summary(self, text: str) -> str:
        """Generate study summary from material"""
        if not self.client:
            return self._mock_summary(text)
        
        try:
            prompt = f"""
            Create a concise study summary of the key points from this text.
            Focus on the most important concepts that students should know for exams.
            Use bullet points and clear organization.
            
            Text:
            {text}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._mock_summary(text)
    
    def chat_with_material(self, question: str, context: str) -> str:
        """Answer questions about study material"""
        if not self.client:
            return f"Based on the material, here's what I understand about your question: {question}"
        
        try:
            prompt = f"""
            You are a helpful study assistant. Answer the student's question based on the provided material.
            Be accurate and helpful. If the answer isn't in the material, say so.
            
            Material:
            {context}
            
            Question: {question}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return "I'm sorry, I couldn't process your question right now. Please try again."
    
    # Mock methods for when OpenAI API is not available
    def _mock_deadline_extraction(self, text: str) -> List[Dict[str, Any]]:
        """Mock deadline extraction for testing"""
        return [
            {
                "title": "Midterm Exam",
                "due_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
                "type": "exam",
                "weight": 0.3
            },
            {
                "title": "Final Project",
                "due_date": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
                "type": "project", 
                "weight": 0.4
            }
        ]
    
    def _mock_flashcards(self, count: int) -> List[Dict[str, str]]:
        """Mock flashcard generation for testing"""
        return [
            {
                "question": f"Sample question {i+1}",
                "answer": f"Sample answer {i+1}"
            } for i in range(count)
        ]
    
    def _mock_quiz(self, count: int) -> List[Dict[str, Any]]:
        """Mock quiz generation for testing"""
        return [
            {
                "question": f"Sample question {i+1}?",
                "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
                "correct_answer": "A",
                "explanation": f"Explanation for question {i+1}"
            } for i in range(count)
        ]
    
    def _mock_summary(self, text: str) -> str:
        """Mock summary generation for testing"""
        return f"Summary of the provided material:\n\n• Key point 1\n• Key point 2\n• Key point 3\n\nThis is a sample summary generated from: {text[:100]}..."

ai_service = AIService()