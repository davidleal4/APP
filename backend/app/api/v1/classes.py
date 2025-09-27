from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.v1 import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Class])
def read_classes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve classes for current user.
    """
    classes = db.query(models.Class).filter(
        models.Class.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return classes

@router.post("/", response_model=schemas.Class)
def create_class(
    *,
    db: Session = Depends(deps.get_db),
    class_in: schemas.ClassCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new class.
    """
    class_obj = models.Class(**class_in.dict(), owner_id=current_user.id)
    db.add(class_obj)
    db.commit()
    db.refresh(class_obj)
    return class_obj

@router.get("/{class_id}", response_model=schemas.Class)
def read_class(
    *,
    db: Session = Depends(deps.get_db),
    class_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get class by ID.
    """
    class_obj = db.query(models.Class).filter(
        models.Class.id == class_id,
        models.Class.owner_id == current_user.id
    ).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    return class_obj

@router.put("/{class_id}", response_model=schemas.Class)
def update_class(
    *,
    db: Session = Depends(deps.get_db),
    class_id: int,
    class_in: schemas.ClassUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a class.
    """
    class_obj = db.query(models.Class).filter(
        models.Class.id == class_id,
        models.Class.owner_id == current_user.id
    ).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    update_data = class_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(class_obj, field, value)
    
    db.add(class_obj)
    db.commit()
    db.refresh(class_obj)
    return class_obj

@router.delete("/{class_id}")
def delete_class(
    *,
    db: Session = Depends(deps.get_db),
    class_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a class.
    """
    class_obj = db.query(models.Class).filter(
        models.Class.id == class_id,
        models.Class.owner_id == current_user.id
    ).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")
    
    db.delete(class_obj)
    db.commit()
    return {"message": "Class deleted successfully"}