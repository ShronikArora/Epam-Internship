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

    def validate(self, data):
        """
        Validate category attributes.

        :param data: Category data to validate.
        :return: Validated data.
        :raise serializers.ValidationError: If a category with the same name already exists.
        """
        # Check if a category with the same name already exists, excluding the current instance if updating
        if self.instance:
            if Category.objects.exclude(pk=self.instance.pk).filter(name=data['name']).exists():
                raise serializers.ValidationError("A category with this name already exists.")
        else:
            if Category.objects.filter(name=data['name']).exists():
                raise serializers.ValidationError("A category with this name already exists.")

        return data


class AttributeTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for AttributeType model.

    Attributes:
        name: Name of the attribute.
    """

    class Meta:
        model = AttributeType
        fields = ('id', 'name')

    def validate(self, data):
        """
        Validate attribute type.
        """
        name = data.get('name')
        if self.instance and self.instance.name != name and AttributeType.objects.filter(name=name).exists():
            raise serializers.ValidationError("An attribute with this name already exists.")
        return data


class ProductAttributeSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductAttribute model.

    Attributes:
        product: The product model (foreign key).
        attribute_name: The name of the attribute (foreign key).
        attribute_value: The value of the attribute.
    """
    attribute_name = AttributeTypeSerializer()

    class Meta:
        model = ProductAttribute
        fields = ('id', 'attribute_name', 'attribute_value')

    def create(self, validated_data):
        attribute_name_data = validated_data.pop('attribute_name')
        attribute_name_instance, created = AttributeType.objects.get_or_create(**attribute_name_data)
        if not created:
            # Handle existing AttributeType instance
            validated_data['attribute_name'] = attribute_name_instance
            validated_data['attribute_name'] = attribute_name_instance
            return super().create(validated_data)

        # New AttributeType instance created, validate and create ProductAttribute
        attribute_serializer = self.fields['attribute_name']
        attribute_instance = attribute_serializer.create(attribute_name_data)
        validated_data['attribute_name'] = attribute_instance
        return super().create(validated_data)


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model.

    Attributes:
        product: The product model (foreign key).
        image: The image of the product.
    """

    class Meta:
        model = ProductImage
        fields = ('id', 'image_url')


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
    attributes = ProductAttributeSerializer(many=True)
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'brand', 'description', 'category', 'price', 'attributes', 'images')

    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes', [])
        images_data = validated_data.pop('images', [])

        product = Product.objects.create(**validated_data)

        for attribute_data in attributes_data:
            attribute_serializer = ProductAttributeSerializer(data=attribute_data)
            attribute_serializer.is_valid(raise_exception=True)
            attribute_serializer.save(product=product)

        for image_data in images_data:
            image_serializer = ProductImageSerializer(data=image_data)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save(product=product)

        return product

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)

        # Update attributes
        instance.attributes.all().delete()
        for attribute_data in validated_data.get('attributes', []):
            attribute_name_data = attribute_data.pop('attribute_name', {})
            attribute_name_instance, _ = AttributeType.objects.get_or_create(**attribute_name_data)
            ProductAttribute.objects.create(product=instance, attribute_name=attribute_name_instance, **attribute_data)

        # Update images
        images_data = validated_data.get('images', [])
        instance.images.all().delete()  # Remove existing images
        for image_data in images_data:
            image_serializer = ProductImageSerializer(data=image_data)
            image_serializer.is_valid(raise_exception=True)
            image_serializer.save(product=instance)

        instance.save()
        return instance

    def validate(self, data):
        """
        Validate product attributes.

        :param data: Product data to validate.
        :return: Validated data.
        :raise serializers.ValidationError: If the price is less than or equal to zero.
        """
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")

        if self.instance:
            if Product.objects.exclude(pk=self.instance.pk).filter(title=data['title']).exists():
                raise serializers.ValidationError("A product with this title already exists.")
        else:
            if Product.objects.filter(title=data['title']).exists():
                raise serializers.ValidationError("A product with this title already exists.")

        return data
