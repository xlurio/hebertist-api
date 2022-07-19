import copy
import logging
import os
import time
from core import models
from django.core.exceptions import ObjectDoesNotExist
from games_price_digger.src.adapters.file_deleter import FileDeleter

from games_price_digger.src.image_downloaders.image_downloader import \
    ImageDownloader


class GamePipeline:
    _model_manager = models.GameModel.objects

    def process_item(self, item, _):
        try:
            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"
            object_to_process = item.get('game_metadata')
            object_to_process = copy.deepcopy(object_to_process)
            processed_item = self._get_or_create_object(object_to_process)

            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "false"
            return processed_item

        except AttributeError:
            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "false"
            return item

        except KeyError:
            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "false"
            return item

        finally:
            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "false"

    def _get_or_create_object(self, item) -> dict:
        try:
            return self._update_object(item)

        except ObjectDoesNotExist:
            return self._create_object(item)

    def _update_object(self, item) -> dict:
        game_name = item.get_name()
        game = self._model_manager.get(
            name=game_name
        )

        old_image = getattr(game, 'image').path
        self._delete_old_image(old_image)

        new_image = item.get_image()

        image_path = self._get_image_path(new_image)
        game_score = item.get_score()

        setattr(game, 'image', image_path)
        setattr(game, 'score', game_score)
        game.save()

        logging.info(f'{game_name} updated on database')

        time.sleep(3)

        return {
            'name': game_name,
            'score': game_score,
            'image': image_path,
        }

    def _delete_old_image(self, old_image):
        old_image_basename = os.path.basename(old_image)
        old_image_directory = self._get_image_destination_folder()
        old_image_path = os.path.join(old_image_directory, old_image_basename)
        FileDeleter().delete(old_image_path)

    def _create_object(self, item) -> dict:
        game_name = item.get_name()
        game_score = item.get_score()
        game_image = item.get_image()
        image_path = self._get_image_path(game_image)

        self._model_manager.create(
            name=game_name, score=game_score, image=image_path
        )
        logging.info(f'{game_name} registered on database')

        time.sleep(3)

        return {
            'name': game_name,
            'score': game_score,
            'image': image_path,
        }

    def _get_image_path(self, url):
        destination_folder = self._get_image_destination_folder()
        downloader = ImageDownloader(destination_folder)

        downloader.download(url)
        image_filename = downloader.get_filename()
        image_path = os.path.join('uploads/game', image_filename)
        return image_path

    def _get_image_destination_folder(self):
        current_module = os.path.dirname(__file__)
        module_path = os.path.abspath(current_module)
        root_folder = os.path.join(module_path, '../../')
        destination_folder = os.path.join(root_folder, './api/uploads/game')
        return os.path.abspath(destination_folder)


class PricePipeline:
    _game_manager = models.GameModel.objects
    _store_manager = models.StoreModel.objects
    _price_manager = models.PriceModel.objects

    def process_item(self, item, _):
        try:
            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "true"
            object_to_process = copy.deepcopy(item)
            processed_item = self._create_objects(object_to_process)
            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "false"

            return processed_item

        except AttributeError:
            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "false"
            return item

        except KeyError:
            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "false"
            return item

        finally:
            os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = "false"

    def _create_objects(self, item):
        game_data = item.get('game')
        search_data = item.get('search')

        self.game = self._game_manager.get_or_create(
            name=search_data.get_game()
        )[0]
        self.store = self._store_manager.get_or_create(
            name=search_data.get_store()
        )[0]
        self.price = game_data.get_price()
        self.link = game_data.get_link()

        self._get_or_create_objects()

        return {
            'game': str(game_data),
            'search': str(search_data),
        }

    def _get_or_create_objects(self):
        try:
            self._update_price_object()
        except ObjectDoesNotExist:
            self._create_price_object()

    def _update_price_object(self):
        price_object = self._price_manager.get(
            game=self.game,
            store=self.store,
        )
        setattr(price_object, 'price', self.price)
        setattr(price_object, 'link', self.link)
        price_object.save()
        logging.info('Price updated in the database!')

    def _create_price_object(self):
        self._price_manager.create(
            game=self.game,
            store=self.store,
            price=self.price,
            link=self.link,
        )
        logging.info('Price created in the database!')
