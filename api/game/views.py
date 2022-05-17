from rest_framework.permissions import IsAuthenticated
# noinspection PyUnresolvedReferences
from core.models import GameModel
# noinspection PyUnresolvedReferences
from game.serializers import GameSerializer
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication


class BasicGameAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Basic view set class for the game API"""

    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        """Return the objects of the serializer"""
        return self.queryset.order_by('name')


class GameViewSet(BasicGameAttrViewSet):
    """View set to manage the game objects"""

    queryset = GameModel.objects.all()
    serializer_class = GameSerializer
