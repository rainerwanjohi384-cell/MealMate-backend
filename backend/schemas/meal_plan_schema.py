from pydantic import BaseModel

class MealPlanBase(BaseModel):
    day_of_week: str
    recipe_id: int

class MealPlanCreate(MealPlanBase):
    pass

class MealPlan(MealPlanBase):
    plan_id: int
    user_id: int

    class Config:
        from_attributes = True
