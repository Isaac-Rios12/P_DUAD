class Person:
    def __init__(self, name):
        self.name = name 


class Bus:
    def __init__(self):
        self.max_passengers = 30
        self.passengers = []
        
    

    def add_passenger(self, person):
        if len(self.passengers) < self.max_passengers:
            self.passengers.append(person)
            print(f"{person.name} ha subido al bus...")
        else:
            print("Bus lleno...")

    def remove_passenger(self):
        if self.passengers:
            remove_passenger = self.passengers.pop()
            print(f'{remove_passenger} ha bajado del bus')
        else:
            print("El pasajero no ha bajado...")


my_bus = Bus()

while True:

    print("1. Subir pasajero")
    print("2. Bajar pasajero")
    print("3. Salir")
    option = int(input("Ingrese la opcion necesaria..."))

    if option == 1:
        passenger_name = input("Ingrese el nombre del pasajero...")
        person = Person(passenger_name)
        my_bus.add_passenger(person)
    
    elif option == 2:
        my_bus.remove_passenger()
    
    else:
        print("has salido...")
        break
