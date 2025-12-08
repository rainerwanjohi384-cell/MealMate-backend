#!/bin/bash
# Script to run the FastAPI application

echo "Starting MealMate Backend Server"
echo "================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Using default configuration."
    echo "   Copy .env.example to .env and configure it."
fi

# Run the application with uvicorn
echo "Starting server on http://0.0.0.0:8000"
echo "API documentation available at http://0.0.0.0:8000/docs"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
