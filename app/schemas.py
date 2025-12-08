from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    firebase_uid: str


class UserResponse(UserBase):
    id: int
    firebase_uid: str
    created_at: datetime
    
    model_config = {"from_attributes": True}


# Recipe Schemas
class RecipeBase(BaseModel):
    title: str
    ingredients: str
    instructions: str
    category: Optional[str] = None
    prep_time: Optional[int] = None
    image_url: Optional[str] = None


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: Optional[str] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None
    category: Optional[str] = None
    prep_time: Optional[int] = None
    image_url: Optional[str] = None


class RecipeResponse(RecipeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


# Meal Plan Schemas
class MealPlanBase(BaseModel):
    recipe_id: int
    day_of_week: str
    meal_type: Optional[str] = None
    week_start: Optional[str] = None


class MealPlanCreate(MealPlanBase):
    pass


class MealPlanUpdate(BaseModel):
    recipe_id: Optional[int] = None
    day_of_week: Optional[str] = None
    meal_type: Optional[str] = None
    week_start: Optional[str] = None


class MealPlanResponse(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    day_of_week: str
    meal_type: Optional[str] = None
    week_start: Optional[str] = None
    recipe: Optional[RecipeResponse] = None
    
    model_config = {"from_attributes": True}


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None
    firebase_uid: Optional[str] = None
