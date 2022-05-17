from rest_framework.routers import DefaultRouter
# noinspection PyUnresolvedReferences
from game.views import GameViewSet
from django.urls import include, path

router = DefaultRouter()
router.register('games', GameViewSet, basename='game')

app_name = 'game'

urlpatterns = [
    path('', include(router.urls)),
]
