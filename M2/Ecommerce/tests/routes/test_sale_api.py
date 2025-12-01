import pytest
import threading
import json
from flask.testing import FlaskClient
from unittest.mock import patch
from repositories.sale_repo import SaleCreationError, SaleRepositoryError,SaleNotFoundError

from concurrent.futures import ThreadPoolExecutor, as_completed


@patch("routes.sale_api.get_current_user", return_value = {"id": 1})
@patch("routes.sale_api.sale_repo.create_sale", return_value = {"id": 123, "user_id": 1, "billing_address": "San Jose"})
@patch("routes.sale_api.cache_manager.delete_data")
@patch("routes.sale_api.cache_manager.delete_data_with_pattern")
def test_create_sale_success(mock_delete_pattern, mock_delete_data, mock_create_sale, mock_get_user, client):
    response = client.post("/sales/new-sale", json = {"billing_address": "San Jose"})
    assert response.status_code == 201
    assert response.get_json() == {"id": 123, "user_id": 1, "billing_address": "San Jose"}

    assert mock_delete_data.call_count == 2
    assert mock_delete_pattern.call_count == 2

@patch("routes.sale_api.get_current_user", return_value = {"id": 1})
def test_create_sale_mossong_billing_address_error(mock_get_user, client):
    response = client.post("/sales/new-sale", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "billing_address required"}

