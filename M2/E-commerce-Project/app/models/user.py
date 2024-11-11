import os
import json

class User:
    def __init__(self, id_user, name_user, email, age):
        self.id_user = id_user
        self.name_user = name_user
        self.email = email
        self.age = age

   
class UserHandler:
    def __init__(self):
        self.user_list = {}

    def get_user(self, id_user):
        return self.user_list.get(id_user)
    
    def add_new_user(self, user_id, name_user, email, age):

        if not isinstance(user_id, int) or user_id <= 0:
            print("Error, el ID de usuario debe ser un numero entero positivo")
            return None

        if user_id in self.user_list:
            print("El usuario ya se encuentra verificado.")
            return None
        
        if not isinstance(name_user, str) or not name_user.strip():
            print("Error, el nombre de usuario no puede estar vacio")
            return None
        
        if not isinstance(age, int) or not(0 < age < 120):
            print("Error en la edad")
            return None
        
        user = User(user_id, name_user, email, age)
        self.user_list[user_id] = user
        print("Usuario registrado exactamente.....")
        return user

    def delete_user(self, id_user):

        if id_user in self.user_list:
            del self.user_list[id_user]
            print(f"User {id_user} deleted ")

        else: 
            print("User doesnt exist")

    def update_user(self, id_user, **kwargs):

        user = self.get_user(id_user)

        if not isinstance(id_user, int) or id_user <= 0:
            print("Error, el ID de usurio no es valido")

        # aca debo investigar como validar las values para que sea correctoss
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):

                    if key == "age" and (not isinstance(value, int) or value <= 0):
                        print(f'Error, la edad {value} no es valida')
                        continue

                    elif key == "name_user" and (not isinstance(value, str)):
                        print(f"Error, el nombre {value} no es valido")
                        continue
                    
                    setattr(user, key, value)
                    print(f'El campo {key} ha sido actualizado a {value}')
                else:
                    print(f"El campo {key} no existe en el usuario")

        else:
            print("el usuario no se encuentra")

    def read_data(self, file):
        try:
            if not os.path.exists(file):
                print("El documento no existe...")
                
            with open(file,'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                self.user_list = saved_data
                print("Datos cargados...")

        except json.JSONDecodeError:
            print("Error al leer el archivo")
        except Exception as ex:
            print(f'Ha ocurrido un error {ex}')

def export_data(self, file):
    try:
        with open(file, 'w', encoding='utf-8') as f:
            json.dumps(self.user_list, f, indent=4 )
            print("Informacion guardada")
    except Exception as ex:
        print(f"Ha ocurrido un error {ex}")

