from django.test import TestCase
from .models import Category

class CategoryModelTest(TestCase):

    def setUp(self):
        # Create a category
        self.category = Category.objects.create(
            name='Test Category'
        )

    def test_category_creation(self):
        # Check if the Category is created successfully
        self.assertEqual(self.category.name, 'Test Category')

    def test_category_str_method(self):
        # Check the __str__ method of Category
        self.assertEqual(str(self.category), 'Test Category')