from django.urls import path

from .views import CreateCustomTransactionView, UpdateTransactionStatusView, ReportView, FetchTransactionsView
from . import views
app_name = 'api'

urlpatterns = [
    path('transaction/<id>', UpdateTransactionStatusView.as_view(), name='transaction'),
    path('report/<date>', ReportView.as_view(), name='report'),
    path('fetch/', FetchTransactionsView.as_view(), name='fetch'),
    path('create_custom/',
         CreateCustomTransactionView.as_view(), name='create_custom'),
    path('token/', views.CreateTokenView.as_view(), name='token'),

]
