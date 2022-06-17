import pandas as pd
import os
import sys
import uuid

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from datetime import date
from django.contrib.auth.hashers import make_password
from django.db import models
from django.conf import settings
from django.utils import timezone


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_image_path(instance, filename):
    """Returns the final path of the uploaded image"""
    extension = str(filename).split('.')[-1]
    filename = f'{uuid.uuid4()}.{extension}'
    return os.path.join('uploads/game', filename)


class UserManager(BaseUserManager):
    """Holds the methods to create new users"""

    def _create_user(self, email, password, date_of_birth, **kwargs):
        """Creates and returns a new user"""
        if not email:
            raise ValueError('An username must be set')
        if not date_of_birth:
            raise ValueError('An date of birth must be set')
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            **kwargs
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, **kwargs):
        """Creates and returns a common user"""
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(**kwargs)

    def create_superuser(self, **kwargs):
        """Creates and returns a common user"""
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if not kwargs.get("is_staff"):
            raise ValueError('Superuser must have is_staff=True')
        if not kwargs.get("is_superuser"):
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(**kwargs)


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
        """Visible name of the model"""
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        """Defines the string representation of the user objects as its
        email"""
        return self.email


class GameModel(models.Model):
    """Model of the game objects"""
    name = models.CharField(max_length=254, unique=True)
    score = models.IntegerField(null=True)
    image = models.ImageField(null=True, upload_to=get_image_path)

    class Meta:
        """Display the name of the game model on admin interface"""
        verbose_name = _('game')
        verbose_name_plural = _('games')

    def __str__(self):
        """Defines the string form of the game object as its name"""
        return self.name


def update_game_model():
    """Updates the game model data"""
    sys.path.append(os.path.join(BASE_DIR, '../../crawler'))
    # noinspection PyUnresolvedReferences
    from crawler.game_crawler import GameCrawler
    crawler = GameCrawler()
    crawler.run_crawler()


class StoreModel(models.Model):
    """Model of the game stores objects"""
    name = models.CharField(max_length=254, unique=True)
    link = models.URLField(unique=True)
    image = models.ImageField(null=True, upload_to=get_image_path)

    class Meta:
        """Display the name of the store model on admin interface"""
        verbose_name = _('store')
        verbose_name_plural = _('stores')

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = f'https://{self.name}.com/'
            super(StoreModel, self).save()

        super().save(*args, **kwargs)

    def __str__(self):
        """Defines the string form of the store objects as its name"""
        return self.name


class PriceModel(models.Model):
    """Model of the game prices objects"""
    game = models.ForeignKey(to='GameModel', on_delete=models.CASCADE)
    store = models.ForeignKey(to='StoreModel', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        """Display the name of the price model on admin interface"""
        verbose_name = _('price')
        verbose_name_plural = _('prices')

    def __str__(self):
        """Defines the string form of the price objects as the name of the
        game and of the store from which the price was provided"""
        return f'{str(self.game)} price on {str(self.store)}'


def update_price_model():
    """Updates the game model data"""
    sys.path.append(os.path.join(BASE_DIR, '../../crawler'))
    # noinspection PyUnresolvedReferences
    from crawler.price_crawler import PriceCrawler
    crawler = PriceCrawler()
    crawler.run_crawler()


class PriceHistoricModel(models.Model):
    """Models of the price historic objects"""
    game = models.ForeignKey(
        to='GameModel',
        on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=6, decimal_places=2)
    time_saved = models.DateField(unique_for_date='game',
                                  default=date.today)

    class Meta:
        """Display the name of the price historic model on admin interface"""
        verbose_name = 'price historic'
        verbose_name_plural = 'prices historic'

    def __str__(self):
        """Defines the string form of the price historic object as its game
        name and the time of the historic"""
        return f'{self.game} price at {str(self.time_saved)}'


def _save_price_historic_to_model(data_to_insert, time_saved=None):
    """Saves inserts data directly in a SQL data table"""
    if time_saved:
        for index, row in data_to_insert.iterrows():
            PriceHistoricModel.objects.create(
                game=GameModel.objects.get(id=int(row['game_id'])),
                price=float(row['price']),
                time_saved=time_saved,
            )
    else:
        for index, row in data_to_insert.iterrows():
            PriceHistoricModel.objects.create(
                game=GameModel.objects.get(id=int(row['game_id'])),
                price=float(row['price']),
            )


def save_price_historic(time_saved=None):
    """Saves the current lowest price of each game"""
    prices_data = pd.DataFrame(PriceModel.objects.all().values())
    prices_data = prices_data.groupby(by='game_id').min().reset_index()
    prices_data = prices_data[['game_id', 'price']]
    _save_price_historic_to_model(prices_data, time_saved)
    return PriceHistoricModel.objects.all()


class WishlistModel(models.Model):
    """Model of the wishes on the users wishlist"""
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    game = models.ForeignKey(
        to=GameModel,
        on_delete=models.CASCADE
    )
