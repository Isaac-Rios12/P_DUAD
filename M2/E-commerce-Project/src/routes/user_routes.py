from flask.views import MethodView
from flask import Flask, jsonify, request, Blueprint

from ..models.user import UserHandler


#from models.user import UserHandler


user_bp = Blueprint('user_bp', __name__)

class UserAPI(MethodView):

    def __init__(self):
        
        self.user_instance = UserHandler()
        #self.user_instance.read_data('users.json')
        
    def get(self, user_id=None):

        try:

            file_path = r"C:\Users\Admin\Desktop\DUAD\P_DUAD\M2\E-commerce-Project\data\users.json"

            self.user_instance.read_data(file_path)

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
            if "id" not in request.json:
                raise ValueError("Debes ingresar el ID")
            if "name_user" not in request.json:
                raise ValueError("Debes ingresar el nombre")
            if "email" not in request.json:
                raise ValueError("Debes ingresar el email")
            if "age" not in request.json:
                raise ValueError("Debes ingresar la edad")
            

            id = request.json['id']
            exist_user = self.user_instance.get_user(id)

            if exist_user:
                raise ValueError("El usuario con este ID ya existe")
            
            response = self.user_instance.add_new_user()
            

            
            
            
        except ValueError as ex:
            return jsonify(message=str(ex)), 400
        except Exception as ex:
            return jsonify(message="Error interno del servidor", details=str(ex)), 500
        

user_view = UserAPI.as_view('user_api')
user_bp.add_url_rule('/users', defaults={'user_id': None}, view_func=user_view, methods=['GET'])
user_bp.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET'])
user_bp.add_url_rule('/users', view_func=user_view, methods=['POST'])
         
                


            




