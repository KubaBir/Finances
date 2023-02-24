from django.urls import path

from .views import fetch_transactions, main_page

app_name = 'core'

urlpatterns = [
    path('', main_page, name='home'),
]
