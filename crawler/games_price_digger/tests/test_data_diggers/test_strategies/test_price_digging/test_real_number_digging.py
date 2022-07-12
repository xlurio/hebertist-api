import os
import unittest
from games_price_digger.src.data_diggers.strategies.price_digging_strategies import RealNumberDigging
from games_price_digger.src.utils.fake_response_builders import HTMLResponseBuilder
from games_price_digger.src.utils import TestHTMLGetter


class RealNumberDiggingTests(unittest.TestCase):
    fake_response_builder = HTMLResponseBuilder()
    test_html_getter = TestHTMLGetter()

    def setUp(self):
        html_file_path = self.test_html_getter.get_html_file_by_name(
            'generic.html'
        )
        self.fake_response_builder.set_html_file_path(html_file_path)
        response = self.fake_response_builder.build()

        item_box_xpath = '//div[@id = "item-price-box"]'
        self.item_box = response.xpath(item_box_xpath)

        price_xpath = 'p[@id = "real-number-price"]'
        self.real_number_digging = RealNumberDigging(price_xpath)

    def test_dig_data(self):
        """Test the dig_data() method"""
        expected_result = 2.99
        result = self.real_number_digging.dig_data(self.item_box)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
