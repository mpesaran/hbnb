import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

@pytest.fixture
def client():
    """A test client for the app."""
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture
def valid_amenity():
    """Fixture to provide a valid amenity."""
    return {
        "name": "Swimming Pool"
    }

@pytest.fixture
def invalid_amenity():
    """Fixture to provide a valid user dictionary."""
    return {
        "name": ""
    }

@pytest.fixture
def create_valid_amenity():
    response = client.post('/api/v1/amenities/', json=valid_user)
    assert response.status_code == 201
    user_data = response.json
    # assert "id" in user_data, "User ID is missing in the API response!"
    return user_data


class TestAmenityEndpoints:
    def test_register_new_amenity_with_an_invalid_name(self, client, invalid_amenity):
        """Test registering a new amenity with an empty name string."""
        response = client.post('/api/v1/amenities/', json=invalid_amenity)
        assert response.status_code == 400  # this should fail - fix errro handling in facade
        assert 'error' in response.json
        assert response.json['error'] == 'Amenity name must be a non-empty string'

    def test_register_new_amenity(self, client, valid_amenity):
        """Test registering a new amenity."""
        response = client.post('/api/v1/amenities/', json=valid_amenity)
        assert response.status_code == 201  # Check if creation was successful
        assert 'id' in response.json  # Check if an ID was returned
        assert 'name' in response.json  # Check if an name was returned
    
    def test_get_all_amenities(self, client):
        """Test getting all amenities."""
        response = client.get('/api/v1/amenities/')
        assert response.status_code == 200  # Check if creation was successful
        assert isinstance(response.json, list)
        assert len(response.json) > 0
    
    def test_get_created_amenity(self, client):
        """Test getting all amenities."""
        amenity_id = 
