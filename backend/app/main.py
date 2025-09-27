from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db, engine
from app.api.v1.api import api_router
from app.models import models
# from app.core.scheduler import scheduler

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StudyOS API",
    description="AI-powered study assistant for college students",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Start scheduler for reminders (disabled for now)
# @app.on_event("startup")
# async def startup_event():
#     scheduler.start()

# @app.on_event("shutdown")
# async def shutdown_event():
#     scheduler.shutdown()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "StudyOS API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)