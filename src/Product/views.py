from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Category, Product, ProductAttribute, ProductImage, AttributeType
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    AttributeTypeSerializer,
    ProductAttributeSerializer,
    ProductImageSerializer
)

"""
This module contains viewsets for the API and the root API view.
"""


@api_view(['GET'])
def api_root(request, format=None):
    """
    Root endpoint for the API.

    Provides hyperlinks to the list endpoints of all models.

    :param request: The HTTP request object.
    :param format: The format suffix (optional).
    :return: A response containing the URLs of the list endpoints.
    """
    return Response({
        'categories': reverse('category-list', request=request, format=format),
        'products': reverse('product-list', request=request, format=format),
        'attribute-types': reverse('attributetype-list', request=request, format=format),
        'product-attributes': reverse('productattribute-list', request=request, format=format),
        'product-images': reverse('productimage-list', request=request, format=format),
    })


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing category instances.

    Attributes:
        queryset: The queryset used to retrieve objects.
        serializer_class: The serializer class used to validate and deserialize objects.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.

    Attributes:
        queryset: The queryset used to retrieve objects.
        serializer_class: The serializer class used to validate and deserialize objects.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AttributeTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing attribute type instances.
    """
    queryset = AttributeType.objects.all()
    serializer_class = AttributeTypeSerializer


class ProductAttributeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product attribute instances..
    """
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product image instances.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
