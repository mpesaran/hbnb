import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()


    # - - - TESTS: CREATE PLACE (POST) - - - 
    def test_create_place_valid_data(self):
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com"
        })
        self.assertEqual(user_response.status_code, 201)
        user_data = user_response.get_json()
        owner_id = user_data["id"]
        
        response = self.client.post('/api/v1/places/', json={
            "title": "Test place",
            "description": "This place exists",
            "price": 120.00,
            "latitude": 33.333,
            "longitude": -122.2222,
            "owner": owner_id,
            "amenities": ["amenity1", "amenity2"]
        })
        self.assertEqual(response.status_code, 201, f"Unexpected response: {response.get_json()}")
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Test place")
        self.assertEqual(data["price"], 120.00)


    def test_create_place_invalid_title(self):
        response = self.client.post('/api/v1/places/', json={
            "description": "Place no title",
            "price": 120.5,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner": "user123",
            "amenities": ["amenity1", "amenity2"]
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["ERROR"], "ERROR: Title must not be empty.")
    
        
    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test place",
            "description": "This place exists",
            "price": -120.00,
            "latitude": 33.333,
            "longitude": -122.2222,
            "owner": "user123",
            "amenities": ["amenity1", "amenity2"]
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["ERROR"], "ERROR: Price must be a non-negative number.")
        
        
    def test_create_place_invalid_latitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test place",
            "description": "This place exists",
            "price": 120.00,
            "latitude": -333.333,
            "longitude": -22.2222,
            "owner": "user123",
            "amenities": ["amenity1", "amenity2"]
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["ERROR"], "ERROR: Latitude must be between -90 and 90")


    def test_create_place_invalid_longitude(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test place",
            "description": "This place exists",
            "price": 120.00,
            "latitude": 33.333,
            "longitude": -2222.22,
            "owner": "user123",
            "amenities": ["amenity1", "amenity2"]
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["ERROR"], "ERROR: Longitude must be between -180 and 180")
        
        
    # - - - TESTS: GET PLACE  (GET) - - -
    def test_get_places(self):
        response = self.client.post('/api/v1/places/', json={
        "title": "Test place",
        "description": "This place exists",
        "price": 120.00,
        "latitude": 33.333,
        "longitude": -122.2222,
        "owner": "user123",
        "amenities": ["amenity1", "amenity2"]
        })
        self.assertEqual(response.status_code, 201)
        
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        if data:
            self.assertIn("id", data[0])
            self.assertIn("title", data[0])
        else:
            self.fail("No places in database.")



    def test_get_place_not_found(self):
        response = self.client.get('/api/v1/places/nonexistent_id')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["ERROR"], "Place not found")
        

    # - - - TESTS: UPDATE PLACE (PUT) - - -
    def test_update_place_valid_data(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test place",
            "description": "This place exists",
            "price": 120.00,
            "latitude": 33.333,
            "longitude": -122.2222,
            "owner": "user123",
            "amenities": ["amenity1", "amenity2"]
        })
        place_id = response.get_json()["id"]
        
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Test place",
            "price": 150.0
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Place updated successfully!")


    def test_update_place_invalid_data(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Test place",
            "description": "This place exists",
            "price": 120.00,
            "latitude": 33.333,
            "longitude": -122.2222,
            "owner": "user123",
            "amenities": ["amenity1", "amenity2"]
        })
        place_id = response.get_json()["id"] # maybe convert to integer 
        

        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "price": -230.00
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["ERROR"], "Price must be a non-negative number.")
