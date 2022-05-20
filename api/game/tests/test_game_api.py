from rest_framework.test import APIClient
# noinspection PyUnresolvedReferences
from core.models import GameModel
# noinspection PyUnresolvedReferences
from game.serializers import GameSerializer
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

GAME_URL = reverse('game:game-list')


class PublicGameAPITests(TestCase):
    """Test the public features of the game API tests"""

    def setUp(self):
        self.client = APIClient()

    def test_list_games(self):
        """Test retrieve all game objects"""
        GameModel.objects.create(
            name='Call of Duty',
            score=91,
        )
        GameModel.objects.create(
            name='The Witcher 3: Wild Hunt',
            score=93
        )

        games = GameModel.objects.all().order_by('name')
        serializer = GameSerializer(games, many=True)

        res = self.client.get(GAME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
