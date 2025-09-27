import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.db import get_db, Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_classes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def authenticated_user():
    """Create and authenticate a user for testing"""
    # Register user
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "classtest@example.com",
            "password": "testpassword123",
            "full_name": "Class Test User"
        }
    )
    
    # Login and get token
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "classtest@example.com",
            "password": "testpassword123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_class(authenticated_user):
    """Test creating a new class"""
    class_data = {
        "name": "Introduction to Computer Science",
        "code": "CS101",
        "description": "Basic computer science concepts",
        "credits": 3,
        "semester": "Fall 2024",
        "professor": "Dr. Smith"
    }
    
    response = client.post(
        "/api/v1/classes/",
        json=class_data,
        headers=authenticated_user
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == class_data["name"]
    assert data["code"] == class_data["code"]
    assert data["credits"] == class_data["credits"]
    assert "id" in data

def test_get_classes_empty(authenticated_user):
    """Test getting classes when user has none"""
    response = client.get("/api/v1/classes/", headers=authenticated_user)
    assert response.status_code == 200
    assert response.json() == []

def test_get_classes_with_data(authenticated_user):
    """Test getting classes when user has some"""
    # Create a class first
    class_data = {
        "name": "Mathematics",
        "code": "MATH101",
        "credits": 4
    }
    
    create_response = client.post(
        "/api/v1/classes/",
        json=class_data,
        headers=authenticated_user
    )
    assert create_response.status_code == 200
    
    # Get classes
    response = client.get("/api/v1/classes/", headers=authenticated_user)
    assert response.status_code == 200
    classes = response.json()
    assert len(classes) == 1
    assert classes[0]["name"] == class_data["name"]

def test_get_specific_class(authenticated_user):
    """Test getting a specific class by ID"""
    # Create a class first
    class_data = {
        "name": "Physics",
        "code": "PHY101",
        "credits": 3
    }
    
    create_response = client.post(
        "/api/v1/classes/",
        json=class_data,
        headers=authenticated_user
    )
    class_id = create_response.json()["id"]
    
    # Get the specific class
    response = client.get(f"/api/v1/classes/{class_id}", headers=authenticated_user)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == class_data["name"]
    assert data["id"] == class_id

def test_get_nonexistent_class(authenticated_user):
    """Test getting a class that doesn't exist"""
    response = client.get("/api/v1/classes/999", headers=authenticated_user)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_update_class(authenticated_user):
    """Test updating a class"""
    # Create a class first
    class_data = {
        "name": "Chemistry",
        "code": "CHEM101",
        "credits": 3
    }
    
    create_response = client.post(
        "/api/v1/classes/",
        json=class_data,
        headers=authenticated_user
    )
    class_id = create_response.json()["id"]
    
    # Update the class
    update_data = {
        "name": "Advanced Chemistry",
        "professor": "Dr. Johnson"
    }
    
    response = client.put(
        f"/api/v1/classes/{class_id}",
        json=update_data,
        headers=authenticated_user
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["professor"] == update_data["professor"]
    assert data["code"] == class_data["code"]  # Should remain unchanged

def test_delete_class(authenticated_user):
    """Test deleting a class"""
    # Create a class first
    class_data = {
        "name": "Biology",
        "code": "BIO101",
        "credits": 4
    }
    
    create_response = client.post(
        "/api/v1/classes/",
        json=class_data,
        headers=authenticated_user
    )
    class_id = create_response.json()["id"]
    
    # Delete the class
    response = client.delete(f"/api/v1/classes/{class_id}", headers=authenticated_user)
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/classes/{class_id}", headers=authenticated_user)
    assert get_response.status_code == 404

def test_create_class_minimal_data(authenticated_user):
    """Test creating a class with minimal required data"""
    class_data = {
        "name": "Minimal Class"
    }
    
    response = client.post(
        "/api/v1/classes/",
        json=class_data,
        headers=authenticated_user
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == class_data["name"]
    assert data["credits"] == 3  # Default value