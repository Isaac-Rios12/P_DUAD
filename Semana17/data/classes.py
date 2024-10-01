import os
import json

class Category:
    def __init__(self, name):
        self.name = name

class Transaction:
    def __init__(self, title, amount, category, type):
        self.title = title
        self.amount = amount
        self.category = category
        self.type = type 

class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.categories = []

    def add_transaction(self, title, amount, category, type):
        transaction = Transaction(title, amount, category, type)
        self.transactions.append(transaction)
        
    def add_category(self, name):

        for category in self.categories:
            if category.name == name:
                print("Categoria ya existente...")
                return False
        
        category = Category(name)
        self.categories.append(category)
        return True

    def get_categories(self):
        return [category.name for category in self.categories]

    def export_data(self, file):
        try:
            dir_name = os.path.dirname(file)
            if not os.path.exists(dir_name) and dir_name != '':
                os.makedirs(dir_name)

            transactions_data = []
            for t in self.transactions:
                transactions_data.append({
                    "title": t.title,
                    "amount": t.amount,
                    "category": t.category,
                    "type": t.type
                })

            categories_data = [c.name for c in self.categories]

            data = {
                "transactions": transactions_data,
                "categories": categories_data
            }

            with open(file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                print("Agregado...")
                
        except Exception as e:
            print(f"Problema al guardar datos: {e}")

    def import_data(self, file):
        try:
            if not os.path.exists(file):
                print("Documento no encontrado...")
                self.export_data(file)

            with open(file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)

                self.transactions = []
                self.categories = []

                for t in saved_data.get("transactions", []):
                    self.add_transaction(t["title"], t["amount"], t["category"], t["type"])

                for c in saved_data.get("categories", []):
                    self.add_category(c)

                return saved_data
        except json.JSONDecodeError as e:
            print(f"Error al leer el archivo JSON: {e}")
        except Exception as e:
            print(f"Problema al cargar datos: {e}")
