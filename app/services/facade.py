from uuid import uuid4
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
    
    # ----------- USER methods -----------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
      
        def get_all_users(self):
        """Retrieve all users from the repository."""
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        """Update an existing user's details."""
        self.user_repo.update(user_id, update_data)
        user =  self.get_user(user_id)
        if not user:
            return None

        # Validate that email is unique if it's being updated
        if 'email' in update_data:
            existing_user = self.get_user_by_email(update_data['email'])
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        user.update(update_data)
        return user
    
    
    # ----------- PLACE methods -----------
    def create_place(self, place_data):
        """Validates input and creates new place"""
        
        if place_data.get('title') is None:
            raise TypeError("ERROR: Title must not be empty")
        
        if not isinstance(place_data.get('price'), (float, int)):
            raise TypeError("ERROR: Price must be a non-negative number.")
        if place_data.get('price') < 0:
            raise ValueError("ERROR: Price must be a non-negative number.")

        if not isinstance(place_data.get('longitude'), (float, int)):
            raise TypeError("ERROR: Longitude must be a number")
        if not (-180 <= place_data.get('longitude') <= 180):
            raise ValueError("ERROR: Longitude must be between -180 and 180")
        
        if not isinstance(place_data.get('latitude'), (int, float)):
            raise TypeError("ERROR: Latitude must be a number")
        if not (-90 <= place_data.get('latitude') <= 90):
            raise ValueError("ERROR: Latitude must be between -90 and 90")
        
        owner_found = self.get_user(place_data["owner"])
        if not owner_found:
            return {"ERROR": "Owner not found."}, 404
        
        place = Place(
            title=place_data["title"],
            description=place_data["description"],
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner_found,
            amenities=place_data.get("amenities", [])
        )
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        """"Retrieve a place using ID, owner and amenities"""
        place = self.place_repo.get(place_id)
        
        if place is None:
            return None

        owner = place.owner
        owner_data = None
        if owner is None:
            return None
        
        owner_data = {
            "id": owner.id,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email
        }

        
        amenities_found_by_id = []
        for amenity_id in place.amenities:
            amenity = self.amenity_repo.get(amenity_id)
            amenities_found_by_id.append(amenity)
        
        formatted_amenities = []
        for amenity in amenities_found_by_id:
            if amenity:
                formatted_amenities.append({"id": amenity.id, "name": amenity.name})

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": owner_data,
            "amenities": formatted_amenities
        }, 200


    def get_all_places(self):
        """Retrieves all places."""
        places = self.place_repo.get_all()
        list_all_places = []
        for place in places:
            list_all_places.append({
                                    "id": place.id, 
                                    "title": place.title,
                                    "latitude": place.latitude,
                                    "longitude": place.longitude
            })
        return list_all_places


    def update_place(self, place_id, place_data):
      """Update a place's information."""
        place = self.place_repo.get(place_id)
        if not place:
            return {"ERROR": "Place not found."}, 400

        if "price" in place_data:
            if not isinstance(place_data["price"], (float, int)) or place_data["price"] < 0:
                return {"ERROR": "Price must be a non-negative number."}, 400
            place.price=place_data["price"]

        if "latitude" in place_data:
            if not isinstance(place_data["latitude"], (float, int)) or not (-90 <= place_data["latitude"] <= 90):
                return {"ERROR": "Latitude must be between -90 and 90."}, 400
            place.latitude=place_data["latitude"]

        if "longitude" in place_data:
            if not isinstance(place_data["longitude"], (float, int)) or not (-180 <= place_data["longitude"] <= 180):
                return {"ERROR": "Longitude must be between -180 and 180."}
            place.longitude=place_data["longitude"]

        # updating values if all checks hae passed.
        for key, value in place_data.items():
            if hasattr(place, key) and key not in ['price', 'latitude', 'longitude']:
                setattr(place, key, value)

        return {"message": "Place updated successfully!"}
      
      
    

    # - - - AMENITIES methods - - - 
    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        return self.amenity_repo.update(amenity_id, amenity_data)
       
   
  
  

    # - - - REVIEW methods - - -
    
    # Methods for Review
    def create_review(self, review_data):
        """Create new review after validation"""
        user = self.user_repo.get(review_data['user_id'])
        place = self.place_repo.get(review_data['place_id'])
        if not user or not place:
            raise ValueError("Invalid user_id or place_id")
        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1 and 5")
        review = Review(
            id=str(uuid4()),
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieves a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieves all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieves all reviews for a specific place."""
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        """Updates an existing review"""
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data and 1 <= review_data['rating'] <= 5:
            review.rating = review_data['rating']
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        """Delete review"""
        return self.review_repo.delete(review_id)

