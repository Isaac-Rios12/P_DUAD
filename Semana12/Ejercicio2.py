from abc import ABC, abstractmethod

class Shape(ABC):
    
    @abstractmethod
    def calculate_perimeter(self):
        pass

    @abstractmethod
    def calculate_area(self):
        pass

class Circle(Shape):
    
    def __init__(self, r):
        self.radio = r

    def calculate_perimeter(self):
        return 2 * self.radio * 3.141509

    def calculate_area(self):
        return 3.141509 * self.radio
    
class Square(Shape):
    def __init__(self, side_length):
        self.side_length = side_length

    def calculate_area(self):
        return self.side_length ** 2
    
    def calculate_perimeter(self):
        return 4 * self.side_length


class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width =  width

    def calculate_perimeter(self):
        return 2 * (self.length + self.width)
    
    def calculate_area(self):
        return self.length * self.width
    
radio = float(input("Ingresa el radio del círculo: "))
circle = Circle(radio)
calculate_circle_area = circle.calculate_area()
calculate_circle_perimeter = circle.calculate_perimeter()
print(f'El área del círculo es: {calculate_circle_area}')
print(f'El perímetro del círculo es: {calculate_circle_perimeter}')


side_length = float(input("Ingresa el lado del cuadrado: "))
square = Square(side_length)
calculate_square_area = square.calculate_area()
calculate_square_perimeter = square.calculate_perimeter()
print(f'El área del cuadrado es: {calculate_square_area}')
print(f'El perímetro del cuadrado es: {calculate_square_perimeter}')

length = float(input("Ingresa la longitud del rectángulo: "))
width = float(input("Ingresa el ancho del rectángulo: "))
rectangle = Rectangle(length, width)
calculate_rectangle_area = rectangle.calculate_area()
calculate_rectangle_perimeter = rectangle.calculate_perimeter()
print(f'El área del rectángulo es: {calculate_rectangle_area}')
print(f'El perímetro del rectángulo es: {calculate_rectangle_perimeter}')