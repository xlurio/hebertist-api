from rest_framework.settings import api_settings
# noinspection PyUnresolvedReferences
from user.serializers import AuthTokenSerializer, UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication


class CreateTokenView(ObtainAuthToken):
    """View to create an authentication token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(RetrieveUpdateAPIView):
    """View to manage user"""
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        """Retrieve and return the authenticated user information"""
        return self.request.user
