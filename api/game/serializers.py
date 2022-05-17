# noinspection PyUnresolvedReferences
from core.models import GameModel
from rest_framework import serializers


class GameSerializer(serializers.ModelSerializer):
    """Serializes the game objects"""

    class Meta:
        model = GameModel
        fields = ['id', 'name', 'score', ]
