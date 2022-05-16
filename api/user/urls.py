from django.urls import path
from user.views import CreateTokenViewSet

app_name = 'users'

urlpatterns = [
    path('token/', CreateTokenViewSet.as_view(), name='token')
]