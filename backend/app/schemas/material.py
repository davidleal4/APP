from pydantic import BaseModel
from typing import Optional
from .common import BaseSchema, TimestampMixin

class MaterialBase(BaseModel):
    title: str
    content: Optional[str] = None
    material_type: Optional[str] = None
    url: Optional[str] = None
    file_path: Optional[str] = None

class MaterialCreate(MaterialBase):
    class_id: int

class MaterialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    material_type: Optional[str] = None
    url: Optional[str] = None
    file_path: Optional[str] = None

class MaterialInDBBase(MaterialBase, TimestampMixin):
    id: Optional[int] = None
    class_id: int

    class Config:
        from_attributes = True

class Material(MaterialInDBBase):
    pass