from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CartItem
from .serializers import CartItemSerializer
from Order.models import Order, OrderItem
from Order.serializers import OrderSerializer
from Users.models import Address


class CartItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing the user's cart items.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return the cart items for the authenticated user
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user to the currently authenticated user
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        # Ensure the user is the owner of the cart item being updated
        if serializer.instance.user != self.request.user:
            return Response({"error": "You do not have permission to modify this cart item."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        # Ensure the user is the owner of the cart item being deleted
        instance = self.get_object()
        if instance.user != self.request.user:
            return Response({"error": "You do not have permission to delete this cart item."},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def total_price(self, request):
        """
        Calculate the total price of all items in the user's cart.
        """
        cart_items = self.get_queryset()
        total = sum(item.quantity * item.product.price for item in cart_items)
        return Response({"total_price": total}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """
        Checkout the cart items and create an order.
        """
        cart_items = self.get_queryset()
        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        address_id = request.data.get('address_id')
        if not address_id:
            return Response({"error": "Address is required."}, status=status.HTTP_400_BAD_REQUEST)

        address = Address.objects.filter(id=address_id, user=request.user).first()
        if not address:
            return Response({"error": "Invalid address."}, status=status.HTTP_400_BAD_REQUEST)

        # Create the order
        order = Order.objects.create(user=request.user, address=address, status='pending')

        # Create order items
        order_items = [
            OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        # Clear the cart
        cart_items.delete()

        # Serialize the order and return the response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
