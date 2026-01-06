import pytest
from fastapi.testclient import TestClient
from src.app import app  # Import the FastAPI app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity():
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Chess Club" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Chess Club/signup", params={"email": "duplicate@example.com"})
    # Second signup
    response = client.post("/activities/Chess Club/signup", params={"email": "duplicate@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up for this activity" in data["detail"]

def test_unregister_from_activity():
    # First signup
    client.post("/activities/Programming Class/signup", params={"email": "unregister@example.com"})
    # Then unregister
    response = client.delete("/activities/Programming Class/signup", params={"email": "unregister@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@example.com from Programming Class" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@example.com" not in data["Programming Class"]["participants"]

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess Club/signup", params={"email": "notsigned@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "Student not signed up for this activity" in data["detail"]