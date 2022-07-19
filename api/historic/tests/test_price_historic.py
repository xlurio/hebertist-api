from rest_framework.test import APIClient
from datetime import date
from core.models import GameModel, PriceHistoricModel
from historic.serializers import (
    PriceHistoricSerializer, PriceHistoricDetailSerializer
)
from django.urls import reverse
from rest_framework import status
from django.test import TestCase


def get_price_historic_url(price_id=None):
    """Returns the price historic API url"""
    if price_id:
        return reverse('historic:price-detail', args=[price_id])
    else:
        return reverse('historic:price-list')


def create_price_historic(time_saved, game_name='Sample Game', price=29.99):
    """Creates and returns a price historic objects"""
    game = GameModel.objects.get_or_create(
        name=game_name,
    )[0]
    price = PriceHistoricModel.objects.create(
        game=game,
        price=price,
        time_saved=time_saved,
    )
    return game, price


class PublicPriceHistoricAPI(TestCase):
    """Test the private features of the price historic API"""
    def setUp(self):
        self.client = APIClient()

    def test_list_price_historic(self):
        """Test retrieving all price historic objects"""
        create_price_historic(
            time_saved=date(year=2022, month=2, day=6)
        )
        create_price_historic(
            time_saved=date(year=2022, month=3, day=6)
        )
        prices = PriceHistoricModel.objects.all().order_by('price')[:100]
        res = self.client.get(get_price_historic_url())
        serializer = PriceHistoricSerializer(prices, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_details(self):
        """Test retrieving the details of the price historic object"""
        _, price = create_price_historic(
            time_saved=date(year=2022, month=3, day=6)
        )
        serializer = PriceHistoricDetailSerializer(price)
        res = self.client.get(get_price_historic_url(price.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
