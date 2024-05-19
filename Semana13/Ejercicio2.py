
def numbers_only(func):
    def wrapper(*args):
        try:
            for valor in args:
                if not isinstance(valor, (int, float)):
                    raise ValueError(f"{valor} No es un numero")
            func(*args)
        except ValueError as e:
            print(e)
    return wrapper

        

@numbers_only
def my_parameters(*args):
    print(*args)

my_parameters(2.5, 1, 2, 3, 4, 5, "a")