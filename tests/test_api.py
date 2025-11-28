"""
Corrected integration tests for the SpectrumCircle REST API endpoints 
using FastAPI's TestClient.
"""
import fastmcp
import mcp.types

import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import pytest
import uuid
from fastapi.testclient import TestClient
from backend.api.main import app

# Initialize the TestClient
client = TestClient(app)

# Global Test Variables
TEST_USER_ID_CONTAINER = {} 
TEST_PROFILE_DATA = {
    "age": 25,
    "diagnosis": "autism_level1",
    "communication_preference": "direct",
    "sensory_profile": {
        "seeking": ["proprioceptive"],
        "avoiding": ["auditory"]
    },
    "special_interests": [
        {"topic": "astronomy", "intensity": "high"}
    ]
}

def get_unique_user_id():
    """Generates a unique user ID for test isolation."""
    return f"temp_test_{uuid.uuid4().hex[:10]}"

# Test runner cases
def test_01_health_check():
    """Test API health status on the root endpoint ('/')."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "SpectrumCircle API" in data["service"]

def test_02_create_profile():
    """Test profile creation (POST /profiles) with a unique ID."""
    global TEST_USER_ID_CONTAINER
    
    new_user_id = get_unique_user_id()
    TEST_USER_ID_CONTAINER['id'] = new_user_id
    
    profile_data = TEST_PROFILE_DATA.copy()
    profile_data["user_id"] = new_user_id
    
    response = client.post("/profiles", json=profile_data)
    
    assert response.status_code == 200 
    assert response.json()["success"] is True

def test_03_get_profile_success():
    """Test successful profile retrieval using the created unique ID."""
    user_id = TEST_USER_ID_CONTAINER.get('id')
    
    if not user_id: pytest.skip("Skipping as profile creation failed.") 
    
    response = client.get(f"/profiles/{user_id}")
    
    assert response.status_code == 200
    assert response.json()["success"] is True
    
    profile = response.json()["profile"]
    assert profile["user_id"] == user_id
    assert profile["age"] == 25

def test_04_get_profile_not_found():
    """Test profile retrieval for a non-existent user."""

    response = client.get("/profiles/definitely_not_a_real_id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_05_user_stats():
    """Test user statistics retrieval using the created unique ID."""
    user_id = TEST_USER_ID_CONTAINER.get('id')
    if not user_id: pytest.skip("Skipping as profile creation failed.")
    
    response = client.get(f"/stats/{user_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["success"] is True
    assert "stats" in data
    
    stats = data["stats"]
    
    assert stats["special_interests_count"] == 1 
    assert "total_conversations" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])