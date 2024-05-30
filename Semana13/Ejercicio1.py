
def my_decorator(func):
    def wrapper(*args):
        print("iniciando...")
        func(*args)
        print("terminado...")

    return wrapper

@my_decorator
def my_function(*args):
    print(*args)

my_function("a", "b", "c", "d", 1,)