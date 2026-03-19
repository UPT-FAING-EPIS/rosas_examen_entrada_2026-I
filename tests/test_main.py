import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    activities["Test Activity"] = {
        "description": "Test",
        "schedule": "Test",
        "max_participants": 5,
        "participants": []
    }
    yield
    activities.pop("Test Activity", None)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200

def test_signup_success():
    response = client.post("/activities/Test Activity/signup?email=test@test.edu")
    assert response.status_code == 200

def test_signup_duplicate():
    client.post("/activities/Test Activity/signup?email=test@test.edu")
    response = client.post("/activities/Test Activity/signup?email=test@test.edu")
    assert response.status_code == 400

def test_unregister():
    client.post("/activities/Test Activity/signup?email=test@test.edu")
    response = client.delete("/activities/Test Activity/participants/test@test.edu")
    assert response.status_code == 200
    assert "test@test.edu" not in activities["Test Activity"]["participants"]
