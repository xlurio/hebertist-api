from rest_framework.test import APIClient
# noinspection PyUnresolvedReferences
from core.models import GameModel, PriceModel, StoreModel
# noinspection PyUnresolvedReferences
from game.serializers import PriceSerializer, PriceDetailSerializer
from django.urls import reverse
from rest_framework import status
from django.test import TestCase


def get_price_url(price_id=None):
    """Retrieves the price url"""
    if price_id:
        return reverse('game:price-detail', args=[price_id])
    else:
        return reverse('game:price-list')


def create_price_object(game_name='Sample Game',
                        store_name='Sample Store',
                        store_link='https://store.sample.com/',
                        price=45.35):
    """Returns the necessary parameter for testing the price objects
    listing"""
    game = GameModel.objects.get_or_create(
        name=game_name,
    )[0]
    store = StoreModel.objects.get_or_create(
        name=store_name,
        link=store_link
    )[0]
    price = PriceModel.objects.create(
        game=game,
        store=store,
        price=price
    )
    return game, store, price


class PublicPriceAPITests(TestCase):
    """Test the public features of the price API"""

    def setUp(self):
        self.client = APIClient()

    def test_list_prices(self):
        """Test retrieving all price objects"""
        # Test parameters
        game_name1 = 'Hextech Mayhem: A League of Legends Story'
        game_name2 = 'V Rising'
        store_name1 = 'Steam'
        store_link1 = 'https://store.steampowered.com/'
        store_name2 = 'Origin'
        store_link2 = 'https://www.origin.com/'
        create_price_object(game_name=game_name1, store_name=store_name1,
                            store_link=store_link1)
        create_price_object(game_name=game_name1, store_name=store_name2,
                            store_link=store_link2)
        create_price_object(game_name=game_name2, store_name=store_name1,
                            store_link=store_link1)
        prices = PriceModel.objects.all().order_by('price')
        serializer = PriceSerializer(prices, many=True)
        res = self.client.get(get_price_url())

        # Assertions
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, res.data)

    def test_retrieve_details(self):
        """Test retrieving the details of the price objects"""
        game, store, price = create_price_object(
            game_name='Hextech Mayhem: A League of Legends Story',
            store_name='Steam',
            store_link='https://store.steampowered.com/'
        )
        serializer = PriceDetailSerializer(price)
        res = self.client.get(get_price_url(price.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
