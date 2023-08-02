from core.models import Transaction, MonthlyReport
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model


class TransactionSerializer(serializers.ModelSerializer):
    change_ignore = serializers.BooleanField(default=False, required=False)
    change_type = serializers.BooleanField(default=False, required=False)
    debtor_name = serializers.CharField(required=False)
    info = serializers.CharField(default="", required=False)

    class Meta:
        model = Transaction
        fields = ['id', 'change_ignore', 'change_type', 'debtor_name', 'info']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        print(validated_data)

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


class ReportSerializer(serializers.ModelSerializer):
    date = serializers.DateField()

    class Meta:
        model = MonthlyReport
        fields = ['date', 'total_spendings',
                  'total_income', 'number_of_transactions']
        # read_only_fields = ['total_spendings',
        #                     'total_income', 'number_of_transactions']


class MonthSelectSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    year = serializers.IntegerField()

    class Meta:
        fields = '__all__'


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authh token."""
    username = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        """Validate and auth the user."""
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password,
        )
        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
