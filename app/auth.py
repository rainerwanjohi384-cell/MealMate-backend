from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import TokenData

security = HTTPBearer()

# Optional: Firebase Admin SDK integration
# Uncomment these lines if you want to verify Firebase tokens directly
# import firebase_admin
# from firebase_admin import auth as firebase_auth, credentials
# 
# if not firebase_admin._apps:
#     cred = credentials.Certificate("path/to/serviceAccountKey.json")
#     firebase_admin.initialize_app(cred)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify and decode JWT token (our own or Firebase)"""
    try:
        # First try to decode as our JWT
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("user_id")
        firebase_uid: str = payload.get("firebase_uid")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        
        return TokenData(user_id=user_id, firebase_uid=firebase_uid)
    except JWTError:
        # Optional: Try Firebase token verification
        # Uncomment if using Firebase Admin SDK
        # try:
        #     decoded_token = firebase_auth.verify_id_token(token)
        #     firebase_uid = decoded_token['uid']
        #     return TokenData(firebase_uid=firebase_uid)
        # except Exception:
        #     pass
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    token = credentials.credentials
    token_data = verify_token(token)
    
    # Try to find user by ID first (our JWT)
    if token_data.user_id:
        user = db.query(User).filter(User.id == token_data.user_id).first()
    # Fallback to Firebase UID (if Firebase token was verified)
    elif token_data.firebase_uid:
        user = db.query(User).filter(User.firebase_uid == token_data.firebase_uid).first()
    else:
        user = None
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user
