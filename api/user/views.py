from rest_framework.settings import api_settings
# noinspection PyUnresolvedReferences
from user.serializers import (
    AuthTokenSerializer, UserSerializer, WishlistSerializer,
    WishlistDetailSerializer
)
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
# noinspection PyUnresolvedReferences
from core.models import WishlistModel


class CreateUserView(CreateAPIView):
    """View to create user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """View to create an authentication token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(RetrieveUpdateAPIView):
    """View to manage user"""
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user information"""
        return self.request.user


class WishlistViewSet(viewsets.ModelViewSet):
    """View to manage the wishlist objects"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = WishlistModel.objects.all()
    serializer_class = WishlistSerializer

    def get_queryset(self):
        """Return the wishlist objects"""
        return self.queryset.filter(user=self.request.user).order_by(
            'game__name'
        )

    def perform_create(self, serializer):
        """Create a wishlist object"""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return the appropriate serializer"""
        if self.action == 'retrieve':
            return WishlistDetailSerializer
        return self.serializer_class
