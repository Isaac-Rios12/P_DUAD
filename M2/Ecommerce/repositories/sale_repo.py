from db.models.sale import Sale
from db.models.cart import Cart
from db.models.product import Product
from db.models.sale_item import SaleItem
from db.manager import db

from sqlalchemy import select

class SaleRepositoryError(Exception):
    pass
class SaleNotFoundError(SaleRepositoryError):
    pass
class SaleCreationError(SaleRepositoryError):
    pass


class SaleRepository:
    def __init__(self):
        self.sale_table = Sale

    def _format_sale(self, sale):
        return{
            "id": sale.id,
            "user_id": sale.user_id,
            "billing_address": sale.billing_address,
            "total_amount": float(sale.total_amount),
            "items": [
                {
                    "product_id": item.product_id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price)
                }
                for item in sale.items
            ],
        }
    
    def _calculate_total(self, cart):
        # si cart es dict con 'items' #!esto lo hago para el test
        if isinstance(cart, dict):
            return sum(item["quantity"] * item["unit_price"] for item in cart["items"])
        # si es ORM
        return sum(item.quantity * item.product.price for item in cart.items)
    
    def _copy_cart_items_to_sale(self, session, cart, sale):
        for item in cart.items:
            sale_item = SaleItem(
                sale_id = sale.id,
                product_id = item.product_id,
                quantity = item.quantity,
                unit_price = item.product.price
            )
            session.add(sale_item)
        session.flush()

    
    def create_sale(self, user_id, billing_address):
        try:
            with db.get_session() as session:
                with session.begin():
                    cart = (
                        session.query(Cart).filter(
                            Cart.user_id == user_id, 
                            Cart.is_finalized == False
                        ).one_or_none()
                    )
                    if not cart or not cart.items:
                        raise SaleCreationError("Cart is empty or not found")
                    
                    #calculo del total
                    total = self._calculate_total(cart)

                    #crea venta
                    new_sale = Sale(
                        user_id = user_id,
                        cart_id = cart.id,
                        billing_address = billing_address,
                        total_amount = total
                    )
                    session.add(new_sale)
                    session.flush()

                    #para actualizar stock
                    for cart_item in cart.items:
                        product = (
                            session.query(Product)
                            .filter(Product.id == cart_item.product_id)
                            .with_for_update()
                            .one()
                        )
                        if product.stock < cart_item.quantity:
                            raise SaleCreationError(f"Not enough stock for product {cart_item.product.name}")
                        
                        product.stock -= cart_item.quantity
                        session.add(product)

                    #copia datos del cart_items a sale_item
                    self._copy_cart_items_to_sale(session, cart, new_sale)
                    
                    #!Nuevaaaaaaaaaa
                    cart.is_finalized = True
                    session.flush()
                    #!retornar sale crear func
                    return self._format_sale(new_sale)
                
        except SaleCreationError:
            raise
        except Exception as e:
            print(e)
            raise SaleRepositoryError(f"Error...")
        
    def get_sales_by_user(self, user_id):
        try:
            with db.get_session() as session:
                with session.begin():
                    stmt = select(Sale).where(Sale.user_id == user_id)
                    sales = session.scalars(stmt).all()

                    if not sales:
                        raise SaleNotFoundError(f"No sales found for user {user_id}")

                    return [self._format_sale(sale) for sale in sales]

        except SaleNotFoundError:
            raise
        except Exception as e:
            raise SaleRepositoryError(f"Error retrieving sales for user {user_id}: {str(e)}")

    def get_sale_by_id(self, user_id, sale_id):
        try:
            with db.get_session() as session:
                with session.begin():
                    stmt = select(Sale).where(Sale.id == sale_id, Sale.user_id == user_id)
                    sale = session.scalars(stmt).one_or_none()
                    if not sale:
                        raise SaleNotFoundError(f"Sale {sale_id} not found for user {user_id}")
                    return self._format_sale(sale)

        except SaleNotFoundError:
            raise
        except Exception as e:
            raise SaleRepositoryError(f"Error retrieving sale {sale_id} for user {user_id}: {str(e)}")

    def get_sale_by_id_admin(self, sale_id):
        try:
            with db.get_session() as session:
                with session.begin():
                    stmt = select(Sale).where(Sale.id == sale_id)
                    sale = session.scalars(stmt).one_or_none()
                    if not sale:
                        raise SaleNotFoundError(f"Sale {sale_id} not found")
                    return self._format_sale(sale)
        except SaleNotFoundError:
            raise
        except Exception as e:
            raise SaleRepositoryError(f"Error retrieving sale {sale_id}: {str(e)}")

    def get_all_sales(self):
        try:
            with db.get_session() as session:
                with session.begin():
                    stmt = select(Sale)
                    sales = session.execute(stmt).scalars().all()
                    if not sales:
                        raise SaleNotFoundError(f"No sales found")
                    return [self._format_sale(sale) for sale in sales]
        except SaleNotFoundError:
            raise
        except Exception as e:
            raise SaleRepositoryError(f"Error retrieving sale sales: {str(e)}")