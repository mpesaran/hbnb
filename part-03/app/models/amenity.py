""" Amenity Model """

import uuid
from datetime import datetime
from app import db
from sqlalchemy.orm import validates


class Amenity(db.Model):
    """ Amenity class """
    __tablename__ = 'amenities'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now())

    @validates("name")
    def validates_name(self, key, value):
        """Validates the amenity name - though not neccasery, could be a Setter insted"""
        # ensure that the value is up to 50 characters after removing excess white-space
        is_valid_name = 0 < len(value.strip()) <= 50
        if is_valid_name:
            return value.strip()
        else:
            raise ValueError("Invalid name length!")

    def __init__(self, name):
        if name is None:
            raise ValueError("Required attributes not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name.strip()

    # --- Getters and Setters ---
    # @property
    # def name(self):
    #     """ Returns value of property name """
    #     return self._name

    # @validates("name")
    # def name(self, value):
    #     """Setter for prop name"""
    #     # ensure that the value is up to 50 characters after removing excess white-space
    #     is_valid_name = 0 < len(value.strip()) <= 50
    #     if is_valid_name:
    #         self._name = value.strip()
    #     else:
    #         raise ValueError("Invalid name length!")
        
    # @name.setter
    # def name(self, value):
    #     """Setter for prop name"""
    #     # ensure that the value is up to 50 characters after removing excess white-space
    #     is_valid_name = 0 < len(value.strip()) <= 50
    #     if is_valid_name:
    #         self._name = value.strip()
    #     else:
    #         raise ValueError("Invalid name length!")


    # --- Methods ---
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()
