from django.urls import path

from .views import fetch_data

app_name = 'nordigen'

urlpatterns = [
    path('fetch/', fetch_data, name='fetch'),
]
