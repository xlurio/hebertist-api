from rest_framework.routers import DefaultRouter
# noinspection PyUnresolvedReferences
from game.views import GameViewSet, PriceViewSet, StoreViewSet
from django.urls import include, path

router = DefaultRouter()
router.register('games', GameViewSet, basename='game')
router.register('prices', PriceViewSet, basename='price')
router.register('stores', StoreViewSet, basename='store')

app_name = 'game'

urlpatterns = [
    path('', include(router.urls)),
]
