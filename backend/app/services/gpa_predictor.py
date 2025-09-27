from typing import List, Dict, Optional
from datetime import datetime, timedelta
import statistics

class GPAPredictor:
    def __init__(self):
        pass
    
    def predict_semester_gpa(self, classes: List[Dict], current_assignments: List[Dict]) -> Dict:
        """
        Predict end-of-semester GPA based on current performance and remaining assignments
        """
        predictions = {}
        total_predicted_grade_points = 0
        total_credits = 0
        
        for class_info in classes:
            class_id = class_info['id']
            credits = class_info['credits']
            
            # Get assignments for this class
            class_assignments = [a for a in current_assignments if a.get('class_id') == class_id]
            
            # Calculate current performance
            completed_assignments = [a for a in class_assignments if a.get('completed', False)]
            upcoming_assignments = [a for a in class_assignments if not a.get('completed', False)]
            
            # Predict final grade for this class
            predicted_grade = self._predict_class_grade(completed_assignments, upcoming_assignments)
            predicted_gpa = self._percentage_to_gpa(predicted_grade)
            
            predictions[class_info['name']] = {
                'predicted_percentage': predicted_grade,
                'predicted_gpa': predicted_gpa,
                'credits': credits,
                'confidence': self._calculate_confidence(completed_assignments, upcoming_assignments)
            }
            
            total_predicted_grade_points += predicted_gpa * credits
            total_credits += credits
        
        overall_predicted_gpa = total_predicted_grade_points / total_credits if total_credits > 0 else 0
        
        return {
            'overall_predicted_gpa': round(overall_predicted_gpa, 2),
            'class_predictions': predictions,
            'total_credits': total_credits,
            'prediction_date': datetime.now().isoformat()
        }
    
    def calculate_target_performance(self, target_gpa: float, classes: List[Dict], current_assignments: List[Dict]) -> Dict:
        """
        Calculate what performance is needed on remaining assignments to achieve target GPA
        """
        recommendations = {}
        
        for class_info in classes:
            class_id = class_info['id']
            credits = class_info['credits']
            
            class_assignments = [a for a in current_assignments if a.get('class_id') == class_id]
            completed_assignments = [a for a in class_assignments if a.get('completed', False)]
            upcoming_assignments = [a for a in class_assignments if not a.get('completed', False)]
            
            # Calculate current class average
            current_avg = self._calculate_current_average(completed_assignments)
            
            # Calculate needed performance on remaining assignments
            needed_performance = self._calculate_needed_performance(
                current_avg, 
                len(completed_assignments),
                len(upcoming_assignments),
                target_gpa
            )
            
            recommendations[class_info['name']] = {
                'current_average': current_avg,
                'needed_average_on_remaining': needed_performance,
                'remaining_assignments': len(upcoming_assignments),
                'feasibility': self._assess_feasibility(needed_performance),
                'recommendations': self._generate_recommendations(needed_performance, upcoming_assignments)
            }
        
        return recommendations
    
    def analyze_grade_trends(self, assignments: List[Dict]) -> Dict:
        """
        Analyze grade trends over time to predict future performance
        """
        if not assignments:
            return {'trend': 'insufficient_data'}
        
        # Sort assignments by date
        sorted_assignments = sorted(
            [a for a in assignments if a.get('completed') and a.get('points_earned') is not None],
            key=lambda x: x.get('created_at', datetime.now())
        )
        
        if len(sorted_assignments) < 3:
            return {'trend': 'insufficient_data'}
        
        # Calculate percentage scores
        percentages = []
        for assignment in sorted_assignments:
            if assignment.get('points_possible', 0) > 0:
                percentage = (assignment['points_earned'] / assignment['points_possible']) * 100
                percentages.append(percentage)
        
        if len(percentages) < 3:
            return {'trend': 'insufficient_data'}
        
        # Analyze trend
        recent_avg = statistics.mean(percentages[-3:])  # Last 3 assignments
        older_avg = statistics.mean(percentages[:-3])   # Earlier assignments
        
        if recent_avg > older_avg + 5:
            trend = 'improving'
        elif recent_avg < older_avg - 5:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'recent_average': round(recent_avg, 2),
            'overall_average': round(statistics.mean(percentages), 2),
            'improvement_rate': round(recent_avg - older_avg, 2),
            'consistency': round(statistics.stdev(percentages), 2)  # Lower is more consistent
        }
    
    def _predict_class_grade(self, completed: List[Dict], upcoming: List[Dict]) -> float:
        """Predict final grade for a class"""
        if not completed:
            return 85.0  # Default assumption
        
        # Calculate current average
        current_avg = self._calculate_current_average(completed)
        
        # If no upcoming assignments, return current average
        if not upcoming:
            return current_avg
        
        # Predict performance on upcoming assignments based on trend
        trend_factor = self._calculate_trend_factor(completed)
        predicted_upcoming_avg = max(0, min(100, current_avg + trend_factor))
        
        # Weight current and predicted performance
        completed_weight = len(completed)
        upcoming_weight = len(upcoming)
        total_weight = completed_weight + upcoming_weight
        
        predicted_final = (
            (current_avg * completed_weight) + 
            (predicted_upcoming_avg * upcoming_weight)
        ) / total_weight
        
        return predicted_final
    
    def _calculate_current_average(self, assignments: List[Dict]) -> float:
        """Calculate current average from completed assignments"""
        if not assignments:
            return 0.0
        
        total_points_earned = 0
        total_points_possible = 0
        
        for assignment in assignments:
            if (assignment.get('points_earned') is not None and 
                assignment.get('points_possible') is not None and
                assignment['points_possible'] > 0):
                
                total_points_earned += assignment['points_earned']
                total_points_possible += assignment['points_possible']
        
        if total_points_possible == 0:
            return 0.0
        
        return (total_points_earned / total_points_possible) * 100
    
    def _calculate_trend_factor(self, assignments: List[Dict]) -> float:
        """Calculate performance trend factor"""
        if len(assignments) < 2:
            return 0
        
        # Get last few assignment percentages
        recent_percentages = []
        for assignment in assignments[-3:]:  # Last 3 assignments
            if (assignment.get('points_earned') is not None and 
                assignment.get('points_possible') is not None and
                assignment['points_possible'] > 0):
                
                percentage = (assignment['points_earned'] / assignment['points_possible']) * 100
                recent_percentages.append(percentage)
        
        if len(recent_percentages) < 2:
            return 0
        
        # Simple linear trend
        return (recent_percentages[-1] - recent_percentages[0]) / len(recent_percentages)
    
    def _percentage_to_gpa(self, percentage: float) -> float:
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
    
    def _calculate_confidence(self, completed: List[Dict], upcoming: List[Dict]) -> float:
        """Calculate confidence level of prediction"""
        if not completed:
            return 0.1
        
        # Confidence based on number of completed assignments
        base_confidence = min(0.9, len(completed) / 10)
        
        # Reduce confidence if many assignments remaining
        remaining_factor = 1 - (len(upcoming) / (len(completed) + len(upcoming) + 1))
        
        return round(base_confidence * remaining_factor, 2)
    
    def _calculate_needed_performance(self, current_avg: float, completed_count: int, 
                                    upcoming_count: int, target_gpa: float) -> float:
        """Calculate needed performance on remaining assignments"""
        target_percentage = self._gpa_to_percentage(target_gpa)
        
        if upcoming_count == 0:
            return current_avg
        
        total_assignments = completed_count + upcoming_count
        needed_total_points = target_percentage * total_assignments
        current_total_points = current_avg * completed_count
        
        needed_on_remaining = (needed_total_points - current_total_points) / upcoming_count
        
        return max(0, min(100, needed_on_remaining))
    
    def _gpa_to_percentage(self, gpa: float) -> float:
        """Convert GPA to percentage (rough approximation)"""
        return max(0, min(100, (gpa / 4.0) * 100))
    
    def _assess_feasibility(self, needed_performance: float) -> str:
        """Assess feasibility of achieving needed performance"""
        if needed_performance <= 70:
            return 'very_achievable'
        elif needed_performance <= 85:
            return 'achievable'
        elif needed_performance <= 95:
            return 'challenging'
        else:
            return 'very_difficult'
    
    def _generate_recommendations(self, needed_performance: float, upcoming_assignments: List[Dict]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if needed_performance > 90:
            recommendations.append("Focus intensively on upcoming assignments")
            recommendations.append("Seek help from professors or tutors")
            recommendations.append("Form study groups for difficult topics")
        elif needed_performance > 80:
            recommendations.append("Maintain consistent study schedule")
            recommendations.append("Review assignment requirements carefully")
        else:
            recommendations.append("Continue current study habits")
            recommendations.append("Stay organized with assignment deadlines")
        
        return recommendations