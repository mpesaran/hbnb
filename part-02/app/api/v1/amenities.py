from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
})

def validate_amenity(self):
    if not isinstance(self['name'], str) or not self['name'].strip():
        raise ValueError("Amenity name must be a non-empty string")
    
    self['name'] = self['name'].strip()
    return self

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        # Placeholder for the logic to register a new amenity
        all_amenities = facade.get_all_amenities()
        existing_amenity = any(a.name == amenity_data["name"] for a in all_amenities)

        if existing_amenity:
            return {'error': 'Amenity already exists'}, 400
        
        try:
            amenity_validated = validate_amenity(amenity_data)
            new_amenity = facade.create_amenity(amenity_validated)

            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        # Placeholder for logic to return a list of all amenities
        if not amenities:
            return {'error': 'Amenities not found'}, 404
        return [{'id': a.id, 'name': a.name} for a in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        # Placeholder for the logic to retrieve an amenity by ID
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload
        # Placeholder for the logic to update an amenity by ID
        if not amenity_data:
            return {'error': 'Invalid input data'}, 400
        
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)

            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404

            return {
              "id": updated_amenity.id,
              "name": updated_amenity.name
            }, 200     
        except ValueError:
            return {"error": "Failed to update amenity"}, 500 