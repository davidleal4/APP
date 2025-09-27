from pydantic import BaseModel, EmailStr
from typing import Optional, List, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    plan: str
    first_login: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class MagicLinkRequest(BaseModel):
    email: EmailStr

# Class schemas
class ClassBase(BaseModel):
    name: str
    instructor: Optional[str] = None

class ClassCreate(ClassBase):
    pass

class Class(ClassBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Assignment schemas
class AssignmentBase(BaseModel):
    title: str
    due_date: Optional[datetime] = None
    weight: float = 0.0
    assignment_type: Optional[str] = None

class AssignmentCreate(AssignmentBase):
    class_id: int

class AssignmentUpdate(BaseModel):
    grade: Optional[float] = None

class Assignment(AssignmentBase):
    id: int
    class_id: int
    grade: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Material schemas
class MaterialBase(BaseModel):
    filename: str
    text: Optional[str] = None

class MaterialCreate(MaterialBase):
    class_id: int

class Material(MaterialBase):
    id: int
    class_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Flashcard schemas
class FlashcardBase(BaseModel):
    question: str
    answer: str

class FlashcardCreate(FlashcardBase):
    class_id: int

class Flashcard(FlashcardBase):
    id: int
    class_id: int
    due_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Project schemas
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    members_json: Optional[List[str]] = None

class ProjectCreate(ProjectBase):
    class_id: int

class Project(ProjectBase):
    id: int
    class_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# AI service schemas
class DeadlineExtractionRequest(BaseModel):
    text: str

class FlashcardGenerationRequest(BaseModel):
    class_id: int
    text: str
    count: int = 10

class QuizGenerationRequest(BaseModel):
    class_id: int
    text: str
    count: int = 5

class GPAPredictionRequest(BaseModel):
    assignments: List[Assignment]

class StudyPlanRequest(BaseModel):
    target_gpa: float
    current_assignments: List[Assignment]

# Billing schemas
class CheckoutRequest(BaseModel):
    plan: str  # pro, team

class WebhookEvent(BaseModel):
    type: str
    data: dict