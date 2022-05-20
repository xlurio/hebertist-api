from rest_framework.test import APIClient
# noinspection PyUnresolvedReferences
from core.models import StoreModel
# noinspection PyUnresolvedReferences
from game.serializers import StoreSerializer
from django.urls import reverse
from rest_framework import status
from django.test import TestCase

STORE_URL = reverse('game:store-list')


class PublicStoreAPITests(TestCase):
    """Test the public features of the store API tests"""

    def setUp(self):
        self.client = APIClient()

    def test_list_stores(self):
        """Test retrieve all game objects"""
        StoreModel.objects.create(
            name='Steam',
            link='https://store.steampowered.com/',
        )
        StoreModel.objects.create(
            name='Origin',
            link='https://www.origin.com/',
        )

        stores = StoreModel.objects.all().order_by('name')
        serializer = StoreSerializer(stores, many=True)

        res = self.client.get(STORE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
