# app/decorators.py
from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError
from app import config 

def validate_request(schema_class):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"error": "Invalid input", "details": "Request must be JSON"}), 400
            
            schema = schema_class()
            json_data = request.get_json()
            print(f"Received data: {json_data}")  # Debug print
            
            try:
                validated_data = schema.load(json_data)
                print(f"Validated data: {validated_data}")  # Debug print
                request.validated_data = validated_data
                return f(*args, **kwargs)
            except ValidationError as err:
                print(f"Validation error: {err.messages}")  # Debug print
                return jsonify({"error": "Invalid input", "details": err.messages}), 400
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