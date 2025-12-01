import pytest
from repositories.user_repo import (
    UserRepository, UserRepositoryError, UserCreationError,
    UserNotFoundError
)
def test_insert_user_and_check(user_repo, unique_user_data):
    new_user = user_repo.create_user(**unique_user_data)

    assert new_user["nickname"] == unique_user_data["nickname"]

    all_users = user_repo.get_all_users()
    nicknames = [user["nickname"] for user in all_users]
    assert new_user["nickname"] in nicknames


def test_hash_password_and_verify(user_repo):
    raw_password = "mipassegura"
    hashed = user_repo._hash_password(raw_password)

    assert hashed != raw_password
    assert user_repo._verify_password(raw_password, hashed)
    assert not user_repo._verify_password("incorrecta", hashed)


def test_login_user_success(user_repo, unique_user_data):
    user_repo.create_user(**unique_user_data)

    user_logged = user_repo.get_user_for_login(
        unique_user_data["nickname"], unique_user_data["password"]
    )
    assert user_logged is not None
    assert user_logged["nickname"] == unique_user_data["nickname"]


def test_login_user_wrong_password(user_repo, unique_user_data):
    user_repo.create_user(**unique_user_data)

    with pytest.raises(UserRepositoryError) as exc_info:
        user_repo.get_user_for_login(unique_user_data["nickname"], "wrong_password")

    assert "Contraseña incorrecta" in str(exc_info.value)


def test_delete_user_error(user_repo, unique_user_data):
    user = user_repo.create_user(**unique_user_data)
    user_id = user["id"]

    # Elimina el usuario
    user_repo.delete_user(user_id)

    with pytest.raises(UserNotFoundError):
        user_repo.get_user_by_id(user_id)


def test_create_duplicate_data(user_repo, unique_user_data):
    user_repo.create_user(**unique_user_data)

    with pytest.raises(UserCreationError) as exc_info:
        user_repo.create_user(**unique_user_data)

    assert "llave duplicada" in str(exc_info.value).lower()
