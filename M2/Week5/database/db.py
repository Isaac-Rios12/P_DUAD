import psycopg2

# class PgManager:
#     def __init__(self, db_name, user, password, host, port=5432):
#         self.db_name = db_name
#         self.user = user
#         self.password = password
#         self.host = host
#         self.port = port

#         self.connection = self.create_connection()
#         if self.connection:
#             self.cursor = self.connection.cursor()
#             print("Connection created succesfully....")
#         else:
#             print("Failed to establish connection.")

    
#     def create_connection(self):
#         try:
#             connection = psycopg2.connect(
#                 dbname = self.db_name,
#                 user = self.user,
#                 password = self.password,
#                 host = self.host,
#                 port = self.port
#             )
#             return connection
        
#         except Exception as error:
#             print("Error", error)
#             return None
        
#     def close_connection(self):
#         if self.cursor:
#             self.cursor.close()
#         if self.connection:
#             self.connection.close()
#             print("Connection closed")


#     def execute_query(self, query, *args):
#         try:
#             if not self.cursor or self.cursor.closed:
#                 self.cursor = self.connection.cursor()
                
#             self.cursor.execute(query, args)
#             self.connection.commit()

#             if self.cursor.description:
#                 results = self.cursor.fetchall()
#                 return results
#             #return self.cursor.rowcount
        
#         except Exception as e:
#             return f"database error: {str(e)}"
        
class PgManager:
    def __init__(self, db_name, user, password, host, port=5432):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None
        self.create_connection()

    def create_connection(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connection created successfully....")
        except Exception as error:
            print("Error creating connection:", error)
            self.connection = None

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def execute_query(self, query, *args):
        try:

            if not self.connection or self.connection.closed:
                self.create_connection()

            
            if not self.cursor or self.cursor.closed:
                self.cursor = self.connection.cursor()

            self.cursor.execute(query, args)
            self.connection.commit()

            if self.cursor.description:
                results = self.cursor.fetchall()
                return results
            else:
                return f"Query executed successfully: {self.cursor.rowcount} rows affected."

        except Exception as e:
            return f"database error: {str(e)}"

    def __del__(self):
        self.close_connection()


        

