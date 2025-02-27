from flask import Flask
from routes.user_api import user_blueprint
from routes.vehicle_api import vehicle_blueprint
from routes.rental_api import rental_blueprint

app = Flask(__name__)



app.register_blueprint(vehicle_blueprint, url_prefix='/api')
app.register_blueprint(user_blueprint, url_prefix='/api')
app.register_blueprint(rental_blueprint, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
