from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.auth import verify_token
import models.user as user_models
import schemas.user_schema as user_schemas

router = APIRouter()

@router.post("/users/", response_model=user_schemas.User)
def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = user_models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me", response_model=user_schemas.User)
def read_user(current_user: int = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(user_models.User.user_id == current_user).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
