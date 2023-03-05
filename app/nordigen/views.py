import calendar
import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from app.tasks import get_transactions

from .forms import FetchForm


def fetch_data(request):
    if request.method == 'POST':
        form = FetchForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data.get('month', None)
            year = form.cleaned_data.get('year')
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
            get_transactions.delay(
                request.user.id, day, month, year, request.user.nordigen_user_id, by_month)
            return redirect("core:home")
        messages.error(request, "Wrong month or year.")
        return redirect("core:home")
    form = FetchForm()
    return render(request, 'nordigen/fetch.html', context={'form': form})
