import unittest
from games_price_digger.src.components.meta_game import MetaGame


class MetaGameTests(unittest.TestCase):
    fake_game = 'Crash Bandicoot'
    fake_score = 76

    def setUp(self) -> None:
        self.fake_image = self._make_image_url()

    def _make_image_url(self):
        security_protocol = 'https://'
        domain = 'static.metacritic.com'
        path = '/images/products/games/7/'
        filename = '73cdd5a87df216d29904e808efe3319a-98.jpg'

        return (security_protocol + domain + path + filename)

    def _make_game(self):
        return MetaGame(
            name=self.fake_game,
            score=self.fake_score,
            image=self.fake_image
        )

    def test_get_name(self):
        """Test name getter"""
        result = self._when_name_is_got()
        self._then_should_return_name(result)

    def _when_name_is_got(self):
        game = self._make_game()
        return game.get_name()

    def _then_should_return_name(self, name):
        expected_name = self.fake_game
        self.assertEqual(name, expected_name)

    def test_get_score(self):
        """Test score getter"""
        result = self._when_score_is_got()
        self._then_should_return_score(result)

    def _when_score_is_got(self):
        game = self._make_game()
        return game.get_score()

    def _then_should_return_score(self, score):
        expected_score = self.fake_score
        self.assertEqual(score, expected_score)

    def test_get_image(self):
        """Test image getter"""
        result = self._when_image_is_got()
        self._then_should_return_image(result)

    def _when_image_is_got(self):
        game = self._make_game()
        return game.get_image()

    def _then_should_return_image(self, image):
        expected_image = self.fake_image
        self.assertEqual(image, expected_image)


if __name__ == '__main__':
    unittest.main()
