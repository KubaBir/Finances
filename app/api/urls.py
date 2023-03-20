from .views import UpdateTransactionStatusView
from django.urls import path

app_name = 'api'

urlpatterns = [
    path('transaction/<id>', UpdateTransactionStatusView.as_view(), name='transaction'),
]
