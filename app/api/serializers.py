from core.models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'ignore']
        read_only_fields = ['ignore']


class CustomTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['value_date', 'transaction_amount', 'debtor_name', 'info']
