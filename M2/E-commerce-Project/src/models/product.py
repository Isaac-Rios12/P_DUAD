import os
import json

class Product:
    def __init__(self, id_product, name_product, price_product, quantity_product, description_product ):
        self.id_product = id_product
        self.name_product = name_product
        self.price_product = price_product
        self.quantity_product = quantity_product
        self.description_product = description_product

class ProductHandler:
    def __init__(self):
        self.products_list = {}

    def get_product(self, id_product):
        return self.products_list.get(id_product)

    def validate_product(self, id_product, name_product, price_product, quantity_product, description_product):

        if not isinstance(id_product, int) or id_product <= 0:
            return {"message": "Error, el ID del product debe ser un número entero positivo"}, 400
        
        if not isinstance(name_product, str)or not name_product.strip():
            return {"message": "Error, el nombre del producto no es valido"}, 400
        
        if not isinstance(price_product, (int, float)) or price_product <= 0:
            return {"message": "Error, el precio del producto debe ser un número positivo"}, 400

        if not isinstance(quantity_product, int) or quantity_product < 0:
            return {"message": "Error, la cantidad del producto debe ser un número entero positivo"}, 400

        if not isinstance(description_product, str) or not description_product.strip():
            return {"message": "Error, la descripción del producto no es válida"}, 400
        
        return None

    def add_new_product(self, id_product, name, price, quantity, description):
        
        validation = self.validate_product(id_product, name, price, quantity, description)

        if validation:
            return validation

        if id_product in self.products_list:
            return {"message": "El producto se encuentra registrado"}, 400
        
        product = Product(id_product, name, price, quantity, description)
        self.products_list[id_product] = product
        print(f"Nuevo producto registrado...")
        return {"message": "Producto registrado correctamente", "user": vars(product)}, 201
    
    def delete_product(self, id_product):

        if not isinstance(id_product, int) or id_product <= 0:
            return {"message": "Error, el ID de usuario debe ser un número entero positivo"}, 400
        
        if id_product in self.products_list:
            del self.products_list[id_product]
            return {"message": f"El producto {id_product} ha sido eliminado"}, 200
        else:
            return {"message": f"El product {id_product} no existe en el registro"}, 404

    def update_product(self, id_product, new_name, new_price, new_quantity, new_description):

        validation = self.validate_product(id_product, new_name, new_price, new_quantity, new_description)

        if validation:
            return validation
        
        product = self.get_product(id_product)

        if not product:
            return {"message": "Error, usuario no encontrado"}, 404
        
        product.name_product = new_name
        product.price_product = new_price
        product.quantity_product = new_quantity
        product.description_product = new_description

        self.export_data("products.json")

        return {"message": f"Producto {id_product} actualizado correctamente", "user": vars(product)}, 200

        
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

    def export_data(self, file):
        try:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(self.products_list, f, indent=4)
                print("Informacion guardada...")
        except Exception as ex:
            print(f"Ha ocurrido un error: {ex}")
    
        
