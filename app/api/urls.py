from django.urls import path

from .views import CreateCustomTransactionView, UpdateTransactionStatusView

app_name = 'api'

urlpatterns = [
    path('transaction/<id>', UpdateTransactionStatusView.as_view(), name='transaction'),
    path('create_custom/',
         CreateCustomTransactionView.as_view(), name='create_custom'),
]
