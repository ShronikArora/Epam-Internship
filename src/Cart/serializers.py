from rest_framework import serializers
from .models import CartItem
from Product.models import Product


class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_title', 'product_price', 'quantity', 'total_price']
        read_only_fields = ['product_title', 'product_price', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price
