from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    firebase_uid: str

class User(UserBase):
    user_id: int
    firebase_uid: str

    class Config:
        from_attributes = True
