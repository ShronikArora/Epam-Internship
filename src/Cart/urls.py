from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CartItemViewSet

router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    path('', include(router.urls)),
    path('cart-items/checkout/', CartItemViewSet.as_view({'post': 'checkout'}), name='cart-checkout'),
]
