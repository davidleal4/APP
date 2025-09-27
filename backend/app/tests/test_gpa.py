import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.db import get_db, Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_gpa.db"
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
            "email": "gpatest@example.com",
            "password": "testpassword123",
            "full_name": "GPA Test User"
        }
    )
    
    # Login and get token
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "gpatest@example.com",
            "password": "testpassword123"
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def setup_test_data(authenticated_user):
    """Set up test classes and assignments"""
    # Create a class
    class_response = client.post(
        "/api/v1/classes/",
        json={
            "name": "Test Class",
            "code": "TEST101",
            "credits": 3
        },
        headers=authenticated_user
    )
    class_id = class_response.json()["id"]
    
    # Create assignments
    assignments = [
        {
            "title": "Assignment 1",
            "points_possible": 100,
            "points_earned": 95,
            "completed": True,
            "class_id": class_id
        },
        {
            "title": "Assignment 2",
            "points_possible": 100,
            "points_earned": 87,
            "completed": True,
            "class_id": class_id
        },
        {
            "title": "Assignment 3",
            "points_possible": 100,
            "points_earned": 92,
            "completed": True,
            "class_id": class_id
        }
    ]
    
    for assignment in assignments:
        client.post(
            "/api/v1/assignments/",
            json=assignment,
            headers=authenticated_user
        )
    
    return {"class_id": class_id}

def test_calculate_gpa_no_data(authenticated_user):
    """Test GPA calculation with no assignments"""
    response = client.get("/api/v1/gpa/calculate", headers=authenticated_user)
    assert response.status_code == 200
    data = response.json()
    assert data["overall_gpa"] == 0
    assert data["total_credits"] == 0
    assert data["class_grades"] == []

def test_calculate_gpa_with_data(authenticated_user, setup_test_data):
    """Test GPA calculation with assignments"""
    response = client.get("/api/v1/gpa/calculate", headers=authenticated_user)
    assert response.status_code == 200
    data = response.json()
    
    assert data["overall_gpa"] > 0
    assert data["total_credits"] == 3
    assert len(data["class_grades"]) == 1
    
    # Check class grade calculation
    class_grade = data["class_grades"][0]
    assert class_grade["class_name"] == "Test Class"
    assert class_grade["credits"] == 3
    assert "percentage" in class_grade
    assert "grade_point" in class_grade
    
    # Expected percentage: (95 + 87 + 92) / 300 * 100 = 91.33%
    expected_percentage = (95 + 87 + 92) / 300 * 100
    assert abs(class_grade["percentage"] - expected_percentage) < 0.1

def test_predict_gpa_default_target(authenticated_user):
    """Test GPA prediction with default target"""
    response = client.get("/api/v1/gpa/predict", headers=authenticated_user)
    assert response.status_code == 200
    data = response.json()
    
    assert "current_gpa" in data
    assert data["target_gpa"] == 3.5  # Default target
    assert "current_credits" in data
    assert "upcoming_assignments" in data
    assert "recommendation" in data

def test_predict_gpa_custom_target(authenticated_user):
    """Test GPA prediction with custom target"""
    target_gpa = 3.8
    response = client.get(f"/api/v1/gpa/predict?target_gpa={target_gpa}", headers=authenticated_user)
    assert response.status_code == 200
    data = response.json()
    
    assert data["target_gpa"] == target_gpa
    assert "recommendation" in data

def test_predict_gpa_with_data(authenticated_user, setup_test_data):
    """Test GPA prediction with existing data"""
    # Create an incomplete assignment
    client.post(
        "/api/v1/assignments/",
        json={
            "title": "Future Assignment",
            "points_possible": 100,
            "completed": False,
            "class_id": setup_test_data["class_id"]
        },
        headers=authenticated_user
    )
    
    response = client.get("/api/v1/gpa/predict?target_gpa=4.0", headers=authenticated_user)
    assert response.status_code == 200
    data = response.json()
    
    assert data["target_gpa"] == 4.0
    assert data["upcoming_assignments"] >= 1  # At least the one we just created
    assert data["current_gpa"] > 0  # Should have calculated GPA from completed assignments

def test_gpa_calculation_edge_cases(authenticated_user):
    """Test GPA calculation edge cases"""
    # Create class with zero points assignment
    class_response = client.post(
        "/api/v1/classes/",
        json={
            "name": "Edge Case Class",
            "credits": 2
        },
        headers=authenticated_user
    )
    class_id = class_response.json()["id"]
    
    # Assignment with zero points possible
    client.post(
        "/api/v1/assignments/",
        json={
            "title": "Zero Points Assignment",
            "points_possible": 0,
            "points_earned": 0,
            "completed": True,
            "class_id": class_id
        },
        headers=authenticated_user
    )
    
    response = client.get("/api/v1/gpa/calculate", headers=authenticated_user)
    assert response.status_code == 200
    # Should handle zero points gracefully without crashing

def test_percentage_to_gpa_conversion():
    """Test the percentage to GPA conversion logic"""
    from app.api.v1.gpa import percentage_to_gpa
    
    # Test various percentage ranges
    assert percentage_to_gpa(97) == 4.0
    assert percentage_to_gpa(93) == 3.7
    assert percentage_to_gpa(90) == 3.3
    assert percentage_to_gpa(87) == 3.0
    assert percentage_to_gpa(80) == 2.3
    assert percentage_to_gpa(70) == 1.3
    assert percentage_to_gpa(60) == 0.0