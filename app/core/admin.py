from django.contrib import admin

from .models import MonthlyReport, Transaction, User

admin.site.register(User)


class ReportAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(MonthlyReport, ReportAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('debtor_name', 'info', 'transaction_amount', 'month_year')
    readonly_fields = ('id',)

    def get_ordering(self, request):
        return ['-value_date']


admin.site.register(Transaction, TransactionAdmin)
