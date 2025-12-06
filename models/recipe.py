from sqlalchemy import Column, Integer, String, Text, ForeignKey
from backend.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String)
    description = Column(Text)
    ingredients = Column(Text)
    instructions = Column(Text)
