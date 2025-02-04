from database.db import PgManager
#from ..database.db import PgManager



class UserManager:
    def __init__(self):
        self.db_manager = PgManager(
            db_name="postgres",
            user="postgres",
            password="postgre",
            host="localhost"
        )

    def get_users(self, user_id=None):
        try:
            if user_id:
                query = "SELECT * FROM lyfter_car_rental.users WHERE id = %s"
                results = self.db_manager.execute_query(query, user_id)
                if results:
                    return results[0]
                return None
              
            results = self.db_manager.execute_query("SELECT * FROM lyfter_car_rental.users;")
            self.db_manager.close_connection()
            return (results)
        except Exception as e:
            return ("Error", e)
        
    def filter_user(self, filters):
        #acepta filtrar por cualquier columa, pero no acepta varios parametros...........
        try:
            filter_key, filter_value = next(iter(filters.items()))
            query = f"SELECT * FROM lyfter_car_rental.users WHERE {filter_key} = %s"
            result = self.db_manager.execute_query(query, (filter_value))
            self.db_manager.close_connection()

            if not "error" in result:
                return result
            return None
        
        except ValueError as e:
            raise e
        
        
    def create_user(self, name, email, username, password, birth_date, account_status):
        try:
            query = """
                    INSERT INTO lyfter_car_rental.users (name, email, username, password, birth_date, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
            results = self.db_manager.execute_query(query, name, email, username, password, birth_date, account_status.capitalize()) 
            self.db_manager.close_connection()

            if self.db_manager.cursor.rowcount > 0:
                return f"User {name} created"
            return results
        except Exception as e:
            return f"Error: {str(e)}"
        
    def modify_user_status(self, user_id, new_status):
        try:

            query = """
                    UPDATE lyfter_car_rental.users
                    SET status = %s
                    WHERE id = %s
                """
            results = self.db_manager.execute_query(query, new_status, user_id)

            if self.db_manager.cursor.rowcount > 0:
                return f"User {user_id} status uptaded to {new_status}"
            return f"user {user_id} not found or not status unchaged.."

        except Exception as e:
            return f"error: {str(e)}"
        
    def verify_status(self, status):
        allowed_status = ['Active', 'Blacklisted', 'Debtor']

        if status.capitalize() not in allowed_status:
            return f"{status} not allowed....      Allowed {allowed_status}"
        

        
        

