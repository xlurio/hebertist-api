import numpy.random as np
import pandas as pd

from rest_framework.test import APIClient
# noinspection PyUnresolvedReferences
from core.models import GameModel, PriceModel, StoreModel
# noinspection PyUnresolvedReferences
from game.serializers import PriceSerializer, PriceDetailSerializer
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

BEST_PRICES_URL = reverse('game:price-best-prices')


def get_price_url(price_id=None):
    """Retrieves the price url"""
    if price_id:
        return reverse('game:price-detail', args=[price_id])
    else:
        return reverse('game:price-list')


def get_lowest_prices_id(price_query):
    price_data = pd.DataFrame(price_query.values())
    try:
        filtered_price_data = price_data[['id', 'game_id', 'price']].groupby(
            'game_id'
        ).min()
        return list(filtered_price_data['id'])
    except KeyError:
        raise KeyError(f'The available columns are: {price_data.columns}')


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


def create_multiple_price_objects():
    games = [
        'Tomb Raider',
        'Risk of Rain 2',
        'Grand Theft Auto San Andreas'
    ]
    stores = [
        ('Steam', 'https://store.steampowered.com/'),
        ('GoG.com', 'https://www.gog.com/'),
        ('Microsoft Store',
         'https://www.microsoft.com/pt-br/store/games/')
    ]
    prices = np.random(9, ) * 100
    prices = ['{0:.2f}'.format(price) for price in prices]
    price_counter = 0
    for game in games:
        for store in stores:
            create_price_object(
                game_name=game,
                store_name=store[0],
                store_link=store[1],
                price=float(prices[price_counter])
            )
        price_counter += 1


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
        self.assertEqual(res.data['results'], serializer.data)

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

    def test_retrieve_best_prices(self):
        """Test retrieving best game prices"""
        create_multiple_price_objects()
        price_query = PriceModel.objects.all().order_by('price')
        expected_prices_id = get_lowest_prices_id(price_query)
        best_prices_query = PriceModel.objects.filter(
            id__in=expected_prices_id
        ).order_by('price')[:20]
        serializer = PriceDetailSerializer(best_prices_query, many=True)
        res = self.client.get(BEST_PRICES_URL)
        self.assertEqual(res.data, serializer.data)

    def test_filter_best_prices(self):
        """Test filtering by game name"""
        create_multiple_price_objects()
        price_query = PriceModel.objects.all().order_by('price')
        expected_prices_id = get_lowest_prices_id(price_query)
        best_prices_query = PriceModel.objects.filter(
            id__in=expected_prices_id
        ).order_by('price')

        name_to_search = 'rain'
        best_prices_query = best_prices_query.filter(
            game__name__icontains=name_to_search
        )[2:20]

        serializer = PriceDetailSerializer(best_prices_query, many=True)
        parameters_payload = {
            'game_name': name_to_search,
            'from': 3,
            'to': 20,
        }
        res = self.client.get(BEST_PRICES_URL, parameters_payload)
        self.assertEqual(res.data, serializer.data)