@patch("routes.sale_api.get_current_user")
@patch("routes.sale_api.sale_repo.create_sale", side_effect = SaleCreationError("Could not create sale"))
def test_create_sale_creation_error(mock_get_user, mock_create_sale, client):
    response = client.post("/sales/new-sale", json={"billing_address": "San Jose"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Could not create sale"}

@patch("routes.sale_api.get_current_user")
@patch("routes.sale_api.sale_repo.create_sale", side_effect = Exception())
def test_create_sale_creation_error(mock_get_user, mock_create_sale, client):
    response = client.post("/sales/new-sale", json={"billing_address": "San Jose"})
    assert response.status_code == 500
    assert response.get_json() == {"error": "Internal server error"}

##################################################
@patch("routes.sale_api.get_current_user", return_value = {"id": 1})
@patch("routes.sale_api.sale_repo.get_sales_by_user", return_value = [
    {"id": 1, "billing_address": "San Jose", "total": 5000},
    {"id": 2, "billing_address": "San Jose", "total": 10000}
])
def test_get_my_sales_success(mock_get_sales, mock_get_user, client):
    response = client.get("/sales/my-sales")
    assert response.status_code == 200
    mock_get_sales.assert_called_once_with(1)\
    
@patch("routes.sale_api.get_current_user", side_effect = PermissionError("Unauthorized access"))
def test_get_my_sales_permission_error(mock_get_user, client):
    response = client.get("sales/my-sales")
    assert response.status_code == 401
    assert response.get_json() == {"error": "Unauthorized access"}

@patch("routes.sale_api.get_current_user", return_value = {"id": 1})
@patch("routes.sale_api.sale_repo.get_sales_by_user", side_effect = SaleNotFoundError("No sales found"))
def test_get_my_sales_nof_found_error(mock_get_sales, mock_get_user, client):
    response = client.get("/sales/my-sales")
    assert response.status_code == 404
    assert response.get_json() == {"error": "No sales found"}

@patch("routes.sale_api.get_current_user", return_value={"id": 1})
@patch("routes.sale_api.sale_repo.get_sales_by_user", side_effect=SaleRepositoryError("DB failure"))
def test_get_my_sales_repository_error(mock_get_sales, mock_get_user, client):
    response = client.get("/sales/my-sales")
    assert response.status_code == 500
    assert response.get_json() == {"error": "DB failure"}

###################

@patch("routes.sale_api.get_current_user", return_value = {"id": 1})
@patch("routes.sale_api.sale_repo.get_sale_by_id", return_value = {"id": 10, "total": 56000})
def test_get_my_sale_success(mock_get_sale, mock_get_user, client):
    response = client.get("sales/my-sales/10")
    assert response.status_code == 200
    assert response.get_json() == {"id": 10, "total": 56000}

@patch("routes.sale_api.get_current_user", return_value = {"id": 1})
@patch("routes.sale_api.sale_repo.get_sale_by_id", side_effect = SaleNotFoundError("Sale not found"))
def test_get_my_sale_not_found_error(mock_get_sale, mock_get_user, client):
    response = client.get("sales/my-sales/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Sale not found"}

@patch("routes.sale_api.get_current_user", side_effect = PermissionError("Not allowed"))
def test_get_my_sale_permission_error(mock_get_user, client):
    response = client.get("sales/my-sales/999")
    assert response.status_code == 401
    assert response.get_json() == {"error": "Not allowed"}

@patch("routes.sale_api.get_current_user", return_value={"id": 1})
@patch("routes.sale_api.sale_repo.get_sale_by_id", side_effect=SaleRepositoryError("Database failure"))
def test_get_my_sale_repository_error(mock_get_sale, mock_get_user, client):
    response = client.get("/sales/my-sales/5")
    
    assert response.status_code == 500
    assert response.get_json() == {"error": "Database failure"}

####################

@patch("routes.sale_api.jwt_instance.decode", return_value = {"id": 1, "role": "Admin"})
@patch("routes.sale_api.cache_manager.get_data")
def test_get_sale_admin_from_cache(mock_cache_get, mock_jwt_decode, client):
    sale_id = 10
    cached_sale = {"id": sale_id, "billing_address": "cr", "total": 10000}
    mock_cache_get.return_value = json.dumps(cached_sale)

    headers = {"Authorization": "Bearer fake-admin-token"}
    response = client.get(f"sales/admin/{sale_id}", headers=headers)

    assert response.status_code == 200
    assert response.get_json() == cached_sale


@patch("routes.sale_api.jwt_instance.decode", return_value = {"id": 1, "role": "Admin"})
@patch("routes.sale_api.cache_manager.store_data")
@patch("routes.sale_api.cache_manager.get_data", return_value = None)
@patch("routes.sale_api.sale_repo.get_sale_by_id_admin")
def test_get_sale_admin_no_cache_success(mock_get_sale, mock_get_data, mock_store_data, mock_jwt, client):
    sale_id = 10
    sale_data = {"id": sale_id, "billng_address": "cr", "total": 10000}
    mock_get_sale.return_value = sale_data

    headers = {"Authorization": "Bearer fake-admin-token"}
    response = client.get(f"/sales/admin/{sale_id}", headers=headers)

    assert response.status_code == 200
    assert response.get_json() == sale_data

@patch("routes.sale_api.jwt_instance.decode", return_value = {"id": 1, "role": "Admin"})
@patch("routes.sale_api.cache_manager.get_data", return_value = None)
@patch("routes.sale_api.sale_repo.get_sale_by_id_admin", side_effect = SaleNotFoundError("Sale not found"))
def test_get_sale_admin_not_sale_found_error(mock_get_sale, mock_cache_get, mock_jwt_decode, client):
    sale_id = 99
    headers = {"Authorization": "Bearer fake-admin-token"}

    response = client.get(f"sales/admin/{sale_id}", headers=headers)
    response.status_code = 404
    assert response.get_json() == {"error": "Sale not found"}



@patch("routes.sale_api.jwt_instance.decode", return_value = {"id": 1, "role": "Admin"})
@patch("routes.sale_api.cache_manager.get_data", return_value = None)
@patch("routes.sale_api.sale_repo.get_sale_by_id_admin", side_effect = SaleRepositoryError("DB error"))
def test_get_sale_admin_repository_error(mock_get_sale, mock_cache_get, mock_jwt_decode, client):
    sale_id = 10
    headers = {"Authorization": "Bearer fake-admin-token"}

    response = client.get(f"sales/admin/{sale_id}", headers=headers)
    assert response.status_code == 500
    assert response.get_json() == {"error": "DB error"}


@patch("routes.sale_api.jwt_instance.decode", side_effect=Exception("Invalid token"))
def test_get_sale_admin_invalid_token(mock_jwt_decode, client):
    sale_id = 1
    headers = {"Authorization": "Bearer invalid-token"}

    response = client.get(f"/sales/admin/{sale_id}", headers=headers)
    assert response.status_code == 401
    data = response.get_json() == "Invalid token"


######################################
@patch("routes.sale_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.sale_api.cache_manager.store_data")
@patch("routes.sale_api.cache_manager.get_data", return_value=None)
@patch("routes.sale_api.sale_repo.get_all_sales")
def test_get_all_sales_admin_no_cache(mock_get_all_sales, mock_get_data, mock_store_data, mock_jwt_decode, client):
    sales = [{"id": 1, "total": 100}, {"id": 2, "total": 50}]
    mock_get_all_sales.return_value = sales

    response = client.get("/sales/admin/all-sales", headers={"Authorization": "Bearer fake-admin-token"})
    assert response.status_code == 200
    assert response.get_json() == sales

@patch("routes.sale_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.sale_api.cache_manager.get_data")
def test_get_all_sales_admin_from_cache(mock_get_data, mock_jwt_decode, client):
    cached_sales = [{"id": 1, "total": 100}, {"id": 2, "total": 50}]
    mock_get_data.return_value = json.dumps(cached_sales)

    response = client.get("/sales/admin/all-sales", headers={"Authorization": "Bearer fake-admin-token"})
    assert response.status_code == 200
    assert response.get_json() == cached_sales

@patch("routes.sale_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.sale_api.cache_manager.get_data", return_value=None)
@patch("routes.sale_api.sale_repo.get_all_sales", side_effect = Exception())
def test_get_all_sales_admin_repo_error(mock_get_all_sales, mock_get_data, mock_jwt_decode, client):
    response = client.get("/sales/admin/all-sales", headers={"Authorization": "Bearer fake-admin-token"})
    assert response.status_code == 500
    assert response.get_json() == {"error": "Internal server error"}


@patch("routes.sale_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.sale_api.cache_manager.get_data", return_value=None)
@patch("routes.sale_api.sale_repo.get_all_sales", side_effect = SaleNotFoundError("No sales found"))
def test_get_all_sales_admin_not_found(mock_get_all_sales, mock_get_data, mock_jwt_decode, client):
    mock_get_all_sales.return_value = []
    
    response = client.get("/sales/admin/all-sales", headers={"Authorization": "Bearer fake-admin-token"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "No sales found"}




# @pytest.mark.parametrize("threads", [5])
# @patch("routes.sale_api.get_current_user", return_value = {"id": 4, "username": "Joan"})
# def test_concurrent_create_sale(mock_user, client: FlaskClient, threads):
#     results = []
#     lock = threading.Lock()

#     def make_request():
#         response = client.post("sales/new-sale", json = {"billing_address": "calle falsa"})
#         data = {"status": response.status_code, "body": response.get_json()}
#         with lock:
#             results.append(data)
        
#     thread_list = [threading.Thread(target=make_request) for _ in range(threads)]
#     for t in thread_list:
#         t.start()
#     for t in thread_list:
#         t.join()

#     for i, result in enumerate(results, 1):
#         print(f"--> Respuesta {i}: {result}")

#     assert len(results) == threads
#     #assert all("error" not in r["body"] for r in results), "Alguna venta fallo"





# # Usuarios que queremos probar
# users = [
#     {"id": 702},
#     {"id": 703},
#     {"id": 704},
# ]

# billing_address = "Calle Falsa 123"
# product_id = 2

# def test_concurrent_sales_real_users(client):
#     """
#     Test concurrente para usuarios 702,703,704 comprando producto 2
#     con stock limitado (2 unidades).
#     """

#     results = []
#     lock = threading.Lock()

#     def make_purchase(user):
#         # Mockeamos get_current_user para cada hilo
#         with patch("routes.sale_api.get_current_user", return_value=user):
#             response = client.post("sales/new-sale", json={"billing_address": billing_address})
#             with lock:
#                 results.append({
#                     "user_id": user["id"],
#                     "status": response.status_code,
#                     "body": response.get_json()
#                 })

#     # Crear y lanzar hilos
#     threads = [threading.Thread(target=make_purchase, args=(u,)) for u in users]
#     for t in threads:
#         t.start()
#     for t in threads:
#         t.join()

#     # Imprimir resultados
#     for r in results:
#         print(r)

#     # Separar ventas exitosas y fallidas
#     success = [r for r in results if r["status"] == 201]
#     fail = [r for r in results if r["status"] != 201]

#     print(f" Ventas exitosas: {len(success)}")
#     print(f" Ventas fallidas: {len(fail)}")

#     # Validaciones
#     # assert len(results) == 3, "Deben ejecutarse 3 peticiones"
#     # assert len(success) <= 2, "No se puede vender más unidades que el stock disponible"



# Suponiendo que tu cliente de Flask está disponible como "client"
# y get_current_user ya está mockeado para retornar el user_id correcto

# users = [
#     {"id": 702, "billing_address": "Calle Falsa 123"},
#     {"id": 703, "billing_address": "Calle Falsa 123"},
#     {"id": 704, "billing_address": "Calle Falsa 123"},
# ]

# def make_sale_request(client, user):
#     """Hace la petición POST al endpoint /new-sale."""
#     # Mockeamos get_current_user para cada petición
#     from routes.sale_api import get_current_user

#     with patch("routes.sale_api.get_current_user", return_value={"id": user["id"]}):
#         resp = client.post(
#             "sales/new-sale",
#             json={"billing_address": user["billing_address"]}
#         )
#         return {"user_id": user["id"], "status": resp.status_code, "body": resp.get_json()}

# @pytest.mark.parametrize("concurrent_users", [users])
# def test_concurrent_sales_api(client, concurrent_users):
#     results = []

#     with ThreadPoolExecutor(max_workers=len(concurrent_users)) as executor:
#         futures = [executor.submit(make_sale_request, client, user) for user in concurrent_users]

#         for future in as_completed(futures):
#             results.append(future.result())

#     # Contar ventas exitosas y fallidas
#     success = [r for r in results if r["status"] == 201]
#     failed = [r for r in results if r["status"] != 201]

#     # Mostrar resultados
#     for r in results:
#         print(r)

#     print(f"✅ Ventas exitosas: {len(success)}")
#     print(f"❌ Ventas fallidas: {len(failed)}")

#     # Assert: Si stock inicial = 2 y cada usuario quiere 1 unidad, máximo 2 ventas exitosas
#     assert len(success) <= 2
#     assert len(failed) >= 1



