from scrapy_djangoitem import DjangoItem
# noinspection PyUnresolvedReferences
from core import models


class GameItem(DjangoItem):
    """Saves the scraped information about the games in the game model"""
    django_model = models.GameModel
