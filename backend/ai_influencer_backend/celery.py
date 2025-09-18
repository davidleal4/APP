import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_influencer_backend.settings')

app = Celery('ai_influencer_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    'reset-monthly-credits': {
        'task': 'users.tasks.reset_monthly_credits',
        'schedule': 86400.0,  # Run daily to check for resets
    },
    'cleanup-expired-generations': {
        'task': 'ai_generation.tasks.cleanup_expired_generations',
        'schedule': 3600.0,  # Run hourly
    },
    'update-system-metrics': {
        'task': 'admin_panel.tasks.update_system_metrics',
        'schedule': 300.0,  # Run every 5 minutes
    },
    'check-gpu-health': {
        'task': 'ai_generation.tasks.check_gpu_health',
        'schedule': 60.0,  # Run every minute
    },
}

app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')