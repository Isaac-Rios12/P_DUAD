from database.db import PgManager

class VehicleRental:
    def __init__(self):
        self.db_manager = PgManager(
            db_name = 'postgres',
            user = 'postgres',
            password = 'postgre',
            host = 'localhost'

        )

    def get_rentals(self, rental_id=None):
        try:
            if rental_id:
                query = "SELECT * FROM lyfter_car_rental.rentals WHERE id = %s"
                results = self.db_manager.execute_query(query, rental_id)
                if results:
                    return results
                return None
            
            query = "SELECT * FROM lyfter_car_rental.rentals"
            results = self.db_manager.execute_query(query)
            if results:
                return results
        except Exception as e:
            return {"Error": str(e)}
        
    def filter_rental(self, filters):
        try:
            filter_key, filter_value = next(iter(filters.items()))
            query = f"SELECT * FROM lyfter_car_rental.rentals WHERE {filter_key} = %s"
            result = self.db_manager.execute_query(query, filter_value.capitalize)
            if not "error" in result:
                return result
            return None
        except Exception as e:
            return {"Error": str(e)}
        
    def create_rental(self, status, vehicle_id, user_id, return_date):
        try:
            query = """
                    INSERT INTO lyfter_car_rental.rentals (status, vehicle_id, user_id, return_date)
                    VALUES (%s, %s, %s, %s)
                    """
            results = self.db_manager.execute_query(query, status, vehicle_id, user_id, return_date)

            if self.db_manager.cursor.rowcount > 0:
                return f"Rental created succesfully for user {user_id} with vehicle {vehicle_id}"
            return results
        
        except Exception as e:
            return {"Error": str(e)}
        
    def modify_rental_status(self, rental_id, new_status):
        try:
            query = """
                    UPDATE lyfter_car_rental.rentals
                    SET status = %s
                    WHERE id = %s
                    """
            results = self.db_manager.execute_query(query, new_status, rental_id)

            if self.db_manager.cursor.rowcount > 0:
                return f"Status modify in rental = {rental_id}"
            return f"Error {results}"
        
        except Exception as e:
            return {"Error": str(e)}


    def verify_status(self, status):
        allowed_status = ['Reserved', 'In progress', 'Completed', 'Canceled', 'Overdue']
        if status.capitalize() not in allowed_status:
            return f"{status} not allowed...     Allowed: {allowed_status}"        

        
