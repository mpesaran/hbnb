from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.places import api as places_ns



def create_app(test_config=None):
    app = Flask(__name__)
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',  # Replace with a more secure key in production
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///:memory:',  # In-memory DB for testing
        TESTING=True,  # Enable Flask's testing mode
    )

    if test_config:
        # Load the provided test config (if any)
        app.config.from_mapping(test_config)
    
    
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')

    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    api.add_namespace(places_ns,  path='/api/v1/places')

    return app