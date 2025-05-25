from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey

DB_URI = 'postgresql://postgres:postgre@localhost:5432/W6MB'
engine = create_engine(DB_URI, echo=True)
metadata_obj = MetaData()


user_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("email", String(40), unique=True, nullable=False),
    Column("phone", String(10), nullable=False)
)

address_table = Table(
    "addresses",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("street", String(100), nullable=False),
    Column("city", String(75), nullable=False),
    Column("state", String(100), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False)
)

car_table = Table(
    "cars",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("brand", String(100), nullable=False),
    Column("model", String(100), nullable=False),
    Column("year", Integer, nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=True)
)

def create_metadata():
    metadata_obj.create_all(engine)
    print("Tablas creadas correctamente.")
