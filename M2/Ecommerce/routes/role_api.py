from flask import Flask, request, Response, jsonify, Blueprint
from repositories.role_repo import RoleRepository, RoleCreationError, RoleNotFoundError, RoleRepositoryError
from auth.jwt_instance import jwt_instance
from auth.utils import token_required_admin, get_current_user

role_routes = Blueprint("role_routes", __name__)

role_repo = RoleRepository()

@role_routes.route('/add', methods=['POST'])
@token_required_admin
def add_role():
    try:
        data = request.get_json()

        role_name = data.get("name")
        if not role_name:
            return jsonify({"error": "Role name not given"}), 400
        
        new_role = role_repo.create_role(role_name)
        return jsonify({"message": "Role created", "role": new_role}), 201

    except RoleCreationError as e:
        return jsonify({"error": str(e)}), 500
    except RoleRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal error"}), 500

@role_routes.route('/all-roles', methods=['GET'])   
@token_required_admin
def get_all_roles():
    try:
        all_roles = role_repo.get_all_roles()
        return jsonify({"roles": all_roles}), 200
    except RoleNotFoundError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve roles {str(e)}"}), 500


@role_routes.route('/<string:name>', methods=['GET'])
@token_required_admin
def get_role_by_name(name):
    try:
        role = role_repo.get_role_by_name(name)
        if not role:
            return jsonify({"error": f"Role '{name}' not found"}), 404

        return jsonify(role), 200
    except RoleNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except RoleRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
@role_routes.route('/<int:role_id>', methods=['PUT'])
@token_required_admin
def update_role_endpoint(role_id):
    try:
        data = request.get_json()
        new_name = data.get("new_name")
        if not new_name:
            return jsonify({"error": "new_name is required"}), 400

        updated_role = role_repo.update_role(role_id, new_name)
        return jsonify(updated_role), 200

    except RoleNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except RoleRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
@role_routes.route('/<int:role_id>', methods=['DELETE'])
@token_required_admin
def delete_role_endpoint(role_id):
    try:
        role_repo.delete_role(role_id)
        return jsonify({"message": f"Role with ID {role_id} deleted successfully"}), 200

    except RoleNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except RoleRepositoryError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500