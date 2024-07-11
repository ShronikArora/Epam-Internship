from rest_framework import serializers
from .models import Category, Product, ProductAttribute, ProductImage, AttributeType

"""
This file creates the Serializers for the Product Models.
"""


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.

    Attributes:
        name: Name of the category.
        parent: Name of parent category (uses django_mptt).
    """

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.

    Attributes:
        title: Title of the product.
        brand: Brand of the product.
        description: Short description of the product.
        category: Name of category (foreign key).
        price: Price of the product.
    """

    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        """
        Validate product attributes.

        :param data: Product data to validate.
        :return: Validated data.
        :raise serializers.ValidationError: If the price is less than or equal to zero.
        """
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return data


class AttributeTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for AttributeType model.

    Attributes:
        name: Name of the attribute.
    """

    class Meta:
        model = AttributeType
        fields = '__all__'


class ProductAttributeSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductAttribute model.

    Attributes:
        product: The product model (foreign key).
        attribute_name: The name of the attribute (foreign key).
        attribute_value: The value of the attribute.
    """

    class Meta:
        model = ProductAttribute
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model.

    Attributes:
        product: The product model (foreign key).
        image: The image of the product.
    """

    class Meta:
        model = ProductImage
        fields = '__all__'
