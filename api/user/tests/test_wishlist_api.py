from rest_framework.test import APIClient
from datetime import date
# noinspection PyUnresolvedReferences
from core.models import GameModel, WishlistModel
# noinspection PyUnresolvedReferences
from user.serializers import WishlistSerializer, WishlistDetailSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from django.test import TestCase


def get_wishlist_url(wish_id=None):
    """Returns the wishlist API url"""
    if wish_id:
        return reverse('users:wishlist-detail', args=[wish_id])
    else:
        return reverse('users:wishlist-list')


def create_wishlist(user, game_name='Sample Game'):
    """Creates and returns a wishlist objects"""
    game = GameModel.objects.get_or_create(
        name=game_name,
    )[0]
    wish = WishlistModel.objects.create(
        user=user,
        game=game,
    )
    return game, wish


class PublicWishlistAPI(TestCase):
    """Test the public features of the wishlist API"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test unauthorized access to the API"""
        res = self.client.get(get_wishlist_url())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWishlistAPI(TestCase):
    """Test the private features of the wishlist API"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='sample@user.com',
            password='samplepassword123',
            date_of_birth=date(year=2007, month=6, day=3)
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_list_wishlist(self):
        """Test retrieving all wishlist objects"""
        create_wishlist(
            user=self.user,
            game_name='Cities: Skylines',
        )
        create_wishlist(
            user=self.user,
            game_name='State of Decay 2',
        )
        wishlist = WishlistModel.objects.all().order_by('game__name')
        res = self.client.get(get_wishlist_url())
        serializer = WishlistSerializer(wishlist, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_details(self):
        """Test retrieving the details of the wishlist object"""
        game, wish = create_wishlist(
            user=self.user
        )
        serializer = WishlistDetailSerializer(wish)
        res = self.client.get(get_wishlist_url(wish.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
