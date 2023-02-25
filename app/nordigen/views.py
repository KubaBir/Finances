import calendar
import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from app.tasks import get_transactions_by_month

from .forms import FetchForm


def fetch_data(request):
    if request.method == 'POST':
        form = FetchForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data.get('month')
            year = form.cleaned_data.get('year')
            today = datetime.date.today()
            if today.year == year and today.month == month:
                day = today.day
            else:
                day = calendar.monthrange(year, month)[1]
            get_transactions_by_month.delay(
                request.user.id, day, month, year, request.user.nordigen_user_id)
            return redirect("core:home")
        messages.error(request, "Error")
        return render(request, 'nordigen/fetch.html', {'form': form})
    form = FetchForm()
    return render(request, 'nordigen/fetch.html', context={'form': form})
