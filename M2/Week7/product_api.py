#   debo empezar aca definiendo todo lo necesario de aca
from flask import Flask, request, Response, jsonify, Blueprint
from auth.decorators import token_required_admin
from db import Product_Manager

db_manager = Product_Manager()

product_routes  = Blueprint('product_routes', __name__)

@product_routes.route('/register', methods=['POST'])
@token_required_admin
def register():
    try:
        data = request.get_json()

        if data.get('name') == None or data.get('price') == None or data.get('quantity') == None: #or data.get('quantity') <= 0#
            return Response(status=400)
        else:
            result = db_manager.create_product(data.get('name'), data.get('price'), data.get('quantity'))
            product_id = result[0]

            print(product_id)

            return jsonify("Created"), 200

    except Exception as e:
        return jsonify(error=str(e)), 500
    
@product_routes.route('/<int:product_id>', methods=['GET'])
@token_required_admin
def get_product(product_id):
    try:
        product = db_manager.get_product_by_id(product_id)  # <--- Aquí los paréntesis son clave
        if product:
            return jsonify(dict(product._mapping)), 200
        else:
            return jsonify({"error": "Not founded"}), 404
    except Exception as e:
        return jsonify(error=str(e)), 500
    
    #quedo aca, lo ultimo que hice fue hacer este get producto

#validad si existe ya, y buscar como manejjar el caso de agregar mas al mismo....#
#def check

