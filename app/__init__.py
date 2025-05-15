"""
Flask application factory.
"""
from flask import Flask
from app.api import api_bp

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=True
    )
    
    if test_config:
        # Load test config if passed
        app.config.from_mapping(test_config)
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    # Simple index route
    @app.route('/')
    def index():
        return {
            "message": "Inventory Management System API",
            "endpoints": {
                "GET /inventory": "Fetch all items",
                "GET /inventory/<id>": "Fetch a specific item",
                "POST /inventory": "Create a new item",
                "PATCH /inventory/<id>": "Update an item",
                "DELETE /inventory/<id>": "Delete an item",
                "GET /lookup/barcode/<barcode>": "Lookup product by barcode",
                "GET /lookup/name/<name>": "Search products by name"
            }
        }
    
    return app