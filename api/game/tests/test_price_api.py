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


def make_price_objects():
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
        self._given_the_objects()
        result = self._when_prices_endpoint_receives_get_request()
        self._then_should_list_all_price_objects(result)

    def _when_prices_endpoint_receives_get_request(self):
        return self.client.get(get_price_url())

    def _then_should_list_all_price_objects(self, result):
        prices = PriceModel.objects.all().order_by('price')
        serializer = PriceSerializer(prices, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data['results'], serializer.data)

    def test_retrieve_details(self):
        """Test retrieving the details of the price objects"""
        price = self._given_the_object()

        detail_endpoint_url = get_price_url(price.id)
        result = self._when_price_detail_endpoint_is_requested(
            detail_endpoint_url
        )

        self._then_should_retrieve_price_details(result, price)

    def _given_the_object(self):
        _, _, price = create_price_object(
            game_name='Hextech Mayhem: A League of Legends Story',
            store_name='Steam',
            store_link='https://store.steampowered.com/'
        )

        return price

    def _when_price_detail_endpoint_is_requested(self, url):
        return self.client.get(url)

    def _then_should_retrieve_price_details(self, result, price_object):
        serializer = PriceDetailSerializer(price_object)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_filter_prices_by_game_id(self):
        """Test game ID filter on prices endpoint"""
        self._given_the_objects()
        price = self._given_the_object()
        result = self._when_prices_endpoint_is_requested_with_arguments(
            {'game_id': price.game.id}
        )
        self._then_should_filter_prices_by_game_id(result, price.game.id)

    def _when_prices_endpoint_is_requested_with_arguments(
        self, arguments: dict
    ):
        return self.client.get(get_price_url(), arguments)

    def _then_should_filter_prices_by_game_id(self, result, object_id):
        expected_objects = PriceModel.objects.all()\
            .filter(game__id=object_id).order_by('price')
        serializer = PriceSerializer(expected_objects, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_retrieve_best_prices(self):
        """Test retrieving best game prices"""
        self._given_the_objects()
        result = self._when_best_prices_endpoint_is_requested_with_arguments(
            {'to': 20}
        )
        self._then_should_list_twenty_best_prices(result)

    def _then_should_list_twenty_best_prices(self, result):
        price_query = PriceModel.objects.all().order_by('price')
        expected_prices_id = get_lowest_prices_id(price_query)

        best_prices_query = PriceModel.objects.filter(
            id__in=expected_prices_id
        ).order_by('price')[:20]
        serializer = PriceDetailSerializer(best_prices_query, many=True)

        self.assertEqual(result.data, serializer.data)

    def test_filter_best_prices_by_game_name(self):
        """Test filtering by game name"""
        self._given_the_objects()

        parameters_payload = {
            'game_name': 'rain',
            'from': 4,
            'to': 10,
        }
        result = self._when_best_prices_endpoint_is_requested_with_arguments(
            parameters_payload
        )
        self._then_should_filter_best_prices_by_game_name(result)

    def _then_should_filter_best_prices_by_game_name(self, result):
        price_query = PriceModel.objects.all().order_by('price')
        expected_prices_id = get_lowest_prices_id(price_query)

        name_to_search = 'rain'

        best_prices_query = PriceModel.objects.filter(
            id__in=expected_prices_id
        ).order_by('price')
        best_prices_query = best_prices_query.filter(
            game__name__icontains=name_to_search
        )[3:10]
        serializer = PriceDetailSerializer(best_prices_query, many=True)

        self.assertEqual(result.data, serializer.data)

    def _when_best_prices_endpoint_is_requested_with_arguments(
        self, arguments: dict
    ):
        return self.client.get(BEST_PRICES_URL, arguments)

    def _given_the_objects(self):
        make_price_objects()
