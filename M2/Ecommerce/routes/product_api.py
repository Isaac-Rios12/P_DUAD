from flask import Flask, request, Response, jsonify, Blueprint
from repositories.product_repo import ProductRepositoryError, ProductRepository, ProductNotFoundError, ProductCreationError
from auth.utils import token_required_admin
from caching.cache import cache_manager
product_routes = Blueprint("product_routes", __name__)
import json

product_repo = ProductRepository()

@product_routes.route('/all-products', methods=['GET'])
def get_all_products():
    try:
        cache_key = "products:all"
        cached_data = cache_manager.get_data(cache_key)
        if cached_data:
            print("desde redis.............")
            return jsonify({"products": json.loads(cached_data)}), 200
        
        products = product_repo.get_all_products()
        if not products:
            return jsonify({'error': "No products found"}), 404
        
        cache_manager.store_data(cache_key, json.dumps(products), time_to_live=300)
        return jsonify({"products": products}), 200
    
    except ProductNotFoundError as e:
        print(e)
        return jsonify({"Message": "No products found"}), 404
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal Error"}), 500
    
@product_routes.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        cache_key = f"product:{product_id}"
        cached_data = cache_manager.get_data(cache_key)

        if cached_data:
            return jsonify({"Product": json.loads(cached_data)}), 200
        
        product = product_repo.get_product_by_id(product_id)
        if not product:
            return jsonify({'error': "No products found"}), 404
        
        cache_manager.store_data(cache_key, json.dumps(product), time_to_live=300)

        return jsonify({"Product": product}), 200

    except ProductNotFoundError as e:
        print(e)
        return jsonify({"error": str(e)}), 404
    except Exception as j:
        print(j)
        return jsonify({"error": "Internal error"}), 500

@product_routes.route('/register', methods=['POST'])
@token_required_admin
def register_product():
    data = request.get_json()

    required_fields = ["name", "description", "price", "stock"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({"Error": f"Missing data: {', '.join(missing_fields)}"}), 400
    
    try:
        price = float(data.get("price"))
        stock = int(data.get("stock"))
        if price < 0 or stock < 0:
            return jsonify({"error": "Price and stock must be positive"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Price must be a number and stock an integer"}), 400
    
    try:
        new_product = product_repo.create_product(
            name=data["name"],
            description=data["description"],
            price=price,
            stock=stock
        )

        cache_manager.delete_data("products:all")
        cache_manager.delete_data_with_pattern("products:search:*")
        return jsonify({"New product": new_product}), 201
    except ProductCreationError as e:
        print(e)
        return jsonify({"Message": "Error creating the product"}), 400
    except Exception as j:
        print(j)
        return jsonify({"Message": "Internal Error"}), 500
    
@product_routes.route('/delete/<int:product_id>', methods=['DELETE'])
@token_required_admin  
def delete_product(product_id):
    try:
        delete_product = product_repo.delete_product(product_id)

        cache_manager.delete_data("products:all")
        cache_manager.delete_data(f"product:{product_id}")
        cache_manager.delete_data_with_pattern("products:search:*")

        return jsonify({"message": f"Product with ID {product_id} deleted"}), 200
    except ProductNotFoundError as e:
        print(e)
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except ProductRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    
@product_routes.route('/update-price/<int:product_id>', methods=['PUT'])
@token_required_admin 
def update_product_price(product_id):
    try:
        data = request.get_json()
        
        if not data or "new_price" not in data:
            return jsonify({"error":"new_price is required"}), 400
        new_price = data["new_price"]

        if not isinstance(new_price, (int,float)):
            return jsonify({"error": "New price must be a float number"}), 400
        if new_price <= 0:
            return jsonify({"error": "New price must be positive"}), 400
        update_product_price = product_repo.update_product_price(product_id, new_price)

        cache_manager.delete_data(f"product:{product_id}")
        cache_manager.delete_data("products:all")
        cache_manager.delete_data_with_pattern("products:search:*")

        return jsonify({"message": f"product {product_id} price updated succesfully",
                         "product": update_product_price
                         }), 200
     
    except ProductNotFoundError as e:
        print(e)
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)})
    except ProductRepositoryError as e:
        return jsonify({"error": str(e)}), 500
         

@product_routes.route('/', methods=['GET'])
def get_products_by_name():
    try:
        name = request.args.get('name')
        if name:
            cache_key = f"products:search:{name}"
            cached_data = cache_manager.get_data(cache_key)
            if cached_data:
                return jsonify(json.loads(cached_data)), 200
            
            product = product_repo.get_products_by_name(name)
            if not product:
                return jsonify({"message": "No product found with that name"}), 404
            
            cache_manager.store_data(cache_key, json.dumps(product), time_to_live=120)
            return jsonify(product), 200
    except ProductNotFoundError as e:
        print(e)
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)})
    except ProductRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    