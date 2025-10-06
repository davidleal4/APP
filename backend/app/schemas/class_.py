from pydantic import BaseModel
from typing import Optional
from .common import BaseSchema, TimestampMixin

class ClassBase(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    credits: int = 3
    semester: Optional[str] = None
    professor: Optional[str] = None

class ClassCreate(ClassBase):
    pass

class ClassUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    credits: Optional[int] = None
    semester: Optional[str] = None
    professor: Optional[str] = None

class ClassInDBBase(ClassBase, TimestampMixin):
    id: Optional[int] = None
    owner_id: int

    class Config:
        from_attributes = True

class Class(ClassInDBBase):
    pass