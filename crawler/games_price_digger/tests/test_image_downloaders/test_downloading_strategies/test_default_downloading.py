import os
import unittest
import tempfile
from unittest.mock import Mock
from games_price_digger.src.image_downloaders.downloading_strategies \
    .default_downloading import DefaultDownloading


class DefaultDownloadingTests(unittest.TestCase):

    def test_download(self):
        """Test downloading method"""
        arrangement = self._given_the_strategy()
        result = self._when_image_is_downloaded(arrangement)
        self._then_it_should_save_image(result)

    def _given_the_strategy(self):
        destination_folder = tempfile.mkdtemp()
        strategy = self._make_strategy()

        return {
            'destination_folder': destination_folder,
            'strategy': strategy,
        }

    def _make_strategy(self):
        fake_response = self._make_fake_response()

        fake_response_factory = Mock()
        fake_response_factory.make_response.return_value = fake_response

        strategy = DefaultDownloading()
        strategy._response_factory = fake_response_factory

        return strategy

    def _make_fake_response(self):
        self.temporary_image = self._make_temporary_image()

        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.raw = self.temporary_image

        return fake_response

    def _make_temporary_image(self):
        return tempfile.TemporaryFile(suffix='.jpg')

    def _when_image_is_downloaded(self, arrangement):
        strategy = arrangement.get('strategy')

        fake_url = 'https://fakeurl.com/media/image.jpg'

        destination_folder = arrangement.get('destination_folder')
        destination = os.path.join(destination_folder, 'temporary-image.jpg')

        strategy.download(fake_url, destination)
        self.temporary_image.close()

        return os.listdir(destination_folder)

    def _then_it_should_save_image(self, result):
        expected_result = 'temporary-image.jpg'
        self.assertIn(expected_result, result)


if __name__ == '__main__':
    unittest.main()
