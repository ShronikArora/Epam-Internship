from django.test import TestCase
from .models import User, Address
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from .serializers import CustomerRegistrationSerializer
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class UserAddressModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com'
        )

    def test_user_creation(self):
        # Check if the User is created successfully
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.username, 'testuser')

    def test_user_str_method(self):
        # Check the __str__ method of User
        self.assertEqual(str(self.user), 'testuser')

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


User = get_user_model()


class CustomerRegistrationSerializerTest(TestCase):
    """
    Test case for the CustomerRegistrationSerializer.
    """

    def test_valid_data(self):
        """
        Test creating a user with valid data.
        Should succeed and create a new user.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Str0ngP@ssw0rd!',
            'password_confirmation': 'Str0ngP@ssw0rd!',
        }
        serializer = CustomerRegistrationSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)  # Print errors if validation fails
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])
        self.assertTrue(user.check_password(data['password']))

    def test_passwords_do_not_match(self):
        """
        Test creating a user when the passwords do not match.
        Should fail and raise a validation error.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password_confirmation': 'password321',
        }
        serializer = CustomerRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(serializer.errors['non_field_errors'][0], 'Passwords do not match.')


class CustomerRegistrationViewTest(APITestCase):
    """
    Test case for the CustomerRegistrationView.
    """

    def test_register_user(self):
        """
        Test registering a user with valid data.
        Should succeed and return the created user data.
        """
        url = reverse('customer_registration')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Str0ngP@ssw0rd!',
            'password_confirmation': 'Str0ngP@ssw0rd!',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], data['username'])
        self.assertEqual(response.data['user']['email'], data['email'])
        user = User.objects.get(username=data['username'])
        self.assertTrue(user.check_password(data['password']))

    def test_passwords_do_not_match(self):
        """
        Test registering a user when the passwords do not match.
        Should fail and return a 400 status with an error message.
        """
        url = reverse('customer_registration')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
            'password_confirmation': 'password321',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Passwords do not match.')


class TokenViewTest(APITestCase):
    """
    Test case for JWT token endpoints.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

    def test_token_obtain_successful(self):
        """
        Test obtaining a token with valid credentials.
        Should return a 200 status and tokens.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_token_refresh_successful(self):
        """
        Test refreshing the token with a valid refresh token.
        Should return a new access token.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'password123',
        }
        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']

        url_refresh = reverse('token_refresh')
        data_refresh = {
            'refresh': refresh_token,
        }
        response_refresh = self.client.post(url_refresh, data_refresh, format='json')
        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_refresh.data)
