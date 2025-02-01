import sys
import os

# Agregar la carpeta raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

print("PYTHONPATH:", sys.path)  # Para verificar

import pytest
from services.user_service import UserManager

@pytest.fixture
def user_manager():
    return UserManager()

def test_get_users(user_manager):
    users = user_manager.get_users()

    print("Usuarios obtenidos:", users)
    assert isinstance(users, list)

# Ejecutar pytest al final
if __name__ == "__main__":
    pytest.main()


'''
import pytest
pytest.main()
from services.user_service import UserManager

@pytest.fixture
def user_manager():
    return UserManager()

def test_get_users(user_manager):
    users = user_manager.get_users()

    print("Usuarios obtenidos:", users)
    assert isinstance(users, list)
'''


