from django.test import TestCase
from Users.models import User
from Product.models import Product
from .models import Order, OrderItem

class OrderModelsTest(TestCase):

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

        # Create an order
        self.order = Order.objects.create(
            user=self.user,
            total_price=199.98,
            status='Pending'
        )

        # Create an order item
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price
        )

    def test_order_creation(self):
        # Check if the Order is created successfully
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.total_price, 199.98)
        self.assertEqual(self.order.status, 'Pending')

    def test_order_str_method(self):
        # Check the __str__ method of Order
        expected_str = f"Order {self.order.id} by {self.user.email}"
        self.assertEqual(str(self.order), expected_str)

    def test_order_item_creation(self):
        # Check if the OrderItem is created successfully
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, 99.99)

    def test_order_item_str_method(self):
        # Check the __str__ method of OrderItem
        expected_str = f"2 of {self.product.title} in order {self.order.id}"
        self.assertEqual(str(self.order_item), expected_str)