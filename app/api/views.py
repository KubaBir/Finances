from core.views import Transaction, MonthlyReport
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
import datetime
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


import calendar
from app.tasks import get_transactions
from .serializers import CustomTransactionSerializer, TransactionSerializer, ReportSerializer, MonthSelectSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken


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


class ReportView(RetrieveAPIView):
    serializer_class = ReportSerializer
    queryset = MonthlyReport.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = 'date'

    def get_object(self):
        date = self.kwargs.get('date')
        obj = MonthlyReport.objects.filter(
            user=self.request.user, date=date).get()
        if obj:
            return obj
        else:
            return Response({"detail": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class FetchTransactionsView(GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        return MonthSelectSerializer(*args, **kwargs)

    def post(self, request, format=None):
        serializer = MonthSelectSerializer(data=request.data)
        if serializer.is_valid():
            month = serializer.data.get('month')
            year = serializer.data.get('year')
            today = datetime.date.today()
            by_month = True

            if month is None:
                by_month = False
                if year == today.year:
                    month = today.month
                else:
                    month = 12

            if today.year == year and today.month == month:
                day = today.day
            else:
                day = calendar.monthrange(year, month)[1]
            get_transactions(
                request.user.id, day, month, year, 0, by_month)

            return Response({'status': 'successs'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
