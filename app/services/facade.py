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
    
    
    # Methods for Place
    def create_place(self, place_data):
        """Validates input and creates new place"""
        
        if place_data.get('price') < 0:
            raise ValueError("Error: Price must be a non-negative number.")

        if not (-180 <= place_data.get('longitude', 181) <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        
        if not (-90 <= place_data.get('latitude', 91) <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        
        owner = self.get_user(place_data["owner_id"])
        if not owner:
            raise ValueError("Unknown Owner")
        
        place = Place(
            title=place_data["title"],
            description=place_data["description"],
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id=place_data["owner_id"],
            amenities=place_data["amenities"]
        )
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        """"Retrieve a place using ID, owner and amenities"""
        
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.get_user(place.owner_id)
        owner_data = None
        if owner:
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
            "amenities": place.amenities
        }

    def get_all_places(self):
        """Retrieves all places."""
        places = self.place_repo.get_all()
        list_all_places = []
        for place in places:
            list_all_places.append({
                                    "id": place.id, 
                                    "title": place.title,
                                    "latitutde": place.latitude,
                                    "longitude": place.longitude
            })
        return list_all_places

    def update_place(self, place_id, place_data):
        """Update a place's information."""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")

        for key, value in place_data.items():
            if hasattr(place, key):
                setattr(place, key, value)

        if place.price < 0:
            raise ValueError("Price must be a non-negative number.")
        if not (-90 <= place.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= place.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        return {"message": "Place updated successfully!"}
    