from django.test import TestCase
from .models import Product, ProductAttribute, ProductImage, Category, AttributeType
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    AttributeTypeSerializer,
    ProductAttributeSerializer,
    ProductImageSerializer
)
from django.contrib.auth import get_user_model

"""
This module contains test cases for the Product, ProductAttribute, ProductImage, Category, and AttributeType models,
as well as API tests and serializer tests.
"""


class ProductModelTest(TestCase):
    """
        Test case for the Product model.
    """

    # Creates a category and Product
    def setUp(self):
        self.parent_category = Category.objects.create(name='Parent Category')
        self.child_category = Category.objects.create(name='Child Category', parent=self.parent_category)
        self.child_category2 = Category.objects.create(name='kid Category', parent=self.child_category)
        self.child_category3 = Category.objects.create(name='infant Category', parent=self.child_category2)

        self.product = Product.objects.create(
            title='Test Product',
            brand='Test Brand',
            description='Test Description',
            category=self.child_category,
            price=99.99
        )
        self.type = AttributeType.objects.create(
            name='Color'
        )

    def test_category_str_method(self):
        """
        Test the __str__ method of Category model.
        """

        self.assertEqual(str(self.parent_category), 'Parent Category')
        self.assertEqual(str(self.child_category), 'Child Category')
        self.assertEqual(str(self.child_category2), 'kid Category')
        self.assertEqual(str(self.child_category3), 'infant Category')

    def test_get_category_tree(self):
        """
        Test getting the category tree.
        """
        expected_order = [self.parent_category, self.child_category, self.child_category2, self.child_category3]
        category_tree = list(self.parent_category.get_category_tree())
        self.assertEqual(category_tree, expected_order)

    def test_infant_category_parent(self):
        """
        Test the parent categories of 'Infant Category'.
        """
        # Check if the parent of 'infant Category' is 'kid Category'
        self.assertEqual(self.child_category3.parent, self.child_category2)
        # Check if the parent of 'kid Category' is 'Child Category'
        self.assertEqual(self.child_category2.parent, self.child_category)
        # Check if the parent of 'Child Category' is 'Parent Category'
        self.assertEqual(self.child_category.parent, self.parent_category)

    def test_parent_category_of_infant_category(self):
        """
        Test the ancestor chain from 'Infant Category' to 'Parent Category'.
        """
        # Check the ancestor for 'infant Category' to 'Parent Category'
        infant_parent_chain = []
        current_category = self.child_category3
        while current_category.parent is not None:
            infant_parent_chain.append(current_category.parent)
            current_category = current_category.parent
        expected_chain = self.parent_category
        self.assertEqual(infant_parent_chain[2], expected_chain)

    def test_product_creation(self):
        """
        Test the creation of a Product instance.
        """
        # Check if the Product is created successfully
        self.assertEqual(self.product.title, 'Test Product')
        self.assertEqual(self.product.brand, 'Test Brand')
        self.assertEqual(self.product.description, 'Test Description')
        self.assertEqual(self.product.category, self.child_category)
        self.assertEqual(self.product.price, 99.99)

    def test_product_str_method(self):
        """
        Test the __str__ method of Product model.
        """
        # Check the __str__ method of Product
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_attribute_creation(self):
        """
        Test the creation of a ProductAttribute instance.
        """
        # Create a ProductAttribute
        attribute = ProductAttribute.objects.create(
            product=self.product,
            attribute_name=self.type,
            attribute_value='Red'
        )

        # Check if the ProductAttribute is created successfully
        self.assertEqual(attribute.product, self.product)
        self.assertEqual(attribute.attribute_name, self.type)
        self.assertEqual(attribute.attribute_value, 'Red')

    def test_product_attribute_type_str_method(self):
        """
        Test the __str__ method of AttributeType model.
        """
        type = AttributeType.objects.create(
            name='Color'
        )
        self.assertEqual(str(type), 'Color')

    def test_product_attribute_str_method(self):
        """
        Test the __str__ method of ProductAttribute model.
        """
        # Create a ProductAttribute
        attribute = ProductAttribute.objects.create(
            product=self.product,
            attribute_name=self.type,
            attribute_value='Red'
        )

        # Check the __str__ method of ProductAttribute
        self.assertEqual(str(attribute), 'Color: Red')

    def test_product_image_creation(self):
        """
        Test the creation of a ProductImage instance.
        """
        image = ProductImage.objects.create(
            product=self.product,
            image_url='http://example.com/image.jpg'
        )

        # Check if the ProductImage is created successfully
        self.assertEqual(image.product, self.product)
        self.assertEqual(image.image_url, 'http://example.com/image.jpg')

    def test_product_image_str_method(self):
        """
        Test the __str__ method of ProductImage model.
        """
        # Create a ProductImage
        image = ProductImage.objects.create(
            product=self.product,
            image_url='http://example.com/image.jpg'
        )

        # Check the __str__ method of ProductImage
        self.assertEqual(str(image), 'http://example.com/image.jpg')

    def test_related_name(self):
        """
        Test the related name for ProductImage instances.
        """
        product = self.product
        image = ProductImage.objects.create(product=product, image_url="http://example.com/image.jpg")
        related_images = product.images.all()
        self.assertIn(image, related_images)


