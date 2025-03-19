from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from app import db

# Association table: many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
  Column('place_id', db.String(36), ForeignKey('places.id'), primary_key=True),
  Column('amenity_id', db.String(36), ForeignKey('amenities.id'), primary_key=True)
)