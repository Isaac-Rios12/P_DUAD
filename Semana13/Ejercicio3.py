from datetime import date

class User:
    date_of_birth = date

    def __init__(self, date_of_birth):
        self.date_of_birth = date_of_birth

    @property
    def age(self):
        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )
    
def adult_only(func):
    def wrapper(*args, **kwargs):
        user = args[0]
        if user.age < 18:
            raise ValueError("No es mayor de edad...")
        return func(*args, **kwargs)
    return wrapper

@adult_only
def verify_if_user_is_adult(user):
    print("El usuario es mayor de edad")
    

def main():
    try:
        user = User(date(2010, 3, 12))
        print(f'la edad es {user.age}')
        verify_if_user_is_adult(user)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
