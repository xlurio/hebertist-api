# noinspection PyUnresolvedReferences
from core.models import GameModel, PriceModel, StoreModel
from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    """Serializes the game objects"""

    class Meta:
        model = GameModel
        fields = ['id', 'name', 'score']
        read_only_fields = ['id']


class StoreSerializer(serializers.ModelSerializer):
    """Serializes the store objects"""

    class Meta:
        model = StoreModel
        fields = ['id', 'name', 'link']
        read_only_fields = ['id']


class PriceSerializer(serializers.ModelSerializer):
    """Serializes the store objects"""
    game = serializers.PrimaryKeyRelatedField(
        queryset=GameModel.objects.all()
    )
    store = serializers.PrimaryKeyRelatedField(
        queryset=StoreModel.objects.all()
    )

    class Meta:
        model = PriceModel
        fields = ['id', 'game', 'store', 'price', 'link']
        read_only_fields = ['id']


class PriceDetailSerializer(PriceSerializer):
    """Serialize the details of the price objects"""
    game = GameSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
