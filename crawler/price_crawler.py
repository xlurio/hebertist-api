import base_crawler
import django
import os
import sys
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(BASE_DIR, '../api'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings'
django.setup()

# noinspection PyUnresolvedReferences
from games_price_digger import spiders


class PriceCrawler(base_crawler.Crawler):
    """Crawls the game prices"""
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(spiders.epic_price.EpicPriceParser)
    runner.crawl(spiders.gog_price.GogPriceParser)
    runner.crawl(spiders.greenman_price.GreenManPriceSpider)
    runner.crawl(spiders.microsoft_price.MicrosoftPriceSpider)
    runner.crawl(spiders.nuuvem_price.NuuvemPriceParser)
    runner.crawl(spiders.origin_price.OriginPriceSpider)
    runner.crawl(spiders.rockstar_price.RockstarPriceSpider)
    runner.crawl(spiders.ubisoft_price.UbisoftPriceSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())


if __name__ == '__main__':
    crawler = PriceCrawler()
    crawler.run_crawler()
