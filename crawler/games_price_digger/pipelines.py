# noinspection PyUnresolvedReferences
from locale import LC_NUMERIC
from games_price_digger import cleaners
# noinspection PyUnresolvedReferences
from core import models
from decimal import Decimal


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
            game_data = item.get('game')
            search_data = item.get('search')

            game = models.GameModel.objects.get_or_create(
                name=search_data.get_game()
            )[0]
            store = models.StoreModel.objects.get_or_create(
                name=search_data.get_store()
            )[0]
            price = game_data.get_price()
            link = game_data.get_link()

            self._create_price_object(
                game, store, price, link
            )

            return {
                'game': str(game_data),
                'search': str(search_data),
            }

        except KeyError:
            return item

    def _create_price_object(self, game, store, price, link):
        try:
            price_object = models.PriceModel.objects.get(
                game=game,
                store=store,
            )
            setattr(price_object, 'price', price)
            setattr(price_object, 'link', link)
            price_object.save()
        except Exception:
            models.PriceModel.objects.create(
                game=game,
                store=store,
                price=price,
                link=link,
            )


""" class PricePipeline:

    def process_item(self, item, spider):
        if 'price_item' in item.keys():
            cleaner = cleaners.PriceCleaner(item['price_item'])
            game = _get_params_for_price_object(
                item=item['price_item'],
                model_class=models.GameModel,
                does_exists=cleaner.does_game_exists(),
                object_id=cleaner.get_game_id(),
                field_name='game',
            )
            store = _get_params_for_price_object(
                item=item['price_item'],
                model_class=models.StoreModel,
                does_exists=cleaner.does_store_exists(),
                object_id=cleaner.get_store_id(),
                field_name='store',
            )
            try:
                price = models.PriceModel.objects.get(
                    game=game,
                    store=store,
                )
                setattr(price, 'price', cleaner.clean_price())
            except models.PriceModel.DoesNotExist:
                models.PriceModel.objects.create(
                    game=game,
                    store=store,
                    price=cleaner.clean_price(),
                )
        return item """
