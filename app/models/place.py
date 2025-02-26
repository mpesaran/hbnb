from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        """Initialisation for Place instances"""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price 
        self.latitude = latitude 
        self.longitude = longitude
        self.owner = owner 
        self.reviews = []
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
        self._title = value
        

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
        if value >= 0 and value.isdigit():
            self._price = value
        else:
            return "Error: Price must be a non-negative number"
        
    
    @property
    def latitude(self):
        """Getter for latitude attribute"""
        return self._latitude
        
    @latitude.setter
    def latitude(self, value):
        """Setter for latitude attribute"""
        if not value.isdigit():
            raise TypeError("ERROR: Latitude must be a number")
        if not -180 >= value <= 180:
            raise ValueError("ERROR: Latitude must be between -180 and 180")
        self._latitude = value
    
    @property
    def longitude(self):
        """Getter for longitude attribute"""
        return self._longitude
        
    @longitude.setter
    def longitude(self, value):
        """Setter for longitude attribute"""
        if not value.isdigit():
            raise TypeError("ERROR: Longitude must be a number")
        if not -180 >= value <= 180:
            raise ValueError("ERROR: Longitude must be between -180 and 180")
        self._longitude = value
        

    @property
    def owner(self):
        """Getter for owner attribute"""
        return self._owner
    
    @owner.setter
    def description(self, value):
        """Setter for owner attribute"""
        self._owner = value  
