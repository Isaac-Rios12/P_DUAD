from db.models.product import Product
from db.manager import db
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select

class ProductRepositoryError(Exception):
    pass
class ProductNotFoundError(ProductRepositoryError):
    pass
class ProductCreationError(ProductRepositoryError):
    pass
class ProductValidationError(Exception):
    pass

class ProductRepository:
    def __init__(self):
        self.product_table = Product

    def _format_product(self, product):
        return{
            "id": product.id,
            "sku": product.sku,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "stock": product.stock
        }
    
    def create_product(self, name, description, price, stock):
        try:
            if not isinstance(price, (int, float)):
                raise ProductValidationError("The price should be numeric.")
            if not isinstance(stock, int):
                raise ProductValidationError("The stock must be a whole number.")
            with db.get_session() as session:
                with session.begin():
                    # Generar SKU automáticamente
                    last_sku = session.execute(
                        select(Product.sku).order_by(Product.id.desc()).limit(1)
                    ).scalar()

                    if last_sku:
                        number = int(last_sku.split("-")[1]) + 1
                    else:
                        number = 1

                    new_sku = f"PROD-{number:04d}"

                    new_product = Product(sku=new_sku,name=name, description=description, price=price, stock=stock)
                    session.add(new_product)
                    session.flush()
                    return self._format_product(new_product)
        except ProductValidationError:
            raise
        except IntegrityError:
            raise ProductCreationError(f"A product with SKU '{new_sku}' already exists")
        except Exception as e:
            raise ProductCreationError(f"The Role could not be created...{e}")
    
    def get_products_by_name(self, name):
        with db.get_session() as session:
            products = session.query(Product).filter_by(name=name).all()
            return [self._format_product(p) for p in products] if products else []
            
    def get_product_by_id(self, product_id):
        try:
            if not isinstance(product_id, int):
                raise ValueError("Product ID must be an integer.")
            with db.get_session() as session:
                with session.begin():
                    product = session.get(Product, product_id)
                    if not product:
                        raise ProductNotFoundError(F"Product with ID...{product_id} not found")
                    return self._format_product(product)
        except (ProductNotFoundError, ValueError):
            raise
        except Exception as e:
            raise ProductRepositoryError("Error obtaining the product")
        
    def get_all_products(self):
        try:
            with db.get_session() as session:
                with session.begin():
                    stmt = select(Product)
                    result = session.execute(stmt)
                    products = result.scalars().all()

                    if not products:
                        raise ProductNotFoundError("No products were found")
                    return [self._format_product(product) for product in products]
        except ProductNotFoundError:
            raise
        except Exception as e:
            raise ProductRepositoryError(f"Error retrieving products...{e}")
        
    def update_product_price(self, product_id, new_price):
        try:
            if int(new_price) <= 0:
                raise ValueError("Price must be positive.")
            if not isinstance(product_id, int):
                raise ValueError("Product ID must be an integer.")
            if not isinstance(new_price, (int, float)):
                raise ValueError("Price must be numeric.")
            with db.get_session() as session:
                with session.begin():
                    product = session.get(Product, product_id)
                    if not product:
                        raise ProductNotFoundError(f"Product with ID...{product_id} not found")
                    
                    product.price = new_price
                    session.flush()
                    return self._format_product(product)
        except (ProductNotFoundError, ValueError):
            raise
        except Exception as e:
            raise ProductRepositoryError(f"Error updating the product...{e}")
        
    def delete_product(self, product_id):
        try:
            if not isinstance(product_id, int):
                raise ValueError("Product ID must be an integer.")
            with db.get_session() as session:
                with session.begin():
                    product = session.get(Product, product_id)
                    if not product:
                        raise ProductNotFoundError(f"Product with ID...{product_id} not found")
                    session.delete(product)
        except (ProductNotFoundError, ValueError):
            raise
        except Exception as e:
            raise ProductRepositoryError(f"Error deleting the product...{e}")