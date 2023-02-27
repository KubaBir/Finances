import calendar
import datetime
import json
import os
from os import environ

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from core.models import MonthlyReport, Transaction
from django.contrib.auth import get_user_model
from django.db import models

from app.settings import BASE_DIR

logger = get_task_logger(__name__)


@shared_task
def get_transactions_by_month(id, day, month, year, user_id):
    print(f"Got fetch request for {day}-{month}-{year}")
    url = "https://ob.nordigen.com/api/v2/token/new/"
    payload = f"secret_id={environ['SECRET_ID']}&secret_key={environ['SECRET_KEY']}"

    res = requests.request("POST", url, headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'},
        data=payload)

    token = res.json().get('access', False)

    date_from = str(year) + '-' + str(month) + '-01'
    date_to = str(year) + '-' + str(month) + '-' + \
        str(day)

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

    # file_path = os.path.join(BASE_DIR, 'result.json')
    # f = open(file_path)
    # data = json.load(f)['booked']
    # f.close()

    for transaction in data:
        if transaction.get('debtorName'):
            info = transaction.get('remittanceInformationUnstructured', "")
        else:
            info = ""

        booking_date = datetime.datetime.strptime(
            transaction.get('bookingDate'), "%Y-%m-%d").date()
        value_date = datetime.datetime.strptime(
            transaction.get('valueDate'), "%Y-%m-%d").date()

        values = {
            'user': get_user_model().objects.get(id=id),
            'booking_date': booking_date,
            'value_date': value_date,
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

    # Update stats on monthly reports
    for report in MonthlyReport.objects.all():
        returned = Transaction.objects.filter(
            report=report, value='RE').aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0
        spent = Transaction.objects.filter(
            report=report, value='SP').aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0
        report.total_spendings = returned - spent

        report.total_income = Transaction.objects.filter(
            report=report, value='IN').aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0
        report.number_of_transactions = Transaction.objects.filter(
            report=report).aggregate(models.Count('transaction_amount'))['transaction_amount__count'] or 0
    report.save()

    return True
