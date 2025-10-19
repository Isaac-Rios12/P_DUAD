#from db.manager import DatabaseManager
from db.models.user import User
from db.manager import db

from sqlalchemy import select
import bcrypt

#!reubicar
class UserRepositoryError(Exception):
    pass
class UserNotFoundError(UserRepositoryError):
    pass
class UserCreationError(UserRepositoryError):
    pass



class UserRepository:
    def __init__(self):
        self.user_table = User
    def _format_user(self, user):
        return {
            "id": user.id,
            "fullname": user.fullname,
            "nickname": user.nickname,
            "email": user.email,
            "role_id": user.role.id,
            "role_name": user.role.name,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None
        }
    @staticmethod
    def _hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')  # Lo decodificamos para guardarlo como string normal
    
    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def get_all_users(self):
        try:
            with db.get_session() as session:
                with session.begin():
                    stmt = select(User)
                    result = session.execute(stmt)
                    users = result.scalars().all()
                    if not users:
                        raise UserNotFoundError("No users found")
                    return [self._format_user(user) for user in users]

        except UserNotFoundError:
            raise 
        except Exception as e:
            raise UserRepositoryError(f"Error retrieving all users: {e}")

    def create_user(self, fullname, nickname, email, password, role_id):
        try:
            with db.get_session() as session:
                with session.begin():
                    hashed_pwd = self._hash_password(password)
                    new_user = User(fullname=fullname, nickname=nickname, email=email, password=hashed_pwd, role_id=role_id)
                    session.add(new_user)
                    session.flush() # asegura que se actualicen campos autogenerados
                    return self._format_user(new_user)
        except Exception as e:
            print(f"Error al insertar usuario...{e}")
            raise UserCreationError(f"Error creating the user")

    def get_user_for_login(self, nickname, password):
        try:
            with db.get_session() as session:
                with session.begin():

                    stmt = select(User).where(User.nickname == nickname)
                    user = session.scalars(stmt).first()
                    if not user:
                        raise UserNotFoundError("User not found")
                    
                    if not self._verify_password(password, user.password):
                        raise UserRepositoryError("Incorrect password")

                    return self._format_user(user)
        except UserNotFoundError:
            raise
        except Exception as e:
            print(e)
            raise UserRepositoryError(f"Login Error")
        

    def get_user_by_id(self, user_id):
        try:
            with db.get_session() as session:
                with session.begin():
                    user = session.get(User, user_id)
                    if not user:
                        raise UserNotFoundError(f"User with ID {user_id} not found")
                    return self._format_user(user)
        except UserNotFoundError:
            raise
        except Exception as e:
            #print(f"Error al obtener usuario... {e}")
            raise UserRepositoryError(f"Error retrieving user witd ID {user_id}")

    def update_user(self, user_id, email, password):
        try:
            with db.get_session() as session:
                with session.begin():
                    user = session.get(User, user_id)

                    if not user:
                        raise UserNotFoundError(f"User with ID {user_id} not found")
                    
                    #user.fullname = fullname
                    #user.nickname = nickname
                    user.email = email
                    user.password = self._hash_password(password)

                    session.flush()
                    return self._format_user(user)
                
        except UserNotFoundError:
            raise
        except Exception as e:
            raise UserRepositoryError(f"Error updating user with ID user {user_id}")
        
    def get_user_by_nickname(self, nickname):
        with db.get_session() as session:
            user = session.query(User).filter_by(nickname=nickname).first()
            if user:
                return self._format_user(user)  # ya devuelve dict
            return None

    def delete_user(self, user_id):
        try:
            with db.get_session() as session:
                with session.begin():
                    user = session.get(User, user_id)
                    if not user:
                        raise UserNotFoundError("User not found")
                    session.delete(user)
        except UserNotFoundError:
            raise
        except Exception as e:
            print(f"Error al eliminar usuario...{user_id}")
            raise UserRepositoryError(f"Error deleting the user..")
