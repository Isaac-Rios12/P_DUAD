from flask import Flask, request, Response, jsonify, Blueprint
from repositories.user_repo import UserRepository, UserCreationError, UserNotFoundError, UserRepositoryError
from repositories.role_repo import RoleRepository
from auth.jwt_instance import jwt_instance
from auth.utils import token_required_admin, get_current_user

user_routes = Blueprint("user_routes", __name__)

user_repo = UserRepository()
role_repo = RoleRepository()


@user_routes.route('/me')
def me():
    try:
        user = get_current_user()  # devuelve un dict: {"id": ..., "fullname": ...}
        return jsonify(id=user["id"], fullname=user["fullname"]), 200
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        print(f"Internal error: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@user_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ["fullname", "nickname", "email", "password"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing data: {', '.join(missing_fields)}"}), 400
    
    role_name = "user"
    role = role_repo.get_role_by_name(role_name)

    if role is None:
        return jsonify({"error": f"Role '{role_name}' not found"}), 500

    try:
        new_user = user_repo.create_user(
            fullname=data["fullname"],
            nickname=data['nickname'],
            email=data['email'],
            password=data['password'],
            role_id=role["id"]
        )
        user_id = new_user["id"]
        role = new_user["role_name"]

        token = jwt_instance.encode({'id': user_id, "role": role})

        return jsonify({
            "message": "User registered successfully",
            "user": {
                "id": new_user["id"],
                "fullname": new_user["fullname"],
                "nickname": new_user["nickname"],
                "email": new_user["email"],
                "role": role
            },
            "token": token
        }), 201
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except UserRepositoryError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # log interno
        print(f"Unexpected error: {e}")
        # respuesta genérica al cliente
        return jsonify({"error": "Internal server error"}), 500
    

@user_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if(data.get('nickname') == None or data.get('password') == None):
            return jsonify({"error": "nickname or password not found"}), 400
        else:
            result = user_repo.get_user_for_login(data.get('nickname'), data.get("password"))

            if result == None:
                return jsonify({"error": "Invalid nickname or password"}), 406
            else:
                user_id = result["id"]
                print(result["role_name"])
                role = result["role_name"]
                token = jwt_instance.encode({'id': user_id, 'role': role})
                return jsonify(token=token)
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except UserRepositoryError as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
       
        print(f"Unexpected error: {e}")
        
        return jsonify({"error": "Internal server error"}), 500
    
@user_routes.route('/update', methods=['PATCH'])
def update_user():
    try:
        user = get_current_user()
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401
     
    user_id = user["id"]
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is missing"}), 400
        
    required_fields = ["email", "password"]
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify({"error": f"Missing data: {', '.join(missing_fields)}"}), 400
    
    try:
        updated_user = user_repo.update_user(
            user_id=user_id,
            email=data["email"],
            password=data["password"]
        )
        return jsonify({"message": "User updated successfully", "user": updated_user}), 200
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@user_routes.route('/<int:user_id>', methods=['GET'])
@token_required_admin
def get_user_by_admin(user_id):
    try:
        user = user_repo.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({"User": user}), 200
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_routes.route('/all-users', methods=['GET'])
@token_required_admin
def get_all_users():
    try:
        all_users = user_repo.get_all_users()
        if not all_users:
            return jsonify({"Error": "No users found"}), 404
        return jsonify(all_users), 200
    except UserNotFoundError as e:
        print(e)
        return jsonify({"error": "no users"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Interal Error"})
    
