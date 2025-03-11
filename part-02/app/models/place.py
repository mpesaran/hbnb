from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner, amenities=None):
        """Initialisation for Place instances"""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price 
        self.latitude = latitude 
        self.longitude = longitude
        self.owner = owner 
        self.reviews = []
        if amenities is not None:
            self.amenities = amenities
        else:
            self.amenities = []

    def add_review(self, review):
        """Adds a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Adds an amenity to the place."""
        self.amenities.append(amenity)
    
    
    # - - -Getters and setters here - - -
    @property
    def title(self):
        """Getter for title attribute"""
        return self._title
    
    @title.setter
    def title(self, value):
        """Setter for title attribute"""
        if value != None:
            self._title = value
        else:
            raise TypeError("ERROR: Title must not be empty")
        

    @property
    def description(self):
        """Getter for description attribute"""
        return self._description
    
    @description.setter
    def description(self, value):
        """Setter for description attribute"""
        self._description = value
        
    
    @property
    def price(self):
        """Getter for price attribute"""
        return self._price
    
    @price.setter
    def price(self, value):
        """Setter for price attribute"""
        if value <= 0 or not isinstance(value, (int, float)):
            raise ValueError("ERROR: Price must be a non-negative number.")
        self._price = value
        
    
    @property
    def latitude(self):
        """Getter for latitude attribute"""
        return self._latitude
        
    @latitude.setter
    def latitude(self, value):
        """Setter for latitude attribute"""
        if not isinstance(value, (int, float)):
            raise TypeError("ERROR: Latitude must be a number")
        if not (-90 <= value <= 90):
            raise ValueError("ERROR: Latitude must be between -90 and 90")
        self._latitude = value
    
    @property
    def longitude(self):
        """Getter for longitude attribute"""
        return self._longitude
        
    @longitude.setter
    def longitude(self, value):
        """Setter for longitude attribute"""
        if not isinstance(value, (int, float)):
            raise TypeError("ERROR: Longitude must be a number")
        if not (-180 <= value <= 180):
            raise ValueError("ERROR: Longitude must be between -180 and 180")
        self._longitude = value
        

    @property
    def owner(self):
        """Getter for owner attribute"""
        return self._owner
    
    @owner.setter
    def owner(self, value):
        """Setter for owner attribute"""
        self._owner = value  
    
    # adding a ownerID property derived from owner object
    @property
    def owner_id(self):
        if self._owner:
            return self.owner.id
        return None

    def to_dict(self):
        place_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner,
            "amenities": self.amenities
        }
        return place_dict