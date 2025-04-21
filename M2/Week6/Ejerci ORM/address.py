from tables import address_table
from db_setup import DatabaseRepo

class AddressRepository:
    def __init__(self):
        self.db = DatabaseRepo()
        self.address_table = address_table

    def _format_address(self, address_record):
        return {
            "Address ID": address_record[0],
            "street": address_record[1],
            "city": address_record[2],
            "state": address_record[3],
            "user Id": address_record[4]
        }

    def create_new_address(self, street, city, state, user_id):
        try:
            stmt = self.address_table.insert().values(street=street, city=city, state=state, user_id=user_id)
            execute_stmt = self.db.execute(stmt, True)
            return execute_stmt
        except Exception as e:
            print(f"Error  {e}")

    def modify_address(self, id_to_modify, street, city, state):
        try:
            stmt = self.address_table.update().where(self.address_table.c.id == id_to_modify).values(street=street, city=city, state=state)
            execute_stmt = self.db.execute(stmt, True)
            return execute_stmt
        except Exception as e:
            print(f"Error  {e}")

    def delete_address(self, address_id):
        try:
            stmt = self.address_table.delete().where(self.address_table.c.id == address_id)
            execute_stmt = self.db.execute(stmt, True)

            if execute_stmt.rowcount > 0:
                print("Address deleted")
            else:
                print("Address not found")
        except Exception as e:
            print(f"Error {e}")

    def get_all_address(self):
        try:
            stmt = self.address_table.select()
            execute_stmt = self.db.execute(stmt)
            addresses = execute_stmt.fetchall()
            formated_addresses = [self._format_address(address) for address in addresses]
            return formated_addresses

        except Exception as e:
            print(f"Error {e}")
            
def get_validated_int(prompt):
    value = input(prompt)
    if not value.isdigit():
        print("Error: debe ser un número válido.")
        return None
    return int(value)


def request_address_data(is_new=False):
    street = input("Ingrese street: ")
    city = input("Ingrese la ciudad: ")
    state = input("Ingrese el estado: ")

    if is_new:
        user_id = get_validated_int("Ingrese el ID del usuario de esta dirección: ")
        if user_id is None:
            return None
        return street, city, state, user_id
    else:
        return street, city, state


def address_main():
    address = AddressRepository()
    try:
        while True:
            print(
                """\nMódulo de Direcciones
1. Agregar dirección
2. Modificar dirección
3. Eliminar dirección
4. Ver todas las direcciones"""
            )
            option = get_validated_int("Ingrese la opción necesaria: ")
            if option is None:
                continue

            if option == 1:
                data = request_address_data(is_new=True)
                if not data:
                    continue
                street, city, state, user_id = data
                address.create_new_address(street, city, state, user_id)
                print("Dirección creada exitosamente.")

            elif option == 2:
                address_id = get_validated_int("Ingrese el ID de la dirección a editar: ")
                if address_id is None:
                    continue
                new_street, new_city, new_state = request_address_data()
                address.modify_address(address_id, new_street, new_city, new_state)
                print("Dirección modificada.")

            elif option == 3:
                address_id = get_validated_int("Ingrese el ID de la dirección a eliminar: ")
                if address_id is None:
                    continue
                address.delete_address(address_id)

            elif option == 4:
                addresses = address.get_all_address()
                if not addresses:
                    print("No hay direcciones registradas.")
                else:
                    for addr in addresses:
                        print(addr)

    except Exception as e:
        return f"Error: {e}"