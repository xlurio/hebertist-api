import unittest
from unittest.mock import MagicMock

from scrapy import Selector
from games_price_digger.src.builders import MetaDataSettingsBuilder
from games_price_digger.src.data_structures.digging_settings \
    .meta_data_settings import MetaDataSettings

fake_item_box = MagicMock(spec=Selector)


class MetaDataSettingsBuilderTests(unittest.TestCase):

    def test_build(self):
        """Test building product"""
        result = self._when_product_is_built()
        self._then_product_must_have_right_interface(result)

    def _when_product_is_built(self):
        builder = MetaDataSettingsBuilder()
        builder.set_item_box(fake_item_box)
        builder.set_item_title_xpath('h3')
        builder.set_item_image_xpath('image')
        builder.set_item_score_xpath('span[@class="score"]')
        return builder.build()

    def _then_product_must_have_right_interface(self, product):
        self.assertTrue(isinstance(product, MetaDataSettings))


if __name__ == '__main__':
    unittest.main()
