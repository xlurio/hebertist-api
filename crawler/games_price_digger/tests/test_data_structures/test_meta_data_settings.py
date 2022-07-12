import unittest
from unittest.mock import MagicMock

from scrapy import Selector
from games_price_digger.src.components.meta_game import MetaGame
from games_price_digger.src.data_structures.digging_settings import MetaDataSettings


class MetaDataSettingsTests(unittest.TestCase):

    def test_get_item_box(self):
        """Item box getter"""
        arrangement = self._given_the_settings()
        result = self._when_the_item_box_is_got(arrangement)
        self._then_it_should_return_box(result)

    def _when_the_item_box_is_got(self, arrangement):
        return arrangement.get_item_box()

    def _then_it_should_return_box(self, result):
        self.assertTrue(isinstance(result, Selector))

    def test_get_title_xpath(self):
        """Test title xpath getter"""
        arrangement = self._given_the_settings()
        result = self._when_the_title_xpath_is_got(arrangement)
        self._then_it_should_return_title_xpath(result)

    def _when_the_title_xpath_is_got(self, arrangement):
        return arrangement.get_item_title_xpath()

    def _then_it_should_return_title_xpath(self, result):
        expected_result = './/descendant::h3/text()'
        self.assertEqual(result, expected_result)

    def test_score_xpath(self):
        """Test score xpath getter"""
        arrangement = self._given_the_settings()
        result = self._when_the_score_xpath_is_got(arrangement)
        self._then_it_should_return_score(result)

    def _when_the_score_xpath_is_got(self, arrangement):
        return arrangement.get_item_score_xpath()

    def _then_it_should_return_score(self, result):
        expected_result = './/descendant::span[@class="score"]/text()'
        self.assertEqual(result, expected_result)

    def test_image_xpath(self):
        """Test image xpath getter"""
        arrangement = self._given_the_settings()
        result = self._when_the_image_xpath_is_got(arrangement)
        self._then_it_should_return_image_xpath(result)

    def _given_the_settings(self):
        fake_item_box = MagicMock(spec=Selector)
        item_title_xpath = 'h3'
        item_score_xpath = 'span[@class="score"]'
        item_image_xpath = 'img'

        return MetaDataSettings(
            fake_item_box,
            item_title_xpath,
            item_score_xpath,
            item_image_xpath
        )

    def _when_the_image_xpath_is_got(self, arrangement):
        return arrangement.get_item_image_xpath()

    def _then_it_should_return_image_xpath(self, result):
        expected_result = './/descendant::img/@src'
        self.assertEqual(result, expected_result)

    def test_make_item(self):
        """Test MetaGame object factory method"""
        arrangement = self._given_the_arguments()
        result = self._when_the_item_is_made(arrangement)
        self._then_it_should_return_item(result)

    def _given_the_arguments(self):
        return (
            self._given_the_settings(),
            {
                'name': 'The Game',
                'score': 99,
                'image': 'https://static.thestore.com/media/the-game.jpg'
            },
        )

    def _when_the_item_is_made(self, arrangement):
        SETTINGS_OBJECT = 0
        FAKE_META_DATA = 1

        settings = arrangement[SETTINGS_OBJECT]
        meta_data = arrangement[FAKE_META_DATA]

        return settings.make_item(**meta_data)

    def _then_it_should_return_item(self, result):
        self.assertTrue(isinstance(result, MetaGame))


if __name__ == '__main__':
    unittest.main()
