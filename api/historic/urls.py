from rest_framework.routers import DefaultRouter
from django.urls import include, path
# noinspection PyUnresolvedReferences
from historic.views import PriceHistoricViewSet

router = DefaultRouter()
router.register('prices', PriceHistoricViewSet, 'price')

app_name = 'historic'

urlpatterns = [
    path('', include(router.urls))
]
