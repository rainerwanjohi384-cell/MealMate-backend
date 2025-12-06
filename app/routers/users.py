from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.auth import create_access_token, get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with Firebase UID"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.firebase_uid == user_data.firebase_uid) | (User.email == user_data.email)
    ).first()
    
    if existing_user:
        # User exists, return token
        access_token = create_access_token(
            data={"user_id": existing_user.id, "firebase_uid": existing_user.firebase_uid}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    # Create new user
    new_user = User(
        firebase_uid=user_data.firebase_uid,
        email=user_data.email,
        name=user_data.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(
        data={"user_id": new_user.id, "firebase_uid": new_user.firebase_uid}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Delete current user account"""
    db.delete(current_user)
    db.commit()
    return None
