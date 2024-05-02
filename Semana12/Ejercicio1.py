class BankAccount:

    def __init__(self):
        self._balance = 0

    def _add_Balance(self, amount):
        self._balance += amount

    def _substract_balance(self, amount):
        self._balance -= amount


class SavingsAccount(BankAccount):
    def __init__(self):
        super().__init__()
        self.min_balance = 100

    def add_balance(self, amount):
        self._add_Balance(amount)
        print(f"el monto agregado es de...{amount}")

    def check_withdrawal(self, substract):
        if self._balance - substract < self.min_balance:
            print("Monto supera el min_balance")
        else:
            self._substract_balance(substract)
            print("Transaccion realizada...")
            print(f"Su balance es de {self._balance}")

savings_account = SavingsAccount()      
amount = int(input("Ingrese el monto que desea depositar..."))
savings_account.add_balance(amount)
substract = int(input("Ingrese el monto a retirar..."))
savings_account.check_withdrawal(substract)

