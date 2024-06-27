from django.test import TestCase
from .models import Product, ProductAttribute, ProductImage
from Category.models import Category

class ProductModelTest(TestCase):
    # Creates a category and Product
    def setUp(self):
        
        self.category = Category.objects.create(
            name='Test Category'
        )

        self.product = Product.objects.create(
            title='Test Product',
            brand='Test Brand',
            description='Test Description',
            category=self.category,
            price=99.99
        )

    def test_product_creation(self):
        # Check if the Product is created successfully
        self.assertEqual(self.product.title, 'Test Product')
        self.assertEqual(self.product.brand, 'Test Brand')
        self.assertEqual(self.product.description, 'Test Description')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.price, 99.99)

    def test_product_str_method(self):
        # Check the __str__ method of Product
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_attribute_creation(self):
        # Create a ProductAttribute
        attribute = ProductAttribute.objects.create(
            product=self.product,
            attribute_name='Color',
            attribute_value='Red'
        )

        # Check if the ProductAttribute is created successfully
        self.assertEqual(attribute.product, self.product)
        self.assertEqual(attribute.attribute_name, 'Color')
        self.assertEqual(attribute.attribute_value, 'Red')

    def test_product_attribute_str_method(self):
        # Create a ProductAttribute
        attribute = ProductAttribute.objects.create(
            product=self.product,
            attribute_name='Color',
            attribute_value='Red'
        )

        # Check the __str__ method of ProductAttribute
        self.assertEqual(str(attribute), 'Color: Red')

    def test_product_image_creation(self):
        # Create a ProductImage
        image = ProductImage.objects.create(
            product=self.product,
            image_url='http://example.com/image.jpg'
        )

        # Check if the ProductImage is created successfully
        self.assertEqual(image.product, self.product)
        self.assertEqual(image.image_url, 'http://example.com/image.jpg')

    def test_product_image_str_method(self):
        # Create a ProductImage
        image = ProductImage.objects.create(
            product=self.product,
            image_url='http://example.com/image.jpg'
        )

        # Check the __str__ method of ProductImage
        self.assertEqual(str(image), 'http://example.com/image.jpg')
