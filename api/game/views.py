import pandas as pd

from rest_framework.decorators import action
# noinspection PyUnresolvedReferences
from core.models import GameModel, PriceModel, StoreModel
# noinspection PyUnresolvedReferences
from game.serializers import (
    GameSerializer, PriceSerializer, PriceDetailSerializer, StoreSerializer
)
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status


class BasicGameAttrViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Basic view set class for the game API"""

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
    queryset = PriceModel.objects.all()
    serializer_class = PriceSerializer

    def get_queryset(self):
        """Retrieve the price objects"""
        return self.queryset.order_by('price')

    @action(detail=False, methods=['get'])
    def best_prices(self, request, pk=None):
        game_name = self.request.query_params.get('game_name')
        lowest_prices_ids = self.get_lowest_prices_ids()
        filtered_queryset = self.queryset.filter(id__in=lowest_prices_ids)

        if game_name:
            filtered_queryset = filtered_queryset.filter(
                game__name__icontains=game_name
            )

        ordered_queryset = filtered_queryset.order_by('price')[:20]
        serializer = self.get_serializer(ordered_queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def get_lowest_prices_ids(self):
        price_query = self.queryset.values()
        price_data = pd.DataFrame(price_query.values())
        try:
            filtered_price_data = price_data[
                ['id', 'game_id', 'price']
            ].groupby(
                ['game_id']
            ).min()
            return list(filtered_price_data['id'])
        except KeyError:
            raise KeyError(f'The available columns are: {price_data.columns}')

    def get_serializer_class(self):
        """Return the appropriated serializer class based on the action
        requested"""
        if self.action == 'retrieve' or self.action == 'best_prices':
            return PriceDetailSerializer
        return self.serializer_class
