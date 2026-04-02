import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert (AAA) pattern is used in all tests

def test_get_activities():
    # Arrange: (No setup needed for a simple GET)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()), None)
    assert activity is not None, "No activities available for testing."
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code in (200, 400)  # 400 if already signed up
    data = response.json()
    assert "message" in data or "detail" in data

def test_unregister_activity():
    # Arrange
    email = "testuser@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()), None)
    assert activity is not None, "No activities available for testing."
    # Ensure user is signed up first
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code in (200, 404)  # 404 if not found
    data = response.json()
    assert "message" in data or "detail" in data
