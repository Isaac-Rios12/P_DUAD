from flask import Flask
import product_api
from user_api import user_routes
from product_api import product_routes

app = Flask("user-service")

#app.register_blueprint(product_api)
app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(product_routes, url_prefix='/products')

@app.route("/liveness")
def liveness():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)