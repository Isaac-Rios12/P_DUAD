import pytest

from app.models.cart import CartHandler

def test_carts_add_new_cart():
    
    cart_id = "1"
    user_id = "1"
    products = [{"product_id": "p1", "quantity": 1}]

    cart_instance = CartHandler()

    cart_instance.add_cart(cart_id, user_id, products)

    added_cart = cart_instance.get_cart(cart_id)
    
    assert added_cart is not None
    assert added_cart.cart_id == cart_id
    assert added_cart.user_id == user_id
    assert added_cart.products == products

def test_add_product_to_existing_cart():

    cart_instance = CartHandler()

    cart_instance.add_cart('cart1', 'user1', [{'product_id': 'prod1', 'quantity': 1}])

    cart = cart_instance.get_cart('user1')
    assert len(cart.products) == 1
    assert cart.products[0]['product_id'] == 'prod1'
    assert cart.products[0]['quantity'] == 1
    
    cart_instance.add_product_to_cart('user1', 'prod1', 2)

    assert cart.products[0]['quantity'] == 3

def test_add_product_to_existing_cart():

    cart_instance = CartHandler()

    cart_instance.add_cart('cart2', 'user2', [])

    cart_instance.add_product_to_cart('user2', 'prod2', 1)

    cart = cart_instance.get_cart('user2')
    assert cart.products[0]['product_id'] == 'prod2'
    assert cart.products[0]['quantity'] == 1

    print(cart.products)



