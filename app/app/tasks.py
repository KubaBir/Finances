import calendar
import datetime
from os import environ

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from core.models import Transaction
from django.contrib.auth import get_user_model
from django.db.models import Q

logger = get_task_logger(__name__)


@shared_task
def get_transactions_by_month(month, year, user_id):
    url = "https://ob.nordigen.com/api/v2/token/new/"
    payload = f"secret_id={environ['SECRET_ID']}&secret_key={environ['SECRET_KEY']}"

    res = requests.request("POST", url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'},
        data=payload)

    token = res.json().get('access', False)

    date_from = str(year) + '-' + str(month) + '-01'
    date_to = str(year) + '-' + str(month) + '-' + \
        str(calendar.monthrange(year, month)[1])

    user_id = "8cf965fa-6ed0-494d-ad5c-cfa5f660ee55"

    url = f"https://ob.nordigen.com/api/v2/accounts/{user_id}/transactions/?date_from={date_from}&date_to={date_to}"

    res = requests.request("GET", url, headers={
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'},
        data={})

    if res.status_code != 200:
        print("Status code: ", res.status_code, res.text)
        return False
    data = res.json()['transactions']['booked']

    for transaction in data:
        if transaction.get('debtorName'):
            info = transaction.get('remittanceInformationUnstructured', "")
        else:
            info = ""

        values = {
            'booking_date': transaction.get('bookingDate'),
            'value_date': transaction.get('valueDate'),
            'transaction_amount': float(transaction.get(
                'transactionAmount')['amount']),
            'debtor_name': transaction.get('debtorName', transaction.get(
                'remittanceInformationUnstructured')),
            'info': info
        }

        Transaction.objects.update_or_create(
            id=transaction.get('transactionId'),
            defaults=values
        )
    return
