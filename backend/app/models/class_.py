from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.db import Base

class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=True)  # e.g., CS101
    description = Column(Text, nullable=True)
    credits = Column(Integer, default=3)
    semester = Column(String, nullable=True)  # e.g., Fall 2024
    professor = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="classes")
    assignments = relationship("Assignment", back_populates="class_")
    materials = relationship("Material", back_populates="class_")