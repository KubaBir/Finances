from django.urls import path

from .views import dashboard, fetch_transactions, main_page, overview

app_name = 'core'

urlpatterns = [
    path('', main_page, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('mock_fetch/', fetch_transactions, name='mock_fetch'),
    path('overview/<id>', overview, name='overview'),
]
