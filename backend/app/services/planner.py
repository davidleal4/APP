from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

class StudyPlanner:
    def __init__(self):
        pass
    
    def generate_study_schedule(self, assignments: List[Dict], preferences: Dict = None) -> Dict:
        """
        Generate an optimized study schedule based on assignments and user preferences
        """
        if not preferences:
            preferences = self._get_default_preferences()
        
        # Sort assignments by priority (due date, difficulty, points)
        prioritized_assignments = self._prioritize_assignments(assignments)
        
        # Generate daily schedule
        schedule = self._create_daily_schedule(prioritized_assignments, preferences)
        
        # Add buffer time and breaks
        schedule = self._add_buffer_time(schedule, preferences)
        
        return {
            'schedule': schedule,
            'summary': self._generate_schedule_summary(schedule),
            'recommendations': self._generate_study_recommendations(prioritized_assignments, preferences)
        }
    
    def optimize_assignment_order(self, assignments: List[Dict]) -> List[Dict]:
        """
        Optimize the order of assignments based on multiple factors
        """
        def assignment_score(assignment):
            # Multi-factor scoring for assignment priority
            score = 0
            
            # Due date urgency (higher score for sooner due dates)
            if assignment.get('due_date'):
                due_date = datetime.fromisoformat(assignment['due_date'].replace('Z', '+00:00'))
                days_until_due = (due_date - datetime.now()).days
                if days_until_due <= 1:
                    score += 100
                elif days_until_due <= 3:
                    score += 50
                elif days_until_due <= 7:
                    score += 25
            
            # Point value (higher points = higher priority)
            points = assignment.get('points_possible', 0)
            score += min(points / 10, 25)  # Cap at 25 points
            
            # Assignment type weighting
            assignment_type = assignment.get('assignment_type', '').lower()
            type_weights = {
                'exam': 30,
                'final': 40,
                'midterm': 35,
                'project': 25,
                'homework': 10,
                'quiz': 15
            }
            score += type_weights.get(assignment_type, 10)
            
            # Difficulty factor (if available)
            difficulty = assignment.get('difficulty', 'medium')
            difficulty_weights = {'easy': 5, 'medium': 10, 'hard': 20}
            score += difficulty_weights.get(difficulty, 10)
            
            return score
        
        return sorted(assignments, key=assignment_score, reverse=True)
    
    def suggest_break_intervals(self, study_duration_hours: float) -> List[Dict]:
        """
        Suggest optimal break intervals using research-based techniques
        """
        breaks = []
        
        if study_duration_hours <= 1:
            # Short study session - one break in middle
            breaks.append({
                'time': study_duration_hours / 2,
                'duration_minutes': 5,
                'type': 'micro_break'
            })
        elif study_duration_hours <= 2:
            # Pomodoro-style breaks
            for i in range(int(study_duration_hours * 2)):  # Every 30 minutes
                breaks.append({
                    'time': (i + 1) * 0.5,
                    'duration_minutes': 5 if i % 2 == 0 else 15,
                    'type': 'pomodoro_break'
                })
        else:
            # Longer study session - mix of short and long breaks
            current_time = 0
            while current_time < study_duration_hours:
                if current_time % 2 == 0:  # Every 2 hours, longer break
                    breaks.append({
                        'time': current_time + 1,
                        'duration_minutes': 15,
                        'type': 'long_break'
                    })
                else:  # Otherwise, short break every hour
                    breaks.append({
                        'time': current_time + 0.5,
                        'duration_minutes': 5,
                        'type': 'short_break'
                    })
                current_time += 1
        
        return breaks
    
    def create_revision_schedule(self, topics: List[str], exam_date: datetime, 
                               difficulty_levels: Dict[str, str] = None) -> Dict:
        """
        Create a spaced repetition schedule for exam revision
        """
        if not difficulty_levels:
            difficulty_levels = {topic: 'medium' for topic in topics}
        
        revision_schedule = {}
        current_date = datetime.now()
        days_until_exam = (exam_date - current_date).days
        
        # Spaced repetition intervals (days)
        intervals = [1, 3, 7, 14, 30]  # Based on forgetting curve research
        
        for topic in topics:
            difficulty = difficulty_levels.get(topic, 'medium')
            
            # Adjust intervals based on difficulty
            if difficulty == 'hard':
                topic_intervals = [1, 2, 5, 10, 20]  # More frequent review
            elif difficulty == 'easy':
                topic_intervals = [2, 5, 10, 21, 42]  # Less frequent review
            else:
                topic_intervals = intervals
            
            # Schedule revision sessions
            revision_dates = []
            for interval in topic_intervals:
                revision_date = current_date + timedelta(days=interval)
                if revision_date < exam_date:
                    revision_dates.append(revision_date.isoformat())
            
            # Add final review 1-2 days before exam
            final_review = exam_date - timedelta(days=1 if difficulty == 'hard' else 2)
            if final_review > current_date:
                revision_dates.append(final_review.isoformat())
            
            revision_schedule[topic] = {
                'revision_dates': revision_dates,
                'difficulty': difficulty,
                'total_sessions': len(revision_dates)
            }
        
        return revision_schedule
    
    def _prioritize_assignments(self, assignments: List[Dict]) -> List[Dict]:
        """Prioritize assignments based on multiple factors"""
        return self.optimize_assignment_order(assignments)
    
    def _create_daily_schedule(self, assignments: List[Dict], preferences: Dict) -> Dict:
        """Create day-by-day study schedule"""
        schedule = {}
        daily_study_hours = preferences.get('daily_study_hours', 4)
        preferred_times = preferences.get('preferred_study_times', ['morning', 'afternoon'])
        
        current_date = datetime.now()
        
        for i, assignment in enumerate(assignments):
            # Determine study date (spread assignments over available days)
            study_date = current_date + timedelta(days=i % 7)  # Cycle through week
            date_str = study_date.strftime('%Y-%m-%d')
            
            if date_str not in schedule:
                schedule[date_str] = {
                    'total_hours': 0,
                    'sessions': []
                }
            
            # Estimate study time needed
            estimated_hours = self._estimate_study_time(assignment)
            
            # Add to schedule if within daily limit
            if schedule[date_str]['total_hours'] + estimated_hours <= daily_study_hours:
                session = {
                    'assignment_id': assignment.get('id'),
                    'assignment_title': assignment.get('title', 'Untitled'),
                    'estimated_hours': estimated_hours,
                    'preferred_time': preferred_times[0] if preferred_times else 'morning',
                    'priority': assignment.get('priority', 'medium')
                }
                
                schedule[date_str]['sessions'].append(session)
                schedule[date_str]['total_hours'] += estimated_hours
        
        return schedule
    
    def _estimate_study_time(self, assignment: Dict) -> float:
        """Estimate study time needed for assignment"""
        base_hours = 2.0  # Default
        
        assignment_type = assignment.get('assignment_type', '').lower()
        type_hours = {
            'exam': 4.0,
            'final': 6.0,
            'midterm': 3.0,
            'project': 5.0,
            'homework': 1.5,
            'quiz': 1.0,
            'essay': 3.0
        }
        
        estimated = type_hours.get(assignment_type, base_hours)
        
        # Adjust for difficulty
        difficulty = assignment.get('difficulty', 'medium')
        if difficulty == 'hard':
            estimated *= 1.5
        elif difficulty == 'easy':
            estimated *= 0.7
        
        return round(estimated, 1)
    
    def _add_buffer_time(self, schedule: Dict, preferences: Dict) -> Dict:
        """Add buffer time and breaks to schedule"""
        buffer_percentage = preferences.get('buffer_percentage', 0.2)
        
        for date, day_schedule in schedule.items():
            # Add buffer time to each session
            for session in day_schedule['sessions']:
                original_hours = session['estimated_hours']
                buffer_hours = original_hours * buffer_percentage
                session['estimated_hours'] = round(original_hours + buffer_hours, 1)
                session['buffer_time'] = round(buffer_hours, 1)
            
            # Recalculate total hours
            day_schedule['total_hours'] = sum(s['estimated_hours'] for s in day_schedule['sessions'])
            
            # Add break suggestions
            total_hours = day_schedule['total_hours']
            day_schedule['breaks'] = self.suggest_break_intervals(total_hours)
        
        return schedule
    
    def _generate_schedule_summary(self, schedule: Dict) -> Dict:
        """Generate summary statistics for the schedule"""
        total_hours = sum(day['total_hours'] for day in schedule.values())
        total_sessions = sum(len(day['sessions']) for day in schedule.values())
        average_daily_hours = total_hours / len(schedule) if schedule else 0
        
        return {
            'total_study_hours': round(total_hours, 1),
            'total_sessions': total_sessions,
            'average_daily_hours': round(average_daily_hours, 1),
            'number_of_days': len(schedule)
        }
    
    def _generate_study_recommendations(self, assignments: List[Dict], preferences: Dict) -> List[str]:
        """Generate personalized study recommendations"""
        recommendations = []
        
        # Based on assignment load
        total_assignments = len(assignments)
        if total_assignments > 10:
            recommendations.append("Heavy assignment load detected. Consider breaking large tasks into smaller chunks.")
        
        # Based on due dates
        urgent_assignments = [a for a in assignments if self._is_urgent(a)]
        if urgent_assignments:
            recommendations.append(f"{len(urgent_assignments)} assignments due soon. Prioritize these immediately.")
        
        # Based on preferences
        daily_hours = preferences.get('daily_study_hours', 4)
        if daily_hours > 6:
            recommendations.append("Long study sessions planned. Remember to take regular breaks to maintain productivity.")
        
        recommendations.append("Use active recall techniques like flashcards for better retention.")
        recommendations.append("Review difficult topics multiple times using spaced repetition.")
        
        return recommendations
    
    def _is_urgent(self, assignment: Dict) -> bool:
        """Check if assignment is urgent (due within 3 days)"""
        if not assignment.get('due_date'):
            return False
        
        due_date = datetime.fromisoformat(assignment['due_date'].replace('Z', '+00:00'))
        return (due_date - datetime.now()).days <= 3
    
    def _get_default_preferences(self) -> Dict:
        """Get default study preferences"""
        return {
            'daily_study_hours': 4,
            'preferred_study_times': ['morning', 'afternoon'],
            'buffer_percentage': 0.2,
            'break_frequency': 'pomodoro',  # pomodoro, hourly, custom
            'difficulty_weighting': True
        }