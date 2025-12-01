import pytest
from unittest.mock import patch
from routes.user_api import UserNotFoundError, UserCreationError

@patch("routes.user_api.get_current_user")
def test_me_success(mock_get_user, client):
    mock_get_user.return_value = {"id": 1, "fullname": "Joan Rios"}
    response = client.get("users/me")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1

def test_register_missing_fields(client):
    response = client.post("/users/register", json={"fullname": "Joan"})
    assert response.status_code == 400
    data = response.get_json()
    #print(data)
    assert "Missing data" in data["error"]

@patch("routes.user_api.role_repo.get_role_by_name")
def test_register_user_with_not_found_role(mock_get_role, client):
    mock_get_role.return_value = None
    payload = {
        "fullname": "Joan", "nickname": "Joan", "email": "joan@gmail.com", "password": "1234"
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == 500

@patch("routes.user_api.jwt_instance.encode")
@patch("routes.user_api.user_repo.create_user")
@patch("routes.user_api.role_repo.get_role_by_name")
def test_register_with_success( mock_get_role, mock_create_user, mock_jwt_encode, client):
    mock_get_role.return_value = {"id": 1, "name": "user"}

    mock_create_user.return_value = {
        "id": 123,
        "fullname": "Joan Rios",
        "nickname": "joan",
        "email": "joan@mail.com",
        "role_name": "user"
    }

    mock_jwt_encode.return_value = "fake-jwt-token"

    payload = {
        "fullname": "Joan Rios",
        "nickname": "joan",
        "email": "joan@mail.com",
        "password": "1234"
    }

    response = client.post("/users/register", json=payload)

    assert response.status_code == 201
    data = response.get_json()

    assert data["message"] == "User registered successfully"
    assert data["token"] == "fake-jwt-token"
    assert data["user"]["id"] == 123
    assert data["user"]["nickname"] == "joan"

@patch("routes.user_api.jwt_instance.encode")
@patch("routes.user_api.user_repo.get_user_for_login")
def test_login_with_success(mock_get_user_for_login, mock_jwt_encode, client):
    mock_get_user_for_login.return_value = {"id": 123, "nickname": "joan", "password": "1234", "role_name": "user"}
    mock_jwt_encode.return_value = "fake-jwt-token"

    payload = {
        "id": 123,
        "nickname": "joan",
        "password": "1234",
        "role_name": "user"
    }

    response = client.post("/users/login", json=payload)
    
    assert response.status_code == 200

@patch("routes.user_api.user_repo.get_user_for_login")
def test_login_user_not_found(mock_get_user_for_login, client):

    mock_get_user_for_login.return_value = None

    payload = {
        "nickname": "no-existe",
        "password": "no-existe"
    }

    response = client.post("/users/login", json=payload)

    assert response.status_code == 406
    data = response.get_json()
    assert data["error"] == "Invalid nickname or password"


@patch("routes.user_api.user_repo.get_user_for_login")
def test_login_incomplete_data(mock_get_user_for_login, client):

    mock_get_user_for_login.return_value = {
        "id": 123, 
        "nickname": "joan", 
        "password": "1234", 
        "role_name": "user"}
    
    

    payload = {
        "nickname": "no-existe"
    }

    response = client.post("/users/login", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "nickname or password not found"

@patch("routes.user_api.user_repo.get_user_for_login")
def test_login_Unexpected_error(mock_get_user_for_login, client):

    mock_get_user_for_login.side_effect = Exception("Database connection lost")

    
    

    payload = {
        "nickname": "joan",
        "password": "pass"
    }

    response = client.post("/users/login", json=payload)

    assert response.status_code == 500
    data = response.get_json()
    assert data["error"] == "Internal server error"

@patch("routes.user_api.user_repo.update_user")
@patch("routes.user_api.get_current_user")
def test_update_user_with_success(mock_get_current_user, mock_update_user, client):
    mock_get_current_user.return_value = {
        "id": 123,
        "name": "Joan"
    }

    mock_update_user.return_value = {
        "id": "123",
        "email": "joan_new@mail.com",
        "password": "newpass"
    }

    payload = {
        "email": "joan_new@mail.com",
        "password": "newpass"
    }

    response = client.patch("/users/update", json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User updated successfully"
    assert data["user"]["email"] == "joan_new@mail.com"

@patch("routes.user_api.get_current_user")
def test_update_user_no_data(mock_get_current_user, client):
    mock_get_current_user.return_value = {
        "id": 123,
        "nickname": "joan"
    }
    payload = {}

    response = client.patch("/users/update", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Request body is missing"

@patch("routes.user_api.get_current_user")
def test_update_user_missing_password(mock_get_current_user, client):
    mock_get_current_user.return_value = {
        "id": 123,
        "nickname": "joan"
    }
    payload = {"email": "joan@gmail.com"}

    response = client.patch("/users/update", json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Missing data: password"

@patch("routes.user_api.get_current_user")
def test_update_user_missing_current_user(mock_get_current_user, client):
    mock_get_current_user.return_value = {}
    payload = {"email": "joan@gmail.com",
               "password": "1232"}

    response = client.patch("/users/update", json=payload)

    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] ==  "No authenticated user found"


#se mockea para ser usado en el decorador del endpoint, se usa en el token_required_admin
@patch("routes.user_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.user_api.user_repo.get_user_by_id")
def test_get_user_by_admin_success(mock_get_user_by_id, mock_jwt_decode, client):
    mock_get_user_by_id.return_value = {
        "id": 123,
        "nickname": "joan",
        "email": "joan@gmail.com"
    }

    headers = {"Authorization": "Bearer fake-admin-token"}
    user_id = 123
    response = client.get(f"/users/{user_id}", headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['User']["id"] == 123

#se mockea para ser usado en el decorador del endpoint, se usa en el token_required_admin
@patch("routes.user_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.user_api.user_repo.get_user_by_id")
def test_get_user_by_admin_success(mock_get_user_by_id, mock_jwt_decode, client):
    mock_get_user_by_id.return_value = {
        "id": 123,
        "nickname": "joan",
        "email": "joan@gmail.com"
    }

    headers = {"Authorization": "Bearer fake-admin-token"}
    user_id = 123
    response = client.get(f"/users/{user_id}", headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    assert data['User']["id"] == 123

@patch("routes.user_api.user_repo.get_user_by_id")
def test_get_user_by_admin_no_token(mock_get_user_by_id, client):
    #no se envian headers

    user_id = 123
    response = client.get(f"/users/{user_id}")

    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "No token provided"

#se mockea para ser usado en el decorador del endpoint, se usa en el token_required_admin
@patch("routes.user_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.user_api.user_repo.get_user_by_id")
def test_get_user_by_admin_success(mock_get_user_by_id, mock_jwt_decode, client):
    mock_get_user_by_id.return_value = {}

    headers = {"Authorization": "Bearer fake-admin-token"}
    user_id = 999
    response = client.get(f"/users/{user_id}", headers=headers)

    assert response.status_code == 404
    data = response.get_json()
    assert data['error']== "User not found"

#se mockea para ser usado en el decorador del endpoint, se usa en el token_required_admin
@patch("routes.user_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.user_api.user_repo.get_user_by_id")
def test_get_user_by_admin_success(mock_get_user_by_id, mock_jwt_decode, client):
    mock_get_user_by_id.side_effect = Exception("Database down")

    headers = {"Authorization": "Bearer fake-admin-token"}
    user_id = 123
    response = client.get(f"/users/{user_id}", headers=headers)

    assert response.status_code == 500
    data = response.get_json()
    assert data['error']== "Database down"

#se mockea para ser usado en el decorador del endpoint, se usa en el token_required_admin
@patch("routes.user_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.user_api.user_repo.get_all_users")
def test_get_all_users_success(mock_get_all_users, mock_jwt_decode, client):
    mock_get_all_users.return_value = [
        {
            "id": 1,
            "name": "Joan"
        },
        {
            "id": 2,
            "name": "Nicko"
        }
    ]

    headers = {"Authorization": "Bearer fake-admin-token"}
    response = client.get(f"/users/all-users", headers=headers)

    assert response.status_code == 200
    data = response.get_json()
    
#se mockea para ser usado en el decorador del endpoint, se usa en el token_required_admin
@patch("routes.user_api.jwt_instance.decode", return_value={"id": 1, "role": "Admin"})
@patch("routes.user_api.user_repo.get_all_users")
def test_get_all_users_no_users_found(mock_get_all_users, mock_jwt_decode, client):
    mock_get_all_users.return_value = {}

    headers = {"Authorization": "Bearer fake-admin-token"}
    response = client.get(f"/users/all-users", headers=headers)

    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "No users found"



