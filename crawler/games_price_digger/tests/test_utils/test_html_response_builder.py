import unittest

from numpy import isin
from games_price_digger.src.utils.fake_response_builders import HTMLResponseBuilder
from games_price_digger.src.utils.test_html_getter import TestHTMLGetter
from scrapy.http import Response


class HTMLResponseBuilderTests(unittest.TestCase):

    def test_build(self):
        """Test building method"""
        getter = TestHTMLGetter()
        html_path = getter.get_html_file_by_name('generic.html')
        builder = HTMLResponseBuilder().set_html_file_path(html_path)
        result = builder.build()
        self.assertTrue(isinstance(result, Response))


if __name__ == '__main__':
    unittest.main()
