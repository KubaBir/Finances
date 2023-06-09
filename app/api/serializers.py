from core.models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    change_ignore = serializers.BooleanField(default=False, required=False)
    change_type = serializers.BooleanField(default=False, required=False)
    debtor_name = serializers.CharField(required=False)

    class Meta:
        model = Transaction
        fields = ['id', 'change_ignore', 'change_type', 'debtor_name']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        if validated_data['change_ignore']:
            instance.ignore = not instance.ignore
        if validated_data['change_type']:
            if instance.value == 'IN':
                instance.value = 'RE'
            else:
                instance.value = 'IN'

        instance.save()
        instance.report.sync()
        return instance


class CustomTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['value_date', 'transaction_amount', 'debtor_name', 'info']
