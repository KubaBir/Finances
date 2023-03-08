from django.urls import path

from .views import (change_category, dashboard, fetch_transactions,
                    ignore_transaciton, main_page, overview)

app_name = 'core'

urlpatterns = [
    path('', main_page, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('mock_fetch/', fetch_transactions, name='mock_fetch'),
    path('overview/<id>', overview, name='overview'),
    path('change_category/<id>', change_category, name='change_category'),
    path('ignore_transaction/<id>', ignore_transaciton, name='ignore_transaciton'),
]
