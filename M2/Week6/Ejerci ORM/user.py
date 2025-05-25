#from sqlalchemy import select

from tables import user_table

from db_setup import DatabaseRepo

class UserRepository:
    def __init__(self):
        self.db = DatabaseRepo()  #para usar los metodos de datarepo
        self.user_table = user_table

    def _format_user(self, user_record):
        return {
            "id": user_record[0],
            "full_name": user_record[1],
            "email": user_record[2],
            "phone": user_record[3],
        }   

    def get_all_users(self):
        try:  
            stmt = self.user_table.select()
            result = self.db.execute(stmt)
            users = result.fetchall()
            formatted_users = [self._format_user(user) for user in users]
            return formatted_users
        except Exception as e:
            print(f"Error...{e}")
    
    def create_user(self, name, email, phone):
        try:
            stmt = self.user_table.insert().values(name=name, email=email, phone=phone)
            self.db.execute(stmt, True)
            print(f"usuario creado")
        
        except Exception as e:
            print(f"Error {e}")

    def update_user(self, id, new_name, email, phone):
        try:
            stmt = self.user_table.update().where(self.user_table.c.id == id).values(name=new_name, email=email, phone=phone)
            result = self.db.execute(stmt, True)

            if result.rowcount > 0:
                print("Usuario modificado")
            
            else:
                print("No se encontró el usuario para modificar")
    
        except Exception as e:
            print(f"Error {e}")

    def delete_user(self, user_to_delete):
        try:
            stmt = self.user_table.delete().where(self.user_table.c.id == user_to_delete)
            result = self.db.execute(stmt, True)

            if result.rowcount > 0:
                print("User deleted...")
            else:
                print("Usuario no encontrado...")
        except Exception as e:
            print(f"Error {e}")

def request_user_data():
    name = input("Ingresa el nombre... ")
    phone = input("Ingresa el numero telefo... ")
    email = input("Ingresa el email.... ")
    return name, email, phone

def get_validated_int(prompt):
    value = input(prompt)
    if not value.isdigit():
        print("Error: debe ser un número válido.")
        return None
    return int(value)

def user_main():
    user = UserRepository()
    try:
        while True:
            print(""" MODULO USUARIOS
                  1. Agregar usuario
                  2. Modificar Usuario
                  3. Eliminar usuario
                  4. Ver todos los usuarios
                  5. Menu principal""")
            option = input("Ingrese la opcion necesaria...")
            if not option.isdigit():
                print("Error, ingresa un valor valido")
                continue
            option = int(option)
            if option == 1:
                name, email, phone = request_user_data()
                add_user = user.create_user(name, email, phone)


            elif option == 2:
                user_to_search = get_validated_int("Ingrese el ID de la persona a modificar...")
                if user_to_search:
                    name, email, phone = request_user_data()
                    update = user.update_user(user_to_search, name, email, phone)
            elif option == 3:
                id_user_to_delete = get_validated_int("Ingrese el ID de la persona a borrar...")
                if id_user_to_delete:
                    delete = user.delete_user(id_user_to_delete)
            elif option == 4:
                find_all_users = user.get_all_users()
                print(find_all_users)

            elif option == 5:
                break

    except Exception as e:
        return f"Error {e}"
    

# quedo aca, acaba de implemtar en la funcion de eliminar, que me valide si se encontro y elimino
# o no, debo de hacer esto en las demas funciones...
        