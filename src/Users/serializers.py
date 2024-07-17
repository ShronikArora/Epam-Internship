from rest_framework import serializers
from django.contrib.auth import get_user_model

"""
This file creates the Serializers for the Users Models.
"""
User = get_user_model()


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    """
        Serializer for Category model.

        Attributes:
            username: username from django.contrib.auth.models .
            email: email variable from django.contrib.auth.models.
            password: password variable from django.contrib.auth.models
            password_confirmation: password confirmation variable from django.contrib.auth.models
        """
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']

    def validate(self, data):
        """
              Validate category attributes.

              :param data: Category data to validate.
              :return: Validated data.
              :raise serializers.ValidationError: If a category with the same name already exists.
              """
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user
