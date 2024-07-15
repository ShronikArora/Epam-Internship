from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    AttributeTypeViewSet,
    ProductAttributeViewSet,
    ProductImageViewSet,
    api_root
)

"""
This module configures the URL routing for the API.
"""

# Initialize the default router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'attribute-types', AttributeTypeViewSet)
router.register(r'product-attributes', ProductAttributeViewSet)
router.register(r'product-images', ProductImageViewSet)

# Define URL patterns
urlpatterns = [
    path('', api_root, name='api-root'),  # Root URL for API
    path('', include(router.urls)),  # Include the router URLs
]
