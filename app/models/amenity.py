BaseModel = __import__('base_model').BaseModel

class Amenity(BaseModel):

	def __init__(self, name):
		super().__init__()
		self.name = name