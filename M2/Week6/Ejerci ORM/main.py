# from db_setup import DatabaseRepo, engine
from tables import create_metadata
from user import user_main
from car import car_main
from address import address_main



def main():
    create_metadata()
    try:

        while True:
        
            print("""                 BIENVENIDO
                1. USUARIOS
                2. AUTOMOVILES
                3. DIRECCIONES
                4. Salir
                """)
            option = input("Ingrese la opcion necesaria...")
            if not option.isdigit():
                print("Invalido, debes ingresar un digito...")
                continue
            option = int(option)
            if option == 1:
                user_main()
            if option == 2:
                car_main()
            if option == 3:
                address_main()
            if option == 4:
                break

    except Exception as e:
        print(f"Error...{e}")


main()

        
