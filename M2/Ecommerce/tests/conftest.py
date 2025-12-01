import os
import uuid
import pytest
from dotenv import load_dotenv
import random
from db.models import Product

load_dotenv()

os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL_TEST")

from main import create_app
from db.manager import db 
from repositories.user_repo import UserRepository
from repositories.product_repo import ProductRepository
from repositories.cart_repo import CartRepository
from repositories.sale_repo import SaleRepository
from repositories.role_repo import RoleRepository, RoleNotFoundError

# APP Y CLIENT
@pytest.fixture(scope="session")
def app():
    app = create_app(testing=True)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


# SESIÓN TEMPORAL
@pytest.fixture(scope="session")
def db_session(app):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        session = db.Session(bind=connection)
        try:
            yield session
        finally:
            transaction.rollback()# !no funciona aca
            connection.close()
            session.close()

# FIXTURES DE REPOSITORIOS, inyeccion de instancias.
@pytest.fixture(scope="session")
def user_repo():
    return UserRepository()

@pytest.fixture(scope="session")
def product_repo():
    return ProductRepository()

@pytest.fixture(scope="session")
def role_repo():
    return RoleRepository()

@pytest.fixture(scope="session")
def cart_repo():
    return CartRepository()

@pytest.fixture(scope="session")
def sale_repo():
    return SaleRepository()


# ROLES BASE
@pytest.fixture(scope="session")
def base_roles(role_repo):
    """
    Crea los roles 'Admin' y 'Customer' en la DB de test una sola vez.
    Permanecen en la DB durante toda la sesión de tests.
    """
    roles_data = ["Admin", "Customer"]
    created_roles = []

    for role_name in roles_data:
        try:
            # Intenta obtener el rol
            role = role_repo.get_role_by_name(role_name)
        except RoleNotFoundError:
            # Si no existe, lo crea
            role = role_repo.create_role(role_name)
            # db_session.add(role)
            # db_session.commit()
        created_roles.append(role)

    return created_roles


# USUARIO BASE POR TEST
@pytest.fixture
def test_user(user_repo, base_roles):
    customer_role = next(r for r in base_roles if r["name"] == "Customer")
    unique_suffix = random.randint(1, 100000)
    return user_repo.create_user(
        fullname="Test User",
        nickname=f"test-user-{unique_suffix}",
        email=f"testuser{unique_suffix}@example.com",
        password="securepass",
        role_id=customer_role["id"]
    )


# DATOS ÚNICOS POR TEST
@pytest.fixture
def unique_user_data(base_roles):
    customer_role = next(r for r in base_roles if r["name"] == "Customer")
    uid = uuid.uuid4().hex[:8]
    return {
        "fullname": f"User {uid}",
        "nickname": f"user_{uid}",
        "email": f"user_{uid}@test.com",
        "password": "pass123",
        "role_id": customer_role["id"]
    }

# PRODUCTOS POR TEST
@pytest.fixture(scope="function")
def test_products(product_repo):
    unique_id = uuid.uuid4().hex[:8]
    products_data = [
        {"name": f"Test Product 1 {unique_id}", "description": "Producto de prueba 1", "price": 50.0, "stock": 100},
        {"name": f"Test Product 2 {unique_id}", "description": "Producto de prueba 2", "price": 75.0, "stock": 100},
    ]
    created_products = []

    for pdata in products_data:
        new_product = product_repo.create_product(**pdata)
        if isinstance(new_product, list):
            created_products.extend(new_product)
        else:
            created_products.append(new_product)
    
    return created_products


# CARRITO POR TEST
@pytest.fixture(scope="function")
def test_cart(cart_repo, test_user, test_products):
    # Limpiar carrito antes de empezar
    for p in test_products:
        try:
            cart_repo.remove_item_from_user_cart(test_user["id"], p["id"])
        except Exception:
            pass  

    cart = cart_repo.get_or_create_cart_by_user(test_user["id"])
    items = [{"product_id": p["id"], "quantity": 2} for p in test_products]
    cart = cart_repo.add_items_to_user_cart(test_user["id"], items)
    return cart
