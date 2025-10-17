import pytest
from db.manager import DatabaseManager
from repositories.product_repo import ProductRepository, ProductCreationError, ProductNotFoundError, ProductRepositoryError, ProductValidationError


def test_add_product_with_success(product_repo):
    new_product = product_repo.create_product("Dog food", "Premium foof", 2500, 10 )

    assert new_product["name"] == "Dog food"
    assert new_product["price"] == 2500

def test_add_product_with_invalid_price_type(product_repo):
    with pytest.raises(ProductValidationError):
        product_repo.create_product("cat food", "Premium food", "150", 10)

def test_add_product_with_invalid_stock_type(product_repo):
    with pytest.raises(ProductValidationError):
        product_repo.create_product("mice food", "Premium food", 1000, "20")

def test_get_product_by_id_with_success(product_repo):
    new_product = product_repo.create_product("Pig food", "Premium food", 5000, 25)
    product_id = new_product["id"]

    fetched_product = product_repo.get_product_by_id(product_id)

    assert fetched_product["id"] == product_id

def test_get_product_by_id_with_invalid_id_type(product_repo):
    with pytest.raises(ValueError):
        product_repo.get_product_by_id("12")

def test_get_product_by_id_not_registered(product_repo):
    with pytest.raises(ProductNotFoundError):
        product_repo.get_product_by_id(999999999)

def test_update_product_price_with_success(product_repo):
    new_product = product_repo.create_product("update_price", "nothing", 1575, 15)
    product_id = new_product["id"]

    update_price = product_repo.update_product_price(product_id, 2755)

    assert update_price["price"] == 2755.0

def test_update_product_price_with_invalid_type(product_repo):
    new_product = product_repo.create_product("invalid_price", "nothing", 1575, 15)
    product_id = new_product["id"]

    with pytest.raises(ValueError):
        product_repo.update_product_price(product_id, "1500")

def test_delete_product_when_not_found(product_repo):
    with pytest.raises(ProductNotFoundError):
        product_repo.delete_product(999999999900099)

def test_delete_product_with_success(product_repo):
    new_product = product_repo.create_product("to_delete", "nothing", 1575, 15)
    product_id = new_product["id"]

    product_repo.delete_product(product_id)

    with pytest.raises(ProductNotFoundError):
        delete = product_repo.delete_product(product_id)
