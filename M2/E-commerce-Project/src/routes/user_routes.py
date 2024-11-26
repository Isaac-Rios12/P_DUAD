from flask.views import MethodView
from flask import Flask, jsonify, request, Blueprint

from ..models.user import UserHandler



class UserAPI(MethodView):

    def __init__(self):
        
        self.user_instance = UserHandler()
        self.file_path = './data/users.json'
        
    def get(self, user_id=None):

        try:

            #estoy aca debo revisar por que no me sirve el buscar solo 1
            

            self.user_instance.read_data(self.file_path)

            if user_id is None:
                all_users = self.user_instance.get_all_users()
                return jsonify(all_users)
            
            else:
                user = self.user_instance.get_user(user_id)

                if user:
                    return jsonify(user)
                else:
                    return jsonify({"message": "Usaurio no encontrado"}), 404
                
        except FileNotFoundError as e:
            return jsonify({"error": str(e)}), 404
        
        except FileNotFoundError as e:
            return jsonify({"error": f"Error inesperado: {str(e)}"}), 500
        
    def post(self):
        try:

            data = request.get_json()

            if not data:
                return jsonify({"message": "El cuerpo de la solicitud está vacío o es inválido"}), 400

            self.user_instance.read_data(self.file_path)

            required_fields =  ["id_user", "name_user", "email", "age" ]

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                raise ValueError(f"Faltan los siguientes campos: {', '.join(missing_fields)}")            

            id_user = request.json["id_user"]
            name_user = request.json["name_user"]
            email = request.json["email"]
            age = request.json["age"]

            exist_user = self.user_instance.get_user(id_user)

            if exist_user:
                raise ValueError("El usuario con este ID ya existe")
            
            response = self.user_instance.add_new_user(self.file_path, id_user, name_user, email, age)

            if response[1] == 201:
                return jsonify(response[0]), 201
            else:
                return jsonify(response[0]), response[1]
                 
        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except Exception as ex:
            return jsonify(message="Error interno del servidor", details=str(ex)), 500
        

    def delete(self, user_id):
        try:
            self.user_instance.read_data(self.file_path)
            if not user_id:
                raise ValueError("Id del usuario es requerido")

            
            exist_user = self.user_instance.get_user(user_id)

            if not exist_user:
                raise ValueError(f"No se encontró un usuario con el ID: {user_id}")

            
            response = self.user_instance.delete_user(self.file_path, user_id)

            
            if response[1] == 200:
                return jsonify({"message": "Usuario eliminado correctamente"}), 200
            else:
                return jsonify(response[0]), response[1]

        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except Exception as ex:
            return jsonify(message="Error interno del servidor", details=str(ex)), 500
        
    def put(self, user_id):
        try:

            if not user_id:
                raise ValueError("ID del usuario es requerido")
            
            data = request.get_json()

            if not data:
                return jsonify({"Error":" Los datos no han sido recibidos"}),404
            
            self.user_instance.read_data(self.file_path)

            exist_user = self.user_instance.get_user(user_id)

            if not exist_user:
                raise ValueError("El usuario no existe")

            name_user = request.json["name_user"]
            email = request.json["email"]
            age = request.json["age"]

            if not(name_user and email and age):
                return jsonify({"error": "Datos necesarios faltamtes..."}), 400
            
            response, status = self.user_instance.update_user(self.file_path, user_id, name_user, email, age)

            if status == 200:
                return jsonify({"message": f"Usuario {user_id} actualizado correctamente...", "user": response})
            else:
                return jsonify(response), status

        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except Exception as ex:
            return jsonify(message="Error interno del servidor", details=str(ex)), 500
        




user_bp = Blueprint('user_bp', __name__)

user_view = UserAPI.as_view('user_api')
user_bp.add_url_rule('/users', defaults={'user_id': None}, view_func=user_view, methods=['GET'])
user_bp.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET'])
user_bp.add_url_rule('/users', view_func=user_view, methods=['POST'])
user_bp.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['DELETE'])
user_bp.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['PUT'])
         


#esta listo aca, creo que puedo seguir con la otra entidad
                


            




