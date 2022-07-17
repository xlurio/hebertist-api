from games_price_digger.pipelines import PricePipeline
from games_price_digger.src.adapters.fake_manager import FakeManager
from games_price_digger.src.components.fake_game_model import FakeGameModel
from games_price_digger.src.components.fake_model import FakeModel
from games_price_digger.src.components.fake_price_model import FakePriceModel
from games_price_digger.src.components.fake_store_model import FakeStoreModel

GAME_MANAGER = 0
STORE_MANAGER = 1
PRICE_MANAGER = 2


class PricePipelineForTestsFactory:

    def make_pipeline(self):
        pipeline = PricePipeline()
        managers = self._make_fake_manager()
        pipeline._game_manager = managers[GAME_MANAGER]
        pipeline._store_manager = managers[STORE_MANAGER]
        pipeline._price_manager = managers[PRICE_MANAGER]

        return pipeline

    def _make_fake_manager(self):
        game_model = FakeGameModel(name='Crash Bandicoot')
        store_model = FakeStoreModel(name='Steam')
        price_model = FakePriceModel(
            game=game_model,
            store=store_model,
            price=36.99,
            link='https://some.store.com/game-page/',
        )

        game_manager = self._make_manager(game_model)
        store_manager = self._make_manager(store_model)
        price_manager = self._make_manager(price_model)

        return (game_manager, store_manager, price_manager)

    def _make_manager(self, model_object: FakeModel) -> FakeModel:
        data = [model_object]
        manager = FakeManager(model_object, data)

        return manager
