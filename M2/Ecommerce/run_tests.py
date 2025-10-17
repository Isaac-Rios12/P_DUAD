import pytest
import sys

def main():
    #los tests estan separados en estas carpetas
    #test_path = ["test/routes", "tests/repositories"]


    print("Which test do ypu wnant to run")
    print("1. Route tests")
    print("2. Repository tests")
    print("3. All tests")

    choice = input("Which tests do you want to run? 1. Routes  2. Repositories  3. All: ")
    try:
        choice = int(choice.strip())  # elimina espacios y convierte a entero
    except ValueError:
        print("Please enter a valid number")
        exit()  # sale si no es un número

    if choice == 1:
        test_paths = ["tests/routes"]
    elif choice == 2:
        test_paths = ["tests/repositories"]
    elif choice == 3:
        test_paths = ["tests/routes", "tests/repositories"]
    else:
        print("Invalid choice")
        exit()  # sale si no es una opción válida

    print(f"\nRunning tests for option {choice}...\n")


    result = pytest.main(test_paths + ["-q", "--disable-warnings"])

    # result devuelve:
    # # 0 = todos pasaron
    # 1 = tests fallidos
    # 2 = interrupción
    # 3 = tests con error de configuración
    # 4 = pytest usage error

    if result == 0:
        print("\n All tests passed")
    else:
        print(f"\n Some tests failed (exit code {result})")

if __name__ == "__main__":
    main()