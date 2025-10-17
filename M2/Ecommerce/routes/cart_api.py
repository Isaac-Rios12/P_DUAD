from flask import request, jsonify, Blueprint
from repositories.cart_repo import CartRepository, ItemNotInCartError, ProductNotFoundError, InsufficientStockError, InvalidCartIdentifierError, CartCreationError, CartRepositoryError, CartNotFoundError

from auth.jwt_instance import jwt_instance
from auth.utils import get_current_user


cart_routes = Blueprint("cart_routes", __name__)

cart_repo = CartRepository()

@cart_routes.route('/', methods=['GET'])
def get_cart():
    
    try:
        user = get_current_user()
        
        cart = cart_repo.get_or_create_cart_by_user(user['id'])
        return jsonify(cart), 200
    except (CartNotFoundError, InvalidCartIdentifierError) as e:
        return jsonify({"error": str(e)}), 404
    except CartRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error"}), 500

@cart_routes.route('/delete', methods=['DELETE'])
def delete_cart():
    try:
        user = get_current_user()
        cart_repo.delete_cart_by_user(user['id'])
        return jsonify({"message": "Cart deleted successfully"}), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
    except CartNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except CartRepositoryError as e:
        return jsonify({"error": str(e)}), 500

@cart_routes.route('/add-items', methods=['POST'])
def add_item_to_cart():
    try:
        user = get_current_user()
        data = request.get_json()

        if not data or "items" not in data:
            return jsonify({"error": "Items are required"}), 400
        
        items = data["items"]
        cart = cart_repo.add_items_to_user_cart(user['id'], items)

        return jsonify(cart), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
    except InsufficientStockError as e:
        return jsonify({"error": str(e)}), 400
    except ProductNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except CartRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@cart_routes.route('/delete-item/<int:product_id>', methods=['DELETE'])
def delete_item_from_cart(product_id):
    try:
        user = get_current_user()

        cart = cart_repo.remove_item_from_user_cart(user['id'], product_id)
        return jsonify(cart), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
    except CartNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except ItemNotInCartError as e:
        return jsonify({"error": str(e)}), 404
    except CartRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
@cart_routes.route('/update-quantity/<int:product_id>', methods=['PATCH'])
def update_item_quantity(product_id):
    try:
        user = get_current_user()
        
        data = request.get_json()
        if not data or "new_quantity" not in data:
            return jsonify({"error": "new_quantity is required"}), 400
        
        new_quantity = data["new_quantity"]
        cart = cart_repo.update_item_quantity_in_user_cart(user["id"], product_id, new_quantity)
        return jsonify(cart), 200
    
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
    except InsufficientStockError as e:
        return jsonify({"error": str(e)}), 400
    except ItemNotInCartError as e:
        return jsonify({"error": str(e)}), 404
    except CartRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500
