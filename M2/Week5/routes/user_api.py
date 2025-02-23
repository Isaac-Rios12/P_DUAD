from flask.views import MethodView
from flask import Flask, jsonify, request, Blueprint
from services.user_service import UserManager

user_blueprint = Blueprint('user_blueprint', __name__)

class UserListAPI(MethodView):

    def __init__(self):
        self.user_instance = UserManager()

    def get(self):
        try:
            filters = request.args.to_dict()
            users = self.user_instance.filter_user(filters) if filters else self.user_instance.get_all_users()

            if users:
                return jsonify(users), 200
            return jsonify({"Error": "No users found"}), 404
        except Exception as e:
            return jsonify({"Error": str(e)}), 500
    
    def post(self):
        try:
            required_fields = ["name", "email", "username", "password", "birth_date", "status"]

            for field in required_fields:
                if field not in request.json:
                    return jsonify({"error": f"{field} is required"}), 400
            new_status = request.json['status'].lower()
            check_status = self.user_instance.verify_status(new_status)

            if check_status:
                return {"error": check_status}, 400
            
            new_user = self.user_instance.create_user(
                request.json["name"],
                request.json["email"],
                request.json["username"],
                request.json["password"],
                request.json["birth_date"],
                new_status
            )

            if "error" in new_user:
                return jsonify(new_user), 400 
            
            return jsonify(new_user), 201
        
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
        
class UserDetailAPI(MethodView):

    def __init__(self):
        self.user_instance = UserManager()

    def get(self, user_id):
        try:
            user = self.user_instance.get_user_by_id(user_id)
            if user:
                return jsonify(user), 200
            return jsonify({"Error": "Not user found with the given criteria"})
        except Exception as e:
            return jsonify({"error": str({e})}), 400
    
    def patch(self, user_id):

        try:

            user = self.user_instance.get_user_by_id(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            new_status = request.json.get("status").lower() if request.json.get("status") else None

            if not new_status:
                return jsonify({"error": "status is required"}), 400
            
            check_status = self.user_instance.verify_status(new_status)

            if check_status:
                return {"error": check_status}, 400

            change_status = self.user_instance.modify_user_status(user_id, new_status)
            return jsonify({"message": change_status}), 200

        except Exception as e:
            return jsonify({"error": str({e})}), 400
        

user_blueprint.add_url_rule('/users', view_func=UserListAPI.as_view('users_list'), methods=['GET', 'POST'])
user_blueprint.add_url_rule('/users/<int:user_id>', view_func=UserDetailAPI.as_view('user_detail'), methods=['GET','PATCH'])
            
        
        
        
        
