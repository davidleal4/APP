from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio
import logging
from app.core.db import get_db, Base, engine
from app.core.config import settings
from app import models
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Student Productivity App API"}

@app.get("/health")
def health_check():
    return {"ok": True}


# --- Startup / Scheduler ---
scheduler: AsyncIOScheduler | None = None

async def send_reminder_emails(db: Session):
    # Stubbed Resend integration
    try:
        # Query upcoming assignments within next 7 days
        upcoming = db.query(models.Assignment).filter(
            models.Assignment.completed == False
        ).all()
        # Here you would group by user and send via Resend
        logging.info(f"Reminder job ran: {len(upcoming)} upcoming assignments found")
    except Exception as exc:
        logging.exception(f"Reminder job failed: {exc}")

@app.on_event("startup")
async def on_startup():
    # Ensure tables exist (keeps local/dev simple; use Alembic in prod)
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        logging.exception(f"DB init failed: {exc}")

    global scheduler
    scheduler = AsyncIOScheduler()
    # Morning daily reminders at 08:00 UTC
    scheduler.add_job(lambda: _run_job(send_reminder_emails), CronTrigger(hour=8, minute=0))
    # Weekly digest Sunday 09:00 UTC
    scheduler.add_job(lambda: _run_job(send_reminder_emails), CronTrigger(day_of_week="sun", hour=9, minute=0))
    scheduler.start()

async def _run_job(job_coro):
    # Acquire DB session per job run
    db_gen = get_db()
    db = next(db_gen)
    try:
        await job_coro(db)
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass