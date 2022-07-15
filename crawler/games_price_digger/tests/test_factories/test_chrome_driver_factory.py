import unittest

from games_price_digger.src.factories.chrome_driver_factory import \
    ChromeDriveFactory
from selenium.webdriver.remote.webdriver import WebDriver


class ChromeDriverFactoryTests(unittest.TestCase):

    def test_factory_method(self):
        """Test factory method"""
        arrangement = self._given_the_factory()
        result = self._when_factored(arrangement)
        self._then_should_return_webdriver(result)

    def _given_the_factory(self):
        return ChromeDriveFactory()

    def _when_factored(self, arrangement):
        return arrangement.make_driver()

    def _then_should_return_webdriver(self, result):
        self.assertTrue(isinstance(result, WebDriver))


if __name__ == '__main__':
    unittest.main()
