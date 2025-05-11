import jwt

class JWT_Manager:
    def __init__(self, private, public, algorithm):
        self.private = private
        self.public = public
        self.algorithm = algorithm


    def encode(self, data):
        try:
            encoded = jwt.encode(data, self.private, algorithm=self.algorithm)
            return encoded
        except Exception as e:
            print(e)
            return None
        
    def decode(self, token):
        try:
            decoded = jwt.decode(token, self.public, algorithms=[self.algorithm])
            return decoded
        except Exception as e:
            print(e)
            return None
        

        