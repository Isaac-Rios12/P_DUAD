from flask import request, Response
from functools import wraps
from auth.jwt_instance import jwt_manager
from flask import request, jsonify

jwt_manager = jwt_manager

def validate_product_data(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request must be JSON"}), 400
        
        name = data['name']
        if not isinstance(name, str) or not name.strip():
            return jsonify({"error": "Name must be a non-empty string"}), 400
        if len(name.strip()) < 2:
            return jsonify({"error": "Name must be at least 2 characters"}), 400
        
        quantity = data['quantity']
        if not isinstance(quantity, int):
            return jsonify({"error": "Quantity must br an integer"}), 400
        if quantity < 0:
            return jsonify({"error": "Quantity cannot be negative"}), 400
        
        price = data['price']
        if not isinstance(price, (int, float)):
            return jsonify({"error": "Price must be a number"}), 400
        if price <= 0:
            return jsonify({"error": "Price must be positive"}), 400
            
        return f(*args, **kwargs)
    return decorator


def token_required_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return Response("Token is missing", status=403)
        
        try:
            decoded = jwt_manager.decode(token)
            if not decoded:
                return Response("Token is invalid",status=403)
            if decoded.get('role') != 'admin':
                return Response("You need to be a admin", status=403)
            
        except Exception as e:
            return Response("Token invalid o expired", status=403)
        
        return f(*args, **kwargs)
    return decorator
        
            