import pandas as pd
import warnings
# noinspection PyUnresolvedReferences
from core import models

warnings.simplefilter('ignore')


def _get_to_compare_name(name):
    """Returns the game of the name clean and ready for comparison"""
    accepted_characters = 'abcdefghijklmnopqrstuvxwyz1234567890'
    name = name.lower()
    cleaned_name = ''
    for character in name:
        if character in accepted_characters:
            cleaned_name += character
    return cleaned_name


def _convert_to_integer(number):
    """Returns a cleaned integer"""
    # Removes nonnumerical characters
    figures = '1234567890,.'
    new_number = ''
    for character in str(number):
        if character in figures:
            new_number += character
    # Removes decimals
    for separator in ['.', ',']:
        if separator in new_number:
            new_number = new_number[:new_number.indexOf(separator)]
    # Parse to integer
    try:
        return int(new_number)
    except ValueError:
        return 0


def _clean_dataframe(dataframe, name_column):
    """Returns a dataframe cleaned"""
    dataframe = dataframe
    if len(dataframe) > 0:
        try:
            dataframe = dataframe[['id', name_column]]
            dataframe[name_column] = \
                dataframe[name_column].apply(
                    lambda name: _get_to_compare_name(name)
                )
            dataframe = dataframe.drop_duplicates(subset=name_column)
            return dataframe
        except KeyError:
            raise KeyError(f'Column available are: '
                           f'{list(dataframe.columns)}')
    else:
        return pd.DataFrame({
            'id': [0],
            name_column: ['no_value'],
        })


def _clean_game_dataframe(game_dataframe):
    """Returns the game dataframe cleaned"""
    return _clean_dataframe(game_dataframe, 'name')


def _get_data(model_class, cleaning_function):
    """Returns a cleaned dataframe with the specified models data"""
    queryset = model_class.objects.all().values()
    dataframe = pd.DataFrame(queryset)
    return cleaning_function(dataframe)


class GameCleaner:
    """Holds the methods to clean the game scraped data"""

    def __init__(self, game_item):
        self.game_item = game_item
        self.to_compare_game_name = \
            _get_to_compare_name(self.game_item['name'])
        self.game_dataframe = _get_data(
            model_class=models.GameModel,
            cleaning_function=_clean_game_dataframe,
        )

    def does_exists(self):
        """Return true if the game is already in the game query"""
        return self.to_compare_game_name in list(self.game_dataframe['name'])

    def get_game_id(self):
        """Returns the game id if it exists"""
        if self.does_exists():
            game_row = self.game_dataframe[
                self.game_dataframe.name == self.to_compare_game_name
                ].reset_index()
            return int(game_row.at[0, 'id'])
        return None

    def clean_score(self):
        """Returns the game score cleaned"""
        return _convert_to_integer(self.game_item['score'])


def _clean_price_dataframe(price_dataframe):
    """Returns the price dataframe cleaned"""
    price_dataframe = price_dataframe
    try:
        price_dataframe = price_dataframe[['id', 'game', 'store']]
        price_dataframe['game'] = \
            price_dataframe['game'].apply(
                lambda game_name: _get_to_compare_name(game_name)
            )
        price_dataframe['store'] = \
            price_dataframe['store'].apply(
                lambda store_name: _get_to_compare_name(store_name)
            )
        price_dataframe = price_dataframe.drop_duplicates()
        return price_dataframe
    except KeyError:
        raise KeyError(f'Column available are: '
                       f'{list(price_dataframe.columns)}')


def _clean_store_dataframe(store_dataframe):
    """Returns the store dataframe cleaned"""
    return _clean_dataframe(store_dataframe, 'name')


def _convert_to_float(to_convert):
    """Returns a validated float"""
    to_convert = str(to_convert)
    try:
        new_float = ''
        for character in to_convert:
            if character in '1234567890.':
                new_float += character
        return new_float
    except ValueError:
        return 0.0


class PriceCleaner:
    """Holds the methods to clean the game price scraped data"""

    def __init__(self, price_item):
        self.price_item = price_item
        self.to_compare_game_name = \
            _get_to_compare_name(self.price_item['game'])
        self.to_compare_store_name = \
            _get_to_compare_name(self.price_item['store'])

        # Get the game data
        self.game_dataframe = _get_data(
            model_class=models.GameModel,
            cleaning_function=_clean_game_dataframe,
        )
        # Get the store data
        self.store_dataframe = _get_data(
            model_class=models.StoreModel,
            cleaning_function=_clean_store_dataframe,
        )

    def does_game_exists(self):
        """Return true if the game is already in the game query"""
        return self.to_compare_game_name in list(self.game_dataframe['name'])

    def does_store_exists(self):
        """Return true if the game is already in the game query"""
        return self.to_compare_store_name in list(
            self.store_dataframe['name']
        )

    def get_game_id(self):
        """Returns the game id if it exists"""
        if self.does_game_exists():
            game_row = self.game_dataframe[
                self.game_dataframe.name == self.to_compare_game_name
                ].reset_index()
            return int(game_row.at[0, 'id'])
        return None

    def get_store_id(self):
        """Returns the game id if it exists"""
        if self.does_store_exists():
            store_row = self.store_dataframe[
                self.store_dataframe.name == self.to_compare_store_name
                ].reset_index()
            return int(store_row.at[0, 'id'])
        return None

    def clean_price(self):
        """Returns the cleaned price of the game"""
        return _convert_to_float(self.price_item['price'])
