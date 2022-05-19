# noinspection PyUnresolvedReferences
from core.models import GameModel, PriceHistoricModel
# noinspection PyUnresolvedReferences
from game.serializers import GameSerializer
from rest_framework import serializers


class PriceHistoricSerializer(serializers.ModelSerializer):
    """Serializes the price historic objects"""
    game = serializers.PrimaryKeyRelatedField(
        queryset=GameModel
    )

    class Meta:
        model = PriceHistoricModel
        fields = ['id', 'game', 'price', 'time_saved']
        read_only_field = ['id']


class PriceHistoricDetailSerializer(PriceHistoricSerializer):
    """Serializes the details of the price historic objects"""
    game = GameSerializer(read_only=True)
