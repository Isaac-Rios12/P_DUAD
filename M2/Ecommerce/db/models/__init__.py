# Import all models here to ensure they are registered in the metadata.
# This is necessary so that SQLAlchemy can detect and create the corresponding tables.
# If a model is not imported here, its table will not be created automatically.


from .user import User
from .role import Role
from .product import Product
from .cart import Cart
from .cart_item import CartItem
from .sale import Sale
from .sale_item import SaleItem
