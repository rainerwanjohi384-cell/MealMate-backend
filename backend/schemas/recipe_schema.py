from pydantic import BaseModel

class RecipeBase(BaseModel):
    name: str
    ingredients: str
    instructions: str
    category: str | None = None

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    recipe_id: int
    user_id: int

    class Config:
        from_attributes = True