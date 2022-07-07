from core import models
from django.core.exceptions import ObjectDoesNotExist


class GamePipeline:

    def process_item(self, item, _):
        try:
            return self._create_object(item)
        except AttributeError:
            return item

    def _create_object(self, item):
        game_name = item.get_name()
        game_score = item.get_score()
        game_image = item.get_image()
        models.GameModel.objects.create(
            name=game_name, score=game_score, image=game_image
        )
        return item


class PricePipeline:

    def process_item(self, item, _):
        try:
            return self._get_or_create_objects(item)
        except KeyError:
            return item
        except AttributeError:
            return item

    def _get_or_create_objects(self, item):
        game_data = item.get('game')
        search_data = item.get('search')

        self.game = models.GameModel.objects.get_or_create(
            name=search_data.get_game()
        )[0]
        self.store = models.StoreModel.objects.get_or_create(
            name=search_data.get_store()
        )[0]
        self.price = game_data.get_price()
        self.link = game_data.get_link()

        self._create_price_object()

        return {
            'game': str(game_data),
            'search': str(search_data),
        }

    def _create_price_object(self):
        try:
            self._update_price_object()
        except ObjectDoesNotExist:
            self._create_price_object()

    def _update_price_object(self):
        price_object = models.PriceModel.objects.get(
            game=self.game,
            store=self.store,
        )
        setattr(price_object, 'price', self.price)
        setattr(price_object, 'link', self.link)
        price_object.save()

    def _create_price_object(self):
        models.PriceModel.objects.create(
            game=self.game,
            store=self.store,
            price=self.price,
            link=self.link,
        )
