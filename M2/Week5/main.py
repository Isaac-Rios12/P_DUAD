from flask import Flask
from routes.user_api import UserAPI
from routes.vehicle_api import VehicleAPI
from routes.rental_api import RentalAPI

app = Flask(__name__)

# Crear la vista para el UserAPI
user_api_view = UserAPI.as_view('user_api')
vehicle_api_view = VehicleAPI.as_view('vehicle_api')
rental_api_view= RentalAPI.as_view('rental_api')

#user_api_view = UserAPI.as_view('user_api', user_instance=UserModel())

# Registrar la vista con la URL correspondiente
app.add_url_rule('/api/users', view_func=user_api_view, methods=['GET', 'POST'])
#app.add_url_rule('/api/users/<int:user_id>', view_func=user_api_view, methods=['GET'])
app.add_url_rule('/api/users/<int:user_id>', view_func=user_api_view, methods=['PATCH'])

#vehicles
app.add_url_rule('/api/vehicles', view_func=vehicle_api_view, methods=['GET', 'POST'])
app.add_url_rule('/api/vehicles/<int:vehicle_id>', view_func=vehicle_api_view, methods=['PATCH'])

app.add_url_rule('/api/rentals', view_func=rental_api_view, methods=['GET', 'POST'])
app.add_url_rule('/api/rentals/<int:rental_id>', view_func=rental_api_view, methods=['PATCH'])
if __name__ == "__main__":
    app.run(debug=True)
