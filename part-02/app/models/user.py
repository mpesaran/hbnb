import re
from app.models.base_model import BaseModel

class User(BaseModel):

	def __init__(self, first_name, last_name, email, is_admin=False):
		super().__init__()
		if len(first_name) > 50 or len(last_name) > 50:
			raise ValueError("First name and last name must be less than 50 characters.")
		if "@" not in email and "." not in email:
			raise ValueError("Invalid email format.")
		self.first_name = first_name
		self.last_name = last_name
		self.email = email
		self.is_admin = is_admin
		self.places = []
		self.reviews=[]

	# - - -Getters and setters here - - -
	@property
	def first_name(self):
		return self._first_name

	@first_name.setter
	def first_name(self, value):
		if not value:
			raise ValueError("First name cannot be empty.")
		if not 0 < len(value.strip()) < 50:
			raise ValueError("First name must be less than 50 characters.")
		self._first_name = value.strip()

	@property
	def last_name(self):
		return self._last_name

	@last_name.setter
	def last_name(self, value):
		if not value:
			raise ValueError("Last name cannot be empty.")
		if not 0 < len(value.strip()) < 50:
			raise ValueError("Last name must be less than 50 characters.")
		self._last_name = value.strip()

	@property
	def email(self):
		return self._email

	@staticmethod
	def is_valid_email(email):
		"""Validate the format of an email address using regex."""
		regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
		return re.match(regex, email) is not None

	@email.setter
	def email(self, value):
		cleaned_email = re.sub(r'\s+', '', value).lower()
		if not self.is_valid_email(cleaned_email):
			raise ValueError("Invalid email format.")
		self._email = cleaned_email

	def add_place(self, place):
		"""Add a place to the user's list of places."""
		self.places.append(place)

	def add_review(self, review):
		"""Add a review to the user's list of reviews."""
		self.reviews.append(review)
