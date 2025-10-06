from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api.v1 import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Assignment])
def read_assignments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve assignments for current user.
    """
    assignments = db.query(models.Assignment).filter(
        models.Assignment.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return assignments

@router.post("/", response_model=schemas.Assignment)
def create_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_in: schemas.AssignmentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new assignment.
    """
    assignment_obj = models.Assignment(**assignment_in.dict(), user_id=current_user.id)
    db.add(assignment_obj)
    db.commit()
    db.refresh(assignment_obj)
    return assignment_obj

@router.get("/{assignment_id}", response_model=schemas.Assignment)
def read_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get assignment by ID.
    """
    assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id,
        models.Assignment.user_id == current_user.id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment

@router.put("/{assignment_id}", response_model=schemas.Assignment)
def update_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: int,
    assignment_in: schemas.AssignmentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an assignment.
    """
    assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id,
        models.Assignment.user_id == current_user.id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    update_data = assignment_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)
    
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment

@router.delete("/{assignment_id}")
def delete_assignment(
    *,
    db: Session = Depends(deps.get_db),
    assignment_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an assignment.
    """
    assignment = db.query(models.Assignment).filter(
        models.Assignment.id == assignment_id,
        models.Assignment.user_id == current_user.id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}