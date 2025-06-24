from flask import Flask
from routes.purchase_api import purchase_routes
from routes.user_api import user_routes
from routes.product_api import product_routes

app = Flask("user-service")

#app.register_blueprint(product_api)
app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(product_routes, url_prefix='/products')
app.register_blueprint(purchase_routes, url_prefix='/purchases')

@app.route("/liveness")
def liveness():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)