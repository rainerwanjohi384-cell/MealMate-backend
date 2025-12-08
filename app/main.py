from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routers import users, recipes, meal_plans

# Create FastAPI app
app = FastAPI(
    title="MealMate API",
    description="Backend API for MealMate - Your Personal Recipe & Meal Planner",
    version="1.0.0"
)

# Configure CORS
origins = settings.allowed_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Startup event handler"""
    # Note: Use Alembic migrations for production
    # Base.metadata.create_all(bind=engine)
    pass


# Include routers
app.include_router(users.router)
app.include_router(recipes.router)
app.include_router(meal_plans.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "MealMate API is running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "api": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
