from db.models.cart import Cart
from db.models.product import Product
from db.models.cart_item import CartItem
from db.manager import db
from sqlalchemy import select
from repositories.product_repo import ProductNotFoundError

class CartRepositoryError(Exception):
    pass
class CartCreationError(CartRepositoryError):
    pass
class CartNotFoundError(CartRepositoryError):
    pass
class ItemNotInCartError(CartRepositoryError):
    pass
class InsufficientStockError(CartRepositoryError):
    pass
class InvalidCartIdentifierError(CartRepositoryError):
    pass


class CartRepository:
    def __init__(self):
        pass

    def _validate_int(self, value, name, error_cls=InvalidCartIdentifierError):
        if not isinstance(value, int):
            raise error_cls(f"{name} must be an integer")
    
    def _format_cart(self, cart):
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "created_at": cart.created_at,
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": float(item.product.price)
                }
                for item in cart.items
            ],
        }
    
    def _validate_product_and_stock(self, session, product_id, quantity):
        product = session.get(Product, product_id)
        if not product:
            raise ProductNotFoundError(f"Product with ID {product_id} not found")
        if quantity > product.stock:
            raise InsufficientStockError(
                f"Not enough stock for {product.name}. Requested: {quantity}, Available: {product.stock}"
            )
        return product
    
    def _add_items_logic(self, session, cart, items):
        for item in items:
            product_id = item["product_id"]
            quantity = item["quantity"]

            product = self._validate_product_and_stock(session, product_id, quantity)

            existing_item = session.scalars(
                select(CartItem).where(
                    CartItem.cart_id == cart.id,
                    CartItem.product_id == product_id
                )
            ).first()

            if existing_item:
                new_quantity = existing_item.quantity + quantity
                if new_quantity > product.stock:
                    raise InsufficientStockError(
                        f"Not enough stock to add {quantity} more units of {product.name}"
                    )
                existing_item.quantity = new_quantity
            else:
                new_item = CartItem(
                    cart_id=cart.id,
                    product_id=product_id,
                    quantity=quantity
                )
                session.add(new_item)

    def delete_cart_by_user(self, user_id):
        self._validate_int(user_id, "User ID")
        try:
            with db.get_session() as session:
                with session.begin():
                    cart = session.query(Cart).filter_by(user_id=user_id).first()
                    if not cart:
                        raise CartNotFoundError(f"Cart for user {user_id} not found")
                    session.delete(cart)
                    return True
        except Exception as e:
            raise CartRepositoryError(f"Error deleting cart for user {user_id}: {e}")

    def get_or_create_cart_by_user(self, user_id):
        self._validate_int(user_id, "User ID")
        try:
            with db.get_session() as session:
                with session.begin():
                    cart = session.query(Cart).filter_by(user_id=user_id, is_finalized=False).first()
                    if not cart:
                        cart = Cart(user_id=user_id)
                        session.add(cart)
                        session.flush()
                    return self._format_cart(cart)
        except Exception as e:
            raise CartRepositoryError(f"Error getting/creating cart for user {user_id}: {e}")

    def add_items_to_user_cart(self, user_id, items):
        self._validate_int(user_id, "User ID")
        try:
            with db.get_session() as session:
                with session.begin():
                    cart = session.query(Cart).filter_by(user_id=user_id).first()
                    if not cart:
                        cart = Cart(user_id=user_id)
                        session.add(cart)
                        session.flush()
                    self._add_items_logic(session, cart, items)
                    session.flush()
                    return self._format_cart(cart)
        except (InsufficientStockError, ProductNotFoundError) as e:
            raise
        except Exception as e:
            raise CartRepositoryError(f"Error adding items to user cart: {e}")

    def remove_item_from_user_cart(self, user_id, product_id):
        self._validate_int(user_id, "User ID")
        self._validate_int(product_id, "Product ID")
        try:
            with db.get_session() as session:
                with session.begin():
                    cart = session.query(Cart).filter_by(user_id=user_id).first()
                    if not cart:
                        raise CartNotFoundError(f"No cart found for user {user_id}")
                    item = session.scalars(
                        select(CartItem).where(
                            CartItem.cart_id == cart.id,
                            CartItem.product_id == product_id
                        )
                    ).first()
                    if not item:
                        raise ItemNotInCartError(
                            f"Product ID {product_id} not found in user {user_id}'s cart"
                        )
                    session.delete(item)
                    session.flush()
                    return self._format_cart(cart)
        except (CartNotFoundError, ItemNotInCartError) as e:
            raise
        except Exception as e:
            raise CartRepositoryError(f"Error removing item from user cart: {e}")

    def update_item_quantity_in_user_cart(self, user_id, product_id, new_quantity):
        self._validate_int(user_id, "User ID")
        self._validate_int(product_id, "Product ID")
        self._validate_int(new_quantity, "New Quantity")
        try:
            with db.get_session() as session:
                with session.begin():
                    cart = session.query(Cart).filter_by(user_id=user_id).first()
                    if not cart:
                        raise CartNotFoundError(f"No cart found for user {user_id}")
                    item = session.scalars(
                        select(CartItem).where(
                            CartItem.cart_id == cart.id,
                            CartItem.product_id == product_id
                        )
                    ).first()
                    if not item:
                        raise ItemNotInCartError(
                            f"Item with product ID {product_id} not found in user {user_id}'s cart"
                        )
                    if new_quantity == 0:
                        session.delete(item)
                    else:
                        self._validate_product_and_stock(session, product_id, new_quantity)
                        item.quantity = new_quantity
                    session.flush()
                    return self._format_cart(cart)
        except (CartNotFoundError, ItemNotInCartError) as e:
            raise
        except Exception as e:
            raise CartRepositoryError(f"Error updating quantity in user {user_id}'s cart: {e}")
