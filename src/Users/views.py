from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, action
from .models import User, Address
from Shop.permissions import IsOwnerOrReadOnly
from .serializers import CustomerRegistrationSerializer, AddressSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

"""
This file contains viewsets for the User API .
"""


@api_view(['GET'])
def api_root(request, format=None):
    """
        Root endpoint for the API.

        Provides hyperlinks to the list endpoints of user-related and token endpoints.
        """

    return Response({
        'registration': request.build_absolute_uri('/api/users/registration/'),
        'token_obtain': request.build_absolute_uri('/api/users/token/'),
        'token_refresh': request.build_absolute_uri('/api/users/token/refresh/'),
    })


class CustomerRegistrationView(generics.CreateAPIView):
    """
    A view for editing Customer registration instances.
    """

    serializer_class = CustomerRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": serializer.data,
            "message": "User registered successfully.",
            "token": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    A view for retrieving, updating, and deleting the authenticated user.
    """
    queryset = User.objects.all()
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """
    A view for changing the user's password.
    """
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)


class AddressListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating user addresses.
    """
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific address.
    """
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
