from flask import request

from db.db import User_Manager
from .jwt_instance import jwt_manager

db_manager = User_Manager()

def get_current_user():
    token = request.headers.get("Authorization")
    if token is None:
        raise PermissionError("Token no proporcionado")
    
    try:
        token = token.replace("Bearer ", "")
        decoded = jwt_manager.decode(token)
        user_id = decoded['id']
        user = db_manager.get_user_by_id(user_id)
        return user
    except Exception as e:
        raise PermissionError({"Token Invalido o error interno": str(e)})