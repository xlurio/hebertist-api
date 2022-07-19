import unittest
from unittest.mock import MagicMock

from scrapy import Spider
from games_price_digger.src.factories.price_pipeline_for_tests_factory \
    import PricePipelineForTestsFactory
from games_price_digger.src.components.found_game import FoundGame
from games_price_digger.src.components.search import Search
from games_price_digger.src.factories \
    .game_pipeline_for_tests_factory import GamePipelineForTestsFactory


class PricePipelineTests(unittest.TestCase):

    def setUp(self) -> None:
        self.spider = MagicMock(spec=Spider)

    def test_processing_after_game_pipeline(self):
        """Test processing item that was already processed by game pipeline"""
        arrangements = self._given_the_item_processed_by_game_pipeline()
        result = self._when_price_pipeline_processes_item(arrangements)
        self._then_should_return_game_data(result)

    def _given_the_item_processed_by_game_pipeline(self):
        fake_item = self._make_fake_item()

        game_pipeline = GamePipelineForTestsFactory().make_pipeline()
        processed_item = game_pipeline.process_item(fake_item, self.spider)

        return processed_item

    def _make_fake_item(self):
        fake_game = FoundGame(
            name='Batman Arkham City',
            price=20.98,
            link='https://random.store.com/crash-bandicoot'
        )
        fake_search = Search(
            game='Batman Arkham City',
            store='Random'
        )
        return {
            'game': fake_game,
            'search': fake_search,
        }

    def _when_price_pipeline_processes_item(self, item):
        price_pipeline = PricePipelineForTestsFactory().make_pipeline()
        return price_pipeline.process_item(item, self.spider)

    def _then_should_return_game_data(self, result):
        fake_game = FoundGame(
            name='Batman Arkham City',
            price=20.98,
            link='https://random.store.com/crash-bandicoot'
        )
        fake_search = Search(
            game='Batman Arkham City',
            store='Random'
        )

        expected_result = {
            'game': str(fake_game),
            'search': str(fake_search),
        }

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
