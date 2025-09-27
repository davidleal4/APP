from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.db import Base

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    material_type = Column(String, nullable=True)  # pdf, video, link, note, etc.
    url = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    
    # Foreign keys
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    class_ = relationship("Class", back_populates="materials")
    flashcards = relationship("Flashcard", back_populates="material")