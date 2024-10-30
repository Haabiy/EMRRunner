from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError
from app import config 

def validate_request(schema):
    """Decorator to validate request data against a schema."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                schema().load(request.json)
            except ValidationError as err:
                return jsonify({"error": "Invalid input", "details": err.messages}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_api_key(func):
    """Decorator to check for valid API key in request headers."""
    @wraps(func)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-Api-Key')
        if api_key and api_key == config.API_KEY_VALUE:
            return func(*args, **kwargs)
        return jsonify({'error': 'Unauthorized'}), 401
    return decorated
