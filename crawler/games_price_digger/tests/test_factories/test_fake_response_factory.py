import unittest
from scrapy.http import Response
from games_price_digger.src.factories.fake_response_factory import FakeResponseFactory


class FakeResponseFactoryTests(unittest.TestCase):

    def test_make_response(self):
        """Test the factory method"""
        result = self._when_response_is_made()
        self._then_it_should_have_the_right_interface(result)

    def _when_response_is_made(self):
        factory = FakeResponseFactory()
        return factory.make_response('generic.html')

    def _then_it_should_have_the_right_interface(self, product):
        self.assertTrue(isinstance(product, Response))


if __name__ == '__main__':
    unittest.main()
