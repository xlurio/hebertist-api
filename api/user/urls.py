from django.urls import path
# noinspection PyUnresolvedReferences
from user.views import CreateTokenView, ManageUserView

app_name = 'users'

urlpatterns = [
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManageUserView.as_view(), name='me'),
]
