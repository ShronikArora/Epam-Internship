from django.test import TestCase
from Users.models import User  
from Product.models import Product 
from .models import CartItem 
from Category.models import Category

class CartItemModelTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create(
            email='testuser@example.com'
        )
        # Create a product
        self.product = Product.objects.create(
            title='Test Product',
            brand='Test Brand',
            description='Test Description',
            price=99.99
        )

        # Create a cart item
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
            price=self.product.price
        )

    def test_cart_item_creation(self):
        # Check if the CartItem is created successfully
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.price, 99.99)

    def test_cart_item_str_method(self):
        # Check the __str__ method of CartItem
        expected_str = f"2 of {self.product.title} "
        self.assertEqual(str(self.cart_item), expected_str)

    def test_cart_item_unique_constraint(self):
        # Attempt to create a duplicate cart item 
        with self.assertRaises(Exception):
            CartItem.objects.create(
                user=self.user,
                product=self.product,
                quantity=1,
                price=self.product.price
            )
