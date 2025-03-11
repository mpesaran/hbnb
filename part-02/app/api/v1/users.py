from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Attempt to create a new user and handle any validation errors
        try:
            new_user = facade.create_user(user_data)
        except ValueError as error:
            return {'error': f'setter validation failure: {error}'}, 400

        # Return newly created user details with a success message
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'message': 'user created successfully'
            }, 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve the list of users"""
        users = facade.get_all_users()
        user_list = [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            } for user in users
        ]
        return user_list, 200  # Return the list of users

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }, 200  # Return user details

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid user input')
    def put(self, user_id):
        """Update user details"""
        update_data = api.payload
        try:
            updated_user = facade.update_user(user_id, update_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200  # Return updated user details
        except ValueError as e:
            return{'error': str(e)}, 400  # Return error message for invalid input
