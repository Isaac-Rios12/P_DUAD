from auth.decorators import token_required_admin
from db.db import Purchase_Manager
from flask import Blueprint, Response, request, jsonify
from auth.current_user import get_current_user

db_manager = Purchase_Manager()
purchase_routes = Blueprint('purchase_routes', __name__)

@purchase_routes.route('/', methods=['POST'])
def purchase_products():
    try:
        
        user = get_current_user()
        data = request.get_json()

        if not data or not isinstance(data, list):
            return jsonify({"error": "Se requiere una lista de productos"}), 400
        
        purchase_result = db_manager.make_purchase(user[0],data)
        return jsonify(purchase_result), 201

    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error": "Ocurrió un error interno...", "details": str(e)}), 500

@purchase_routes.route('/my-purchases', methods=['GET'])
def get_my_purchases():
    try:
        user = get_current_user()
        get_purchases = db_manager.get_invoices_by_user(user[0])
        return jsonify(get_purchases), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error":str(e)}), 500

