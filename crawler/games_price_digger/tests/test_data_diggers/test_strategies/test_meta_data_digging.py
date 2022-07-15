import unittest
from unittest.mock import MagicMock
from games_price_digger.src.data_diggers.strategies import MetaDataDigging
from games_price_digger.src.data_structures.digging_settings \
    .meta_data_settings import MetaDataSettings
from games_price_digger.src.factories.fake_response_factory import \
    FakeResponseFactory


class MetaDataDiggingTests(unittest.TestCase):

    def test_dig_data(self):
        """Test data digging method"""
        result = self._when_the_data_is_digged()
        self._then_it_shoud_return_data(result)

    def _when_the_data_is_digged(self):
        strategy = MetaDataDigging()
        settings = self._make_settings()
        return strategy.dig_data(settings)

    def _make_settings(self):
        fake_settings = MagicMock(spec=MetaDataSettings)
        fake_item_box = self._make_item_box()

        fake_settings.get_item_box.return_value = fake_item_box
        fake_settings.get_item_title_xpath.return_value = (
            './/descendant::h2/text()'
        )
        fake_settings.get_item_score_xpath.return_value = (
            './/descendant::span[@id="score"]/text()'
        )
        fake_settings.get_item_image_xpath.return_value = (
            './/descendant::img/@src'
        )

        return fake_settings

    def _make_item_box(self):
        factory = FakeResponseFactory()
        return factory.make_response('generic.html')

    def _then_it_shoud_return_data(self, result):
        expected_result = {
            'name': 'Generic Title',
            'score': 96,
            'image': 'https://static.store.com/media/generic.jpg',
        }

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
