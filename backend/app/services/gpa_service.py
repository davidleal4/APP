import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
from app.models.models import Assignment

class GPAService:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def predict_gpa(self, assignments: List[Assignment], target_gpa: Optional[float] = None) -> Dict[str, Any]:
        """Predict GPA based on current and upcoming assignments"""
        try:
            # Group assignments by class
            class_data = {}
            for assignment in assignments:
                class_id = assignment.class_id
                if class_id not in class_data:
                    class_data[class_id] = {
                        'completed': [],
                        'upcoming': [],
                        'total_weight': 0
                    }
                
                class_data[class_id]['total_weight'] += assignment.weight
                
                if assignment.grade is not None:
                    class_data[class_id]['completed'].append(assignment)
                else:
                    class_data[class_id]['upcoming'].append(assignment)
            
            # Calculate current and predicted class GPAs
            class_predictions = {}
            overall_prediction = 0
            total_classes = len(class_data)
            
            for class_id, data in class_data.items():
                completed = data['completed']
                upcoming = data['upcoming']
                
                if completed:
                    # Calculate current weighted average for completed assignments
                    current_score = sum(a.grade * a.weight for a in completed) / sum(a.weight for a in completed)
                    
                    # Predict performance on upcoming assignments based on current performance
                    if upcoming:
                        upcoming_weight = sum(a.weight for a in upcoming)
                        completed_weight = sum(a.weight for a in completed)
                        
                        # Use trend analysis for prediction
                        predicted_upcoming_score = self._predict_upcoming_performance(completed)
                        
                        # Calculate overall class grade
                        total_weight = completed_weight + upcoming_weight
                        predicted_class_grade = (
                            (current_score * completed_weight + predicted_upcoming_score * upcoming_weight) 
                            / total_weight
                        )
                    else:
                        predicted_class_grade = current_score
                else:
                    # No completed assignments - use default prediction
                    predicted_class_grade = 85.0  # Optimistic default
                
                class_predictions[class_id] = {
                    'current_average': current_score if completed else None,
                    'predicted_grade': predicted_class_grade,
                    'confidence': self._calculate_confidence(completed)
                }
                
                overall_prediction += self._grade_to_gpa(predicted_class_grade)
            
            predicted_gpa = overall_prediction / total_classes if total_classes > 0 else 0.0
            
            return {
                'predicted_gpa': round(predicted_gpa, 2),
                'class_predictions': class_predictions,
                'confidence': self._calculate_overall_confidence(class_predictions),
                'recommendations': self._generate_recommendations(class_predictions, target_gpa)
            }
            
        except Exception as e:
            print(f"Error predicting GPA: {e}")
            return {
                'predicted_gpa': 0.0,
                'class_predictions': {},
                'confidence': 0.0,
                'recommendations': []
            }
    
    def generate_study_plan(self, assignments: List[Assignment], target_gpa: float) -> Dict[str, Any]:
        """Generate a study plan to achieve target GPA"""
        try:
            current_prediction = self.predict_gpa(assignments)
            current_gpa = current_prediction['predicted_gpa']
            
            if current_gpa >= target_gpa:
                return {
                    'status': 'on_track',
                    'message': f"You're on track to achieve your target GPA of {target_gpa}!",
                    'daily_tasks': self._generate_maintenance_tasks(assignments),
                    'focus_areas': []
                }
            
            # Calculate what needs to improve
            gpa_gap = target_gpa - current_gpa
            
            # Identify classes that need the most improvement
            focus_classes = []
            for class_id, prediction in current_prediction['class_predictions'].items():
                if prediction['predicted_grade'] < 90:  # Room for improvement
                    focus_classes.append({
                        'class_id': class_id,
                        'current_grade': prediction['predicted_grade'],
                        'improvement_needed': min(95 - prediction['predicted_grade'], gpa_gap * 25)
                    })
            
            return {
                'status': 'needs_improvement',
                'message': f"You need to improve by {gpa_gap:.2} GPA points to reach your target.",
                'daily_tasks': self._generate_improvement_tasks(assignments, focus_classes),
                'focus_areas': focus_classes,
                'weekly_goals': self._generate_weekly_goals(focus_classes)
            }
            
        except Exception as e:
            print(f"Error generating study plan: {e}")
            return {
                'status': 'error',
                'message': "Unable to generate study plan",
                'daily_tasks': [],
                'focus_areas': []
            }
    
    def _predict_upcoming_performance(self, completed_assignments: List[Assignment]) -> float:
        """Predict performance on upcoming assignments based on trends"""
        if not completed_assignments:
            return 85.0
        
        # Simple trend analysis
        grades = [a.grade for a in completed_assignments]
        if len(grades) == 1:
            return grades[0]
        
        # Calculate trend
        recent_avg = np.mean(grades[-3:]) if len(grades) >= 3 else np.mean(grades)
        overall_avg = np.mean(grades)
        
        # Weight recent performance more heavily
        return recent_avg * 0.7 + overall_avg * 0.3
    
    def _grade_to_gpa(self, grade: float) -> float:
        """Convert percentage grade to 4.0 GPA scale"""
        if grade >= 97:
            return 4.0
        elif grade >= 93:
            return 4.0
        elif grade >= 90:
            return 3.7
        elif grade >= 87:
            return 3.3
        elif grade >= 83:
            return 3.0
        elif grade >= 80:
            return 2.7
        elif grade >= 77:
            return 2.3
        elif grade >= 73:
            return 2.0
        elif grade >= 70:
            return 1.7
        elif grade >= 67:
            return 1.3
        elif grade >= 65:
            return 1.0
        else:
            return 0.0
    
    def _calculate_confidence(self, completed_assignments: List[Assignment]) -> float:
        """Calculate confidence in prediction based on data quality"""
        if not completed_assignments:
            return 0.3
        
        # More completed assignments = higher confidence
        base_confidence = min(len(completed_assignments) / 5, 1.0)
        
        # Consistent grades = higher confidence
        grades = [a.grade for a in completed_assignments]
        if len(grades) > 1:
            std_dev = np.std(grades)
            consistency_factor = max(0.5, 1.0 - (std_dev / 20))
            return base_confidence * consistency_factor
        
        return base_confidence
    
    def _calculate_overall_confidence(self, class_predictions: Dict) -> float:
        """Calculate overall confidence across all classes"""
        if not class_predictions:
            return 0.0
        
        confidences = [pred['confidence'] for pred in class_predictions.values()]
        return np.mean(confidences)
    
    def _generate_recommendations(self, class_predictions: Dict, target_gpa: Optional[float]) -> List[str]:
        """Generate study recommendations"""
        recommendations = []
        
        for class_id, prediction in class_predictions.items():
            grade = prediction['predicted_grade']
            
            if grade < 80:
                recommendations.append(f"Class {class_id}: Focus on fundamental concepts - current performance needs significant improvement")
            elif grade < 85:
                recommendations.append(f"Class {class_id}: Review recent material and practice problems")
            elif grade < 90 and target_gpa and target_gpa > 3.5:
                recommendations.append(f"Class {class_id}: Polish your understanding to reach target GPA")
        
        if not recommendations:
            recommendations.append("Keep up the excellent work! Stay consistent with your study routine.")
        
        return recommendations
    
    def _generate_maintenance_tasks(self, assignments: List[Assignment]) -> List[str]:
        """Generate daily maintenance tasks"""
        return [
            "Review flashcards for 15 minutes",
            "Complete practice problems",
            "Read ahead in course material",
            "Update assignment progress"
        ]
    
    def _generate_improvement_tasks(self, assignments: List[Assignment], focus_classes: List[Dict]) -> List[str]:
        """Generate improvement-focused daily tasks"""
        tasks = []
        
        for focus_class in focus_classes[:2]:  # Top 2 priority classes
            tasks.extend([
                f"Spend 30 minutes on Class {focus_class['class_id']} fundamentals",
                f"Complete extra practice for Class {focus_class['class_id']}",
            ])
        
        tasks.extend([
            "Review and correct past assignments",
            "Ask questions in office hours",
            "Form study group for difficult topics"
        ])
        
        return tasks
    
    def _generate_weekly_goals(self, focus_classes: List[Dict]) -> List[str]:
        """Generate weekly study goals"""
        goals = []
        
        for focus_class in focus_classes:
            improvement = focus_class['improvement_needed']
            goals.append(f"Improve Class {focus_class['class_id']} grade by {improvement:.1f} points")
        
        return goals

gpa_service = GPAService()