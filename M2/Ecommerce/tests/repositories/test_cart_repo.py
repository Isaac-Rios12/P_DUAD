import pytest
from repositories.cart_repo import CartRepository, CartRepositoryError, CartCreationError, CartNotFoundError, ItemNotInCartError, InsufficientStockError, InvalidCartIdentifierError
from repositories.user_repo import UserRepository
from repositories.product_repo import ProductNotFoundError

def test_create_cart_with_success(cart_repo, test_user):
    new_cart = cart_repo.get_or_create_cart_by_user(test_user["id"])
    assert new_cart["user_id"] == test_user["id"]

def test_try_insert_cart_with_invalid_data(cart_repo):
    with pytest.raises(InvalidCartIdentifierError):
        cart_repo.get_or_create_cart_by_user("asd") 

def test_add_items_to_cart_successfully(cart_repo, test_user, test_products):
    # Usamos user_id, no cart_id
    updated_cart = cart_repo.add_items_to_user_cart(test_user["id"],
        [{"product_id": p["id"], "quantity": 2} for p in test_products]
    )

    print(updated_cart)

    assert updated_cart["user_id"] == test_user["id"]
    assert len(updated_cart["items"]) == len(test_products)

def test_add_nonexistent_product_to_cart_raises_error(cart_repo, test_user):
    with pytest.raises(ProductNotFoundError):
        fake_product = [{"product_id": 999999, "quantity": 1}]
        cart_repo.add_items_to_user_cart(test_user["id"], fake_product)



def test_remove_item_from_cart_successfully(cart_repo, test_user, test_products):
    cart_repo.add_items_to_user_cart(test_user["id"],
        [{"product_id": p["id"], "quantity": 2} for p in test_products]
    )

    product_to_remove = test_products[0]["id"]
    updated_cart = cart_repo.remove_item_from_user_cart(test_user["id"], product_to_remove)

    remaining_ids = [item["product_id"] for item in updated_cart["items"]]
    assert product_to_remove not in remaining_ids
    assert test_products[1]["id"] in remaining_ids


def test_remove_nonexistent_item_from_cart(cart_repo, test_user, test_products):
    cart_repo.add_items_to_user_cart(test_user["id"],
        [{"product_id": p["id"], "quantity": 2} for p in test_products]
    )

    with pytest.raises(ItemNotInCartError):
        cart_repo.remove_item_from_user_cart(test_user["id"], 999999)


def test_update_item_quantity_successfully(cart_repo, test_user, test_products):
    product_id = test_products[0]["id"]
    cart_repo.add_items_to_user_cart(test_user["id"], [{"product_id": product_id, "quantity": 8}])

    updated_cart = cart_repo.update_item_quantity_in_user_cart(test_user["id"], product_id, 5)
    updated_item = next(item for item in updated_cart["items"] if item["product_id"] == product_id)
    assert updated_item["quantity"] == 5
    

def test_update_item_quantity_to_zero_removes_item(cart_repo, test_user, test_products):
    new_cart = cart_repo.get_or_create_cart_by_user(test_user["id"])
    product_id = test_products[1]["id"]
    cart_repo.add_items_to_user_cart(new_cart["user_id"], [{"product_id": product_id, "quantity": 4}])

    updated_cart = cart_repo.update_item_quantity_in_user_cart(new_cart["user_id"], product_id, 0)
    remaining_ids = [item["product_id"] for item in updated_cart["items"]]
    assert product_id not in remaining_ids