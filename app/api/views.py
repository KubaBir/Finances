from core.views import Transaction
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

from .serializers import CustomTransactionSerializer, TransactionSerializer


class UpdateTransactionStatusView(RetrieveUpdateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.ignore)
        print(request.data)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            if instance.ignore == True:
                instance.ignore = False
            else:
                instance.ignore = True
            instance.save()
            return Response(serializer.data)


class CreateCustomTransactionView(CreateAPIView):
    serializer_class = CustomTransactionSerializer
    queryset = Transaction.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        booking_date=self.request.data['value_date'])
