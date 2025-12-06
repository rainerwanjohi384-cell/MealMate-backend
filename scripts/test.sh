#!/bin/bash
# Script to run tests

echo "🧪 Running MealMate Backend Tests"
echo "================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run pytest with coverage
echo "Running tests with coverage..."
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html

# Check test results
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo "📊 Coverage report generated in htmlcov/index.html"
else
    echo ""
    echo "❌ Some tests failed. Please check the output above."
    exit 1
fi
