from auth.jwt_manager import JWT_Manager


with open("auth/keys/private.pem", "rb") as f:
    private_key = f.read()

with open("auth/keys/public.pem", "rb") as f:
    public_key = f.read()

jwt_manager = JWT_Manager(private_key, public_key, 'RS256')