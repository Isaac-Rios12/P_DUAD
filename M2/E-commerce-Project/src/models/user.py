import os
import json

class User:
    def __init__(self, id_user=None, name_user=None, email=None, age=None):
        self.id_user = id_user
        self.name_user = name_user
        self.email = email
        self.age = age

    def to_dict(self):
        return{
            "id_user": self.id_user,
            "name_user": self.name_user,
            "email": self.email,
            "age": self.age
        }

   
class UserHandler:
    def __init__(self):
        self.user_list = {}
 
    def get_all_users(self):
        
        return [user.to_dict() for user in self.user_list.values()]

    def get_user(self, id_user):
        return self.user_list.get(id_user)
    
    def validate_user(self, id_user, name_user, email, age):

        if not isinstance(id_user, int) or id_user <= 0:
            return {"message": "Error, el ID de usuario debe ser un número entero positivo"}, 400
         
        if not isinstance(name_user, str) or not name_user.strip():
            return {"message": "Error, el nombre de usuario no es válido"}, 400

        if not isinstance(age, int) or not (0 < age < 100):
            return {"message": "Error, la edad debe ser un número entre 1 y 99 años"}, 400

        return None

    def add_new_user(self, id_user, name_user, email, age):

        validation = self.validate_user(id_user, name_user, age)

        if validation:
            return validation
        
        if id_user in self.user_list:
            return {"message": "El usuario se encuentra registrado"}, 400
        
        user = User(id_user, name_user, email, age)
        self.user_list[id_user] = user
        self.export_data("users.json")
        return {"message": "Usuario registrado correctamente", "user": vars(user)}, 201
    

    def delete_user(self, id_user):

        if not isinstance(id_user, int) or id_user <= 0:
            return {"message": "Error, el ID de usuario debe ser un número entero positivo"}, 400

        if id_user in self.user_list:
            del self.user_list[id_user]
            self.export_data("users.json")
            return {"message": f"El Usuario {id_user} ha sido eliminado"}, 200

        else: 
            return {"message": f"El Usuario {id_user} no existe en el registro"}, 404
        

    def update_user(self, id_user, new_name, new_email, new_age):

        validation = self.validate_user(id_user, new_name, new_age)
        if validation:
            return validation

        user = self.get_user(id_user)

        if not user:
            return {"message": "Error, usuario no encontrado"}, 404
            
        user.name_user = new_name
        user.email = new_email
        user.age = new_age

        self.export_data("users.json")

        return {"message": f"Usuario {id_user} actualizado correctamente", "user": vars(user)}, 200

    def read_data(self, file):
        try:

            current_dir = os.path.dirname(__file__)  # Directorio actual de user.py
            parent_dir = os.path.dirname(current_dir)  # Subir un nivel para salir de 'models'
            data_dir = os.path.join(parent_dir, 'data')  # Acceder a 'data' en el nivel superior
            file_path = os.path.join(data_dir, file)

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Archivo no encontrado: {file}")

            with open(file_path, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                self.user_list = {user_data['id_user']: User(**user_data) for user_data in saved_data}

        except FileNotFoundError as fnf_error:
            raise fnf_error  

        except json.JSONDecodeError:
            raise ValueError("El archivo contiene datos inválidos o está corrupto.")

        except Exception as ex:
            raise Exception(f"Ha ocurrido un error inesperado: {ex}")

    def export_data(self, file):
        try:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump([user.to_dict() for user in self.user_list.values()], f, indent=4 )
                print("Informacion guardada")
        except Exception as ex:
            print(f"Ha ocurrido un error {ex}")



# estaba aca implemetnado el read, ya lee los datos, ahora esta la duda con la rutaaa
