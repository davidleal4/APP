from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.v1 import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Flashcard])
def read_flashcards(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve flashcards for current user.
    """
    flashcards = db.query(models.Flashcard).filter(
        models.Flashcard.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return flashcards

@router.post("/", response_model=schemas.Flashcard)
def create_flashcard(
    *,
    db: Session = Depends(deps.get_db),
    flashcard_in: schemas.FlashcardCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new flashcard.
    """
    flashcard_obj = models.Flashcard(**flashcard_in.dict(), user_id=current_user.id)
    db.add(flashcard_obj)
    db.commit()
    db.refresh(flashcard_obj)
    return flashcard_obj

@router.get("/{flashcard_id}", response_model=schemas.Flashcard)
def read_flashcard(
    *,
    db: Session = Depends(deps.get_db),
    flashcard_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get flashcard by ID.
    """
    flashcard = db.query(models.Flashcard).filter(
        models.Flashcard.id == flashcard_id,
        models.Flashcard.user_id == current_user.id
    ).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    return flashcard

@router.put("/{flashcard_id}", response_model=schemas.Flashcard)
def update_flashcard(
    *,
    db: Session = Depends(deps.get_db),
    flashcard_id: int,
    flashcard_in: schemas.FlashcardUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a flashcard.
    """
    flashcard = db.query(models.Flashcard).filter(
        models.Flashcard.id == flashcard_id,
        models.Flashcard.user_id == current_user.id
    ).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    update_data = flashcard_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(flashcard, field, value)
    
    db.add(flashcard)
    db.commit()
    db.refresh(flashcard)
    return flashcard

@router.delete("/{flashcard_id}")
def delete_flashcard(
    *,
    db: Session = Depends(deps.get_db),
    flashcard_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a flashcard.
    """
    flashcard = db.query(models.Flashcard).filter(
        models.Flashcard.id == flashcard_id,
        models.Flashcard.user_id == current_user.id
    ).first()
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    db.delete(flashcard)
    db.commit()
    return {"message": "Flashcard deleted successfully"}