class CategoryModelTest(TestCase):
    """
    Test case for the Category model.
    """

    def setUp(self):
        """
        Set up initial test data.
        """
        self.category = Category.objects.create(
            name='Test Category'
        )

    def test_category_creation(self):
        """
        Test the creation of a Category instance.
        """
        self.assertEqual(self.category.name, 'Test Category')

    def test_category_str_method(self):
        """
        Test the __str__ method of Category model.
        """
        self.assertEqual(str(self.category), 'Test Category')


class ProductAPITestCase(TestCase):
    """
    Test case for the Product API endpoints.
    """

    def setUp(self):
        """
        Set up initial test data and API client.
        """
        self.client = APIClient()

        # Create and authenticate a superuser
        self.User = get_user_model()
        self.user = self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            title='Laptop',
            brand='BrandX',
            description='A high-performance laptop',
            category=self.category,
            price=1000.00
        )
        self.attribute_type = AttributeType.objects.create(name='Color')
        self.product_attribute = ProductAttribute.objects.create(
            product=self.product,
            attribute_name=self.attribute_type,
            attribute_value='Black'
        )
        self.product_image = ProductImage.objects.create(
            product=self.product,
            image_url='http://example.com/image.jpg'
        )

    def test_get_categories(self):
        """
        Test the retrieval of categories through the API.
        """
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_products(self):
        """
        Test the retrieval of products through the API.
        """
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_attribute_types(self):
        """
        Test the retrieval of attribute types through the API.
        """
        url = reverse('attributetype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_attributes(self):
        """
        Test the retrieval of product attributes through the API.
        """
        url = reverse('productattribute-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_images(self):
        """
        Test the retrieval of product images through the API.
        """
        url = reverse('productimage-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_product(self):
        """
        Test the creation of a new product through the API.
        """
        url = reverse('product-list')
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Smartphone',
            'brand': 'BrandY',
            'description': 'A feature-packed smartphone',
            'category': self.category.id,
            'price': '500.00',
            'attributes': [],
            'images': []
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(id=response.data['id']).title, 'Smartphone')

    def test_create_duplicate_product(self):
        """
        Test creating a product with a duplicate title.
        """
        url = reverse('product-list')
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Laptop',
            'brand': 'BrandY',
            'description': 'Another high-performance laptop',
            'category': self.category.id,
            'price': '1200.00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product(self):
        """
        Test deleting a product through the API.
        """
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_update_product(self):
        """
        Test updating a product through the API.
        """
        url = reverse('product-detail', kwargs={'pk': self.product.id})
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'Updated Laptop',
            'brand': 'BrandX',
            'description': 'An updated high-performance laptop',
            'category': self.category.id,
            'price': '1100.00',
            'attributes': [],
            'images': []
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(id=self.product.id).title, 'Updated Laptop')


class ProductSerializerTestCase(TestCase):
    """
    Test case for the ProductSerializer and related serializers.
    """

    def setUp(self):
        """
        Set up initial test data.
        """
        self.client = APIClient()

        # Create and authenticate a superuser
        self.User = get_user_model()
        self.user = self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            title='Laptop',
            brand='BrandX',
            description='A high-performance laptop',
            category=self.category,
            price=1000.00
        )
        self.attribute_type = AttributeType.objects.create(name='Color')
        self.product_attribute = ProductAttribute.objects.create(
            product=self.product,
            attribute_name=self.attribute_type,
            attribute_value='Black'
        )
        self.product_image = ProductImage.objects.create(
            product=self.product,
            image_url='http://example.com/image.jpg'
        )

    def test_product_serializer(self):
        """
        Test the ProductSerializer.
        """
        serializer = ProductSerializer(self.product)
        self.assertEqual(serializer.data['title'], 'Laptop')
        self.assertEqual(serializer.data['brand'], 'BrandX')
        self.assertEqual(serializer.data['description'], 'A high-performance laptop')
        self.assertEqual(serializer.data['category'], self.category.id)
        self.assertEqual(serializer.data['price'], '1000.00')

    def test_attribute_type_serializer(self):
        """
        Test the AttributeTypeSerializer.
        """
        serializer = AttributeTypeSerializer(self.attribute_type)
        expected_data = {
            'id': self.attribute_type.id,
            'name': self.attribute_type.name
        }
        self.assertEqual(serializer.data, expected_data)

    def test_product_attribute_serializer(self):
        serializer = ProductAttributeSerializer(self.product_attribute)
        # Ensure attribute_name is serialized correctly
        self.assertEqual(serializer.data['attribute_name']['id'], self.attribute_type.id)
        # Ensure other fields are serialized correctly
        self.assertEqual(serializer.data['attribute_value'], 'Black')
        # Since 'product' is not directly serialized, access it via the instance
        self.assertEqual(serializer.instance.product.id, self.product.id)

    def test_product_image_serializer(self):
        serializer = ProductImageSerializer(self.product_image)
        # Ensure 'image_url' is serialized correctly
        self.assertEqual(serializer.data['image_url'], 'http://example.com/image.jpg')
        # Since 'product' is not directly serialized, access it via the instance
        self.assertEqual(serializer.instance.product.id, self.product.id)
