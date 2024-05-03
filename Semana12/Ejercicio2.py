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
    
circle = Circle(10)
calculate_circle_area = circle.calculate_area()
calculate_circle_perimeter = circle.calculate_perimeter()
print(f'el area es de...{calculate_circle_area}')
print(f'el perimetro es de...{calculate_circle_perimeter}')
