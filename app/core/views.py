import datetime
import json
import os
from calendar import monthrange

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import models
from django.shortcuts import HttpResponse, redirect, render

from app.settings import BASE_DIR
from app.tasks import get_transactions

from .models import MonthlyReport, Transaction

# Create your views here.


def main_page(request):
    return redirect('core:dashboard')


@login_required()
def dashboard(request):
    date = datetime.date(datetime.date.today().year,
                         datetime.date.today().month, 1)
    report_list = MonthlyReport.objects.filter(
        user=request.user).order_by('-date')
    latest, created = MonthlyReport.objects.get_or_create(
        date=date, user=request.user)
    return render(request, 'core/dashboard.html', context={'report_list': report_list, 'latest': latest})


@login_required()
def fetch_transactions(request):
    # get_transactions_by_month.delay(
    #     request.user.id, 1, 2023, "8cf965fa-6ed0-494d-ad5c-cfa5f660ee55")
    file_path = os.path.join(BASE_DIR, 'result.json')
    f = open(file_path)
    data = json.load(f)['booked']
    f.close()

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
            'user': get_user_model().objects.get(id=request.user.id),
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
        report.total_spendings = Transaction.objects.filter(
            report=report, transaction_amount__lt=0).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0
        report.total_income = Transaction.objects.filter(
            report=report, transaction_amount__gte=0).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0
        report.number_of_transactions = Transaction.objects.filter(
            report=report).aggregate(models.Count('transaction_amount'))['transaction_amount__count'] or 0
        report.save()
    return render(request, 'core/home.html')


@login_required()
def overview(request, id=None):
    report = MonthlyReport.objects.get(id=id)
    if report.previous is not None:
        spendings_bar = report.total_spendings / \
            (report.previous.total_spendings + 1) * 100
        income_bar = report.total_income / \
            (report.previous.total_income + 1) * 100
        transactions_bar = report.number_of_transactions / \
            (report.previous.number_of_transactions + 1) * 100
    else:
        spendings_bar = 100
        income_bar = 100
        transactions_bar = 100

    outgoing = Transaction.objects.filter(
        value='SP', report=report).order_by('-value_date', 'debtor_name')
    income = Transaction.objects.filter(
        value='IN', report=report).order_by('-value_date', 'debtor_name')
    returns = Transaction.objects.filter(
        value='RE', report=report).order_by('-value_date', 'debtor_name')

    report_spendings = -round(Transaction.objects.filter(
        models.Q(value='SP') | models.Q(value='RE'),
        report=report,
        ignore=False,
    ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2)

    categories = {
        'groceries': -round(Transaction.objects.filter(
            ignore=False,
            value='SP',
            category='Groceries',
            report=report
        ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2),
        'food': -round(Transaction.objects.filter(
            ignore=False,
            value='SP',
            category='Food',
            report=report
        ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2),
        'groceries': -round(Transaction.objects.filter(
            ignore=False,
            value='SP',
            category='Groceries',
            report=report
        ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2),
        'travel': -round(Transaction.objects.filter(
            ignore=False,
            value='SP',
            category='Travel',
            report=report
        ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2),
        'clothing': -round(Transaction.objects.filter(
            ignore=False,
            value='SP',
            category='Clothing',
            report=report
        ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2),
        'transfers': -round(Transaction.objects.filter(
            ignore=False,
            value='SP',
            category='Transfers',
            report=report
        ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2),
        'entertainment': -round(Transaction.objects.filter(
            ignore=False,
            value='SP',
            category='Entertainment',
            report=report
        ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2),
        'other': -round(Transaction.objects.filter(
            ignore=False,
            value='SP',
            category='Other',
            report=report
        ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2),
    }

    dates = [report.date + datetime.timedelta(days=x) for x in range(
        monthrange(report.date.year, report.date.month)[1])]
    daily_spendings = []
    for i, date in enumerate(dates):
        daily_spendings.append(-round(Transaction.objects.filter(
            user=request.user,
            value='SP',
            report=report,
            value_date=date,
            ignore=False
        ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0, 2))
    timeline = []
    for i in range(0, len(daily_spendings), 3):
        timeline.append(sum(daily_spendings[i:i+3]))

    context = {
        'income': income,
        'returns': returns,
        'outgoing': outgoing,
        'report': report,
        'spendings_bar': spendings_bar,
        'income_bar': income_bar,
        'transactions_bar': transactions_bar,
        'report_spendings': report_spendings,
        'categories': categories,
        'timeline': timeline
    }

    return render(request, 'core/overview.html', context=context)


def update_report(id):
    transaction = Transaction.objects.get(id=id)
    report = transaction.report

    report.total_spendings = round(-Transaction.objects.filter(
        models.Q(value='SP') | models.Q(value='RE'),
        report=report
    ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'], 2)

    report.total_income = Transaction.objects.filter(
        report=report,
        value='IN'
    ).aggregate(models.Sum('transaction_amount'))['transaction_amount__sum'] or 0

    report.number_of_transactions = Transaction.objects.filter(
        report=report
    ).aggregate(models.Count('transaction_amount'))['transaction_amount__count'] or 0

    report.save()
