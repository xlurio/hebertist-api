import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from scrapy import Spider
from games_price_digger.src.factories.game_pipeline_for_tests_factory \
    import GamePipelineForTestsFactory, make_temporary_image
from games_price_digger.src.factories.price_pipeline_for_tests_factory \
    import PricePipelineForTestsFactory
from games_price_digger.src.components.meta_game import MetaGame


class GamePipelineTests(unittest.TestCase):
    temporary_directory = object

    def setUp(self) -> None:
        self.fake_spider = MagicMock(spec=Spider)
        self.temporary_directory = tempfile.mkdtemp()
        self.factory = GamePipelineForTestsFactory(self.temporary_directory)

    @patch(
        'games_price_digger.pipelines.GamePipeline._get_image_path'
    )
    def test_old_image_is_deleted_before_setting_a_new_one(self, mocked_path):
        """Test if the old image of a game is erased before new one is
        downloaded"""
        arrangements = self._given_the_pipeline()
        result = self._when_item_with_old_image_is_processed(
            arrangements, mocked_path)
        self._then_the_old_image_should_be_deleted(result)

    def _given_the_pipeline(self):
        pipeline = self.factory.make_pipeline()

        return pipeline

    def _when_item_with_old_image_is_processed(self, arrangements,
                                               mocked_path):
        old_data = arrangements._model_manager._data[0]
        old_image_path = old_data.image.path
        old_image_filename = os.path.basename(old_image_path)

        new_image_path = make_temporary_image(self.temporary_directory)
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

    @patch(
        'games_price_digger.pipelines.GamePipeline._get_image_path'
    )
    def test_processing_after_price_pipeline(self, mocked_path):
        """Test if it can process the item after the price pipeline"""
        arrangements = self._given_the_item_processed_by_price_pipeline()
        result = self._when_processed_item_is_reprocessed(
            arrangements, mocked_path
        )
        self._then_should_return_game_data(result)

    def _given_the_item_processed_by_price_pipeline(self):
        fake_game = MetaGame(
            name='Crash Bandicoot',
            score=76,
            image='https://static.store.com/image.jpg',
        )
        fake_item = {
            'game_metadata': fake_game
        }

        price_pipeline_factory = PricePipelineForTestsFactory()
        price_pipeline = price_pipeline_factory.make_pipeline()
        processed_item = price_pipeline.process_item(
            fake_item, self.fake_spider
        )

        game_pipeline_factory = GamePipelineForTestsFactory(
            self.temporary_directory
        )
        game_pipeline = game_pipeline_factory.make_pipeline()

        return (game_pipeline, processed_item)

    def _when_processed_item_is_reprocessed(self, arrangements, mocked_path):
        PIPELINE = 0
        ITEM = 1

        pipeline = arrangements[PIPELINE]
        item = arrangements[ITEM]

        new_image_path = make_temporary_image(self.temporary_directory)
        mocked_path.return_value = new_image_path

        result = pipeline.process_item(item, self.fake_spider)
        result.pop('image')

        return result

    def _then_should_return_game_data(self, result):
        expected_result = {
            'name': 'Crash Bandicoot',
            'score': 76,
        }

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
