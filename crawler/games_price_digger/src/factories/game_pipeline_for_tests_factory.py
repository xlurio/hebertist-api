import os
import tempfile
import uuid
from games_price_digger.pipelines import GamePipeline
from games_price_digger.src.adapters.fake_manager import FakeManager
from games_price_digger.src.components.fake_image_field_file import \
    FakeImageFieldFile
from games_price_digger.src.components.fake_game_model import FakeGameModel


def make_temporary_image(directory) -> str:
    image_filename = uuid.uuid4()
    image_path = os.path.join(
        directory,
        f'{image_filename}.jpg'
    )

    with open(image_path, 'wb') as image:
        temporary_image = tempfile.TemporaryFile(suffix='.jpg')
        image.write(temporary_image.read())
        temporary_image.close()

    return image_path


class GamePipelineForTestsFactory:

    def __init__(self, directory=None):
        if directory:
            self._directory = directory
        else:
            self._directory = tempfile.mkdtemp()

    def make_pipeline(self) -> GamePipeline:
        pipeline = GamePipeline()
        pipeline._model_manager = self._make_fake_manager()

        def _get_fake_image_destination_folder():
            return self._directory

        pipeline._get_image_destination_folder = \
            _get_fake_image_destination_folder

        return pipeline

    def _make_fake_manager(self) -> FakeManager:
        old_image_path = make_temporary_image(self._directory)
        fake_object = FakeGameModel(
            name='Crash Bandicoot',
            score=76,
            image=FakeImageFieldFile(old_image_path),
        )
        fake_data = [fake_object]

        return FakeManager(FakeGameModel, fake_data)
