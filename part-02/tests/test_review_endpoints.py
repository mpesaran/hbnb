import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        """Setup test client"""
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review_valid(self):
        """Test creating a valid review"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_rating(self):
        """Test creating a review with invalid rating"""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice spot!",
            "rating": 6,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_reviews(self):
        """Test retrieving all reviews"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)

    def test_get_review_not_found(self):
        """Test retrieving non-existent review"""
        response = self.client.get('/api/v1/reviews/invalid-id')
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        """Test updating an existing review"""
        review_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review",
            "rating": 4
        })
        self.assertEqual(response.status_code, 200)

    def test_update_review_not_found(self):
        """Test updating a non-existent review"""
        response = self.client.put('/api/v1/reviews/invalid-id', json={
            "text": "Good experience!",
            "rating": 5
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_review(self):
        """Test deleting an existing review"""
        review_id = "2fa85f64-5717-4562-b3fc-2c963f66afa6"
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_review_not_found(self):
        """Test deleting non-existent review"""
        response = self.client.delete('/api/v1/reviews/invalid-id')
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()