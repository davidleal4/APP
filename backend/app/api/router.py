from fastapi import APIRouter
from app.api.v1 import auth, classes, assignments, flashcards, gpa

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])  
api_router.include_router(assignments.router, prefix="/assignments", tags=["assignments"])
api_router.include_router(flashcards.router, prefix="/flashcards", tags=["flashcards"])
api_router.include_router(gpa.router, prefix="/gpa", tags=["gpa"])