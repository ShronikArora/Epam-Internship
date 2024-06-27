from django.test import TestCase
from .models import User, Address

class UserAddressModelTest(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create(
            email='testuser@example.com'
        )

    def test_user_creation(self):
        # Check if the User is created successfully
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_user_str_method(self):
        # Check the __str__ method of User
        self.assertEqual(str(self.user), 'testuser@example.com')

    def test_address_creation(self):
        # Create an Address
        address = Address.objects.create(
            address_line='123 Test Street',
            city='Test City',
            state='Test State',
            zip_code='12345',
            country='Test Country',
            user=self.user
        )

        # Check if the Address is created successfully
        self.assertEqual(address.address_line, '123 Test Street')
        self.assertEqual(address.city, 'Test City')
        self.assertEqual(address.state, 'Test State')
        self.assertEqual(address.zip_code, '12345')
        self.assertEqual(address.country, 'Test Country')
        self.assertEqual(address.user, self.user)

    def test_address_str_method(self):
        # Create an Address
        address = Address.objects.create(
            address_line='123 Test Street',
            city='Test City',
            state='Test State',
            zip_code='12345',
            country='Test Country',
            user=self.user
        )

        # Check the __str__ method of Address
        self.assertEqual(str(address), '123 Test Street, Test City, Test State, Test Country')

