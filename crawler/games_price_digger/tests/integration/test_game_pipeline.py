import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import uuid
import warnings
from scrapy import Spider

from games_price_digger.pipelines import GamePipeline
from games_price_digger.src.adapters.fake_manager import FakeManager
from games_price_digger.src.components.fake_model import FakeModel
from games_price_digger.src.components.meta_game import MetaGame


class GamePipelineTests(unittest.TestCase):
    temporary_directory = object

    def setUp(self) -> None:
        self.fake_spider = MagicMock(spec=Spider)
        self.temporary_directory = tempfile.mkdtemp()

    @patch(
        'games_price_digger.pipelines.GamePipeline._get_image_path'
    )
    def test_old_image_is_deleted_before_setting_a_new_one(self, mocked_path):
        """Test if the old image of a game is erased before new one is 
        downloaded"""
        arrangements = self._given_this_dataset()
        result = self._when_item_is_processed(arrangements, mocked_path)
        self._then_the_old_image_should_be_deleted(result)

    def _given_this_dataset(self):
        old_image_path = self._make_image()
        fake_object = FakeModel(
            name='Crash Bandicoot',
            score=76,
            image=old_image_path,
        )

        fake_data = [fake_object]
        fake_manager = FakeManager(FakeModel, fake_data)

        pipeline = GamePipeline()
        pipeline._model_manager = fake_manager
        return pipeline

    def _make_image(self):
        image_filename = uuid.uuid4()
        image_path = os.path.join(
            self.temporary_directory,
            f'{image_filename}.jpg'
        )

        with open(image_path, 'wb') as image:
            temporary_image = tempfile.TemporaryFile(suffix='.jpg')
            image.write(temporary_image.read())
            temporary_image.close()

        return image_path

    def _when_item_is_processed(self, arrangements, mocked_path):
        old_data = arrangements._model_manager._data[0]
        old_image_path = old_data.image
        old_image_filename = os.path.basename(old_image_path)

        new_image_path = self._make_image()
        mocked_path.return_value = new_image_path
        new_image_filename = os.path.basename(new_image_path)

        fake_game = MetaGame(
            name='Crash Bandicoot',
            score=76,
            image='https://static.store.com/image.jpg',
        )
        fake_item = {
            'game_metadata': fake_game
        }

        arrangements.process_item(fake_item, self.fake_spider)

        list_of_files = os.listdir(self.temporary_directory)

        return (
            list_of_files,
            old_image_filename,
            new_image_filename,
        )

    def _then_the_old_image_should_be_deleted(self, result):
        LIST_OF_FILES = 0
        OLD_IMAGE = 1
        NEW_IMAGE = 2

        self.assertNotIn(result[OLD_IMAGE], result[LIST_OF_FILES])
        self.assertIn(result[NEW_IMAGE], result[LIST_OF_FILES])


if __name__ == '__main__':
    unittest.main()
