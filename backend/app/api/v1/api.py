from fastapi import APIRouter
from app.api.v1.endpoints import auth, classes

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])