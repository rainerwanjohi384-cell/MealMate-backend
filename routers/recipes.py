from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.auth import verify_token
import models.recipe as recipe_models
import schemas.recipe_schema as recipe_schemas

router = APIRouter()

@router.post("/recipes/", response_model=recipe_schemas.Recipe)
def create_recipe(recipe: recipe_schemas.RecipeCreate, current_user: int = Depends(verify_token), db: Session = Depends(get_db)):
    db_recipe = recipe_models.Recipe(**recipe.dict(), user_id=current_user)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.get("/recipes/", response_model=list[recipe_schemas.Recipe])
def read_recipes(current_user: int = Depends(verify_token), db: Session = Depends(get_db)):
    recipes = db.query(recipe_models.Recipe).filter(recipe_models.Recipe.user_id == current_user).all()
    return recipes

@router.get("/recipes/{recipe_id}", response_model=recipe_schemas.Recipe)
def read_recipe(recipe_id: int, current_user: int = Depends(verify_token), db: Session = Depends(get_db)):
    recipe = db.query(recipe_models.Recipe).filter(recipe_models.Recipe.recipe_id == recipe_id, recipe_models.Recipe.user_id == current_user).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@router.put("/recipes/{recipe_id}", response_model=recipe_schemas.Recipe)
def update_recipe(recipe_id: int, recipe: recipe_schemas.RecipeCreate, current_user: int = Depends(verify_token), db: Session = Depends(get_db)):
    db_recipe = db.query(recipe_models.Recipe).filter(recipe_models.Recipe.recipe_id == recipe_id, recipe_models.Recipe.user_id == current_user).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    for key, value in recipe.dict().items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, current_user: int = Depends(verify_token), db: Session = Depends(get_db)):
    db_recipe = db.query(recipe_models.Recipe).filter(recipe_models.Recipe.recipe_id == recipe_id, recipe_models.Recipe.user_id == current_user).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted"}
