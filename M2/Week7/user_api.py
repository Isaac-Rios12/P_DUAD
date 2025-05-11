from flask import Flask, request, Response, jsonify
from db import DB_Manager
from auth.jwt_manager import JWT_Manager
from functools import wraps

app = Flask("user-service")
db_manager = DB_Manager()

## usar llaves

with open("auth/keys/private.pem", "rb") as f:
    private_key = f.read()

with open("auth/keys/public.pem", "rb") as f:
    public_key = f.read()

jwt_manager = JWT_Manager(private_key, public_key, 'RS256')

@app.route("/liveness")
def liveness():
    return "<p>Hello, World!</p>"

def token_required_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return Response("Token is missing", status=403)
        
        try:
            decoded = jwt_manager.decode(token)
            if not decoded:
                return Response("Token is invalid",status=403)
            if decoded.get('role') != 'admin':
                return Response("You need to be a admin", status=403)
            
        except Exception as e:
            return Response("Token invalid o expired", status=403)
        
        return f(*args, **kwargs)
    return decorator
        
            

@app.route('/register', methods=['POST'])
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
    
@app.route('/login', methods=['POST'])
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
        
@app.route('/me')
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


app.run(host="localhost",port=5000, debug=True)