from core.models import GameModel
from games_price_digger.items import GameItem
import os
import sys
import django
import pandas as pd
import scrapy

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../../../api'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings'
django.setup()


def get_game_names():
    """Function that return the list of all games in Metacritics"""
    game_table = GameModel.objects.all().values()
    games = pd.DataFrame(game_table)
    return list(games['name'])


class GamesMetascoreSpider(scrapy.Spider):
    """Spider that gets the names and scores of the PC games in Metacritics"""
    name = 'games_metascore'
    allowed_domains = ['www.metacritic.com']
    start_urls = [
        'https://www.metacritic.com/browse/games/release-date/available/pc/'
        'metascore'
    ]

    game_item_box = 'div[starts-with(@class, "browse_list_wrapper")]'
    game_item_row = 'tr[not(@class="spacer")]'
    game_item_score = 'div[starts-with(@class, "metascore_w")]'

    def parse(self, response, **kwargs):
        # Get game boxes
        game_boxes = response.xpath(
            f'//{self.game_item_box}/descendant::{self.game_item_row}'
        )

        # Get name and score of each game on the page
        if game_boxes:
            yield from self._iterate_games(game_boxes)

        # Go to the next page
        next_page_link = response.xpath('//a[@rel="next"]/@href').get()
        if next_page_link:
            yield response.follow(url=next_page_link, callback=self.parse)

    def _iterate_games(self, game_boxes):
        for game in game_boxes:
            game_name = game.xpath('.//descendant::h3/text()')
            game_name = str(game_name.get()).strip()

            game_score = game.xpath(
                f'.//descendant::{self.game_item_score}/text()'
            )
            game_score = str(game_score.get()).strip()

            yield {
                'game_item': self._get_game_item(game_name, game_score),
            }

    def _get_game_item(self, name, score):
        item = GameItem()
        item['name'] = name
        item['score'] = score
        return item
