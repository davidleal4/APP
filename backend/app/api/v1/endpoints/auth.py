from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.auth import authenticate_user, create_access_token, get_password_hash, verify_token
from app.core.email import send_magic_link_email
from app.models.models import User
from app.schemas.schemas import UserCreate, UserLogin, Token, MagicLinkRequest, User as UserSchema
from app.core.config import settings
import secrets

router = APIRouter()

@router.post("/register", response_model=UserSchema)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password) if user_data.password else None,
        plan="free",
        first_login=True
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password"""
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/magic")
def request_magic_link(request: MagicLinkRequest, db: Session = Depends(get_db)):
    """Request a magic link for passwordless login"""
    # Check if user exists, create if not
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        user = User(
            email=request.email,
            plan="free",
            first_login=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Generate magic token
    magic_token = create_access_token(
        data={"user_id": user.id, "type": "magic_link"},
        expires_delta=timedelta(minutes=15)
    )
    
    # Send magic link email
    if not send_magic_link_email(request.email, magic_token):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send magic link email"
        )
    
    return {"message": "Magic link sent to your email"}

@router.post("/magic/verify", response_model=Token)
def verify_magic_link(token: str, db: Session = Depends(get_db)):
    """Verify magic link token and log in user"""
    try:
        user_id = verify_token(token)
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid magic link"
            )
        
        # Create new access token for regular authentication
        access_token_expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired magic link"
        )