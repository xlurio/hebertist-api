import os

from datetime import date, datetime
# noinspection PyUnresolvedReferences
from core.models import (
    GameModel, get_image_path, PriceModel, PriceHistoricModel,
    save_price_historic, StoreModel, WishlistModel
)
from django.contrib.auth import get_user_model
from unittest.mock import patch
from django.test import TestCase


def create_sample_user(**kwargs):
    """Creates a sample user objects"""
    payload = {
        'email': 'sample@email.com',
        'password': 'samplepass123',
        'date_of_birth': datetime(1996, 8, 20),
    }
    payload.update(kwargs)
    return get_user_model().objects.create_user(
        **payload
    )


def create_sample_game(**kwargs):
    """Creates a sample game object"""
    payload = {
        'name': 'Sample game',
        'score': 83
    }
    payload.update(kwargs)
    return GameModel.objects.create(**payload)


def create_sample_store(**kwargs):
    """Creates a sample store object"""
    payload = {
        'name': 'Sample store',
        'link': 'https://store.sample.com/'
    }
    payload.update(kwargs)
    return StoreModel.objects.create(**payload)


def create_sample_price(game, store, price=36.99):
    """Creates a sample price object"""
    payload = {
        'game': game,
        'store': store,
        'price': price,
    }
    return PriceModel.objects.create(**payload)


def _create_objects_for_price_historic_test(game1, game2, store1,
                                            store2, store3):
    """Creates and returns the objects for the price historic test"""
    price1 = create_sample_price(
        game=game1,
        store=store1,
        price=5.99
    )
    price2 = create_sample_price(
        game=game2,
        store=store2,
        price=6.99
    )
    create_sample_price(
        game=game1,
        store=store2,
        price=10.99
    )
    create_sample_price(
        game=game2,
        store=store3,
        price=10.99
    )
    return price1, price2


def _get_historic_price_data_for_test(time_of_the_historic, game1, game2):
    save_price_historic(time_of_the_historic)
    historic_saved = PriceHistoricModel.objects.all().filter(
        time_saved=time_of_the_historic
    )
    game1_historic = PriceHistoricModel.objects.all().filter(
        game=game1,
        time_saved=time_of_the_historic
    ).values()
    game2_historic = PriceHistoricModel.objects.all().filter(
        game=game2,
        time_saved=time_of_the_historic
    ).values()
    return historic_saved, game1_historic, game2_historic


class ModelsTests(TestCase):
    """Models tests"""
    test_email = 'sample@email.com'
    test_password = 'samplepass123'
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

    def test_create_game(self):
        """Test creating a game object"""
        game = GameModel.objects.create(
            name='Life is Strange',
            score=83
        )
        self.assertEqual(game.name, 'Life is Strange')
        self.assertEqual(game.score, 83)

    def test_create_store(self):
        """Test creating game store"""
        store_name = 'Steam'
        store_link = 'https://store.steampowered.com/'
        store = StoreModel.objects.create(
            name=store_name,
            link=store_link,
        )
        self.assertEqual(store.name, store_name)

    def test_create_price(self):
        """Test creating game store"""
        game_name = 'Life is Strange'
        store_name = 'Steam'
        store_link = 'https://store.steampowered.com/'
        price_value = 36.99
        game = GameModel.objects.create(
            name=game_name,
            score=83
        )
        store = StoreModel.objects.create(
            name=store_name,
            link=store_link,
        )
        game_price = PriceModel.objects.create(
            game=game,
            store=store,
            price=price_value,
        )
        self.assertEqual(game_price.game.name, game_name)
        self.assertEqual(game_price.store.name, store_name)
        self.assertEqual(game_price.price, price_value)

    @patch('uuid.uuid4')
    def test_image_path(self, mock_uuid):
        """Test if the image is being correctly stored"""
        uuid = 'test_uuid'
        mock_uuid.return_value = uuid
        expected_result = os.path.join('uploads/game', f'{uuid}.jpg')
        output_result = get_image_path(None, 'someImage.jpg')
        self.assertEqual(expected_result, output_result)

    def test_save_price_historic(self):
        """Test creating a registry of the current price of game"""
        # Create the objects for the test
        game1 = create_sample_game(name="Assassin's Creed: Valhala")
        game2 = create_sample_game(name="Battlefield 4")
        store1 = create_sample_store(
            name='Ubisoft',
            link='https://store.ubi.com/',
        )
        store2 = create_sample_store(
            name='Steam',
            link='https://store.steampowered.com/'
        )
        store3 = create_sample_store(
            name='Origin',
            link='https://www.origin.com/',
        )
        price1, price2 = _create_objects_for_price_historic_test(
            game1=game1,
            game2=game2,
            store1=store1,
            store2=store2,
            store3=store3,
        )
        time_of_the_historic = date.today()

        # Save historic
        historic_saved, game1_historic, game2_historic = \
            _get_historic_price_data_for_test(
                time_of_the_historic=time_of_the_historic,
                game1=game1,
                game2=game2
            )

        # Assertions
        self.assertEqual(len(historic_saved), 2)
        self.assertEqual(len(game1_historic), 1)
        self.assertEqual(float(game1_historic[0]['price']), price1.price)
        self.assertEqual(len(game2_historic), 1)
        self.assertEqual(float(game2_historic[0]['price']), price2.price)

    def test_save_to_wishlist(self):
        """Test adding a game to the wishlist of a user"""
        user = create_sample_user()
        game = create_sample_game()
        wish = WishlistModel.objects.create(
            user=user,
            game=game
        )
        self.assertEqual(wish.user, user)
        self.assertEqual(wish.game, game)
