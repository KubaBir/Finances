from django.contrib import admin

from .models import MonthlyReport, Transaction, User

admin.site.register(User)
admin.site.register(MonthlyReport)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('debtor_name', 'info', 'transaction_amount', 'month_year')

    def get_ordering(self, request):
        return ['-value_date']


admin.site.register(Transaction, TransactionAdmin)
