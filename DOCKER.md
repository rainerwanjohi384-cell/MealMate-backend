# Docker Setup

## Using docker-compose (easiest way)

Start the application:
```bash
docker-compose up -d
```

Stop it:
```bash
docker-compose down
```

View logs:
```bash
docker-compose logs -f backend
```

Rebuild after changes:
```bash
docker-compose up -d --build
```

## Manual Docker commands

Build:
```bash
docker build -t mealmate-backend .
```

Run:
```bash
docker run -d -p 8000:8000 --name mealmate-backend mealmate-backend
```

Stop:
```bash
docker stop mealmate-backend
docker rm mealmate-backend
```

## Access

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
