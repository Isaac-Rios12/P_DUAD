from flask import Flask, request, Response, jsonify, Blueprint
from auth.decorators import token_required_admin, validate_product_data
from db.db import Product_Manager
from caching.cache import cache_manager
import json

db_manager = Product_Manager()


product_routes  = Blueprint('product_routes', __name__)

@product_routes.route('/', methods=['GET'])

def get_all_products():
    try:
        cache_key = "getProducts:all"

        cached_products = cache_manager.get_data(cache_key)
        if cached_products:
            print("Productos obtenidos desde redis...")
            return jsonify(json.loads(cached_products)), 200
        
        products = db_manager.get_all_products()
        if not products:
            return jsonify({"error": "No products found"}), 404
        else:
            products_list = [dict(product._mapping) for product in products]
            
            cache_manager.store_data(cache_key, json.dumps(products_list, default=str))

            print("Obtenidos desde la bd...")
            return jsonify(products_list), 200
        
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

        cache_manager.delete_data("getProducts:all")

        return jsonify({"message": "Product created"}), 201
    
    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403

    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
    
@product_routes.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        #redis
        cache_key = f"product:{product_id}"

        cached_product = cache_manager.get_data(cache_key)
        if cached_product:
            print("Data obteniidad desde Redis")
            return jsonify(json.loads(cached_product)), 200
        

        product = db_manager.get_product_by_id(product_id)

        if product:
            product_dict = dict(product._mapping)

            
            cache_manager.store_data(cache_key, json.dumps(product_dict, default=str))

            return jsonify(product_dict), 200
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
            return jsonify({"error": "Product not registered"}), 404
        else:
            data = request.get_json()
            result = db_manager.update_product(product_id, data.get('name'), price=data.get('price'), quantity=data.get('quantity'))

            if result:
                cache_manager.delete_data(f"product:{product_id}")
                cache_manager.delete_data("getProducts:all")
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
            cache_manager.delete_data(f"product:{product_id}")
            cache_manager.delete_data("getProducts:all")
            return jsonify({"message": "Product deleted successfully"}),200
        else:
            return jsonify({"error": "Product not deleted"}), 400
        
    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403
    
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

        

