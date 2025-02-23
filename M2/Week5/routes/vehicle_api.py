from flask.views import MethodView
from flask import jsonify, request, Blueprint
from services.vehicle_service import VehicleManager

vehicle_blueprint = Blueprint("vehicle_blueprint", __name__)

class VehicleListAPI(MethodView):
    def __init__(self):
        self.vehicle_instance = VehicleManager()

    def get(self):
        try:
            filters = request.args.to_dict()
            users = self.vehicle_instance.filter_vehicle(filters) if filters else self.vehicle_instance.get_all_vehicles()

            if users:
                return jsonify(users), 200
            return jsonify({"Error": "No vehicles found"})
        except Exception as e:
            return jsonify({"Error": str(e)}), 500
        
    def post(self):
        try:
            required_fields = ["vin", "model_id", "status"]

            for field in required_fields:
                if field not in request.json:
                    return jsonify({"Error": f"{field} is required"}), 400
                
            new_status = request.json["status"].lower()
                
            check_status = self.vehicle_instance.verify_status(new_status)

            if check_status:
                return jsonify({"error": check_status}), 400
                
            new_vehicle = self.vehicle_instance.create_vehicle(
                request.json["vin"],
                request.json["model_id"],
                new_status
            )

            if "error" in new_vehicle:
                return jsonify(new_vehicle), 400

            return jsonify(new_vehicle), 201
        
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        

class VehicleDetailAPI(MethodView):
    def __init__(self):
        self.vehicle_instance = VehicleManager()

    def get(self, vehicle_id):

        try:
            vehicle = self.vehicle_instance.get_car_by_id(vehicle_id)
            if vehicle:
                return jsonify(vehicle), 200
            return jsonify({"Error": "Not vehicle found with the given criteria"})
    
        except Exception as e:
            return jsonify({"Error": str({e})}), 500
    
    def patch(self, vehicle_id):
        try:
            vehicle = self.vehicle_instance.get_car_by_id(vehicle_id)
            if not vehicle:
                return jsonify({"error": "Vehicle not found"}), 404
            
            new_status = request.json.get("status").lower()
            if not new_status:
                return jsonify({"error": "status is required"}), 400
            
            check_status = self.vehicle_instance.verify_status(new_status)

            if check_status:
                return jsonify({"error": check_status}), 400

            change_status = self.vehicle_instance.modify_vehicle_status(vehicle_id, new_status)
            return jsonify({"message": change_status}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
        

vehicle_blueprint.add_url_rule('/vehicles', view_func=VehicleListAPI.as_view('vehicle_list'), methods=['GET', 'POST'])
vehicle_blueprint.add_url_rule('/vehicles/<int:vehicle_id>', view_func=VehicleDetailAPI.as_view('vehicle_detail'), methods=['GET','PATCH'] )  


