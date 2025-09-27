import resend
from app.core.config import settings
from typing import Optional

# Initialize Resend
if settings.EMAIL_API_KEY:
    resend.api_key = settings.EMAIL_API_KEY

def send_magic_link_email(email: str, magic_token: str) -> bool:
    """Send magic link email for authentication"""
    try:
        magic_link = f"http://localhost:3000/auth/magic?token={magic_token}"
        
        params = {
            "from": "StudyOS <noreply@studyos.app>",
            "to": [email],
            "subject": "Your StudyOS Magic Link",
            "html": f"""
            <h2>Welcome to StudyOS!</h2>
            <p>Click the link below to sign in to your account:</p>
            <a href="{magic_link}" style="background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;">
                Sign In to StudyOS
            </a>
            <p>This link will expire in 15 minutes.</p>
            <p>If you didn't request this, please ignore this email.</p>
            """
        }
        
        if settings.EMAIL_API_KEY:
            email_response = resend.Emails.send(params)
            return email_response.get("id") is not None
        else:
            print(f"Magic link email would be sent to {email}: {magic_link}")
            return True
            
    except Exception as e:
        print(f"Failed to send magic link email: {e}")
        return False

def send_reminder_email(email: str, subject: str, content: str) -> bool:
    """Send reminder email"""
    try:
        params = {
            "from": "StudyOS <reminders@studyos.app>",
            "to": [email],
            "subject": subject,
            "html": f"""
            <h2>Study Reminder</h2>
            <div>{content}</div>
            <p>Keep up the great work!</p>
            <p>- Your StudyOS Team</p>
            """
        }
        
        if settings.EMAIL_API_KEY:
            email_response = resend.Emails.send(params)
            return email_response.get("id") is not None
        else:
            print(f"Reminder email would be sent to {email}: {subject}")
            return True
            
    except Exception as e:
        print(f"Failed to send reminder email: {e}")
        return False