from models.user import UserHandler
from models.product import ProductHandler

class Cart:
    def __init__(self, cart_id, user_id, products=None):

        if products is None:
            products = []
        self.cart_id = cart_id
        self.user_id = user_id
        self.products = products


class CartHandler:

    def __init__(self):
        self.carts = {}

    def check_if_exist_product(self, id_product):
        product_instance = ProductHandler()
        exist_product = product_instance.get_product(id_product)

        if exist_product:
            return exist_product
        else:
            return{"message": f"El producto {id_product} no existe..."}
        
    def check_if_user_is_registrated(self, id_user):
        user_instance = UserHandler()
        exist_user = user_instance.get_user(id_user)

        if exist_user:
            return exist_user
        else:
            return{"message": f"El usuario {id_user} no se encuentra registrado"}
        
    def get_user_cart(self, user_id, cart_id):
        
        exist_user = self.check_if_user_is_registrated(user_id)
        if "message" in exist_user:
            return exist_user  
        
        
        cart = self.carts.get(cart_id)
        if not cart:
            return {"message": f"El carrito {cart_id} no existe"}, 404
        
        # Verificoo si el carrito pertenece al usuario correcto
        if cart.user_id != user_id:
            return {"message": f"El carrito {cart_id} no pertenece al usuario {user_id}"}, 403

        return cart  


    def get_cart(self, user_id):
        for cart in self.carts.values():
            if cart.user_id == user_id:
                return cart
        return None

    def add_cart(self, cart_id, user_id, products=None):
        # Verificar si el usuario está registrado
        exist_user = self.check_if_user_is_registrated(user_id)
        if "message" in exist_user:
            return exist_user 

        if products:
            for product in products:
                id_product = product.get('product_id')
                quantity = product.get('quantity', 0)
                
                exist_product = self.check_if_exist_product(id_product)
                if "message" in exist_product:
                    return exist_product  

                # Verifico la cantidad
                if quantity <= 0:
                    return {"message": f"La cantidad para el producto {id_product} debe ser mayor a cero."}

        # Si el carrito no existe, crearlo
        if cart_id not in self.carts:
            cart = Cart(cart_id, user_id, products)
            self.carts[cart_id] = cart
        else:
            cart = self.carts[cart_id]  

        return cart

    def remove_cart(self, cart_id):
        if cart_id in self.carts:
            del self.carts[cart_id]
        else:
            return {"message": f"El carrito {cart_id} no existe"}, 404

    def add_product_to_cart(self, id_user, id_product, id_cart, quantity):

        exist_user = self.check_if_user_is_registrated(id_user)
        if "message" in exist_user:
            return exist_user
        
        cart = self.carts.get(id_cart)

        if not cart:
            return {"message": f"El carrito {id_cart} no existe"}, 404
        
        product_instance = ProductHandler()
        exist_product = product_instance.get_product(id_product)

        if not exist_product:
            return{"message": f"El producto {id_product} no existe"}, 400
        
        product_found = False
        for product in cart.products:
            if product['product_id'] == id_product:
                if product["quantity"] + quantity > exist_product.quantity_product:
                    return {"message": f"Stock insuficiente para el producto {exist_product.name_product}"}, 400
                #si hay stock
                product["quantity"] += quantity
                product_found = True
                break

            #si no esta en el carrito lo agregamos
        
        if not product_found:
            
            if quantity > exist_product.quantity_product:
                return {"message": f"No hay suficiente stock del producto {exist_product.name_product}"}
            
            cart.products.append({
                'product_id': id_product,
                'quantity': quantity
            })

        return {"message": "Producto agregado al carrito correctamente"}, 200



    def remove_product_to_cart(self, user_id, cart_id, product_id, quantity):
        
        cart = self.get_user_cart(user_id, cart_id)
        if isinstance(cart, dict):
            return cart 

        
        for product in cart.products:
            if product['product_id'] == product_id:
                if product['quantity'] > quantity:
                    product['quantity'] -= quantity
                    return {"message": "Cantidad ajustada en el carrito"}, 200
                else:
                    cart.products.remove(product)
                    return {"message": "Producto eliminado del carrito"}, 200

        return {"message": f"El producto {product_id} no existe en el carrito"}, 404

new_cart = CartHandler()

add_cart = new_cart.add_cart('cart1', 'user1', [{'product_id': 'prod1', 'quantity': 5}])

# Creamos un objeto CartHandler
cart_handler = CartHandler()

# Agregamos un carrito para un usuario existente
cart = cart_handler.add_cart("cart1", "user1", [{"product_id": "prod1", "quantity": 5}])
print("Carrito agregado:")

# Caso 1: Agregar un producto existente con suficiente stock
resultado_agregar = cart_handler.add_product_to_cart("user1", "prod2", "cart1", 3)
print("Resultado agregar producto:", resultado_agregar)

# Caso 2: Intentar agregar un producto inexistente
resultado_agregar_inexistente = cart_handler.add_product_to_cart("user1", "prod99", "cart1", 2)
print("Resultado agregar producto inexistente:", resultado_agregar_inexistente)

# Caso 3: Agregar un producto pero con cantidad superior al stock disponible
resultado_agregar_stock_insuficiente = cart_handler.add_product_to_cart("user1", "prod2", "cart1", 100)
print("Resultado agregar producto con stock insuficiente:", resultado_agregar_stock_insuficiente)

# Caso 4: Eliminar cierta cantidad de un producto en el carrito
resultado_eliminar_cantidad = cart_handler.remove_product_to_cart("cart1", "prod1", 3)
print("Resultado eliminar cantidad del producto:", resultado_eliminar_cantidad)

# Caso 5: Eliminar más cantidad de la que tiene un producto, debería quitar el producto del carrito
resultado_eliminar_completamente = cart_handler.remove_product_to_cart("cart1", "prod1", 5)
print("Resultado eliminar producto completamente:", resultado_eliminar_completamente)





    
