from rest_framework.test import APIClient
from datetime import date
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')


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

    def test_create_token_nonexistent_user(self):
        """Test creating a token with credentials of a nonexistent user"""
        res = self.client.post(TOKEN_URL, {
            'email': 'sample@email.com',
            'password': 'samplepassword123',
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """Test creating a token with credentials of a nonexistent user"""
        payload = {
            'email': 'sample@email.com',
            'password': 'samplepassword123',
            'date_of_birth': date(year=1996, month=5, day=15),
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, {
            'email': payload['email'],
            'password': 'wrongpassword'
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_required_fields(self):
        """Test creating token with missing information in the credentials"""
        payload = {
            'email': 'sample@email.com',
            'password': 'samplepassword123',
            'date_of_birth': date(year=1996, month=5, day=15),
        }
        get_user_model().objects.create_user(**payload)
        del payload['date_of_birth']
        res = self.client.post(TOKEN_URL, {
            'email': payload['email'],
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_unauthorized_user_managing(self):
        """Test unauthorized access to user management API"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    """Test the private features of the user API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='sample@user.com',
            password='samplepassword123',
            date_of_birth=date(year=2000, month=3, day=30),
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_user_management(self):
        """Test user management access"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'date_of_birth': str(self.user.date_of_birth),
        })

    def test_post_on_management(self):
        """Test sending HTTP POST method to user management"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user information"""
        payload = {
            'password': 'otherpassword123',
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))
