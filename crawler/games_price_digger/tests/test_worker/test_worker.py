import asyncio
import unittest
from games_price_digger.src.adapters.fake_crawler import FakeCrawler, WasRunned
from worker import DataUpdater


class DataUpdaterTests(unittest.TestCase):

    def test_crawler_execution(self):
        """Test if crawler are executed by the DataUpdater"""
        arrangements = self._given_the_updater()
        def result(): self._when_it_updates_with_the(arrangements)
        self._then_the_crawler_should_be_executed(result)

    def _given_the_updater(self):
        routines = (
            (FakeCrawler(), 1),
        )
        return DataUpdater(routines)

    def _when_it_updates_with_the(self, updater):
        asyncio.run(updater.update())

    def _then_the_crawler_should_be_executed(self, result):
        with self.assertRaises(WasRunned):
            result()


if __name__ == '__main__':
    unittest.main()
