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
            print("Monto agregado...")
            self._balance -= amount
            return True


class SavingsAccount(BankAccount):
    def __init__(self):
        super().__init__()
        self.min_balance = 100

    def add_balance(self, amount):
        super().add_balance(amount)
        print(f"el monto agregado es de...{amount}")

    def subtract_balance(self, amount):
        if self._balance >= amount:
            if self._balance - amount >= self.min_balance:
                super().subtract_balance(amount)
                print("Transaccion realizada...")
                print(f"Su balance es de {self._balance}")
            else:
                print(f"Monto supera el min_balance... total en cuenta: {self._balance}... disponible a retirar: {(self._balance - self.min_balance)}")
        else:
            print("Fondos insuficientes...")


savings_account = SavingsAccount()     
amount = int(input("Ingrese el monto que desea depositar..."))
savings_account.add_balance(amount)
substract = int(input("Ingrese el monto a retirar..."))
savings_account.subtract_balance(substract)

