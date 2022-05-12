import os

from datetime import datetime
# noinspection PyUnresolvedReferences
from core.models import game_image_path, GameModel
from django.contrib.auth import get_user_model
from django.test import TestCase
from unittest.mock import patch


class ModelsTests(TestCase):
    """Models tests"""
    test_email = 'takakara@nomuro.com'
    test_password = 'takakarapass123'
    test_date_of_birth = datetime(1996, 8, 20)

    def test_create_user(self):
        """Test valid user creation"""
        user = get_user_model().objects.create_user(
            email=self.test_email,
            password=self.test_password,
            date_of_birth=self.test_date_of_birth
        )
        self.assertEqual(user.email, self.test_email)
        self.assertEqual(user.date_of_birth, self.test_date_of_birth)
        self.assertTrue(user.check_password(self.test_password))

    def test_create_user_wo_username(self):
        """Test creating user without providing an username"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password=self.test_password,
                date_of_birth=self.test_date_of_birth
            )

    def test_create_superuser(self):
        """Test creating superuser"""
        user = get_user_model().objects.create_superuser(
            email=self.test_email,
            password=self.test_password,
            date_of_birth=self.test_date_of_birth
        )
        self.assertTrue(user.is_superuser)

    def test_create_game(self):
        """Test creating a game object"""
        game = GameModel.objects.create(
            name='Life is Strange',
            score=83,
            steam_price=36.99,
            gog_price=37.99
        )
        self.assertEqual(game.name, 'Life is Strange')
        self.assertEqual(game.score, 83)
        self.assertEqual(game.steam_price, 36.99)
        self.assertEqual(game.gog_price, 37.99)
        self.assertIsNone(game.epic_price)

    @patch('uuid.uuid4')
    def test_image_path(self, mock_uuid):
        """Test if the image is being correctly stored"""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        expected_result = os.path.join('uploads/game', f'{uuid}.jpg')
        output_result = game_image_path(None, 'someImage.jpg')
        self.assertEqual(expected_result, output_result)
