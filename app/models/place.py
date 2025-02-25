from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price 
        self.latitude = latitude 
        self.longitude = longitude
        self.owner = owner 
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities


    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
    
    
    # property setters to raise corresponding exceptions for invalid values
    @price.setter
    def price(self, value):
        if value >= 0 and value.isdigit():
            self.price = value
        else:
            return "Error: Price must be a non-negative number"
        
    @latitude.setter
    def latitude(self, value):
        if value.isdigit():
            if value <= 90 and value >= -90:
                self.latitude = value
        else:
            return "Error: Latitude must be between -90 and 90"
        
    @longitude.setter
    def longitude(self, value):
        if value.isdigit():
            if value <= 180 and value >= -180:
                self.longitude = value
        else:
            return "Error: Longitude must be between -180 and 180"
