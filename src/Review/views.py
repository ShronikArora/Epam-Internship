from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import ReviewSerializer
from Shop.permissions import IsOwnerOrReadOnly
from Order.models import Order


class ReviewViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing review instances.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned reviews to a given product by filtering against
        a `product_id` query parameter in the URL.
        """
        queryset = Review.objects.all()
        product_id = self.kwargs.get('product_id')  # Assumes the URL includes `product_id`

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, order=self.get_order())

    def get_order(self):
        product_id = self.request.data.get('product')
        if not product_id:
            raise serializers.ValidationError("Product ID is required.")

        try:
            # Convert product_id to integer if needed
            product_id = int(product_id)
        except ValueError:
            raise serializers.ValidationError("Invalid product ID format.")

        # Validate if the user has purchased the product
        order = Order.objects.filter(user=self.request.user, items__product_id=product_id).first()
        if not order:
            raise serializers.ValidationError("You need to have purchased this product to review it.")
        return order
