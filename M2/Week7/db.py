from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, Numeric, Date
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
    Column("entry_date", Date),
    Column("quantity", Integer)
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
            
class Product_Maneger(BaseManager):
    def __init__(self):
        super().__init__()

    def create_product(self, name, price, entry_date, quantity):
        stmt = insert(product_table).returning(product_table.c.id).values(name=name, price=price, entry_date=entry_date, quantity=quantity)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        return result.all()[0]
    
    def get_product_by_id(self, id_product):
        stmt = select(product_table).where(product_table.c.id == id_product)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            product = result.all
            if len(product) == 0:
                return None
            else:
                return product[0]
        
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
        

#quedo aca, implemento crud en db de los prodtcutos, ahiora sigue crear los endpoints.....
        
        




    

        
db = DB_Manager()