from unittest.mock import patch
from repositories.cart_repo import (CartNotFoundError, InvalidCartIdentifierError, CartRepositoryError, 
                                    ProductNotFoundError, InsufficientStockError, ItemNotInCartError)

@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.get_or_create_cart_by_user")
def test_get_cart_success(mock_get_cart, mock_get_user, client):
    cart = {"user_id": 1, "items": []}
    mock_get_cart.return_value = cart

    response = client.get("carts/")
    assert response.status_code == 200
    assert response.get_json() == cart


@patch("routes.cart_api.get_current_user", return_value = {"id": 1})
@patch("routes.cart_api.cart_repo.get_or_create_cart_by_user", side_effect = CartNotFoundError("Cart not found"))
def test_get_cart_not_found(mock_get_cart, mock_get_user, client):
    response = client.get("carts/")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Cart not found"}



@patch("routes.cart_api.get_current_user", return_value = {"id": 1})
@patch("routes.cart_api.cart_repo.get_or_create_cart_by_user", side_effect = CartRepositoryError("DB connection failed"))
def test_get_cart_repository_error(mock_get_cart, mock_get_user,client):
    response = client.get("carts/")
    assert response.status_code == 500


@patch("routes.cart_api.get_current_user", side_effect=PermissionError("Not allowed"))
def test_get_cart_permission_error(mock_get_user, client):
    response = client.get("carts/")
    assert response.status_code ==  401
    assert response.get_json()["error"] == "Not allowed"

###########################


@patch("routes.cart_api.get_current_user", return_value = {"id": 1})
@patch("routes.cart_api.cart_repo.delete_cart_by_user")
def test_delete_cart_success(mock_delete_cart, mock_get_user, client):
    response = client.delete("/carts/delete")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Cart deleted successfully"


@patch("routes.cart_api.get_current_user", side_effect = PermissionError("Not allowed"))
def test_delete_cart_permission_error(mock_get_user, client):
    response = client.delete("carts/delete")
    assert response.status_code == 401

@patch("routes.cart_api.get_current_user", return_value = {"id": 1})
@patch("routes.cart_api.cart_repo.delete_cart_by_user", side_effect = CartNotFoundError("Cart not found"))
def test_delete_cart_not_found(mock_delete_cart, mock_get_user, client):
    response = client.delete("carts/delete")
    assert response.status_code == 404

@patch("routes.cart_api.get_current_user", return_value={"id": 1}) 
@patch("routes.cart_api.cart_repo.delete_cart_by_user", side_effect=CartRepositoryError("DB error")) 
def test_delete_cart_repository_error(mock_delete_cart, mock_get_user, client): 
    response = client.delete("carts/delete") 
    assert response.status_code == 500 
    assert response.get_json()["error"] == "DB error"



###################################
@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.add_items_to_user_cart")
def test_add_items_to_cart_success(mock_add_items, mock_get_user, client):
    mock_add_items.return_value = {"id": 1, "items":[{"product_id": 10, "quantity": 2}]}

    response = client.post(
        "carts/add-items",
        json = {"items": [{"product_id": 10, "quantity": 2}]}
    )
    assert response.status_code == 200


@patch("routes.cart_api.get_current_user", return_value={"id": 1})
def test_add_items_missing_items_key_returns_400( mock_get_user, client):
    response = client.post(
        "carts/add-items",
        json = {}
    )
    assert response.status_code == 400


