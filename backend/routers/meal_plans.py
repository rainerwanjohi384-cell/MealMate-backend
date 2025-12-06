from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_token
import models.meal_plan as meal_plan_models
import schemas.meal_plan_schema as meal_plan_schemas

router = APIRouter(
    prefix="/meal-plans",
    tags=["meal-plans"]
)

@router.post("/", response_model=meal_plan_schemas.MealPlan)
def create_meal_plan(meal_plan: meal_plan_schemas.MealPlanCreate, db: Session = Depends(get_db), current_user: int = Depends(verify_token)):
    db_meal_plan = meal_plan_models.MealPlan(**meal_plan.dict(), user_id=current_user)
    db.add(db_meal_plan)
    db.commit()
    db.refresh(db_meal_plan)
    return db_meal_plan

@router.get("/", response_model=list[meal_plan_schemas.MealPlan])
def read_meal_plans(db: Session = Depends(get_db), current_user: int = Depends(verify_token)):
    meal_plans = db.query(meal_plan_models.MealPlan).filter(meal_plan_models.MealPlan.user_id == current_user).all()
    return meal_plans

@router.get("/{plan_id}", response_model=meal_plan_schemas.MealPlan)
def read_meal_plan(plan_id: int, db: Session = Depends(get_db), current_user: int = Depends(verify_token)):
    meal_plan = db.query(meal_plan_models.MealPlan).filter(
        meal_plan_models.MealPlan.plan_id == plan_id,
        meal_plan_models.MealPlan.user_id == current_user
    ).first()
    if meal_plan is None:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    return meal_plan

@router.put("/{plan_id}", response_model=meal_plan_schemas.MealPlan)
def update_meal_plan(plan_id: int, meal_plan: meal_plan_schemas.MealPlanCreate, db: Session = Depends(get_db), current_user: int = Depends(verify_token)):
    db_meal_plan = db.query(meal_plan_models.MealPlan).filter(
        meal_plan_models.MealPlan.plan_id == plan_id,
        meal_plan_models.MealPlan.user_id == current_user
    ).first()
    if db_meal_plan is None:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    for key, value in meal_plan.dict().items():
        setattr(db_meal_plan, key, value)
    db.commit()
    db.refresh(db_meal_plan)
    return db_meal_plan

@router.delete("/{plan_id}")
def delete_meal_plan(plan_id: int, db: Session = Depends(get_db), current_user: int = Depends(verify_token)):
    db_meal_plan = db.query(meal_plan_models.MealPlan).filter(
        meal_plan_models.MealPlan.plan_id == plan_id,
        meal_plan_models.MealPlan.user_id == current_user
    ).first()
    if db_meal_plan is None:
        raise HTTPException(status_code=404, detail="Meal plan not found")
    db.delete(db_meal_plan)
    db.commit()
    return {"message": "Meal plan deleted"}

