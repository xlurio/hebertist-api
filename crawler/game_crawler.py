import base_crawler
import django
import os
import sys

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../api'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings'
django.setup()

# noinspection PyUnresolvedReferences
from games_price_digger.spiders.games_metascore import GamesMetascoreSpider


class GameCrawler(base_crawler.Crawler):
    """Crawls the game and score"""
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    d = runner.crawl(GamesMetascoreSpider)


if __name__ == '__main__':
    crawler = GameCrawler()
    crawler.run_crawler()
