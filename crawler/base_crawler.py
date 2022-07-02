from twisted.internet import reactor


class Crawler:
    """Base crawler class"""
    def run_crawler(self):
        self.d.addBoth(lambda _: reactor.stop())
        reactor.run()
