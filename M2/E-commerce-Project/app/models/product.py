import os
import json

class Product:
    def __init__(self, id_product, name_product, price_product, quantity_product, description_product ):
        self.id_product = id_product
        self.name_product = name_product
        self.price_prodcut = price_product
        self.quantity_product = quantity_product
        self.description_product = description_product

class ProducHandler:
    def __init__(self):
        self.products_list = {}

    def add_new_product(self, id_product, name, price, quantity, description):
        if not isinstance(id_product, int) or id_product <= 0:
            print(f"Error, ID invalida")
            return None
        if not isinstance(name, str):
            print(f"Error, nombre Invalido")
            return None
        if not isinstance(price, float) or price <= 0:
            print(f"Error, el precio {price} es invalido.")
            return None
        if not isinstance(quantity, int) or quantity <= 0:
            print(f"Error, cantidad {quantity} no es valida")
        
        product = Product(id_product, name, price, quantity, description)
        self.products_list[id_product] = product
        print(f"Nuevo producto registrado...")
        return product
    
    def read_data(self, file):
        
        try:
            if not os.path.exists(file):
                print(f"El documento {file} no se encuentra...")
            
            with open(file, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                self.products_list = saved_data
                print("Datos leidos correctamente")

        except json.JSONDecodeError:
            print("Error al leer el archivo")
        except Exception as ex:
            print(f"Error {ex}")
    
        
