from flask.views import MethodView
from flask import jsonify, request, Blueprint
from services.rental_service import VehicleRental

rental_blueprint = Blueprint('rental_blueprint', __name__)

class RentalListAPI(MethodView):
    def __init__(self):
        self.rental_instance = VehicleRental()

    def get(self):
        try:
            filters = request.args.to_dict()
            rentals = self.rental_instance.filter_rental(filters) if filters else self.rental_instance.get_all_rentals()
            
            if rentals:
                return jsonify(rentals), 200
            return jsonify({"Error": "No rentals found"}), 404
        except Exception as e:
            return jsonify({"Error": str(e)}), 500
    
    def post(self):
        try:
            required_fields = ["status", "vehicle_id", "user_id", "return_date"]
            for field in required_fields:
                if field not in request.json:
                    return jsonify({"Error": f"{field} is required"}), 400
            
            new_status = request.json['status'].lower()
            check_status = self.rental_instance.verify_status(new_status)

            if check_status is not None:
                return jsonify({"Error": f"Invalid status {new_status}"}), 400
            
            new_rental = self.rental_instance.create_rental(
                request.json['status'].lower(),
                request.json['vehicle_id'],
                request.json['user_id'],
                request.json['return_date']
            )

            if "error" in new_rental:
                return jsonify(new_rental), 400
            
            return jsonify(new_rental), 201
        except Exception as e:
            return jsonify({"Error": str(e)}), 500


class RentalDetailAPI(MethodView):
    def __init__(self):
        self.rental_instance = VehicleRental()
    
    def get(self, rental_id):
        try:
            rental = self.rental_instance.get_rental_by_id(rental_id)
            if rental:
                return jsonify(rental), 200
            return jsonify({"Error": "Rental not found"}), 404
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

    def patch(self, rental_id):
        try:
            exists_rental = self.rental_instance.get_rental_by_id(rental_id)
            if not exists_rental:
                return jsonify({"Error": "Rental not found"}), 404
            
            new_status = request.json.get("status")
            if not new_status:
                return jsonify({"Error": "status is required"}), 400
            
            check_status = self.rental_instance.verify_status(new_status)
            if check_status is not None:
                return jsonify({"Error": check_status}), 400
            
            change_status = self.rental_instance.modify_rental_status(rental_id, new_status.lower())
            if "error" in change_status:
                return jsonify(change_status), 400
            
            return jsonify({"Message": change_status}), 200
        except Exception as e:
            return jsonify({"Error": str(e)}), 500

rental_blueprint.add_url_rule('/rentals', view_func=RentalListAPI.as_view('rental_list'), methods=['GET', 'POST'])
rental_blueprint.add_url_rule('/rentals/<int:rental_id>', view_func=RentalDetailAPI.as_view('rental_detail'), methods=['GET', 'PATCH'])
