from django.test import TestCase
from Users.models import User
from Product.models import Product
from .models import CartItem
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from Order.models import Order, OrderItem
from Product.models import Product
from Users.models import Address

User = get_user_model()


class CartItemModelTest(TestCase):
    """
       Test case for the CartItem model.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user, product, and cart item.
        """
        # Create a user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
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
        )

    def test_cart_item_creation(self):
        """
        Test if the CartItem is created successfully.
        """
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)

    def test_cart_item_str_method(self):
        """
        Test the __str__ method of CartItem.
        """
        expected_str = f"2 of {self.product.title} "
        self.assertEqual(str(self.cart_item), expected_str)

    def test_cart_item_unique_constraint(self):
        """
        Test that creating a duplicate CartItem raises an IntegrityError.
        """
        with self.assertRaises(Exception):
            CartItem.objects.create(
                user=self.user,
                product=self.product,
                quantity=1,
            )


class CheckoutTestCase(APITestCase):
    """
    Test case for the checkout functionality.
    """

    def setUp(self):
        # Create a user, product, address, and cart item
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.product = Product.objects.create(title='Product 1', price=10.00)
        self.address = Address.objects.create(user=self.user, address_line='123 Main St', city='Anytown', state='CA',
                                              zip_code='12345', country='USA')
        self.cart_item = CartItem.objects.create(user=self.user, product=self.product, quantity=2)
        self.client.force_authenticate(user=self.user)

    def test_checkout_creates_order(self):
        """
        Test that performing checkout creates an order with the correct details.
        """
        url = reverse('cart-checkout')
        response = self.client.post(url, data={'address_id': self.address.id})

        # Assert that the order was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)

    def test_checkout_removes_cart_items(self):
        """
        Test that performing checkout removes cart items.
        """
        url = reverse('cart-checkout')
        self.client.post(url, data={'address_id': self.address.id})

        # Assert that the cart is now empty
        self.assertEqual(CartItem.objects.filter(user=self.user).count(), 0)
