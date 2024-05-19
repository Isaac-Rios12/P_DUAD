class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f'{self.name} está comiendo')

    def sleep(self):
        print(f'{self.name} está durmiendo')

class Mascot:
    def __init__(self, name):
        self.name = name

    def play(self):
        print(f'{self.name} está jugando')

class Dog(Animal, Mascot):
    def __init__(self, name):
        Animal.__init__(self, name)
        Mascot.__init__(self, name)

    def bark(self):
        print(f'{self.name} está ladrando')

my_dog = Dog("Kila")

my_dog.bark()
my_dog.eat()
my_dog.play()