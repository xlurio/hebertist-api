from rest_framework.settings import api_settings
from user.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken


class CreateTokenViewSet(ObtainAuthToken):
    """View set to create an authentication token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
