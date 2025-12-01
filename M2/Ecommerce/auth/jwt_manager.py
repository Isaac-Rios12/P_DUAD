import jwt
import datetime

class JWT_Manager:
    def __init__(self, private, public, algorithm):
        self.private = private
        self.public = public
        self.algorithm = algorithm

    def encode(self, data, expire_minutes=100):
        try:
            payload = data.copy()
            payload['iat'] = datetime.datetime.utcnow()
            payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes= expire_minutes)
            encoded = jwt.encode(payload, self.private, algorithm=self.algorithm)
            return encoded
        except Exception as e:
            print(e)
            return None
        
    def decode(self, token):
        try:
            decoded = jwt.decode(token, self.public, algorithms=[self.algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            print("El token ha expirado ⏳")
            return None
        except Exception as e:
            print(e)
            return None
        