#from db.manager import DatabaseManager
from db.models.role import Role
from db.manager import db
from sqlalchemy.exc import IntegrityError

from sqlalchemy import select

class RoleRepositoryError(Exception):
    pass
class RoleNotFoundError(RoleRepositoryError):
    pass
class RoleCreationError(RoleRepositoryError):
    pass


class RoleRepository:
    def __init__(self):
        self.role_table = Role

    def _format_role(self, role):
        if not role:
            return None
        return {
            "id": int(role.id),
            "name": str(role.name)
        }
    
    def get_role_by_name(self, name):
        try:
            with db.get_session() as session:
                role = session.query(Role).filter_by(name=name).first()
                if not role:
                    raise RoleNotFoundError(f"Role '{name}' not found")
                return self._format_role(role)
        except RoleNotFoundError:
            raise
        except Exception as e:
            raise RoleRepositoryError(f"Error retrieving role '{name}': {e}")
    
    def create_role(self, name):
        try:
            with db.get_session() as session:
                with session.begin():
                    new_role = Role(name=name)
                    session.add(new_role)
                    session.flush()
                    return self._format_role(new_role)
        except IntegrityError:
            raise RoleCreationError(f"Role '{name}' already exists")
        except Exception as e:
            raise RoleCreationError(f"Failed to create the role: {e}")
            
    def get_role_by_id(self, role_id):
        try:
            with db.get_session() as session:
                with session.begin():
                    role = session.get(Role, role_id)
                    if not role:
                        raise RoleNotFoundError(f"Role with ID...{role_id} not found")
                    return self._format_role(role)
        except RoleNotFoundError:
            raise
        except Exception as e:
            raise RoleRepositoryError("Error retrieving the role")
        
    def get_all_roles(self):
        try:
            with db.get_session() as session:
                with session.begin():
                    stmt = select(Role)
                    result = session.execute(stmt)
                    roles = result.scalars().all()

                    if not roles:
                        raise RoleNotFoundError("No roles were found")
                    return [self._format_role(role) for role in roles]
        except RoleNotFoundError:
            raise
        except Exception as e:
            raise RoleRepositoryError("Error retrieving all roles")
    
    def update_role(self, role_id, new_name):
        try:
            with db.get_session() as session:
                with session.begin():
                    role = session.get(Role, role_id)
                    if not role:
                        raise RoleNotFoundError(f"Role with ID...{role_id} not found")
                    
                    role.name = new_name
                    session.flush()
                    return self._format_role(role)
        except RoleNotFoundError:
            raise
        except Exception as e:
            raise RoleRepositoryError(f"Error updating role: {e}")
    
    def delete_role(self, role_id):
        try:
            with db.get_session() as session:
                with session.begin():
                    role = session.get(Role, role_id)
                    if not role:
                        raise RoleNotFoundError(f"Role with ID...{role_id} not found")
                    session.delete(role)
        except RoleNotFoundError:
            raise
        except Exception as e:
            raise RoleRepositoryError(f"Error deleting the role {e}")
            