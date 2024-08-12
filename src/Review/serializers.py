from rest_framework import serializers
from .models import Review
from Order.models import Order


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Attributes:
        user: The user who created the review.
        product: The product being reviewed.
        rating: The rating given by the user.
        description: The review text.
        order: The order associated with the review.
    """

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'description', 'order']
        read_only_fields = ['user', 'order']

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']
        rating = data.get('rating')

        # Check if the user has bought the product before reviewing it
        if not Order.objects.filter(user=user, items__product=product).exists():
            raise serializers.ValidationError("You can only review products that you have purchased.")

        # Additional validation for rating (example: must be between 1 and 5)
        if rating and (rating < 1 or rating > 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
