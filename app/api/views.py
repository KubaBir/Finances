from rest_framework.generics import RetrieveUpdateAPIView
from core.views import Transaction
from .serializers import TransactionSerializer
from rest_framework.response import Response


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
