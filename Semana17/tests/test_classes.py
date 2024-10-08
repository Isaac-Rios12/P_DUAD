import pytest
from data.classes import FinanceManager, Category

def test_clasess_add_category():
    fm = FinanceManager()
    fm.add_category("Casa")

    assert len(fm.categories) == 1
    assert fm.categories[0].getName() == "Casa"

def test_classes_add_transaction():
    fm = FinanceManager()
    category = Category("Alimentos")
    fm.add_category(category.getName())
    fm.add_transaction("Compra quincena", 50.000, category.getName(), "Gasto")

    assert len(fm.transactions) == 1

    added_transaction = fm.transactions[0]
    assert added_transaction.getTitle() == "Compra quincena"
    assert added_transaction.getAmount() == 50.000
    assert added_transaction.getCategory() == category.getName()
    assert added_transaction.getType() == "Gasto"

def test_classes_save_data():
    fm = FinanceManager()

    fm.add_category("Alimentos")
    fm.add_category("Entretenimiento")

    fm.add_transaction("compra en Pali", 10.000, "Alimentos", "Gasto")
    fm.add_transaction("Entradas museos", 20.000, "Entretenimiento", "Gasto")

    test_file = "test_finanzas.json"
    fm.save_data(test_file)

    saved_data = fm.read_data("test_finanzas.json")

    expected_data = {
        "transactions": [
            {
                "title": "compra en Pali",
                "amount": 10.000,
                "category": "Alimentos",
                "type": "Gasto"
            },
            {
                "title": "Entradas museos",
                "amount": 20.000,
                "category": "Entretenimiento",
                "type": "Gasto"
            }
        ],
        "categories": [
            "Alimentos",
            "Entretenimiento"
        ]
    }

   
    assert saved_data == expected_data, f"Los datos guardados no coinciden con los esperados. Guardado: {saved_data}, Esperado: {expected_data}"

def test_read_data_and_show():

    path = "test_finanzas.json"
    
    fm = FinanceManager()
    saved_data = fm.read_data(path)

    print(f"el diccionario es {saved_data}")


