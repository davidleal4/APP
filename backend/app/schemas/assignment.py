from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .common import BaseSchema, TimestampMixin

class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    points_possible: Optional[float] = None
    points_earned: Optional[float] = None
    completed: bool = False
    assignment_type: Optional[str] = None
    class_id: Optional[int] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    points_possible: Optional[float] = None
    points_earned: Optional[float] = None
    completed: Optional[bool] = None
    assignment_type: Optional[str] = None
    class_id: Optional[int] = None

class AssignmentInDBBase(AssignmentBase, TimestampMixin):
    id: Optional[int] = None
    user_id: int

    class Config:
        from_attributes = True

class Assignment(AssignmentInDBBase):
    pass