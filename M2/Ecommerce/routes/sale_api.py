from flask import request, Response, jsonify, Blueprint
from repositories.sale_repo import SaleRepository, SaleCreationError, SaleRepositoryError, SaleNotFoundError
from auth.jwt_instance import jwt_instance
from auth.utils import token_required_admin, get_current_user

sale_routes = Blueprint("sale_routes", __name__)

sale_repo = SaleRepository()


@sale_routes.route('new-sale', methods=['POST'])
def create_sale():
    try:
        user = get_current_user()
        data = request.get_json()

        if not data or "billing_address" not in data:
            return jsonify({"error": "billing_address required"}), 400
        
        user_id = user["id"]
        address = data["billing_address"]

        sale = sale_repo.create_sale(user_id, address)

        return jsonify(sale), 201
    
    except SaleCreationError as e:
        return jsonify({"error": str(e)}), 400
    except SaleRepositoryError as e:
        return jsonify({"error": str(e)}), 500   
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@sale_routes.route('my-sales', methods=['GET'])
def get_my_sales():
    try: 
        user = get_current_user()
        sales = sale_repo.get_sales_by_user(user['id'])
        return jsonify(sales), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
    except SaleNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except SaleRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(e)
        return jsonify({"error": "Unexpected error"}), 500
    
@sale_routes.route('my-sales/<int:sale_id>', methods=['GET'])    
def get_my_sale(sale_id):
    try:
        user = get_current_user()
        sale = sale_repo.get_sale_by_id(user['id'], sale_id)
        return jsonify(sale), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
    except SaleNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except SaleRepositoryError as e:
        return jsonify({"error": str(e)}), 500

    
@sale_routes.route('/admin/<int:sale_id>', methods=['GET'])
@token_required_admin
def get_sale_admin(sale_id):
    try:
        sale = sale_repo.get_sale_by_id_admin(sale_id)
        return jsonify(sale), 200
    except SaleNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except SaleRepositoryError as e:
        return jsonify({"error": str(e)}), 500

@sale_routes.route('/admin/all-sales', methods=['GET'])
@token_required_admin
def get_all_sales_admin():
    try:
        sales = sale_repo.get_all_sales()
        return jsonify(sales), 200
    except SaleNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except SaleRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    
