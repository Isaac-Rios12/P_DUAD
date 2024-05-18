
def numbers_only(func):
    def try_print_numbers(*args):
        try:
            for valor in args:
                if not isinstance(valor, int):
                    raise print("No es un numero")
            func(*args)
        except Exception:
            print("Este parametro no es un numero")
    return try_print_numbers

        

@numbers_only
def my_parameters(*args):
    print(*args)

my_parameters(1, 2, 3, 4, 5, "a")