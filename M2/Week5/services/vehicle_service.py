from database.db import PgManager

class VehicleManager:
    def __init__(self):
        self.db_manager = PgManager(
            db_name = "postgres",
            user = "postgres",
            password = "postgre",
            host = "localhost"
        )

    def get_all_vehicles(self):
        try:
            query = """
                        SELECT v.*, m.*
                        FROM lyfter_car_rental.vehicles v
                        JOIN lyfter_car_rental.vehicle_model m ON v.model_id = m.id
                        """
            results = self.db_manager.execute_query(query)
            if results:
                return results
            return None
        except Exception as e:
            return {"Error": str(e)}

    def get_car_by_id(self, vehicle_id):
        try:
            if vehicle_id:
                query = """
                            SELECT v.id, v.vin, v.status, m.id, m.make, m.year
                            FROM lyfter_car_rental.vehicles v
                            JOIN lyfter_car_rental.vehicle_model m ON v.model_id = m.id
                            WHERE v.id = %s
                        """
                results = self.db_manager.execute_query(query, vehicle_id)
                if results:
                    return results
                return None
        except Exception as e:
            return ("Error", e)
        
    def filter_vehicle(self, filters):
        try:

            filter_key, filter_value = next(iter(filters.items()))  
            query = f"SELECT * FROM lyfter_car_rental.vehicles WHERE {filter_key} = %s"  
            result = self.db_manager.execute_query(query, (filter_value))
            self.db_manager.close_connection()

            if not "error" in result:
                return result
            return None
            
        
        except Exception as e:
            return ("error", e)


    def create_vehicle(self, vin, model_id, status):
        try:
            query = """
                    INSERT INTO lyfter_car_rental.vehicles (vin, model_id, status)
                    VALUES (%s, %s, %s) 

                    """
            results = self.db_manager.execute_query(query, vin, model_id, status.lower())
            self.db_manager.close_connection()

            if self.db_manager.cursor.rowcount > 0:
                return f"Vehicle {vin} created"
            
            return results
        except Exception as e:
            return ("error", e)
        



    def modify_vehicle_status(self, vehicle_id, new_status):
        try:

            
            query = """
                    UPDATE lyfter_car_rental.vehicles 
                    SET status = %s
                    WHERE id = %s
                    """
            
            results = self.db_manager.execute_query(query, new_status.lower(), vehicle_id)
            print(f"Query results: {results}")

            if self.db_manager.cursor.rowcount > 0:
                return f"Modified vehicle"

        except Exception as e:
            print(f"Error updating vehicle status: {str(e)}")
            return f"error: {str(e)}"
        
    def verify_status(self, status):
        availables_status = ['available', 'rented', 'reserved', 'maintenance', 'damaged']

        if status.lower() not in availables_status:
            return f"{status} status not allowed... Allowed={availables_status}"



