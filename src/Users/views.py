from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerRegistrationSerializer


class CustomerRegistrationView(generics.CreateAPIView):
    """
    A viewset for editing Customer registration instances.
    """
    serializer_class = CustomerRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": serializer.data,
            "message": "User registered successfully."
        }, status=status.HTTP_201_CREATED)
