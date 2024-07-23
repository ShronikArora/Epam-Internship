from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerRegistrationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action


@api_view(['GET'])
def api_root(request, format=None):
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
