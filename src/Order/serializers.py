from rest_framework import serializers
from .models import Order, OrderItem
from Users.serializers import AddressSerializer
from Product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_title', 'quantity', 'price']
        read_only_fields = ['product_title']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'status', 'address', 'total_price', 'items']
        read_only_fields = ['user', 'order_date', 'total_price']
