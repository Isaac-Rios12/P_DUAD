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
        try:
            if user.age < 18:
                print("No es mayor de edad...")
                return
            return func(*args, **kwargs)
        except ValueError as e:
            print(e)
    return wrapper

@adult_only
def verify_if_user_is_adult(user):
    print("El usuario es mayor de edad")
    
user = User(date(2010, 3, 12))
print(f'la edad es {user.age}')
verify_if_user_is_adult(user)

user = User(date(2022, 6, 1))
print(f'la edad es {user.age}')
verify_if_user_is_adult(user)

user = User(date(2003, 3, 1))
print(f'la edad es {user.age}')
verify_if_user_is_adult(user)
