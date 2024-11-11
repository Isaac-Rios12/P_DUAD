import pytest

from app.models.user import UserHandler

def test_user_prevent_duplicate_user():
    user_handler = UserHandler()

    user_handler.add_new_user(1, 'joan', 'joanexample', 21)

    duplicate_user = user_handler.add_new_user(1, 'joan', 'joanexample', 21)

    assert duplicate_user is None

def test_user_update_non_existent_field():
    user_handler = UserHandler()

    user_handler.add_new_user(1, "Joan", "example.com", 40)

    user_handler.update_user(1, non_existent_field="nothing")

    user = user_handler.get_user(1)
    assert not hasattr(user, "non_existent_field")

def test_user_add_user_and_update_user_():

    user_handler = UserHandler()

    user_handler.add_new_user(1, "Joan", "joanexample.com", 21)

    user = user_handler.get_user(1)
    assert user.name_user == 'Joan'
    assert user.email == 'joanexample.com'
    assert user.age == 21

    user_handler.update_user(1, name_user='Pedro')

    updated_user = user_handler.get_user(1)
    assert updated_user.name_user == 'Pedro'
    print(updated_user.__dict__)

def test_user_update_user_invalid_value():

    user_handler = UserHandler()

    user_handler.add_new_user(1, "Joan", "joanexample.com", 21)

    user_handler.update_user(1, age = "cien")

    updated_user = user_handler.get_user(1)
    assert updated_user.age == 21
    print(updated_user.__dict__)

def test_user_delete_user():
    user_handler = UserHandler()

    user_handler.add_new_user(2, "Maria", "maria@example.com", 30)
    assert user_handler.get_user(2) is not None

    user_handler.delete_user(2)

    assert user_handler.get_user(2) is None

