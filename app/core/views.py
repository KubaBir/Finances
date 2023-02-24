from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.tasks import get_transactions_by_month

from .models import MonthlyReport

# Create your views here.


def main_page(request):
    return render(request, 'core/home.html')


@login_required()
def fetch_transactions(request):
    # get_transactions_by_month.delay(
    #     request.user.id, 1, 2023, "8cf965fa-6ed0-494d-ad5c-cfa5f660ee55")
    get_transactions_by_month(
        request.user.id, 1, 2023, "8cf965fa-6ed0-494d-ad5c-cfa5f660ee55")
    return render(request, 'core/home.html')
