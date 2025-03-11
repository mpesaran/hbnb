import sys
import os
import pytest
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

@pytest.fixture
def client():
    """Provides a test client for making API requests."""
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture
def valid_amenity():
    """Returns a valid amenity payload."""
    return {"name": "Swimming Pool"}

@pytest.fixture
def invalid_amenity():
    """Returns an invalid amenity payload (empty name)."""
    return {"name": ""}

@pytest.fixture
def created_valid_amenity(client, valid_amenity):
    amenity_data = {"name": "Library"}
    """Creates a valid amenity in the database for testing."""
    response = client.post('/api/v1/amenities/', json=amenity_data)
    assert response.status_code == 201
    return response.json 

@pytest.fixture
def created_valid_amenity_2(client):
    """Creates a second amenity in the database for update testing."""
    amenity_data = {"name": "Cinema"}
    response = client.post('/api/v1/amenities/', json=amenity_data)
    assert response.status_code == 201
    return response.json

class TestAmenityEndpoints:
    """Test suite for amenity-related API endpoints."""

    """POST Methods"""
    def test_register_new_amenity_with_an_invalid_name(self, client, invalid_amenity):
        """Test registering a new amenity with an empty name."""
        response = client.post('/api/v1/amenities/', json=invalid_amenity)
        assert response.status_code == 400  
        assert response.json == {'error': 'Amenity name must be a non-empty string'}

    def test_register_new_amenity(self, client, valid_amenity):
        """Test successfully registering a new amenity."""
        response = client.post('/api/v1/amenities/', json=valid_amenity)
        assert response.status_code == 201 
        assert 'id' in response.json  
        assert response.json['name'] == valid_amenity['name']

    """GET Methods"""
    def test_get_all_amenities(self, client):
        """Test retrieving all amenities."""
        response = client.get('/api/v1/amenities/')
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) > 0

    def test_get_created_amenity(self, client, created_valid_amenity):
        """Test retrieving a specific amenity by ID."""
        amenity_id = created_valid_amenity['id']
        response = client.get(f'/api/v1/amenities/{amenity_id}')
        assert response.status_code == 200
        assert response.json['id'] == amenity_id
        assert response.json['name'] == created_valid_amenity['name']

    def test_get_amenity_with_an_invalid_ID(self, client):
        """Test retrieving a non-existent amenity."""
        invalid_amenity_id = random.randint(8000, 10000)
        response = client.get(f'/api/v1/amenities/{invalid_amenity_id}')
        assert response.status_code == 404
        assert response.json == {'error': 'Amenity not found'}

    """PUT Methods"""
    def test_to_update_amenity_name(self, client, created_valid_amenity_2):
        """Test updating an existing amenity's name."""
        updated_name = "Sauna"
        amenity_id = created_valid_amenity_2['id']

        response = client.put(f'/api/v1/amenities/{amenity_id}', json={'name': updated_name})
        assert response.status_code == 200
        assert response.json['id'] == amenity_id
        assert response.json['name'] == updated_name
