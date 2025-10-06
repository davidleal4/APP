from typing import Any, List, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models
from app.api.v1 import deps

router = APIRouter()

@router.get("/calculate")
def calculate_gpa(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Calculate current GPA based on completed assignments.
    """
    # Get all classes with completed assignments
    classes = db.query(models.Class).filter(
        models.Class.owner_id == current_user.id
    ).all()
    
    total_grade_points = 0
    total_credits = 0
    class_grades = []
    
    for class_obj in classes:
        assignments = db.query(models.Assignment).filter(
            models.Assignment.class_id == class_obj.id,
            models.Assignment.completed == True,
            models.Assignment.points_possible.isnot(None),
            models.Assignment.points_earned.isnot(None)
        ).all()
        
        if assignments:
            total_possible = sum(a.points_possible for a in assignments)
            total_earned = sum(a.points_earned for a in assignments)
            
            if total_possible > 0:
                percentage = (total_earned / total_possible) * 100
                grade_point = percentage_to_gpa(percentage)
                
                class_grades.append({
                    "class_name": class_obj.name,
                    "percentage": percentage,
                    "grade_point": grade_point,
                    "credits": class_obj.credits
                })
                
                total_grade_points += grade_point * class_obj.credits
                total_credits += class_obj.credits
    
    overall_gpa = total_grade_points / total_credits if total_credits > 0 else 0
    
    return {
        "overall_gpa": round(overall_gpa, 2),
        "total_credits": total_credits,
        "class_grades": class_grades
    }

@router.get("/predict")
def predict_gpa(
    target_gpa: float = 3.5,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Predict what grades are needed to achieve target GPA.
    """
    # This is a simplified prediction - in a real app, you'd use more sophisticated algorithms
    current_data = calculate_gpa(db=db, current_user=current_user)
    current_gpa = current_data["overall_gpa"]
    current_credits = current_data["total_credits"]
    
    # Get upcoming assignments
    upcoming_assignments = db.query(models.Assignment).filter(
        models.Assignment.user_id == current_user.id,
        models.Assignment.completed == False
    ).all()
    
    return {
        "current_gpa": current_gpa,
        "target_gpa": target_gpa,
        "current_credits": current_credits,
        "upcoming_assignments": len(upcoming_assignments),
        "recommendation": f"To achieve a {target_gpa} GPA, focus on completing assignments with high quality."
    }

def percentage_to_gpa(percentage: float) -> float:
    """Convert percentage to 4.0 GPA scale"""
    if percentage >= 97:
        return 4.0
    elif percentage >= 93:
        return 3.7
    elif percentage >= 90:
        return 3.3
    elif percentage >= 87:
        return 3.0
    elif percentage >= 83:
        return 2.7
    elif percentage >= 80:
        return 2.3
    elif percentage >= 77:
        return 2.0
    elif percentage >= 73:
        return 1.7
    elif percentage >= 70:
        return 1.3
    elif percentage >= 67:
        return 1.0
    elif percentage >= 65:
        return 0.7
    else:
        return 0.0