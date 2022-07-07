from core.models import GameModel
import django
import pandas as pd
import scrapy
from games_price_digger.src.components.game import Game

from games_price_digger.src.components.meta_game import MetaGame

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

    game_box_xpath = (
        'div[starts-with(@class, "browse_list_wrapper")]'
        '/descendant::tr[not(@class="spacer")]'
    )
    game_score_xpath = 'div[starts-with(@class, "metascore_w")]'
    game_image_xpath = 'img'

    def parse(self, response, **kwargs):
        # Get game boxes
        game_boxes = response.xpath(self.game_box_xpath)

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

            game_score_element = game.xpath(
                f'.//descendant::{self.game_score_xpath}/text()'
            )
            scraped_game_score = game_score_element.get()
            scraped_game_score = str(scraped_game_score)
            stripped_game_score = scraped_game_score.strip()
            game_score = int(stripped_game_score)

            game_image_element = game.xpath(
                f'.//descendant::{self.game_image_xpath}/@src'
            )
            game_image_url = game_image_element.get()
            game_image_url = str(game_image_url)
            stripped_game_image_url = game_image_url.strip()

            game_data = MetaGame(
                name=game_name,
                score=game_score,
                image=stripped_game_image_url,
            )

            yield game_data
