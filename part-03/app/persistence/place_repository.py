from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_place_by_title(self, title):
        """Get a place by its title."""
        return self.model.query.filter_by(title=title).first()

    def place_exists(self, place_id):
        """Check if a place exists by its ID."""
        return self.model.query.filter_by(id=place_id).first() is not None
