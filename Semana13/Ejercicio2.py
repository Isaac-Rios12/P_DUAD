
def numbers_only(func):
    def wrapper(*args):
            for valor in args:
                if not isinstance(valor, (int, float)):
                    raise ValueError(f"{valor} no es un número")
            return func(*args)
    return wrapper

        

@numbers_only
def my_parameters(*args):
    print(*args)

def main():
    try:
        my_parameters(2.5, 1, 2, 3, 4, 5, "a")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()