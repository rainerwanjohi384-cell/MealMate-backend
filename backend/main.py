# setting up FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing the routers
from routers import recipes, meal_plans, users
from database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()

# CORS SETTINGS (FULL FIX)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",

    # Your deployed frontend URLs:
    "https://dailydish-frontend.firebaseapp.com",
    "https://dailydish-frontend.web.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(recipes.router)
app.include_router(meal_plans.router)
app.include_router(users.router)

# Home endpoint
@app.get("/")
def home():
    return {"message": "MealMate Backend Running"}

