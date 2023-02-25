from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.tasks import get_transactions_by_month

from .models import MonthlyReport, Transaction

# Create your views here.


def main_page(request):
    return redirect('core:dashboard')


@login_required()
def dashboard(request):
    report_list = MonthlyReport.objects.filter(
        user=request.user).order_by('-year')
    return render(request, 'core/dashboard.html', context={'report_list': report_list})


@login_required()
def fetch_transactions(request):
    # get_transactions_by_month.delay(
    #     request.user.id, 1, 2023, "8cf965fa-6ed0-494d-ad5c-cfa5f660ee55")
    get_transactions_by_month(
        request.user.id, 28, 1, 2023, "8cf965fa-6ed0-494d-ad5c-cfa5f660ee55")
    return render(request, 'core/home.html')


@login_required()
def overview(request, id=None):
    report = MonthlyReport.objects.get(id=id)
    incoming = Transaction.objects.filter(
        transaction_amount__gte=0, report=report).order_by('-value_date')
    outgoing = Transaction.objects.filter(
        transaction_amount__lt=0, report=report).order_by('-value_date')

    return render(request, 'core/overview.html', context={'outgoing': outgoing, 'incoming': incoming, 'report': report})
