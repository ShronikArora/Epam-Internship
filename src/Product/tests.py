from django.test import TestCase
from .models import Product, ProductAttribute, ProductImage, Category, AttributeType


class ProductModelTest(TestCase):
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
        self.assertEqual(str(self.parent_category), 'Parent Category')
        self.assertEqual(str(self.child_category), 'Child Category')
        self.assertEqual(str(self.child_category2), 'kid Category')
        self.assertEqual(str(self.child_category3), 'infant Category')

    def test_get_category_tree(self):
        # Checks the order that the Category is added in
        expected_order = [self.parent_category, self.child_category, self.child_category2, self.child_category3]
        category_tree = list(self.parent_category.get_category_tree())
        self.assertEqual(category_tree, expected_order)

    def test_infant_category_parent(self):
        # Check if the parent of 'infant Category' is 'kid Category'
        self.assertEqual(self.child_category3.parent, self.child_category2)
        # Check if the parent of 'kid Category' is 'Child Category'
        self.assertEqual(self.child_category2.parent, self.child_category)
        # Check if the parent of 'Child Category' is 'Parent Category'
        self.assertEqual(self.child_category.parent, self.parent_category)

    def test_parent_category_of_infant_category(self):
        # Check the ancestor for 'infant Category' to 'Parent Category'
        infant_parent_chain = []
        current_category = self.child_category3
        while current_category.parent is not None:
            infant_parent_chain.append(current_category.parent)
            current_category = current_category.parent
        expected_chain = self.parent_category
        self.assertEqual(infant_parent_chain[2], expected_chain)

    def test_product_creation(self):
        # Check if the Product is created successfully
        self.assertEqual(self.product.title, 'Test Product')
        self.assertEqual(self.product.brand, 'Test Brand')
        self.assertEqual(self.product.description, 'Test Description')
        self.assertEqual(self.product.category, self.child_category)
        self.assertEqual(self.product.price, 99.99)

    def test_product_str_method(self):
        # Check the __str__ method of Product
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_attribute_creation(self):
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
        type = AttributeType.objects.create(
            name='Color'
        )
        self.assertEqual(str(type), 'Color')

    def test_product_attribute_str_method(self):
        # Create a ProductAttribute
        attribute = ProductAttribute.objects.create(
            product=self.product,
            attribute_name=self.type,
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

    def test_related_name(self):
        product = self.product
        image = ProductImage.objects.create(product=product, image_url="http://example.com/image.jpg")
        related_images = product.images.all()
        self.assertIn(image, related_images)


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Test Category')

    def test_category_str_method(self):
        self.assertEqual(str(self.category), 'Test Category')
