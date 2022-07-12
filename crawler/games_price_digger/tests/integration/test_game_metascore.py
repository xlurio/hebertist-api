import unittest
from games_price_digger.spiders.games_metascore import GamesMetascoreSpider
from games_price_digger.src.factories.fake_response_factory import FakeResponseFactory


class GamesMetascoreSpiderTests(unittest.TestCase):

    def setUp(self) -> None:
        response_factory = FakeResponseFactory()
        self.fake_response = response_factory.make_response(
            'metacritic_test.html'
        )
        self.spider = GamesMetascoreSpider()

    def test_parsing(self):
        """Test parse() method"""
        results = [result.get('game_metadata')
                   for result in self._when_data_is_parsed()]
        self._then_data_must_be_in(results)

    def _when_data_is_parsed(self):
        return self.spider.parse(self.fake_response, testing=True)

    def _then_data_must_be_in(self, game_data):
        expected_amount = 100

        games = [game.get_name() for game in game_data]
        expected_game = 'Batman: Arkham City'

        scores = [game.get_score() for game in game_data]
        expected_score = 91

        images = [game.get_image() for game in game_data]
        expected_image = self._make_image_url()

        self.assertEqual(expected_amount, len(game_data))
        self.assertIn(expected_game, games)
        self.assertIn(expected_score, scores)
        self.assertIn(expected_image, images)

    def _make_image_url(self):
        security_protocol = 'https://'
        domain = 'static.metacritic.com'
        path = '/images/products/games/7/'
        filename = '8ca786aa6ce79e3b0c30cdda2f3cb821-98.jpg'

        return (security_protocol + domain + path + filename)


if __name__ == '__main__':
    unittest.main()
