from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CustomerRegistrationView,
    api_root
)

"""
This module configures the URL routing for the API.
"""

# Initialize the default router


# Define URL patterns
urlpatterns = [
    path('', api_root, name='api_root'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', CustomerRegistrationView.as_view(), name='customer_registration'),
]
