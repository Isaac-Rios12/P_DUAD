from flask import Flask
from routes.user_api import user_routes
from routes.product_api import product_routes
from routes.cart_api import cart_routes
from routes.sale_api import sale_routes
from routes.role_api import role_routes

app = Flask("user-service")

app.register_blueprint(user_routes, url_prefix='/users')
app.register_blueprint(role_routes, url_prefix='/roles')
app.register_blueprint(product_routes, url_prefix='/products')
app.register_blueprint(cart_routes, url_prefix='/carts')
app.register_blueprint(sale_routes, url_prefix='/sales')

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)