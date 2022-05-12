from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **kwargs):
        """Creates and returns a new user"""
        if not email:
            raise ValueError('An username must be set')
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        """Creates and returns a common user"""
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        """Creates and returns a common user"""
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if not kwargs.get("is_staff"):
            raise ValueError('Superuser must have is_staff=True')
        if not kwargs.get("is_superuser"):
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    objects = UserManager()

    class Meta:
        # Visible name of the model
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """Defines the string representation of the user objects as its
        email"""
        return self.email
