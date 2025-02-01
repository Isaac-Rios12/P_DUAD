from database.db import PgManager

class VehicleManager:
    def __init__(self):
        self.db_manager = PgManager(
            db_name = "postgres",
            user = "postgres",
            password = "postgre",
            host = "localhost"
        )

    def get_cars(self, vehicle_id=None):
        try:
            if vehicle_id:
                query = """
                            SELECT v.id, v.vin, v.status, m.id, m.make, m.year
                            FROM lyfter_car_rental.vehicles v
                            JOIN lyfter_car_rental.vehicle_model m ON v.model_id = m.id
                            WHERE v.id = %s
                        """
                #query = "SELECT * FROM lyfter_car_rental.vehicles WHERE id = %s"
                results = self.db_manager.execute_query(query, vehicle_id)
                self.db_manager.close_connection()

                # if not results:
                #     return f"Error: usuario no encontrado"
                return results
            
            query = """
                        SELECT v.*, m.*
                        FROM lyfter_car_rental.vehicles v
                        JOIN lyfter_car_rental.vehicle_model m ON v.model_id = m.id
                        """
            results = self.db_manager.execute_query(query)
            self.db_manager.close_connection()
            return (results)
        except Exception as e:
            return ("Error", e)
        
    def filter_vehicle(self, filters):
        try:

            filter_key, filter_value = next(iter(filters.items()))  
            query = f"SELECT * FROM lyfter_car_rental.vehicles WHERE {filter_key} = %s"  
            result = self.db_manager.execute_query(query, (filter_value))
            self.db_manager.close_connection()


            if result:
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
            results = self.db_manager.execute_query(query, vin, model_id, status)
            self.db_manager.close_connection()

            if self.db_manager.cursor.rowcount > 0:
                return f"Vehicle {vin} created"
            
            return results
        except Exception as e:
            return ("error", e)
        


        """
        quedo aca, estoy aun con los servicios y apis de vehicles.....


        """

    def modify_vehicle_status(self, vehicle_id, new_status):
        try:

            # check_status = self.verify_status(new_status)

            # if check_status:
            #     return {"error": check_status}, 400
            
            query = """
                    UPDATE lyfter_car_rental.vehicles 
                    SET status = %s
                    WHERE id = %s
                    """
            
            results = self.db_manager.execute_query(query, new_status, vehicle_id)
            print(f"Query results: {results}")

            if "rows affected" in results and int(results.split()[3]) > 0:
                return f"Vehicle {vehicle_id} status updated to {new_status}"
            else:
                return f"Vehicle {vehicle_id} not found or status unchanged."

        except Exception as e:
            print(f"Error updating vehicle status: {str(e)}")
            return f"error: {str(e)}"
        
    def verify_status(self, status):
        availables_status = ['available', 'rented', 'reserved', 'under maintance', 'damaged']

        if status.lower() not in availables_status:
            return f"{status} status not allowed... Allowed={availables_status}"



