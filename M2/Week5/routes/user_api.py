from flask.views import MethodView
from flask import Flask, jsonify, request, Blueprint
from services.user_service import UserManager


class UserAPI(MethodView):

    def __init__(self):
        self.user_instance = UserManager()

    def get(self):
        try:
            filters = request.args.to_dict()
            if not filters:
                data = self.user_instance.get_users()
                return jsonify(data), 200
            
            user = self.user_instance.filter_user(filters)
            if user:  
                return jsonify(user), 200
            else:  
                return jsonify({"error": "No vehicle found with the given criteria"}), 404
            
        except Exception as e:
            return jsonify({"error": str({e})}), 400
        

    def post(self):
        try:
            required_fields = ["name", "email", "username", "password", "birth_date", "status"]

            for field in required_fields:
                if field not in request.json:
                    return jsonify({"error": f"{field} is required"}), 400
            new_status = request.json['status']
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
        
    def patch(self, user_id):

        try:

            user = self.user_instance.get_users(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404
            
            new_status = request.json.get("status")

            if not new_status:
                return jsonify({"error": "status is required"}), 400
            
            check_status = self.user_instance.verify_status(new_status)

            if check_status:
                return {"error": check_status}, 400

            change_status = self.user_instance.modify_user_status(user_id, new_status)
            return jsonify({"message": change_status}), 200

        except Exception as e:
            return jsonify({"error": str({e})}), 400
            
        
        
        
        
