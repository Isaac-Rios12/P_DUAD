from unittest.mock import patch
import json
from repositories.product_repo import ProductNotFoundError, ProductCreationError


@patch("routes.product_api.cache_manager.get_data")
def test_get_all_products_from_cache_success(mock_get_data, client):
    products = [{"id": 1, "name": "dog food"}, {"id": 2, "name": "cat food"}]

    mock_get_data.return_value = json.dumps(products)

    response = client.get("products/all-products")
    assert response.status_code == 200
    data = response.get_json()
    assert "products" in data

@patch("routes.product_api.cache_manager.store_data")
@patch("routes.product_api.product_repo.get_all_products")
@patch("routes.product_api.cache_manager.get_data")
def test_get_all_products_from_repo_success(mock_get_data, mock_get_all_products, mock_store_data, client):
    mock_get_data.return_value = None

    products = [{"id": 1, "name": "dog food"}, {"id": 2, "name": "cat food"}]
    mock_get_all_products.return_value = products

    response = client.get("products/all-products")
    assert response.status_code == 200

    data = response.get_json()
    assert "products" in data

    #verifico que se huarda la dataa
    mock_store_data.assert_called_once_with("products:all", json.dumps(products), time_to_live=300)

@patch("routes.product_api.product_repo.get_all_products")
@patch("routes.product_api.cache_manager.get_data", return_value = None)
def test_get_all_products_no_products(mock_get_data, mock_get_all_products, client):
    mock_get_all_products.return_value = []

    response = client.get("/products/all-products")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "No products found"

@patch("routes.product_api.product_repo.get_all_products")
@patch("routes.product_api.cache_manager.get_data", return_value = None)
def test_get_all_products_product_notfound_exception(mock_get_data, mock_get_all_products, client):
    mock_get_all_products.side_effect = ProductNotFoundError("no products in bd")

    response = client.get("/products/all*products")
    assert response.status_code == 404

@patch("routes.product_api.cache_manager.get_data")
def test_get_all_products_cache_get_failure_returns_500(mock_get_data, client):
    #error desde el cache redis
    mock_get_data.side_effect = Exception("Redis Down")

    response = client.get("/products/all-products")
    assert response.status_code == 500

    data = response.get_json()
    assert data["error"] == "Internal Error"

@patch("routes.product_api.cache_manager.store_data") 
@patch("routes.product_api.product_repo.get_all_products") 
@patch("routes.product_api.cache_manager.get_data")
def test_get_all_products_cache_store_failure_returns_500(mock_get_data, mock_get_all_products, mock_store_data, client):
    #sin data en redis
    mock_get_data.return_value = None
    products = [{"id": 1, "name": "dog food"}, {"id": 2, "name": "cat food"}]
    mock_get_all_products.return_value = products

    #error al guardar data
    mock_store_data.side_effect = Exception("Redis store failed")


    response = client.get("/products/all-products")
    assert response.status_code == 500

    data = response.get_json()
    assert data["error"] == "Internal Error"


##############################################
@patch("routes.product_api.cache_manager.get_data")
def test_get_product_by_id_from_cache_success(mock_get_data, client):
    product = {"id": 1, "name": "dog food"}
    mock_get_data.return_value = json.dumps(product)

    response = client.get("products/1")

    assert response.status_code == 200
    data = response.get_json()
    assert data["Product"] == product 


@patch("routes.product_api.cache_manager.store_data")
@patch("routes.product_api.product_repo.get_product_by_id")
@patch("routes.product_api.cache_manager.get_data")
def test_get_product_by_id_from_db_success(mock_get_data, mock_get_product_by_id, mock_store_data, client):
    mock_get_data.return_value = None
    product = {"id": 1, "name": "dog food"}
    mock_get_product_by_id.return_value = product

    response = client.get("products/1")

    assert response.status_code == 200
    mock_store_data.assert_called_once()


@patch("routes.product_api.product_repo.get_product_by_id")
@patch("routes.product_api.cache_manager.get_data")
def test_get_product_by_id_not_found(mock_get_data, mock_get_product_by_id, client):
    mock_get_data.return_value = None
    mock_get_product_by_id.return_value = None

    response = client.get("products/999")

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "No products found"

@patch("routes.product_api.cache_manager.store_data")
@patch("routes.product_api.product_repo.get_product_by_id")
@patch("routes.product_api.cache_manager.get_data")
def test_get_product_by_id_store_failure_returns_500(mock_get_data, mock_get_product_by_id, mock_store_data, client):
    mock_get_data.return_value = None
    product = {"id": 1, "name": "dog food"}
    mock_get_product_by_id.return_value = product

    mock_store_data.side_effect = Exception("Redis store failed")

    response = client.get("products/1")

    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Internal error"

#########################################

@patch("routes.product_api.cache_manager.delete_data")
@patch("routes.product_api.cache_manager.delete_data_with_pattern")
@patch("routes.product_api.product_repo.create_product")
@patch("auth.jwt_instance.jwt_instance.decode",  return_value={"id": 1, "role": "Admin"})
def test_register_product_success(mock_jwt_instance, mock_create_product, mock_delete_pattern, mock_delete_data, client):
    product = {"id": 1, "name": "dog food", "description": "good", "price": 20.0, "stock": 10}
    mock_create_product.return_value = product

    response = client.post(
        "products/register",
        json = {"name": "dog food", "description": "good", "price": 1.00, "stock": 10},
        headers = {"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['New product'] ==  product
    mock_create_product.assert_called_once()

@patch("auth.jwt_instance.jwt_instance.decode",  return_value={"id": 1, "role": "Admin"})
def tes_register_product_missing_fields(mock_jwt_decode, client):
    response = client.post(
        "products/register",
        json = {"name": "cat food"},
        headers = {"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert "Missing data" in data["Error"]

@patch("auth.jwt_instance.jwt_instance.decode",  return_value={"id": 1, "role": "Admin"})
def test_register_product_with_negative_price_or_stock(mock_jwt_decode, client):
    response = client.post(
        "products/register",
        json = {"name": "dog", "description": "food", "price": -5, "stock": 10},
        headers = {"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 400

@patch("auth.jwt_instance.jwt_instance.decode",  return_value={"id": 1, "role": "Admin"})
def test_register_product_with_invalid_types(mock_jwt_decode, client):
    response = client.post(
        "products/register",
        json={"name": "dog", "description": "food", "price": "abc", "stock": "xyz"},
        headers = {"Authorization": "Bearer fake-token"}
    )

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Price must be a number and stock an integer"

@patch("routes.product_api.product_repo.create_product", side_effect=ProductCreationError("fail"))
@patch("auth.jwt_instance.jwt_instance.decode",  return_value={"id": 1, "role": "Admin"})
def test_register_product_repo_error(mock_jwt_decode, mock_create_product, client):
    response = client.post(
        "products/register",
        json={"name": "dog", "description": "food", "price": 10, "stock": 5},
        headers={"Authorization": "Bearer fake-token"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["Message"] == "Error creating the product"