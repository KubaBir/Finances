import datetime

from django import forms
from django.core.exceptions import ValidationError


class FetchForm(forms.Form):
    today = datetime.date.today()
    month = forms.IntegerField(required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '#', 'value': today.month}))
    year = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '#', 'value': today.year}))

    def clean_month(self):
        today = datetime.date.today()
        month = self.cleaned_data.get('month', None)
        if month is None:
            return month
        year = self.cleaned_data.get('year')
        if month > 12 or month <= 0 or (year == today.year and month > today.month):
            raise ValidationError("The month is not valid!")

        return month

    def clean_year(self):
        today = datetime.date.today()
        year = self.cleaned_data['year']
        if year > today.year:
            raise ValidationError("The year is not valid")

        return year
