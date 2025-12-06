# MealMate Backend - Docker Commands

## Quick Start with Docker

### Build and run with docker-compose:
```bash
docker-compose up -d
```

### Stop the application:
```bash
docker-compose down
```

### View logs:
```bash
docker-compose logs -f backend
```

### Rebuild after code changes:
```bash
docker-compose up -d --build
```

## Manual Docker Commands

### Build the image:
```bash
docker build -t mealmate-backend .
```

### Run the container:
```bash
docker run -d -p 8000:8000 --name mealmate-backend mealmate-backend
```

### Stop and remove container:
```bash
docker stop mealmate-backend
docker rm mealmate-backend
```

## Access the Application

- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
