from auth.decorators import token_required_admin
from db.db import Purchase_Manager, User_Manager
from flask import Blueprint, Response, request, jsonify
from auth.current_user import get_current_user

user_manager = User_Manager()
db_manager = Purchase_Manager()
purchase_routes = Blueprint('purchase_routes', __name__)

@purchase_routes.route('/', methods=['POST'])
def purchase_products():
    try:
        
        user = get_current_user()
        data = request.get_json()

        if not data or not isinstance(data, list):
            return jsonify({"error": "A list of products is required"}), 400 
        
        purchase_result = db_manager.make_purchase(user[0], data)
        return jsonify(purchase_result), 201
    
    except ValueError as e:
        return jsonify({"error":str(e)})

    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@purchase_routes.route('/my-purchases', methods=['GET'])
def get_my_purchases():
    try:
        user = get_current_user()
        get_purchases = db_manager.get_invoices_by_user(user[0])
        return jsonify(get_purchases), 200
    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@purchase_routes.route('/user/<int:user_id>', methods=['GET'])
@token_required_admin
def get_user_purchases(user_id):
    try:
        exists_user = user_manager.get_user_by_id(user_id)
        if not exists_user:
            return jsonify({"error": "User not found"}), 404
        
        purchases = db_manager.get_invoices_by_user(user_id)

        if not purchases:
            return jsonify({"message": "No invoices found for this user"}), 404
        return jsonify(purchases), 200
    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

