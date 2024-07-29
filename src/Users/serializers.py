from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

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

            # Validate password strength
        try:
            validate_password(data['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

            # Check for unique username and email
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username is already taken.'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email is already in use.'})
        return data

    def create(self, validated_data):
        """
            Create a new user.
            :param validated_data: Validated user data.
            :return: The created user instance.
        """
        validated_data.pop('password_confirmation')
        user = User.objects.create_user(**validated_data)
        return user
