from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model


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
