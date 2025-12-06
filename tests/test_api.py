"""
API Integration Tests
Tests for all API endpoints including authentication, recipes, and meal plans
"""


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "api" in data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "MealMate" in data["message"]


# User Tests
def test_user_registration(client):
    """Test user registration"""
    user_data = {
        "email": "newuser@example.com",
        "name": "New User",
        "firebase_uid": "firebase_uid_456"
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "id" in data


def test_duplicate_user_registration(client, test_user):
    """Test that duplicate user registration fails"""
    user_data = {
        "email": test_user["email"],
        "name": "Duplicate User",
        "firebase_uid": test_user["firebase_uid"]
    }
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code == 400


def test_get_user_profile(client, auth_headers):
    """Test getting user profile"""
    response = client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "name" in data


# Recipe Tests
def test_create_recipe(client, auth_headers):
    """Test creating a recipe"""
    recipe_data = {
        "name": "Pancakes",
        "ingredients": "Flour, eggs, milk, sugar",
        "instructions": "Mix ingredients and cook on griddle",
        "category": "Breakfast"
    }
    response = client.post("/api/recipes", json=recipe_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == recipe_data["name"]
    assert data["category"] == recipe_data["category"]
    assert "id" in data


def test_get_recipes(client, auth_headers):
    """Test getting all recipes for a user"""
    # Create a recipe first
    recipe_data = {
        "name": "Test Recipe",
        "ingredients": "Test ingredients",
        "instructions": "Test instructions"
    }
    client.post("/api/recipes", json=recipe_data, headers=auth_headers)
    
    # Get all recipes
    response = client.get("/api/recipes", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_recipe_by_id(client, auth_headers):
    """Test getting a specific recipe"""
    # Create a recipe
    recipe_data = {
        "name": "Spaghetti",
        "ingredients": "Pasta, tomato sauce",
        "instructions": "Boil pasta, add sauce"
    }
    create_response = client.post("/api/recipes", json=recipe_data, headers=auth_headers)
    recipe_id = create_response.json()["id"]
    
    # Get the recipe
    response = client.get(f"/api/recipes/{recipe_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == recipe_data["name"]


def test_update_recipe(client, auth_headers):
    """Test updating a recipe"""
    # Create a recipe
    recipe_data = {
        "name": "Original Recipe",
        "ingredients": "Original ingredients",
        "instructions": "Original instructions"
    }
    create_response = client.post("/api/recipes", json=recipe_data, headers=auth_headers)
    recipe_id = create_response.json()["id"]
    
    # Update the recipe
    update_data = {"name": "Updated Recipe"}
    response = client.put(f"/api/recipes/{recipe_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Recipe"


def test_delete_recipe(client, auth_headers):
    """Test deleting a recipe"""
    # Create a recipe
    recipe_data = {
        "name": "Recipe to Delete",
        "ingredients": "Ingredients",
        "instructions": "Instructions"
    }
    create_response = client.post("/api/recipes", json=recipe_data, headers=auth_headers)
    recipe_id = create_response.json()["id"]
    
    # Delete the recipe
    response = client.delete(f"/api/recipes/{recipe_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/recipes/{recipe_id}", headers=auth_headers)
    assert get_response.status_code == 404


# Meal Plan Tests
def test_create_meal_plan(client, auth_headers):
    """Test creating a meal plan"""
    # First create a recipe
    recipe_data = {
        "name": "Breakfast Recipe",
        "ingredients": "Eggs, toast",
        "instructions": "Cook eggs, toast bread"
    }
    recipe_response = client.post("/api/recipes", json=recipe_data, headers=auth_headers)
    recipe_id = recipe_response.json()["id"]
    
    # Create meal plan
    meal_plan_data = {
        "recipe_id": recipe_id,
        "day_of_week": "Monday",
        "meal_type": "Breakfast"
    }
    response = client.post("/api/meal-plans", json=meal_plan_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["day_of_week"] == "Monday"
    assert data["recipe_id"] == recipe_id


def test_get_meal_plans(client, auth_headers):
    """Test getting all meal plans"""
    response = client.get("/api/meal-plans", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_meal_plan(client, auth_headers):
    """Test updating a meal plan"""
    # Create recipe and meal plan
    recipe_data = {
        "name": "Dinner Recipe",
        "ingredients": "Chicken, rice",
        "instructions": "Cook chicken and rice"
    }
    recipe_response = client.post("/api/recipes", json=recipe_data, headers=auth_headers)
    recipe_id = recipe_response.json()["id"]
    
    meal_plan_data = {
        "recipe_id": recipe_id,
        "day_of_week": "Tuesday",
        "meal_type": "Dinner"
    }
    create_response = client.post("/api/meal-plans", json=meal_plan_data, headers=auth_headers)
    meal_plan_id = create_response.json()["id"]
    
    # Update meal plan
    update_data = {"is_completed": 1}
    response = client.put(f"/api/meal-plans/{meal_plan_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["is_completed"] == 1


def test_delete_meal_plan(client, auth_headers):
    """Test deleting a meal plan"""
    # Create recipe and meal plan
    recipe_data = {
        "name": "Lunch Recipe",
        "ingredients": "Sandwich ingredients",
        "instructions": "Make sandwich"
    }
    recipe_response = client.post("/api/recipes", json=recipe_data, headers=auth_headers)
    recipe_id = recipe_response.json()["id"]
    
    meal_plan_data = {
        "recipe_id": recipe_id,
        "day_of_week": "Wednesday",
        "meal_type": "Lunch"
    }
    create_response = client.post("/api/meal-plans", json=meal_plan_data, headers=auth_headers)
    meal_plan_id = create_response.json()["id"]
    
    # Delete meal plan
    response = client.delete(f"/api/meal-plans/{meal_plan_id}", headers=auth_headers)
    assert response.status_code == 200


# Authentication Tests
def test_unauthorized_access(client):
    """Test that endpoints require authentication"""
    response = client.get("/api/recipes")
    assert response.status_code in [401, 403]  # Unauthorized or Forbidden without auth
