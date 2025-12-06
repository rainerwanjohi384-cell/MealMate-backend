from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class MealPlan(Base):
    __tablename__ = "meal_plans"

    plan_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    day_of_week = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))

