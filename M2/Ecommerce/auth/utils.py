from flask import request, Response, jsonify
from functools import wraps
from auth.jwt_instance import jwt_instance
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError, InvalidSignatureError


def token_required_admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({"error": "No token provided"}), 401
        
        try:
            decoded = jwt_instance.decode(token)
            if not decoded:
                return jsonify({"error": "Token is invalid"}), 401
            if decoded.get('role') != 'Admin': 
                print(decoded.get('role'))
                return jsonify({"error": "Admins only"}), 403
            
        except ExpiredSignatureError:
            return jsonify({"error": "Token expired ⏳"}), 401
        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401
        
        return f(*args, **kwargs)
    return decorator

from repositories.user_repo import UserRepository
user_rep = UserRepository()
def get_current_user():
    token = request.headers.get("Authorization")
    
    if not token:
        raise PermissionError("No token given")

    try:
        token = token.replace("Bearer ", "")
        decoded = jwt_instance.decode(token)
        user_id = decoded['id']
        user = user_rep.get_user_by_id(user_id)
        if not user:
            raise PermissionError("User not found")
        return user
    except ExpiredSignatureError:
        raise PermissionError("Token expired ⏳")
    except (InvalidTokenError, DecodeError, InvalidSignatureError):
        raise PermissionError("Invalid Token")
    except Exception:
        raise PermissionError("Invalid Token or internal error")