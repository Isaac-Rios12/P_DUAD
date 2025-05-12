from flask import Flask, request, Response, jsonify, Blueprint
from db import DB_Manager
from auth.jwt_instance import jwt_manager
from auth.decorators import token_required_admin

from functools import wraps

user_routes = Blueprint('user_routes', __name__)


db_manager = DB_Manager()
          

@user_routes.route('/register', methods=['POST'])
@token_required_admin
def register():
    try:
        data = request.get_json()
        if data.get('role') not in ['admin', 'user']:
            return Response('Role is missing',status=400)
            
        if(data.get('username') == None or data.get('password') == None):
            return  Response(status=400)
        else:
            result = db_manager.insert_user(data.get('username'), data.get('password'), role= data.get('role'))
            user_id = result[0]

            print(result)

            token = jwt_manager.encode({'id':user_id})
            return jsonify(token=token)
    except Exception as e:
        return jsonify(error=str(e)), 500
    
@user_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if(data.get('username') == None or data.get('password')== None):
        return Response(status=400)
    else:
        result = db_manager.get_user(data.get('username'), data.get('password'))

        if result == None:
            return Response('User not registered', status=403)
        else:
            user_id = result[0]
            role = result[3]
            token = jwt_manager.encode({'id': user_id, 'role': role})

            return jsonify(token=token)
        
@user_routes.route('/me')
def me():
    try:
        token = request.headers.get('Authorization')
        if (token is not None):
            token = token.replace("Bearer ","")
            decoded = jwt_manager.decode(token)
            user_id = decoded['id']
            user = db_manager.get_user_by_id(user_id)
            return jsonify(id=user_id, username=user[1])
        else:
            return Response(status=403)
    except Exception as e:
        return Response(status=500)


# app.run(host="localhost",port=5000, debug=True)