class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print("esta comiendo...")

    def sleep(sleep):
        print("esta durmiendo...")

class Mascot:
    def __init__(self, name):
        self.name = name

    def play(self):
        print("esta jugando...")

class Dog(Animal, Mascot):
    def __init__(self, name, raza):
        Animal.__init__(self, name)
        Mascot.__init__(self, name)
        self.raza = raza

    def bark(self):
        print("esta ladrando...")

my_dog = Dog("Kila", "Amstaff")

my_dog.bark()