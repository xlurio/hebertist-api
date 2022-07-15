import asyncio
import logging

from game_crawler import GameCrawler
from price_crawler import PriceCrawler

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
MONTH = 30 * DAY


class DataUpdater:

    _routines = ()

    def __init__(self, routines: tuple = ()):
        self._routines = [routine for routine in self._make_routines(routines)]

    def _make_routines(self, routine_parameters):
        for parameter in routine_parameters:
            yield self._run_routine(*parameter)

    async def _run_routine(self, crawler, time):
        SUCCESS_MESSAGE = f'{crawler.data_name} updated!'

        crawler.run_crawler()
        logging.info(SUCCESS_MESSAGE)

        while True:
            await asyncio.sleep(time)
            crawler.run_crawler()
            logging.info(SUCCESS_MESSAGE)

    async def update(self):
        await asyncio.gather(*self._routines)


if __name__ == '__main__':
    routines = (
        (GameCrawler(), MONTH),
        (PriceCrawler(), 3 * DAY),
    )
    worker = DataUpdater(routines)
    asyncio.run(worker.update())
