from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from Shop.permissions import IsAdminUserOrReadOnly
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
    permission_classes = [IsAdminUserOrReadOnly]


class AttributeTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing attribute type instances.
    """
    queryset = AttributeType.objects.all()
    serializer_class = AttributeTypeSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ProductAttributeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product attribute instances.
    """
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ProductImageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product image instances.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUserOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.

    Attributes:
        queryset: The queryset used to retrieve objects.
        serializer_class: The serializer class used to validate and deserialize objects.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Return the list of permissions required for this view.
        """
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
               Override the create method to require authentication for creating products.
               """
        admin_check = self.check_admin(request)
        if admin_check:
            return admin_check

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def update(self, request, *args, **kwargs):
    """
    Override the update method to require authentication for updating products.
    """
    admin_check = self.check_admin(request)
    if admin_check:
        return admin_check

    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data)


def destroy(self, request, *args, **kwargs):
    """
    Override the destroy method to require authentication for deleting products.
    """
    admin_check = self.check_admin(request)
    if admin_check:
        return admin_check

    instance = self.get_object()
    self.perform_destroy(instance)
    return Response(status=status.HTTP_204_NO_CONTENT)


@action(detail=True, methods=['post'], url_path='attributes', serializer_class=ProductAttributeSerializer)
def add_attribute(self, request, pk=None):
    """
    Add attributes to a product. Requires authentication.
    """
    admin_check = self.check_admin(request)
    if admin_check:
        return admin_check
    product = self.get_object()
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(product=product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@action(detail=True, methods=['post'], url_path='images', serializer_class=ProductImageSerializer)
def add_image(self, request, pk=None):
    """
    Add images to a product. Requires authentication.
    """
    admin_check = self.check_admin(request)
    if admin_check:
        return admin_check
    product = self.get_object()
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(product=product)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
