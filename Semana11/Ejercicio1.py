class Circle:
    def __init__(self, radio = 0):
        self.radio = radio

    def get_area(self):
        area= 3.14159 * self.radio**2
        return area

radio = float(input("Ingrese el radio..."))
my_circle = Circle(radio)

area_circulo = my_circle.get_area()
print(f'El area del circulo es....{area_circulo}')
