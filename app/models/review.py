from app.models.base_model import BaseModel

class Review(BaseModel):

	def __init__(self, text, rating, place, user):
		super().__init__()
		self.text = text 
		self.rating = rating
		self.place = place
		self.user = user

	def to_dict(self):
		"""Convert Review object to dictionary for API response"""
		return {
			"id": self.id,
			"text": self.text,
			"rating": self.rating,
			"place_id": self.place.id if self.place else None,
			"user_id": self.user.id if self.user else None,
			"created_at": self.created_at.isoformat(),
			"updated_at": self.updated_at.isoformat(),
		}
