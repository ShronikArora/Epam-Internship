from django.test import TestCase
from Users.models import User, Address
from Product.models import Product
from .models import Order, OrderItem
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderModelsTest(TestCase):

    def setUp(self):
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

        # Create an order
        self.order = Order.objects.create(
            user=self.user,
            status='Pending'
        )
        self.address = Address.objects.create(
            address_line='123 Test Street',
            city='Test City',
            state='Test State',
            zip_code='12345',
            country='Test Country',
            user=self.user
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

    def test_order_total_price_property(self):
        # Test the total_price property of the Order model
        expected_total = Decimal('199.98').quantize(Decimal('0.00'))
        self.assertEqual(self.order.total_price, expected_total)

    def test_order_items_related_name(self):
        order_items = self.order.items.all()
        self.assertEqual(order_items.count(), 1)
        self.assertEqual(order_items[0], self.order_item)

    def test_order_address_str_method(self):
        # Create an Address
        address = Address.objects.create(
            address_line='123 Test Street',
            city='Test City',
            state='Test State',
            zip_code='12345',
            country='Test Country',
            user=self.user
        )


class OrderDetailTestCase(APITestCase):

    def setUp(self):
        # Create a user, product, order, and order item
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.product = Product.objects.create(title='Product 1', price=10.00)
        self.address = Address.objects.create(user=self.user, address_line='123 Main St', city='Anytown', state='CA',
                                              zip_code='12345', country='USA')
        self.order = Order.objects.create(user=self.user, address=self.address, status='pending')
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2,
                                                   price=self.product.price)
        self.client.force_authenticate(user=self.user)

    def test_order_detail_includes_product_name(self):
        # Get order details
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        response = self.client.get(url)

        # Assert that the response includes the product name
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('product_title', response.data['items'][0])
        self.assertEqual(response.data['items'][0]['product_title'], self.product.title)

    def test_order_detail_access(self):
        # Ensure that another user cannot access the order
        other_user = User.objects.create_user(username='otheruser', email='other@example.com', password='testpass')
        self.client.force_authenticate(user=other_user)
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
