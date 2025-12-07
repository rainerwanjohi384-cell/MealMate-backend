from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    title = Column(String, nullable=False)
    ingredients = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)

    category = Column(String, nullable=True)
    prep_time = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)

