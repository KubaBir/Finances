from core.views import Transaction
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .serializers import CustomTransactionSerializer, TransactionSerializer


class UpdateTransactionStatusView(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        report = instance.report
        self.perform_destroy(instance)
        report.sync()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCustomTransactionView(CreateAPIView):
    serializer_class = CustomTransactionSerializer
    queryset = Transaction.objects.all()

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user,
                              booking_date=self.request.data['value_date'])
        obj.report.sync()
