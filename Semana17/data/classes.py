class Category:
    def __init__(self, name):
        self.name =name

    def getName(self):
        return self.name
    

class Transaction:
    def __init__(self, title, amount, category, type):
        self.title = title
        self.amount = amount
        self.category = category
        self.type = type 

    def getTitle(self):
        return self.title
    def getAmount(self):
        return self.amount
    def getCategory(self):
        return self.category
    def getType(self):
        return self.type

class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.categories = []

    def add_transaction(self, title, amount, category, type):
        transaction = Transaction(title, amount, category, type)
        self.transactions.append(transaction)
    
    def add_category(self, name):
        category = Category(name)
        self.categories.append(category)

    def save_data(self, file):

        try:
            transactions_data = []

            for t in self.transactions:
                transactions_data.append({
                    "title": t.getTitle(),
                    "amount": t.getAmount(),
                    "category": t.getCategory(),
                    "type": t.getType()
                })

            categories_data = []

            for c in self.categories:
                transactions_data.append(c.getName())
                
        except Exception as e:
            print("problema")
