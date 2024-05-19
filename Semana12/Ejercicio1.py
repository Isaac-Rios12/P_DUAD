class BankAccount:

    def __init__(self):
        self._balance = 0

    def add_balance(self, amount):
        self._balance += amount

    def subtract_balance(self, amount):
        if self._balance < amount:
            print("Fondos insuficientes...")
            return False
        else:
            self._balance -= amount
            print("Monto retirado...")
            print(f"Su balance es de {self._balance}")
            return True


class SavingsAccount(BankAccount):
    def __init__(self, min_balance):
        super().__init__()
        self.min_balance = min_balance

    def add_balance(self, amount):
        super().add_balance(amount)
        print(f"el monto agregado es de...{amount}")

    def subtract_balance(self, amount):
        if self._balance - amount >= self.min_balance:
                super().subtract_balance(amount)      
        else:
                print(f"Operacion no realizada... total en cuenta: {self._balance}... disponible a retirar: {(self._balance - self.min_balance)}")

min_balance = int(input("Ingrese el balance minimo de su cuenta de ahorros..."))
savings_account = SavingsAccount(min_balance)     
amount = int(input("Ingrese el monto que desea depositar..."))
savings_account.add_balance(amount)
substract = int(input("Ingrese el monto a retirar..."))
savings_account.subtract_balance(substract)

