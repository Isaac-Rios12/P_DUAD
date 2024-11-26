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
        user =  self.user_list.get(id_user)
        return user.to_dict() if user else None
    
    def validate_user(self, id_user, name_user, age):

        if not isinstance(id_user, int) or id_user <= 0:
            raise ValueError("El ID de usuario debe ser un número entero positivo")

        if not isinstance(name_user, str) or not name_user.strip():
            raise ValueError("El nombre de usuario no es válido")

        if not isinstance(age, int) or not (0 < age < 100):
            raise ValueError("La edad debe ser un número entre 1 y 99 años")

        return None

    def add_new_user(self, file_path, id_user, name_user, email, age):

        try:
            #validation = self.validate_user(id_user, name_user, age)
            self.validate_user(id_user, name_user, age)
            #if validation:
                

            if id_user in self.user_list:
                return {"message": "El usuario se encuentra registrado"}, 400

            
            user = User(id_user, name_user, email, age)
            self.user_list[id_user] = user

            self.export_data(file_path)

            return {"message": "Usuario registrado correctamente", "user": vars(user)}, 201

        except ValueError as ve:
            return {"error": f"Error de validación: {str(ve)}"}, 400

        except Exception as e:
            return {"error": f"Error inesperado: {str(e)}"}, 500

    def delete_user(self, file_path,  id_user):

        if not isinstance(id_user, int) or id_user <= 0:
            return {"message": "Error, el ID de usuario debe ser un número entero positivo"}, 400

        if id_user in self.user_list:
            del self.user_list[id_user]
            self.export_data(file_path)
            return {"message": f"El Usuario {id_user} ha sido eliminado"}, 200

        else: 
            return {"message": f"El Usuario {id_user} no existe en el registro"}, 404
        

    def update_user(self, file_path, id_user, new_name, new_email, new_age):

        validation = self.validate_user(id_user, new_name, new_age)

        if validation:
            return validation

        user = self.get_user(id_user)

        if not user:
            return {"message": "Error, usuario no encontrado"}, 404
            
        user["name_user"] = new_name
        user["email"] = new_email
        user["age"] = new_age

        self.export_data(file_path)

        return user, 200

    def read_data(self, file):
        try:

            if not os.path.exists(file):
                raise FileNotFoundError(f"Archivo no encontrado: {file}")

            with open(file, 'r', encoding='utf-8') as f:
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




