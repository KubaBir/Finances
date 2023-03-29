from core.views import Transaction
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .serializers import CustomTransactionSerializer, TransactionSerializer


class UpdateTransactionStatusView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_field = 'id'


class CreateCustomTransactionView(CreateAPIView):
    serializer_class = CustomTransactionSerializer
    queryset = Transaction.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        booking_date=self.request.data['value_date'])
