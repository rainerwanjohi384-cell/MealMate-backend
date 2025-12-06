import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User, Recipe, MealPlan

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """Create test database tables before each test and drop after"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create test client with overridden database"""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    """Create a test user"""
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "firebase_uid": "test_firebase_uid_123"
    }
    response = client.post("/api/users/register", json=user_data)
    return response.json()


@pytest.fixture
def auth_headers(test_user):
    """Get authentication headers for test user"""
    # In a real scenario, you'd get a valid token
    # For testing, we'll create a mock token
    from app.auth import create_access_token
    token = create_access_token(
        data={"user_id": test_user["id"], "firebase_uid": test_user["firebase_uid"]}
    )
    return {"Authorization": f"Bearer {token}"}
