import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

# sys.path.append("..")
# @pytest.fixture()
# def app():
#     """Creates a single app instance for all tests in the session."""
#     app = create_app()
    
#     return app 

@pytest.fixture
def client():
    """A test client for the app."""
    app = create_app()
    with app.test_client() as client:
        yield client

@pytest.fixture
def valid_user():
    """Fixture to provide a valid user dictionary."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@doe.com",
    }

@pytest.fixture
def created_user(client, valid_user):
    """Create a user in the database for testing purposes."""
    response = client.post('/api/v1/users/', json=valid_user)
    assert response.status_code == 201
    user_data = response.json
    # assert "id" in user_data, "User ID is missing in the API response!"
    return user_data

class TestUserEndpoints:
    def test_create_user(self, client, valid_user):
        """Test creating a user."""
        response = client.post('/api/v1/users/', json=valid_user)
        assert response.status_code == 201  # Check if creation was successful
        assert 'id' in response.json  # Check if an ID was returned

    def test_get_users(self, client, created_user):
        """Test retrieving the created user."""
        response = client.get('/api/v1/users/')
        assert response.status_code == 200  # Check if retrieval was successful
        assert isinstance(response.json, list)  # Ensure response is a list
        assert len(response.json) > 0  # Ensure at least one user exists
        assert isinstance(response.json[0], dict)

    def test_get_user(self, client, created_user):
        """Test retrieving the created user."""
        user_id = created_user['id']
        response = client.get(f'/api/v1/users/{user_id}')
        assert response.status_code == 200  # Check if retrieval was successful
        assert response.json['email'] == "john@doe.com"  # Verify user data matches valid_user

    def test_update_user(self, client, created_user):
        """Test updating a user."""
        user_id = created_user['id']
        if user_id:
            response = client.put(f'/api/v1/users/{user_id}', json={
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com"
            })
            assert response.status_code == 200  # Check if update was successful
        else:
            assert response.status_code == 404
        # Retrieve the user again to check if the update was applied
        response = client.get(f'/api/v1/users/{user_id}')
        assert response.json['email'] == "jane.smith@example.com"  # Verify updated user data

    def test_create_user_with_invalid_email(self, client):
        """Test creating a user with invalid email."""
        invalid_user_data = {
            "first_name": "Jhone",
            "last_name": "Smith",
            "email": "not-an-email"
        }

        response = client.post('/api/v1/users/', json=invalid_user_data)
        assert response.status_code == 400  # Check if creation was unsuccessful
        assert 'error' in response.json
        assert response.json['error'] == 'setter validation failure: Invalid email format.'

    def test_create_user_with_invalid_name(self, client):
        """Test creating a user with invalid username."""
        invalid_user_data = {
            "first_name": "",
            "last_name": "Smith",
            "email": "smith@example.com"
        }

        response = client.post('/api/v1/users/', json=invalid_user_data)
        assert response.status_code == 400  # Check if creation was unsuccessful
        assert 'error' in response.json
        assert response.json['error'] == 'setter validation failure: First name cannot be empty.'

    def test_create_user_with_existing_email(self, client, created_user):
        """Test creating a user with an email that already exists in the database."""
        existing_email_user = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": created_user["email"]  # Use the same email as the existing user
        }

        response = client.post('/api/v1/users/', json=existing_email_user)
        assert response.status_code == 400  # Ensure user creation fails
        assert 'error' in response.json  # Ensure error message is present
        assert response.json['error'] == 'Email already registered'

    def test_update_user_with_invalid_email(self, client, created_user):
        """Test updating a user with an invalid email format."""
        user_id = created_user['id']
        invalid_email_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email-format"
        }

        response = client.put(f'/api/v1/users/{user_id}', json=invalid_email_data)
        assert response.status_code == 400
        assert 'error' in response.json
        assert response.json['error'] == "Invalid email format." 