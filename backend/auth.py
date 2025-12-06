from fastapi import HTTPException, Header, Depends
from sqlalchemy.orm import Session
from database import get_db
import models.user as user_models

# Temporary mock authentication for testing
def verify_token(authorization: str = Header(None), db: Session = Depends(get_db)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="No token provided")

    # For testing, accept any token and return a mock user ID
    # In production, replace with proper Firebase authentication
    try:
        # Mock user creation/retrieval
        mock_uid = "test-user-uid"
        db_user = db.query(user_models.User).filter(user_models.User.firebase_uid == mock_uid).first()
        if not db_user:
            db_user = user_models.User(
                firebase_uid=mock_uid,
                name="Test User",
                email="test@example.com"
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        return db_user.user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")

