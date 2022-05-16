from rest_framework.test import APIClient
from datetime import date
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

TOKEN_URL = reverse('users:token')


class PublicUserAPITest(TestCase):
    """Test the public features from users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_token(self):
        """Test creating token"""
        payload = {
            'email': 'tomo@noku.com',
            'password': 'tomopassword123',
            'date_of_birth': date(year=1998, month=8, day=26)
        }
        get_user_model().objects.create_user(**payload)
        del payload['date_of_birth']
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
