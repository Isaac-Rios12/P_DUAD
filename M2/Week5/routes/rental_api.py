from flask.views import MethodView
from flask import jsonify, request
from services.rental_service import VehicleRental

class RentalAPI(MethodView):
    def __init__(self):
        self.rental_instance = VehicleRental()

    def get(self):

        try:
            filters = request.args.to_dict()

            if not filters:
                all_rentals = self.rental_instance.get_rentals()
                if all_rentals:
                    return jsonify(all_rentals), 200
            if "id" in filters:
                rental_id = filters['id']
                try:
                    rental_id = int(rental_id)
                except ValueError:
                    return jsonify({"Error": "Id must be integer"}), 400
                
                get_rental = self.rental_instance.get_rentals(rental_id)
                if get_rental:
                    return jsonify(get_rental), 200
                return jsonify({"Error": "Rental not found"}), 404
            
            filtered_rentals = self.rental_instance.filter_rental(filters)
            if filtered_rentals:
                return jsonify(filtered_rentals), 200
            return jsonify({"Error": "Not rental found with the given criteria"}), 404
            

        except Exception as e:
            return jsonify({"Error": e}), 500
        
    def post(self):
        try:
            required_fields = ["status", "vehicle_id", "user_id", "return_date"]

            for field in required_fields:
                if field not in request.json:
                    return jsonify({"Error": f"{field} is required"}), 400
            
            new_status = request.json['status']
            check_status = self.rental_instance.verify_status(new_status)

            if check_status:
                return jsonify({"Error": f"Invalid status {new_status}"}), 400
            
            new_rental = self.rental_instance.create_rental(
                request.json['status'],
                request.json['vehicle_id'],
                request.json['user_id'],
                request.json['return_date']
            )

            if "error" in new_rental:
                return jsonify(new_rental), 400
            
            return jsonify(new_rental), 201
        except Exception as e:
            return jsonify(str(e)), 500
            

    def patch(self, rental_id):
        try:

            exists_rental = self.rental_instance.get_rentals(rental_id)
            if not exists_rental:
                return jsonify({"Error": "Rental not found"}), 404
            
            new_status = request.json.get("status")
            
            if not new_status:
                return jsonify({"Error": "status is required"}), 400
            
            check_status = self.rental_instance.verify_status(new_status)
            if check_status:
                return jsonify({"Error": check_status}), 400
            
            change_status = self.rental_instance.modify_rental_status(rental_id, new_status.capitalize())
            if "error" in change_status:
                return jsonify(change_status), 400
            
            return jsonify({"Message": change_status}), 200
        
        except Exception as e:
            return jsonify(str(e))