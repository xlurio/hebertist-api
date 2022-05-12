from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTests(TestCase):
    """Models tests"""
    test_username = 'takakara123'
    test_password = 'takakarapass123'
    test_email = 'takakara@nomuro.com'
    test_date_of_birth = datetime(1996, 8, 20)

    def test_create_user(self):
        """Test valid user creation"""
        user = get_user_model().objects.create_user(
            username=self.test_username,
            password=self.test_password,
            email=self.test_email,
            date_of_birth=self.test_date_of_birth
        )
        self.assertEqual(user.username, 'takakara123')
        self.assertEqual(user.email, 'takakara@nomuro.com')
        self.assertTrue(user.check_password('takakarapass123'))

    def test_create_user_wo_username(self):
        """Test creating user without providing an username"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                username=None,
                password=self.test_password,
                email=self.test_email,
                date_of_birth=self.test_date_of_birth
            )

    def test_create_superuser(self):
        """Test creating superuser"""
        user = get_user_model().objects.create_superuser(
            username=self.test_username,
            password=self.test_password,
            email=self.test_email,
            date_of_birth=self.test_date_of_birth
        )
        self.assertTrue(user.is_superuser)
