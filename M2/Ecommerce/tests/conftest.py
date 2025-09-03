
import pytest
import uuid
from repositories.user_repo import UserRepository
from repositories.product_repo import ProductRepository
from repositories.cart_repo import CartRepository
from repositories.sale_repo import SaleRepository
from repositories.role_repo import RoleRepository


# ==============================
# FIXTURES DE REPOSITORIOS
# ==============================
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

# FIXTURE DE ROLES
@pytest.fixture(scope="session")
def test_roles(role_repo):
    """Crea roles base si no existen."""
    roles_data = [
        {"name": "Admin"},
        {"name": "Customer"}
    ]
    created_roles = []

    for rdata in roles_data:
        existing_role = role_repo.get_role_by_name(rdata["name"])
        if existing_role:
            created_roles.append(existing_role)
        else:
            new_role = role_repo.create_role(rdata["name"])
            created_roles.append(new_role)

    return created_roles

# FIXTURE DE USUARIO BASE
@pytest.fixture(scope="session")
def test_user(user_repo, test_roles):
    """Crea un usuario de prueba con rol Customer si no existe."""
    customer_role = next(r for r in test_roles if r["name"] == "Customer")
    existing_user = user_repo.get_user_by_nickname("test-user")
    if existing_user:
        return existing_user

    return user_repo.create_user(
        fullname="Test User",
        nickname="test-user",
        email="testuser@example.com",
        password="securepass",
        role_id=customer_role["id"]
    )


# GENERADOR DE DATOS ÚNICOS PARA TESTS
@pytest.fixture
def unique_user_data(test_roles):
    """Genera datos de usuario únicos para evitar duplicados en las pruebas."""
    customer_role = next(r for r in test_roles if r["name"] == "Customer")
    uid = uuid.uuid4().hex[:8]
    return {
        "fullname": f"User {uid}",
        "nickname": f"user_{uid}",
        "email": f"user_{uid}@test.com",
        "password": "pass123",
        "role_id": customer_role["id"]
    }


# FIXTURE DE PRODUCTOS
@pytest.fixture(scope="session")
def test_products(product_repo):
    products_data = [
        {"name": "Test Product 1", "description": "Producto de prueba 1", "price": 50.0, "stock": 100},
        {"name": "Test Product 2", "description": "Producto de prueba 2", "price": 75.0, "stock": 100},
    ]
    created_products = []

    for pdata in products_data:
        existing_product = product_repo.get_products_by_name(pdata["name"])
        if existing_product:
            created_products.extend(existing_product)  # ya es dict/ORM
        else:
            new_product = product_repo.create_product(**pdata)
            created_products.extend(new_product)

    return created_products


# FIXTURE DE CARRITO
@pytest.fixture
def test_cart(cart_repo, test_user, test_products):
    cart = cart_repo.get_or_create_cart_by_user(test_user["id"])
    items = [{"product_id": p["id"], "quantity": 2} for p in test_products]
    cart = cart_repo.add_items_to_user_cart(cart["id"], items)
    return cart
