from rest_framework.routers import DefaultRouter
from django.urls import include, path
# noinspection PyUnresolvedReferences
from user.views import (
    CreateTokenView, CreateUserView, ManageUserView, WishlistViewSet
)

router = DefaultRouter()
router.register('wishlist', WishlistViewSet, 'wishlist')

app_name = 'users'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('', include(router.urls))
]
