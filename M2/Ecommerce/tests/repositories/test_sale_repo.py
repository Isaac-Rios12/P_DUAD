import pytest
from repositories.sale_repo import (
    SaleRepository, SaleNotFoundError, SaleCreationError, SaleRepositoryError
)


def test_calculate_total(test_cart):
    sale_repo = SaleRepository()
    total = sale_repo._calculate_total(test_cart)
    print("testCart", test_cart)
    print(total)
    expected_total = 250.0

    assert total == expected_total

def test_create_sale_success(sale_repo, test_user, test_cart):
    print("cart", test_cart)
    sale = sale_repo.create_sale(
    user_id=test_user["id"],
    billing_address="Limon Centro"
    )

    assert sale["user_id"] == test_user["id"]
    assert len(sale["items"]) == 2
    assert all("product_id" in item for item in sale["items"])
    assert all("quantity" in item for item in sale["items"])
    assert all("unit_price" in item for item in sale["items"])


# @pytest.fixture
# def temp_user(user_repo, base_roles):
#     """Usuario temporal para tests que se destruye luego."""
#     customer_role = next(r for r in base_roles if r["name"] == "Customer")
#     uid = uuid.uuid4().hex[:8]
#     return user_repo.create_user(
#         fullname=f"User {uid}",
#         nickname=f"user_{uid}",
#         email=f"user_{uid}@test.com",
#         password="pass123",
#         role_id=customer_role["id"]
#     )
def test_create_sale_with_empty_cart_raises_error(sale_repo, user_repo, unique_user_data, cart_repo):
    user = user_repo.create_user(**unique_user_data)
    empty_cart = cart_repo.get_or_create_cart_by_user(user["id"])
    
    with pytest.raises(SaleCreationError):
        sale_repo.create_sale(
            user_id=user["id"],
            billing_address="Limon Centro"
        )

def test_get_sale_by_id_success(sale_repo, test_user, test_cart):
    """Obtener una venta por ID exitosa"""
    sale = sale_repo.create_sale(
        user_id=test_user["id"],
        #cart_id=test_cart["id"],
        billing_address="Limon Centro"
    )
    fetched_sale = sale_repo.get_sale_by_id(user_id=test_user["id"], sale_id=sale["id"])

    assert fetched_sale["id"] == sale["id"]
    assert fetched_sale["user_id"] == test_user["id"]
    
def test_get_sale_by_nonexistent_id_raises_error(sale_repo, test_user):
    with pytest.raises(SaleNotFoundError):
        sale_repo.get_sale_by_id(user_id=test_user["id"], sale_id=999999)
