import unittest
from games_price_digger.spiders.games_metascore import GamesMetascoreSpider


class GamesMetascoreSpiderTests(unittest.TestCase):

    def setUp(self) -> None:
        self.spider = GamesMetascoreSpider()

    def test_parsing(self):
        """Test parse() method"""
        result = self._when_data_is_parsed()
        self._then_data_must_be_in(result)

    def _when_data_is_parsed(self):
        return self.spider.parse()

    def _then_data_must_be_in(self, game_data):
        game = game_data.get_name()
        expected_game = 'Crash Bandicoot'

        score = game_data.get_score()
        expected_score = 76

        image = game_data.get_image()
        expected_image = self._make_image_url()

        self.assertEqual(game, expected_game)
        self.assertEqual(score, expected_score)
        self.assertEqual(image, expected_image)

    def _make_image_url(self):
        security_protocol = 'https://'
        domain = 'static.metacritic.com'
        path = '/images/products/games/7/'
        filename = '73cdd5a87df216d29904e808efe3319a-98.jpg'

        return (security_protocol + domain + path + filename)


if __name__ == '__main__':
    unittest.main()
