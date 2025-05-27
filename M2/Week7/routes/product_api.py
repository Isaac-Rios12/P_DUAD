from flask import Flask, request, Response, jsonify, Blueprint
from auth.decorators import token_required_admin, validate_product_data
from db.db import Product_Manager

db_manager = Product_Manager()

product_routes  = Blueprint('product_routes', __name__)

@product_routes.route('/', methods=['GET'])
#@token_required_admin
def get_all_products():
    try:
        products = db_manager.get_all_products()
        if not products:
            return jsonify({"error": "No products found"}), 404
        else:
            return jsonify([dict(product._mapping) for product in products]), 200
        
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@product_routes.route('/register', methods=['POST'])
@token_required_admin
@validate_product_data
def register():
    try:
        data = request.get_json()
        result = db_manager.create_product(data.get('name'), data.get('price'), data.get('quantity'))
        product_id = result[0]

        return jsonify({"message": "Product created"}), 201
    
    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403

    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
    
@product_routes.route('/<int:product_id>', methods=['GET'])
@token_required_admin
def get_product(product_id):
    try:
        product = db_manager.get_product_by_id(product_id)
        if product:
            return jsonify(dict(product._mapping)), 200
        else:
            return jsonify({"error": "Product not found"}), 404
        
    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403
    
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
    
@product_routes.route('/<int:product_id>', methods=['PUT'])
@token_required_admin
@validate_product_data
def update_product(product_id):
    try:
        product = db_manager.get_product_by_id(product_id)
        if not product:
            return jsonify({"error": "Product not registered"})
        else:
            data = request.get_json()
            result = db_manager.update_product(product_id, data.get('name'), price=data.get('price'), quantity=data.get('quantity'))

            if result:
                return jsonify({"message": "Product updated"}), 200
            else:
                return jsonify({"error": "Product not updated"}), 400
    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403
            
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
    
@product_routes.route('/<int:product_id>', methods=['DELETE'])
@token_required_admin
def delete_product(product_id):
    try:
        product = db_manager.get_product_by_id(product_id)
        if not product:
            return jsonify({"error":"Product not registered"}), 404
               
        result = db_manager.delete_product(product_id)
        if result:
            return jsonify({"message": "Product deleted successfully"}),200
        else:
            return jsonify({"error": "Product not deleted"}), 400
        
    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403
    
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

        

