import unittest
from unittest.mock import MagicMock

from scrapy import Selector
from games_price_digger.src.data_structures import SearchPageSettings

mocked_item_box = MagicMock(spec=Selector)


class SearchPageSettingsTests(unittest.TestCase):
    _fake_title = 'h2'
    _fake_link = '@href'

    def test_item_box_getter(self):
        """Test item_box getter"""
        result = self._when_the_data_digger_is_setted()
        self._then_is_must_return_item_box_in(result)

    def _then_is_must_return_item_box_in(self, settings: SearchPageSettings):
        item_box = settings.get_item_box()
        expected_item_box = mocked_item_box
        self.assertEqual(item_box, expected_item_box)

    def test_item_title_xpath_getter(self):
        """Test item_title_xpath getter"""
        result = self._when_the_data_digger_is_setted()
        self._then_is_must_return_item_title_xpath_in(result)

    def _then_is_must_return_item_title_xpath_in(
        self, settings: SearchPageSettings
    ):
        item_title_xpath = settings.get_item_title_xpath()
        expected_item_title_xpath = f'.//descendant::{self._fake_title}/text()'
        self.assertEqual(item_title_xpath, expected_item_title_xpath)

    def test_item_link_xpath_getter(self):
        """Test item_link_xpath getter"""
        result = self._when_the_data_digger_is_setted()
        self._then_is_must_return_item_link_xpath_in(result)

    def _then_is_must_return_item_link_xpath_in(
        self, settings: SearchPageSettings
    ):
        item_link_xpath = settings.get_item_link_xpath()
        expected_item_link_xpath = f'.//{self._fake_link}'
        self.assertEqual(item_link_xpath, expected_item_link_xpath)

    def _when_the_data_digger_is_setted(self):
        return self._make_digger_settings()

    def _make_digger_settings(self):
        settings = SearchPageSettings(
            item_box=mocked_item_box,
            item_title_xpath=self._fake_title,
            item_link_xpath=self._fake_link,
        )
        return settings


if __name__ == '__main__':
    unittest.main()
