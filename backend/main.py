# setting up FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing the routers
from routers import recipes, meal_plans, users
from backend.database import Base, engine

# This creates the tables
Base.metadata.create_all(bind=engine)

# Making the app
app = FastAPI()

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adding the routers
app.include_router(recipes.router)
app.include_router(meal_plans.router)
app.include_router(users.router)

# Home endpoint
@app.get("/")
def home():
    return {"message": "MealMate Backend Running"}
