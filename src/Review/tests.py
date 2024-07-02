from django.test import TestCase
from Users.models import User
from Product.models import Product
from Order.models import Order
from .models import Review


class ReviewModelTest(TestCase):

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

        # Create a review
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4.5,
            description='Test review description',
            order=self.order
        )

    def test_review_creation(self):
        # Check if the Review is created successfully
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(float(self.review.rating), 4.5)
        self.assertEqual(self.review.description, 'Test review description')
        self.assertEqual(self.review.order, self.order)

    def test_review_str_method(self):
        # Check the __str__ method of Review
        expected_str = f"Review by {self.user.email} for {self.product.title}"
        self.assertEqual(str(self.review), expected_str)
