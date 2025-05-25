
from db_setup import DatabaseRepo
from tables import car_table

class CarRepository:
    def __init__(self):
        self.db = DatabaseRepo()
        self.car_table = car_table

    def _format_car(self, car_record):
        return {
            "car ID": car_record[0],
            "brand": car_record[1],
            "model": car_record[2],
            "year": car_record[3],
            "associate user": car_record[4]
        }

    def create_new_car(self, brand, model, year, user_id=None):
        try:
            stmt = self.car_table.insert().returning(self.car_table.c.id).values(brand=brand, model=model, year=year, user_id=user_id)
            result = self.db.execute(stmt, True)
            # return result
            car_id = result.scalar()
            print(f"Auto creado con ID...{car_id}")
            return car_id
        except Exception as e:
            print(f"Error...{e}")

    def modify_car(self, id_to_modify, brand, model, year, user_id=None):
        try:
            stmt = self.car_table.update().where(self.car_table.c.id == id_to_modify).values(brand=brand, model=model, year=year, user_id=user_id)
            execute_stmt = self.db.execute(stmt, True)
            #return execute_stmt
            if execute_stmt.rowcount > 0:
                return("Auto modificado")
            else:
                return("Auto no encontrado para modificar")
        except Exception as e:
            print(f"Error  {e}")

    def delete_car(self, car_id):
        try:
            stmt = self.car_table.delete().where(self.car_table.c.id == car_id)
            execute_stmt = self.db.execute(stmt, True)

            if execute_stmt.rowcount > 0:
                print("Car delete  ")
            else:
                print("Car not found")
        except Exception as e:
            print(f"Error  {e}")

    def get_all_cars(self):
        try:
            stmt = self.car_table.select()
            execute_stmt = self.db.execute(stmt, True)
            cars = execute_stmt.fetchall()
            formatted_cars = [self._format_car(car) for car in cars]
            print(formatted_cars)

        except Exception as e:
            print(f"Error {e}")

    def associate_car_to_user(self, car_id, user_id):
        try:
            stmt = self.car_table.update().where(self.car_table.c.id == car_id).values(user_id=user_id)
            execute_stmt = self.db.execute(stmt, True)

            if execute_stmt.rowcount > 0:
                print("Usuario asociado")
            else:
                print("Operacion no realizada...")
        except Exception as e:
            print(f"Error {e}")

def request_car_data():
    brand = input("Ingrese la marca del auto...")
    model = input("Ingrese el modelo...")
    year = input("Ingrese el year del auto...")
    if not year.isdigit():
        print("Error, year must be a number")
        return None
    return brand, model, year

def request_user_id():
    ask = input("Ingresa 'Yes' si desea asociar el auto a un usuario...")
    if ask.upper() == 'YES':
        user_id = input("Ingresa el ID del usuario...")
        if not user_id.isdigit():
            print("Error, id debe ser digito valido")
            return None
        return user_id

def car_main():
    car = CarRepository()
    try:
        while True:
            print("""Modulo de Automoviles
                  1.Agregar un nuevo auto
                  2.Modificar auto
                  3.Eliminar auto
                  4.Ver todos los autos
                  5.Asociar automovil a usuario 
                  6.Menu Principal""")
    
            option = input("Ingrese la opcion necesaria.... ")
            if not option.isdigit():
                print("Error, ingresa un valor valido...")
                continue

            option = int(option)
            if option == 1:
                data = request_car_data()
                if not data:
                    print("no data")
                    continue
                brand, model, year = data

                user_id = request_user_id()
                result = car.create_new_car(brand, model, year, user_id)

                if not result:
                    print("Error al crear auto..")

            
            elif option == 2:
                car_id = input("Ingrese el id del auto a modificar...")
                if not car_id.isdigit():
                    print("Error, id invalido")
                    continue
                car_id = int(car_id)
                new_brand, new_model, new_year= request_car_data()
                new_user = request_user_id()
                result = car.modify_car(car_id, new_brand, new_model, new_year, new_user)

                print(result)

            elif option == 3:
                car_id = input("Ingrese el id del auto a eliminar...")
                if not car_id.isdigit():
                    print("Error, id invalido")
                    continue
                car_id = int(car_id)
                car.delete_car(car_id)
            
            elif option == 4:
                get_all_cars = car.get_all_cars()
            
            elif option == 5:
                car_id = input("Ingrese el id del auto a asociar...")
                if not car_id.isdigit():
                    print("Error, id invalido")
                    continue
                car_id = int(car_id)

                user_id = input("Ingrese el id del usuario a modificar...")
                if not user_id.isdigit():
                    print("Error, id invalido")
                    continue
                user_id = int(user_id)

                associate_car_to_user = car.associate_car_to_user(car_id, user_id)
            elif option == 6:
                break

    except Exception as e:
        return f"Error {e}"
    

                