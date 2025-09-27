from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from app.core.database import engine
from app.models.models import User, Assignment, Flashcard
from app.core.email import send_reminder_email

scheduler = AsyncIOScheduler()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def send_daily_reminders():
    """Send daily study reminders"""
    db = SessionLocal()
    try:
        # Get users with upcoming assignments (within 3 days)
        upcoming_date = datetime.now() + timedelta(days=3)
        
        users_with_assignments = db.query(User).join(User.classes).join(Assignment).filter(
            Assignment.due_date <= upcoming_date,
            Assignment.due_date >= datetime.now()
        ).distinct().all()
        
        for user in users_with_assignments:
            assignments = []
            for class_ in user.classes:
                class_assignments = [a for a in class_.assignments 
                                   if a.due_date and a.due_date <= upcoming_date and a.due_date >= datetime.now()]
                assignments.extend(class_assignments)
            
            if assignments:
                content = "<ul>"
                for assignment in assignments:
                    days_left = (assignment.due_date - datetime.now()).days
                    content += f"<li><strong>{assignment.title}</strong> - Due in {days_left} day{'s' if days_left != 1 else ''}</li>"
                content += "</ul>"
                
                send_reminder_email(
                    user.email,
                    "📚 Daily Study Reminder",
                    f"You have {len(assignments)} upcoming assignment{'s' if len(assignments) != 1 else ''}: {content}"
                )
        
        # Send flashcard reminders
        users_with_flashcards = db.query(User).join(User.classes).join(Flashcard).filter(
            Flashcard.due_at <= datetime.now()
        ).distinct().all()
        
        for user in users_with_flashcards:
            due_flashcards = []
            for class_ in user.classes:
                class_flashcards = [f for f in class_.flashcards 
                                  if f.due_at and f.due_at <= datetime.now()]
                due_flashcards.extend(class_flashcards)
            
            if due_flashcards:
                send_reminder_email(
                    user.email,
                    "🎯 Flashcard Review Time",
                    f"You have {len(due_flashcards)} flashcard{'s' if len(due_flashcards) != 1 else ''} ready for review!"
                )
    
    finally:
        db.close()

def send_weekly_reminders():
    """Send weekly study summary"""
    db = SessionLocal()
    try:
        # Get all users for weekly summary
        users = db.query(User).all()
        
        for user in users:
            # Calculate weekly stats
            classes_count = len(user.classes)
            total_assignments = sum(len(class_.assignments) for class_ in user.classes)
            completed_assignments = sum(1 for class_ in user.classes 
                                      for assignment in class_.assignments 
                                      if assignment.grade is not None)
            
            if classes_count > 0:
                completion_rate = (completed_assignments / total_assignments * 100) if total_assignments > 0 else 0
                
                send_reminder_email(
                    user.email,
                    "📊 Weekly Study Summary",
                    f"""
                    <h3>Your Week in Review</h3>
                    <p><strong>Classes:</strong> {classes_count}</p>
                    <p><strong>Assignments Completed:</strong> {completed_assignments}/{total_assignments} ({completion_rate:.1f}%)</p>
                    <p>Keep up the great work! Remember to review your flashcards and stay on top of upcoming deadlines.</p>
                    """
                )
    
    finally:
        db.close()

# Schedule daily reminders at 9 AM
scheduler.add_job(
    send_daily_reminders,
    CronTrigger(hour=9, minute=0),
    id="daily_reminders"
)

# Schedule weekly reminders on Sunday at 6 PM
scheduler.add_job(
    send_weekly_reminders,
    CronTrigger(day_of_week=6, hour=18, minute=0),
    id="weekly_reminders"
)