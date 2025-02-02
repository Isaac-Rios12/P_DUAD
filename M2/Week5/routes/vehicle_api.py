from flask.views import MethodView
from flask import jsonify, request
from services.vehicle_service import VehicleManager

class VehicleAPI(MethodView):
    def __init__(self):
        self.vehicle_instance = VehicleManager()

    def get(self):

        try:
            filters = request.args.to_dict()

            if not filters:
                all_vehicles = self.vehicle_instance.get_cars()
                return all_vehicles
            
            if "id" in filters:
                vehicle_id = filters["id"]
                try:
                    vehicle_id = int(vehicle_id)
                except ValueError:
                    return jsonify({"Error": "Id value must be integer"}), 400
                   
                get_vehicle =  self.vehicle_instance.get_cars(vehicle_id)
                if get_vehicle:
                    return jsonify(get_vehicle), 200
                return jsonify({"Error": "Vehicle not found"}), 404
            
           
            filtered_vehicles = self.vehicle_instance.filter_vehicle(filters)
            if filtered_vehicles:
                return jsonify(filtered_vehicles), 200
            return jsonify({"Error": "Not vehicle found with the given criteria..."}), 404
    
        except Exception as e:
            return jsonify({"Error": str({e})}), 500
        

    def post(self):
        try:
            required_fields = ["vin", "model_id", "status"]

            for field in required_fields:
                if field not in request.json:
                    return jsonify({"Error": f"{field} is required"}), 400
                
            new_status = request.json["status"]
                
            
            check_status = self.vehicle_instance.verify_status(new_status)

            if check_status:
                return {"error": check_status}, 400
                
            new_vehicle = self.vehicle_instance.create_vehicle(
                request.json["vin"],
                request.json["model_id"],
                new_status.lower()
            )

            if "error" in new_vehicle:
                return jsonify(new_vehicle), 400

            return jsonify(new_vehicle), 201
        
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        
    def patch(self, vehicle_id):
        try:
            vehicle = self.vehicle_instance.get_cars(vehicle_id)
            if not vehicle:
                return jsonify({"error": "Vehicle not found"}), 404
            
            new_status = request.json.get("status")
            if not new_status:
                return jsonify({"error": "status is required"}), 400
            
            check_status = self.vehicle_instance.verify_status(new_status)

            if check_status:
                return {"error": check_status}, 400

            change_status = self.vehicle_instance.modify_vehicle_status(vehicle_id, new_status)
            return jsonify({"message": change_status}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400