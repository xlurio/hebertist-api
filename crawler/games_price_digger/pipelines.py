# noinspection PyUnresolvedReferences
from locale import LC_NUMERIC
from games_price_digger import cleaners
# noinspection PyUnresolvedReferences
from core import models
from django.core.exceptions import ObjectDoesNotExist


def _get_params_for_price_object(item, model_class, does_exists, object_id,
                                 field_name):
    """Returns a object to create a price objects"""
    if not does_exists:
        return model_class.objects.create(
            name=item[field_name]
        )
    return model_class.objects.get(
        id=object_id
    )


class GamePipeline:
    """Pipeline that cleans the game information from Metacritic and saves
    in the games query"""

    def process_item(self, item, spider):
        if 'game_item' in item.keys():
            cleaner = cleaners.GameCleaner(item['game_item'])
            if cleaner.does_exists():
                game = models.GameModel.objects.get(
                    id=cleaner.get_game_id()
                )
                setattr(game, 'score', cleaner.clean_score())
                game.save()
                return item

            models.GameModel.objects.create(
                name=item['game_item']['name'],
                score=cleaner.clean_score(),
            )
        return item


class PricePipeline:

    def process_item(self, item, spider):
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
