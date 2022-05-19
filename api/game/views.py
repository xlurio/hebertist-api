from rest_framework.permissions import IsAuthenticated
# noinspection PyUnresolvedReferences
from core.models import GameModel, PriceModel, StoreModel
# noinspection PyUnresolvedReferences
from game.serializers import (
    GameSerializer, PriceSerializer, PriceDetailSerializer, StoreSerializer
)
from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication


class BasicGameAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Basic view set class for the game API"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the objects of the serializer"""
        return self.queryset.order_by('name')


class GameViewSet(BasicGameAttrViewSet):
    """View set to manage the game objects"""
    queryset = GameModel.objects.all()
    serializer_class = GameSerializer


class StoreViewSet(BasicGameAttrViewSet):
    """View set to manage the game objects"""
    queryset = StoreModel.objects.all()
    serializer_class = StoreSerializer


class PriceViewSet(viewsets.ModelViewSet):
    """View set to manage the price objects"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PriceModel.objects.all()
    serializer_class = PriceSerializer

    def get_queryset(self):
        """Retrieve the price objects"""
        return self.queryset.order_by('price')

    def get_serializer_class(self):
        """Return the appropriated serializer class based on the action
        requested"""
        if self.action == 'retrieve':
            return PriceDetailSerializer
        return self.serializer_class
