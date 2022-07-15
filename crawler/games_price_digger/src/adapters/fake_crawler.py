class WasRunned(Exception):
    pass


class FakeCrawler:
    data_name = 'Fake data'

    def run_crawler(self):
        raise WasRunned()
