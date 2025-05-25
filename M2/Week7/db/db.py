from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, Numeric, DateTime, func, ForeignKey
from sqlalchemy import insert, select, update, delete

metadata_obj = MetaData()

user_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(30)),
    Column("password", String),
    Column("role", String(11))
)

product_table = Table(
    "products",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(75)),
    Column("price", Numeric(10,2)),
    Column("entry_date", DateTime, server_default=func.now()),
    Column("quantity", Integer)
)

invoice_table = Table(
    "invoices",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("total", Numeric(10,2), nullable=False),
    Column("created_at", DateTime, server_default=func.now())
)

invoice_item_table= Table(
    "invoice_itmes",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("invoice_id", Integer, ForeignKey("invoices.id"), nullable=False),
    Column("product_id", Integer, ForeignKey("products.id"), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Numeric(10,2), nullable=False),
    Column("subtotal", Numeric(10,2), nullable=False)
)

class BaseManager:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:postgre@localhost:5432/guiado')
        metadata_obj.create_all(self.engine)


class DB_Manager(BaseManager):
    def __init__(self):
        super().__init__()

    def insert_user(self, username, password, role):
        stmt = insert(user_table).returning(user_table.c.id).values(username=username, password=password, role=role)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.all()[0]
    
    
    
    def get_user(self, username, password):
        stmt = select(user_table).where(user_table.c.username == username).where(user_table.c.password == password)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()

            if (len(users)==0):
                return None
            else:
                return users[0]
            
    def get_user_by_id(self, id):
        stmt = select(user_table).where(user_table.c.id == id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users = result.all()
            if (len(users)==0):
                return None
            else:
                return users[0]
            
class Product_Manager(BaseManager):
    def __init__(self):
        super().__init__()

    def create_product(self, name, price,quantity):
        
        stmt = insert(product_table).returning(product_table.c.id).values(name=name, price=price,quantity=quantity)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.all()[0]
    
    def get_all_products(self):
        stmt = select(product_table)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            users= result.all()

            if (len(users) == 0):
                return None
            else:
                return users
            
    
    def get_product_by_id(self, id_product):
        stmt = select(product_table).where(product_table.c.id == id_product)
        with self.engine.connect() as conn:
            result = conn.execute(stmt).fetchone()
            return result
    
    def update_product(self,id_product, name, price, quantity):
        stmt = update(product_table).where(product_table.c.id == id_product).values(name=name, price=price, quantity=quantity)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()

            if result.rowcount == 0:
                return False
            return True
        
    def delete_product(self, product_id):
        stmt = delete(product_table).where(product_table.c.id == product_id)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()

            if result.rowcount == 0:
                return False
            return True
        
class Purchase_Manager(BaseManager):
    def __init__(self):
        super().__init__()

    def validated_and_get_products(self, products, conn):
        validated_products = []

        for item in products:
            product_id = item['product_id']
            quantity = item['quantity']

            stmt = select(product_table).where(product_table.c.id == product_id)
            row = conn.execute(stmt).mappings().fetchone()

            if not row:
                raise ValueError(f"Producto con el id {product_id} no existe")
            
            product = dict(row)

            if not product:
                raise ValueError(f"Porducto con el id{product_id} no existe")
            if product['quantity'] < quantity:
                raise ValueError(f"Producto {product['name']} no tiene suficiente stock")
            
            validated_products.append((product,quantity))
        
        return validated_products
    
    def calcualte_total_amount(self, validate_products):
        return sum(product['price'] * quantity for product,quantity in validate_products)
    
    def create_invoice(self, user_id, total, conn):
        stmt = insert(invoice_table).returning(invoice_table.c.id).values(user_id=user_id, total=total)
        result = conn.execute(stmt)
        return result.scalar()
    
    def insert_invoice_items_and_update_stock(self, invoice_id, validated_products, conn):
        for product, quantity in validated_products:
            item_stmt = insert(invoice_item_table).values(
                invoice_id=invoice_id,
                product_id=product['id'],
                quantity = quantity,
                unit_price = product['price'],
                subtotal=product['price'] * quantity
            )
            conn.execute(item_stmt)

            #actualizo stock
            updated_stock_stmt = update(product_table).where(product_table.c.id == product['id']).values(
                quantity = product_table.c.quantity - quantity
            )
            conn.execute(updated_stock_stmt)

#preguntar nivel de accesooooo
    def make_purchase(self, user_id, products):
        with self.engine.begin() as conn:
            #primero valido los prodcutos
            validated_products = self.validated_and_get_products(products, conn)

            #luego si todo va bien, calculo total
            total = self.calcualte_total_amount(validated_products)

            #leugo creo la factura
            invoice_id = self.create_invoice(user_id, total, conn)

            #termina creando los items en tabal items
            self.insert_invoice_items_and_update_stock(invoice_id, validated_products, conn)

            return {"message": "Compra realizada con exito", "invoice_id":invoice_id}
        
    def get_invoices_by_user(self, user_id):
        with self.engine.connect() as conn:
            invoices_stmt = select(invoice_table).where(invoice_table.c.user_id == user_id)
            invoices = conn.execute(invoices_stmt).mappings().all()

            result = []

            for invoice in invoices:
                items_stmt = select(invoice_item_table).where(invoice_item_table.c.invoice_id == invoice['id'])
                items = conn.execute(items_stmt).mappings().all()
                result.append({
                    "invoice": dict(invoice),
                    "items": [dict(item) for item in items]
                })

            return result
                
db = DB_Manager()