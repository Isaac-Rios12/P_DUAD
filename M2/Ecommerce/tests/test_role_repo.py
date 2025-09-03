import pytest
from db.manager import DatabaseManager
from repositories.role_repo import RoleRepository, RoleCreationError, RoleNotFoundError, RoleRepositoryError

import uuid

def generate_unique_role_name(base_name="Role"):
    return f"{base_name}_{uuid.uuid4().hex[:8]}"

def test_add_role_and_success(role_repo):
    role_name = generate_unique_role_name("Admin")
    role = role_repo.create_role(role_name)
    assert role["name"] == role_name

def test_create_role_with_duplicate_name_raises_error(role_repo):
    role_name = f"duplicate_role_{uuid.uuid4().hex[:8]}"

    role_repo.create_role(role_name)

    with pytest.raises(RoleCreationError) as exc_info:
        role_repo.create_role(role_name)
    
    assert "llave duplicada" in str(exc_info.value).lower()
def test_try_delete_non_existing_role(role_repo):
    role_name = f"delete_role_{uuid.uuid4().hex[:8]}"
    

    delete_role = role_repo.create_role(role_name)
    role_id_to_delete = delete_role["id"]

    role_repo.delete_role(role_id_to_delete)

    with pytest.raises(RoleNotFoundError):
        role_repo.get_role_by_id(role_id_to_delete)

def test_get_role_by_id(role_repo):
    role_name = f"get_id_{uuid.uuid4().hex[:8]}"
    new_role = role_repo.create_role(role_name)
    role_id = new_role["id"]

    fetched_role = role_repo.get_role_by_id(role_id)
    
    assert fetched_role["id"] == role_id
    assert fetched_role["name"] == role_name

def test_get_role_by_id_not_found(role_repo):
    with pytest.raises(RoleNotFoundError):
        role_repo.get_role_by_id(7777777777)
    
def test_update_role(role_repo):
    role_name = f"to_update_{uuid.uuid4().hex[:8]}"
    new_role = role_repo.create_role(role_name)
    role_id = new_role["id"]

    updated_name = f"already_updated_{uuid.uuid4().hex[:8]}"
    update_role = role_repo.update_role(role_id, updated_name)

    assert update_role["id"] == role_id
    assert update_role["name"] == updated_name

def test_updated_role_not_found(role_repo):
    invalid_id = 9999999
    with pytest.raises(RoleNotFoundError):
        role_repo.update_role(invalid_id, "new_name")

