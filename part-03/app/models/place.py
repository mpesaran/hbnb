import uuid
from datetime import datetime
from app.models.user import User
from app import db
from sqlalchemy.orm import validates


class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        if title is None or description is None or price is None or latitude is None or longitude is None or owner_id is None:
            raise ValueError("Required attributes not specified!")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        # self.reviews = []  # relationship - List to store related reviews
        # self.amenities = []  # relationship - List to store related amenities

     # --- Validators ---
    @validates("title")
    def validate_title(self, key, value):
        value = value.strip()
        if not 1 <= len(value) <= 100:
            raise ValueError("Title must be a non-empty string with max length 100.")
        return value
    
    @validates("price")
    def validate_price(self, key, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Invalid value specified for price")
        return float(value)

    @validates("latitude")
    def validate_latitude(self, key, value):
        if not isinstance(value, (int, float)) or not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        return float(value)
        
    @validates("longitude")
    def validate_longitude(self, key, value):
        if not isinstance (value, (int, float)) or not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        return float(value)



    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    # def add_review(self, review):
    #     """Add a review to the place."""
    #     self.reviews.append(review)

    # def add_amenity(self, amenity):
    #     """Add an amenity to the place."""
    #     self.amenities.append(amenity)

    @staticmethod
    def place_exists(place_id):
        """ Search through all Places to ensure the specified place_id exists """
        # Unused - the facade get_place method will handle this
