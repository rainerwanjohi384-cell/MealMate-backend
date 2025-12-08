from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.database import get_db
from app.models import MealPlan, Recipe, User
from app.schemas import MealPlanCreate, MealPlanUpdate, MealPlanResponse
from app.auth import get_current_user

router = APIRouter(tags=["meal-plans"])


# Frontend expects /api/plan-entries for creating meal plans
@router.post("/api/plan-entries", response_model=MealPlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan_entry(
    meal_plan_data: MealPlanCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new meal plan entry (frontend compatible endpoint)"""
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
        week_start=meal_plan_data.week_start
    )
    
    db.add(new_meal_plan)
    db.commit()
    db.refresh(new_meal_plan)
    
    # Load the recipe relationship
    db.refresh(new_meal_plan, ['recipe'])
    
    return new_meal_plan


# Frontend expects /api/plans/week/{date} for getting weekly meal plans
@router.get("/api/plans/week/{week_start_date}")
def get_week_plan(
    week_start_date: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get meal plans for a specific week (frontend compatible endpoint)"""
    # Query all meal plans for this user and week
    meal_plans = db.query(MealPlan).options(joinedload(MealPlan.recipe)).filter(
        MealPlan.user_id == current_user.id,
        MealPlan.week_start == week_start_date
    ).all()
    
    # Format response to match frontend expectations
    entries = []
    for plan in meal_plans:
        entries.append({
            "id": plan.id,
            "day_of_week": plan.day_of_week,
            "meal_type": plan.meal_type,
            "recipe_id": plan.recipe_id,
            "recipe": {
                "id": plan.recipe.id,
                "title": plan.recipe.title,
                "prep_time": plan.recipe.prep_time,
                "category": plan.recipe.category,
                "image_url": plan.recipe.image_url,
            } if plan.recipe else None
        })
    
    return {"entries": entries}


@router.get("/api/meal-plans/", response_model=List[MealPlanResponse])
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


@router.get("/api/meal-plans/{plan_id}", response_model=MealPlanResponse)
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


@router.put("/api/meal-plans/{plan_id}", response_model=MealPlanResponse)
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
    update_data = meal_plan_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(meal_plan, field, value)
    
    db.commit()
    db.refresh(meal_plan)
    db.refresh(meal_plan, ['recipe'])
    
    return meal_plan


@router.delete("/api/meal-plans/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
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
