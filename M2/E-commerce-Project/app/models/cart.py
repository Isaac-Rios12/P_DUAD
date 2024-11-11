
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

    def get_cart(self, user_id):
        for cart in self.carts.values():
            if cart.user_id == user_id:
                return cart
        return None

    def add_cart(self, cart_id, user_id, products=None):
        #debo agregar una validacion de que el usuario este en lista de usuarios
        #validacion de que el producto exista
        #validacion de que la cantidad sea necesaria
        
        if cart_id not in self.carts:
            cart = Cart(cart_id, user_id, products)
            self.carts[cart_id] = cart
            
        return cart

    def remove_cart(self, cart_id):
        self.carts.remove(cart_id)

    def add_product_to_cart(self, id_user, id_product, quantity):
        cart = self.get_cart(id_user)

        if cart:

            product_found = False
            for product in cart.products:
                if product['product_id'] == id_product:
                    product["quantity"] += quantity
                    product_found = True
                    break

            if not product_found:
                cart.products.append({
                    'product_id': id_product,
                    'quantity': quantity
                })
        else:
            self.add_cart(id_user, id_user, [{'product_id': id_product, 'quantity': quantity}])

    def remove_product_to_cart(self, cart_id, product_id, quantity):
        cart = self.get_cart(cart_id)

        if cart:
            # Itera sobre los productos para encontrar el producto deseado
            for product in cart.products:
                if product['product_id'] == product_id:
                    # Si la cantidad actual es mayor que la cantidad a eliminar, solo resta la cantidad
                    if product['quantity'] > quantity:
                        product['quantity'] -= quantity
                    else:
                        # Si la cantidad a eliminar es igual o mayor a la cantidad del producto, elimina el producto de la lista
                        cart.products.remove(product)
                    break  # Termina después de actualizar o eliminar el producto
        else:
            print("El carrito no existe")


new_cart = CartHandler()

add_cart = new_cart.add_cart('cart1', 'user1', [{'product_id': 'prod1', 'quantity': 5}])

print (add_cart.__dict__)




    