@patch("routes.cart_api.get_current_user", side_effect = PermissionError("Not allowed"))
def test_add_items_permission_error_return_401(mock_get_user, client):
    response = client.post(
        "carts/add-items",
        json = {"items": [{"product_id": 10, "quantity": 2}]}
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Not allowed"



@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.add_items_to_user_cart", side_effect = ProductNotFoundError("Product not found"))
def test_add_items_product_not_found_returns_404(mock_add_items, mock_get_user, client):
    response = client.post(
        "carts/add-items",
        json = {"items": [{"product_id": 9999, "quantity": 2}]}
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"

@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.add_items_to_user_cart", side_effect = InsufficientStockError("Insufficient stock"))
def test_add_items_insufficient_stock_returns_404(mock_add_items, mock_get_user, client):
    response = client.post(
        "carts/add-items",
        json = {"items": [{"product_id": 10, "quantity": 4565}]}
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Insufficient stock"

@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.add_items_to_user_cart", side_effect = CartRepositoryError("DB down"))
def test_add_items_repo_error_returns_500(mock_add_items, mock_get_user, client):
    response = client.post(
        "carts/add-items",
        json = {"items": [{"product_id": 10, "quantity": 100}]}
    )
    assert response.status_code == 500
    assert response.get_json()["error"] == "DB down"

############################
@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.remove_item_from_user_cart", return_value={"id": 1, "items": []})
def test_delete_item_from_cart_success(mock_delete_item, mock_get_user, client):
    response = client.delete("carts/delete-item/10")
    assert response.status_code == 200


@patch("routes.cart_api.get_current_user", side_effect = PermissionError("Not allowed"))
def test_delete_item_from_cart_permission_error(mock_get_user, client):
    response = client.delete("carts/delete-item/10")
    assert response.status_code == 401

@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.remove_item_from_user_cart", side_effect = CartNotFoundError("Cart not found"))
def test_delete_item_cart_not_found_error(mock_delete_item, mock_get_user, client):
    response = client.delete("carts/delete-item/10")
    assert response.status_code == 404
    assert response.get_json()['error'] == "Cart not found"



@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.remove_item_from_user_cart", side_effect = ItemNotInCartError("Item not in cart"))
def test_delete_item_not_in_cart_error(mock_delete_item, mock_get_user, client):
    response = client.delete("carts/delete-item/10")
    assert response.status_code == 404
    assert response.get_json()['error'] == "Item not in cart"

@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.remove_item_from_user_cart", side_effect=CartRepositoryError("DB error"))
def test_delete_item_repo_error(mock_remove_item, mock_get_user, client):
    response = client.delete("/carts/delete-item/10")
    assert response.status_code == 500
    assert response.get_json()['error'] == "DB error"

########################
@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.update_item_quantity_in_user_cart", return_value={"id": 1, "items": [{"product_id": 10, "quantity": 5}]})
def test_update_item_quantity_success(mock_update, mock_get_user, client):
    response = client.patch("/carts/update-quantity/10", json={"new_quantity": 5})
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "items": [{"product_id": 10, "quantity": 5}]}

@patch("routes.cart_api.get_current_user", return_value={"id": 1})
def test_update_item_quantity_missing_field_error(mock_get_user, client):
    response = client.patch("/carts/update-quantity/10", json={})
    assert response.status_code == 400

@patch("routes.cart_api.get_current_user", side_effect = PermissionError("Not allowed"))
def test_update_item_quantity_permission_error(mock_get_user, client):
    response = client.patch("/carts/update-quantity/10", json = {"new_quantity": 3})
    assert response.status_code == 401
    assert response.get_json()["error"] == "Not allowed"


@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.update_item_quantity_in_user_cart", side_effect=InsufficientStockError("Not enough stock"))
def test_update_item_quantity_insufficient_stock(mock_update, mock_get_user, client):
    response = client.patch("/carts/update-quantity/10", json = {"new_quantity": 3})
    assert response.status_code == 400



@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.update_item_quantity_in_user_cart", side_effect=ItemNotInCartError("Item not in cart"))
def test_update_item_quantity_item_not_in_cart_error(mock_update, mock_get_user, client):
    response = client.patch("/carts/update-quantity/10", json = {"new_quantity": 3})
    assert response.status_code == 404

@patch("routes.cart_api.get_current_user", return_value={"id": 1})
@patch("routes.cart_api.cart_repo.update_item_quantity_in_user_cart", side_effect=CartRepositoryError("DB error"))
def test_update_quantity_repo_error(mock_update, mock_get_user, client):
    response = client.patch("/carts/update-quantity/10", json={"new_quantity": 2})
    assert response.status_code == 500
    assert "DB error" in response.get_json()["error"]
#pytest -s -v tests/test_cart_api.py

