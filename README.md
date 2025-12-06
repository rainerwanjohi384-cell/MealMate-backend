# MealMate Backend API

[![CI/CD](https://github.com/rainerwanjohi384-cell/MealMate-backend/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/rainerwanjohi384-cell/MealMate-backend/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Backend API for the MealMate recipe and meal planning application. This is a FastAPI project with JWT authentication, testing, and Docker support.

> Note: This is part of a group project where I'm handling the DevOps, testing, and deployment setup.

## Features

- User authentication with Firebase and JWT tokens
- Recipe management (create, read, update, delete)
- Weekly meal planning
- Token-based authorization
- RESTful API endpoints
- Pytest test suite
- Docker support
- GitHub Actions CI/CD

## Table of Contents

- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)

## Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Database | SQLite (dev) / PostgreSQL (prod) |
| ORM | SQLAlchemy |
| Authentication | Firebase + JWT |
| Testing | Pytest |
| Containerization | Docker + docker-compose |
| CI/CD | GitHub Actions |
| API Docs | Swagger/OpenAPI (auto-generated) |

## Quick Start

### Using Docker

```bash
# Clone the repository
git clone https://github.com/rainerwanjohi384-cell/MealMate-backend.git
cd MealMate-backend

# Start with docker-compose
docker-compose up -d

# Access the API
open http://localhost:8000/docs
```

### Using Scripts

```bash
# Setup environment
./scripts/setup.sh

# Run the application
./scripts/run.sh

# Run tests
./scripts/test.sh
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- virtualenv (optional but recommended)
- Docker (optional, for containerized deployment)

### Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rainerwanjohi384-cell/MealMate-backend.git
   cd MealMate-backend
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
# Database
DATABASE_URL=sqlite:///./mealmate.db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Firebase (optional for full authentication)
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./mealmate.db` |
| `SECRET_KEY` | JWT secret key (⚠️ change in production!) | Required |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `FIREBASE_CREDENTIALS_PATH` | Path to Firebase credentials | `./firebase-credentials.json` |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:3000` |

## Running the Application

### Development Mode

```bash
# Using the convenience script
./scripts/run.sh

# Or directly with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Using Docker
docker-compose up -d

# Or with gunicorn (install first: pip install gunicorn)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Access Points

- **API**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Documentation

### Authentication

All protected endpoints require a Bearer token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Main Endpoints

#### Users
- `POST /api/users/register` - Register a new user
- `POST /api/users/login` - Login with Firebase token
- `GET /api/users/me` - Get current user profile

#### Recipes
- `GET /api/recipes` - List all user recipes
- `POST /api/recipes` - Create a new recipe
- `GET /api/recipes/{id}` - Get specific recipe
- `PUT /api/recipes/{id}` - Update recipe
- `DELETE /api/recipes/{id}` - Delete recipe

#### Meal Plans
- `GET /api/meal-plans` - List all meal plans
- `POST /api/meal-plans` - Create a meal plan
- `GET /api/meal-plans/{id}` - Get specific meal plan
- `PUT /api/meal-plans/{id}` - Update meal plan
- `DELETE /api/meal-plans/{id}` - Delete meal plan

### Example Requests

#### Create a Recipe

```bash
curl -X POST "http://localhost:8000/api/recipes" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Spaghetti Carbonara",
    "ingredients": "Pasta, eggs, bacon, parmesan cheese, black pepper",
    "instructions": "1. Cook pasta. 2. Fry bacon. 3. Mix eggs and cheese. 4. Combine all.",
    "category": "Dinner"
  }'
```

#### Create a Meal Plan

```bash
curl -X POST "http://localhost:8000/api/meal-plans" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "recipe_id": 1,
    "day_of_week": "Monday",
    "meal_type": "Dinner"
  }'
```

For complete API documentation, visit http://localhost:8000/docs after starting the server.

## Testing

### Run All Tests

```bash
# Using the test script
./scripts/test.sh

# Or directly with pytest
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=app --cov-report=html
```

### Test Coverage

```bash
# Generate HTML coverage report
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

### Run Specific Tests

```bash
# Test specific file
pytest tests/test_api.py -v

# Test specific function
pytest tests/test_api.py::test_create_recipe -v
```

## Deployment

### Docker Deployment

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Deployment

```bash
# Pull latest code
git pull origin main

# Run deployment script
./scripts/deploy.sh
```

### CI/CD

The project includes GitHub Actions workflows for:
- Automated testing on push/PR
- Docker image building
- Deployment automation

See `.github/workflows/` for configuration.

## Project Structure

```
MealMate-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   └── routers/             # API route handlers
│       ├── __init__.py
│       ├── users.py
│       ├── recipes.py
│       └── meal_plans.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   └── test_api.py          # API tests
├── scripts/
│   ├── setup.sh             # Environment setup
│   ├── run.sh               # Run application
│   ├── test.sh              # Run tests
│   └── deploy.sh            # Deployment script
├── .github/
│   └── workflows/
│       ├── backend-ci.yml   # Backend CI/CD
│       └── frontend-deploy.yml  # Frontend deployment
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── .gitignore
├── pyproject.toml          # Project configuration
├── DOCKER.md               # Docker documentation
└── README.md               # This file
```

## Database Schema

### Users Table
- `id`: Primary key
- `firebase_uid`: Unique Firebase identifier
- `email`: User email
- `name`: User name
- `created_at`, `updated_at`: Timestamps

### Recipes Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `name`: Recipe name
- `ingredients`: Recipe ingredients (text)
- `instructions`: Cooking instructions (text)
- `category`: Recipe category (optional)
- `image_url`: Recipe image URL (optional)
- `created_at`, `updated_at`: Timestamps

### Meal_Plans Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `recipe_id`: Foreign key to Recipes
- `day_of_week`: Day for meal plan
- `meal_type`: Type of meal (Breakfast/Lunch/Dinner)
- `is_completed`: Completion status
- `planned_date`: Optional planned date
- `created_at`, `updated_at`: Timestamps

## Contributing

This is a group project. To contribute:

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and commit**
   ```bash
   git add .
   git commit -m "feat: description of your changes"
   ```

3. **Push to your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Select your branch
   - Add description and request review

### Commit Message Convention

We follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `ci:` CI/CD changes
- `devops:` DevOps/deployment changes

## Team Roles

- **Frontend Developer**: React UI implementation
- **Backend Developer**: API endpoints and business logic
- **Database Administrator**: Schema design and optimization
- **DevOps Engineer**: CI/CD, testing, deployment, and integration (this repository)

## Contact

For questions, open an issue on GitHub.