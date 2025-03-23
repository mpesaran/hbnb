from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.user_repository import UserRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.place_repository import PlaceRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = AmenityRepository()


    # --- Users ---
    def create_user(self, user_data):
        if self.user_repo.email_exists(user_data['email']):
            raise ValueError("Email already exists")

        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)


    # --- Amenities ---
    # Used during record insertion to prevent duplicate amenities
    def get_amenity_by_name(self, name):
        return self.amenity_repository.get_by_attribute('name', name)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repository.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repository.update(amenity_id, amenity_data)


    # --- Places ---
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        self.place_repo.update(place_id, place_data)


    # --- Reviews ---
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repository.get(review_id)

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repository.get_by_attribute('place_id', place_id)

    def get_reviews_by_rating(self, rating):
        return self.review_repository.get_reviews_by_rating(rating)

    def update_review(self, review_id, review_data):
        self.review_repository.update(review_id, review_data)

    def delete_review(self, review_id):
        self.review_repository.delete(review_id)

    # --- Place and Amenity ---
    def add_amenity_to_place(self, place_id, amenity_id):
        place = self.get_place(place_id)
        amenity = self.amenity_repository.get(amenity_id)
        if not place:
            raise ValueError("Place not found")
        if not amenity:
            raise ValueError("Amenity not found")
        
        place.add_amenity(amenity)


    # # --- Place and Review ---
    # def get_review_by_place(self, place_id):
    #     place = self.get_place(place_id)
    #     if not place:
    #         raise ValueError("Place not found")
    #     return place.reviews_r