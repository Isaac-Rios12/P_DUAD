
def my_decorator(func):
    def return_function(*args):
        print("iniciando...")
        func(*args)
        print("terminado...")

    return return_function

@my_decorator
def my_function(*args):
    print(*args)

my_function("a", "b", "c", "d", 1)