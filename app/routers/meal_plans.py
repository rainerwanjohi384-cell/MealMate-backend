from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models import MealPlan, Recipe, User
from app.schemas import MealPlanCreate, MealPlanUpdate, MealPlanResponse
from app.auth import get_current_user

router = APIRouter(prefix="/api/meal-plans", tags=["meal-plans"])


@router.get("/", response_model=List[MealPlanResponse])
def get_meal_plans(
    skip: int = 0,
    limit: int = 100,
    day_of_week: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all meal plans for the current user"""
    query = db.query(MealPlan).options(joinedload(MealPlan.recipe)).filter(
        MealPlan.user_id == current_user.id
    )
    
    if day_of_week:
        query = query.filter(MealPlan.day_of_week == day_of_week)
    
    meal_plans = query.offset(skip).limit(limit).all()
    return meal_plans


@router.get("/{plan_id}", response_model=MealPlanResponse)
def get_meal_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific meal plan by ID"""
    meal_plan = db.query(MealPlan).options(joinedload(MealPlan.recipe)).filter(
        MealPlan.id == plan_id,
        MealPlan.user_id == current_user.id
    ).first()
    
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )
    
    return meal_plan


@router.post("/", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
def create_meal_plan(
    meal_plan_data: MealPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new meal plan"""
    # Verify recipe exists and belongs to user
    recipe = db.query(Recipe).filter(
        Recipe.id == meal_plan_data.recipe_id,
        Recipe.user_id == current_user.id
    ).first()
    
    if not recipe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    
    new_meal_plan = MealPlan(
        user_id=current_user.id,
        recipe_id=meal_plan_data.recipe_id,
        day_of_week=meal_plan_data.day_of_week,
        meal_type=meal_plan_data.meal_type,
        planned_date=meal_plan_data.planned_date
    )
    
    db.add(new_meal_plan)
    db.commit()
    db.refresh(new_meal_plan)
    
    # Load the recipe relationship
    db.refresh(new_meal_plan, ['recipe'])
    
    return new_meal_plan


@router.put("/{plan_id}", response_model=MealPlanResponse)
def update_meal_plan(
    plan_id: int,
    meal_plan_data: MealPlanUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update an existing meal plan"""
    meal_plan = db.query(MealPlan).filter(
        MealPlan.id == plan_id,
        MealPlan.user_id == current_user.id
    ).first()
    
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )
    
    # Update fields if provided
    update_data = meal_plan_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(meal_plan, field, value)
    
    db.commit()
    db.refresh(meal_plan)
    db.refresh(meal_plan, ['recipe'])
    
    return meal_plan


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal_plan(
    plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a meal plan"""
    meal_plan = db.query(MealPlan).filter(
        MealPlan.id == plan_id,
        MealPlan.user_id == current_user.id
    ).first()
    
    if not meal_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal plan not found"
        )
    
    db.delete(meal_plan)
    db.commit()
    
    return None
