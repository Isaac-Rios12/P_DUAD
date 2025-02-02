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
                all_users = self.user_instance.get_users()
                return jsonify(all_users), 200
            
            if "id" in filters:
                user_id = filters["id"]
                try:
                    user_id = int(user_id)
                except ValueError:
                    return jsonify({"Error": "Id value mist be integer"}), 400
            
                get_user = self.user_instance.get_users(user_id)
                if get_user:  
                    return jsonify(get_user), 200
                return jsonify({"error": "User not exist"}), 404
            
            filtered_users = self.user_instance.filter_user(filters)
            if filtered_users:
                return jsonify(filtered_users), 200
            return jsonify({"Error": "Not user found with the given criteria"})

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
            
        
        
        
        
