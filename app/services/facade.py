from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    
    # ----------- PLACE methods -----------
    def create_place(self, place_data):
        """Validates input and creates new place"""
        
        if not place_data.get('title'):
            return {"ERROR": "Title is required."}, 400
        
        if not isinstance(place_data.get('price'), (float, int)):
            return {"ERROR": "Error: Price must be a number."}, 400
        if place_data.get('price') < 0:
            return {"ERROR": "Error: Price must be a non-negative number."}, 400

        if not isinstance(place_data.get('longitude'), (float, int)):
            return {"ERROR": "Error: Longitude must be a number."}, 400
        if not (-180 <= place_data.get('longitude') <= 180):
            return {"ERROR": "Longitude must be between -180 and 180."}, 400
        
        if not isinstance(place_data.get('latitude'), (float, int)):
            return {"ERROR": "Error: Latitude must be a number."}, 400
        if not (-90 <= place_data.get('latitude') <= 90):
            return {"ERROR": "Latitude must be between -90 and 90."}, 400
        
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
            return {"ERROR": "Place not found"}, 404

        owner = place.owner
        owner_data = None
        if owner is None:
            return {"ERROR": "Owner not found"}, 404
        
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
        }


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
    