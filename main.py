from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import recipes, meal_plans, users
from backend import auth
from backend.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MealMate API",
    description="API for MealMate - Personal Recipe & Meal Planner",
    version="1.0.0"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(meal_plans.router)

@app.get("/")
def home():
    return {"message": "MealMate Backend Running"}
