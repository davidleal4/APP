from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .common import BaseSchema, TimestampMixin

class FlashcardBase(BaseModel):
    question: str
    answer: str
    difficulty: str = "medium"
    material_id: Optional[int] = None

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    difficulty: Optional[str] = None
    last_reviewed: Optional[datetime] = None
    review_count: Optional[int] = None
    correct_count: Optional[int] = None

class FlashcardInDBBase(FlashcardBase, TimestampMixin):
    id: Optional[int] = None
    user_id: int
    last_reviewed: Optional[datetime] = None
    review_count: int = 0
    correct_count: int = 0
    is_ai_generated: bool = False

    class Config:
        from_attributes = True

class Flashcard(FlashcardInDBBase):
    pass