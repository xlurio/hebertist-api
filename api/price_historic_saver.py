import logging
import os
import time

import django
import pandas as pd

os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings'

try:
    django.setup()
    from core.models import GameModel, PriceHistoricModel, PriceModel
finally:
    pass

SECOND = 1
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR


def _save_price_historic_to_model(data_to_insert, time_saved=None):
    """Saves inserts data directly in a SQL data table"""
    if time_saved:
        for _, row in data_to_insert.iterrows():
            PriceHistoricModel.objects.create(
                game=GameModel.objects.get(id=int(row['game_id'])),
                price=float(row['price']),
                time_saved=time_saved,
            )

    for _, row in data_to_insert.iterrows():
        PriceHistoricModel.objects.create(
            game=GameModel.objects.get(id=int(row['game_id'])),
            price=float(row['price']),
        )


def save_price_historic(time_saved=None):
    """Saves the current lowest price of each game"""
    prices_data = pd.DataFrame(PriceModel.objects.all().values())
    prices_data = prices_data.groupby(by='game_id').min().reset_index()
    prices_data = prices_data[['game_id', 'price']]
    _save_price_historic_to_model(prices_data, time_saved)
    return PriceHistoricModel.objects.all()


class PriceHistoricSaver:

    def save_historic(self):
        SUCCESS_MESSAGE = 'Price historic saved'
        logging.info('Price historic saver started')

        while True:
            time.sleep(DAY)
            save_price_historic()
            logging.info(SUCCESS_MESSAGE)


if __name__ == '__main__':
    PriceHistoricSaver().save_historic()
