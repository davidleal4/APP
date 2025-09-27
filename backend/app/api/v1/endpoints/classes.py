from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.models import User, Class
from app.schemas.schemas import ClassCreate, Class as ClassSchema
from app.core.config import settings

router = APIRouter()

@router.get("/", response_model=List[ClassSchema])
def get_classes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all classes for the current user"""
    return db.query(Class).filter(Class.user_id == current_user.id).all()

@router.post("/", response_model=ClassSchema)
def create_class(
    class_data: ClassCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Create a new class"""
    # Check plan limits for free users
    if current_user.plan == "free":
        existing_classes = db.query(Class).filter(Class.user_id == current_user.id).count()
        if existing_classes >= settings.FREE_PLAN_CLASSES_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Free plan limited to {settings.FREE_PLAN_CLASSES_LIMIT} classes. Upgrade to Pro for unlimited classes."
            )
    
    class_obj = Class(
        user_id=current_user.id,
        name=class_data.name,
        instructor=class_data.instructor
    )
    
    db.add(class_obj)
    db.commit()
    db.refresh(class_obj)
    
    return class_obj

@router.get("/{class_id}", response_model=ClassSchema)
def get_class(
    class_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Get a specific class"""
    class_obj = db.query(Class).filter(
        Class.id == class_id, 
        Class.user_id == current_user.id
    ).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    return class_obj

@router.put("/{class_id}", response_model=ClassSchema)
def update_class(
    class_id: int, 
    class_data: ClassCreate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Update a class"""
    class_obj = db.query(Class).filter(
        Class.id == class_id, 
        Class.user_id == current_user.id
    ).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    class_obj.name = class_data.name
    class_obj.instructor = class_data.instructor
    
    db.commit()
    db.refresh(class_obj)
    
    return class_obj

@router.delete("/{class_id}")
def delete_class(
    class_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Delete a class"""
    class_obj = db.query(Class).filter(
        Class.id == class_id, 
        Class.user_id == current_user.id
    ).first()
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    db.delete(class_obj)
    db.commit()
    
    return {"message": "Class deleted successfully"}