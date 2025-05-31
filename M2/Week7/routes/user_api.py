from flask import Flask, request, Response, jsonify, Blueprint
from db.db import User_Manager
from auth.jwt_instance import jwt_manager
from auth.decorators import token_required_admin
from auth.current_user import get_current_user
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError


user_routes = Blueprint('user_routes', __name__)


db_manager = User_Manager()
          

@user_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
      
        if(data.get('username') == None or data.get('password') == None):
            return jsonify({"error": "user or password not found"}), 400
        else:
            role = 'user'
            result = db_manager.insert_user(data.get('username'), data.get('password'), role=role)
            user_id = result[0]

            print(result)

            token = jwt_manager.encode({'id':user_id})
            return jsonify(token=token)
        
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            return jsonify({"error": "Username already exists"}), 400
        else:
            print("database integirty error: ", e)
            return jsonify({"error": "database integrity error"}), 500
        
    except PermissionError as e:
        print("Permission error:", e)
        return jsonify({"error": "You do not have permission to perform this operation"}), 403
    
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
    
@user_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if(data.get('username') == None or data.get('password')== None):
            return jsonify({"error": "user or password not found"}), 400
        else:
            result = db_manager.get_user(data.get('username'), data.get('password'))

            if result == None:
                return jsonify({"error": "User not registered."}), 403
            else:
                user_id = result[0]
                role = result[3]
                token = jwt_manager.encode({'id': user_id, 'role': role})

                return jsonify(token=token)
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
        
@user_routes.route('/me')
def me():
    try:
        user = get_current_user()
        return jsonify(id=user[0], username=user[1]), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500
    
@user_routes.route('/promote', methods=['POST'])
@token_required_admin
def promote_user():
    try:

        data = request.get_json()
        username = data.get("username")

        if not username:
            return jsonify({"error": "Username is required"}), 400
        
        result = db_manager.update_user_role(username)

        if result:
            return jsonify({"message": "User promoted to admin"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
        
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500


    