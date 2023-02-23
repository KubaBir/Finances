from django.urls import path

from .views import fetch_transactions, main_page

app_name = 'core'

urlpatterns = [
    path('', main_page, name='home'),
    path('fetch/', fetch_transactions, name='fetch'),
]
