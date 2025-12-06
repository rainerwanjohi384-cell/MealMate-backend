#!/bin/bash
# Script to deploy backend (production)

echo "🚀 Deploying MealMate Backend"
echo "============================="

# Stop on errors
set -e

# Pull latest changes
echo "📥 Pulling latest changes from git..."
git pull origin main

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations (if using alembic)
# echo "🗄️  Running database migrations..."
# alembic upgrade head

# Run tests
echo "🧪 Running tests..."
./scripts/test.sh

# Restart the application
echo "🔄 Restarting application..."
# This will depend on your deployment method (systemd, docker, etc.)
# Example for systemd:
# sudo systemctl restart mealmate-backend

echo ""
echo "✅ Deployment complete!"
echo "🌐 Backend is running"
